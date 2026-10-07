#!/usr/bin/env python3
"""Vergleicht die Zweitrechnung (modell/pfad.py, modell/aufschlag.py) mit den Originalskripten
aus dem Vorchat (modell/rahmen/, Logbuch Band III, v3.8).

Die Originale rechnen mit festen Zahlen im Skript (Eurostat-Werte 2024, nicht an der Quelle geprüft).
Die Zweitrechnung liest modell/parameter.toml und daten/aggregate/laender_2024.csv. Stimmen beide
überein, ist das ein Beleg für die Rechenlogik, nicht für die Eingangsdaten.

Aufruf:  python3 modell/vergleich_original.py
Ausgabe: daten/aggregate/vergleich_original.csv
Rückgabe: 0 bei Übereinstimmung innerhalb der Toleranz, 2 sonst. Die Einwohnerzahlen sind
ausgenommen: sie weichen für acht Länder ab (bekannt, v3.8) und werden nur gemeldet.
"""
import contextlib
import csv
import io
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WURZEL / "modell" / "rahmen"))
sys.path.insert(0, str(WURZEL / "modell"))

with contextlib.redirect_stdout(io.StringIO()):  # basis.py druckt beim Import
    import basis  # noqa: E402
    import final  # noqa: E402

ZEILEN: list[list] = []
ABWEICHUNG = False


def melde(thema: str, groesse: str, original: float, zweit: float, tol: float, einheit: str,
          informativ: bool = False) -> None:
    """informativ: Abweichung wird gemeldet, bestimmt aber nicht den Rückgabewert (bekannte Datenabweichung)."""
    global ABWEICHUNG
    d = zweit - original
    ok = abs(d) <= tol
    ABWEICHUNG |= (not ok) and not informativ
    ZEILEN.append([thema, groesse, f"{original:.4f}", f"{zweit:.4f}", f"{d:+.4f}", einheit, "ja" if ok else "NEIN"])


# 1. Einwohnerzahlen 2024: Original (basis.py) gegen laender_2024.csv
with open(WURZEL / "daten/aggregate/laender_2024.csv", encoding="utf-8") as f:
    laender = {r["land"]: r for r in csv.DictReader(f)}
for k, pop in basis.POP.items():
    melde("Einwohner 2024", k, pop / 1e6, float(laender[k]["einwohner_mio_2024"]), 0.0005, "Mio",
           informativ=True)  # bekannte Datenabweichung, Logbuch Band III v3.8

# 2. Zeitpfad: Dividendenanteil je Jahr, Original (final.pfad) gegen pfad.csv
orig = final.pfad()
with open(WURZEL / "daten/aggregate/pfad.csv", encoding="utf-8") as f:
    zweit = {int(r["jahr"]): r for r in csv.DictReader(f)}
for r in orig:
    j = r["jahr"]
    if j in zweit:
        melde("Dividendenanteil", str(j), r["div"], float(zweit[j]["dividende_anteil_pct_bip"]), 0.01, "% des BIP")

# 3. Mindestquote: Original-Methode (Bisektion auf KOPF_DE, ohne reales Wachstum)
lo, hi = 25.0, 40.0
for _ in range(90):
    m = (lo + hi) / 2
    if min(r["de_fix"] for r in final.pfad(m)) < final.VERSPRECHEN:
        lo = m
    else:
        hi = m
q_orig = (lo + hi) / 2
import pfad as zweit_pfad  # noqa: E402  (Zweitrechnung)

P_ZWEIT = zweit_pfad.lade()
lo, hi = 25.0, 40.0
for _ in range(90):
    m = (lo + hi) / 2
    if min(r["de_real"] for r in final.pfad(m)) < final.VERSPRECHEN:
        lo = m
    else:
        hi = m
q_orig_real = (lo + hi) / 2
melde("Mindestquote", "streng (ohne reales Wachstum)", q_orig, zweit_pfad.rechne(P_ZWEIT, real_exakt=0.0)["mindestquote"],
      0.005, "% des BIP")
melde("Mindestquote", "zentral (0,98 % real)", q_orig_real,
      zweit_pfad.rechne(P_ZWEIT, real_exakt=final.G_REAL * 100)["mindestquote"], 0.005, "% des BIP")

# 4. Aufschlag: Original (aufschlag.py) neu gerechnet gegen daten/aggregate/aufschlag.csv
satz = 78.4 * 1.53 / 100  # aufschlag.py setzt D_START = 78.4 fest (gerundet), nicht den berechneten Wert
F = 1.13535
with open(WURZEL / "daten/aggregate/aufschlag.csv", encoding="utf-8") as f:
    auf = {r["land"]: float(r["aufschlag_eur_je_kopf_und_jahr"]) for r in csv.DictReader(f)}
summe = 0.0
for k in basis.GDP:
    bip28 = basis.GDP[k] / 1000 * F
    kopf = bip28 * 1e9 / basis.POP[k]
    aus = basis.SCHULD[k] / 100 * bip28 * 1.53 / 100 * 1e9 / basis.POP[k]
    ein = satz / 100 * kopf
    summe += (aus - ein) * basis.POP[k] / 1e9
    melde("Aufschlag", k, aus - ein, auf[k], 3.0, "EUR je Kopf und Jahr")
ZEILEN.append(["Aufschlag", "Summe (Original, Mrd EUR)", f"{summe:.4f}", "0", "", "Mrd EUR",
               "Original druckt 'null, wie gefordert', rechnet aber 0,0955 Mrd: das Skript setzt D_START auf den gerundeten Wert 78,4"])

pfad_aus = WURZEL / "daten/aggregate/vergleich_original.csv"
with open(pfad_aus, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["thema", "groesse", "original", "zweitrechnung", "differenz", "einheit", "innerhalb_toleranz"])
    w.writerows(ZEILEN)

nein = [z for z in ZEILEN if z[-1] == "NEIN"]
for z in nein:
    print("  ", z)
bekannt = sum(1 for z in nein if z[0] == "Einwohner 2024")
print(f"{len(ZEILEN)} Zeilen, außerhalb der Toleranz {len(nein)}, davon bekannt {bekannt} "
      f"(Einwohner in basis.py, Korrektur 49)")
sys.exit(2 if ABWEICHUNG else 0)
