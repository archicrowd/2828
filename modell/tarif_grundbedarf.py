#!/usr/bin/env python3
"""Tarifstufen als Vielfache des Grundbedarfs (Logbuch v3.21, Vorschlag der Initiative).

Regel (seit v3.37: Stufen beim 1-, 1,5-, 2- und 3-fachen Grundbedarf, Parameter tarif_stufen_vielfache; v3.22 bis v3.36): Die Stufen des Einkommensteuertarifs 0 / 9 / 16 / 21 / 28 % beginnen beim 1-, 2-, 3- und 4-fachen
Grundbedarf; 28 % ab dem Vierfachen (v3.21: fünf Stufen bis zum 5-fachen mit 26 %, verworfen). Grundbedarf = steuerliches Existenzminimum eines Erwachsenen (Grundfreibetrag Deutschland, 12.348 EUR
2026), am Wohnort mit dem Preisniveau übertragen und jährlich fortgeschrieben. Die Dividende ist der halbe Grundbedarf.

Aufkommensschätzung: mit der Aufkommensfunktion des nationalen Modells (modell/kern/modell-2828.py, est_aufkommen,
Szenario "Robust", Dividendenstufe 50 %), also Stand A, deutsche Basis, sieben Einkommensgruppen, Modellbasis
4.200 Mrd, Euro 2026. Grob: keine Haushaltsmikrosimulation. Das Original wird nur gelesen, nicht verändert.

Ausgabe: daten/aggregate/tarif_grundbedarf.csv (Varianten), daten/aggregate/tarif_grundbedarf.json
"""
import contextlib, csv, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
spec = importlib.util.spec_from_file_location("kern", W / "modell" / "kern" / "modell-2828.py")
kern = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(kern)

PAR = {p["name"]: p["wert"] for p in tomllib.loads((W / "modell/gesamtrechnung.toml").read_text(encoding="utf-8"))["parameter"]}
G26 = float(PAR["existenzminimum_de_jahr"])
G28 = G26 * (1 + float(PAR["preissteigerung"]) / 100) ** 2
INF = float("inf")
SAETZE = [0.00, 0.09, 0.16, 0.21, 0.26, 0.28]
VARIANTEN = [
    ("heute", "Stufen 12.348 / 25.000 / 40.000 / 55.000 / 70.000 EUR (bis v3.20)", SAETZE,
     [G26, 25000, 40000, 55000, 70000, INF]),
    ("grundbedarf_1_5", "Stufen beim 1- bis 5-fachen Grundbedarf (v3.21, verworfen in v3.22)", SAETZE,
     [G26 * k for k in (1, 2, 3, 4, 5)] + [INF]),
    ("grundbedarf_1_4", "Stufen beim 1- bis 4-fachen Grundbedarf, 28 % ab dem 4-fachen (gewählt, v3.22)",
     [0.00, 0.09, 0.16, 0.21, 0.28], [G26 * k for k in (1, 2, 3, 4)] + [INF]),
    ("grundbedarf_1_15_2_3", "Stufen beim 1-, 1,5-, 2- und 3-fachen Grundbedarf, 28 % ab dem 3-fachen (gewählt, v3.37)",
     [0.00, 0.09, 0.16, 0.21, 0.28], [G26 * k for k in (1, 1.5, 2, 3)] + [INF]),
]
ETI = kern.SZ["Robust"]["eti"]
BASIS = kern.BIP0

zeilen, base = [], None
for key, name, s, g in VARIANTEN:
    kern.TARIF_SAETZE[:] = s
    kern.TARIF_GRENZEN[:] = g
    auf = kern.est_aufkommen(50, ETI)
    base = auf if base is None else base
    zeilen.append(dict(variante=key, beschreibung=name, grenzen_eur_2026="/".join(f"{x:.0f}" for x in g[:-1]),
                       saetze_pct="/".join(f"{x*100:.0f}" for x in s), aufkommen_modell_mrd=round(auf, 2),
                       pct_bip_deutsche_basis=round(auf / BASIS * 100, 3), aenderung_mrd=round(auf - base, 2),
                       aenderung_pct_bip=round((auf - base) / BASIS * 100, 3),
                       steuer_25000=round(kern.est_2828(25000, s, g)), steuer_40000=round(kern.est_2828(40000, s, g)),
                       steuer_80000=round(kern.est_2828(80000, s, g))))
with open(AGG / "tarif_grundbedarf.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(zeilen[0].keys()))
    w.writeheader()
    w.writerows(zeilen)

# Stufen je Land in Euro 2028 (Grundbedarf x Preisniveau / Preisniveau DE)
PLI = {r["land"]: float(r["preisniveau_eu27_100"]) for r in csv.DictReader(open(AGG / "preisniveau_2024.csv", encoding="utf-8"))}
VIELFACHE, SATZ_GEW = tuple(float(x) for x in PAR["tarif_stufen_vielfache"]), [0, 9, 16, 21, 28]
laender = {c: [round(G28 * PLI[c] / PLI["DE"] * k) for k in VIELFACHE] for c in sorted(PLI, key=lambda c: -PLI[c])}
GEWAEHLT = {(1.0, 2.0, 3.0, 4.0): "grundbedarf_1_4", (1.0, 1.5, 2.0, 3.0): "grundbedarf_1_15_2_3"}[VIELFACHE]
gew = next(z for z in zeilen if z["variante"] == GEWAEHLT)
alt = next(z for z in zeilen if z["variante"] == "grundbedarf_1_4")
(AGG / "tarif_grundbedarf.json").write_text(json.dumps(dict(
    grundbedarf_2026=G26, grundbedarf_2028=G28, vielfache=list(VIELFACHE), saetze=SATZ_GEW,
    stufen_de_2028=[round(G28 * k) for k in VIELFACHE], stufen_laender_2028=laender,
    einkommen_pct_bip_neu=gew["pct_bip_deutsche_basis"], einkommen_modell_mrd_neu=gew["aufkommen_modell_mrd"],
    aenderung_pct_bip=gew["aenderung_pct_bip"], variante=GEWAEHLT, einkommen_modell_mrd_1_4=alt["aufkommen_modell_mrd"],
    varianten=zeilen), ensure_ascii=False, indent=1), encoding="utf-8")

for z in zeilen:
    print(f"{z['variante']:<17}{z['aufkommen_modell_mrd']:>8.1f} Mrd ({z['pct_bip_deutsche_basis']:.2f} % BIP) "
          f"{z['aenderung_mrd']:+6.1f}  Steuer 80.000: {z['steuer_80000']}")
print(f"Grundbedarf 2028 {G28:.0f} EUR; Stufen DE 2028 {[round(G28*k) for k in VIELFACHE]}")
