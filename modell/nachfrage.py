#!/usr/bin/env python3
"""Nachfrageprüfung: Wie viel Nachfrage und regionale Wertschöpfung erzeugt 28:28? (Logbuch v3.31)

Drei Kanäle, jeweils als Bandbreite:
  1  Umverteilung und Nettoentlastung: Mehrkonsum = Umverteilung x Abstand der Konsumneigung + Entlastung x Konsumneigung,
     abzüglich Importanteil und eines Abschlags für Geldpolitik und Angebotsgrenzen. Niveaueffekt auf das BIP, kein Dauerwachstum.
  2  Angebot (Arbeitsanreiz): klubweiter Niveaueffekt aus modell/anreize.py, bisher nicht eingerechnet, hier als Obergrenze.
  3  Mehrwertsteuer-Label: Preisänderung je Produktgruppe (mit unvollständiger Weitergabe), Mengenreaktion, Umschichtung des
     Konsums bei gleichem Budget; Veränderung des inländischen Wertschöpfungsanteils am Konsum.
  Zusatz: effektiver Labelsatz unter der Zuordnung dieser Prüfung gegen die Annahme des Kernmodells (20 %, Gewichte 10/10/20/30/30).
Eingänge: modell/nachfrage.toml, gesamtrechnung.json, anreize.json. Ausgabe: daten/aggregate/nachfrage.json
Keine Änderung der Gesamtrechnung.
"""
import itertools, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell/nachfrage.toml").read_text(encoding="utf-8"))
GR = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
AN = json.loads((AGG / "anreize.json").read_text(encoding="utf-8"))


def kanal1():
    E, m, out = GR["entlastung"], P["importanteil"], []
    for r, d, c, a in itertools.product(P["umverteilung_pct_bip"], P["mpc_abstand"], P["mpc_entlastung"], P["abschlag_geldpolitik"]):
        konsum = r * d + E * c
        out.append(dict(umverteilung=r, mpc_abstand=d, mpc_entlastung=c, abschlag=a,
                        bip_niveau_pct=round(konsum * (1 - m) * (1 - a), 2)))
    werte = sorted(x["bip_niveau_pct"] for x in out)
    zentral = 4.0 * 0.2 + E * 0.35
    return dict(entlastung_pct_bip=E, min=werte[0], max=werte[-1],
                zentral=round(zentral * (1 - m) * (1 - 0.25), 2),
                zentral_annahmen="Umverteilung 4 % des BIP, Abstand 0,2, Konsumneigung 0,35, Abschlag 0,25",
                faelle=out)


def gewichte():
    g = P["gruppe"]
    w = {x["id"]: (x["q1"] + x["q5"]) / 2 for x in g}
    s = sum(w.values())
    return {k: v / s for k, v in w.items()}


def kanal3(import_faktor=1.0, ws=None, we=None, zuordnung=None):
    zuordnung = zuordnung or {}
    ws = P["weitergabe_senkung"] if ws is None else ws
    we = P["weitergabe_erhoehung"] if we is None else we
    w = gewichte()
    neu = {}
    for x in P["gruppe"]:
        satz = zuordnung.get(x["id"], x["label"])
        roh = (1 + satz / 100) / (1 + x["heute"] / 100) - 1
        p = roh * (ws if roh < 0 else we)
        q = x["elast"] * p
        neu[x["id"]] = w[x["id"]] * (1 + p) * (1 + q)
    s = sum(neu.values())
    neu = {k: v / s for k, v in neu.items()}            # gleiches Budget
    imp = {x["id"]: min(x["import"] * import_faktor, 1.0) for x in P["gruppe"]}
    vorher = sum(w[k] * (1 - imp[k]) for k in w)
    nachher = sum(neu[k] * (1 - imp[k]) for k in w)
    return dict(inland_anteil_vorher=round(vorher * 100, 2), inland_anteil_nachher=round(nachher * 100, 2),
                aenderung_punkte_konsum=round((nachher - vorher) * 100, 3),
                aenderung_pct_bip=round((nachher - vorher) * P["konsum_anteil_bip"] * 100, 3),
                umschichtung={k: round((neu[k] - w[k]) * 1000, 2) for k in w})


def labelsatz(zuordnung=None):
    zuordnung = zuordnung or {}
    """Effektiver Satz auf den steuerpflichtigen Konsum unter der Zuordnung dieser Prüfung."""
    w = gewichte()
    steuerpfl = {x["id"]: x for x in P["gruppe"] if x["label"] > 0}
    s = sum(w[k] for k in steuerpfl)
    r = sum(w[k] * zuordnung.get(k, steuerpfl[k]["label"]) for k in steuerpfl) / s
    anteil_cd = sum(w[k] for k in steuerpfl if zuordnung.get(k, steuerpfl[k]["label"]) >= 22) / s
    r_heute = sum(w[k] * steuerpfl[k]["heute"] for k in steuerpfl) / s
    kern = 20.0
    faktor = (r / (100 + r)) / (kern / (100 + kern))
    konsum_kern = next(x[1] for x in GR["tabelle_deckung"] if x[0].startswith("06"))
    return dict(anteil_c_d_pct=round(anteil_cd * 100, 1), effektiv_label_zuordnung_pct=round(r, 2), effektiv_heute_de_saetze_pct=round(r_heute, 2), kernmodell_pct=kern,
                konsumaufkommen_kern_pct_bip=round(konsum_kern, 2),
                konsumaufkommen_bei_zuordnung_pct_bip=round(konsum_kern * faktor, 2),
                differenz_pct_bip=round(konsum_kern * (faktor - 1), 2),
                hinweis="Kernmodell: 60 % des Konsums in C/D (22/28 %). Bei der Zuordnung dieser Prüfung liegt der größte Teil in B (17 %).")


def main():
    k1 = kanal1()
    k2 = dict(abbau_klub_punkte=AN["abbau_klub_bip_gewichtet_punkte"], obergrenze_niveau_pct=AN["niveaueffekt_klub_nicht_eingerechnet_pct"],
              hinweis="lineare Übertragung über den Bereich der Literatur hinaus; Obergrenze, nicht Prognose")
    ST = P["label_steuernd"]
    k3 = dict(zentral=kanal3(), import_kaeuferpreise=kanal3(0.5), volle_weitergabe=kanal3(1.0, 1.0, 1.0),
              steuernd=kanal3(1.0, None, None, ST), steuernd_volle_weitergabe=kanal3(1.0, 1.0, 1.0, ST),
              steuernd_kaeuferpreise=kanal3(0.5, None, None, ST))
    ls = labelsatz()
    ls_st = labelsatz(ST)
    orig = {g["id"]: g["elast"] for g in P["gruppe"]}
    salienz = {}
    for f in P["salienz_faktoren"]:
        for g in P["gruppe"]:
            g["elast"] = orig[g["id"]] * f
        a, b = kanal3(1.0, None, None, ST), kanal3(1.0, 1.0, 1.0, ST)
        salienz[str(f)] = dict(zentral_punkte=a["aenderung_punkte_konsum"], zentral_pct_bip=a["aenderung_pct_bip"],
                               volle_weitergabe_pct_bip=b["aenderung_pct_bip"])
    for g in P["gruppe"]:
        g["elast"] = orig[g["id"]]
    k3["salienz_steuernd"] = salienz
    E = dict(version=P["version"], kanal1_umverteilung=k1, kanal2_angebot=k2, kanal3_label=k3, labelsatz=ls, labelsatz_steuernd=ls_st)
    (AGG / "nachfrage.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Kanal 1 (Nachfrage, Niveau BIP %): {k1['min']} bis {k1['max']}, zentral {k1['zentral']} ({k1['zentral_annahmen']})")
    print(f"Kanal 2 (Angebot, Obergrenze, nicht eingerechnet): {k2['obergrenze_niveau_pct']}")
    for n, x in k3.items():
        if n == "salienz_steuernd":
            continue
        print(f"Kanal 3 Label [{n}]: Inlandsanteil {x['inland_anteil_vorher']} -> {x['inland_anteil_nachher']} % "
              f"({x['aenderung_punkte_konsum']:+.3f} Punkte des Konsums, {x['aenderung_pct_bip']:+.3f} % BIP)")
    print("   Umschichtung ‰ (zentral):", {k: v for k, v in k3["zentral"]["umschichtung"].items() if abs(v) > 0.3})
    print(f"Labelsatz: Zuordnung {ls['effektiv_label_zuordnung_pct']} % (heute DE-Sätze {ls['effektiv_heute_de_saetze_pct']} %) gegen Kernmodell 20 %; "
          f"Konsumaufkommen {ls['konsumaufkommen_kern_pct_bip']} -> {ls['konsumaufkommen_bei_zuordnung_pct_bip']} % BIP ({ls['differenz_pct_bip']:+.2f})")
    print(f"Labelsatz steuernd: C/D-Anteil {ls_st['anteil_c_d_pct']} %, effektiv {ls_st['effektiv_label_zuordnung_pct']} %; "
          f"Konsumaufkommen {ls_st['konsumaufkommen_bei_zuordnung_pct_bip']} % BIP ({ls_st['differenz_pct_bip']:+.2f})")
    print("Salienz (steuernd):", {f: (x["zentral_pct_bip"], x["volle_weitergabe_pct_bip"]) for f, x in salienz.items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
