#!/usr/bin/env python3
"""Prüft tragende Werte in KENNZAHLEN.md gegen die Ergebnisdateien (Logbuch v4.53, offener Punkt R14; Anlass Korrekturen 74, 79, 80, 81).

Je Prüfung (modell/pruefe_kennzahlen.toml) wird der Wert aus der Ergebnisdatei in deutscher Schreibweise formatiert (Dezimalkomma, Tausenderpunkt,
Minus als „−“ oder „-“, Vorzeichen „+“ optional) und in der benannten Tabellenzeile gesucht. Fehlt er, ist die Kennzahl veraltet oder die Zeile
umbenannt: Rückgabe 1. Ausgabe: daten/aggregate/pruefe_kennzahlen.json
"""
import json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "pruefe_kennzahlen.toml").read_text(encoding="utf-8"))
TEXT = (W / "KENNZAHLEN.md").read_text(encoding="utf-8").splitlines()


def hole(d, pfad):
    for t in pfad.split("/"):
        d = d[int(t)] if isinstance(d, list) else d[t]
    return d


def de(x, stellen):
    s = f"{abs(x):,.{stellen}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if stellen == 0 and abs(x) < 10000:
        s = s.replace(".", "")          # vierstellige Zahlen ohne Tausenderpunkt zulassen (siehe Varianten unten)
    return s, x < 0


def formen(x, stellen):
    s, neg = de(x, stellen)
    roh = [s]
    if stellen == 0 and 1000 <= abs(x) < 10000:
        roh.append(f"{s[0]}.{s[1:]}")   # 1.083 und 1083
    out = []
    for r in roh:
        out += [f"−{r}", f"-{r}"] if neg else [r, f"+{r}"]
    return out


def main():
    erg, fehler = [], 0
    dateien = {}
    for p in P["pruefungen"]:
        d = dateien.setdefault(p["datei"], json.loads((W / "daten" / "aggregate" / p["datei"]).read_text(encoding="utf-8")))
        wert = hole(d, p["pfad"])
        zeilen = [z for z in TEXT if z.startswith(p["zeile"])]
        if len(zeilen) != 1:
            status = f"Zeile {len(zeilen)}-mal gefunden"
        else:
            status = "ok" if any(f in zeilen[0] for f in formen(wert, p["stellen"])) else "fehlt"
        fehler += status != "ok"
        erg.append(dict(zeile=p["zeile"], datei=p["datei"], pfad=p["pfad"], wert=wert, status=status))
    E = dict(version=P["version"], status="Prüfung", geprueft=len(erg), fehler=fehler, ergebnisse=erg)
    (W / "daten" / "aggregate" / "pruefe_kennzahlen.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for e in erg:
        if e["status"] != "ok":
            print(f"FEHLT  {e['zeile'][:50]:50s}  {e['datei']}:{e['pfad']} = {e['wert']}  ({e['status']})")
    print(f"Kennzahlen: {len(erg) - fehler} von {len(erg)} Werten in KENNZAHLEN.md gefunden")
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
