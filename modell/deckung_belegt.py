#!/usr/bin/env python3
"""Belegte Deckung mit den Regeln vom 16.11.2026 (Logbuch v4.97): liest systemvarianten.py für die Variante 33R (Schlüssel belegt = true).

Unternehmen = belegt × (1/3 ÷ 33 %); Übrige = belegt; CO₂ = Modellpfad − (Modell 2028 − belegt 2028); Erbschaft = belegt × Faktor Freibetrag
(lognormal, 2 × Grundbedarf statt 100.000 €) × (1/3 ÷ 33 %) − Kassenwirkung des Stundungskredits.
Ausgabe: daten/aggregate/deckung_belegt.json
"""
import importlib.util
import json
import math
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "deckung_belegt.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("eb", W / "modell" / "einnahmen_belege.py")
EB = importlib.util.module_from_spec(spec)
spec.loader.exec_module(EB)


def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def anteil_ueber(F, mu, s, mittel):
    d1 = (mu + s * s - math.log(F)) / s
    return phi(d1) - F / mittel * phi(d1 - s)


def main():
    q = EB.positionen(P["fall"])
    f = P["satz"] / 33
    E = P["erbschaft"]
    s = math.sqrt(2 * math.log(E["mittel_2015"] / E["median_2015"]))
    mu = math.log(E["median_2015"] * E["preisfaktor_2015_2028"])
    mittel = E["mittel_2015"] * E["preisfaktor_2015_2028"]
    F_neu = E["vielfaches"] * E["grundbedarf_2026"] * (1 + E["preissteigerung"]) ** 2
    faktor = anteil_ueber(F_neu, mu, s, mittel) / anteil_ueber(E["freibetrag_alt"], mu, s, mittel)
    erb_brutto = q["erbschaft"] * faktor * f
    S = P["stundung"]
    stundung = erb_brutto * S["anteil_elternhaus"]
    zinsvorteil = erb_brutto * S["anteil_elternhaus"] * S["mittlere_dauer"] * (S["fondszins"] - S["zins"])
    erb = erb_brutto - stundung
    Eo = dict(version=P["version"], status="geltend ab v4.97", fall=P["fall"], satz=round(P["satz"], 4),
              positionen={"Unternehmen und Plattformen": round(q["unternehmen"] * f, 4), "Übrige Steuern": round(q["uebrige"], 4),
                          "CO₂-Abzug 2028": round(q["co2_2028"] - P["modell_co2_2028"], 4), "Erbschaften": round(erb, 4)},
              erbschaft=dict(belegt_100k=round(q["erbschaft"], 3), freibetrag_eur_2028=round(F_neu), faktor_freibetrag=round(faktor, 3),
                             brutto_drittel=round(erb_brutto, 3), stundung_kasse=round(-stundung, 3), zinsvorteil_dauerhaft=round(-zinsvorteil, 3),
                             hinweis="Kassenausfall durch Stundung vorsichtig dauerhaft angesetzt; ab etwa 2038 bleibt nur der Zinsvorteil"),
              quelle=dict(einnahmen_belege="einnahmen_belege.positionen", hilf=q["hilf"]))
    (AGG / "deckung_belegt.json").write_text(json.dumps(Eo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(Eo["positionen"], ensure_ascii=False), Eo["erbschaft"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
