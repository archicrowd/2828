# modell/rechnungen/ — Einzelrechnungen (Stand A)

Herkunft: Ausgabeordner des Vorchats. Bezeichnungen R1 bis R16 wie im Logbuch (Band I).
Gerechnet auf dem nationalen Stand A; nach dem Rahmenwechsel (v3.1 ff.) nicht neu gerechnet.
Es wurde keines dieser Skripte in dieser Sitzung ausgeführt.

| Ordner | Rechnung |
|---|---|
| `erbschaft/` | R1 bis R1d: Position 03, Freibetrag, Stundung, Zinsleiter |
| `immo/` | R11 bis R16: Position 04b, Veräußerungsgewinne, Freibetrag, Grundsteuerabzug |
| `vermoegen/` | R5a, R5b: Vermögensteuer, Bodenwertabgabe |
| `klima/` | R4, R4b: CO₂-Preis auf Rechtsgrundlage, klimaschädliche Subventionen |
| `haushalt/` | R9, R10: Haushaltspfad, Tarifstufen, Nettoposition, Schlussabgleich |
| `oecd-cbcr/` | R6: OECD Country-by-Country Reporting, Tabelle I (Position 05) |
| `cbcr-auswertung/` | erste Datenprüfung zu Position 05 |
| `pfad/`, `rahmen/`, `zins/` | frühe Skripte für Zeitpfad, Rahmen und Schuldenquote (Stand B im Entstehen) |

**Panel-Falle (OECD).** Für Aufkommensrechnungen nur Panel `_T`, nicht `PANELAI`
(`CLAUDE.md`). `oecd-cbcr/t1-panelAI.csv` enthält die Auswertung nach `PANELAI`; sie ist nur für den
internationalen Satzvergleich zulässig. Das Skript `wirkung_28.py` begründet das im Kopf.

**Rohdaten.** Die OECD-Rohdateien (167 und 69 MB) sind nicht im Repository. Die Skripte erwarten sie
lokal in `daten/roh/` (`.gitignore`); die Pfade in den Skripten können vom Original abweichen und
wurden nicht angepasst.

**Nicht eingecheckt.** Die Rechercheliste der Institute (`recherche/`) enthält persönliche
E-Mail-Adressen externer Forschender und bleibt aus dem Repository heraus.
