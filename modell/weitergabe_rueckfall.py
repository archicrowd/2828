#!/usr/bin/env python3
"""Rückfallregel der Weitergabe: Was fließt in den Fonds, wenn Betriebe weniger als 80 % weitergeben? (Logbuch v4.18). Prüfrechnung.

Regel: Für jeden Arbeitsvertrag, der am Stichtag besteht, gilt neuer Bruttolohn ≥ bisheriger Bruttolohn + 80 % des bisherigen
Arbeitgeberbeitrags. Wer weniger zahlt, führt die Differenz an den Altlastenfonds ab (Nachweis über die Lohnabrechnung).
Folge: Einbehalten bringt dem Betrieb nichts. Gibt er trotzdem weniger weiter, verlieren die Beschäftigten (weitergabe_sensitivitaet),
der Fonds erhält den Betrag; über einen geringeren Fondsbeitrag kommt er allen zugute. Hier: Höhe dieses Betrags, Deutschland.
Ausgabe: daten/aggregate/weitergabe_rueckfall.json
"""
import json
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "weitergabe_rueckfall.toml").read_text(encoding="utf-8"))
GR = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
WS = json.loads((AGG / "weitergabe_sensitivitaet.json").read_text(encoding="utf-8"))
AL = json.loads((AGG / "altlasten.json").read_text(encoding="utf-8"))["beschluss"]


def main():
    ag_oben = P["d12_mio"] / P["bip_mio"] * 100
    ag_unten = P["ag_satz"] * P["beitragspflichtig"] * P["d11_mio"] / P["bip_mio"] * 100
    eur_punkt = GR["punkt_bip_eur_de"]                      # € je Einwohner und Monat je BIP-Punkt, DE 2028
    reihe = []
    for w in P["tatsaechlich"]:
        luecke = max(0.0, P["pflicht"] - w)
        r = dict(weitergabe=w, rueckfluss_pct_bip=[round(luecke * ag_unten, 2), round(luecke * ag_oben, 2)],
                 rueckfluss_eur_kopf_monat=[round(luecke * ag_unten * eur_punkt), round(luecke * ag_oben * eur_punkt)],
                 anteil_am_fondsbeitrag_pct=[round(luecke * ag_unten / AL["beitrag_pct_bip"] * 100), round(luecke * ag_oben / AL["beitrag_pct_bip"] * 100)])
        v = WS["varianten"].get(str(w))
        if v:
            r["mehr_monat_alleinstehend_42000"] = v["de_mehr_monat"]["alleinstehend"]["42000"]
        reihe.append(r)
    E = dict(version=P["version"], status="Prüfrechnung", ag_beitraege_pct_bip=dict(unten=round(ag_unten, 2), oben=round(ag_oben, 2)),
             fondsbeitrag_pct_bip=AL["beitrag_pct_bip"], reihe=reihe,
             hinweis="Spanne: untere Schätzung 21 % × 85 % der Bruttolöhne (Annahme), obere D12 (Eurostat, mit unterstellten Beiträgen). "
                     "Euro je Einwohner und Monat 2028 nominal (punkt_bip_eur_de). Der Rückfluss schützt nicht den einzelnen Beschäftigten, "
                     "sondern nimmt dem Betrieb den Vorteil des Einbehaltens; der Anspruch des Beschäftigten folgt aus dem Gesetz zur Vertragsanpassung.")
    (AGG / "weitergabe_rueckfall.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("AG-Beiträge % BIP", E["ag_beitraege_pct_bip"])
    for r in reihe:
        print(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
