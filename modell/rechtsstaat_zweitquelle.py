#!/usr/bin/env python3
"""Zweite Quelle für die Rechtsstaatsschwelle (Logbuch v4.92, v4.93): Rule of law (TTDI 2024) und Weltbank WGI 2025 gegen den WJP-Index.

Ausgabe: daten/aggregate/rechtsstaat_zweitquelle.json – Rangkorrelation (Spearman) über die Staaten mit beiden Werten, Werte für Schweiz und
Island (ohne WJP), Reihenfolge um die Schwelle 0,66.
"""
import csv
import hashlib
import json
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "rechtsstaat_zweitquelle.toml").read_text(encoding="utf-8"))
SA = tomllib.loads((W / "modell" / "staatenauswahl.toml").read_text(encoding="utf-8"))["staaten"]
F5 = tomllib.loads((W / "modell" / "fonds_5050.toml").read_text(encoding="utf-8"))


def raenge(x):
    o = sorted(x, key=lambda k: x[k])
    r = {}
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]:
            j += 1
        for k in o[i:j + 1]:
            r[k] = (i + j) / 2 + 1
        i = j + 1
    return r


def main():
    werte = dict(P["werte"])
    roh = W / P["datei"]
    geprueft = False
    if roh.exists():
        if hashlib.sha256(roh.read_bytes()).hexdigest() != P["sha256"]:
            raise SystemExit("Rohdatei weicht von der Prüfsumme ab")
        for r in csv.DictReader(roh.open(encoding="utf-8")):
            c = P["iso3"].get(r["REF_AREA"])
            if c and r["COMP_BREAKDOWN_1"] == "WEF_TTDI_VAL" and r["TIME_PERIOD"] == P["jahr"]:
                if abs(float(r["OBS_VALUE"]) - werte[c]) > 0.051:
                    raise SystemExit(f"Wert {c} weicht von der Datei ab")
        geprueft = True
    beide = [c for c in werte if c in SA and SA[c][0] >= 0]
    w = {c: SA[c][0] for c in beide}
    t = {c: werte[c] for c in beide}
    rw, rt = raenge(w), raenge(t)
    n = len(beide)
    mw = sum(rw.values()) / n
    mt = sum(rt.values()) / n
    kov = sum((rw[c] - mw) * (rt[c] - mt) for c in beide)
    sp = kov / (sum((rw[c] - mw) ** 2 for c in beide) * sum((rt[c] - mt) ** 2 for c in beide)) ** 0.5
    s = F5["schwelle_wjp"]
    um = sorted([c for c in beide if 0.58 <= w[c] <= 0.72], key=lambda c: -t[c])
    E = dict(version=P["version"], status="Prüfrechnung; zweite, nichtstaatliche Quelle", quelle="WEF TTDI 2024, Indikator WEF_TTDI_RULELAWIEF (Weltbank Data360)",
             rohdatei_geprueft=geprueft, staaten_mit_beiden_werten=n, spearman=round(sp, 3),
             ohne_wjp={c: werte[c] for c in ("CH", "IS")}, kleinster_wert_teilnehmer=min(t[c] for c in beide if w[c] >= s),
             groesster_wert_partner=max(t[c] for c in beide if w[c] < s),
             reihenfolge_um_schwelle=[dict(staat=c, wjp=w[c], ttdi=t[c], stufe="Teilnahme" if w[c] >= s else "Partner") for c in um])
    # v4.93: Weltbank WGI als amtliche zweite Quelle
    G = P["wgi"]
    gw = dict(G["werte"])
    rohg = W / G["datei"]
    if rohg.exists():
        if hashlib.sha256(rohg.read_bytes()).hexdigest() != G["sha256"]:
            raise SystemExit("WGI-Rohdatei weicht von der Prüfsumme ab")
        for r in csv.DictReader(rohg.open(encoding="utf-8")):
            c = P["iso3"].get(r["REF_AREA"])
            if c and r["TIME_PERIOD"] == G["jahr"] and r["OBS_VALUE"] and abs(float(r["OBS_VALUE"]) - gw[c]) > 0.0006:
                raise SystemExit(f"WGI-Wert {c} weicht von der Datei ab")
    b2 = [c for c in gw if c in SA and SA[c][0] >= 0]
    r1, r2 = raenge({c: SA[c][0] for c in b2}), raenge({c: gw[c] for c in b2})
    m1, m2 = sum(r1.values()) / len(b2), sum(r2.values()) / len(b2)
    sp2 = sum((r1[c] - m1) * (r2[c] - m2) for c in b2) / (sum((r1[c] - m1) ** 2 for c in b2) * sum((r2[c] - m2) ** 2 for c in b2)) ** 0.5
    teil = [c for c in gw if c in SA and (SA[c][0] >= s or c in F5["ohne_wert_teilnahme"])]
    part = [c for c in gw if c in SA and 0 <= SA[c][0] < s]
    E["wgi"] = dict(quelle="Weltbank, Worldwide Governance Indicators, Rule of Law: Estimate (WDI über Data360)", jahr=G["jahr"],
                    rohdatei_geprueft=rohg.exists(), staaten_mit_beiden_werten=len(b2), spearman=round(sp2, 3),
                    ohne_wjp={c: gw[c] for c in ("CH", "IS")}, kleinster_teilnehmer=min((gw[c], c) for c in teil),
                    groesster_partner=max((gw[c], c) for c in part),
                    trennt_sauber=min(gw[c] for c in teil) > max(gw[c] for c in part))
    print("WGI:", E["wgi"])
    (W / "daten" / "aggregate" / "rechtsstaat_zweitquelle.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Spearman {sp:.3f} (n = {n}), CH/IS {E['ohne_wjp']}, kleinster Teilnehmer {E['kleinster_wert_teilnehmer']}, größter Partner {E['groesster_wert_partner']}")
    for r in E["reihenfolge_um_schwelle"]:
        print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
