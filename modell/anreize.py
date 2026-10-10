#!/usr/bin/env python3
"""Anreizbewertung je Land: Abgabenkeil heute gegen 28:28 und daraus abgeleitete Wachstumszuschläge (Logbuch v3.30).

Je Land, Alleinstehende beim Durchschnittslohn:
  heute: Abgabenkeil laut OECD Taxing Wages 2025 (Daten 2024), % der Arbeitskosten (daten/aggregate/abgabenkeil_2024.csv)
  28:28: Arbeitskosten bleiben gleich, die Arbeitgeberbeiträge gehen in den Bruttolohn über (Inzidenz voll, Annahme);
         Einkommensteuer nach den Stufen am Grundbedarf des Landes (Euro 2028), Sozialabgaben 0. Die Dividende ist eine
         Pauschale und gehört nicht zum Abgabenkeil (wie bei der OECD für Alleinstehende).
  Arbeitskosten 2028 = Durchschnittslohn 2024 / (1 − Arbeitgeberanteil) x (1 + nominales Wachstum)^4 (Annahme 3,0 % wie Gesamtrechnung).
Wirkung: Niveaueffekt auf das BIP = kappa x Abbau des Keils (Punkte). Eingerechnet wird nur der Unterschied zum Klubschnitt
(BIP-gewichtet), verteilt über aufbau_jahre; der klubweite Effekt wird nur ausgewiesen.
Ausgabe: daten/aggregate/anreize.json
"""
import csv, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell/anreize.toml").read_text(encoding="utf-8"))
TG = json.loads((AGG / "tarif_grundbedarf.json").read_text(encoding="utf-8"))
G28, SAETZE = float(TG["grundbedarf_2028"]), [float(s) for s in TG["saetze"]]
G_NOM = float({p["name"]: p["wert"] for p in tomllib.loads((W / "modell/gesamtrechnung.toml").read_text(encoding="utf-8"))["parameter"]}["wachstum_nominal"])
with open(AGG / "preisniveau_2024.csv", encoding="utf-8") as f:
    PLI = {r["land"]: float(r["preisniveau_eu27_100"]) for r in csv.DictReader(f)}
for c in ("pl",):                                           # Länder außerhalb der Klubtabelle: Preisniveau aus der Länderrechnung
    p = AGG / "laender" / f"{c}.json"
    if p.exists():
        PLI[c.upper()] = json.loads(p.read_text(encoding="utf-8"))["wohnort"]["preisniveau_2024"]
with open(AGG / "abgabenkeil_2024.csv", encoding="utf-8") as f:
    TW = {r["land"]: r for r in csv.DictReader(f)}
with open(AGG / "laender_2024.csv", encoding="utf-8") as f:
    BIP = {r["land"]: float(r["bip_mio_eur_2024_nominal"]) for r in csv.DictReader(f)}


def steuer(x, stufen):
    s, u = 0.0, 0.0
    for g, p in zip(list(stufen) + [float("inf")], SAETZE):
        if x > u:
            s += (min(x, g) - u) * p / 100
        u = g
    return s


def main():
    erg = {}
    for c, r in TW.items():
        if c == "OECD" or c not in PLI:
            continue
        f = PLI[c] / PLI["DE"]
        stufen = [round(G28 * f * k) for k in (1, 2, 3, 4)]
        if c in TG["stufen_laender_2028"] and TG["stufen_laender_2028"][c] != stufen:
            sys.exit(f"{c}: Tarifstufen weichen ab")
        er = float(r["sv_arbeitgeber_pct"])
        aw28 = float(r["durchschnittslohn_eur"]) * (1 + G_NOM / 100) ** 4
        lc28 = aw28 / (1 - er / 100)
        keil_neu = steuer(lc28, stufen) / lc28 * 100
        heute = float(r["abgabenkeil_pct"])
        erg[c] = dict(keil_heute_pct=heute, keil_2828_pct=round(keil_neu, 2), abbau_punkte=round(heute - keil_neu, 2),
                      arbeitskosten_2028_eur=round(lc28), durchschnittslohn_2024_eur=float(r["durchschnittslohn_eur"]))
    klub = [c for c in erg if c in BIP]
    abbau_klub = sum(erg[c]["abbau_punkte"] * BIP[c] for c in klub) / sum(BIP[c] for c in klub)
    T = P["aufbau_jahre"]
    for c, e in erg.items():
        rel = e["abbau_punkte"] - abbau_klub
        e["abbau_gegen_klub_punkte"] = round(rel, 2)
        e["niveau_relativ_zentral_pct"] = round(P["kappa_zentral"] * rel, 2)
        e["niveau_relativ_niedrig_pct"] = round(P["kappa_niedrig"] * rel, 2)
        e["delta_zentral_pp_je_jahr"] = round(P["kappa_zentral"] * rel / T, 4)
        e["delta_niedrig_pp_je_jahr"] = round(P["kappa_niedrig"] * rel / T, 4)
    E = dict(version=P["version"], kappa_zentral=P["kappa_zentral"], kappa_niedrig=P["kappa_niedrig"], aufbau_jahre=T,
             abbau_klub_bip_gewichtet_punkte=round(abbau_klub, 2),
             niveaueffekt_klub_nicht_eingerechnet_pct=dict(zentral=round(P["kappa_zentral"] * abbau_klub, 1),
                                                           niedrig=round(P["kappa_niedrig"] * abbau_klub, 1)),
             hinweis="Klubweiter Effekt nur ausgewiesen: lineare Übertragung der Literaturwerte (Änderungen um wenige Punkte) auf einen "
                     "Abbau um 20 bis 35 Punkte ist nicht gedeckt. Eingerechnet wird nur der Unterschied zwischen den Ländern.",
             laender=erg)
    (AGG / "anreize.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Abbau Klubschnitt {abbau_klub:.1f} Punkte; Niveaueffekt Klub (nicht eingerechnet) zentral {P['kappa_zentral']*abbau_klub:.1f} %")
    for c, e in sorted(erg.items(), key=lambda x: -x[1]["abbau_punkte"]):
        print(f"{c}: heute {e['keil_heute_pct']:.1f} -> 28:28 {e['keil_2828_pct']:.1f} (Abbau {e['abbau_punkte']:.1f}, gegen Klub "
              f"{e['abbau_gegen_klub_punkte']:+.1f}) | Niveau relativ {e['niveau_relativ_zentral_pct']:+.2f} % | delta {e['delta_zentral_pp_je_jahr']:+.3f} pp/Jahr")
    return 0


if __name__ == "__main__":
    sys.exit(main())
