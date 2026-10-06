# Projektstatus (erzeugt von projekt/pruefe_projekt.py)

Modellstand v3.10 · höchste Korrekturnummer 48 · 210 Dateien im Repository

## Bausteine

| ID | Baustein | Stand | Status | Prüfung |
|---|---|---|---|---|
| B01 | Logbuch | A+B | geprueft | projekt/pruefe_projekt.py (Nummernfolge, Version) |
| B02 | Parameterfile | B | geprueft | modell/lauf.py |
| B03 | Rahmenmodell, Original | B | geprueft | modell/pruefe_konstanten.py;projekt/pruefsummen.sha256 |
| B04 | Zweitrechnung Rahmenmodell | B | geprueft | modell/vergleich_original.py |
| B05 | Kennzahlen | B | geprueft | modell/pruefe_aussagen.py |
| B06 | Aussagenregister | B | geprueft | modell/pruefe_aussagen.py |
| B07 | Gesamtkonzept | B | geprueft | modell/pruefe_aussagen.py;projekt/pruefsummen.sha256 |
| B08 | Nationales Gesamtmodell (Kern) | A | ungeprueft | keine |
| B09 | Einzelrechnungen R1 bis R16 | A | ungeprueft | keine |
| B10 | Audit der Gesamtlogik | A | ungeprueft | keine |
| B11 | Webseite Stand A | A | veraltet | keine |
| B12 | Seite zum Stand B | B | geprueft | modell/pruefe_aussagen.py (A130 bis A132) |
| B13 | Ergebnisdateien | A+B | geprueft | modell/alles.py |
| B14 | Herkunft Drittdateien | A | ungeprueft | keine |
| B15 | Schnittstelle für Dritte | B | entwurf | schnittstelle/pruefe_beitrag.py;projekt/pruefe_projekt.py |
| B16 | Archiv eigener Dateien | A | veraltet | keine |
| B17 | Projektverwaltung | A+B | geprueft | modell/alles.py |
| B18 | Werkzeuge | B | ungeprueft | keine |
| B19 | Hintergrunddokumente Stand A | A | veraltet | keine |

## Nahtstellen

| ID | von | nach | Status |
|---|---|---|---|
| N01 | B02 Parameterfile | B04 Zweitrechnung | ok |
| N02 | B03 Rahmenmodell | B05 Kennzahlen | ok |
| N03 | B05 Kennzahlen | B06 Aussagen | ok |
| N04 | B03 Rahmenmodell | B02 Parameterfile | ok |
| N05 | B08 Kern (Stand A) | B03 Rahmenmodell (Stand B) | offen |
| N06 | B08 Kern | B11 Seite Stand A | ungeprueft |
| N07 | B03 Rahmenmodell | B11 Seite Stand A | fehlt |
| N08 | B05 Kennzahlen | B12 Seite Stand B | ok |
| N09 | B07 Gesamtkonzept | B01 Logbuch | ok |
| N10 | B15 Schnittstelle | extern: Mikrosimulation | entwurf |
| N11 | B09 Einzelrechnungen | B08 Kern | ungeprueft |

## Ergebnis dieses Laufs

- keine Fehler
- Hinweis: Naht N05 offen: B08 Kern (Stand A) -> B03 Rahmenmodell (Stand B): B12 im Logbuch: nicht gerechnet; Kern lieferte 27,91 %
- Hinweis: Naht N07 fehlt: B03 Rahmenmodell -> B11 Seite Stand A: Seite hat Rahmenwechsel nie gesehen
