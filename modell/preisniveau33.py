#!/usr/bin/env python3
"""Einmaliger Preisniveauschub bei Einführung des Goldenen Drittels (Logbuch v4.18). Prüfrechnung, Deutschland, statisch.

  Mehrwertsteuer:  ΔP_m = α · s · ((1 + t_neu) / (1 + t_heute) − 1)       t: effektiver Satz auf die Konsumstruktur
  Arbeitskosten:   ΔP_k = −β · (1 − Weitergabe) · AG-Beiträge (% BIP)    Kostensenkung im Verhältnis zur Wertschöpfung
  Verbraucherpreise einmalig ≈ ΔP_m + ΔP_k; danach sinkt t_neu mit dem Wandel der Konsumstruktur (projektion33: label_effektiv).
Nicht enthalten: CO₂-Preispfad (eigene Größe), Zweitrundeneffekte (Löhne, Indexierung), Geldpolitik, Nachfrageverschiebung.
Die Haushaltsrechnungen (haushalte33) belasten den gesamten Konsum mit der vollen Differenz (α = 1, s = 1) und rechnen die
Kostensenkung nicht – sie liegen beim Preiseffekt auf der vorsichtigen Seite.
Ausgabe: daten/aggregate/preisniveau33.json
"""
import json
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "preisniveau33.toml").read_text(encoding="utf-8"))
PJ = {r["jahr"]: r for r in json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))["reihe"]}
WR = json.loads((AGG / "weitergabe_rueckfall.json").read_text(encoding="utf-8"))
WEITERGABE = 0.8


def main():
    t0 = P["mwst_heute_effektiv"] / 100
    s_oben = P["d211_mio"] / t0 / P["p31_s14_mio"]
    s_unten = s_oben * P["anteil_haushalte_am_aufkommen"]
    ag = WR["ag_beitraege_pct_bip"]
    reihe = []
    for j in (2028, 2035, 2045, 2060):
        t1 = PJ[j]["label_effektiv"] / 100
        mech = ((1 + t1) / (1 + t0) - 1) * 100
        reihe.append(dict(jahr=j, label_effektiv=PJ[j]["label_effektiv"], mechanisch_pct=round(mech, 2),
                          mwst_spanne_pct=[round(min(P["ueberwaelzung_mwst"]) * s_unten * mech, 2), round(max(P["ueberwaelzung_mwst"]) * s_oben * mech, 2)]))
    r28 = reihe[0]
    kosten = {str(b): [round(-b * (1 - WEITERGABE) * ag["unten"], 2), round(-b * (1 - WEITERGABE) * ag["oben"], 2)] for b in P["ueberwaelzung_kosten"]}
    netto = {str(b): [round(r28["mwst_spanne_pct"][0] + kosten[str(b)][1], 2), round(r28["mwst_spanne_pct"][1] + kosten[str(b)][0], 2)]
             for b in P["ueberwaelzung_kosten"]}
    E = dict(version=P["version"], status="Prüfrechnung, statisch", anteil_konsum_mit_mwst=[round(s_unten, 2), round(s_oben, 2)],
             ueberwaelzung_mwst=P["ueberwaelzung_mwst"], reihe=reihe, arbeitskosten_2028_pct=kosten, netto_2028_pct=netto,
             haushaltsrechnung="haushalte33: volle Differenz auf den gesamten Konsum (α = 1, s = 1, ohne Kostensenkung) – obere Grenze",
             hinweis="Einmalige Niveauverschiebung im Einführungsjahr, keine dauerhafte Inflation, solange keine Zweitrundeneffekte entstehen "
                     "(nicht modelliert). Mit sinkendem effektivem Satz (weniger schädliche Produkte) geht ein Teil bis 2060 zurück. "
                     "CO₂-Preispfad nicht enthalten.")
    (AGG / "preisniveau33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Anteil Konsum mit MwSt", E["anteil_konsum_mit_mwst"])
    for r in reihe:
        print(r)
    print("Arbeitskosten", kosten, "| netto 2028", netto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
