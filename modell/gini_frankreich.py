#!/usr/bin/env python3
"""Warum steigt der Gini in Frankreich, und warum sinkt er in Polen so stark? Zerlegung und Gegenproben (Logbuch v4.9). Prüfrechnung.

Gegenproben zur Rechnung modell/gini.py (Kindergewicht nach regel_boden.toml, 2028):
  A  Gewinn je Lohnstufe (alleinstehend): heute, neu, Arbeitgeberbeiträge, Weitergabe – wo entsteht der Gewinn?
  B  Weitergabe gedeckelt: Arbeitgeberbeiträge zählen für die 80-%-Weitergabe nur bis zum Betrag beim 1- bzw. 1,5-fachen Durchschnittslohn
     (Frankreich kennt für Kranken- und Familienbeiträge keine Bemessungsgrenze; Deutschland deckelt bei der BBG).
  C  Abbildung über einen Familienhaushalt (Paar, ein Einkommen, 2 Kinder) statt über eine alleinstehende Person – prüft, ob die Delle beim
     SMIC (Wegfall prime d'activité, keine Arbeitgeberbeiträge wegen RGDU) durch die Abbildung in die mittleren Dezile gerät.
  D  Kenngrößen je Land: Dividende je Erwachsenem / Median, Boden / Median, Netz in % BIP.
Ausgabe: daten/aggregate/gini_frankreich.json
"""
import contextlib, importlib.util, io, json
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
spec = importlib.util.spec_from_file_location("gini", W / "modell" / "gini.py")
G = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(G)
BK, RB, SL = G.BK, G.RB, G.SL
LAENDER = ("DE", "FR", "IT", "ES", "PL")
MR = json.loads((AGG / "moeglichkeitsraum33.json").read_text(encoding="utf-8"))["laender"]


def gini_2028(c, eu=1.0):
    """Gini 2028 (amtlich + Modelländerung) wie gini.py, Mitte des Bands ist bei eu=0,75 nicht definiert – hier eine Annahme je Aufruf."""
    ys, _ = G.verteilung(c)
    bs, hs = G.umkehr(c)
    lohn = [G.lohn_zu(y, bs, hs) for y in ys]
    g_ae = SL.HL.LS["staaten"][c]["grundbedarf_jahr_eur"] * SL.HL.faktor(c) * BK.boden_faktor(RB.P["skala"]["kind"])
    yn = [G.neu_punkt(c, y, b, 2028, eu, g_ae, {}) for y, b in zip(ys, lohn)]
    return round(G.P["gini_amtlich_2025"][c] + G.gini(yn) - G.gini(ys), 2), ys, yn


def gini_familie(c, eu=1.0):
    """Abbildung über Paar + 2 Kinder (Skala 2,1): heutiges Haushaltsnetto / 2,1 = Punkt; neu = RB.neu(Paar + 2) / 2,1."""
    ys, _ = G.verteilung(c)
    fx = SL.HL.faktor(c)
    bs = [100 * fx * 1.03 ** i for i in range(420)]
    hs, m = [], 0.0
    for b in bs:
        m = max(m, SL.heute(c, b, 2, 2) / 2.1)
        hs.append(m)
    d, F = RB.dividenden(c, 2, 2), RB.boden(c, 2, 2)
    yn = []
    for y in ys:
        b = G.lohn_zu(y, bs, hs)
        if b is None:
            e = y * 2.1 * eu
            yn.append((d + e + max(0.0, F - d - RB.P["anrechnung"] * e)) / 2.1)
        else:
            yn.append(RB.neu(c, b, 2, 2) / 2.1)
    return round(G.P["gini_amtlich_2025"][c] + G.gini(yn) - G.gini(ys), 2)


def mit_deckel(c, faktor):
    aw = SL.HL.P["oecd"]["durchschnittslohn"][c]
    alt = SL.ag
    deckel = alt(c, faktor * aw)
    SL.ag = lambda cc, b: min(alt(cc, b), deckel) if cc == c else alt(cc, b)
    try:
        return gini_2028(c)[0]
    finally:
        SL.ag = alt


def stufen(c):
    aw = SL.HL.P["oecd"]["durchschnittslohn"][c]
    out = []
    for f in (0.3, 0.5, 0.75, 1, 1.5, 2, 3, 5, 8):
        b = f * aw
        h, n, a = SL.heute(c, b, 1, 0), RB.neu(c, b, 1, 0), SL.ag(c, b)
        out.append(dict(lohn_x_durchschnitt=f, brutto=round(b), ag_beitraege_pct_brutto=round(100 * a / b, 1),
                        heute_pct_brutto=round(100 * h / b, 1), neu_pct_brutto=round(100 * n / b, 1), aenderung_pct=round(100 * (n / h - 1), 1)))
    return out


def dezile(c):
    g, ys, yn = gini_2028(c)
    n = len(ys) // 10
    return [round(100 * (sum(yn[i * n:(i + 1) * n]) / sum(ys[i * n:(i + 1) * n]) - 1), 1) for i in range(10)]


def kenngroessen(c):
    fx = SL.HL.faktor(c)
    med = BK.P["dezile"][c][4] * BK.P["fortschreibung_2024_2026"][c]
    d = RB.dividenden(c, 1, 0)
    z = MR[c]["z2028"]
    return dict(dividende_zu_median_pct=round(100 * d / med, 1), boden_zu_median_pct=round(100 * RB.boden(c, 1, 0) / med, 1),
                netz_pct_bip=z["netz_pct_bip"], gesundheit_pct_bip=z["netz"]["Gesundheit"], arbeitslosigkeit_pct_bip=z["netz"]["Arbeitslosigkeit"],
                dividende_pct_bip=z["dividende_pct_bip"], preisniveau_de_100=MR[c]["preisniveau_de_100"],
                median_zu_bip_kopf=round(med / fx / MR[c]["bip_kopf_eur_2024"], 2))


def main():
    E = dict(version="v4.9", status="Prüfrechnung", staaten={})
    for c in LAENDER:
        E["staaten"][c] = dict(gini_amtlich=G.P["gini_amtlich_2025"][c], gini_2028=gini_2028(c)[0],
                               gini_weitergabe_gedeckelt_1x=mit_deckel(c, 1.0), gini_weitergabe_gedeckelt_1_5x=mit_deckel(c, 1.5),
                               gini_abbildung_familie=gini_familie(c), aenderung_je_dezil_pct=dezile(c), stufen=stufen(c),
                               kenngroessen=kenngroessen(c))
    E["hinweis"] = ("Gini 2028 mit eigenem Einkommen in D1–D2 voll (untere Schätzung der Wirkung). Deckel: Weitergabe nur bis zu den Arbeitgeberbeiträgen "
                    "beim 1- bzw. 1,5-fachen Durchschnittslohn. Familie: Abbildung über Paar + 2 Kinder statt alleinstehend.")
    (AGG / "gini_frankreich.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in E["staaten"].items():
        print(c, "amtlich", x["gini_amtlich"], "| 2028", x["gini_2028"], "| Deckel 1×", x["gini_weitergabe_gedeckelt_1x"], "1,5×", x["gini_weitergabe_gedeckelt_1_5x"],
              "| Familie", x["gini_abbildung_familie"])
        print("   Dezile %", x["aenderung_je_dezil_pct"])
        print("   ", x["kenngroessen"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
