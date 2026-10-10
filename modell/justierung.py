#!/usr/bin/env python3
"""Justierungspakete und Stabilitätsprüfung (Logbuch v3.34). Vorschlag der Initiative vom 10.10.2026:
29:29 in allen Konzeptteilen, Erbschaftsfreibetrag 100.000 € je Erwerb, Vermögensteuer leicht höher, Mehrwertsteuer leicht höher.

Hebel (Punkte des BIP gegen den Stand nach Entscheidung E1 C, Deckung 28,98 %, Lücke 2,92):
  Einkommensteuer 29 %: Kernmodell est_aufkommen (deutsche Basis, grob), optional Stufen beim 1-/1,5-/2-/3-fachen Grundbedarf.
  Kapital, Konzerne, Erbschaftssatz 29 %: statisch proportional (29/28) zur Deckungszeile (Annahme, kein Ausweichen).
  Erbschaftsfreibetrag 200.000 -> 100.000 €: Steuerbasis + 100.000 € je Erwerb über 200.000 € und anteilig 100–200.000 €;
     Zahl der Erwerbe über 200.000 € in Deutschland 100.000 bis 200.000 je Jahr (ANNAHME, keine Verteilung der Bruttoerwerbe gefunden).
  Vermögensteuer 1,25 / 1,5 %: proportional, die Hälfte der Mehreinnahme geht durch Ausweichen verloren (ANNAHME).
  Mehrwertsteuer-Label: steuernde Zuordnung (E1 C), alle Sätze +1 bzw. +2 Punkte (modell/nachfrage.py).
Stabilität: Wie weit darf der Dividendenanteil sinken, bevor die Mindestdividende im Klubschnitt in einem Jahr bricht?
Eine Deckungslücke senkt den Dividendenanteil um denselben Betrag. Stabil heißt: Lücke geschlossen und Reserve >= Schwelle.
Ausgabe: daten/aggregate/justierung.json. Keine Änderung der Gesamtrechnung.
"""
import contextlib, importlib.util, io, json, sys
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
T = json.loads((AGG / "tragfaehigkeit.json").read_text(encoding="utf-8"))
ZEILE = {r[0]: r[1] for r in G["tabelle_deckung"]}


def zeile(praefix):
    return next(v for k, v in ZEILE.items() if k.startswith(praefix))


def lade(name, pfad):
    spec = importlib.util.spec_from_file_location(name, pfad)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


KERN = lade("kern", W / "modell" / "kern" / "modell-2828.py")
NF = lade("nf", W / "modell" / "nachfrage.py")


def einkommen(spitze, stufen):
    g26, eti, inf = 12348.0, KERN.SZ["Robust"]["eti"], float("inf")

    def auf(s, m):
        KERN.TARIF_SAETZE[:] = s
        KERN.TARIF_GRENZEN[:] = [g26 * x for x in m] + [inf]
        return KERN.est_aufkommen(50, eti)
    return zeile("01") * (auf([0, .09, .16, .21, spitze], stufen) / auf([0, .09, .16, .21, .28], (1, 2, 3, 4)) - 1)


def label(plus):
    st = dict(NF.P["label_steuernd"])
    basis = NF.labelsatz(st)["konsumaufkommen_bei_zuordnung_pct_bip"]
    z = {g["id"]: st.get(g["id"], g["label"]) + plus for g in NF.P["gruppe"] if g["label"] > 0}
    ls = NF.labelsatz(z)
    return ls["konsumaufkommen_bei_zuordnung_pct_bip"] - basis, ls["effektiv_label_zuordnung_pct"]


def reserve():
    S, kopf, g, div = G["schwelle_klub"], G["kopf_klub"], G["g_real"], G["reihe_div"]
    tief = lambda c: min(((d - c) / 100 * kopf * (1 + g) ** t / 12) / S * 100 for t, d in enumerate(div))
    lo, hi = 0.0, 5.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if tief(mid) >= 100 else (lo, mid)
    return round(lo, 2)


def main():
    h = {}
    h["einkommen_29"] = einkommen(.29, (1, 2, 3, 4))
    h["einkommen_29_stufen_1_15_2_3"] = einkommen(.29, (1, 1.5, 2, 3))
    h["kapital_29"] = zeile("02") * (29 / 28 - 1)
    h["konzerne_29"] = zeile("05") * (29 / 28 - 1)
    h["erbschaft_satz_29"] = zeile("03") * (29 / 28 - 1)
    h["erbschaft_freibetrag_100k_niedrig"] = (100e3 * 100e3 + 3e9) * 0.29 / 1e9 / 4200 * 100
    h["erbschaft_freibetrag_100k_hoch"] = (200e3 * 100e3 + 6e9) * 0.29 / 1e9 / 4200 * 100
    verm = zeile("04c") + zeile("Vermögensteuer")
    h["vermoegen_125"] = verm * 0.25 * 0.5
    h["vermoegen_150"] = verm * 0.5 * 0.5
    h["label_plus1"], eff1 = label(1)
    h["label_plus2"], eff2 = label(2)
    h["label_plus3"], eff3 = label(3)
    h["einkommen_28_stufen_1_15_2_3"] = einkommen(.28, (1, 1.5, 2, 3))
    # Verwaltung (v3.35): netto 0,1 bis 0,3 % des BIP nach 8 bis 12 Jahren (Rechercheagent 10.10.2026: deutsche Ex-ante-Studien
    # NKR/ÖFIT 2015, NKR/McKinsey 2017; COFOG-Abstand im Verwaltungskern DE 2,1 gegen DK 1,7 / EE 1,8 als Obergrenze 0,4). ANNAHME.
    h["verwaltung_niedrig"], h["verwaltung_hoch"] = 0.1, 0.3
    # Ablösung (v3.36): Verwaltung der Sozialschutzsysteme Deutschland 1,12 % BIP (Eurostat tps00098 x tps00101, 2024 vorläufig);
    # entfällt durch Steuerfinanzierung ohne Beiträge und automatische Dividende zu 40 bis 70 % (ANNAHME; Gesundheit und Renten-
    # übergang bleiben zu verwalten). Übertragung auf den Klub mit dem deutschen Anteil (Annahme).
    h["abloesung_sozialverwaltung_niedrig"], h["abloesung_sozialverwaltung_hoch"] = 1.12 * 0.4, 1.12 * 0.7
    # Dach (v3.36): Posten Wirtschaftsraum 3,75 = COFOG GF04 (EU27 2024: 5,3) ohne örtlichen Verkehr. Streichung bzw. Abgabe an die
    # Gemeindeebene ohne zusätzliches Gemeindebudget (Entscheidung der Initiative): S1 Landwirtschaft 0,3 + Industrie 0,2 + halbe Energie 0,3;
    # S2 dazu halbe allgemeine Wirtschafts- und Arbeitsmarktangelegenheiten 0,5 und halber Rest 0,35. EU27-Anteile als Annahme für den Klub.
    h["dach_s1"], h["dach_s2"] = 0.3 + 0.2 + 0.3, 0.3 + 0.2 + 0.3 + 0.5 + 0.35
    h = {k: round(v, 2) for k, v in h.items()}
    erb_mitte = round((h["erbschaft_freibetrag_100k_niedrig"] + h["erbschaft_freibetrag_100k_hoch"]) / 2, 2)
    satz29 = h["einkommen_29"] + h["kapital_29"] + h["konzerne_29"] + h["erbschaft_satz_29"]
    pakete = {
        "P1 moderat (29:29, Erbe 100k, Vermögen 1,25 %, Label +1)": satz29 + erb_mitte + h["vermoegen_125"] + h["label_plus1"],
        "P2 kräftig (29:29, Erbe 100k, Vermögen 1,5 %, Label +2)": satz29 + erb_mitte + h["vermoegen_150"] + h["label_plus2"],
        "P3 wie P2, Stufen 1/1,5/2/3 bei 29 %": satz29 - h["einkommen_29"] + h["einkommen_29_stufen_1_15_2_3"] + erb_mitte
                                                 + h["vermoegen_150"] + h["label_plus2"],
    }
    basis4 = h["einkommen_28_stufen_1_15_2_3"] + erb_mitte + h["vermoegen_150"]
    pakete["P4 Entscheidung v3.35 (28 % bleibt, Stufen 1/1,5/2/3, Erbe 100k, Vermögen 1,5 %, Label +2, Verwaltung 0,1)"] = basis4 + h["label_plus2"] + h["verwaltung_niedrig"]
    pakete["P4 wie oben, Verwaltung 0,3"] = basis4 + h["label_plus2"] + h["verwaltung_hoch"]
    pakete["P5 wie P4, Label +3, Verwaltung 0,1"] = basis4 + h["label_plus3"] + h["verwaltung_niedrig"]
    pakete["P5 wie P4, Label +3, Verwaltung 0,3"] = basis4 + h["label_plus3"] + h["verwaltung_hoch"]
    basis6 = h["einkommen_28_stufen_1_15_2_3"] + erb_mitte + h["vermoegen_150"]
    for ab, abn in (("abloesung_sozialverwaltung_niedrig", "Ablösung 0,45"), ("abloesung_sozialverwaltung_hoch", "Ablösung 0,78")):
        pakete[f"P6 ohne Mehrwertsteuer-Erhöhung, {abn}, Dach S1"] = basis6 + h[ab] + h["dach_s1"]
        pakete[f"P7 Mehrwertsteuer +1, {abn}, Dach S1"] = basis6 + h["label_plus1"] + h[ab] + h["dach_s1"]
        pakete[f"P8 ohne Mehrwertsteuer-Erhöhung, {abn}, Dach S2"] = basis6 + h[ab] + h["dach_s2"]
    luecke0, res = T["deckung"]["luecke_nach_e1c"], reserve()
    erg = {}
    for n, v in pakete.items():
        l = round(luecke0 - v, 2)
        erg[n] = dict(mehr_pct_bip=round(v, 2), luecke_danach=l, reserve_mindestdividende=round(res - max(l, 0), 2),
                      reserve_mit_ueberschuss=round(res + max(-l, 0) - max(l, 0), 2),
                      stabil=bool(l <= 0 and res + max(-l, 0) >= 1.0))
    E = dict(hebel=h, erbschaft_mitte=erb_mitte, label_effektiv=dict(plus1=eff1, plus2=eff2, plus3=eff3), luecke_vorher=luecke0,
             reserve_heute_pkt=res, stabilitaetskriterium="Lücke <= 0 und Reserve >= 1,0 Punkte des BIP (Vorschlag)",
             pakete=erg, hinweis="Hebel grob (deutsche Basis, Kernmodell); Erbschaft und Vermögen mit gekennzeichneten Annahmen")
    (AGG / "justierung.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Hebel:", h, "| Erbschaft Mitte", erb_mitte, "| Label effektiv", eff1, eff2)
    print(f"Reserve heute (Mindestdividende im Klubschnitt): {res} Punkte; Lücke nach E1 C {luecke0}")
    for n, x in erg.items():
        print(f"{n}: +{x['mehr_pct_bip']} -> Lücke {x['luecke_danach']}, Reserve {x['reserve_mit_ueberschuss']}, stabil {x['stabil']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
