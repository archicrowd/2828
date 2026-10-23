# Projektstatus (erzeugt von projekt/pruefe_projekt.py)

Modellstand v4.28 · höchste Korrekturnummer 70 · 458 Dateien im Repository

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
| B15 | Schnittstelle für Dritte | C | geprueft | schnittstelle/pruefe_beitrag.py;projekt/pruefe_projekt.py |
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
| B31 | Drittel-System: Zeitpfad, Haushalte, Webseitenentwurf | B | geprueft | modell/projektion33.py;modell/haushalte33.py |
| B32 | Länderseiten: Referenzland je Sprachversion | B | geprueft | modell/heute_laender.py (OECD-Abgleich, Selbstprüfung Raster) |

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
| N21 | B28 Sozialschutz und Übergang | B20 Gesamtrechnung | geschlossen |
| N22 | B30 Altlastenfonds | B20 Gesamtrechnung | geschlossen |
| N23 | B31 Drittel-System | B20 Gesamtrechnung | offen |
| N24 | B32 Länderseiten | B31 Drittel-System | offen |
| N25 | B31/B32 Haushaltsrechnungen | B31 Drittel-System | geschlossen |
| N26 | B32 Länderseiten | B31 Drittel-System | geschlossen |
| N27 | B32 Länderseiten | B31 Drittel-System | offen |
| N28 | B32 Länderseiten | B31 Drittel-System | offen |
| N29 | B30 Altlastenfonds | B31 Drittel-System | offen |
| N30 | B31 Drittel-System | B32 Länderseiten | offen |
| N31 | B30 Altlastenfonds | B32 Länderseiten | geschlossen |
| N32 | B32 Länderseiten | B31 Drittel-System | offen |
| N33 | B31 Drittel-System | B32 Länderseiten | offen |
| N34 | B32 Länderseiten | B31 Drittel-System | offen |
| N35 | B30 Altlastenfonds | B31 Drittel-System | geschlossen |
| N36 | B32 Länderseiten | B31 Drittel-System | offen |

## Ergebnis dieses Laufs

- keine Fehler
- Hinweis: Naht N05 offen: B08 Kern (Stand A) -> B03 Rahmenmodell (Stand B): v3.12: auf deutscher Basis 29,85 % nachgewiesen (Kern + Bausteine + Bodenwert), Lücke 0,95 Punkte zur Quote 30,8 % (v3.19: 1,05 Punkte zu 30,9 %; v3.20: 2,05 Punkte zu 31,9 %; v3.21: 1,79 Punkte; v3.22: 1,73 Punkte, Tarif 0/9/16/21/28 am Grundbedarf); Klubebene fehlt (deckung_quote.csv)
- Hinweis: Naht N07 fehlt: B03 Rahmenmodell -> B11 Seite Stand A: Seite hat Rahmenwechsel nie gesehen
- Hinweis: Naht N23 offen: B31 Drittel-System -> B20 Gesamtrechnung: v3.47: Entscheidung über Dauerhaftigkeit der Dividende (hinnehmen, Bodenwertabgabe, Bürgerfonds)
- Hinweis: Naht N24 offen: B32 Länderseiten -> B31 Drittel-System: v4.1: Entscheidung der Initiative zur französischen Variante; feinere Lohnverteilungen je Land
- Hinweis: Naht N27 offen: B32 Länderseiten -> B31 Drittel-System: v4.7: Vergleich DK/SE; Vorschlag H1–H3, K1, G1–G5 zur Entscheidung; Kosten von H1–H3 und K1 nicht gerechnet (Mietdaten nach Haushaltstyp fehlen) | v4.8: H1–H3 und G1–G5 nach Empfehlung angenommen und grob gerechnet; Kindergewicht 0,55 vorgeschlagen; Freigabe der Initiative offen; Mietdaten weiter offen
- Hinweis: Naht N28 offen: B32 Länderseiten -> B31 Drittel-System: v4.9: Gini FR steigt durch ungedeckelte Weitergabe; Deckel 1× / 1,5× Durchschnittslohn senkt FR auf 27,6 / 29,8 (Korrektur 64)
- Hinweis: Naht N29 offen: B30 Altlastenfonds -> B31 Drittel-System: v4.10: Vorschlag A (Kürzung 7,5 %), B1, T1, L1 (⅔-Kopplung); Rentenalter 65/67 vereinheitlichen; Korrektur 65 | v4.11: beschlossen und gerechnet; Fonds +0,69 % BIP (T1 +0,50); Rentenalter 67 einheitlich; offen: DRV-Rentenverteilung, Eigentumsschutz | v4.26: Regel E beschlossen und gerechnet; offen nur Rechtsprüfung (Art. 14 GG)
- Hinweis: Naht N30 offen: B31 Drittel-System -> B32 Länderseiten: v4.12: DE trägt auch ohne Weitergabe (+149…+433 €), FR/ES nicht; Durchsetzungsregel fehlt | v4.13: Gesetz zur Vertragsanpassung bis zum Stichtag beschlossen; offen Nachweis, Sanktion, neue Verträge | v4.18: Monitoring und Rückfallregel (Differenz an den Fonds, 2,4–2,8 % BIP bei 50 %); offen: neue Verträge nach dem Stichtag | v4.27: offen nur neue Verträge nach dem Stichtag (E8)
- Hinweis: Naht N32 offen: B32 Länderseiten -> B31 Drittel-System: v4.15: Pflichtquote 6,19 → 7,29 % BIP, Kasse 2,65 → 3,09 % (Annahmen), Irland 261 € je Einwohner und Monat bei BIP-Bemessung
- Hinweis: Naht N33 offen: B31 Drittel-System -> B32 Länderseiten: v4.15: nicht gerechnet | v4.16: 400 Kreise (Eurostat): Formel P90/P10 1,05, Strukturzuschlag 10 % hebt dünn besiedelte Kreise auf Index 111; heutige Gemeindeeinnahmen je Kreis fehlen (robots.txt)
- Hinweis: Naht N34 offen: B32 Länderseiten -> B31 Drittel-System: v4.16: 50 % der Verteidigung gemeinsam = 15,1 % der Mehrwertsteuer 2035; Gesamtlast unverändert
- Hinweis: Naht N36 offen: B32 Länderseiten -> B31 Drittel-System: v4.22: Vollzeit 99,3 %, Teilzeit 99,8 %, Minijob 47,6 %, Bürgergeld ohne Erwerb 14,7 %, Rentner 0 %; Validierung Lohnsumme −3,2 %, Lohnsteuer −4,8 %; Grundsicherung im Alter nicht bestanden (Rentenverteilung je Rente) | v4.23: Rentner mit Haushaltseinkommen: 5,4 % mit mehr, −145 € im Mittel; Prüfwerte bestanden; Ausgleich offen | v4.24: Vorschlag E (Boden 1.083/1.632 €, 15 % auf Zusagen über dem Grundbedarf): unteres Fünftel +21 €, oberes −477 €, gegen Beschluss −0,05 % BIP; Entscheidung offen | v4.26: E beschlossen und eingerechnet (Fonds 5,17 %, Zuschlag 15,5 %); Webseitentexte offen | v4.28: Beamte 83 % (Zulage), Selbständige 78 %
