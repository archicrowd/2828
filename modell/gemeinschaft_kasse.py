#!/usr/bin/env python3
"""Gemeinschaft der Staaten: Größe einer gemeinsamen Kasse in drei Varianten (Logbuch v4.76). Entwicklungsmodus, vorläufig, kein Beschluss.

Grundlage ist die Rechnung dach_beitrag.py (v4.15/v4.16): Liste der gemeinsamen Aufgaben (Gesamtrechnung, Ziel 2035, Verteidigung 2,5 % BIP)
und Kassenanteile je Aufgabe (Annahmen der Initiative). Je Variante: Kasse in % des BIP, Verhältnis zur Eigenmittelobergrenze der EU (1,40 % BNE),
Betrag für Deutschland 2028 (BIP 2028 aus dach_beitrag.json, nominal) je Einwohner und Monat. Die Gesamtlast ändert sich nicht: Was in die
Kasse geht, gibt der Staat nicht selbst aus.
Ausgabe: daten/aggregate/gemeinschaft_kasse.json
"""
import json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "gemeinschaft_kasse.toml").read_text(encoding="utf-8"))
D = json.loads((W / "daten" / "aggregate" / "dach_beitrag.json").read_text(encoding="utf-8"))
T = tomllib.loads((W / "modell" / "dach_beitrag.toml").read_text(encoding="utf-8"))
A = {a["aufgabe"]: a for a in D["aufgaben"]}
DE = next(s for s in D["staaten"] if s["land"] == "DE")
EW_DE = DE["bip28_mrd"] * 1e9 / (DE["kasse_2028_eur_kopf_monat"] * 12) * D["reihe"][0]["kasse"] / 100   # Einwohner aus Kasse je Kopf (Rückrechnung)


def main():
    erg = {}
    for k, v in P["variante"].items():
        kasse = sum(A[a]["kasse"] for a in v["aufgaben"])
        de_mrd = DE["bip28_mrd"] * kasse / 100
        erg[k] = dict(name=v["name"], aufgaben={a: round(A[a]["kasse"], 3) for a in v["aufgaben"]}, kasse_pct_bip=round(kasse, 2),
                      zu_eu_obergrenze=round(kasse / T["eu_obergrenze_zahlungen_pct_bne"], 2),
                      de_2028_mrd=round(de_mrd, 1), de_2028_eur_kopf_monat=round(de_mrd * 1e9 / EW_DE / 12))
    E = dict(version=P["version"], status="Entwicklungsmodus: vorläufig, kein Beschluss", varianten=erg,
             hinweis="Kasse in % des BIP, Ziel 2035 (Verteidigung 2,5 %); Kassenanteile je Aufgabe Annahmen (dach_beitrag.toml). DE: BIP 2028 nominal "
                     "× Kassensatz (Größenordnung; mischt Zielsätze 2035 mit BIP 2028). Keine Änderung der Gesamtlast.")
    (W / "daten" / "aggregate" / "gemeinschaft_kasse.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in erg.items():
        print(k, v["kasse_pct_bip"], v["zu_eu_obergrenze"], v["de_2028_mrd"], v["de_2028_eur_kopf_monat"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
