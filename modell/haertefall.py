#!/usr/bin/env python3
"""Härtefall H1–H3 mit dem Boden (Kindergewicht nach regel_boden.toml) gegen das Netzbudget je Land (Logbuch v4.8). Prüfrechnung, grob.

Kosten im Erwerbsalter, 2028, Preise 2026:
  Boden   = Aufstockung aus boden_kosten (Band, EU-SILC-Dezile);
  H1      = betroffene Äquivalenzerwachsene × Anteil mit Überhang × mittlerer Überhang (Annahmen in haertefall.toml);
  H2, H3  = Annahmen in % BIP bzw. € je Einwohner.
Budget: Härtefall + Arbeitslosigkeit + Invalidität des Netzes (moeglichkeitsraum33, 2028). Ausgabe: daten/aggregate/haertefall.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "haertefall.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("bk", W / "modell" / "boden_kosten.py")
BK = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(BK)
LS = BK.LS


def h1_de(s=None):
    """v4.39 (R7): mittlerer Überhang der Wohnkosten über dem Wohnanteil des Bodens je Äquivalenzerwachsenem (€ im Monat, DE, Kaufkraft 2026)."""
    from math import log
    from scipy.stats import norm
    H = P["h1"]
    s = H["streuung_log"] if s is None else s
    gb = LS["staaten"]["DE"]["grundbedarf_jahr_eur"] / 12
    kw, ew = BK.RB.P["skala"]["kind"], BK.RB.P["skala"]["erwachsen"]
    skala = dict(allein=1.0, alleinerziehend=1 + kw * H["kinder"]["alleinerziehend"], paar_ohne=1 + ew, paar_mit=1 + ew + kw * H["kinder"]["paar_mit"])
    num = den = anteil = 0.0
    typen = {}
    for t, w in H["bg_anteile"].items():
        m = H["kdu_monat_2025"][t] * H["fortschreibung_2025_2026"]
        g = P["wohnanteil_grundbedarf"] * gb * skala[t]
        mu = log(m) - s * s / 2
        d1 = (mu + s * s - log(g)) / s
        e, p = float(m * norm.cdf(d1) - g * norm.cdf(d1 - s)), float(norm.cdf(d1 - s))
        typen[t] = dict(kdu=round(m), wohnanteil=round(g), ueberhang_mittel=round(e, 1), anteil_ueber=round(p, 3))
        num, den, anteil = num + w * e, den + w * skala[t], anteil + w * p
    return dict(je_aequivalent_monat=round(num / den, 2), anteil_bg_ueber=round(anteil, 3), typen=typen)


H1 = h1_de()


def land(c):
    gb = LS["staaten"][c]["grundbedarf_jahr_eur"] / LS["staaten"]["DE"]["grundbedarf_jahr_eur"]     # Preisniveau relativ DE (EUR)
    ew = float(LS["staaten"][c].get("einwohner_mio", 0)) or BK.MR["laender"][c]["einwohner_mio"]
    aequiv = ew * 1e6 * BK.P["anteil_erwerbsalter"] / BK.P["personen_je_aequivalent"]
    bip = BK.MR24["bip_mio_eur"][c] / 1000 * BK.P["bip_fortschreibung"]
    n = BK.MR["laender"][c]["z2028"]["netz"]
    budget = n["Härtefall"] + n["Arbeitslosigkeit"] + n["Invalidität"]
    out = dict(budget_pct_bip=round(budget, 2), band={})
    for name, eu in (("untere", BK.P["eigenanteil_unten"][1]), ("obere", BK.P["eigenanteil_unten"][0])):
        k = BK.kosten(c, eu)
        h1 = aequiv * k["anteil_mit_aufstockung"] / 100 * H1["je_aequivalent_monat"] * gb * 12 / 1e9   # v4.39: aus Mietdaten (DE), andere nach Grundbedarf
        h3 = ew * 1e6 * P["h3_eur_je_einwohner"] * gb / 1e9
        h1p, h3p = 100 * h1 / bip, 100 * h3 / bip
        summe = k["pct_bip"] + h1p + P["h2_pct_bip"] + h3p
        out["band"][name] = dict(boden=k["pct_bip"], h1=round(h1p, 2), h2=P["h2_pct_bip"], h3=round(h3p, 3), summe=round(summe, 2),
                                 reserve=round(budget - summe, 2),
                                 dividende_minus_monat=round(max(0.0, summe - budget) * LS["staaten"][c]["dividende_erw_eur"][0]
                                                             / LS["staaten"][c]["dividende_pct_bip"][0] * BK.RB.SL.HL.faktor(c), 1))
    return out


def main():
    E = dict(version=P["version"], status="Prüfrechnung, grob", kindergewicht=BK.RB.P["skala"]["kind"], regeln=P["regeln"],
             h1_mietdaten_de=dict(H1, band={str(s): h1_de(s)["je_aequivalent_monat"] for s in P["h1"]["streuung_band"]},
                                  bis_v438_je_aequivalent_monat=75.0),
             staaten={c: land(c) for c in ("DE", "FR", "IT", "ES", "PL")},
             hinweis="% BIP 2028. H1 aus den anerkannten Wohnkosten im SGB II (DE, März 2025) gegen den Wohnanteil des Bodens; andere Länder nach Grundbedarf "
                     "skaliert (Annahme, keine Mietdaten). H2 und H3 Annahmen (haertefall.toml). H1 nur für Haushalte mit Aufstockung (Näherung). "
                     "Reserve = Budget − Summe; bei negativer Reserve Kürzung der Erwachsenendividende je Monat (Landeswährung).")
    (AGG / "haertefall.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in E["staaten"].items():
        print(c, "Budget", x["budget_pct_bip"], "| untere", x["band"]["untere"], "| obere", x["band"]["obere"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
