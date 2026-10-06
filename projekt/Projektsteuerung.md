# Projektsteuerung TAX 28:28 (Stand v3.10, 6. Oktober 2026)

Maßgeblich ist das private Repository `archicrowd/2828` (main, Commit 4dd9da1). Dieser Projektraum spiegelt nur
Logbuch Band I bis III und diese Anleitung; der Abgleich geschieht von Hand.
Autor und Projektverantwortlicher des Konzepts: Arndt Hermann.

## Aufbau
- `logbuch/` Versionsgeschichte (Band I bis III), Korrekturen fortlaufend nummeriert, nächste freie Nummer 49.
- `modell/` Parameterfile, Zweitrechnung, `rahmen/` Originalskripte (unverändert), `kennzahlen.py`, Prüfskripte.
- `dokumente/` Gesamtkonzept (Stand B) und `aussagen.csv` (131 Zahlen mit Sollwert).
- `projekt/` Bausteinregister (19), Nahtstellen (11), Prüfsummen, `pruefe_projekt.py`.
- `schnittstelle/`, `beitraege/` Entwurf für Dritte (Mikrosimulation); Tarifmittelstufen offen.
- `seite/` Webseite Stand A (veraltet) und Seitenstruktur Stand B.

## Ablauf je Änderung
1. Parameter oder Skript ändern. 2. `python3 modell/alles.py` (acht Stufen). 3. Logbuch-Eintrag mit Datum,
Änderung, Quelle, bewegter Zahl. 4. Register anpassen. 5. Ein Commit, ein Tag. 6. Projektraum nachführen.
Tag-Push scheitert über den Sitzungsproxy (HTTP 403); Tags und GitHub Releases setzt der Verantwortliche.

## Offene Entscheidungen des Autors
Lizenz und Sichtbarkeit (`LIZENZ-VORSCHLAG.md`), Korrektur 49 (B1 und/oder B7), B4 (Irland BIP oder BIP*),
B6 (Ausgangslage 2024 oder 2028), mittlere Tarifstufen (9/16/21/26 gegen 9/19/24/27).
Offene Rechenpunkte: B7, B8, B9, B12, B14 (Band III, Abschnitt 7). Der Vorchat ist nur Sekundärquelle.
