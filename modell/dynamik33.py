#!/usr/bin/env python3
"""Dynamische Wirkungen im Drittel-System (Logbuch v3.49): Beschäftigung, Automatisierung/KI, Verschiebung zum Kapital. Prüfrechnung.

Grundpfad: projektion33.json (System 33R, Trends v3.47). Wirkungen als Szenarien (Parameter in dynamik33.toml):
  - Mehr Arbeitsvolumen erhöht das BIP (Elastizität lohnanteil_bip); die Steuern sind Anteile am BIP, die Dividende in Euro wächst mit dem BIP je Kopf.
  - KI erhöht das Wachstum der Arbeitsproduktivität; ebenso wirkt es auf die Dividende in Euro.
  - Verschiebung von Arbeits- zu Kapitaleinkommen ändert das Aufkommen um Verschiebung × (Belastung Kapital − Belastung Arbeit); im Drittel-System
    fließt die Änderung in die Dividende (Rest); zum Vergleich die Wirkung im heutigen System.
  - Mehr Einkommen je Kopf hebt über die Stufen am Grundbedarf den Anteil der Einkommensteuer (Progression, wie projektion33.py v3.49).
  - Altlasten: feste Beträge, ihr Anteil am BIP sinkt mit dem höheren BIP (Fondsbeitrag näherungsweise / BIP-Faktor 2060).
Nicht enthalten: Rückwirkung auf Löhne und Preise, Verteilung innerhalb der Haushalte, Kosten der Umstellung.
Ausgabe: daten/aggregate/dynamik33.json
"""
import contextlib, importlib.util, io, itertools, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "dynamik33.toml").read_text(encoding="utf-8"))
PJ = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))
AL = json.loads((AGG / "altlasten.json").read_text(encoding="utf-8"))
R = {r["jahr"]: r for r in PJ["reihe"]}
NZ = {r["jahr"]: r for r in json.loads((AGG / "netz33.json").read_text(encoding="utf-8"))["beschluss"]["reihe"]}   # v4.41 (R9): Netz-Beschluss
FG = json.loads((AGG / "fonds_geltend.json").read_text(encoding="utf-8"))                                            # v4.41: Fonds der 30
_s = importlib.util.spec_from_file_location("pj", W / "modell" / "projektion33.py")
PJM = importlib.util.module_from_spec(_s)
with contextlib.redirect_stdout(io.StringIO()):
    _s.loader.exec_module(PJM)
E0 = PJM.SVM.deckung(PJM.sy)[0]["Einkommen"]
LA = PJM.P["stufen_lohnanteil"]


def faktor_beschaeftigung(b, j):
    anteil = min(1.0, (j - 2028) / P["einfuehrung_jahre"])
    return 1 + b / 100 * anteil * P["lohnanteil_bip"]


def faktor_ki(pp, j):
    f = 1.0
    for t in range(2029, j + 1):
        f *= 1 + (pp if t <= 2040 else pp / 2) / 100
    return f


def main():
    erg = []
    for b, ki, kv in itertools.product([0.0] + P["beschaeftigung_pct"], [0.0] + P["ki_pp"], P["kapital_verschiebung_pp"]):
        reihe = {}
        for j in (2028, 2035, 2045, 2060):
            r = R[j]
            fy = faktor_beschaeftigung(b, j) * faktor_ki(ki, j)
            v = kv * (j - 2028) / (2060 - 2028)
            plus_33 = v * (P["belastung_kapital_33"] - P["belastung_arbeit_33"])
            fr = r["wachstum_je_kopf_faktor"]
            prog = E0 * (PJM.progression((fr * fy) ** (1 - LA)) - PJM.progression(fr ** (1 - LA)))   # zusätzliche Progression durch mehr Wachstum
            plus_33 += prog
            n = NZ[j]
            div_pct = n["dividende_pct_bip"] + plus_33                        # v4.41: Grundpfad Netz-Beschluss statt projektion33
            eur = n["dividende_erw_eur2026"] / n["dividende_pct_bip"] * div_pct * fy
            reihe[str(j)] = dict(bip_faktor=round(fy, 3), aufkommen_aenderung_33_pct_bip=round(plus_33, 2),
                                 dividende_pct_bip=round(div_pct, 2), dividende_erw_eur2026=round(eur))
        fy60 = reihe["2060"]["bip_faktor"]
        erg.append(dict(beschaeftigung_pct=b, ki_pp=ki, kapital_verschiebung_pp=kv, reihe=reihe,
                        fondsbeitrag_naeherung_pct_bip=round(FG["beitrag_pct_bip"] / ((1 + fy60) / 2), 2),   # v4.41: Fonds der 30
                        heute_aufkommen_aenderung_2060_pct_bip=round(kv * (P["belastung_kapital_heute"] - P["belastung_arbeit_heute"]), 2)))
    E = dict(version="v4.41", status="Prüfrechnung", grundpfad="netz33.json beschluss.reihe (Netz-Beschluss); Fonds der 30 (fonds_geltend.json)", szenarien=erg,
             hinweis="Szenarien mit Annahmen; KI-Spanne Acemoglu 2024 bis OECD 2024; Fondsbeitrag nur als Näherung (Mittel des BIP-Faktors)")
    (AGG / "dynamik33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for e in erg:
        if e["kapital_verschiebung_pp"] == 0 or (e["beschaeftigung_pct"] == 4.6 and e["ki_pp"] == 0.3):
            print(f"Besch {e['beschaeftigung_pct']:>3} KI {e['ki_pp']:>4} Kap {e['kapital_verschiebung_pp']}: "
                  + " ".join(f"{j}:{x['dividende_erw_eur2026']}€(BIP×{x['bip_faktor']})" for j, x in e["reihe"].items())
                  + f" | Fonds ≈ {e['fondsbeitrag_naeherung_pct_bip']} | heute Kapitalverschiebung {e['heute_aufkommen_aenderung_2060_pct_bip']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
