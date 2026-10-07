#!/usr/bin/env python3
"""Ländervarianten der Dividende und der Gemeindeformel (Logbuch B17, v3.17).

Rechnet für die zehn Staaten, was Dividende und Gemeindebudget je Einwohner in jeder Lesart ergeben. Ändert die
geltende Quote nicht; die Wahl ist eine Entscheidung der Initiative.

Lesarten der Dividende (je Erwachsenem und Monat, 2028, Preise 2028; Kinder zur Hälfte):
  V1  gleicher Eurobetrag im Klub
  V2  gleicher Anteil am örtlichen BIP je Kopf
  V3a halbes Existenzminimum am Wohnort, budgetneutral: der Klubtopf wird nach Einwohnern x Preisniveau verteilt
  V3b halbes Existenzminimum am Wohnort, verankert: 514,50 EUR in Deutschland, übrige Länder nach Preisniveau;
      Vergleich mit dem verfügbaren Topf (Deckungsgrad)
Gemeinden: Formel je Einwohner und je Kind als Anteil am BIP je Kopf des eigenen Landes ("Pro-Kopf-Variante des
Länderbeitrags"), dazu der klubweit einheitliche Betrag zum Vergleich.

Eingänge: gesamtrechnung.json, laender_2024.csv, preisniveau_2024.csv, modell/rahmen/basis.py (BIP 2024).
Ausgabe:  daten/aggregate/laendervarianten.csv, laendervarianten.json
"""
import contextlib, csv, io, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
sys.path.insert(0, str(W / "modell" / "rahmen"))
with contextlib.redirect_stdout(io.StringIO()):
    import basis  # noqa: E402

J = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
PAR = {p["name"]: p["wert"] for p in tomllib.loads((W / "modell/gesamtrechnung.toml").read_text(encoding="utf-8"))["parameter"]}
POP = {r["land"]: float(r["einwohner_mio_2024"]) * 1e6 for r in csv.DictReader(open(AGG / "laender_2024.csv", encoding="utf-8"))}
PLI = {r["land"]: float(r["preisniveau_eu27_100"]) for r in csv.DictReader(open(AGG / "preisniveau_2024.csv", encoding="utf-8"))}
L = ("DE", "FR", "ES", "NL", "IE", "BE", "AT", "DK", "SI", "EE")

k = J["anteil_minderjaehrige"] / 100
f_erw = 1 / (1 - k / 2)                       # Schnitt je Einwohner -> je Erwachsenem
div = J["div_2028"] / 100                     # Dividendenanteil am BIP 2028
B, SCHULE, KIND = J["b_fach"] / 100, 3.70 / 100, J["kind_ant"] / 100
pop_k = sum(POP[c] for c in L)
pli_k = sum(POP[c] * PLI[c] for c in L) / pop_k
anker_de = float(PAR["existenzminimum_de_jahr"]) / 12 / 2

zeilen, topf, bedarf_v3b = [], 0.0, 0.0
for c in L:
    kopf = basis.GDP[c] / 1000 * J["faktor"] * 1e9 / POP[c]
    v1 = J["erw_2028"]
    v2 = div * kopf / 12 * f_erw
    v3a = J["erw_2028"] * PLI[c] / pli_k
    v3b = anker_de * PLI[c] / PLI["DE"]
    topf += div * kopf * POP[c]
    bedarf_v3b += v3b / f_erw * 12 * POP[c]
    zeilen.append(dict(land=c, einwohner_mio=POP[c] / 1e6, bip_je_kopf_2028=kopf, preisniveau=PLI[c],
                       div_v1=v1, div_v2=v2, div_v3a=v3a, div_v3b=v3b,
                       gemeinde_je_einwohner_land=(B - SCHULE) * kopf, gemeinde_je_kind_land=SCHULE * kopf / KIND,
                       gemeinde_budget_je_kopf_land=B * kopf,
                       gemeinde_je_einwohner_klub=J["formel_einw"], gemeinde_je_kind_klub=J["formel_kind"]))
deckung = topf / bedarf_v3b
E = dict(preisniveau_klub=pli_k, anker_de=anker_de, deckungsgrad_v3b=deckung, zeilen=zeilen)
(AGG / "laendervarianten.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
with open(AGG / "laendervarianten.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(zeilen[0].keys()))
    w.writeheader()
    w.writerows({kk: (round(v, 2) if isinstance(v, float) else v) for kk, v in z.items()} for z in zeilen)
print(f"{'':4}{'Preis':>7}{'V1':>6}{'V2':>7}{'V3a':>6}{'V3b':>6}{'Gem/Kopf Land':>15}{'Klub':>7}")
for z in zeilen:
    print(f"{z['land']:4}{z['preisniveau']:7.1f}{z['div_v1']:6.0f}{z['div_v2']:7.0f}{z['div_v3a']:6.0f}{z['div_v3b']:6.0f}"
          f"{z['gemeinde_budget_je_kopf_land']:15.0f}{J['tabelle_einzug'][5][2]:7.0f}")
print(f"Preisniveau Klub (einwohnergewichtet) {pli_k:.1f}; Anker DE {anker_de:.2f} EUR; Deckungsgrad V3b {deckung*100:.1f} %")
