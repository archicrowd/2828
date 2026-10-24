# Datenzugang: TAX 28:28 prüfen und weiterbearbeiten

Diese Seite ist für Dritte geschrieben: Fachleute, Prüferinnen und Prüfer, Studierende und KI-Agenten. Sie sagt,
wo jede Zahl herkommt, wie man sie nachprüft und wie man am Konzept weiterarbeitet. KI-Agenten lesen zusätzlich
`AGENTS.md`. Die Projektkarte in Maschinenform steht in `projekt/manifest.json`.

Stand: Modellstand und Fassung siehe `INDEX.md`. **Für die Prüfung von Stand C (geltend) zuerst `projekt/Pruefmappe-Extern-2026-10-24.md`;** diese Seite beschreibt den Datenweg überwiegend für Stand B. Autorin: Initiative 28:28,
2828@archicrowd.de.

## 1 Zugang zum Material

| Was | Wo | Zugang |
|---|---|---|
| Repository (Rechnungen, Logbuch, Dokumente) | github.com/archicrowd/2828 | Sichtbarkeit laut GitHub am 24.10.2026: **öffentlich** (bis v4.45 stand hier „privat“, Korrektur 76). Für Weitergabe ohne GitHub: `git archive --format=tar HEAD` erzeugt ein Paket ohne Versionsgeschichte |
| Gesamtkonzept und Kurzfassung | `dokumente/TAX-2828-Gesamtkonzept.pdf`, `dokumente/TAX-2828-Kurzfassung.pdf` | im Repository |
| Logbuch (alle Versionen, 52 Korrekturen) | `logbuch/` (Band I bis III) | im Repository; Spiegel im Projektraum auf claude.ai (nicht öffentlich) |
| Amtliche Eingangsdaten | Eurostat-API, OECD | offen, ohne Anmeldung |
| Gesperrte Daten | Taxplorer, SOEP, EU-SILC, Drittdateien | nicht im Repository; nur beim Anbieter (Abschnitt 4) |

Lizenz: maßgeblich ist `LIZENZ.md` (Skripte MIT, Wortlaut in `LICENSE`; Texte und Ergebnisse CC BY 4.0, Hinweis in
`LICENSE-DOKUMENTE.md`). Daten Dritter unterliegen den Bedingungen ihrer Anbieter.

## 2 Von der Quelle zum Dokument

```
Eurostat / OECD / Gesetz        daten/quellen.csv            (21 Quellen, Status, Weitergabe)
        │                       daten/aggregate/eingangswerte.csv  (120 Werte, je eine Abruf-URL)
        ▼
Eingangsdateien                 modell/rahmen/basis.py, modell/rechnungen/rahmen/daten.py (Abrufe 2.-4.10.2026)
                                daten/aggregate/laender_2024.csv, zinsausgaben_2024.csv (Abrufe 6.10.2026)
        ▼
Parameter und Entscheidungen    modell/gesamtrechnung.toml   (jede Setzung mit Quelle und Status)
        ▼
Rechnung                        modell/gesamtrechnung.py     (Formeln der Originale in modell/rahmen/;
                                                              Selbstprüfung gegen das Original)
        ▼
Ergebnis                        daten/aggregate/gesamtrechnung.json (+ _pfad.csv, _obergrenze.csv, deckung_quote.csv)
        ▼
Dokumente                       dokumente/werkzeuge/*-bau.js (Paket docx, siehe package.json) → *.docx → PDF
        ▼
Prüfung                         modell/pruefe_konzept.py (jede Kernzahl im PDF), modell/alles.py (alle Stufen)
```

## 3 Prüfen in vier Schritten

1. **Rechnung nachvollziehen.** `python3 modell/alles.py` führt alle Stufen aus (Python 3.11 oder neuer, nur
   Standardbibliothek). Erwartet: jede Stufe ohne Fehler. Die Gesamtrechnung prüft sich selbst: mit den Eingängen der
   Fassung vom 4. Oktober trifft sie die Originalskripte in allen 33 Jahren exakt.
2. **Eingangswerte an der Quelle prüfen.** `daten/aggregate/eingangswerte.csv` nennt für jeden amtlichen Wert die
   Eurostat-Adresse. Mit Netzzugang ruft `python3 modell/eingangswerte.py --abrufen` alle Werte einzeln ab und schreibt
   `daten/aggregate/eingangswerte_abgleich.csv`. Spalte `getestet`: ja = diese Abrufform hat im Projekt funktioniert;
   nein = Vorlage, Dimensionen vorher prüfen. **Immer ein Land und eine Größe je Abruf**; Sammelabrufe liefern bei
   Eurostat unvollständige oder falsch zugeordnete Werte. Eurostat revidiert; eine Abweichung kann eine Revision sein.
3. **Annahmen und Setzungen prüfen.** Jeder Parameter in `modell/gesamtrechnung.toml` und `modell/parameter.toml`
   trägt `status` (belegt, abgerufen, annahme, setzung, regel, schaetzung, entscheidung) und `quelle`. Die
   Entscheidungen vom 6. Oktober 2026 und ihre Begründung stehen im Logbuch, Band III, v3.12.
4. **Dokument gegen Rechnung prüfen.** `python3 modell/pruefe_konzept.py` sucht jede Kernzahl in der Schreibweise des
   PDF. Für alles Übrige: Text lesen, Behauptung in `gesamtrechnung.json` oder in `daten/quellen.csv` suchen.

**Bekannte Revision:** Eurostat meldet seit dem 6.10.2026 für Deutschland ein BIP 2024 von 4.386.940 Mio EUR
(vorläufig; im Modell 4.328.970, +1,34 %; maschinell gelesen am 7.10.2026). Die übrigen neun Länder sind nicht neu
abgerufen; die Rechnung bleibt bis zum vollständigen Neuabruf auf dem alten Stand (B15).

Was noch nicht geprüft ist, steht offen im Logbuch (Band III, Abschnitt 7), insbesondere: BIP, Schuldenquoten,
Renditen und COFOG-Posten seit dem 4. Oktober nicht neu abgerufen (B15); Zinsausgaben Estland geschätzt; die
Gruppenschätzung „über 95 %" stammt aus dem nationalen Modell ohne Mikrosimulation (B18); Dividende gleich oder je
Land (B17); die Zuordnung der COFOG-Gruppen zu den Posten der Ebenen A und B und die Bodenwertabgabe 0,82 sind nicht
als Tabelle mit Abrufadresse dokumentiert (B19).

## 4 Daten, die nicht weitergegeben werden

| Daten | Grund | Wie Dritte sie bekommen |
|---|---|---|
| Taxplorer-Rohdatenbank | CC BY-NC-ND 4.0 | eigene Anmeldung beim Anbieter; im Projekt nur Aggregate mit Zitat |
| SOEP, EU-SILC (Mikrodaten) | Datenschutz, Datenvertrag | eigener Vertrag mit DIW bzw. Eurostat; Ergebnisse nur als Aggregat zurückgeben |
| Drittdateien aus dem Vorchat (Studien, Tabellen) | Urheberrecht | beim Herausgeber; `daten/herkunft/uploads-manifest.csv` nennt Name, Größe und SHA-256 zur Identifikation |
| Vorchat auf claude.ai | nicht öffentlich | nicht zugänglich; was daraus übernommen ist, steht im Logbuch und ist als Sekundärquelle gekennzeichnet |

## 5 Weiterbearbeiten

- **Woran gearbeitet werden soll** (Reihenfolge des Verantwortlichen): Deckung der Quote auf Klubebene aus den
  Steuerbasen der zehn Staaten (B12); Neuabruf der übrigen Eingänge (B15); Seiten neu bauen (B16); danach die
  Haushaltsmikrosimulation. Schnittstelle: `schnittstelle/MIKROSIMULATION.md`, Ergebnisformat
  `schnittstelle/ergebnis-schema.csv`, Formprüfung `schnittstelle/pruefe_beitrag.py`.
- **Regeln** (`CLAUDE.md`, `CONTRIBUTING.md`): keine Rohdaten einchecken; eine Rechnung, ein Skript, Parameter im
  Parameterfile, Ergebnis maschinenlesbar; Euro-Beträge mit Bezugsjahr und Preisbasis; jede Änderung als neue Version
  im Logbuch mit bewegter Zahl und Quelle; Fehler als nummerierte Korrektur, auch eigene.
- **Beiträge** als Pull Request oder per E-Mail; sie stehen unter der Lizenz des Teils, in den sie eingehen, und werden
  im Logbuch vermerkt.

## 6 Begriffe

| Begriff | Bedeutung |
|---|---|
| Stand A / Stand B | nationales Modell (Quote 27,91 %, ältere Webseite) / europäisches Rahmenmodell (Gesamtkonzept) |
| Klub, Ebene A | gemeinsames Dach der zehn gerechneten Staaten |
| Ebene B | Gemeinden; erhalten die Formel je Einwohner und je Kind |
| Einzug | Quote abzüglich der Bodenwertabgabe, die B selbst erhebt |
| Dividende | Rest bei B nach den Fachaufgaben, monatlich je Einwohner (Kinder zur Hälfte) |
| Fassung 4. / 6. Oktober | abgelöste Gesamtkonzepte Stand B (`dokumente/archiv/`, `dokumente/`) |
| Stand C, Fassung 4.x | geltend: „Das Goldene Drittel“, Konzept `dokumente/entwurf/TAX-Drittel-Konzept.pdf`, Skripte siehe README (Korrektur 66) |
