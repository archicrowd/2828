#!/usr/bin/env python3
"""Verrechnung je Staat im Fonds der 30: Wirkung auf die Haushalte 2028 (Logbuch v4.37, R6). Prüfrechnung, Empfindlichkeit.

Die Haushaltsrechnungen nutzen den gleichen Zuschlag für alle Staaten (fonds_geltend.json, vereinfachend). Nach der Verrechnung je Staat
(fonds_klub.py, Beschlusslogik der zehn auf die 30 übertragen) trägt 2028 jeder Staat nach seiner eigenen Altlast; der Unterschied schmilzt
bis 2058 auf den gleichen Satz ab. Hier: Zuschlag 2028 je Staat statt des gemeinsamen Satzes, alleinstehend beim 0,5- / 1- / 2-fachen
Durchschnittslohn (mehr im Monat, Landeswährung, Kaufkraft 2026) und Anteil der Beschäftigten mit mehr (regel_boden).
Ausgabe: daten/aggregate/verrechnung_haushalte.json
"""
import contextlib, importlib.util, io, json
from pathlib import Path

W = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("rb", W / "modell" / "regel_boden.py")
RB = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(RB)
SL = RB.SL
FG = json.loads((W / "daten" / "aggregate" / "fonds_geltend.json").read_text(encoding="utf-8"))
LAENDER = ("DE", "FR", "IT", "ES", "PL")


def lauf(c):
    aw = SL.HL.P["oecd"]["durchschnittslohn"][c]
    return dict(mehr_monat={str(f): round((RB.neu(c, f * aw, 1, 0) - SL.heute(c, f * aw, 1, 0)) / 12) for f in (0.5, 1, 2)}, anteil_mehr=RB.anteile(c))


def main():
    out = {}
    for c in LAENDER:
        st = SL.HL.LS["staaten"][c]["fonds"]
        z0 = SL.P["zuschlag_de"] if c == "DE" else st["zuschlag_pct"]
        zn = FG["verrechnung"]["laender"][c]["reihe"]["2028"]["zuschlag_pct"]
        gleich = lauf(c)
        if c == "DE":
            SL.P["zuschlag_de"] = zn
        else:
            st["zuschlag_pct"] = zn
        try:
            verr = lauf(c)
        finally:
            SL.P["zuschlag_de"] = FG["zuschlag_auf_alle_steuern_pct"]
            st["zuschlag_pct"] = z0 if c != "DE" else st["zuschlag_pct"]
        out[c] = dict(zuschlag_gleich=z0, zuschlag_verrechnung_2028=zn, gleich=gleich, verrechnung_2028=verr)
    E = dict(version="v4.37", status="Prüfrechnung, Empfindlichkeit (geltend in den Haushalten: gleicher Satz)", laender=out,
             hinweis="2028; die Verrechnung schmilzt in 30 Jahren auf den gleichen Satz ab. PL in zł.")
    (W / "daten" / "aggregate" / "verrechnung_haushalte.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in out.items():
        print(c, x["zuschlag_gleich"], "->", x["zuschlag_verrechnung_2028"], x["gleich"], x["verrechnung_2028"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
