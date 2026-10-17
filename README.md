# TAX 28:28

Modell und Dokumentation eines Steuer- und Abgabenkonzepts mit einem einheitlichen
Satz von 28 % (Einkommensteuer-Spitze, Kapital, Unternehmen und Plattformen,
Erbschaft, Mehrwertsteuer-Topstufe), gerechnet zunächst für Deutschland, dann für
einen europäischen Kern von zehn Staaten.

Dieses Repository ist die **Rückseite der Webseite**: Es zeigt, woher jede Zahl
kommt, wann sie sich geändert hat und was sich als falsch erwiesen hat.

**Modellstand: v3.52** (Logbuch Band III, 10. Oktober 2026). Geltende Fassung des Gesamtkonzepts: 10. Oktober 2026, Quote 30,2 % (Entscheidungen vom 10. Oktober, freigegeben), dazu eine Kurzfassung (zwei Seiten), gerechnet von `modell/gesamtrechnung.py`. Lizenz: Skripte MIT, Texte und Ergebnisse CC BY 4.0 (`LIZENZ.md`). **Einstieg für Dritte: `DATENZUGANG.md`, für KI-Agenten: `AGENTS.md`.** Das Release `v3.5`
auf GitHub zeigt auf den Stand des übernommenen Logbuchs (Commit `a5808b1`).

Einstieg: `INDEX.md` (Wegweiser, Stand A und Stand B, Naht zwischen beiden).

## Aufbau

| Ordner | Inhalt |
|---|---|
| `logbuch/` | Versionsgeschichte, Korrekturen, Datenbestand, Rechenplan, offene Punkte |
| `modell/` | Rechenskripte: `rahmen/` (Originale Stand B), Zweitrechnung, Parameterfile, `kern/`, `rechnungen/`, `audit/` (Stand A); siehe `modell/LIESMICH.md` |
| `daten/aggregate/` | Ergebnisdateien (`.csv`, `.json`) und aufbereitete Aggregate mit Quellenangabe |
| `daten/herkunft/` | Manifest der Drittdateien (nicht eingecheckt) |
| `daten/roh/` | **nur lokal, wird nicht versioniert** (siehe `.gitignore`) |
| `seite/` | Webseite, Stand A, acht Sprachen; siehe `seite/LIESMICH.md` |
| `dokumente/` | Gesamtkonzept (maßgeblich), ältere Dokumente, Werkzeuge |
| `archiv/` | eigene Dateien aus früheren Sitzungen, teils abweichende Fassung |

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
  **nicht an der Quelle geprüft**. Die Klub-Einwohnerzahl ist seit v3.11 255,061 Mio (Eurostat demo_gind; Korrektur 49); das Gesamtkonzept
  rechnet seit v3.12 damit. `basis.py` bleibt als Original auf 254,8 Mio.
- **Stand A und Stand B** widersprechen sich (Quote 27,91 gegen 30,6 %, fünf Ebenen gegen
  zwei). Das nationale Modell, die Webseite und die Einzelrechnungen stehen auf Stand A und
  wurden nach dem Rahmenwechsel nicht neu gerechnet. Ob die Steuerpositionen die Quote 30,6 %
  tragen, ist nicht gerechnet (Logbuch Band III, B12).
- **Nicht ausgeführt**: die Skripte in `modell/kern/`, `modell/rechnungen/`, `modell/audit/` und
  die Patch-Skripte der Seite. Eingecheckt ist, was im Export lag.
- **Nicht eingecheckt**: Drittdateien (nur Manifest), OECD-Rohdaten, die Rechercheliste der
  Institute (enthält persönliche E-Mail-Adressen Dritter).
- Das Logbuch Band I ist seit v3.8 vollständig (v0.1 bis v3.4). Eine frühere Fassung dieses
  Textes behauptete, die Einträge bis v3.4 seien verloren; das war falsch (Korrektur 47).

## Datenauflagen

Rohdaten gehören nicht in dieses Repository. Maßgeblich ist Logbuch Abschnitt 5.
Kurzfassung: Taxplorer (CC BY-NC-ND 4.0), OECD-Rohdaten, SOEP und EU-SILC-Mikrodaten
werden nicht weitergegeben. Nur Skripte und Aggregate, mit Zitat.
