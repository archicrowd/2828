#!/usr/bin/env python3
"""Gemeinsame Aufgaben ohne eigene Steuer: Pflichtquote mit zwei Wegen (Logbuch v4.15). Prüfrechnung.

Regel (Vorschlag 20.10.2026, Architektur „Regelwerk“):
  1  Pflichtquote: Jeder Staat wendet denselben Anteil seines BIP für die abschließende Liste gemeinsamer Aufgaben auf
     (Wert je Jahr = Dach-Pfad der Rechnung, projektion33 dach_ohne_zins; 2028 6,19 %, ab 2035 7,29 %).
  2  Zwei Wege: ein Teil in die gemeinsame Kasse (Kassenanteil je Aufgabe, Annahme), der Rest als eigene Ausgabe nach gemeinsamem
     Mindeststandard, vom Prüfhof angerechnet.
  3  Rückfallregel: Wer weniger anrechenbar ausgibt, zahlt die Differenz in die Kasse; Verrechnung durch die Ausgleichsstelle.
  4  Obergrenze: Pflichtquote höchstens 32 % des Steueraufkommens (bisherige Dach-Regel).
Die Verteidigung folgt dem Pfad der Gesamtrechnung (1,4 → 2,5 % BIP bis 2035, Beschluss 20.10.2026: bleibt).
Dividende, Netz und Gemeindeformel ändern sich nicht, solange die Pflichtquote insgesamt erfüllt ist.

Eingänge: daten/aggregate/gesamtrechnung.json (tabelle_a, bip28_klub_mrd, punkt_bip_eur_de), projektion33.json (reihe),
modell/rechnungen/rahmen/daten.py (Eurostat 2024: BIP, Einwohner, COFOG GF02 Verteidigung, % BIP).
Ausgabe: daten/aggregate/dach_beitrag.json
"""
import importlib.util
import json
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "dach_beitrag.toml").read_text(encoding="utf-8"))
GR = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
PJ = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))
_s = importlib.util.spec_from_file_location("daten", W / "modell" / "rechnungen" / "rahmen" / "daten.py")
D = importlib.util.module_from_spec(_s)
_s.loader.exec_module(D)

VERT = "Verteidigung und digitale Souveränität"


def main():
    posten = [(n, v) for n, v, _ in GR["tabelle_a"] if n != "Summe"]
    ziel = round(sum(v for _, v in posten), 2)
    ka = P["kassenanteil"]
    fehlt = [n for n, _ in posten if n not in ka]
    if fehlt:
        raise SystemExit(f"Kassenanteil fehlt für: {fehlt}")
    reihe_pj = {r["jahr"]: r for r in PJ["reihe"]}
    v_ziel = dict(posten)[VERT]
    reihe = []
    for j in P["jahre"]:
        r = reihe_pj[j]
        quote = r["dach_ohne_zins"]
        v_j = round(v_ziel - (ziel - quote), 2)               # nur die Verteidigung wächst bis 2035
        werte = [(n, v_j if n == VERT else v) for n, v in posten]
        kasse = sum(v * ka[n] for n, v in werte)
        steuern = r["deckung"] + r.get("progression", 0.0)
        reihe.append(dict(jahr=j, pflichtquote=round(quote, 2), verteidigung=v_j, kasse=round(kasse, 2),
                          angerechnet=round(quote - kasse, 2), kasse_anteil_pct=round(kasse / quote * 100, 1),
                          steuern=round(steuern, 2), obergrenze=round(P["regel"]["obergrenze_anteil_steuern"] * steuern, 2),
                          unter_obergrenze=quote <= P["regel"]["obergrenze_anteil_steuern"] * steuern + 1e-9,
                          kasse_zu_eu_obergrenze=round(kasse / P["eu_obergrenze_zahlungen_pct_bne"], 2)))
    tab = [dict(aufgabe=n, pct_bip_ziel=v, kassenanteil=ka[n], kasse=round(v * ka[n], 3), angerechnet=round(v * (1 - ka[n]), 3))
           for n, v in posten]
    # je Staat 2028 und 2035 (BIP 2024 × Fortschreibungsfaktor der Gesamtrechnung, nominal)
    f2428 = GR["bip28_klub_mrd"] / (sum(D.GDP.values()) / 1000)
    r28 = next(x for x in reihe if x["jahr"] == 2028)
    r35 = next(x for x in reihe if x["jahr"] == 2035)
    i02 = D.F.index("GF02")
    staaten = []
    for k in D.GDP:
        bip28 = D.GDP[k] / 1000 * f2428
        heute_v = D.S13[k][i02]
        staaten.append(dict(
            land=k, bip28_mrd=round(bip28, 1),
            kasse_2028_mrd=round(r28["kasse"] / 100 * bip28, 1),
            kasse_2028_eur_kopf_monat=round(r28["kasse"] / 100 * bip28 * 1e9 / D.POP[k] / 12, 1),
            verteidigung_2024_cofog=heute_v,
            rueckfall_2035_bei_stand_2024=round(max(0.0, r35["verteidigung"] - heute_v) * P["regel"]["rueckfall_faktor"], 2),
            mehr_als_quote_2035=round(max(0.0, heute_v - r35["verteidigung"]), 2)))
    # v4.16: Sicherheitskasse über einen festen Anteil der Mehrwertsteuer (Quellenabzug nach Vertrag, keine Verhandlung je Jahr)
    sicherheit = []
    for j in (2028, 2035, 2060):
        mwst = reihe_pj[j]["konsum"]
        v_j = round(v_ziel - (ziel - reihe_pj[j]["dach_ohne_zins"]), 2)
        for a in P["verteidigung_kassenanteile"]:
            sicherheit.append(dict(jahr=j, anteil_verteidigung=a, kasse_pct_bip=round(a * v_j, 2), mwst_pct_bip=mwst,
                                   anteil_der_mwst_pct=round(a * v_j / mwst * 100, 1)))
    E = dict(version=P["version"], status="Prüfrechnung", einheit="% des BIP, Klub der zehn; Euro nominal 2028",
             ziel_pflichtquote=ziel, reihe=reihe, aufgaben=tab, staaten=staaten, regel=P["regel"], sicherheitskasse_mwst=sicherheit,
             hinweis="Kassenanteile sind Annahmen (dach_beitrag.toml). Verteidigung heute: COFOG GF02 2024 (Eurostat gov_10a_exp), nicht "
                     "NATO-Abgrenzung. Rückfall 2035 = Betrag, den ein Staat in die Kasse zahlen müsste, wenn er seine Verteidigungsausgaben "
                     "auf dem Stand 2024 ließe und die übrigen Aufgaben voll erfüllte. Die Rechnung ändert weder Dividende noch Netz.")
    (AGG / "dach_beitrag.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in reihe:
        print(r)
    for s in staaten:
        print(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
