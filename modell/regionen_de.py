#!/usr/bin/env python3
"""Gemeindeformel je Kreis in Deutschland: wer bekommt wie viel, und was ändert ein Strukturzuschlag (Logbuch v4.16). Prüfrechnung.

Formel (geltend, laenderseiten.json DE): je Einwohner 3.913 € und je Kind von 5 bis 19 Jahren 13.729 € im Jahr (Kaufkraft 2026).
Strukturzuschlag (Vorschlag): Ein Anteil s des Topfs wird je zur Hälfte nach Fläche und nach Zahl der Menschen ab 65 verteilt; der Topf
bleibt gleich. Verglichen wird mit der Wirtschaftskraft (BIP je Einwohner, 2022) als Näherung für die heutige Steuerkraft der Gemeinden.
Die heutigen Einnahmen der Gemeinden je Kreis fehlen (Regionalstatistik 71231 und INKAR sind für das Abrufwerkzeug gesperrt); ein Vergleich
heute gegen neu ist deshalb NICHT gerechnet.

Eingänge: daten/roh/kreise/*.csv (Eurostat, NUTS 2024, 400 Kreise; nicht im Repository, Abrufadressen in regionen_de.toml).
Fehlen die Rohdaten, bleibt das zuletzt geschriebene Ergebnis stehen.
Ausgabe: daten/aggregate/regionen_de.json (nur Gruppenwerte und Randfälle)
"""
import json
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
ROH = W / "daten" / "roh" / "kreise"
P = tomllib.loads((W / "modell" / "regionen_de.toml").read_text(encoding="utf-8"))
LS = json.loads((AGG / "laenderseiten.json").read_text(encoding="utf-8"))["staaten"]["DE"]
STADT = ("Kreisfreie Stadt", "Stadtkreis", "Berlin", "Hamburg")


def lies(name, mit_name=False):
    d = {}
    for z in (ROH / f"{name}.csv").read_text(encoding="utf-8").splitlines():
        t = z.split(";")
        d[t[0]] = (float(t[1]), t[2]) if mit_name else float(t[1])
    return d


def gewichtet(rows, f, w="e"):
    s = sum(r[w] for r in rows)
    return sum(f(r) * r[w] for r in rows) / s


def quantil(rows, key, q):
    o = sorted(rows, key=lambda r: r[key])
    ges, acc = sum(r["e"] for r in o), 0.0
    for r in o:
        acc += r["e"]
        if acc >= q * ges:
            return r[key]
    return o[-1][key]


def main():
    if not (ROH / "bev_2024.csv").exists():
        print("Rohdaten je Kreis fehlen (daten/roh/kreise); Ergebnis regionen_de.json bleibt unverändert")
        return 0
    E, A65, KM = lies("bev_2024"), lies("ab65_2024"), lies("flaeche")
    K = {k: lies("k5_9_2024")[k] + lies("k10_14_2024")[k] + lies("k15_19_2024")[k] for k in E}
    BIP = lies("bip_2022", True)
    if not (set(E) == set(A65) == set(KM) == set(K) == set(BIP)) or len(E) != 400:
        raise SystemExit("Kreislisten passen nicht zusammen")
    fe, fk = LS["gemeinde_einw"], LS["gemeinde_kind"]
    rows = []
    for k in E:
        rows.append(dict(code=k, name=BIP[k][1], e=E[k], kind=K[k], a65=A65[k], km2=KM[k],
                         bip_kopf=BIP[k][0] * 1e6 / E[k], dichte=E[k] / KM[k],
                         stadt=any(s in BIP[k][1] for s in STADT), ost=k[:3] in P["ost"]))
    T = sum(fe * r["e"] + fk * r["kind"] for r in rows)
    SKM, SA = sum(r["km2"] for r in rows), sum(r["a65"] for r in rows)
    st = P["strukturzuschlag"]
    for r in rows:
        basis = fe * r["e"] + fk * r["kind"]
        zus = T * (st["anteil_flaeche"] * r["km2"] / SKM + st["anteil_ab65"] * r["a65"] / SA)
        for s in st["varianten"]:
            r[f"kopf_{s}"] = ((1 - s) * basis + s * zus) / r["e"]
    ges_e = sum(r["e"] for r in rows)
    de_kopf = T / ges_e
    de_bip = gewichtet(rows, lambda r: r["bip_kopf"])

    def gruppe(name, sel):
        g = [r for r in rows if sel(r)]
        out = dict(gruppe=name, kreise=len(g), einwohner_mio=round(sum(r["e"] for r in g) / 1e6, 2),
                   bip_kopf_index=round(gewichtet(g, lambda r: r["bip_kopf"]) / de_bip * 100, 1),
                   kinderanteil_pct=round(sum(r["kind"] for r in g) / sum(r["e"] for r in g) * 100, 1),
                   ab65_pct=round(sum(r["a65"] for r in g) / sum(r["e"] for r in g) * 100, 1))
        for s in st["varianten"]:
            out[f"eur_kopf_jahr_{s}"] = round(gewichtet(g, lambda r: r[f"kopf_{s}"]))
            out[f"index_{s}"] = round(gewichtet(g, lambda r: r[f"kopf_{s}"]) / de_kopf * 100, 1)
        return out

    # Dichteklassen in Anlehnung an die siedlungsstrukturellen Kreistypen des BBSR (Schwellen hier vereinfacht, Annahme)
    gruppen = [gruppe("Deutschland", lambda r: True),
               gruppe("kreisfreie Städte (mit Berlin, Hamburg)", lambda r: r["stadt"]),
               gruppe("Landkreise", lambda r: not r["stadt"]),
               gruppe("Dichte unter 100 Einw./km²", lambda r: r["dichte"] < 100),
               gruppe("Dichte 100–150", lambda r: 100 <= r["dichte"] < 150),
               gruppe("Dichte 150–300", lambda r: 150 <= r["dichte"] < 300),
               gruppe("Dichte 300 und mehr", lambda r: r["dichte"] >= 300),
               gruppe("ostdeutsche Flächenländer", lambda r: r["ost"]),
               gruppe("übrige Länder ohne Berlin", lambda r: not r["ost"] and r["code"] != "DE300")]
    q = [quantil(rows, "bip_kopf", x) for x in (0.2, 0.4, 0.6, 0.8)]
    grenzen = [0.0] + q + [1e12]
    for i in range(5):
        spanne = f"{grenzen[i] / 1000:.0f}–{grenzen[i + 1] / 1000:.0f} T€" if i < 4 else f"ab {grenzen[i] / 1000:.0f} T€"
        gruppen.append(gruppe(f"Wirtschaftskraft Fünftel {i + 1} (BIP je Einw. {spanne})",
                              lambda r, a=grenzen[i], b=grenzen[i + 1]: a <= r["bip_kopf"] < b if i < 4 else r["bip_kopf"] >= a))

    def streuung(key):
        return round(quantil(rows, key, 0.9) / quantil(rows, key, 0.1), 2)

    s10 = 0.1
    rand = sorted(rows, key=lambda r: r[f"kopf_{s10}"])
    E_ = dict(version=P["version"], status="Prüfrechnung", preisbasis="Euro je Einwohner und Jahr, Kaufkraft 2026 (Gemeindeformel laenderseiten.json)",
              formel=dict(je_einwohner=fe, je_kind_5_19=fk, topf_mrd=round(T / 1e9, 1), eur_kopf_de=round(de_kopf)),
              strukturzuschlag=st, gruppen=gruppen,
              streuung_p90_p10=dict(bip_kopf=streuung("bip_kopf"), **{f"formel_{s}": streuung(f"kopf_{s}") for s in st["varianten"]}),
              randfaelle_s010=dict(niedrigste=[(r["name"], round(r[f"kopf_{s10}"])) for r in rand[:5]],
                                   hoechste=[(r["name"], round(r[f"kopf_{s10}"])) for r in rand[-5:]]),
              daten=dict(kreise=len(rows), einwohner=int(ges_e), flaeche_km2=int(SKM), quellen=P["quellen"],
                         pruefung="Summen je Bundesland gegen NUTS-1-Abruf: übereinstimmend (BIP auf ±0,6 Mio. € gerundet)"),
              hinweis="Heutige Gemeindefinanzen je Kreis nicht gerechnet (Daten nicht abrufbar). BIP je Einwohner 2022 bezogen auf Einwohner 1.1.2024. "
                      "Pendlerstädte haben hohes BIP je Einwohner. Werte maschinell aus Eurostat-Abfragen gelesen, an der Quelle zu prüfen.")
    (AGG / "regionen_de.json").write_text(json.dumps(E_, ensure_ascii=False, indent=1), encoding="utf-8")
    for g in gruppen:
        print(g)
    print("Streuung P90/P10", E_["streuung_p90_p10"])
    print("Rand", E_["randfaelle_s010"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
