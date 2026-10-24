# TAX 28:28

Modell und Dokumentation eines Steuer- und Abgabenkonzepts mit einem einheitlichen
Satz von 28 % (Einkommensteuer-Spitze, Kapital, Unternehmen und Plattformen,
Erbschaft, Mehrwertsteuer-Topstufe), gerechnet zunächst für Deutschland, dann für
einen europäischen Kern von zehn Staaten.

Dieses Repository ist die **Rückseite der Webseite**: Es zeigt, woher jede Zahl
kommt, wann sie sich geändert hat und was sich als falsch erwiesen hat.

**Modellstand: v4.47** (Logbuch Band III, 24. Oktober 2026). Geltend ist Stand C „Das Goldene Drittel“ (siehe unten); die frühere Fassung des Gesamtkonzepts vom 10. Oktober 2026 (Stand B, Quote 30,2 %, `modell/gesamtrechnung.py`) ist Vorläufer. Lizenz: Skripte MIT, Texte und Ergebnisse CC BY 4.0 (`LIZENZ.md`). **Einstieg für Dritte: `DATENZUGANG.md`, für KI-Agenten: `AGENTS.md`.** Das Release `v3.5`
auf GitHub zeigt auf den Stand des übernommenen Logbuchs (Commit `a5808b1`).

Einstieg: `INDEX.md` (Wegweiser, Stand A und Stand B, Naht zwischen beiden).

## Aktueller Stand: Stand C „Das Goldene Drittel“ (Fassung 4.x, seit v3.43)

**Die Webseite (www.archicrowd.de, „Das Goldene Drittel“) und das Konzept Fassung 4.x rechnen mit Stand C, nicht mit der
28:28-Gesamtrechnung.** Stand A (national) und Stand B (europäisch, `modell/gesamtrechnung.py`, Quote 30,2 %) sind Vorläufer und bleiben als
Referenz und Regressionsprüfung erhalten. Bis v4.11 wiesen README, INDEX, AGENTS und DATENZUGANG fälschlich Stand B als geltend aus
(Korrektur 66).

| Baustein | Skript (Parameter in `.toml`, Ergebnis in `daten/aggregate/`) |
|---|---|
| Tarif 0/11/19/25/33 % am Grundbedarf, Mehrwertsteuer-Label, Deckung | `modell/systemvarianten.py` (System 33R), `modell/projektion33.py` (Zeitpfad 2028–2060) |
| Starkes Netz, Mindestrente, Dividende | `modell/netz33.py`, `modell/dynamik33.py` |
| Altlasten: Schuld und Altrenten, gemeinsamer Fonds, Rentnerregeln | `modell/sozialschutz.py`, `modell/altlasten.py`, `modell/neustart33.py`, `modell/rentnerausgleich.py` |
| 30 Staaten (Möglichkeitsraum), Länderseiten | `modell/moeglichkeitsraum33.py`, `modell/laenderseiten.py` |
| Haushalte heute gegen neu | `modell/haushalte33.py` (DE), `modell/heute_laender.py`, `modell/sozial_laender.py` (FR, IT, ES, PL) |
| Grundauskommen (Aufstockung mit Halbanrechnung), Härtefall | `modell/regel_boden.py`, `modell/boden_kosten.py`, `modell/kindergewicht.py`, `modell/haertefall.py` (Dateinamen historisch) |
| Verteilung (Gini), Empfindlichkeiten, Gesamtlast | `modell/gini.py`, `modell/gini_frankreich.py`, `modell/weitergabe_sensitivitaet.py`, `modell/gesamtlast33.py` |
| Architektur: gemeinsame Aufgaben, Regionen (DE, Kreise) | `modell/dach_beitrag.py`, `modell/regionen_de.py` (Rohdaten je Kreis nur lokal) |
| Offene Punkte der Prüfung: Rückfallregel, Preisniveau, Ausweichen | `modell/weitergabe_rueckfall.py`, `modell/preisniveau33.py`, `modell/ausweichen33.py` |
| Fonds der 30, Verrechnung je Staat, Kürzungssatz der Renten je Staat | `modell/fonds_klub.py`, `modell/kuerzung_laender.py`, `modell/verrechnung_haushalte.py`, `modell/fondszins.py` |
| Mikrosimulation DE (Beschäftigte, Beamte, Selbständige, Rentner, Kapital, Inanspruchnahme), Rentnerregel E | `modell/mikro_de.py`, `modell/mikro_bs_de.py`, `modell/mikro_rentner_de.py`, `modell/rentner_kombi.py` |
| Mehrwertsteuer nach Einkommen, Vermögensbasis, Deckel der Weitergabe | `modell/mwst_verteilung.py`, `modell/vermoegensbasis33.py`, `modell/deckel_einheitlich.py` |
| Webseite (sechs Sprachen) | `seite/werkzeuge/drittel_bau.py` → `seite/stand-c/` |
| Konzept und Kurzfassung | `dokumente/werkzeuge/konzept33-bau.js` → `dokumente/entwurf/TAX-Drittel-Konzept.pdf` |

Welche Zahl gilt und wie sie abgegrenzt ist (Dividendenpfade, Altlasten, Gesamtlast, Lohnbasis): **`KENNZAHLEN.md`**. Für eine externe Prüfung: **`projekt/Pruefmappe-Extern-2026-10-24.md`**. Alle Stufen: `python3 modell/alles.py`. Beschlüsse und offene Punkte: Logbuch Band III ab v3.43, Abschnitt 7.

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
