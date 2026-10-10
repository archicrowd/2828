# Projektsteuerung TAX 28:28 (Stand v3.28, 10. Oktober 2026)

Maßgeblich ist das private Repository `archicrowd/2828` (main). Der Projektraum „2525" spiegelt Logbuch
Band I bis III und diese Anleitung; der Abgleich geschieht von Hand.
Autorin des Konzepts: Initiative 28:28 (Name nur im Impressum der Webseite). Lizenz: Skripte MIT, Texte und Ergebnisse CC BY 4.0.

## Geltende Fassung
Gesamtkonzept vom 7. Oktober 2026 (dazu Kurzfassung, zwei Seiten): Quote 31,9 %, Obergrenze von A 35 % des Einzugs, Dividende nach Preisniveau des Wohnlandes (seit v3.20), Boden halbes
Existenzminimum; Deutschland 591 € je Erwachsenem und Monat 2028, 801 € 2060; Klubschnitt 537 € je Einwohner 2028, Tiefpunkt 529 € 2032 (Preise 2028); Umzugsregel drei Jahre mit Steuernachweis (Kinder, Studierende ohne; Fälle ohne Einkommen vorerst ausgeklammert); Tarif 0/9/16/21/28 % mit Stufen beim 1- bis 4-fachen Grundbedarf (DE 2028: 12.847 / 25.694 / 38.541 / 51.387 €); Schuldenquote 2028 81,3 % (Fortschreibung des Status quo, seit v3.19). Rechnung `modell/gesamtrechnung.py`.

## Einstieg für Dritte
`DATENZUGANG.md` (Menschen), `AGENTS.md` (KI-Agenten), `projekt/manifest.json` (maschinenlesbar),
`daten/quellen.csv` (21 Quellen), `daten/aggregate/eingangswerte.csv` (125 Werte mit Abrufadresse).

## Aufbau
- `logbuch/` Versionsgeschichte (Band I bis III); Korrekturen fortlaufend, nächste freie Nummer 58.
- `modell/gesamtrechnung.py` + `gesamtrechnung.toml`: geltende Rechnung (Selbstprüfung gegen die Originale).
- `modell/rahmen/` Originalskripte (unverändert), `parameter.toml` + Zweitrechnung: Regression der Fassung 4. Oktober.
- `modell/laender/` Länderrechnungen nach Standard (`STANDARD.md`, Fassung 1.3): ein Skript `rechne.py`, je Land `<cc>.toml`; Ergebnisse `daten/aggregate/laender/`. Gerechnet: Frankreich, Spanien, Niederlande, Belgien, Polen; gemeinsame Klubwirkung FR+ES+NL 81,55 % (`laender_klub.json`, nach Korrektur 57).
- `modell/laendervergleich.py` + `modell/laender/vergleich.toml`: Ländervergleich nach den Kriterien der Webseite (elf Länder), Ergebnis `daten/aggregate/laendervergleich.json`. Arbeitsweise für nachfolgende Agenten: `modell/laender/ARBEITSANWEISUNG.md` (Kopie im Projektraum).
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
1. **B12 auf Klubebene:** Deckung der Quote aus den Steuerbasen der zehn Staaten (deutsche Basis: Lücke 0,95 Punkte).
2. **B15:** BIP (DE bei Eurostat revidiert, +1,34 %), Schuldenquoten, Renditen, COFOG-Posten neu abrufen; Zinsausgaben Estland nachholen. **B19:** Zuordnung der Posten dokumentieren.
3. **B16:** Seite in sechs Sprachen (`seite/stand-b/*.html`, Bau: `python3 seite/werkzeuge/seite_bau.py`); Gegenlesen, Länderanpassung und Veröffentlichung offen.
4. Haushaltsmikrosimulation (kalibriert die Tarifstufen 0/9/16/21/28 am Grundbedarf).
5. **Länderrechnungen:** Polen 2028 aus dem Original; weitere Länder; Entscheidung über Wachstum je Land (Polen 6,2 % nominal statt 3,0 %); Umsetzung in Webseite und Konzepttexten (Standard 6, Nahtstelle N16); Abgabenkeil je Land (OECD Taxing Wages) für den Vergleich „heute gegen 28:28“.
