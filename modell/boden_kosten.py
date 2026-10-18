#!/usr/bin/env python3
"""Kosten der Regel „Grundbedarf als Boden, eigenes Einkommen zur Hälfte“ je Land, geschätzt aus veröffentlichten Verteilungstabellen (Logbuch v4.6).

Weil der Boden mit der OECD-modifizierten Skala gebildet wird, ist er je Äquivalenzerwachsenem genau der Grundbedarf G. Damit lässt sich die
Aufstockung je Äquivalenzerwachsenem aus der Dezilverteilung des äquivalenzgewichteten verfügbaren Einkommens Y (EU-SILC) schätzen:
    Aufstockung = max(0, G − D_ä − ½ · E),   E = eigenes Einkommen je Äquivalenzerwachsenem,   D_ä = Dividenden je Äquivalenzerwachsenem.
Heutiges Y enthält Transfers; deshalb ein Band: E = Y (untere Schätzung der Kosten) bzw. E = ½ · Y in den untersten zwei Dezilen (obere).
Die Verteilung innerhalb der Dezile ist linear (D1 ab 0,4 × D1). Nur Haushalte im Erwerbsalter (Rentner über Altrenten und Mindestrente).
Verglichen wird mit dem Budget des Netzes für Grundbedarfsleistungen im Erwerbsalter: Härtefall + Arbeitslosigkeit + Invalidität (2028).
Ausgabe: daten/aggregate/boden_kosten.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "boden_kosten.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("rb", W / "modell" / "regel_boden.py")
RB = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(RB)
MR = json.loads((AGG / "moeglichkeitsraum33.json").read_text(encoding="utf-8"))
MR24 = json.loads((AGG / "moeglichkeitsraum_2024.json").read_text(encoding="utf-8"))
LS = RB.SL.HL.LS


def punkte(c):
    """Stützpunkte der Verteilung (Anteil, Einkommen) in Preisen 2026."""
    f = P["fortschreibung_2024_2026"][c]
    d = [x * f for x in P["dezile"][c]]
    return [(0.0, P["untergrenze_d1"] * d[0])] + [(0.1 * (i + 1), x) for i, x in enumerate(d)]


def kosten(c, eigen_unten):
    fx = RB.SL.HL.faktor(c)
    g = LS["staaten"][c]["grundbedarf_jahr_eur"] * fx
    d = LS["staaten"][c]["dividende_erw_eur"][0] * 12 * fx * RB.topf(RB.S)
    d_ae = d * P["personen_je_aequivalent"] * (1 - RB.SL.K + RB.S * RB.SL.K)
    pk = punkte(c)
    schritte, summe, betroffen = 400, 0.0, 0.0
    for i in range(schritte):                       # Integration über die unteren 90 %
        q = (i + 0.5) / schritte * 0.9
        j = int(q / 0.1)
        (q0, y0), (q1, y1) = pk[j], pk[j + 1]
        y = y0 + (y1 - y0) * (q - q0) / (q1 - q0)
        e = y * (eigen_unten if q < 0.2 else 1.0)
        a = max(0.0, g - d_ae - RB.P["anrechnung"] * e)
        summe += a * 0.9 / schritte
        betroffen += (0.9 / schritte) if a > 0 else 0.0
    ew = float(RB.SL.HL.LS["staaten"][c].get("einwohner_mio", 0)) or MR["laender"][c]["einwohner_mio"]
    aequiv = ew * 1e6 * P["anteil_erwerbsalter"] / P["personen_je_aequivalent"]
    mrd = summe * aequiv / 1e9 / fx                  # in Mrd. € (PL umgerechnet)
    bip = MR24["bip_mio_eur"][c] / 1000 * P["bip_fortschreibung"]
    return dict(mrd_eur=round(mrd, 1), pct_bip=round(100 * mrd / bip, 2), anteil_mit_aufstockung=round(100 * betroffen), grundbedarf=round(g),
                dividenden_je_aequivalent=round(d_ae))


def main():
    erg = {}
    for c in ("DE", "FR", "IT", "ES", "PL"):
        n = MR["laender"][c]["z2028"]["netz"]
        budget = n["Härtefall"] + n["Arbeitslosigkeit"] + n["Invalidität"]
        lo, hi = kosten(c, P["eigenanteil_unten"][1]), kosten(c, P["eigenanteil_unten"][0])
        median = P["dezile"][c][4] * P["fortschreibung_2024_2026"][c]
        erg[c] = dict(grundbedarf_zu_median_pct=round(100 * lo["grundbedarf"] / median), untere_schaetzung=lo, obere_schaetzung=hi, budget_pct_bip=round(budget, 2),
                      budget_haertefall_pct_bip=n["Härtefall"],
                      dividende_je_erw_eur_bei_ueberschreitung=round(max(0.0, hi["pct_bip"] - budget) * LS["staaten"][c]["dividende_erw_eur"][0]
                                                                    / LS["staaten"][c]["dividende_pct_bip"][0], 1))
    E = dict(version=P["version"], status="Prüfrechnung, grob", quelle=P["quelle"], staaten=erg,
             hinweis="Kosten der Aufstockung für Haushalte im Erwerbsalter, 2028, Preise 2026. Band aus der Annahme über Transfers in D1–D2. "
                     "Budget: Härtefall + Arbeitslosigkeit + Invalidität des Netzes (moeglichkeitsraum33, 2028).")
    (AGG / "boden_kosten.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in erg.items():
        print(c, "Kosten", x["untere_schaetzung"]["pct_bip"], "–", x["obere_schaetzung"]["pct_bip"], "% BIP (",
              x["untere_schaetzung"]["mrd_eur"], "–", x["obere_schaetzung"]["mrd_eur"], "Mrd. €), betroffen",
              x["untere_schaetzung"]["anteil_mit_aufstockung"], "–", x["obere_schaetzung"]["anteil_mit_aufstockung"], "% | Budget", x["budget_pct_bip"],
              "| G", x["untere_schaetzung"]["grundbedarf"], "D_ä", x["untere_schaetzung"]["dividenden_je_aequivalent"],
              "| Dividende −", x["dividende_je_erw_eur_bei_ueberschreitung"], "| G/Median", x["grundbedarf_zu_median_pct"], "%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
