#!/usr/bin/env python3
"""Führt alle Prüfungen in fester Reihenfolge aus und fasst das Ergebnis zusammen.

Aufruf:  python3 modell/alles.py
Rückgabe: 0, wenn jede Stufe 0 liefert.

Reihenfolge: siehe Liste STUFEN unten (Parameter, Zweitrechnung und Vergleich mit den Originalen, Konstanten,
Kennzahlen, Aussagen der Fassung 4. Oktober, Gesamtrechnung, Dokumente gegen Rechnung, Datenzugang, Projektprüfung).
Der Lauf schreibt Ergebnisdateien nach daten/aggregate/ und projekt/manifest.json; er ist wiederholbar
(gleicher Stand ergibt gleiche Dateien). Wer nichts verändern will, arbeitet in einer Kopie. Jede Stufe schreibt ihre Ergebnisdatei nach daten/aggregate/.
Ändert sich ein Parameter, ein Skript oder ein Dokument, zeigt dieser Lauf, welcher Baustein betroffen ist.
"""
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
STUFEN = [
    ("Parameterfile prüfen", ["modell/lauf.py"]),
    ("Zeitpfad (Zweitrechnung)", ["modell/pfad.py"]),
    ("Aufschlag (Zweitrechnung)", ["modell/aufschlag.py"]),
    ("Zweitrechnung gegen Originale", ["modell/vergleich_original.py"]),
    ("Konstanten der Originalskripte", ["modell/pruefe_konstanten.py"]),
    ("Kennzahlen", ["modell/kennzahlen.py"]),
    ("Aussagen (Fassung 4.10.)", ["modell/pruefe_aussagen.py"]),
    ("Schuldenpfad bis 2028", ["modell/schuldenpfad.py"]),
    ("Tarif nach Grundbedarf", ["modell/tarif_grundbedarf.py"]),
    ("Gesamtrechnung (Fassung 6.10.)", ["modell/gesamtrechnung.py"]),
    ("Ländervarianten (B17)", ["modell/laendervarianten.py"]),
    ("Länderpfade nach Standard", ["modell/laender/rechne.py"]),
    ("Anreize je Land (Abgabenkeil)", ["modell/anreize.py"]),
    ("Ländervergleich (Webseite)", ["modell/laendervergleich.py"]),
    ("Übergangsrechnung 2028–2060", ["modell/uebergang.py"]),
    ("Nachfrageprüfung", ["modell/nachfrage.py"]),
    ("Tragfähigkeit (Entscheidungen)", ["modell/tragfaehigkeit.py"]),
    ("Justierung und Stabilität", ["modell/justierung.py"]),
    ("Sozialschutz und Übergang (Vorbereitung)", ["modell/sozialschutz.py"]),
    ("Systemvarianten 25:25 und 33:33", ["modell/systemvarianten.py"]),
    ("Altlastenfonds (Streckung)", ["modell/altlasten.py"]),
    ("Drittel-System: Zeitpfad mit Trends", ["modell/projektion33.py"]),
    ("Drittel-System: Starkes Netz (Grundversorgung)", ["modell/netz33.py"]),
    ("Drittel-System: Haushalte gegen heute", ["modell/haushalte33.py"]),
    ("Drittel-System: Einwanderung", ["modell/einwanderung33.py"]),
    ("Drittel-System: Beschäftigung und Automatisierung", ["modell/dynamik33.py"]),
    ("Drittel-System: Möglichkeitsraum", ["modell/moeglichkeitsraum33.py"]),
    ("Drittel-System: Neustartverfahren", ["modell/neustart33.py"]),
    ("Drittel-System: Webseitenentwurf (alt, eigene Gliederung)", ["seite/werkzeuge/entwurf33_bau.py"]),
    ("Länderseiten: Pfade, Fluss, Gemeinde, Fonds je Staat", ["modell/laenderseiten.py"]),
    ("Länderseiten: Haushalte heute gegen neu (FR, IT, ES, PL)", ["modell/heute_laender.py"]),
    ("Länderseiten: Zerlegung neu gegen heute (FR, IT)", ["modell/zerlegung_laender.py"]),
    ("Länderseiten: Bedarfsleistungen, Kinderanteil, Mindestlohn", ["modell/sozial_laender.py"]),
    ("Regeln R1–R4 in der Modellrechnung", ["modell/regeln_r1_r4.py"]),
    ("Regel Boden: Grundbedarf, Halbanrechnung, Vorsorge ab dem ersten Euro", ["modell/regel_boden.py"]),
    ("Regel Boden: Kosten aus der Dezilverteilung (EU-SILC)", ["modell/boden_kosten.py"]),
    ("Vergleich Dänemark/Schweden, Härtefall", ["modell/vergleich_dk_se.py"]),
    ("Webseite Fassung 4.x (sechs Sprachen, Länderbezug)", ["seite/werkzeuge/drittel_bau.py"]),
    ("Gesamtkonzept gegen Rechnung", ["modell/pruefe_konzept.py"]),
    ("Textentwurf gegen Rechnung", ["modell/pruefe_konzept.py", "--entwurf"]),
    ("Eingangswerte (Datenzugang)", ["modell/eingangswerte.py"]),
    ("Projektkarte (Datenzugang)", ["projekt/manifest.py"]),
    ("Projektprüfung", ["projekt/pruefe_projekt.py"]),
]


def main() -> int:
    ergebnis = []
    for name, cmd in STUFEN:
        p = subprocess.run([sys.executable, *cmd], cwd=WURZEL, capture_output=True, text=True)
        letzte = (p.stdout.strip().splitlines() or [""])[-1] if p.returncode == 0 else \
            " | ".join((p.stdout + p.stderr).strip().splitlines()[:3])
        ergebnis.append((name, p.returncode, letzte[:110]))
    breite = max(len(n) for n, _, _ in ergebnis)
    for name, rc, text in ergebnis:
        print(f"{'OK  ' if rc == 0 else 'FEHL'} {name:<{breite}}  {text}")
    schlecht = [n for n, rc, _ in ergebnis if rc != 0]
    print(f"\n{len(ergebnis) - len(schlecht)} von {len(ergebnis)} Stufen ohne Fehler.")
    return 1 if schlecht else 0


if __name__ == "__main__":
    sys.exit(main())
