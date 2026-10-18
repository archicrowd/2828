#!/usr/bin/env python3
"""Kindergewicht im Boden: Varianten 0,3 bis 0,8 (Logbuch v4.8). Prüfrechnung.

Auftrag der Initiative (18.10.2026): Kindergewicht 0,3 fair anpassen, auch 0,7–0,8 prüfen. Maßstäbe:
  - Bedarf: steuerliches Existenzminimum Kind (sächlich, mit Wohnen) / Grundbedarf = 6.828 / 12.348 = 0,55; mit Betreuung, Erziehung,
    Ausbildung (BEA) 9.756 / 12.348 = 0,79 (Grundlage von R1); Bürgergeld mit Unterkunft je Kind ≈ 0,46; Riksnorm (SE) ohne Wohnen 0,57–1,0;
  - Gleichbehandlung im Haushalt: weitere/r Erwachsene/r 0,5;
  - Abstand zur Arbeit: Haushalt ohne Erwerb gegen denselben Haushalt mit Vollzeit-Mindestlohn (Regel Boden, Halbanrechnung).
Je Variante und Land: Boden je Monat, verfügbares Einkommen bei 0 / ½ / 1 × Vollzeit-Mindestlohn, Anteil der Beschäftigten mit mehr,
Kosten der Aufstockung (boden_kosten, Band) gegen das Netzbudget.
Ausgabe: daten/aggregate/kindergewicht.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"


def lade(name, pfad):
    spec = importlib.util.spec_from_file_location(name, W / pfad)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


BK = lade("bk", "modell/boden_kosten.py")
RB = BK.RB
SL = RB.SL
VARIANTEN = (0.3, 0.45, 0.5, 0.55, 0.7, 0.8)
MAS = dict(existenzminimum_kind_saechlich=round(6828 / 12348, 2), existenzminimum_kind_mit_bea=round(9756 / 12348, 2),
           buergergeld_mit_kdu_je_kind=0.46, weitere_erwachsene=0.5, riksnorm_ohne_wohnen=[0.57, 1.0],
           quelle="Kinderfreibetrag 2026 sächlich 6.828 €, BEA 2.928 € (sozial_laender.toml, Sekundärquelle); Riksnorm: vergleich_dk_se.json")


def rechne(w):
    alt = RB.P["skala"]["kind"]
    RB.P["skala"]["kind"] = w
    out = {}
    for c in SL.LAENDER:
        ml = SL.P["mindestlohn"]["monat_2026"].get(c)
        voll = ml * 12 if ml else SL.HL.P["oecd"]["durchschnittslohn"][c] / 3
        hh = {}
        for n, e, k in SL.HAUSHALTE:
            hh[n] = dict(boden=round(RB.boden(c, e, k) / 12),
                         ohne_erwerb=round(RB.neu(c, 0.0, e, k) / 12),
                         halber_mindestlohn=round(RB.neu(c, voll * 0.5, e, k) / 12),
                         voller_mindestlohn=round(RB.neu(c, voll, e, k) / 12),
                         heute_voller_mindestlohn=round(SL.heute(c, voll, e, k) / 12))
            hh[n]["abstand_arbeit_pct"] = round(100 * (hh[n]["voller_mindestlohn"] / hh[n]["ohne_erwerb"] - 1))
        lo, hi = BK.kosten(c, BK.P["eigenanteil_unten"][1], w), BK.kosten(c, BK.P["eigenanteil_unten"][0], w)
        n = BK.MR["laender"][c]["z2028"]["netz"]
        budget = n["Härtefall"] + n["Arbeitslosigkeit"] + n["Invalidität"]
        out[c] = dict(haushalte=hh, anteil_mit_mehr=RB.anteile(c), kosten_pct_bip=[lo["pct_bip"], hi["pct_bip"]], budget_pct_bip=round(budget, 2))
    RB.P["skala"]["kind"] = alt
    return out


def main():
    E = dict(version="v4.8", status="Prüfrechnung", vorschlag=RB.P["skala"]["kind"], masstaebe=MAS, varianten={str(w): rechne(w) for w in VARIANTEN},
             hinweis="Monatsbeträge 2028, Kaufkraft 2026, Landeswährung (PL: Zł). Mindestlohn je Land (IT: ⅓ Durchschnittslohn). Kosten: Band aus "
                     "boden_kosten (Haushaltsmischung je Äquivalenzerwachsenem angenommen). Abstand zur Arbeit: Vollzeit-Mindestlohn gegen ohne Erwerb.")
    (AGG / "kindergewicht.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for w, v in E["varianten"].items():
        print("Kindergewicht", w)
        for c, x in v.items():
            p = x["haushalte"]["Paar, ein Einkommen, 2 Kinder"]
            a = x["haushalte"]["alleinerziehend, 1 Kind"]
            print(f"  {c} Paar+2: Boden {p['boden']} ohne {p['ohne_erwerb']} ML {p['voller_mindestlohn']} (heute {p['heute_voller_mindestlohn']}, Abstand {p['abstand_arbeit_pct']} %)"
                  f" | AE+1: ohne {a['ohne_erwerb']} ML {a['voller_mindestlohn']} | Anteile {x['anteil_mit_mehr']} | Kosten {x['kosten_pct_bip']} / {x['budget_pct_bip']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
