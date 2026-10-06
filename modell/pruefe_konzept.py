#!/usr/bin/env python3
"""Prüft das Gesamtkonzept (Fassung ab v3.12) gegen die Gesamtrechnung.

Seit v3.12 entstehen die Zahlen des Gesamtkonzepts im Bauskript aus daten/aggregate/gesamtrechnung.json.
Diese Prüfung liest den Text der fertigen PDF (pdftotext) und sucht jede Kernzahl in der Schreibweise
des Dokuments. Sie fängt drei Fehler: eine veraltete PDF (Rechnung geändert, Dokument nicht neu gebaut),
einen Fehler im Bauskript (falscher Schlüssel, falsche Rundung) und eine von Hand nachträglich geänderte
Datei. Sie prüft nicht, ob die Rechnung selbst stimmt; das tun gesamtrechnung.py (Selbstprüfung gegen
die Originale) und das Logbuch.

Außerdem: Die PDF darf keine Zahlen der alten Tabellen mehr enthalten (Quote „30,60", Klubdividende
2028 „506", Formel „3.602"), außer im Abschnitt „Gegenüber der Fassung vom 4. Oktober 2026 geändert".

Aufruf:  python3 modell/pruefe_konzept.py
Ausgabe: daten/aggregate/konzept_pruefung.csv; Rückgabe 0 oder 2.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
PDF = WURZEL / "dokumente" / "TAX-2828-Gesamtkonzept.pdf"
J = json.loads((WURZEL / "daten" / "aggregate" / "gesamtrechnung.json").read_text(encoding="utf-8"))


def de(x, nk=0):
    s = f"{x:,.{nk}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> int:
    if not PDF.exists():
        print("FEHLER: PDF fehlt")
        return 2
    text = subprocess.run(["pdftotext", str(PDF), "-"], capture_output=True, text=True).stdout
    flach = " ".join(text.split())
    tp = {r["jahr"]: r for r in J["tabelle_pfad"]}
    soll = [
        ("Quote", f"Steuerquote {de(J['quote'], 1)} %"),
        ("Obergrenze", f"{de(J['obergrenze'])} % dessen, was A einzieht"),
        ("Klubdividende 2028", f"bei {de(J['klub_2028'])} €"),
        ("Klubdividende Tiefpunkt", f"auf {de(J['kl_tief'])} €"),
        ("Formel je Einwohner", f"{de(J['formel_einw'])} € je Einwohner"),
        ("Formel je Kind", f"{de(J['formel_kind'])} € je Kind"),
        ("Einwohner", f"{de(J['pop_klub_mio'], 1)} Mio Menschen"),
        ("Klub-BIP 2028", f"{de(J['bip28_klub_mrd'])} Mrd €"),
        ("A 2028", f"{de(J['a_2028'], 2)} % des BIP im Startjahr"),
        ("Höchstbedarf", f"Höchststand {de(J['a_hoechst'], 2)} %"),
        ("Zins 2024", f"effektiver Satz von {de(J['zins_eff_2024'], 2)} %"),
        ("Zinsdienst 2028 Mrd", f"{de(J['zd_2028_mrd'])} Mrd €"),
        ("DE 2028", f"{de(J['de_2028'])} € im Startjahr"),
        ("DE 2060", f"{de(J['de_2060'])} € im Jahr 2060"),
        ("Strenge Mindestquote", f"genügen {de(J['mindestquote_streng'], 2)} %"),
        ("Anteilsverlust", f"vermindert um {de(-J['div_aenderung_pct'], 1)} %"),
        ("Entlastung", f"Entlastung von {de(J['entlastung'], 2)} Punkten"),
        ("Gesamtlast Entwurf", de(J["last_entwurf"], 2)),
        ("Deckung nachgewiesen", de(J["deckung_gesamt"], 2)),
        ("Deckungslücke", f"{de(J['deckung_luecke'], 2)} Punkte des BIP"),
        ("Aufschlag größter Anteil", f"{de(J['aufschlag_max_pos_anteil_a'], 1)} % dessen"),
        ("Entlastung Irland", f"(Irland) {de(J['aufschlag_max_anteil_a'], 1)} %"),
        ("Verwaltung", f"bis zu {de(J['verw_ersparnis_eur'])} € im Monat"),
        ("Tilgungsverzicht", f"im Startjahr {de(J['tilg_verzicht'])} € Dividende"),
        ("Dividende Tabelle 2035", de(tp[2035]["klub"])),
        ("Dividende Tabelle 2060", de(tp[2060]["klub"])),
        ("Autor", "Arndt Hermann"),
        ("Lizenz", "CC BY 4.0"),
    ]
    zeilen, fehler = [], 0
    for name, muster in soll:
        ok = muster in flach
        fehler += not ok
        zeilen.append([name, muster, "ja" if ok else "NEIN"])
    # veraltete Werte außerhalb des Änderungsabsatzes
    teil = flach.split("Gegenüber der Fassung vom 4. Oktober 2026 geändert")[0]
    for alt in ("30,60", "Steuerquote 30,6 %", "bei 506 €", "3.602 €", "254,8 Mio"):
        ok = alt not in teil
        fehler += not ok
        zeilen.append([f"veraltet: {alt}", alt, "ja (fehlt)" if ok else "NEIN (noch im Text)"])
    with open(WURZEL / "daten" / "aggregate" / "konzept_pruefung.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pruefung", "muster", "ergebnis"])
        w.writerows(zeilen)
    for z in zeilen:
        if z[2].startswith("NEIN"):
            print("  ", z)
    print(f"{len(zeilen)} Prüfungen am Gesamtkonzept ({J['fassung']}), davon fehlgeschlagen: {fehler}")
    return 2 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
