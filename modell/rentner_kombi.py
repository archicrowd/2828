#!/usr/bin/env python3
"""Rentner: „Grundbedarf garantiert, Zusagen darüber gekürzt“ (Logbuch v4.24). Vorschlag, Prüfrechnung.

Regel (Vorschlag E): 1. Kein Rentnerhaushalt fällt unter die heutige Grundsicherung (1.083 € allein, 1.632 € Paar).
2. Zusagen ohne eigene Deckung (gesetzliche Rente, Beamtenversorgung) werden auf den Teil über dem Grundbedarf (1.029 € je Person) gekürzt.
3. Eigene Vorsorge (Betriebsrente, private Vorsorge) und Erwerb werden nicht gekürzt; alle Einkommen werden nach 33R besteuert.
Rentnerhaushalte aus mikro_rentner_de (EU-SILC 2025, ASID 2023). Vergleich mit dem Beschluss (A). Netto für den Staat = Kürzung − Boden.
Ausgabe: daten/aggregate/rentner_kombi.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path
import numpy as np

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "rentner_kombi.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("mr", W / "modell" / "mikro_rentner_de.py")
M = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(M)
A, DE, HL, H = M.ANTEILE, M.DE, M.HL, M.H


def neu(g, n, satz, boden, ueber):
    p, an, b, v, e = (g * A[x] for x in ("grv", "andere", "bav", "privat", "erwerb"))
    zusage = p + an
    kb = max(0.0, zusage - M.GB) * satz if ueber else zusage * satz
    eink = zusage - kb + b + v + e + P["weitergabe"] * H.ag(e)
    st = HL.stufen(eink, DE["tarif_stufen"], [0.0, 11.0, 19.0, 25.0, 33.0]) * n
    y = eink * n - st
    kon = HL.kq(y, "DE") * y
    y = y - kon * ((1 + M.EFF / 100) / (1 + HL.eff_alt("DE") / 100) - 1) - M.ZU / 100 * (st + kon * M.EFF / (100 + M.EFF))
    bod = 12 * boden[n - 1]
    return max(y, bod), max(0.0, bod - y), kb * n


def main():
    R, gw = M.ziehe(np.random.default_rng(P["seed"]), P["stichprobe"], 18.0, 6.3)
    pre = []
    for r in R:
        nh = r["netto_2024"] * 1.06
        pre.append((M.brutto_aus_netto(nh / r["n"], A), max(nh, M.bedarf_heute(r["n"])), r["n"]))
    hs = np.array([h for _, h, _ in pre])
    grp = np.searchsorted(np.quantile(hs, [.2, .4, .6, .8]), hs)
    sing = np.array([n == 1 for _, _, n in pre])
    erg, basis = [], None
    for v in P["variante"]:
        d, auf, kb = (np.array(x) for x in zip(*[((y - h) / 12, a, c) for (g, h, n) in pre for y, a, c in [neu(g, n, v["satz"], v["boden"], v["ueber_grundbedarf"])]]))
        netto = float((gw * (kb - auf)).sum())
        basis = netto if basis is None else basis
        erg.append(dict(name=v["name"], anteil_mehr_pct=round(float(gw[d > 0].sum() / gw.sum() * 100), 1),
                        mittel_monat=round(float(np.average(d, weights=gw))), allein=round(float(np.average(d[sing], weights=gw[sing]))),
                        paar=round(float(np.average(d[~sing], weights=gw[~sing]))),
                        fuenftel_monat=[round(float(np.average(d[grp == i], weights=gw[grp == i]))) for i in range(5)],
                        fuenftel_pct_netto=[round(float(np.average(d[grp == i] * 12 / hs[grp == i], weights=gw[grp == i]) * 100), 1) for i in range(5)],
                        kuerzung_mrd=round(float((gw * kb).sum() / 1e9), 1), boden_mrd=round(float((gw * auf).sum() / 1e9), 1),
                        gegen_beschluss_mrd=round((netto - basis) / 1e9, 1), gegen_beschluss_pct_bip=round((netto - basis) / 1e9 / P["bip_2028_mrd"] * 100, 2)))
    E = dict(version=P["version"], status="Vorschlag, Prüfrechnung (2028, Kaufkraft 2026)", varianten=erg,
             hinweis="Fünftel nach heutigem Haushaltsnetto der Rentnerhaushalte. Zusammensetzung der Alterseinkommen gleich über alle Einkommen "
                     "(ASID, Annahme); Beamtenversorgung als Zusage behandelt (Annahme). Kosten nur für 2028; der Bestand sinkt mit der Zeit.")
    (W / "daten" / "aggregate" / "rentner_kombi.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for x in erg:
        print(x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
