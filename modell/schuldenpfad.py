#!/usr/bin/env python3
"""Schuldenquote des Klubs 2010-2025 und Fortschreibung des Status quo bis zum Systemwechsel 2028.

Eingang: daten/aggregate/schulden_2010_2025.csv (Eurostat gov_10dd_edpt1, GD und B9, S13, % des BIP; je Land einzeln am
7.10.2026 abgerufen, maschinell gelesen), Gewichte: BIP 2024 (modell/rahmen/basis.py).
Fortschreibung: d(t+1) = d(t) / (1 + g) - b(2025), b = Finanzierungssaldo 2025 (Status quo: gleich bleibende Defizite),
g = nominales Wachstum der Gesamtrechnung (3,0 %). Vereinfachung: konstante Gewichte des Jahres 2024.
Ausgabe: daten/aggregate/schuldenpfad.json
"""
import contextlib, csv, io, json, sys, tomllib
from pathlib import Path
W = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(W / "modell" / "rahmen"))
with contextlib.redirect_stdout(io.StringIO()):
    import basis  # noqa: E402
PAR = {p["name"]: p["wert"] for p in tomllib.loads((W / "modell/gesamtrechnung.toml").read_text(encoding="utf-8"))["parameter"]}
g = float(PAR["wachstum_nominal"]) / 100
rows = list(csv.DictReader(open(W / "daten/aggregate/schulden_2010_2025.csv", encoding="utf-8")))
gew = {r["land"]: basis.GDP[r["land"]] for r in rows}
s = sum(gew.values())
jahre = list(range(2010, 2026))
hist = [sum(float(r[str(j)]) * gew[r["land"]] for r in rows) / s for j in jahre]
saldo = sum(float(r["defizit_2025"]) * gew[r["land"]] for r in rows) / s
prog_j, prog = [2025], [hist[-1]]
d = hist[-1]
for j in (2026, 2027, 2028):
    d = d / (1 + g) - saldo
    prog_j.append(j); prog.append(d)
E = dict(jahre=jahre, klub=hist, saldo_2025=saldo, prog_jahre=prog_j, prog=prog, start_2028=prog[-1], g=g)
(W / "daten/aggregate/schuldenpfad.json").write_text(json.dumps(E, indent=1), encoding="utf-8")
print("Klub 2010..2025:", " ".join(f"{x:.1f}" for x in hist))
print(f"Saldo 2025 {saldo:.2f} % BIP; Fortschreibung 2026-2028: " + " ".join(f"{x:.2f}" for x in prog[1:]))
