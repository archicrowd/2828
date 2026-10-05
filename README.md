# TAX 28:28

Modell und Dokumentation eines Steuer- und Abgabenkonzepts mit einem einheitlichen
Satz von 28 % (Einkommensteuer-Spitze, Kapital, Unternehmen und Plattformen,
Erbschaft, Mehrwertsteuer-Topstufe), gerechnet zunächst für Deutschland, dann für
einen europäischen Kern von zehn Staaten.

Dieses Repository ist die **Rückseite der Webseite**: Es zeigt, woher jede Zahl
kommt, wann sie sich geändert hat und was sich als falsch erwiesen hat.

**Modellstand: v3.6** (Logbuch Band III, 5. Oktober 2026). Das Release `v3.5`
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

## Was dieses Repository nicht kann

Die Skripte der Versionen bis v3.4 sind nicht enthalten. Sie lagen in einer
flüchtigen Arbeitsumgebung, die zurückgesetzt wurde (Logbuch Band II,
„Vorbemerkung zur Lücke"). Was vor diesem Repository gerechnet wurde, ist im
Logbuch beschrieben, aber aus diesem Repository **nicht reproduzierbar**.
Reproduzierbar ist nur, was ab dem ersten Skript-Commit hier liegt.

Seit v3.6 liegt `modell/pfad.py` als **Rekonstruktion** vor, nicht als Original. Sie
trifft 23 von 23 Referenzwerten der Zeitpfad-Tabelle (`daten/aggregate/pfad_abgleich.csv`).
Das zeigt Übereinstimmung, nicht, dass das Original so gerechnet hat.

## Datenauflagen

Rohdaten gehören nicht in dieses Repository. Maßgeblich ist Logbuch Abschnitt 5.
Kurzfassung: Taxplorer (CC BY-NC-ND 4.0), OECD-Rohdaten, SOEP und EU-SILC-Mikrodaten
werden nicht weitergegeben. Nur Skripte und Aggregate, mit Zitat.
