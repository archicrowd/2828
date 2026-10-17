# TAX 28:28 — Wegweiser durch das Repository

Stand: 10. Oktober 2026 · Modellstand v3.51 · Einstieg für Dritte: `DATENZUGANG.md`, für KI-Agenten: `AGENTS.md`

Dieses Repository enthält **zwei Entwicklungsstände**, die einander in Teilen widersprechen.
Wer eine Zahl zitiert, nennt den Stand dazu.

| | Stand A — national | Stand B — europäisch |
|---|---|---|
| Rahmen | Deutschland, fünf Verwaltungsebenen | Klub A und Kommunen B, zwei Ebenen |
| Steuerquote | 27,91 % (v3.4) bzw. 33 % | 30,60 % (v3.5) |
| Sozialabgaben | Position 10, 42 → 28 → 18 % | gestrichen |
| Dividende | 515 € (50 % des Existenzminimums) | Restgröße bei B, 506 € im Klubschnitt (Preise 2028) |
| Logbuchstand | v2.0 | v3.5 und später |
| Wo | `modell/kern/`, `seite/stand-a-*` | `modell/rahmen/` (Original), `modell/gesamtrechnung.py` (geltend), `dokumente/TAX-2828-Gesamtkonzept.*` |

Quelle dieser Angabe: Begleitdatei des Vorchats (`LIESMICH-EXPORT.md`), von mir an Logbuch,
Gesamtkonzept und Skripten stichprobenhaft bestätigt, nicht Zeile für Zeile geprüft.

## Wo liegt was

| Frage | Ort |
|---|---|
| Woher kommt eine Zahl, wann änderte sie sich, was war falsch? | `logbuch/` (Band I bis III), Korrekturen 1 bis 48 |
| Was gilt als Gesamtkonzept? | `dokumente/TAX-2828-Gesamtkonzept.pdf` (Stand B, 6. Oktober 2026, aus `modell/gesamtrechnung.py`; Fassung 4. Oktober in `dokumente/archiv/`) |
| Wie rechnet das Rahmenmodell (Stand B)? | `modell/rahmen/` (Originale), `modell/pfad.py` und `modell/aufschlag.py` (Zweitrechnung), `modell/parameter.toml` |
| Wie rechnet das nationale Gesamtmodell (Stand A)? | `modell/kern/modell-2828.py` |
| Einzelrechnungen (Erbschaft, Immobilien, Vermögen, Klima, OECD, Haushalt) | `modell/rechnungen/`, Stand A |
| Audit der Gesamtlogik (v3.0) | `modell/audit/` |
| Webseite | `seite/` (Stand A; eine Seite zum Stand B liegt in `seite/rahmenstruktur-seiten/`) |
| Ergebnisdateien | `daten/aggregate/` |
| Drittquellen, die nicht eingecheckt sind | `daten/herkunft/uploads-manifest.csv` (Name, Größe, SHA-256) |
| Eigene Dateien aus früheren Sitzungen, teils andere Fassung | `archiv/uploads-eigen/` |

## Die Naht zwischen A und B

Das Rahmenmodell (B) rechnet **ab der Steuerquote 30,6 %**. Es leitet sie aus dem Versprechen
von 479 € ab (Mindestquote 30,61 % ohne reales Wachstum). Dass die Steuerpositionen des
nationalen Modells (A) diese Quote tatsächlich aufbringen, ist in den gelesenen Dateien
**nicht gerechnet** (Logbuch Band III, B12). Das nationale Modell lieferte 27,91 %.

## Regeln

Siehe `CLAUDE.md` (Arbeitsregeln), `README.md` (Versionierung, Datenauflagen) und
`logbuch/HERKUNFT.md` (Herkunft und Prüfstand der Logbuch-Dateien).
