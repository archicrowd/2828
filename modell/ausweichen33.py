#!/usr/bin/env python3
"""Empfindlichkeit der Deckung und der Dividende gegenüber Ausweichreaktionen bei Erbschaft und großen Vermögen (Logbuch v4.18).

Positionen der Deckung 33R (systemvarianten.json, % BIP 2028): Erbschaften (statisch), Große Vermögen (mit 50 % Ausweichen).
Die Dividende ist der Rest: Was ausweicht, fehlt ihr eins zu eins (Euro je BIP-Punkt aus laenderseiten.json DE, 2028 und 2060,
Kaufkraft 2026). Rückwirkungen auf andere Positionen (Kapitalerträge, Umzüge in andere Staaten) nicht gerechnet.
Ausgabe: daten/aggregate/ausweichen33.json
"""
import json
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "ausweichen33.toml").read_text(encoding="utf-8"))
SV = json.loads((AGG / "systemvarianten.json").read_text(encoding="utf-8"))
LS = json.loads((AGG / "laenderseiten.json").read_text(encoding="utf-8"))["staaten"]["DE"]


def main():
    pos = next(v for v in SV["varianten"] if v["id"] == "33R")["deckung_positionen"]
    erb, verm = pos["Erbschaften"], pos["Große Vermögen"]
    verm_statisch = verm / (1 - P["vermoegen_ausweichen_geltend"])
    eur28 = LS["dividende_erw_eur"][0] / LS["dividende_pct_bip"][0]
    eur60 = LS["dividende_erw_eur"][-1] / LS["dividende_pct_bip"][-1]
    faelle = []
    for a_e in P["erbschaft_ausweichen"]:
        for a_v in P["vermoegen_ausweichen"]:
            d = -erb * a_e + (verm_statisch * (1 - a_v) - verm)
            faelle.append(dict(erbschaft_ausweichen=a_e, vermoegen_ausweichen=a_v, delta_pct_bip=round(d, 2),
                               dividende_2028_eur=round(d * eur28), dividende_2060_eur=round(d * eur60),
                               dividende_2028_neu=round(LS["dividende_erw_eur"][0] + d * eur28)))
    E = dict(version=P["version"], status="Prüfrechnung, Empfindlichkeit", positionen_pct_bip=dict(erbschaften=erb, grosse_vermoegen=verm,
             grosse_vermoegen_statisch=round(verm_statisch, 2)), eur_je_bip_punkt=dict(j2028=round(eur28, 1), j2060=round(eur60, 1)),
             dividende_de_2028=LS["dividende_erw_eur"][0], faelle=faelle,
             hinweis="Euro je Erwachsenem und Monat, Kaufkraft 2026, ohne Kinderanteil 0,8 (netz33). Ungünstigster Fall: beide Positionen "
                     "zusammen; Erbschaft-Position hängt zusätzlich an der Annahme von 150.000 Erwerben über 200.000 € je Jahr (gesamtrechnung.toml).")
    (AGG / "ausweichen33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(E["positionen_pct_bip"], E["eur_je_bip_punkt"])
    for f in faelle:
        print(f)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
