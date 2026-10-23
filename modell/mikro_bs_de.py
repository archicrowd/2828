#!/usr/bin/env python3
"""Beamte und Selbständige für die Mikrosimulation Deutschland (Logbuch v4.28). Prüfrechnung; wird von modell/mikro_de.py geladen.

Bis v4.27 waren Haushalte mit Beamten und Selbständigen als Hauptverdiener herausgenommen. Hier werden sie als eigene Haushalte gezogen
(Gewichte: Zahl der Beamten bzw. Selbständigen, Annahme: eine Hauptperson je Haushalt), Partner und Kinder wie bei Beschäftigten.

heute (Recht 2026):
  Beamte: Besoldung, keine Sozialbeiträge, private Krankenversicherung zur Beihilfe (Annahme zur Höhe, zu 80 % abziehbar).
  Selbständige: Gewinn, freiwillige Kranken- und Pflegeversicherung (Satz, Mindestbemessung), keine Rentenversicherung (Annahme).
neu (Stand C):
  Beamte: keine Weitergabe der Ersparnis des Dienstherrn (Beschluss 23.10.2026); Versicherungszulage (Vorschlag): Pflichtvorsorge 10 % der
          Bezüge und Zuschuss zur Zusatzversicherung, beides steuerpflichtig; keine Beiträge; Pflichtvorsorge 10 % wie alle.
  Selbständige: Gewinn nach 33R, keine Beiträge, Pflichtvorsorge 10 % des Gewinns (Annahme: gilt für alle Erwerbseinkommen).
Selbständige: Nettoeinkommen aus dem WSI-Erwerbspersonenpanel (Lognormal über drei Klassengrenzen), Gewinn in mikro_de zurückgerechnet.
"""
import math
import tomllib
from pathlib import Path

import numpy as np
from scipy.stats import norm

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "mikro_bs_de.toml").read_text(encoding="utf-8"))
TYPEN = ("allein", "paar_ohne", "paar_mit")


def selbst_lognormal():
    """mu, sigma des persönlichen Nettoeinkommens (Monat) aus den gewichteten Klassenanteilen (Kleinste Quadrate auf z-Werten)."""
    S = P["selbst"]
    a = [S["anteil_solo"] * x + (1 - S["anteil_solo"]) * y for x, y in zip(S["anteile_solo"], S["anteile_arbeitgeber"])]
    kum = np.cumsum(a)[:3]
    z = norm.ppf(kum)
    x = np.log(S["grenzen_monat"])
    sigma, mu = np.polyfit(z, x, 1)
    return float(mu), float(sigma), [round(float(k), 3) for k in kum]


def beihilfe_je_beamter():
    B = P["beamte"]
    return B["beihilfe_mrd_2024"] * 1e9 * B["anteil_aktive"] / (B["anzahl_mio"] * 1e6)


def pkv(n_partner_ohne, kinder):
    B = P["beamte"]
    return B["pkv_person"] + B["pkv_partner_ohne_einkommen"] * n_partner_ohne + B["pkv_kind"] * kinder


def zulage(b, variante):
    """Jahresbetrag der Zulage zur Besoldung b (steuerpflichtig)."""
    Z = P["beamte"]["zulage"]
    if variante == "ohne":
        return 0.0
    if variante == "weitergabe_20":
        return 0.2 * beihilfe_je_beamter()
    z = Z["vorsorge_satz"] * b
    if variante == "vorsorge_gesundheit":
        z += 12 * Z["gesundheit_monat"]
    return z


def ziehe(rng, n, lohn_quantile, kinderzahl_anteile, faktor_2025_2024):
    """Haushalte mit Beamten bzw. Selbständigen als Hauptperson. lohn_quantile: dict art → Quantilfunktion (2024) für Partner."""
    H = P["haushalt"]
    mu_s, sig_s, _ = selbst_lognormal()
    B = P["beamte"]
    anteil_b = B["anzahl_mio"] / (B["anzahl_mio"] + P["selbst"]["anzahl_mio"])
    out = []
    typ = rng.choice(3, size=n, p=[H["typ_anteile"][t] for t in TYPEN])
    for i in range(n):
        t = TYPEN[typ[i]]
        beamt = rng.random() < anteil_b
        if beamt:
            b = float(np.exp(math.log(B["brutto_mittel_2025"] / faktor_2025_2024) - B["streuung_log"] ** 2 / 2 + B["streuung_log"] * rng.standard_normal()))
            haupt = (b, "beamt")
        else:
            netto_monat = float(np.exp(mu_s + sig_s * rng.standard_normal()))
            haupt = (netto_monat * 12, "selbst_netto")          # in mikro_de in Gewinn umgerechnet
        erw = [haupt]
        if t != "allein":
            art = ("vz", "tz", "mini", "ohne")[rng.choice(4, p=H["partner_status"])]
            erw.append((float(lohn_quantile[art](np.array([rng.random()]))[0]) if art != "ohne" else 0.0, art))
        k = int(rng.choice([1, 2, 3, 4], p=kinderzahl_anteile)) if t == "paar_mit" else 0
        out.append(dict(typ=t, erw=erw, kind=k, vkind=None, paar=t != "allein", bg=False, bs="beamt" if beamt else "selbst"))
    gew_b = B["anzahl_mio"] * 1e6 / max(1, sum(h["bs"] == "beamt" for h in out))
    gew_s = P["selbst"]["anzahl_mio"] * 1e6 / max(1, sum(h["bs"] == "selbst" for h in out))
    return out, np.array([gew_b if h["bs"] == "beamt" else gew_s for h in out])
