#!/usr/bin/env python3
"""Benannte Kennzahlen des Rahmenmodells (Stand B), berechnet aus den Originalskripten in modell/rahmen/.

Zweck: Jede Aussage des Gesamtkonzepts (dokumente/aussagen.csv) verweist auf einen Schlüssel aus diesem
Wörterbuch. So lässt sich bei einer Änderung an Parametern oder Skripten prüfen, welche Aussagen betroffen sind
(modell/pruefe_aussagen.py). Es wird nichts neu erfunden: die Formeln stehen in basis.py, final.py und
tilgung.py; hier werden nur deren Ergebnisse unter Namen abgelegt und die Formeln aus pfad.py, zahlen.py und
aufschlag.py nachgezogen (dort stehen sie im Skriptkörper, nicht in Funktionen).

Aufruf:  python3 modell/kennzahlen.py        (schreibt daten/aggregate/kennzahlen.csv)
Import:  from kennzahlen import kennzahlen; W = kennzahlen()
"""
import contextlib
import csv
import io
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
RAHMEN = WURZEL / "modell" / "rahmen"

LAENDER = ("FR", "BE", "ES", "AT", "SI", "DE", "EE", "NL", "DK", "IE")


def _importiere():
    """Importiert die Originalskripte mit Unterdrückung ihrer Ausgabe. Der Pfad modell/rahmen wird nur
    für die Dauer des Imports an den Anfang gestellt, damit modell/pfad.py (Zweitrechnung) nicht kollidiert."""
    alt = list(sys.path)
    sys.path.insert(0, str(RAHMEN))
    for name in ("basis", "final", "tilgung", "pfad"):
        sys.modules.pop(name, None)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import basis
            import final
            import tilgung
    finally:
        sys.path[:] = alt
    return basis, final, tilgung


def kennzahlen() -> dict:
    basis, final, tilgung = _importiere()
    W: dict[str, float] = {}

    # --- Basis 2028 (basis.py) ---
    W["bip24_klub_mrd"] = basis.BIP24_KLUB
    W["faktor_2024_2028"] = basis.F2428
    W["bip28_klub_mrd"] = basis.BIP28_KLUB
    W["bip28_de_mrd"] = basis.BIP28_DE
    W["pop_klub_mio"] = basis.POP_KLUB / 1e6
    W["kopf_klub_eur"] = basis.KOPF_KLUB
    W["kopf_de_eur"] = basis.KOPF_DE
    W["verhaeltnis_de_klub"] = basis.KOPF_DE / basis.KOPF_KLUB
    W["de_ueber_klub_pct"] = (basis.KOPF_DE / basis.KOPF_KLUB - 1) * 100
    W["de_anteil_klub_bip_pct"] = basis.GDP["DE"] / sum(basis.GDP.values()) * 100
    W["schuldenquote_klub_pct"] = basis.D_START
    W["klub_bip_alt_14227_abweichung_pct"] = (14227 / basis.BIP28_KLUB - 1) * 100

    # --- Struktur und Einzug 2028 (final.py, Konstanten) ---
    q, boden, b = final.QUOTE, final.BODEN, final.B_AUFG
    W["quote_pct"] = q
    W["a_summe_pct"] = final.A_SUM
    W["b_fachaufgaben_pct"] = b
    W["a_zieht_ein_pct"] = q - boden
    W["boden_pct"] = boden
    P = final.pfad()
    p0 = P[0]
    mx = max(P, key=lambda r: r["a"])
    W["a_2028_pct"] = p0["a"]
    W["b_verfuegt_2028_pct"] = q - p0["a"]
    W["dividende_2028_pct"] = p0["div"]
    W["a_hoechstbedarf_pct"] = mx["a"]
    W["a_hoechstbedarf_jahr"] = mx["jahr"]
    W["obergrenze_berechnet_pct_einzug"] = mx["a"] / (q - boden) * 100

    def kopf(pct: float) -> float:
        return pct / 100 * basis.KOPF_KLUB

    W["gesamtaufkommen_eur_kopf"] = kopf(q)
    W["a_zieht_ein_eur_kopf"] = kopf(q - boden)
    W["boden_eur_kopf"] = kopf(boden)
    W["a_behaelt_eur_kopf"] = kopf(p0["a"])
    W["b_verfuegt_eur_kopf"] = kopf(q - p0["a"])
    W["b_fachaufgaben_eur_kopf"] = kopf(b)
    W["b_dividende_eur_kopf"] = kopf(p0["div"])
    W["bodenabgabe_anteil_fachbudget_pct"] = boden / b * 100
    W["bodenabgabe_anteil_b_gesamt_pct"] = boden / (q - p0["a"]) * 100

    # --- Formel (zahlen.py) ---
    schule, kind_ant = final.SCHULE, final.KIND_ANT
    je_einw = (b - schule) / 100 * basis.KOPF_KLUB
    je_kind = schule / 100 * basis.KOPF_KLUB / kind_ant
    W["formel_je_einwohner_eur"] = je_einw
    W["formel_je_kind_eur"] = je_kind
    W["formel_fachbudget_kinder_12_eur"] = je_einw + je_kind * 0.12
    W["formel_fachbudget_kinder_schnitt_eur"] = je_einw + je_kind * kind_ant
    W["formel_fachbudget_kinder_20_eur"] = je_einw + je_kind * 0.20

    # --- Verwaltung (pfad.py) ---
    verw = 1.62
    W["verwaltung_anteil_b_pct"] = verw / b * 100
    W["verwaltung_ersparnis_punkte"] = verw - b * 0.058
    W["verwaltung_ersparnis_eur_monat"] = (verw - b * 0.058) / 100 * basis.KOPF_KLUB / 12

    # --- Zeitpfad (final.pfad) ---
    by = {r["jahr"]: r for r in P}
    for j in (2028, 2030, 2035, 2040, 2050, 2060):
        r = by[j]
        W[f"verteidigung_{j}_pct"] = r["v"]
        W[f"schuld_{j}_pct"] = r["d"]
        W[f"zinsdienst_{j}_pct"] = r["zd"]
        W[f"a_gesamt_{j}_pct"] = r["a"]
        W[f"dividende_{j}_pct"] = r["div"]
        W[f"klub_monat_{j}_eur"] = r["kl_real"]
        W[f"de_monat_real_{j}_eur"] = r["de_real"]
        W[f"de_monat_nominal_{j}_eur"] = r["de_nom"]
        W[f"de_monat_ohne_wachstum_{j}_eur"] = r["de_fix"]
    tief = min(P, key=lambda r: r["de_real"])
    W["de_tiefpunkt_eur"] = tief["de_real"]
    W["de_tiefpunkt_jahr"] = tief["jahr"]
    W["de_tiefpunkt_ueber_versprechen_pct"] = (tief["de_real"] / final.VERSPRECHEN - 1) * 100
    W["de_rueckgang_bis_tiefpunkt_pct"] = (tief["de_real"] / P[0]["de_real"] - 1) * 100
    W["de_anstieg_2060_gegen_2028_pct"] = (P[-1]["de_real"] / P[0]["de_real"] - 1) * 100
    W["dividendenanteil_aenderung_pct"] = (P[-1]["div"] / P[0]["div"] - 1) * 100
    W["reales_wachstum_je_kopf_pct"] = final.G_REAL * 100
    W["versprechen_de_eur"] = final.VERSPRECHEN

    # --- Mindestquote (Bisektion wie final.py) ---
    for schluessel, feld in (("streng", "de_fix"), ("zentral", "de_real")):
        lo, hi = 25.0, 40.0
        for _ in range(90):
            m = (lo + hi) / 2
            if min(r[feld] for r in final.pfad(m)) < final.VERSPRECHEN:
                lo = m
            else:
                hi = m
        W[f"mindestquote_{schluessel}_pct"] = (lo + hi) / 2

    # --- Gegenprobe Quote 27,91 % (altschuld.py) ---
    Q = final.pfad(27.91)
    unter = [r["jahr"] for r in Q if r["de_real"] < final.VERSPRECHEN]
    W["quote_2791_jahre_unter_versprechen"] = len(unter)
    W["quote_2791_letztes_jahr_unter_versprechen"] = unter[-1] if unter else 0

    # --- Sensitivität (tilgung.py: nominal an real gekoppelt) ---
    for g in (0.0, 0.005, 0.010, 0.015, 0.020):
        S = tilgung.pfad(0.0, g_nom=(1 + g) * 1.02 - 1, preis=0.020)
        tag = f"{int(round(g * 1000)):03d}"
        W[f"sens_{tag}_2035_eur"] = S[7]["eur"]
        W[f"sens_{tag}_2060_eur"] = S[32]["eur"]
        W[f"sens_{tag}_gegen_2028_pct"] = (S[32]["eur"] / S[0]["eur"] - 1) * 100

    # --- Aktive Tilgung (tilgung.py) ---
    O, M = tilgung.pfad(0.0), tilgung.pfad(0.50)
    W["tilgung_verzicht_startjahr_eur"] = O[0]["eur"] - M[0]["eur"]

    # --- Altschulden und Aufschlag (aufschlag.py) ---
    satz = 78.4 * 1.53 / 100
    F = 1.13535
    W["zinsdienst_start_pct_bip"] = satz
    W["zinsdienst_start_mrd"] = satz / 100 * basis.BIP28_KLUB
    pop_summe = sum(basis.POP.values())
    a_kopf = 9.04 / 100 * basis.BIP28_KLUB * 1e9 / pop_summe
    groesster = 0.0
    kopf_ie = 0.0
    for k in LAENDER:
        bip28 = basis.GDP[k] / 1000 * F
        kp = bip28 * 1e9 / basis.POP[k]
        aus = basis.SCHULD[k] / 100 * bip28 * 1.53 / 100 * 1e9 / basis.POP[k]
        ein = satz / 100 * kp
        W[f"zins_je_kopf_{k}_eur"] = aus
        W[f"beitrag_je_kopf_{k}_eur"] = ein
        W[f"aufschlag_{k}_eur"] = aus - ein
        groesster = max(groesster, abs(aus - ein))
        if k == "IE":
            kopf_ie = kp
    W["aufschlag_groesster_anteil_a_pct"] = groesster / a_kopf * 100
    W["irland_kopf_faktor"] = kopf_ie / (basis.BIP28_KLUB * 1e9 / pop_summe)
    W["a_einnahmen_anteil_schuld_pct"] = p0["a"] / basis.D_START * 100
    W["obergrenze_anteil_schuld_pct"] = 0.36 * (q - boden) / basis.D_START * 100

    # --- Last (Eingaben des Dokuments: heute 40,76, Gesundheit 7,75) ---
    W["entlastung_punkte"] = 40.76 - (q + 7.75)
    W["entlastung_mrd"] = (40.76 - (q + 7.75)) / 100 * basis.BIP28_KLUB
    W["gesamtlast_entwurf_pct"] = q + 7.75
    W["last_heute_summe_komponenten"] = 25.95 + 14.88  # Eingaben des Dokuments (Abschnitt 7)
    return W


def main() -> int:
    W = kennzahlen()
    ziel = WURZEL / "daten" / "aggregate" / "kennzahlen.csv"
    with ziel.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["schluessel", "wert"])
        for k, v in W.items():
            w.writerow([k, f"{v:.6f}"])
    print(f"{len(W)} Kennzahlen nach {ziel.relative_to(WURZEL)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
