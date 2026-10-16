#!/usr/bin/env python3
"""Systemvarianten 25:25 und 33:33 gegen 28:28 (Logbuch v3.43). Prüfrechnung; die Gesamtrechnung bleibt unverändert.

Je Variante:
  1  Mindestquote: dieselbe Rechnung wie modell/gesamtrechnung.py (Dach, Gemeinden, Dividende, strenge Lesart ohne reales Wachstum),
     mit dem Mindestniveau der Variante (Anteil am Bezugswert).
  2  Deckung: die Positionen der Gesamtrechnung (deutsche Basis), Sätze auf den Spitzensatz der Variante skaliert
     (Einkommen über die Aufkommensfunktion des Kernmodells, Label über den effektiven Satz, übrige statisch proportional).
  3  Was zusätzlich aus Steuern zu tragen ist (Härtefall; bei 33:33 auch Gesundheit, Seil und Zugesagtes Z), Z neu gerechnet mit der Dividende
     der Variante (modell/sozialschutz.py): 2028, 2040, 2050, Dauerzustand nach dem Auslauf von Z.
  4  Was außerhalb der Steuern bleibt (Prämien, Übergangsbeitrag) und die Gesamtlast.
Ausgabe: daten/aggregate/systemvarianten.json, systemvarianten.csv
"""
import contextlib
import csv
import importlib.util
import io
import json
import math
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "systemvarianten.toml").read_text(encoding="utf-8"))


def lade(name, pfad):
    spec = importlib.util.spec_from_file_location(name, pfad)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


GR = lade("gr", W / "modell" / "gesamtrechnung.py")
SZ = lade("sz", W / "modell" / "sozialschutz.py")
KERN = lade("kern", W / "modell" / "kern" / "modell-2828.py")
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
S = json.loads((AGG / "sozialschutz.json").read_text(encoding="utf-8"))
NF = json.loads((AGG / "nachfrage.json").read_text(encoding="utf-8"))
NFT = tomllib.loads((W / "modell" / "nachfrage.toml").read_text(encoding="utf-8"))
ZEILE = {r[0]: r[1] for r in G["tabelle_deckung"]}


def zeile(*praef):
    return sum(v for k, v in ZEILE.items() if k.startswith(praef))


def einkommen(saetze):
    g26, eti, inf = 12348.0, KERN.SZ["Robust"]["eti"], float("inf")

    def auf(s):
        KERN.TARIF_SAETZE[:] = [x / 100 for x in s]
        KERN.TARIF_GRENZEN[:] = [g26 * x for x in (1, 1.5, 2, 3)] + [inf]
        return KERN.est_aufkommen(50, eti)
    return zeile("01") * auf(saetze) / auf([0, 9, 16, 21, 28])


def label_effektiv(saetze):
    """Effektiver Satz unter der steuernden Zuordnung (nachfrage.toml), Stufen A+..D auf die Sätze der Variante abgebildet."""
    stufe = {5: 0, 11: 1, 17: 2, 22: 3, 28: 4}
    w = {g["id"]: (g["q1"] + g["q5"]) / 2 for g in NFT["gruppe"]}
    st = NFT["label_steuernd"]
    pfl = [g for g in NFT["gruppe"] if g["label"] > 0]
    satz = {}
    for g in pfl:
        alt = st.get(g["id"], g["label"])
        satz[g["id"]] = saetze[stufe[alt]] if alt in stufe else alt * saetze[4] / 28   # Verkehrsdienste 13 % proportional
    return sum(w[g["id"]] * satz[g["id"]] for g in pfl) / sum(w[g["id"]] for g in pfl)


def konsum(eff):
    k20 = G["konsum_kern_20_pct_bip"]
    return k20 * (eff / (100 + eff)) / (20 / 120)


def deckung(sy):
    r = sy["spitzensatz"] / 28
    eff = label_effektiv(sy["label_saetze"])
    pos = {
        "Einkommen": einkommen(sy["einkommen_saetze"]),
        "Kapitalerträge": zeile("02") * r,
        "Konsum (Label)": konsum(eff),
        "Unternehmen und Plattformen": zeile("05") * r,
        "Erbschaften": zeile("03", "Erbschaft") * r,
        "Große Vermögen": zeile("04c", "Vermögensteuer"),
        "CO₂-Preis": zeile("07", "CO₂-Pfad"),
        "Subventionsabbau": zeile("Abbau"),
        "Übrige Steuern": zeile("Sonstige"),
        "Grundstücksabgabe": zeile("04a"),
    }
    return pos, eff


def mindestquote(sy):
    anker_alt = GR.ANKER_DE                         # halber Grundbedarf je Erwachsenem DE, Preise 2028
    grund_monat = 2 * anker_alt                     # ganzer Grundbedarf je Monat
    if sy["bezugswert"] == "grundbedarf_sozial":
        sozial = (G["gesundheit"] + S["ausserhalb_quote"]["seil"]) / 100 * GR.KOPF_KLUB / 12 * GR.R_DE
        bezug = grund_monat + sozial
    else:
        sozial, bezug = 0.0, grund_monat
    anker = sy["mindestniveau_anteil"] * bezug
    schwelle = GR.SCHWELLE_KLUB * anker / anker_alt
    mq = GR.mindestquote("kl_real", schwelle=schwelle, g_nom=GR.PREIS)
    q = round(GR.aufrunden(mq, 0.1), 2)
    return q, mq, anker, sozial, bezug


def main():
    k = G["anteil_minderjaehrige"] / 100
    hf = P["annahmen"]["haertefall_pct_bip"]
    gs, seil = G["gesundheit"], S["ausserhalb_quote"]["seil"]
    route = S["ausserhalb_quote"]["route"]
    erg = []
    for sy in P["system"]:
        q, mq, anker, sozial, bezug = mindestquote(sy)
        pfad = GR.pfad(q)
        div28 = pfad[0]["div"]
        div_erw = div28 / (1 - k / 2)
        erw_de = pfad[0]["kl_real"] / (1 - k / 2) * GR.F_DE
        z = SZ.z_klub(div_erw)
        pos, eff = deckung(sy)
        dk = sum(pos.values())
        traegt = sy["steuer_traegt"]

        def zusatz(z_t):
            return (hf if "haertefall" in traegt else 0) + (gs if "gesundheit" in traegt else 0) + \
                   (seil if "seil" in traegt else 0) + (z_t if "z" in traegt else 0)

        def ausser(z_t):
            return (0 if "gesundheit" in traegt else gs) + (0 if "seil" in traegt else seil) + (0 if "z" in traegt else z_t)
        punkte = {}
        for name, j in (("2028", 2028), ("2040", 2040), ("2050", 2050), ("dauer", None)):
            z_t = z[j - 2028] if j else 0.0
            bedarf = q + zusatz(z_t)
            punkte[name] = dict(z=round(z_t, 2), steuerbedarf=round(bedarf, 2), deckung=round(dk, 2),
                                saldo=round(dk - bedarf, 2), ausserhalb_steuern=round(ausser(z_t), 2),
                                gesamtlast_ohne_route=round(bedarf + ausser(z_t), 2),
                                gesamtlast_mit_route=round(bedarf + ausser(z_t) + route, 2))
        erg.append(dict(id=sy["id"], name=sy["name"], spitzensatz=sy["spitzensatz"], einkommen_saetze=sy["einkommen_saetze"],
                        label_saetze=sy["label_saetze"], label_effektiv=round(eff, 2),
                        mindestniveau_de_erw_monat=round(anker, 0), bezugswert_de_monat=round(bezug, 0),
                        sozialabdeckung_de_monat=round(sozial, 0),
                        mindestquote=round(mq, 2), quote_kern=q, dividende_pct_bip_2028=round(div28, 2),
                        dividende_de_erw_2028=round(erw_de, 0), deckung_positionen={n: round(v, 2) for n, v in pos.items()},
                        deckung=round(dk, 2), steuer_traegt=traegt, z_2028=round(z[0], 2),
                        z_ende=next((2028 + i for i, v in enumerate(z) if i > 5 and v < 0.1), None), punkte=punkte))
    E = dict(version=P["version"], status="Prüfrechnung, Gesamtrechnung unverändert bei 28:28", annahmen=P["annahmen"],
             gesundheit=gs, seil=seil, route=route, last_heute=G["last_heute"], varianten=erg)
    (AGG / "systemvarianten.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(AGG / "systemvarianten.csv", "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["system", "zeitpunkt", "quote_kern", "z", "steuerbedarf", "deckung", "saldo", "ausserhalb_steuern",
                     "gesamtlast_ohne_route", "gesamtlast_mit_route"])
        for v in erg:
            for n, p in v["punkte"].items():
                wr.writerow([v["id"], n, v["quote_kern"], p["z"], p["steuerbedarf"], p["deckung"], p["saldo"],
                             p["ausserhalb_steuern"], p["gesamtlast_ohne_route"], p["gesamtlast_mit_route"]])
    for v in erg:
        print(f"{v['name']}: Mindestniveau DE {v['mindestniveau_de_erw_monat']:.0f} €/Erw. (Bezug {v['bezugswert_de_monat']:.0f}), "
              f"Quote Kern {v['quote_kern']} (streng {v['mindestquote']}), Dividende {v['dividende_pct_bip_2028']} % BIP = DE "
              f"{v['dividende_de_erw_2028']:.0f} €/Erw.; Label effektiv {v['label_effektiv']} %; Deckung {v['deckung']}; Z 2028 {v['z_2028']}, Ende {v['z_ende']}")
        for n, p in v["punkte"].items():
            print(f"   {n:>5}: Steuerbedarf {p['steuerbedarf']:>6} Deckung {p['deckung']:>6} Saldo {p['saldo']:>6} | außerhalb {p['ausserhalb_steuern']:>5} "
                  f"| Gesamtlast {p['gesamtlast_ohne_route']} (mit Route {p['gesamtlast_mit_route']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
