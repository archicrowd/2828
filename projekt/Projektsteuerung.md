# Projektsteuerung TAX 28:28 (Stand v3.15, 7. Oktober 2026)

Maßgeblich ist das private Repository `archicrowd/2828` (main). Der Projektraum „2525" spiegelt Logbuch
Band I bis III und diese Anleitung; der Abgleich geschieht von Hand.
Autor und Projektverantwortlicher des Konzepts: Arndt Hermann. Lizenz: Skripte MIT, Texte und Ergebnisse CC BY 4.0.

## Geltende Fassung
Gesamtkonzept vom 6. Oktober 2026 (dazu Kurzfassung, zwei Seiten): Quote 30,8 %, Obergrenze von A 36 % des Einzugs, Dividende im Klubschnitt
490 € je Einwohner und Monat 2028, Tiefpunkt 479 € 2035, 662 € 2060 (Preise 2028). Rechnung `modell/gesamtrechnung.py`.

## Einstieg für Dritte
`DATENZUGANG.md` (Menschen), `AGENTS.md` (KI-Agenten), `projekt/manifest.json` (maschinenlesbar),
`daten/quellen.csv` (21 Quellen), `daten/aggregate/eingangswerte.csv` (125 Werte mit Abrufadresse).

## Aufbau
- `logbuch/` Versionsgeschichte (Band I bis III); Korrekturen fortlaufend, nächste freie Nummer 53.
- `modell/gesamtrechnung.py` + `gesamtrechnung.toml`: geltende Rechnung (Selbstprüfung gegen die Originale).
- `modell/rahmen/` Originalskripte (unverändert), `parameter.toml` + Zweitrechnung: Regression der Fassung 4. Oktober.
- `dokumente/` Gesamtkonzept (aus der Rechnung gebaut), `archiv/` ältere Fassungen.
- `projekt/` Bausteinregister (20), Nahtstellen (13), Prüfsummen, `pruefe_projekt.py`.
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
3. **B16:** Neue deutsche Seite `seite/stand-b/de.html` liegt vor (Bau: `python3 seite/werkzeuge/seite_bau.py`); Übersetzungen und Veröffentlichung offen.
4. Haushaltsmikrosimulation (kalibriert die Tarifstufen 0/9/16/21/26/28).
