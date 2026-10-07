# dokumente/

| Datei | Stand | Rolle |
|---|---|---|
| `TAX-2828-Gesamtkonzept.pdf` / `.docx` | 7. Oktober 2026, Stand B, Quote 30,9 % | **maßgeblich**, zwölf Seiten, gebaut aus `daten/aggregate/gesamtrechnung.json`; geprüft mit `modell/pruefe_konzept.py` |
| `TAX-2828-Kurzfassung.pdf` / `.docx` | 6. Oktober 2026 | zwei Seiten für Laien, gebaut mit `werkzeuge/kurzfassung-bau.js`; geprüft mit `modell/pruefe_konzept.py` |
| `archiv/TAX-2828-Gesamtkonzept-2026-10-04.*` | 4. Oktober 2026, Quote 30,6 % | abgelöst; Grundlage des Aussagenregisters `aussagen.csv` (Regression), Prüfsumme in `projekt/pruefsummen.sha256` |
| `28-28-Homepage-Datenblatt.md` | 16. September 2026, Stand A | Datenblatt zur Seite (Modell `modell-2828.py`) |
| `28-28-Levelanalyse.md` | 16. September 2026, Stand A | Einheitssatz L zwischen 25 und 30 % |
| `DD-Startniveau-500-600.md` | 16. September 2026, Stand A | Startniveau der Dividende |
| `archiv/` | | `Rahmenstruktur-A-und-B.docx` (3. Okt., v3.1), `...-v3.docx` (4. Okt., v3.4, Quote 27,91 %), `Rechenstand-Oktober.docx` (v3.0 bis v3.3). Vom Gesamtkonzept abgelöst |
| `werkzeuge/gesamtkonzept-bau.js` | | erzeugt die Word-Datei aus der Gesamtrechnung (Node, `docx`); PDF danach mit `soffice --headless --convert-to pdf` |

Nicht vorhanden: `Rahmenstruktur-A-und-B-v2.docx` (v3 enthält v2), ein Audit als Word-Datei (das
Audit liegt als Logbuchabschnitt v3.0 und in `modell/audit/`).
Die PDF-Fassung des Gesamtkonzepts wurde gelesen; die Word-Fassung stimmt laut Begleitdatei
des Vorchats überein, ein Textvergleich steht aus.
