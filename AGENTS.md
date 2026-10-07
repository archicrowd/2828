# AGENTS.md: Anleitung für KI-Agenten

Kurzfassung für Agenten, die dieses Repository prüfen oder weiterbearbeiten. Ausführlich für Menschen: `DATENZUGANG.md`.
Verbindliche Arbeitsregeln: `CLAUDE.md` (gelten für jeden Agenten, nicht nur für Claude). Maschinenlesbare
Projektkarte: `projekt/manifest.json`.

## Zuerst lesen (in dieser Reihenfolge)
1. `projekt/manifest.json`: Modellstand, Befehle, Bausteine, Quellen, Invarianten.
2. `CLAUDE.md`: Regeln zu Logbuch, Daten, Rechnung, Commits.
3. `logbuch/Versionsgeschichte-TAX-2828-BandIII.md`: letzte Versionen und Abschnitt 7 (offene Punkte).
4. `modell/gesamtrechnung.toml` und `modell/gesamtrechnung.py`: die geltende Rechnung.

## Befehle
| Zweck | Befehl | Erwartung |
|---|---|---|
| alles prüfen | `python3 modell/alles.py` | jede Stufe ohne Fehler, Rückgabe 0 |
| Rechnung | `python3 modell/gesamtrechnung.py` | „Selbstprüfung … 33 Jahre exakt" |
| Eingangswerte | `python3 modell/eingangswerte.py [--abrufen]` | `daten/aggregate/eingangswerte.csv` |
| Projektkarte | `python3 projekt/manifest.py` | `projekt/manifest.json`, Fehler: 0 |
| Dokumente bauen | `cd dokumente/werkzeuge && npm install && cd ../.. && node dokumente/werkzeuge/gesamtkonzept-bau.js` | docx; danach PDF mit `soffice --headless --convert-to pdf` |

`modell/alles.py` **schreibt** Ergebnisdateien (`daten/aggregate/`, `projekt/manifest.json`); der Lauf ist wiederholbar.
Wer nur prüfen soll, arbeitet in einer Kopie. Stufen, die mit „bekannt" oder „VERALTET" enden, zählen als bestanden;
die Gründe stehen im Logbuch.

## Invarianten (nicht verletzen)
- `modell/rahmen/*.py` und die archivierten Dokumente nicht ändern; `projekt/pruefsummen.sha256` wacht darüber.
- Dokumente (`dokumente/*.docx`, `*.pdf`) nur über `dokumente/werkzeuge/*-bau.js` erzeugen, keine Zahl von Hand.
- Jede Änderung an Rechnung oder Daten: neue Version im Logbuch (Datum, Änderung, Datenquelle, bewegte Zahl, wodurch
  aufgefallen), Register `projekt/bausteine.csv` und `projekt/nahtstellen.csv` anpassen, `modell/alles.py` ausführen.
- Fehler als Korrektur mit der nächsten freien Nummer aus `CLAUDE.md`; Nummern nie neu vergeben.
- Keine Rohdaten, keine Mikrodaten, keine Taxplorer-Rohdaten, keine fremden E-Mail-Adressen oder Personennamen einchecken.
- Euro-Beträge immer mit Bezugsjahr und Preisbasis. OECD-Aufkommen nur Panel `_T`, nie `PANELAI`.

## Daten abrufen
- Eurostat-API: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<datensatz>?format=JSON&lang=EN&geo=<LAND>&time=<JAHR>&<dimension>=<wert>`.
  **Ein Land, eine Größe, alle Dimensionen festgelegt.** Sammelabrufe liefern unvollständige oder falsch zugeordnete
  Werte. Antwort: JSON-stat, Wert in `value`. Ratenbegrenzung beachten (Pausen von mindestens 2 s; bei HTTP 429 abbrechen).
- Fertige URLs je Wert: `daten/aggregate/eingangswerte.csv` (Spalte `getestet` beachten).
- Was ein Agent aus einer Webseite oder einer Zusammenfassung abliest, als „maschinell gelesen, an der Quelle zu prüfen"
  kennzeichnen.

## Kennzeichnung von Aussagen
Belegt (amtliche Quelle, geprüft) · abgerufen (Datum) · übernommen (nicht neu geprüft) · Annahme · Setzung ·
Schätzung · Sekundärquelle. Eine prüfbare Behauptung wird geprüft, bevor sie stehen bleibt. Angaben aus dem Vorchat
sind Sekundärquelle, bis eine Datei sie belegt.

## Ergebnisse zurückgeben
- Als maschinenlesbare Datei in `daten/aggregate/` mit Quelle je Zeile, oder für Mikrosimulationen im Format
  `schnittstelle/ergebnis-schema.csv` (Formprüfung `schnittstelle/pruefe_beitrag.py`).
- Befund mit Fundstelle (Datei, Zeile oder Abschnitt), Soll und Ist, Schweregrad (Fehler / Unschärfe / Hinweis).
- Kontakt des Verantwortlichen: 2828@archicrowd.de.
