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
- Korrekturen werden fortlaufend nummeriert. **Nächste freie Nummer: 47.**
  Die Nummern 31 bis 41 bleiben unbesetzt (siehe Band II, „Vorbemerkung zur Lücke").
  Nummern werden nie neu vergeben.
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

## Commits

- Eine Version, ein Commit, ein Tag `vX.Y.Z`.
- Commit-Nachricht: erste Zeile Version und Thema, danach die bewegte Zahl und die Quelle.
- Dateinamen ohne Umlaute und Leerzeichen.
