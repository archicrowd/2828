# Arbeitsregeln für dieses Repository

## Haltung

- Wissenschaftlich arbeiten: Behauptungen hinterfragen, Quellen angeben.
- Bei nur einer Quelle oder einer nicht amtlichen Quelle kritisch bleiben und das
  im Text kennzeichnen (Muster: „Sekundärquelle", „Annahme", „maschinell aus dem
  PDF gelesen, an der Quelle zu prüfen").
- Sachliche Sprache. Keine Werbesprache, keine unbelegten Superlative.

## Logbuch

- Nach **jeder Rechnung** das Logbuch fortschreiben und committen, nicht am Ende
  einer Sitzung. Die Arbeitsumgebung ist flüchtig, das Repository nicht.
- Versionsschema und Pflichtangaben je Version: siehe `logbuch/` (Abschnitt 2).
  Jede Version nennt Datum, Änderung, Datenquelle, bewegte Zahl und wodurch es auffiel.
- Korrekturen werden fortlaufend nummeriert. **Nächste freie Nummer: 73.**
  Alle Nummern bis 72 sind besetzt (31 bis 41 in Band I; die frühere Aussage, sie seien
  unbesetzt, war falsch, Korrektur 47). Nummern werden nie neu vergeben.
- Fehler offen führen, auch eigene. Ein Entwurf, dessen Irrtümer offen liegen, ist
  überprüfbar.

## Daten

- Keine Rohdaten committen. Auflagen: `logbuch/` Abschnitt 5.
- Taxplorer: Rohdatenbank niemals weitergeben (CC BY-NC-ND 4.0). Nur Aggregate mit Zitat.
- SOEP und EU-SILC-Mikrodaten nur mit Datenvertrag und nicht in dieses Repository.
- Für Aufkommensrechnungen aus den OECD-Länderberichten nur Panel `_T` verwenden,
  nicht `PANELAI` (Panel-Falle, Logbuch Abschnitt 4).

## Rechnung

- Pro Rechnung: ein Skript in `modell/`, Parameter im Parameterfile, Ergebnis als
  maschinenlesbare Datei in `daten/aggregate/`.
- Euro-Beträge immer mit Bezugsjahr und Preisbasis (nominal oder real) kennzeichnen.
  Anteile am BIP und Eurowerte nicht ohne Bezugsgröße nebeneinanderstellen
  (Korrekturen 42 bis 46).
- Eine Behauptung, die sich prüfen lässt, wird geprüft, bevor sie stehen bleibt.

## Projektverwaltung

- Vor jedem Commit `python3 modell/alles.py` ausführen (alle Stufen, Register in `projekt/`). Rückgabe
  ungleich 0 oder neuer Fehler: erst beheben oder offen im Logbuch führen.
- Nach jeder Version `projekt/bausteine.csv` und `projekt/nahtstellen.csv` anpassen. Prüfsummen
  (`projekt/pruefsummen.sha256`) nur bewusst mit `--aktualisieren` ändern und im Logbuch vermerken.
- Projektraum "2525" (Band I bis III, `Projektsteuerung.md`) nach jeder Version von Hand nachführen;
  maßgeblich bleibt das Repository.
- Autorschaft durchgängig: Initiative 28:28 (`CITATION.cff`). Der Name des Verantwortlichen erscheint nur im
  Impressum der Webseite. Keine weiteren Personennamen oder E-Mail-Adressen aus Quellen übernehmen.

- Geltende Rechnung: Stand C „Das Goldene Drittel“ (Skripte im README, Abschnitt „Aktueller Stand“; Konzept nur über
  `dokumente/werkzeuge/konzept33-bau.js`). Vorläufer Stand B: `modell/gesamtrechnung.py` (+ `gesamtrechnung.toml`). Das Gesamtkonzept Stand B wird nur über
  `dokumente/werkzeuge/gesamtkonzept-bau.js` gebaut, nie von Hand; danach `modell/pruefe_konzept.py`.
- Lizenz: Skripte MIT, Texte und Ergebnisse CC BY 4.0 (`LIZENZ.md`).

## Commits

- Eine Version, ein Commit, ein Tag `vX.Y.Z`.
- Commit-Nachricht: erste Zeile Version und Thema, danach die bewegte Zahl und die Quelle.
- Dateinamen ohne Umlaute und Leerzeichen.
