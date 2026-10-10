#!/usr/bin/env python3
"""Übergangsrechnung 2028–2060: Dividende je Land unter gleichen Regeln (Logbuch v3.29).

Zwei Verteilungsregeln für denselben Klubtopf (Dividendenanteil am Klub-BIP je Jahr aus der Gesamtrechnung):
  V3a  geltend (v3.20): Topf nach Einwohnern x Preisniveau. Kaufkraft je Kopf in allen Ländern gleich, vom ersten Jahr an.
  V2B  Leitlinie v3.29: jedes Land erhält denselben Anteil am eigenen BIP je Kopf (gleiche Regel, nationaler Ausgangspunkt);
       Boden V3b (halbes Existenzminimum am Wohnort) als Solidarmechanismus. Liegt ein Land unter dem Boden, wird auf den
       Boden aufgestockt; die übrigen Länder tragen das anteilig (Topf bleibt gleich).
Angleichung: Szenarien mit beta-Konvergenz des realen Einkommens je Kopf und Preisniveau nach Balassa-Samuelson (epsilon).
Anreiz: Anteil eines zusätzlichen Euro BIP je Kopf eines Landes, der in seine eigene Dividende zurückfließt.

Kinder zur Hälfte, Anteil Minderjähriger wie Gesamtrechnung. Euro in Preisen 2028 (Klubpreisniveau 2028 konstant).
Eingänge: modell/uebergang.toml, gesamtrechnung.json, laendervarianten.json. Ausgabe: daten/aggregate/uebergang.json, .csv
Die Gesamtrechnung wird nicht verändert.
"""
import csv, json, math, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell/uebergang.toml").read_text(encoding="utf-8"))
GR = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
LV = {z["land"]: z for z in json.loads((AGG / "laendervarianten.json").read_text(encoding="utf-8"))["zeilen"]}
L = list(LV)
POP = {c: LV[c]["einwohner_mio"] for c in L}
PLI0 = {c: LV[c]["preisniveau"] for c in L}
KOPF0 = {c: LV[c]["bip_je_kopf_2028"] for c in L}          # Euro 2028, nominal = Preise 2028
JAHRE = GR["reihe_jahre"]
DIVQ = GR["reihe_div"]                                      # Dividendenanteil am Klub-BIP, % je Jahr
G = GR["g_real"]
K = GR["anteil_minderjaehrige"] / 100
ANKER, PLI_DE0 = GR["anker_de"], PLI0["DE"]
POPS = sum(POP.values())


def mittel(d, gew):
    return sum(d[c] * gew[c] for c in L) / sum(gew.values())


# epsilon: ln PLI = a + eps * ln(Realeinkommen je Kopf), Querschnitt 2028 ohne Irland (eigene Schätzung)
xs = [math.log(KOPF0[c] / PLI0[c]) for c in L if c != "IE"]
ys = [math.log(PLI0[c]) for c in L if c != "IE"]
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
EPS_SCH = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
EPS = EPS_SCH if P["epsilon"] == "schaetzung" else float(P["epsilon"])


def lauf(beta):
    real = {c: KOPF0[c] / PLI0[c] for c in L}                # Realeinkommen je Kopf (relative Kaufkraft)
    real0, pli = dict(real), dict(PLI0)
    pli_klub0 = mittel(PLI0, POP)
    reihe = []
    for t, (jahr, q) in enumerate(zip(JAHRE, DIVQ)):
        if t > 0:
            y_klub = mittel(real, POP)
            g_c = {c: G + beta * math.log(y_klub / real[c]) + P["delta"][c] / 100 for c in L}
            neu = {c: real[c] * (1 + g_c[c]) for c in L}
            # skalieren: Klub-Realeinkommen wächst mit g_real der Gesamtrechnung
            s = mittel(real, POP) * (1 + G) / mittel(neu, POP)
            real = {c: neu[c] * s for c in L}
            # Preisniveau relativ zum Klub nach Balassa-Samuelson; Klubpreisniveau bleibt (Preise 2028)
            rel = {c: (real[c] / real0[c]) / (mittel(real, POP) / mittel(real0, POP)) for c in L}
            roh = {c: PLI0[c] * rel[c] ** EPS for c in L}
            f = pli_klub0 / mittel(roh, POP)
            pli = {c: roh[c] * f for c in L}
        kopf = {c: real[c] * pli[c] for c in L}               # Euro je Kopf, Klubpreise 2028
        kopf_klub = mittel(kopf, POP)
        topf = q / 100 * kopf_klub * POPS                     # Mio Euro je Jahr (Mio Einwohner x Euro)
        erw = lambda je_kopf: je_kopf / 12 / (1 - K / 2)
        pli_klub = mittel(pli, POP)
        v3a = {c: erw(topf / POPS * pli[c] / pli_klub) for c in L}
        v2 = {c: erw(q / 100 * kopf[c]) for c in L}
        boden = {c: ANKER * pli[c] / PLI_DE0 for c in L}
        unten = {c for c in L if v2[c] < boden[c]}
        for _ in range(10):                                   # Aufstockung budgetneutral, iterativ
            bedarf = sum((boden[c] - v2[c]) * POP[c] for c in unten)
            oben = [c for c in L if c not in unten]
            basis = sum(v2[c] * POP[c] for c in oben)
            v2b = {c: (boden[c] if c in unten else v2[c] * (1 - bedarf / basis)) for c in L}
            neu_unten = unten | {c for c in oben if v2b[c] < boden[c]}
            if neu_unten == unten:
                break
            unten = neu_unten
        summe = sum(v2b[c] * POP[c] for c in L), sum(v3a[c] * POP[c] for c in L)
        if abs(summe[0] - summe[1]) > 1e-6 * summe[1]:
            sys.exit(f"{jahr}: V2B nicht budgetneutral")
        kk = {c: v2b[c] * pli_klub / pli[c] for c in L}       # Kaufkraft in Klubpreisen
        reihe.append(dict(jahr=jahr, pli=pli, real=real, v3a=v3a, v2b=v2b, boden=boden, aufgestockt=sorted(unten),
                          kaufkraft_v2b=kk, aufstockung_pct_topf=round(bedarf / (topf / 12 / (1 - K / 2)) * 100, 2) if topf else 0))
    return reihe


def main():
    # Selbstprüfung: ohne Angleichung reproduziert V3a die Länderdividende der Gesamtrechnung (2028, 2035, 2060)
    ref = {r["land"]: r for r in GR["tabelle_laender_div"]}
    basis = {r["jahr"]: r for r in lauf(0.0)}
    for j in (2028, 2035, 2060):
        for c in L:
            if abs(basis[j]["v3a"][c] - ref[c][f"e{j}"]) > 0.05:
                sys.exit(f"Selbstprüfung: V3a {c} {j} {basis[j]['v3a'][c]:.2f} gegen Gesamtrechnung {ref[c][f'e{j}']:.2f}")
    # Anreiz: Rückfluss eines zusätzlichen Euro BIP je Kopf in die eigene Dividende (2028)
    p28 = basis[2028]["pli"]
    anreiz_v3a = {c: POP[c] * p28[c] / sum(POP[x] * p28[x] for x in L) for c in L}
    E = dict(version=P["version"], einheit="Euro je Erwachsenem und Monat, Preise 2028 (Klubpreisniveau); Kinder zur Hälfte",
             epsilon_schaetzung=round(EPS_SCH, 3), epsilon_verwendet=round(EPS, 3),
             anreiz_rueckfluss_pct=dict(V3a={c: round(anreiz_v3a[c] * 100, 1) for c in L},
                                        V2B="100 % oberhalb des Bodens (abzüglich anteiliger Aufstockung); 0 % für Länder auf dem Boden"),
             szenarien={})
    zeilen = []
    for sz in P["szenario"]:
        r = {x["jahr"]: x for x in lauf(sz["beta"])}
        out = {}
        for j in P["jahre_ausgabe"]:
            x = r[j]
            out[str(j)] = dict(aufgestockt=x["aufgestockt"], aufstockung_pct_topf=x["aufstockung_pct_topf"],
                               laender={c: dict(v3a=round(x["v3a"][c], 2), v2b=round(x["v2b"][c], 2), boden=round(x["boden"][c], 2),
                                                kaufkraft_v2b=round(x["kaufkraft_v2b"][c], 2), preisniveau=round(x["pli"][c], 1))
                                        for c in L})
            for c in L:
                zeilen.append([sz["id"], j, c, round(x["pli"][c], 1), round(x["v3a"][c], 2), round(x["v2b"][c], 2),
                               round(x["boden"][c], 2), round(x["kaufkraft_v2b"][c], 2), int(c in x["aufgestockt"])])
        # Spreizung der Kaufkraft unter V2B (höchste / niedrigste, ohne Irland)
        for j in P["jahre_ausgabe"]:
            kk = {c: r[j]["kaufkraft_v2b"][c] for c in L if c != "IE"}
            out[str(j)]["spreizung_kaufkraft_ohne_ie"] = round(max(kk.values()) / min(kk.values()), 3)
        E["szenarien"][sz["id"]] = dict(beta=sz["beta"], jahre=out)
    (AGG / "uebergang.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(AGG / "uebergang.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["szenario", "jahr", "land", "preisniveau", "v3a_eur", "v2b_eur", "boden_eur", "kaufkraft_v2b", "aufgestockt"])
        w.writerows(zeilen)
    print(f"epsilon (Schätzung ohne IE) {EPS_SCH:.3f}; Rückfluss V3a: " + ", ".join(f"{c} {anreiz_v3a[c]*100:.1f} %" for c in L))
    for sid, s in E["szenarien"].items():
        print(f"--- {sid} (beta {s['beta']})")
        for j, x in s["jahre"].items():
            l = x["laender"]
            print(f" {j}: Spreizung KK {x['spreizung_kaufkraft_ohne_ie']} | aufgestockt {x['aufgestockt']} ({x['aufstockung_pct_topf']} % Topf) | "
                  + " ".join(f"{c} {l[c]['v2b']:.0f}/{l[c]['v3a']:.0f}" for c in L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
