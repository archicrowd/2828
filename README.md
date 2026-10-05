# TAX 28:28

Modell und Dokumentation eines Steuer- und Abgabenkonzepts mit einem einheitlichen
Satz von 28 % (Einkommensteuer-Spitze, Kapital, Unternehmen und Plattformen,
Erbschaft, Mehrwertsteuer-Topstufe), gerechnet zunächst für Deutschland, dann für
einen europäischen Kern von zehn Staaten.

Dieses Repository ist die **Rückseite der Webseite**: Es zeigt, woher jede Zahl
kommt, wann sie sich geändert hat und was sich als falsch erwiesen hat.

**Modellstand: v3.8** (Logbuch Band III, 5. Oktober 2026). Das Release `v3.5`
auf GitHub zeigt auf den Stand des übernommenen Logbuchs (Commit `a5808b1`).

## Aufbau

| Ordner | Inhalt |
|---|---|
| `logbuch/` | Versionsgeschichte, Korrekturen, Datenbestand, Rechenplan, offene Punkte |
| `modell/` | Rechenskripte (Python), je Rechnung eine Datei, mit Parameterfile |
| `daten/aggregate/` | Ergebnisdateien (`.csv`) und aufbereitete Aggregate mit Quellenangabe |
| `daten/roh/` | **nur lokal, wird nicht versioniert** (siehe `.gitignore`) |
| `seite/` | Webseite in den Sprachfassungen |
| `dokumente/` | Ausgearbeitete Dokumente (Gesamtkonzept, Audit, Rahmenstruktur) |

## Versionierung

Schema `MAJOR.MINOR.PATCH` wie im Logbuch (Abschnitt 2):

- **MAJOR**: eine Position ändert sich inhaltlich
- **MINOR**: eine Annahme wird durch eine Quelle ersetzt, oder eine neue Rechnung kommt hinzu
- **PATCH**: Korrektur ohne inhaltliche Änderung

Jede Version ist ein Commit mit Git-Tag `vX.Y.Z`. Das Logbuch wird im selben Commit
fortgeschrieben wie die Rechnung, die es beschreibt.

## Was dieses Repository (noch) nicht kann

- **Reproduzierbar** ist der Zeitpfad des Rahmenmodells (Klub A / Gemeinden B) aus den
  Originalskripten in `modell/rahmen/` und, unabhängig davon, aus `modell/pfad.py` und
  `modell/aufschlag.py` mit `modell/parameter.toml`. `modell/vergleich_original.py` prüft beide
  gegeneinander. Die Eingangsdaten (Eurostat 2024) stehen als feste Zahlen im Skript und sind
  **nicht an der Quelle geprüft**; für acht Länder weichen die Einwohnerzahlen der beiden
  Datensätze ab (Logbuch Band III, B7).
- **Noch nicht eingecheckt** sind aus dem Export des Vorchats: das nationale Gesamtmodell
  (`modell-2828.py` und Ergebnisse), die achtsprachige Webseite mit Quelltext, das
  Gesamtkonzept als Word und PDF, die Einzelrechnungen (Erbschaft, Immobilien, Vermögen, Klima,
  OECD) und das Audit. Diese Teile stehen auf dem **älteren, nationalen Stand A**, das
  Gesamtkonzept auf dem europäischen **Stand B**; beides widerspricht sich (Band III, v3.8, Abschnitt 7).
- Das Logbuch Band I ist seit v3.8 vollständig (v0.1 bis v3.4). Eine frühere Fassung dieses
  Textes behauptete, die Einträge bis v3.4 seien verloren; das war falsch (Korrektur 47).

## Datenauflagen

Rohdaten gehören nicht in dieses Repository. Maßgeblich ist Logbuch Abschnitt 5.
Kurzfassung: Taxplorer (CC BY-NC-ND 4.0), OECD-Rohdaten, SOEP und EU-SILC-Mikrodaten
werden nicht weitergegeben. Nur Skripte und Aggregate, mit Zitat.
