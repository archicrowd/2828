#!/usr/bin/env python3
"""Rentner: Varianten zur Regel E im Entwicklungsmodus (Logbuch v4.68). Vorläufige Prüfrechnung, kein Beschluss.

Ziel der Initiative (4.11.2026): hohe ungedeckte Zusagen treten im Sinne der Generationengerechtigkeit eher zurück; niedrige Zusagen (lange
Beitragszeiten, niedrige Erwartungen) kommen sicher ins Plus. Keine neuen Abgaben oder Sonderregeln; Regeln international übertragbar, daher
in Vielfachen des Grundbedarfs G des Staates statt in nationalen Beträgen.

Gerechnet mit dem Haushaltsmodell von rentner_kombi.py (Rentnerhaushalte Deutschland, EU-SILC 2025/ASID 2023, 2028, Kaufkraft 2026); nur die
Kürzungsfunktion der Zusage ändert sich. Je Variante: Anteil mit mehr, Mittel, Fünftel nach heutigem Haushaltsnetto, Entlastung des Fonds
(Kürzung − Kosten des Bodens) gegen Regel E.
Ausgabe: daten/aggregate/rentner_varianten.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path
import numpy as np

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "rentner_varianten.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("rk", W / "modell" / "rentner_kombi.py")
RK = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(RK)
M, A, DE, HL, H = RK.M, RK.A, RK.DE, RK.HL, RK.H
G = M.GB


def kuerzung(zusage, stufen):
    """Stufenweise Kürzung der Zusage je Person: stufen = [(ab Vielfachem von G, Satz), …], wie ein Tarif (Grenzsatz je Abschnitt)."""
    k = 0.0
    for i, (ab, s) in enumerate(stufen):
        bis = stufen[i + 1][0] if i + 1 < len(stufen) else None
        lo, hi = ab * G, (bis * G if bis else float("inf"))
        k += max(0.0, min(zusage, hi) - lo) * s
    return k


def neu(g, n, stufen, boden, kfun=None):
    """kfun(zusage) ersetzt die Stufenkürzung, wenn angegeben (v4.69: Freibetrag je Versicherungsjahr)."""
    p, an, b, v, e = (g * A[x] for x in ("grv", "andere", "bav", "privat", "erwerb"))
    zusage = p + an
    kb = kfun(zusage) if kfun else kuerzung(zusage, stufen)
    eink = zusage - kb + b + v + e + RK.P["weitergabe"] * H.ag(e)
    st = HL.stufen(eink, DE["tarif_stufen"], [0.0, 11.0, 19.0, 25.0, 33.0]) * n
    y = eink * n - st
    kon = HL.kq(y, "DE") * y
    fm, fb = HL.mwst_phi("DE", y)
    y = y - fm * kon * ((1 + M.EFF / 100) / (1 + HL.eff_alt("DE") / 100) - 1) - M.ZU / 100 * (st + fb * kon * M.EFF / (100 + M.EFF))
    bod = 12 * boden[n - 1]
    return max(y, bod), max(0.0, bod - y), kb * n


def main():
    R, gw = M.ziehe(np.random.default_rng(RK.P["seed"]), RK.P["stichprobe"], 18.0, 6.3)
    pre = []
    for r in R:
        nh = r["netto_2024"] * 1.06
        pre.append((M.brutto_aus_netto(nh / r["n"], A), max(nh, M.bedarf_heute(r["n"])), r["n"]))
    hs = np.array([h for _, h, _ in pre])
    grp = np.searchsorted(np.quantile(hs, [.2, .4, .6, .8]), hs)
    zp = np.array([g * (A["grv"] + A["andere"]) for g, _, _ in pre])            # Zusage je Person
    zgrp = np.searchsorted([1.0 * G, 1.5 * G, 2.0 * G, 3.0 * G], zp)              # Gruppen nach Zusage in Vielfachen von G
    boden = P["boden"]

    def rechne(stufen):
        d, auf, kb = (np.array(x) for x in zip(*[((y - h) / 12, a, c) for (g, h, n) in pre for y, a, c in [neu(g, n, stufen, boden)]]))
        return d, auf, kb

    def kennzahlen(name, stufen, d, auf, kb, ref):
        netto = float((gw * (kb - auf)).sum())
        return dict(name=name, stufen=stufen, anteil_mehr_pct=round(float(gw[d > 0].sum() / gw.sum() * 100), 1),
                    mittel_monat=round(float(np.average(d, weights=gw))),
                    fuenftel_monat=[round(float(np.average(d[grp == i], weights=gw[grp == i]))) for i in range(5)],
                    fuenftel_anteil_mehr_pct=[round(float(gw[(grp == i) & (d > 0)].sum() / gw[grp == i].sum() * 100)) for i in range(5)],
                    nach_zusage_monat={lab: round(float(np.average(d[zgrp == i], weights=gw[zgrp == i]))) if (zgrp == i).any() else None
                                       for i, lab in enumerate(["bis 1 G", "1–1,5 G", "1,5–2 G", "2–3 G", "über 3 G"])},
                    nach_zusage_anteil_mehr_pct={lab: round(float(gw[(zgrp == i) & (d > 0)].sum() / gw[zgrp == i].sum() * 100)) if (zgrp == i).any() else None
                                                 for i, lab in enumerate(["bis 1 G", "1–1,5 G", "1,5–2 G", "2–3 G", "über 3 G"])},
                    anteil_personen_je_zusage_pct={lab: round(float(gw[zgrp == i].sum() / gw.sum() * 100)) for i, lab in enumerate(["bis 1 G", "1–1,5 G", "1,5–2 G", "2–3 G", "über 3 G"])},
                    entlastung_fonds_mrd=round(netto / 1e9, 1),
                    gegen_E_mrd=None if ref is None else round((netto - ref) / 1e9, 1))

    erg, ref = [], None
    # Regel E zuerst (Bezug), dann die festen Varianten
    for v in P["variante"]:
        st = [tuple(x) for x in v["stufen"]]
        d, auf, kb = rechne(st)
        k = kennzahlen(v["name"], st, d, auf, kb, ref)
        if ref is None:
            ref = float((gw * (kb - auf)).sum())
            k["gegen_E_mrd"] = 0.0
        erg.append(k)
    # aufkommensneutral zu E: Schwelle T fest, Satz darüber so, dass die Entlastung des Fonds gleich bleibt
    for v in P["neutral"]:
        lo, hi = 0.0, 0.9
        for _ in range(40):
            s = (lo + hi) / 2
            st = [(0.0, 0.0), (v["schwelle"], s)] + ([(v["zweite_schwelle"], min(0.9, s * v["faktor_zweite"]))] if "zweite_schwelle" in v else [])
            d, auf, kb = rechne(st)
            netto = float((gw * (kb - auf)).sum())
            lo, hi = (lo, s) if netto > ref else (s, hi)
        k = kennzahlen(v["name"], [(a, round(b, 3)) for a, b in st], d, auf, kb, ref)
        erg.append(k)
    E = dict(version=P["version"], status="Entwicklungsmodus: vorläufige Prüfrechnung (Deutschland, 2028, Kaufkraft 2026), kein Beschluss",
             grundbedarf_jahr=round(G), boden_monat=boden, varianten=erg,
             hinweis="Kürzung je Person stufenweise auf die Zusage (gesetzliche Rente, Beamtenversorgung) in Vielfachen des Grundbedarfs G "
                     "(1.029 € im Monat); eigene Vorsorge und Erwerb ungekürzt. Fünftel nach heutigem Haushaltsnetto. Entlastung des Fonds = "
                     "Kürzung − Kosten des Bodens, nur 2028. Beitragsjahre sind in den Daten nicht enthalten.")
    (W / "daten" / "aggregate" / "rentner_varianten.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for x in erg:
        print(f"{x['name'][:58]:58} mehr {x['anteil_mehr_pct']:5}% Mittel {x['mittel_monat']:5} Fünftel {x['fuenftel_monat']} "
              f"Fonds {x['entlastung_fonds_mrd']:5} gegen E {x['gegen_E_mrd']}")
        print(" " * 60, x["nach_zusage_monat"], x["nach_zusage_anteil_mehr_pct"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
