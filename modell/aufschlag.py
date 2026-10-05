#!/usr/bin/env python3
"""Territorialer Aufschlag auf den Klubanteil (Rekonstruktion, Logbuch Band III v3.7).

ACHTUNG: Rekonstruktion, nicht das Original (aufschlag.py / altschuld.py liegen
nicht vor). Aufbau nach Korrektur 44 in Band II und dem Chat-Fragment altschuld.py:
  A übernimmt den Zinsdienst des Altbestands zum Satz 'zins_effektiv_altbestand'.
  Die Beitragsseite folgt dem BIP (A finanziert mit einheitlichem Satz auf das BIP),
  die Auszahlungsseite der Schuld. Der Aufschlag je Gebiet ist
      (Zinsdienst_i - Zinsdienst_Klub * BIP_i / BIP_Klub) / Einwohner_i
  und summiert sich klubweit auf null.
Alle Länder werden mit demselben Fortschreibungsfaktor 2024 -> 2028 auf nominale
Werte 2028 gebracht (Annahme der Rekonstruktion). Schuldenquoten gelten für 2024 und
werden wie im Zeitpfad als Werte 2028 geführt (Logbuch Band III, B6).

Aufruf:  python3 modell/aufschlag.py
Ausgabe: daten/aggregate/aufschlag.csv
Rückgabe: 0 bei Übereinstimmung mit der Referenz (+254 FR, -728 IE), 2 sonst.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pfad  # noqa: E402

AGG = pfad.AGG
TOL_EURO = 3.0  # Referenz auf ganze Euro gerundet; Schuldenquote 78,4 gegen 78,45


def main() -> int:
    P = pfad.lade()
    f = pfad.wert(P, "fortschreibung_bip_2024_2028")
    satz = pfad.wert(P, "zins_effektiv_altbestand") / 100

    with (AGG / "laender_2024.csv").open(encoding="utf-8", newline="") as fh:
        zeilen = list(csv.DictReader(fh))

    land = {}
    for z in zeilen:
        bip = float(z["bip_mio_eur_2024_nominal"]) / 1000 * f      # Mrd EUR, nominal 2028
        schuld = float(z["schuld_pct_bip_2024"]) / 100 * bip       # Mrd EUR
        land[z["land"]] = {"bip": bip, "zins": schuld * satz,
                           "pop": float(z["einwohner_mio_2024"]) * 1e6}
    bip_klub = sum(v["bip"] for v in land.values())
    zins_klub = sum(v["zins"] for v in land.values())

    aus = []
    for k, v in land.items():
        beitrag = zins_klub * v["bip"] / bip_klub
        v["aufschlag_je_kopf"] = (v["zins"] - beitrag) * 1e9 / v["pop"]
        aus.append([k, round(v["bip"], 1), round(v["zins"], 2), round(beitrag, 2),
                    round(v["aufschlag_je_kopf"], 1)])
    aus.sort(key=lambda r: -r[4])
    pfad.schreibe(AGG / "aufschlag.csv",
                  ["land", "bip_2028_mrd_eur_nominal", "zinsdienst_mrd_eur",
                   "beitrag_nach_bip_mrd_eur", "aufschlag_eur_je_kopf_und_jahr"], aus)

    summe = sum((v["zins"] - zins_klub * v["bip"] / bip_klub) for v in land.values())
    max_k, min_k = aus[0], aus[-1]
    print(f"Klub: BIP 2028 {bip_klub:,.1f} Mrd, Zinsdienst {zins_klub:,.1f} Mrd "
          f"= {zins_klub / bip_klub * 100:.3f} % des BIP")
    print(f"Summe der Aufschläge: {summe:.6f} Mrd EUR (muss null sein)")
    print(f"Spanne: {max_k[0]} {max_k[4]:+.0f} bis {min_k[0]} {min_k[4]:+.0f} EUR je Kopf und Jahr")
    ok = (max_k[0] == "FR" and min_k[0] == "IE"
          and abs(max_k[4] - 254) <= TOL_EURO and abs(min_k[4] + 728) <= TOL_EURO
          and abs(summe) < 1e-9)
    print("Referenz (Band II, Korrektur 44: +254 FR, -728 IE):", "erreicht" if ok else "NICHT erreicht")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
