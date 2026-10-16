# Projektstatus (erzeugt von projekt/pruefe_projekt.py)

Modellstand v3.45 · höchste Korrekturnummer 60 · 326 Dateien im Repository

## Bausteine

| ID | Baustein | Stand | Status | Prüfung |
|---|---|---|---|---|
| B01 | Logbuch | A+B | geprueft | projekt/pruefe_projekt.py (Nummernfolge, Version) |
| B02 | Parameterfile | B | geprueft | modell/lauf.py |
| B03 | Rahmenmodell, Original | B | geprueft | modell/pruefe_konstanten.py;projekt/pruefsummen.sha256 |
| B04 | Zweitrechnung Rahmenmodell | B | geprueft | modell/vergleich_original.py |
| B05 | Kennzahlen | B | geprueft | modell/pruefe_aussagen.py |
| B06 | Aussagenregister | B | geprueft | modell/pruefe_aussagen.py |
| B07 | Gesamtkonzept | B | geprueft | modell/pruefe_konzept.py |
| B08 | Nationales Gesamtmodell (Kern) | A | ungeprueft | keine |
| B09 | Einzelrechnungen R1 bis R16 | A | ungeprueft | keine |
| B10 | Audit der Gesamtlogik | A | ungeprueft | keine |
| B11 | Webseite Stand A | A | veraltet | keine |
| B12 | Seite zum Stand B | B | geprueft | modell/pruefe_konzept.py |
| B13 | Ergebnisdateien | A+B | geprueft | modell/alles.py |
| B14 | Herkunft Drittdateien | A | ungeprueft | keine |
| B15 | Schnittstelle für Dritte | B | entwurf | schnittstelle/pruefe_beitrag.py;projekt/pruefe_projekt.py |
| B16 | Archiv eigener Dateien | A | veraltet | keine |
| B17 | Projektverwaltung | A+B | geprueft | modell/alles.py |
| B18 | Werkzeuge | B | geprueft | modell/pruefe_konzept.py |
| B19 | Hintergrunddokumente Stand A | A | veraltet | keine |
| B20 | Gesamtrechnung | B | geprueft | modell/gesamtrechnung.py (Selbstprüfung gegen final.pfad);modell/pruefe_konzept.py |
| B21 | Datenzugang für Dritte | A+B | geprueft | projekt/manifest.py;modell/eingangswerte.py |
| B22 | Länderrechnungen nach Standard | B | geprueft | modell/laender/rechne.py |
| B23 | Ländervergleich nach den Kriterien der Webseite | B | geprueft | modell/laendervergleich.py |
| B24 | Übergangsrechnung Dividende je Land | B | geprueft | modell/uebergang.py (Selbstprüfung V3a gegen Gesamtrechnung) |
| B25 | Anreizbewertung je Land (Abgabenkeil) | B | geprueft | modell/anreize.py |
| B26 | Nachfrageprüfung | B | geprueft | modell/nachfrage.py |
| B27 | Tragfähigkeitsprüfung | B | geprueft | modell/tragfaehigkeit.py |
| B28 | Sozialschutz und Übergang (Gemeinsames/Eigenes/Zugesagtes; Hütte/Route/Seil) | B | geprueft | modell/sozialschutz.py |
| B29 | Systemvarianten 25:25 und 33:33 | B | geprueft | modell/systemvarianten.py |
| B30 | Altlastenfonds | B | geprueft | modell/altlasten.py |

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
| N08 | B20 Gesamtrechnung | B12 Seite Stand B | ok |
| N09 | B07 Gesamtkonzept | B01 Logbuch | ok |
| N10 | B15 Schnittstelle | extern: Mikrosimulation | entwurf |
| N11 | B09 Einzelrechnungen | B08 Kern | ungeprueft |
| N12 | B03 Rahmenmodell | B20 Gesamtrechnung | ok |
| N13 | B20 Gesamtrechnung | B07 Gesamtkonzept | ok |
| N14 | B21 Datenzugang | extern: Dritte | ok |
| N15 | B22 Länderrechnungen | B23 Ländervergleich | ok |
| N16 | B23 Ländervergleich | B12 Seite zum Stand B | ok |
| N17 | B20 Gesamtrechnung | B24 Übergangsrechnung | ok |
| N18 | B25 Anreizbewertung | B24 Übergangsrechnung | ok |
| N19 | B26 Nachfrageprüfung | B20 Gesamtrechnung | ok |
| N20 | B20 Gesamtrechnung | B07 Gesamtkonzept | ok |
| N21 | B28 Sozialschutz und Übergang | B20 Gesamtrechnung | offen |

## Ergebnis dieses Laufs

- keine Fehler
- Hinweis: Naht N05 offen: B08 Kern (Stand A) -> B03 Rahmenmodell (Stand B): v3.12: auf deutscher Basis 29,85 % nachgewiesen (Kern + Bausteine + Bodenwert), Lücke 0,95 Punkte zur Quote 30,8 % (v3.19: 1,05 Punkte zu 30,9 %; v3.20: 2,05 Punkte zu 31,9 %; v3.21: 1,79 Punkte; v3.22: 1,73 Punkte, Tarif 0/9/16/21/28 am Grundbedarf); Klubebene fehlt (deckung_quote.csv)
- Hinweis: Naht N07 fehlt: B03 Rahmenmodell -> B11 Seite Stand A: Seite hat Rahmenwechsel nie gesehen
- Hinweis: Naht N21 offen: B28 Sozialschutz und Übergang -> B20 Gesamtrechnung: nach Entscheidung S1–S13; Korrektur 60
