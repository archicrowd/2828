#!/usr/bin/env python3
"""Wie hängt das Ergebnis für Beschäftigte an der Weitergabe der Arbeitgeberbeiträge? (Logbuch v4.12, Prüfrechnung)

Anlass: externe Prüfung vom 19.10.2026 – die 80-%-Weitergabe sei rechtlich nicht erzwingbar und in der Inzidenzforschung umstritten.
Gerechnet mit der geltenden Regel (regel_boden: Grundauskommen, Kinderanteil 0,8, heute mit Bedarfsleistungen), 2028, Kaufkraft 2026:
mehr im Monat für drei Haushaltstypen und drei Löhne (DE) sowie Anteil der Beschäftigten mit mehr je Land, bei Weitergabe 0 / 50 / 80 / 100 %.
Ausgabe: daten/aggregate/weitergabe_sensitivitaet.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "weitergabe_sensitivitaet.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("rb", W / "modell" / "regel_boden.py")
RB = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(RB)
SL = RB.SL


def rechne(w):
    alt = SL.HL.P["weitergabe"]
    SL.HL.P["weitergabe"] = w
    try:
        de = {n: {str(b): round((RB.neu("DE", b, e, k) - SL.heute("DE", b, e, k)) / 12) for b in P["brutto_de"]} for n, e, k in SL.HAUSHALTE}
        anteil = {c: RB.anteile(c) for c in SL.LAENDER}
    finally:
        SL.HL.P["weitergabe"] = alt
    return dict(de_mehr_monat=de, anteil_mit_mehr=anteil)


def main():
    E = dict(version=P["version"], status="Prüfrechnung", quelle_inzidenz=P["quelle_inzidenz"],
             varianten={str(w): rechne(w) for w in P["weitergabe"]},
             hinweis="Weitergabe = Anteil der wegfallenden Arbeitgeberbeiträge im Bruttolohn; der Rest bleibt beim Arbeitgeber (höherer Gewinn, "
                     "dann mit 33 % besteuert – im Aufkommen hier nicht gegengerechnet). Heute mit Bedarfsleistungen (sozial_laender).")
    (AGG / "weitergabe_sensitivitaet.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for w, x in E["varianten"].items():
        print("Weitergabe", w, x["de_mehr_monat"], {c: min(a.values()) for c, a in x["anteil_mit_mehr"].items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
