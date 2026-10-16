# Projektsteuerung TAX 28:28 (Stand v3.42, 16. Oktober 2026)

Maßgeblich ist das private Repository `archicrowd/2828` (main). Der Projektraum „2525" spiegelt Logbuch
Band I bis III und diese Anleitung; der Abgleich geschieht von Hand.
Autorin des Konzepts: Initiative 28:28 (Name nur im Impressum der Webseite). Lizenz: Skripte MIT, Texte und Ergebnisse CC BY 4.0.

## Geltende Fassung
Gesamtkonzept vom 12. Oktober 2026 (Einführung als RTF, dazu Kurzfassung und PDF-Fassung): Quote 30,2 %, Obergrenze des Daches 32 % des Einzugs, Dividende als gleicher Anteil am eigenen BIP je Kopf (Entscheidung E2), Mindestniveau halbes Existenzminimum als Kriterium im Durchschnitt der Staaten; Deutschland 634 € je Erwachsenem und Monat 2028, 860 € 2060; Durchschnitt 535 € je Einwohner 2028, Tiefpunkt 526 € 2032 (Preise 2028); Tarif 0/9/16/21/28 % mit Stufen beim 1-, 1,5-, 2- und 3-fachen Grundbedarf (DE 2028: 12.847 / 19.270 / 25.694 / 38.541 €); Erbschaftsfreibetrag 100.000 €, Vermögensteuer 1,5 %; Mehrwertsteuer-Label effektiv 16,9 %; Schuldenquote 2028 81,3 %. (Bis v3.40 stand hier noch die Fassung vom 7. Oktober; nachgeführt in v3.42.) Rechnung `modell/gesamtrechnung.py`.

## Einstieg für Dritte
`DATENZUGANG.md` (Menschen), `AGENTS.md` (KI-Agenten), `projekt/manifest.json` (maschinenlesbar),
`daten/quellen.csv` (21 Quellen), `daten/aggregate/eingangswerte.csv` (125 Werte mit Abrufadresse).

## Aufbau
- `logbuch/` Versionsgeschichte (Band I bis III); Korrekturen fortlaufend, nächste freie Nummer 59.
- `modell/gesamtrechnung.py` + `gesamtrechnung.toml`: geltende Rechnung (Selbstprüfung gegen die Originale).
- `modell/rahmen/` Originalskripte (unverändert), `parameter.toml` + Zweitrechnung: Regression der Fassung 4. Oktober.
- `modell/laender/` Länderrechnungen nach Standard (`STANDARD.md`, Fassung 1.3): ein Skript `rechne.py`, je Land `<cc>.toml`; Ergebnisse `daten/aggregate/laender/`. Gerechnet: Frankreich, Spanien, Niederlande, Belgien, Polen; gemeinsame Klubwirkung FR+ES+NL 81,55 % (`laender_klub.json`, nach Korrektur 57).
- `modell/laendervergleich.py` + `modell/laender/vergleich.toml`: Ländervergleich nach den Kriterien der Webseite (elf Länder), Ergebnis `daten/aggregate/laendervergleich.json`. Arbeitsweise für nachfolgende Agenten: `modell/laender/ARBEITSANWEISUNG.md` (Kopie im Projektraum).
- `modell/uebergang.py` + `uebergang.toml`: Übergangsrechnung 2028–2060 nach der Leitlinie v3.29 (nationaler Ausgangspunkt, Angleichung durch gleiche Regeln): Dividende je Land nach V3a und V2B, Angleichung als Szenario.
- `modell/anreize.py` + `anreize.toml`: Abgabenkeil heute (OECD Taxing Wages 2025) gegen 28:28 und Wachstumszuschlag je Land (relativ zum Klub).
- `modell/nachfrage.py` + `nachfrage.toml`: Nachfrageprüfung (Umverteilung, Produktgruppen, Label); Prüfbefund zum Konsumaufkommen (Nahtstelle N19).
- `dokumente/` Gesamtkonzept (aus der Rechnung gebaut), `archiv/` ältere Fassungen.
- `projekt/` Bausteinregister (22), Nahtstellen (13), Prüfsummen, `pruefe_projekt.py`.
- `schnittstelle/`, `beitraege/` für Dritte (Mikrosimulation erst nach Prüfung der Aggregate).

## Ablauf je Änderung
1. Parameter (`gesamtrechnung.toml`) oder Skript ändern. 2. `NODE_PATH=/opt/npm-tools/node_modules node
dokumente/werkzeuge/gesamtkonzept-bau.js`, danach in `dokumente/` `soffice --headless --convert-to pdf
TAX-2828-Gesamtkonzept.docx`. 3. `python3 modell/alles.py` (alle Stufen). 4. Logbuch-Eintrag mit Datum, Änderung,
Quelle, bewegter Zahl. 5. Register anpassen. 6. Ein Commit, ein Tag. 7. Projektraum nachführen.
Tag-Push scheitert über den Sitzungsproxy (HTTP 403); Tags und GitHub Releases setzt der Verantwortliche.
Eurostat ist über das Web-Abrufwerkzeug erreichbar (nicht über die Shell): je Land und Dimension einzeln, Ratenbegrenzung beachten.

## Reihenfolge der offenen Arbeit
0. **Entscheidungen v3.33:** E1 C, E2 V2, E3 je Land, E4 81,3 %. Offen: zusätzliche Lücke 1,19 ohne Verletzung der Mindestdividende schließen (Stufen 1/1,5/2/3 bei 28 %: +1,14; oder Bausteine). v3.35: 28:28 bleibt, Verteidigung außen vor, Strategie Verwaltung (belegt 0,1 bis 0,3 % BIP). v3.36: Ablösung der Sozialverwaltung (0,45 bis 0,78) und Dach auf Kernaufgaben (0,8 bis 1,65) machen Pakete stabil (P6 bis P8); **v3.37: P8 und alle Empfehlungen eingerechnet: Quote 30,2 %, Obergrenze 32 %, Deckung 30,44 (Überschuss 0,24), Reserve 1,08, stabil; Korrektur 59 (Ablösung schließt keine Lücke der Quote); EU-Rechtsrahmen nach Entscheidung nicht bindend.** **v3.38: deutscher Textentwurf (Gesamtkonzept, Kurzfassung, Webseite de) in `dokumente/entwurf/`, `seite/entwurf/`; v3.39: freigegeben (mit Korrekturen an der Webseite) und übernommen; Gesamtkonzept, Kurzfassung und sechs Sprachfassungen der Seite auf Stand 10. Oktober 2026. Geänderte Textteile maschinell übersetzt: muttersprachlich gegenlesen (B16), mindestens FR und PL.** Nächstes: Aufgabenliste des Dachs, Produktliste des Labels, Ausgleichsrücklage, B12 auf Klubebene. **v3.42: Vorschläge Generationenbaustein und Hütte/Route/Seil geprüft und zusammengeführt (`projekt/Zusammenfuehrung-Sozialschutz-2026-10-16.md`); Rechnung `modell/sozialschutz.py`: Z 2028 ≈ 8,9 % BIP, Auslauf bis ≈ 2075; 28:28 bleibt nur mit eigenem, sinkendem Übergangsbeitrag; Korrektur 60 (Gesamtlast-Aussage unvollständig). Antwortbogen S1–S13 offen.**
   **Konsumaufkommen (v3.31):** Zuordnung der Produkte zu den Labelstufen festlegen; effektiver Satz 14,9 bis 16,9 % statt 20 % würde die Deckungslücke um 1,2 bis 2,0 Punkte vergrößern.
1. **B12 auf Klubebene:** Deckung der Quote aus den Steuerbasen der zehn Staaten (deutsche Basis: Lücke 0,95 Punkte).
2. **B15:** BIP (DE bei Eurostat revidiert, +1,34 %), Schuldenquoten, Renditen, COFOG-Posten neu abrufen; Zinsausgaben Estland nachholen. **B19:** Zuordnung der Posten dokumentieren.
3. **B16:** Seite in sechs Sprachen (`seite/stand-b/*.html`, Bau: `python3 seite/werkzeuge/seite_bau.py`); Gegenlesen, Länderanpassung und Veröffentlichung offen.
4. Haushaltsmikrosimulation (kalibriert die Tarifstufen 0/9/16/21/28 am Grundbedarf).
5. **Leitlinie v3.29/v3.30 (Entscheidungen):** Regel der Dividende (V2 nach Leitlinie, gleiches Recht, auch Irland); Mindestdividende im Klubschnitt oder je Land; Anreize für Investition, Binnenmarkt und Arbeitsangebot quantifizieren (Literatur widersprüchlich).
6. **Länderrechnungen:** Polen 2028 aus dem Original; weitere Länder; Entscheidung über Wachstum je Land (Polen 6,2 % nominal statt 3,0 %); Umsetzung in Webseite und Konzepttexten (Standard 6, Nahtstelle N16); Abgabenkeil je Land (OECD Taxing Wages) für den Vergleich „heute gegen 28:28“.
