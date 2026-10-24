#!/usr/bin/env python3
"""Deckel der Weitergabe als einheitliche Regel: Vielfache des Grundbedarfs (Logbuch v4.34). Prüfrechnung, Option zu E2.

Geltend ist der Deckel nur in Frankreich (1,602 × Durchschnittslohn, v4.33). Geprüft: Weitergabe in allen Staaten nur bis zum Arbeitgeberbeitrag
beim k-fachen Grundbedarf des Landes, k = 3 / 5 / 6 / 6,5 / 7 / 8. Mehr im Monat, alleinstehend, 2028, Kaufkraft 2026, beim 0,5- bis 3-fachen
Durchschnittslohn, und Anteil mit mehr (regel_boden). Ausgabe: daten/aggregate/deckel_einheitlich.json
"""
import contextlib, importlib.util, io, json
from pathlib import Path

W = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("rb", W / "modell" / "regel_boden.py")
RB = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(RB)
SL, HL = RB.SL, RB.SL.HL
ROH = lambda c, b: SL.H33.ag(b) if c == "DE" else HL.MODELLE[c][1](b)
LAENDER = ("DE", "FR", "IT", "ES", "PL")
FAKTOREN = (3, 5, 6, 6.5, 7, 8)


def rechne(k):
    alt = SL.ag

    def ag(c, b):
        if k is None:
            return alt(c, b)
        gb = HL.LS["staaten"][c]["grundbedarf_jahr_eur"] * HL.faktor(c)
        return min(ROH(c, b), ROH(c, k * gb))
    SL.ag = ag
    try:
        out = {}
        for c in LAENDER:
            aw = HL.P["oecd"]["durchschnittslohn"][c]
            out[c] = dict(anteil_mehr_allein=RB.anteile(c)["alleinstehend"],
                          mehr_monat={str(f): round((RB.neu(c, f * aw, 1, 0) - SL.heute(c, f * aw, 1, 0)) / 12) for f in (0.5, 1, 2, 3)})
        return out
    finally:
        SL.ag = alt


def main():
    gb = {c: dict(grundbedarf=round(HL.LS["staaten"][c]["grundbedarf_jahr_eur"] * HL.faktor(c)), durchschnittslohn=HL.P["oecd"]["durchschnittslohn"][c])
          for c in LAENDER}
    E = dict(version="v4.34", status="Prüfrechnung, Option zu E2", laender=gb, geltend=rechne(None),
             einheitlich={str(k): rechne(k) for k in FAKTOREN},
             hinweis="Währung je Land (PL in zł). Geltend: Deckel nur FR. Der Rest über dem Deckel bleibt beim Betrieb (E10, v4.34).")
    (W / "daten" / "aggregate" / "deckel_einheitlich.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in E["einheitlich"].items():
        print(k, {c: v[c]["mehr_monat"] for c in LAENDER})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
