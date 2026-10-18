#!/usr/bin/env python3
"""Boden-Regel im Vergleich mit Dänemark (kontanthjælp) und Schweden (försörjningsstöd), Logbuch v4.7. Prüfrechnung.

Verglichen werden drei Kennzahlen, jeweils mit den Sätzen 2026 und dem Median des äquivalenzgewichteten verfügbaren Einkommens (EU-SILC 2025,
fortgeschrieben auf 2026):
  1. Niveau der Mindestsicherung je Äquivalenzerwachsenem in % des Medians – mit und ohne Wohnkosten, weil DK und SE die Wohnkosten getrennt
     (SE: tatsächliche angemessene Miete; DK: Wohngeld über Udbetaling Danmark und kommunale særlig støtte) behandeln, der Boden sie pauschal enthält;
  2. Gewicht eines Kindes relativ zu einem alleinstehenden Erwachsenen (Boden: OECD 0,3; DE-Regelbedarf; SE-Riksnorm);
  3. Belastung eines zusätzlich verdienten Euros im Bezug (Transferentzug und Steuer).
Dazu zwei Härtefall-Beispiele für Deutschland: Familie ohne Erwerb bei Kindergewicht 0,3 / 0,45 / 0,5 und hohe Miete einer alleinstehenden Person.
Ausgabe: daten/aggregate/vergleich_dk_se.json
"""
import json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "vergleich_dk_se.toml").read_text(encoding="utf-8"))
RB = json.loads((AGG / "regel_boden.json").read_text(encoding="utf-8"))
F = P["fortschreibung_median"]


def med(c):
    return P["median"][c] * F


def pct(x, c):
    return round(100 * x / med(c), 1)


def dk_netto(brutto_jahr):
    d = P["dk"]
    return brutto_jahr - max(0.0, brutto_jahr - d["personfradrag"]) * (d["bundskat"] + d["kommuneskat"])


def niveau():
    de, dk, se = P["de"], P["dk"], P["se"]
    em = de["existenzminimum_2026"]
    wohnanteil = (em["bruttokaltmiete"] + em["heizung"]) / (em["regelbedarf"] + em["bruttokaltmiete"] + em["heizung"])
    se_single = (se["personlig_ensam"] + se["gemensam"][0]) * 12
    se_fam = (se["personlig_sammanboende"] + se["barn"]["4-6"] + se["barn"]["7-10"] + se["gemensam"][3]) * 12 / 2.1   # je Äquivalenzerwachsenem (OECD)
    dk_single = dk_netto((dk["forhoejet_sats"] + dk["tillaeg_enlig_uden_boern"]) * 12)
    return {
        "DE Boden, Wohnen enthalten (je Äquivalenzerwachsenem)": pct(de["grundbedarf"], "DE"),
        "DE Boden, ohne Wohnanteil": pct(de["grundbedarf"] * (1 - wohnanteil), "DE"),
        "DE Bürgergeld heute, alleinstehend, mit KdU": pct((de["regelbedarf_monat"]["erwachsen"] + de["kdu_alleinstehend_monat"]) * 12, "DE"),
        "DK kontanthjælp ab 30, alleinstehend, netto (Wohnen daraus; Wohngeld und særlig støtte zusätzlich)": pct(dk_single, "DK"),
        "SE Riksnorm alleinstehend, ohne Wohnkosten": pct(se_single, "SE"),
        "SE Riksnorm Paar + 2 Kinder (4–6, 7–10), ohne Wohnkosten, je Äquivalenzerwachsenem": pct(se_fam, "SE"),
        "_wohnanteil_de_existenzminimum": round(wohnanteil, 3),
        "_dk_netto_monat_kr": round(dk_single / 12),
    }


def kindergewicht():
    de, se = P["de"], P["se"]
    rb = de["regelbedarf_monat"]
    em = de["existenzminimum_2026"]
    single = se["personlig_ensam"] + se["gemensam"][0]
    g = se["gemensam"]
    return {
        "Boden (OECD-modifiziert, bis v4.7)": 0.3,
        "DE Regelbedarf 0–5 / 6–13 / 14–17": [round(rb[k] / rb["erwachsen"], 2) for k in ("kind_0_5", "kind_6_13", "kind_14_17")],
        "DE Existenzminimum Kind (mit Wohnen) / Erwachsene": round((em["kind_regelbedarf"] + em["kind_wohnen"]) /
                                                                 (em["regelbedarf"] + em["bruttokaltmiete"] + em["heizung"]), 2),
        "SE Riksnorm 0 / 4–6 / 7–10 / 15–18 (drittes und viertes Haushaltsmitglied)": [round((se["barn"][a] + (g[3] - g[2])) / single, 2)
                                                                                         for a in ("0", "4-6", "7-10", "15-18")],
    }


def belastung():
    dk, se = P["dk"], P["se"]
    t_dk = dk["bundskat"] + dk["kommuneskat"]
    de = RB["staaten"]["DE"]["lohnabstand"]["alleinstehend"]["belastung_zusatzeuro_bei_halbem_mindestlohn"]
    return {
        "DE heute (Bürgergeld, alleinstehend, halber Mindestlohn)": de["heute"],
        "DE Boden-Regel (dieselbe Lage)": de["neu"],
        "DK im Freibetrag (2.700 kr./Monat)": round(100 * (1 - (1 - dk["am_bidrag"]) * (1 - t_dk))),
        "DK über dem Freibetrag": round(100 * (1 - (1 - dk["am_bidrag"]) * (1 - dk["anrechnung_ueber_fradrag"]) * (1 - t_dk))),
        "SE erste 6 Monate": 100,
        "SE mit Jobbstimulans (24 Monate)": round(100 * (1 - se["jobbstimulans"] * (1 - se["steuer_niedriglohn"]))),
    }


def haertefall_de():
    de = P["de"]
    g = de["grundbedarf"] / 12
    boden = RB["staaten"]["DE"]["boden_monat"]
    fam = {str(k): round(g * (1 + 0.5 + 2 * k)) for k in (0.3, 0.45, 0.5)}
    em = de["existenzminimum_2026"]
    wohn_boden = g * (em["bruttokaltmiete"] + em["heizung"]) / (em["regelbedarf"] + em["bruttokaltmiete"] + em["heizung"])
    return dict(paar_2_kinder_ohne_erwerb=dict(boden_nach_kindergewicht=fam, buergergeld_heute=de["buergergeld_paar_2_kinder_monat"],
                                                boden_modell=boden["Paar, ein Einkommen, 2 Kinder"]),
                hohe_miete_alleinstehend=dict(wohnanteil_im_boden=round(wohn_boden), miete=de["miete_beispiel_monat"],
                                              luecke_ohne_einkommen=round(de["miete_beispiel_monat"] - wohn_boden)))


def main():
    E = dict(version=P["version"], status="Prüfrechnung", niveau_pct_median=niveau(), kindergewicht=kindergewicht(),
             belastung_zusatzeuro_pct=belastung(), haertefall_de_monat=haertefall_de(),
             hinweis="Sätze 2026, Median EU-SILC 2025 × 1,06 (Annahme). DK netto mit Personfradrag, Bundskat und Kommunalsteuer (Sekundärquelle). "
                     "Belastung DK/SE mit Annahmen zur Steuer; DE aus regel_boden.json. Lücke bei hoher Miete: Miete minus Wohnanteil im Boden.")
    (AGG / "vergleich_dk_se.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in E.items():
        if isinstance(v, dict):
            print(k)
            for a, b in v.items():
                print("  ", a, ":", b)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
