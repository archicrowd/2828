#!/usr/bin/env python3
"""Tragfähigkeitsprüfung nach den Entscheidungen der Initiative vom 10.10.2026 (Logbuch v3.33).

Prüft:
  1  Deckung nach Entscheidung E1 C (effektiver Labelsatz 16,9 %, nachfrage.json): Lücke gegen die Quote.
  2  Schließen der zusätzlichen Lücke über die Dividende: Deckung der Mindestdividende im Klubschnitt je Jahr
     (Kriterium v3.20: halbes Existenzminimum, schwelle_klub je Klub-Einwohner und Monat, Preise 2028).
  3  Tarifvarianten der Einkommensteuer (grob, deutsche Basis, Kernmodell est_aufkommen, Szenario Robust):
     Ist die Obergrenze 28 % der Engpass oder die Lage der Stufen?
  4  Abhängigkeit vom Wachstum (Sensitivität der Gesamtrechnung).
  5  Lenkungsabgaben, deren Bemessungsgrundlage mit Zielerreichung schrumpft (CO2).
Ausgabe: daten/aggregate/tragfaehigkeit.json. Keine Änderung der Gesamtrechnung.
"""
import contextlib, importlib.util, io, json, sys
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
N = json.loads((AGG / "nachfrage.json").read_text(encoding="utf-8"))


def deckung():
    zusatz = -N["labelsatz_steuernd"]["differenz_pct_bip"]
    return dict(quote=G["quote"], deckung_bisher=round(G["deckung_gesamt"], 2), luecke_bisher=round(G["deckung_luecke"], 2),
                zusatzluecke_label_c=round(zusatz, 2), deckung_nach_e1c=round(G["deckung_gesamt"] - zusatz, 2),
                luecke_nach_e1c=round(G["deckung_luecke"] + zusatz, 2))


def mindestdividende(kuerzung):
    S, kopf, g, div = G["schwelle_klub"], G["kopf_klub"], G["g_real"], G["reihe_div"]
    r = [((d - kuerzung) / 100 * kopf * (1 + g) ** t / 12) / S * 100 for t, d in enumerate(div)]
    mn = min(r)
    return dict(kuerzung_pkt_bip=kuerzung, dividende_minus_pct=round(kuerzung / div[0] * 100, 1),
                deckung_2028_pct=round(r[0], 1), tiefpunkt_pct=round(mn, 1), tiefpunkt_jahr=G["reihe_jahre"][r.index(mn)],
                jahre_unter_100=sum(1 for x in r if x < 100))


def tarif():
    spec = importlib.util.spec_from_file_location("kern", W / "modell" / "kern" / "modell-2828.py")
    kern = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(kern)
    g26, eti, inf = 12348.0, kern.SZ["Robust"]["eti"], float("inf")
    ek = next(x[1] for x in G["tabelle_deckung"] if x[0].startswith("01"))

    def auf(s, m):
        kern.TARIF_SAETZE[:] = s
        kern.TARIF_GRENZEN[:] = [g26 * x for x in m] + [inf]
        return kern.est_aufkommen(50, eti)
    base = auf([0, .09, .16, .21, .28], (1, 2, 3, 4))
    var = [("geltend 0/9/16/21/28, Stufen 1/2/3/4", [0, .09, .16, .21, .28], (1, 2, 3, 4)),
           ("Spitze 32 %", [0, .09, .16, .21, .32], (1, 2, 3, 4)), ("Spitze 35 %", [0, .09, .16, .21, .35], (1, 2, 3, 4)),
           ("0/10/18/24/32", [0, .10, .18, .24, .32], (1, 2, 3, 4)), ("0/10/20/26/35", [0, .10, .20, .26, .35], (1, 2, 3, 4)),
           ("28 % bleibt, Stufen 1/1,5/2/3", [0, .09, .16, .21, .28], (1, 1.5, 2, 3)),
           ("28 % bleibt, 0/12/20/24/28", [0, .12, .20, .24, .28], (1, 2, 3, 4))]
    return [dict(variante=n, einkommensteuer_pct_bip=round(ek * auf(s, m) / base, 2), aenderung=round(ek * (auf(s, m) / base - 1), 2))
            for n, s, m in var]


def main():
    d = deckung()
    md = [mindestdividende(x) for x in (0.0, d["zusatzluecke_label_c"], d["luecke_nach_e1c"])]
    t = tarif()
    co2 = sum(x[1] for x in G["tabelle_deckung"] if "CO₂" in x[0])
    E = dict(deckung=d, mindestdividende=md, tarif=t,
             wachstum=dict(sensitivitaet=G["tabelle_sens"], mindestquote_strenge_lesart=G["mindestquote_streng"],
                           hinweis="Quote nach strenger Lesart (real 0 % = nominal 2 %); die Mindestdividende hält auch ohne reales Wachstum"),
             lenkung=dict(co2_pct_bip=round(co2, 2), hinweis="Bemessungsgrundlage schrumpft mit Zielerreichung (Klimaneutralität 2045/2050)"),
             hinweis="Tarifvarianten grob: deutsche Basis, sieben Einkommensgruppen, Elastizität 0,35 (Kernmodell)")
    (AGG / "tragfaehigkeit.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Deckung:", d)
    for x in md:
        print(f"Dividende −{x['kuerzung_pkt_bip']} Pkt (−{x['dividende_minus_pct']} %): Mindestdividende 2028 {x['deckung_2028_pct']} %, "
              f"Tiefpunkt {x['tiefpunkt_pct']} % ({x['tiefpunkt_jahr']}), {x['jahre_unter_100']} Jahre unter 100 %")
    for x in t:
        print(f"Tarif {x['variante']}: {x['einkommensteuer_pct_bip']} % BIP ({x['aenderung']:+.2f})")
    print(f"CO2 in der Deckung: {co2:.2f} % BIP")
    return 0


if __name__ == "__main__":
    sys.exit(main())
