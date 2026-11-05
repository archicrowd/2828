#!/usr/bin/env python3
"""Rentnerhaushalte für die Mikrosimulation Deutschland, Stufe 2 (Logbuch v4.23). Prüfrechnung; wird von modell/mikro_de.py geladen.

Anlass: v4.22 zog Renten je Rente (DRV-Zahlbetrag) und setzte daraus Haushalte zusammen. Partnereinkommen, Hinterbliebenen-, Betriebs- und
Beamtenrenten fehlten; die Grundsicherung im Alter war mit 10,5 Mio. Fällen statt 0,76 Mio. weit überschätzt (Validierung nicht bestanden).

Neu:
  1. Haushaltseinkommen statt Renten: äquivalenzgewichtetes Nettoeinkommen der Personen ab 65 aus EU-SILC 2025 (Eurostat ilc_di03 Median
     und Mittel, ilc_li02 Anteile unter 40/50/60/70 % des Gesamtmedians); zwischen den Stützstellen linear, über dem Median lognormal,
     Streuung so, dass das Mittel getroffen wird. Allein lebende und Paare um einen Faktor verschoben, der die Armutsgefährdungsquoten je
     Haushaltstyp (ilc_li03: 30,0 / 14,3 %) trifft.
  2. Zerlegung in Einkommensarten nach dem Alterssicherungsbericht 2024 (ASID 2023): GRV 53 %, andere Systeme 17 %, Betriebsrente 7 %,
     privat 9 %, Erwerb 13 % des Bruttoeinkommens (Annahme: gleiche Anteile über alle Einkommen; Variante „nur GRV“ als Schranke).
     Das Bruttoeinkommen wird so bestimmt, dass das Netto nach Recht 2026 dem gezogenen Netto entspricht.
  3. heute: Netto wie gezogen; Variante „voll“ mit Grundsicherung für alle Berechtigten, Variante „beobachtet“ ohne Aufstockung.
     neu: Renten aus GRV und anderen Systemen um 7,5 % gekürzt, keine Krankenversicherungsbeiträge, alles nach 33R steuerpflichtig,
     Mehrwertsteuer und Zuschlag wie rentnerausgleich, keine zusätzliche Dividende; Grundauskommen je Haushalt (Skala 1 / 1,5), volle Anrechnung.
"""
import contextlib
import importlib.util
import io
import math
import tomllib
from pathlib import Path

import numpy as np
from scipy.stats import norm

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "mikro_rentner_de.toml").read_text(encoding="utf-8"))


def _lade(name, pfad):
    spec = importlib.util.spec_from_file_location(name, W / pfad)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


RA = _lade("ra_r", "modell/rentnerausgleich.py")
H = RA.H                       # haushalte33 (Parameter rentner_kv_pv, besteuerungsanteil)
K = H.K                        # Kernmodell (est_2026, soli_2026)
HL = RA.RB.SL.HL
DE = HL.LS["staaten"]["DE"]
GB = DE["grundbedarf_jahr_eur"]
EFF = HL.EFF_NEU[2028]
ZU = RA.P["zuschlag_pct"]
S = P["silc"]
AB = P["abgaben_heute"]
ANTEILE = {k: P["asid"][k] for k in ("grv", "andere", "bav", "privat", "erwerb")}
NUR_GRV = dict(grv=1.0, andere=0.0, bav=0.0, privat=0.0, erwerb=0.0)


# ------------------------------------------------------------------ Verteilung (EU-SILC)
def _stuetz():
    m = S["median_gesamt"]
    pk = sorted((v, int(k) / 100 * m) for k, v in S["unter_schwelle"].items())
    return [(0.0, 0.2 * m)] + pk + [(0.5, S["median_65"])]          # Untergrenze 20 % des Medians (Annahme)


def _sigma():
    pk = _stuetz()
    u = (np.arange(100000) + 0.5) / 200000                            # 0 … 0,5
    unten = np.interp(u, [a for a, _ in pk], [b for _, b in pk]).mean() * 0.5
    lo, hi = 0.05, 1.5
    t = 0.5 + (np.arange(100000) + 0.5) / 200000
    for _ in range(60):
        s = (lo + hi) / 2
        oben = (S["median_65"] * np.exp(s * norm.ppf(t))).mean() * 0.5
        lo, hi = (lo, s) if unten + oben > S["mittel_65"] else (s, hi)
    return (lo + hi) / 2


SIGMA = _sigma()


def quantil(u):
    u = np.asarray(u, float)
    pk = _stuetz()
    out = np.interp(u, [a for a, _ in pk], [b for _, b in pk])
    o = u > 0.5
    out[o] = S["median_65"] * np.exp(SIGMA * norm.ppf(np.clip(u[o], 0.5, 1 - 1e-7)))
    return out


def _u_von(y):
    g = (np.arange(200000) + 0.5) / 200000
    return float(np.interp(y, quantil(g), g))


SCHWELLE60 = 0.6 * S["median_gesamt"]
FAKTOR = {"rentner_allein": SCHWELLE60 / float(quantil([S["quote60_allein"]])[0]), "rentner_paar": SCHWELLE60 / float(quantil([S["quote60_paar"]])[0])}


# ------------------------------------------------------------------ heute (Recht 2026) je Person
def netto_heute_person(g, a):
    p, an, b, v, e = (g * a[k] for k in ("grv", "andere", "bav", "privat", "erwerb"))
    kv = H.P["rentner_kv_pv"] * p + AB["kv_andere"] * an + AB["kv_bav"] * b + AB["kv_erwerb"] * e
    steuerbar = H.P["besteuerungsanteil"] * p + an + b + AB["ertragsanteil_privat"] * v + max(0.0, e - K.WK_PAUSCH)
    zve = max(0.0, steuerbar - 102 * (p + an + b > 0) - K.SA_PAUSCH - kv)
    est = K.est_2026(zve)
    return g - kv - est - K.soli_2026(est)


def brutto_aus_netto(n_person, a):
    lo, hi = 0.0, max(1000.0, 4 * n_person)
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if netto_heute_person(m, a) < n_person else (lo, m)
    return (lo + hi) / 2


# ------------------------------------------------------------------ neu je Haushalt
def neu_haushalt(g_person, n_pers, a, w, eps=0.0):
    p, an, b, v, e = (g_person * a[x] for x in ("grv", "andere", "bav", "privat", "erwerb"))
    # v4.72 Regel BS35 (haushalte33.rente_regel) auf die Zusagen, Versicherungsjahre zugeschätzt (Annahme); eigene Vorsorge ungekürzt
    eink = H.kuerze(p + an, jahre=H.jahre_zu(p + an, eps)) + b + v + e + w * H.ag(e)
    st = HL.stufen(eink, DE["tarif_stufen"], [0.0, 11.0, 19.0, 25.0, 33.0]) * n_pers
    y = eink * n_pers - st
    konsum = HL.kq(y, "DE") * y
    fm, fb = HL.mwst_phi("DE", y)                                                       # v4.29
    y = y - fm * konsum * ((1 + EFF / 100) / (1 + HL.eff_alt("DE") / 100) - 1) - ZU / 100 * (st + fb * konsum * EFF / (100 + EFF))
    boden = 12 * P["neu"]["boden_monat"][n_pers - 1]                 # v4.26: heutige Grundsicherung (vorher Grundbedarf × 1 / 1,5)
    return max(y, boden), max(0.0, boden - y)


def bedarf_heute(n_pers):
    return 12 * (AB["bedarf_allein_monat"] if n_pers == 1 else AB["bedarf_paar_monat"])


# ------------------------------------------------------------------ Ziehung
def ziehe(rng, n, personen_mio, allein_mio):
    """Rentnerhaushalte mit Gewicht (Haushalte), Typ, Personen, Netto heute (2024, nominal), Brutto je Person (ASID / nur GRV)."""
    p_allein = allein_mio / (allein_mio + (personen_mio - allein_mio) / 2)
    allein = rng.random(n) < p_allein
    u = rng.random(n)
    out = []
    for i in range(n):
        typ = "rentner_allein" if allein[i] else "rentner_paar"
        npers = 1 if allein[i] else 2
        y_aeq = float(quantil([u[i]])[0]) * FAKTOR[typ]
        netto = y_aeq * (1 + 0.5 * (npers - 1))
        out.append(dict(typ=typ, n=npers, netto_2024=netto))
    eps = np.random.default_rng(H.P["rente_jahre"]["seed"]).standard_normal(n)     # v4.72: Zufallszahl der Versicherungsjahre (eigener Strom)
    for i, r in enumerate(out):
        r["eps"] = float(eps[i])
    na = int(allein.sum())
    gew = np.where(allein, allein_mio * 1e6 / max(na, 1), (personen_mio - allein_mio) * 1e6 / 2 / max(n - na, 1))
    return out, gew


def rechne(r, faktor, w, variante="asid", inanspruchnahme="voll"):
    """heute, neu, Aufstockung neu, Grundsicherung heute (Betrag) für einen Haushalt; Euro mit faktor (Kaufkraft 2026) hochgerechnet."""
    a = ANTEILE if variante == "asid" else NUR_GRV
    n_haus = r["netto_2024"] * faktor
    g = brutto_aus_netto(n_haus / r["n"], a)
    bed = bedarf_heute(r["n"])
    gs = max(0.0, bed - n_haus) if inanspruchnahme == "voll" else 0.0
    neu, auf = neu_haushalt(g, r["n"], a, w, r.get("eps", 0.0))
    return n_haus + gs, neu, auf, gs, g


def pruefwerte(rentner, gew, faktor_2023):
    """Nicht geeichte Vergleichswerte: Paar-Mittel/Median (ilc_di04), Netto je Haushalt (ASID 2023), Personen unter dem Grundsicherungsbedarf."""
    y = np.array([r["netto_2024"] for r in rentner])
    paar = np.array([r["typ"] == "rentner_paar" for r in rentner])
    aeq = y / np.where(paar, 1.5, 1.0)

    def med(x, w):
        o = np.argsort(x)
        c = np.cumsum(w[o])
        return float(x[o][np.searchsorted(c, c[-1] / 2)])
    pers = gew * np.where(paar, 2, 1)
    unter = np.array([r["netto_2024"] < bedarf_heute(r["n"]) / 1.06 for r in rentner])    # Bedarf 2026 auf 2024 zurück (Annahme 1,06)
    grv = np.array([brutto_aus_netto(r["netto_2024"] / r["n"], ANTEILE) * ANTEILE["grv"] * r["n"] for r in rentner])   # je Haushalt
    return dict(
        paar_aequiv=dict(modell_mittel=round(float((aeq[paar] * gew[paar]).sum() / gew[paar].sum())), modell_median=round(med(aeq[paar], gew[paar])),
                         silc_mittel=S["paar_mittel"], silc_median=S["paar_median"], hinweis="ilc_di04 A2_GE1_GE65, nicht geeicht (enthält Paare mit nur einer Person ab 65)"),
        netto_haushalt_monat=dict(modell_2024=round(float((y * gew).sum() / gew.sum() / 12)), modell_auf_2023=round(float((y * gew).sum() / gew.sum() / 12 / faktor_2023)),
                                  asid_2023=P["asid"]["netto_haushalt_monat_2023"], hinweis="ASID: Haushalte ab 65, Abgrenzung abweichend; Rückrechnung 2024→2023 mit Rentenanpassung (Annahme)"),
        unter_grundsicherungsbedarf_personen_mio=round(float((pers * unter).sum() / 1e6), 2),
        grundsicherung_alter_empfaenger_mio=P["pruefung"]["grundsicherung_alter_empfaenger_mio"],
        grv_brutto_je_person_monat_2024=round(float((grv * gew).sum() / pers.sum() / 12)),
        aequiv_unter_60_pct=round(float((pers * (aeq < SCHWELLE60)).sum() / pers.sum() * 100), 1),
        aequiv_unter_60_silc_pct=S["unter_schwelle"]["60"] * 100,
        sigma_ueber_median=round(SIGMA, 4), faktor_typ={k: round(v, 4) for k, v in FAKTOR.items()})
