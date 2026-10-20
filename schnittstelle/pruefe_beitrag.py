#!/usr/bin/env python3
"""Prüft die Ergebnisdatei eines Beitrags gegen schnittstelle/ergebnis-schema.csv.

Aufruf:  python3 schnittstelle/pruefe_beitrag.py beitraege/<kuerzel>-<jahr>/ergebnis.csv
Geprüft wird die Form (Spalten, Pflichtfelder, Zahlen, Preisbasis, Ländercodes), nicht der Inhalt.
Rückgabe 0 bei Erfolg.
"""
import csv
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
# v4.21: Stand C rechnet für 30 Staaten (Möglichkeitsraum: EU 27, Norwegen, Island, Schweiz; Eurostat-Codes, Griechenland = EL)
LAENDER = {"AT", "BE", "BG", "CH", "CY", "CZ", "DE", "DK", "EE", "EL", "ES", "FI", "FR", "HR", "HU", "IE", "IS", "IT", "LT", "LU", "LV", "MT",
           "NL", "NO", "PL", "PT", "RO", "SE", "SI", "SK"}
STAENDE = ("Stand A", "Stand B", "Stand C")


def main(pfad: str) -> int:
    with (WURZEL / "schnittstelle" / "ergebnis-schema.csv").open(encoding="utf-8", newline="") as f:
        schema = list(csv.DictReader(f))
    spalten = [s["spalte"] for s in schema]
    fehler = []
    with open(pfad, encoding="utf-8", newline="") as f:
        leser = csv.DictReader(f)
        if leser.fieldnames != spalten:
            fehler.append(f"Spalten stimmen nicht: erwartet {spalten}, gefunden {leser.fieldnames}")
        for i, z in enumerate(leser, start=2):
            def f_(msg):
                fehler.append(f"Zeile {i}: {msg}")
            for s in schema:
                if s["pflicht"] == "ja" and not (z.get(s["spalte"]) or "").strip():
                    f_(f"Pflichtfeld leer: {s['spalte']}")
            if z.get("land") not in LAENDER:
                f_(f"Ländercode unbekannt: {z.get('land')}")
            if z.get("preisbasis") not in ("nominal", "real"):
                f_("preisbasis muss nominal oder real sein")
            if z.get("preisbasis") == "real" and not (z.get("preisjahr") or "").strip().isdigit():
                f_("preisjahr fehlt bei preisbasis real")
            if z.get("stand") not in STAENDE:
                f_("stand muss 'Stand A', 'Stand B' oder 'Stand C' sein")
            for feld in ("jahr", "fallzahl"):
                if not (z.get(feld) or "").strip().isdigit():
                    f_(f"{feld} muss eine Ganzzahl sein")
            try:
                float(z.get("wert") or "x")
            except ValueError:
                f_(f"wert keine Zahl: {z.get('wert')}")
    for e in fehler[:30]:
        print("FEHLER:", e)
    print(f"{len(fehler)} Fehler" if fehler else "Form in Ordnung")
    return 2 if fehler else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
