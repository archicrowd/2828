# modell/ — Rechenskripte

| Ordner / Datei | Stand | Inhalt |
|---|---|---|
| `rahmen/` | B | **Originalskripte** des Rahmenmodells aus dem Vorchat (4. Oktober 2026), unverändert: `basis.py` (Eurostat 2024, Fortschreibung), `pfad.py`, `final.py`, `tilgung.py`, `aufschlag.py`, `altschuld.py`, `kurve.py`, `zahlen.py`. Jedes Skript importiert `basis.py`, das beim Import druckt. `zahlen.py` schreibt nach `/home/claude/modell/` (absoluter Pfad im Original, nicht geändert); die Ausgaben liegen in `daten/aggregate/rahmen_original/` |
| `pfad.py`, `aufschlag.py`, `lauf.py` | B | **Zweitrechnung** aus `parameter.toml`, unabhängig von `rahmen/`; `lauf.py` prüft das Parameterfile |
| `vergleich_original.py` | B | vergleicht Zweitrechnung und Original (Ausgabe `daten/aggregate/vergleich_original.csv`) |
| `parameter.toml` | B | 31 Parameter mit Pflichtfeldern (Einheit, Bezugsjahr, Preisbasis, Quelle, Status) |
| `kern/` | A | nationales Gesamtmodell `modell-2828.py` (Mikro, Makro, Haushaltspfad), Ergebnisse, Rechnerlogik der Seite. Kalibriert auf BIP 4.200 Modell-Mrd; Korrektur 26 und 42 betreffen diese Basis |
| `rechnungen/` | A | Einzelrechnungen R1 bis R16 mit Befunden, siehe `rechnungen/LIESMICH.md` |
| `audit/` | A | Audit der Gesamtlogik, v3.0 (`a1` bis `a4` mit Ergebnisdateien) |

**Stand A und B nicht mischen.** Die Skripte in `kern/`, `rechnungen/` und `audit/` rechnen mit
der Modellbasis 4.200 Mrd und dem nationalen Rahmen. Sie sind nach v3.5 nicht neu gerechnet worden.

**Nicht ausgeführt.** In dieser Sitzung wurden nur `lauf.py`, `pfad.py`, `aufschlag.py`,
`vergleich_original.py` sowie `basis.py`, `pfad.py`, `final.py`, `aufschlag.py`, `altschuld.py`,
`tilgung.py` aus `rahmen/` ausgeführt. Alle übrigen Skripte wurden nur im Kopf gelesen, nicht gestartet.


**Hinweis v3.11 (Sekundärquelle, Vorchat):** `rahmen/altschuld.py` ist ein verworfener erster Versuch (Bemessung je Kopf, Klubschnitt). Maßgeblich ist `rahmen/aufschlag.py` (BIP-Bemessung). Nur zum Nachvollzug von Korrektur 44 behalten.
