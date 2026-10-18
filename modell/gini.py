#!/usr/bin/env python3
"""Gini-Koeffizient des äquivalenzgewichteten verfügbaren Einkommens heute und im neuen System, je Land und Jahr (Logbuch v4.8). Prüfrechnung, statisch.

Verfahren:
  1. Verteilung heute aus EU-SILC 2025: Dezilgrenzen D1–D9 (ilc_di01), innerhalb der Dezile linear; unterstes Dezil von L bis D1, oberstes Dezil
     Pareto ab D9; L und der Pareto-Exponent so, dass die amtlichen Anteile von D1 und D10 getroffen werden. Gini dieser Rekonstruktion gegen den
     amtlichen Wert (ilc_di12) als Probe.
  2. Abbildung heute → neu je Äquivalenzerwachsenem: Bruttolohn b so, dass das heutige Netto einer alleinstehenden Person (mit Bedarfsleistungen,
     sozial_laender) dem Punkt entspricht; neu = Regel Boden (regel_boden) mit den Dividenden je Äquivalenzerwachsenem (wie boden_kosten) und dem
     Boden je Äquivalenzerwachsenem (Kindergewicht nach regel_boden.toml). Punkte unter dem heutigen Mindestnetto: ohne Lohn, eigenes Einkommen
     = heutiges Einkommen (untere Schätzung der Wirkung: voll; obere: zur Hälfte, Rest heutige Transfers) – dasselbe Band wie boden_kosten.
  3. Ausgewiesen wird der amtliche Gini plus die Modelländerung (neu − Rekonstruktion heute), damit Rekonstruktionsfehler nicht als Wirkung erscheinen.
Variante: ein Viertel der Bevölkerung (Rentnerhaushalte) unverändert. Nicht enthalten: Verhaltensänderungen, Kapitaleinkommen, Vermögen, Preise.
Ausgabe: daten/aggregate/gini.json
"""
import contextlib, importlib.util, io, json, math, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "gini.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("bk", W / "modell" / "boden_kosten.py")
BK = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(BK)
RB, SL = BK.RB, BK.RB.SL
N = P["punkte_je_dezil"]


def gini(ys):
    y = sorted(ys)
    n, s = len(y), sum(y)
    return 100 * (2 * sum((i + 1) * v for i, v in enumerate(y)) / (n * s) - (n + 1) / n)


def verteilung(c):
    f = BK.P["fortschreibung_2024_2026"][c]
    d = [x * f for x in BK.P["dezile"][c]]
    u = [(i + 0.5) / N for i in range(N)]
    mitte = [[d[i] + (d[i + 1] - d[i]) * t for t in u] for i in range(8)]          # D2–D9
    M = sum(sum(m) / N for m in mitte)
    s1, s10 = P["anteil_d1"][c] / 100, P["anteil_d10"][c] / 100
    S = M / (1 - s1 - s10)
    m1, m10 = s1 * S, s10 * S
    L = max(0.0, 2 * m1 - d[0])
    d1 = [L + (d[0] - L) * t for t in u]
    lo, hi = 1.05, 20.0                                                               # Pareto-Exponent: Stichprobenmittel = m10
    for _ in range(60):
        a = (lo + hi) / 2
        m = sum(d[8] * (1 - t) ** (-1 / a) for t in u) / N
        lo, hi = (a, hi) if m > m10 else (lo, a)
    d10 = [d[8] * (1 - t) ** (-1 / a) for t in u]
    return d1 + [x for m in mitte for x in m] + d10, dict(untergrenze_d1=round(L), pareto_exponent=round(a, 2))


def umkehr(c):
    """Raster b → heutiges Netto (alleinstehend), monoton gemacht."""
    fx = SL.HL.faktor(c)
    bs = [100 * fx * 1.03 ** i for i in range(420)]
    hs, m = [], 0.0
    for b in bs:
        m = max(m, SL.heute(c, b, 1, 0))
        hs.append(m)
    return bs, hs


def lohn_zu(y, bs, hs):
    if y <= hs[0]:
        return None
    for i in range(1, len(hs)):
        if hs[i] >= y:
            t = (y - hs[i - 1]) / (hs[i] - hs[i - 1]) if hs[i] > hs[i - 1] else 1.0
            return bs[i - 1] + t * (bs[i] - bs[i - 1])
    return bs[-1] * (y / hs[-1])


def neu_punkt(c, y, b, j, eu, g_ae, cache):
    d1 = RB.dividenden(c, 1, 0, j)
    d_ae = d1 * BK.P["personen_je_aequivalent"] * (1 - SL.K + RB.S * SL.K)
    if b is None:
        e = y * eu
        return d_ae + e + max(0.0, g_ae - d_ae - RB.P["anrechnung"] * e)
    key = (round(b), j)
    if key not in cache:
        r, auf = RB.neu(c, b, 1, 0, j, detail=True)
        cache[key] = r - auf
    x = cache[key] - d1 + d_ae
    return x + max(0.0, g_ae - d_ae - RB.P["anrechnung"] * max(0.0, x - d_ae))


def land(c):
    ys, kal = verteilung(c)
    g_heute = gini(ys)
    bs, hs = umkehr(c)
    lohn = [lohn_zu(y, bs, hs) for y in ys]
    g_ae = SL.HL.LS["staaten"][c]["grundbedarf_jahr_eur"] * SL.HL.faktor(c) * BK.boden_faktor(RB.P["skala"]["kind"])
    amt = P["gini_amtlich_2025"][c]
    q = P["anteil_rentner"]
    reihe, cache = [], {}
    for j in P["jahre"]:
        z = dict(jahr=j)
        for name, eu in (("untere", BK.P["eigenanteil_unten"][1]), ("obere", BK.P["eigenanteil_unten"][0])):
            yn = [neu_punkt(c, y, b, j, eu, g_ae, cache) for y, b in zip(ys, lohn)]
            g_neu = gini(yn)
            nr = max(1, round(1 / q))                                                # jeder vierte Punkt unverändert (Rentnervariante)
            g_mix = gini([y if i % nr == 0 else v for i, (y, v) in enumerate(zip(ys, yn))])
            z[name] = dict(gini=round(amt + g_neu - g_heute, 1), gini_rentner_unveraendert=round(amt + g_mix - g_heute, 1))
        z["mitte"] = round((z["untere"]["gini"] + z["obere"]["gini"]) / 2, 1)
        reihe.append(z)
    return dict(gini_amtlich_2025=amt, gini_rekonstruktion_heute=round(g_heute, 1), kalibrierung=kal, reihe=reihe)


def main():
    E = dict(version=P["version"], status="Prüfrechnung, statisch", quelle=P["quelle"], kindergewicht=RB.P["skala"]["kind"],
             vergleich_amtlich_2025={k: v for k, v in P["gini_amtlich_2025"].items() if k in ("DK", "SE")},
             staaten={c: land(c) for c in ("DE", "FR", "IT", "ES", "PL")},
             hinweis="Gini in Punkten (0–100) des äquivalenzgewichteten verfügbaren Einkommens. Neu = amtlicher Wert 2025 + Modelländerung. "
                     "Band aus der Annahme über Transfers in den unteren Dezilen; Variante mit unveränderten Rentnerhaushalten (25 %). "
                     "Statisch: heutige Verteilung, keine Verhaltensänderung, ohne Kapitaleinkommen.")
    (AGG / "gini.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in E["staaten"].items():
        print(c, "amtlich", x["gini_amtlich_2025"], "Rekonstruktion", x["gini_rekonstruktion_heute"], x["kalibrierung"])
        for z in x["reihe"]:
            print("   ", z["jahr"], "mitte", z["mitte"], "| untere", z["untere"], "| obere", z["obere"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
