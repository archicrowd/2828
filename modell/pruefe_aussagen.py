#!/usr/bin/env python3
"""Prüft die Aussagen des Gesamtkonzepts (dokumente/aussagen.csv) gegen die Kennzahlen (modell/kennzahlen.py).

Jede Zeile von aussagen.csv nennt den Sollwert aus dem Dokument, die Einheit mit Bezugsjahr und Preisbasis
und den Schlüssel der Kennzahl, aus der er sich ergeben muss. Das Skript meldet Abweichungen über der
Toleranz. Spalte 'bekannt' = ja: die Abweichung ist im Logbuch geführt und bricht den Lauf nicht. Ändert sich ein Parameter oder ein Skript, zeigt der Lauf, welche Aussagen des Dokuments
nicht mehr stimmen. Für Dritte: neue Aussagen werden als Zeile ergänzt, ohne Code.

Ergebnis: daten/aggregate/aussagen_pruefung.csv. Rückgabe 0, wenn alle Aussagen innerhalb der Toleranz liegen.
"""
import csv
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WURZEL / "modell"))
from kennzahlen import kennzahlen  # noqa: E402


def main() -> int:
    W = kennzahlen()
    with (WURZEL / "dokumente" / "aussagen.csv").open(encoding="utf-8", newline="") as f:
        zeilen = list(csv.DictReader(f))
    ausgabe, nein, fehlt, ids, offen_bekannt = [], [], [], set(), []
    for z in zeilen:
        if z["id"] in ids:
            sys.exit(f"FEHLER: doppelte Aussagen-ID {z['id']}")
        ids.add(z["id"])
        k = z["schluessel"]
        if k not in W:
            fehlt.append(z["id"])
            ausgabe.append([z["id"], z["soll"], "", "", z["toleranz"], "FEHLT"])
            continue
        soll, tol, ist = float(z["soll"]), float(z["toleranz"]), W[k]
        ok = abs(ist - soll) <= tol + 1e-9
        bekannt = (z.get("bekannt") or "").strip() == "ja"
        if not ok and not bekannt:
            nein.append((z["id"], z["aussage"], soll, round(ist, 4)))
        if not ok and bekannt:
            offen_bekannt.append(z["id"])
        ausgabe.append([z["id"], f"{soll}", f"{ist:.4f}", f"{ist - soll:+.4f}", z["toleranz"],
                        "ja" if ok else ("bekannt abweichend" if bekannt else "NEIN")])
    ziel = WURZEL / "daten" / "aggregate" / "aussagen_pruefung.csv"
    with ziel.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "soll", "ist", "differenz", "toleranz", "innerhalb"])
        w.writerows(ausgabe)
    print(f"{len(zeilen)} Aussagen geprüft, {len(nein)} außerhalb der Toleranz, {len(fehlt)} ohne Kennzahl, "
          f"{len(offen_bekannt)} bekannt abweichend ({', '.join(offen_bekannt) or '-'}).")
    for n in nein:
        print("  ABWEICHUNG:", n)
    for i in fehlt:
        print("  FEHLT:", i)
    return 2 if (nein or fehlt) else 0


if __name__ == "__main__":
    sys.exit(main())
