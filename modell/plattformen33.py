#!/usr/bin/env python3
"""Plattformen am Ort der Nutzung: Gewinnweg mit Untergrenze (Logbuch v4.86). Variante, nicht in der Deckung.

Grundlage: Umsatz großer Digitalkonzerne mit Nutzern im Land, aus dem Aufkommen der Digitalsteuern in UK, FR, IT, AT zurückgerechnet (in % BIP).
Fälle vorsichtig / mittel / hoch: Grundlage = kleinster / mittlerer / größter Länderwert; Marge, Anteil unter der Untergrenze und heute schon gezahlte
Steuer nach plattformen33.toml.
  Gewinnweg     33 % × Marge × Umsatz am Nutzungsort
  Untergrenze   33 % × 10 % × Umsatz, angerechnet; greift nur bei Konzernen mit Marge unter 10 %
  Mehraufkommen (Gewinnweg + Aufstockung durch die Untergrenze) × (1 − heute schon gezahlt)
Ausgabe: daten/aggregate/plattformen33.json (in % BIP; Deutschland 2028 in Mrd. € nominal und in Euro Dividende je Erwachsenem und Monat).
"""
import json
import statistics
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "plattformen33.toml").read_text(encoding="utf-8"))
PAR = {p["name"]: p["wert"] for p in tomllib.loads((W / "modell" / "parameter.toml").read_text(encoding="utf-8"))["parameter"]}
EUR_BIP = json.loads((AGG / "ausweichen33.json").read_text(encoding="utf-8"))["eur_je_bip_punkt"]["j2028"]


def main():
    laender = []
    for b in P["basis"]:
        u = b["aufkommen_mio"] / b["satz"]
        laender.append(dict(land=b["land"], jahr=b["jahr"], umsatz_mio=round(u), umsatz_pct_bip=round(u / b["bip_mio"] * 100, 3),
                            umfang=b["umfang"], quelle=b["quelle"]))
    werte = sorted(x["umsatz_pct_bip"] for x in laender if x["land"] != "AT")   # AT nur Werbung: als Untergrenze ausgewiesen, nicht im Band
    basis = [werte[0], statistics.median(werte), werte[-1]]
    s, q, G = P["satz"], P["untergrenze_gewinnquote"], P["gewinn"]
    faelle = {}
    for i, fall in enumerate(["vorsichtig", "mittel", "hoch"]):
        u = basis[i]
        a = G["anteil_unter_untergrenze"][i]
        gewinnweg = s * (G["marge"][i] * (1 - a) + G["marge_unter_untergrenze"] * a) * u
        aufstockung = s * (q - G["marge_unter_untergrenze"]) * a * u
        mehr = (gewinnweg + aufstockung) * (1 - G["heute_schon_gezahlt"][i])
        faelle[fall] = dict(umsatz_pct_bip=round(u, 3), gewinnweg_pct_bip=round(gewinnweg, 4), untergrenze_pct_bip=round(s * q * u, 4),
                            aufstockung_untergrenze_pct_bip=round(aufstockung, 4), mehraufkommen_pct_bip=round(mehr, 4),
                            de_2028_mrd_nominal=round(mehr / 100 * PAR["de_bip_2028"], 1), dividende_eur_erw_monat=round(mehr * EUR_BIP, 1),
                            effektiv_pct_umsatz=round((gewinnweg + aufstockung) / u * 100, 2))
    E = dict(version=P["version"], status="Variante, nicht in der Deckung (Position Unternehmen und Plattformen bleibt 4,42 % BIP, Basis offen)",
             laender=laender, faelle=faelle, regel=dict(satz=s, untergrenze_gewinnquote=q, untergrenze_pct_umsatz=round(s * q * 100, 1)),
             hinweis="Grundlage aus Digitalsteuern zurückgerechnet (nur große Konzerne, Tatbestände je Land verschieden); Marge und Anteile Annahmen. "
                     "Ergänzt R6 um Umsätze, die außerhalb des Nutzerlands gebucht werden; Teil-Doppelzählung möglich.")
    (AGG / "plattformen33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for x in laender:
        print(f"{x['land']} {x['jahr']}: Umsatz {x['umsatz_pct_bip']:.2f} % BIP ({x['umfang']})")
    for f, d in faelle.items():
        print(f"{f:>10}: Umsatz {d['umsatz_pct_bip']:.2f} % BIP → Mehraufkommen {d['mehraufkommen_pct_bip']:.3f} % BIP = {d['de_2028_mrd_nominal']} Mrd. € (DE 2028), "
              f"{d['dividende_eur_erw_monat']} € je Erw.; Untergrenze stockt auf um {d['aufstockung_untergrenze_pct_bip']:.4f} % BIP; effektiv {d['effektiv_pct_umsatz']} % des Umsatzes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
