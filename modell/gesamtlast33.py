#!/usr/bin/env python3
"""Gesamtlast (Steuern, Altlasten, Pflichtvorsorge) Stand C, vergleichbar mit heute (Logbuch v4.14). Prüfrechnung.

Anlass: Prüfbericht 20.10.2026, B15 – systemvarianten.json nennt 2028 eine Gesamtlast von 45,46 % (49,56 % mit Route). Dort sind die Altlasten
als Zahlung im selben Jahr gerechnet (Z + Zinsen = 12,04 % BIP, „ohne Fonds“). Beschlossen ist der gemeinsame Fonds, der die Altlasten bis 2098
mit gleichbleibendem Beitrag trägt. Diese Rechnung stellt beide Lesarten nebeneinander:
  A  Steuern (Deckung 33R) + Fondsbeitrag (Beschluss)                      – Last, die der Staat erhebt
  B  A + Pflichtvorsorge (Route, eigenes Konto, Eigentum der Sparer)       – alle Pflichtzahlungen
  C  Steuern + Altlasten im Jahr ohne Fonds (systemvarianten)               – Vergleich: wenn die Altlasten nicht gestreckt würden
Heute: Steuern und Sozialbeiträge 40,76 % (Gesamtrechnung, Eurostat 2024, ohne D995). Die Streckung über den Fonds hat einen Preis:
Schuldenquote des Fonds bis 149,6 % (2056), wird ausgewiesen.
Ausgabe: daten/aggregate/gesamtlast33.json
"""
import json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "gesamtlast33.toml").read_text(encoding="utf-8"))
SV = json.loads((AGG / "systemvarianten.json").read_text(encoding="utf-8"))
AL = json.loads((AGG / "fonds_geltend.json").read_text(encoding="utf-8"))   # v4.20: geltender Fonds der 30 Staaten
SZ = json.loads((AGG / "sozialschutz.json").read_text(encoding="utf-8"))
PJ = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))


def main():
    v = next(x for x in SV["varianten"] if x["id"] == "33R")
    p28 = v["punkte"]["2028"]
    route = SZ["ausserhalb_quote"]["route"]
    deck = {r["jahr"]: r["deckung"] + r.get("progression", 0.0) for r in PJ["reihe"]}
    reihe = []
    for j in P["jahre"]:
        steuern = deck.get(j, p28["deckung"])
        fonds = AL["beitrag_pct_bip"] if j <= AL["zieljahr"] else 0.0
        reihe.append(dict(jahr=j, steuern=round(steuern, 2), fonds=fonds, a_steuern_und_fonds=round(steuern + fonds, 2),
                          b_mit_pflichtvorsorge=round(steuern + fonds + route, 2)))
    E = dict(version=P["version"], status="Prüfrechnung", heute=SV.get("last_heute", 40.76), pflichtvorsorge_route=route, reihe=reihe,
             # v4.46 (Korrektur 73, Prüfbefund B17): Summe aus den ausgewiesenen Teilen (Deckung + Altlasten), nicht aus dem Steuerbedarf 33,42
             c_ohne_fonds_2028=dict(steuern=p28["deckung"], altlasten_im_jahr=p28["altlastenbeitrag"],
                                    summe=round(p28["deckung"] + p28["altlastenbeitrag"], 2),
                                    mit_route=round(p28["deckung"] + p28["altlastenbeitrag"] + route, 2),
                                    systemvarianten_mit_steuerbedarf=dict(steuerbedarf=p28["steuerbedarf"], summe=p28["gesamtlast_ohne_route"],
                                                                          mit_route=p28["gesamtlast_mit_route"])),
             fonds=dict(beitrag_pct_bip=AL["beitrag_pct_bip"], zuschlag_pct=AL["zuschlag_auf_alle_steuern_pct"], schuldenquote_spitze=AL["schuldenquote_spitze"],
                        spitzenjahr=AL["spitzenjahr"], zieljahr=AL["zieljahr"]),
             hinweis="% des BIP; Fonds: gemeinsamer Fonds der 30 Staaten (fonds_geltend.json; v4.46, Prüfbefund B20 – vorher stand hier „Klub der zehn“). Steuern: Deckung 33R einschließlich Progression (projektion33). "
                     "Heute ohne private Vorsorge; die Pflichtvorsorge ist eigenes, vererbbares Vermögen und deshalb getrennt ausgewiesen.")
    (AGG / "gesamtlast33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("heute", E["heute"], "| C ohne Fonds 2028", E["c_ohne_fonds_2028"])
    for r in reihe:
        print(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
