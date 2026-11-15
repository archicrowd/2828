#!/usr/bin/env python3
"""Beleg der vier Einnahmepositionen (Prüfbefund B-1 vom 14.11.2026; Logbuch v4.87). Prüfrechnung, ändert die Deckung nicht.

Unternehmen  aus unternehmensbasis.json (seit v4.88, Korrektur 89): Basis der Kapitalgesellschaften aus KSt und Gewerbesteuer-Anteil,
             mit Kundenort, Plattformen, Gewinnverlagerung und Verlustverrechnung (bis v4.87: ganzes VGR-Aufkommen D51B / 30 %, enthielt die
             Gewerbesteuer der Personengesellschaften und Einzelunternehmen)
Übrige       VGR 2024: Einfuhrabgaben ohne MwSt + Produktsteuern ohne MwSt + sonstige Produktionsabgaben + sonstige laufende Steuern,
             ohne die Erlöse aus dem Emissionshandel (D29F), die im CO₂-Preis stehen
CO₂          bepreiste Emissionen 2028 × 100 €/t, in % BIP 2028 (gegen den Modellwert 2028)
Erbschaft    Mittel 2022–2025 des steuerlich berücksichtigten Vermögens, fortgeschrieben auf 2028, × Anteil über dem Freibetrag × Zuschlag für
             nicht erfasste Erwerbe × 33 %
Ausgabe: daten/aggregate/einnahmen_belege.json (Lücke je Position in % BIP; Wirkung auf die Dividende 2028 über Euro je BIP-Punkt).
"""
import json
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "einnahmen_belege.toml").read_text(encoding="utf-8"))
PF = json.loads((AGG / "plattformen33.json").read_text(encoding="utf-8"))
EUR = json.loads((AGG / "ausweichen33.json").read_text(encoding="utf-8"))["eur_je_bip_punkt"]["j2028"]
UB = json.loads((AGG / "unternehmensbasis.json").read_text(encoding="utf-8"))
NB = json.loads((AGG / "netz33.json").read_text(encoding="utf-8"))["beschluss"]["reihe"][0]


def main():
    s, V, M, B24 = P["satz"], P["vgr_2024"], P["modell"], P["bip_2024_mio"]
    pct = lambda mio: mio / B24 * 100
    faelle = {}
    for i, fall in enumerate(["vorsichtig", "mittel", "hoch"]):
        unternehmen = UB["faelle"][fall]["unternehmen_pct_bip"]
        u_basis = UB["faelle"][fall]["basis_mrd"]["zusammen"] * 1000
        uebrige = pct(V["D212"] - V.get("zoelle", 0) + V["D214"] + V["D29"] + V["D59"] - V["D29F"])
        C = P["co2"]
        mt28 = C["mt_2025"] * (1 - C["rueckgang_je_jahr"][i]) ** 3
        co2 = mt28 * C["preis_2028"] / 1000 / P["bip_2028_mrd"] * 100
        E = P["erbschaft"]
        w = E["werte_mrd"]
        mittel = sum(w.values()) / len(w)
        jahr_mitte = sum(int(j) for j in w) / len(w)
        b28 = mittel * (1 + E["wachstum"]) ** (2028 - jahr_mitte)
        erbschaft = s * b28 * E["anteil_ueber_freibetrag"][i] * (1 + E["nicht_erfasst_zuschlag"][i]) / P["bip_2028_mrd"] * 100
        pos = dict(unternehmen=(unternehmen, M["unternehmen"]), uebrige=(uebrige, M["uebrige"]), co2_2028=(co2, M["co2_2028"]),
                   erbschaft=(erbschaft, M["erbschaft"]))
        luecke = sum(b - m for b, m in pos.values())
        faelle[fall] = dict(positionen={k: dict(belegt_pct_bip=round(b, 2), modell_pct_bip=m, luecke_pct_bip=round(b - m, 2)) for k, (b, m) in pos.items()},
                            luecke_pct_bip=round(luecke, 2), dividende_eur_erw_monat=round(luecke * EUR),
                            dividende_2028_mit_kinderanteil_eur=round((NB["dividende_erw_eur2026"] + luecke * EUR) * 0.948),
                            hilfsgroessen=dict(unternehmen_basis_mrd_2025=round(u_basis / 1000), co2_mt_2028=round(mt28),
                                               erbschaft_basis_2028_mrd=round(b28)))
    E = dict(version=P["version"], status="interne Prüfrechnung zu Befund B-1; Deckung unverändert, nicht veröffentlichen bis zur Entscheidung (Option C, E1–E5)",
             vgr_2024_anteile_pct_bip={k: round(pct(v), 2) for k, v in V.items() if k.startswith("D")},
             befund_doppelzaehlung_co2=dict(d29f_pct_bip=round(pct(V["D29F"]), 2),
                                            hinweis="Die Position Übrige (165 Modell-Mrd., 3,93 % BIP) entspricht der VGR-Summe D212+D214+D29+D59 (3,81 % BIP 2024) "
                                                    "und enthält damit die heutigen Erlöse aus dem Emissionshandel (D29F); der CO₂-Preis (100 €/t auf die bepreisten "
                                                    "Emissionen) enthält sie ein zweites Mal."),
             faelle=faelle, eur_je_bip_punkt_2028=EUR, dividende_2028_geltend_eur=round(NB["dividende_erw_eur2026"] * 0.948))
    (AGG / "einnahmen_belege.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for f, d in faelle.items():
        print(f"{f:>10}: " + " | ".join(f"{k} {v['belegt_pct_bip']:.2f} ({v['luecke_pct_bip']:+.2f})" for k, v in d["positionen"].items())
              + f" | Lücke {d['luecke_pct_bip']:+.2f} % BIP = {d['dividende_eur_erw_monat']:+d} € → Dividende 2028 {d['dividende_2028_mit_kinderanteil_eur']} € | {d['hilfsgroessen']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
