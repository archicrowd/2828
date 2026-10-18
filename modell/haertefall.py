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
        h1 = aequiv * k["anteil_mit_aufstockung"] / 100 * P["h1_anteil_mit_ueberhang"] * P["h1_ueberhang_monat_de"] * gb * 12 / 1e9
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
             staaten={c: land(c) for c in ("DE", "FR", "IT", "ES", "PL")},
             hinweis="% BIP 2028. H1 und H3 aus Annahmen (haertefall.toml), ohne Mietdaten nach Haushaltstyp; Reserve = Budget − Summe; bei negativer Reserve Kürzung der Erwachsenendividende je Monat (Landeswährung).")
    (AGG / "haertefall.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in E["staaten"].items():
        print(c, "Budget", x["budget_pct_bip"], "| untere", x["band"]["untere"], "| obere", x["band"]["obere"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
