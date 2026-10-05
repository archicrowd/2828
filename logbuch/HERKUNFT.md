# Herkunft und Prüfstand der Logbuch-Dateien

Stand: 5. Oktober 2026

## Was diese Dateien sind

`Versionsgeschichte-TAX-2828.md` (Band I) und `Versionsgeschichte-TAX-2828-BandII.md`
(Band II) sind **Abschriften** der Dateien `claude/Versionsgeschichte-TAX-2828.md`
und `claude/Versionsgeschichte-TAX-2828-BandII.md` aus dem Claude-Projekt „2525"
(Stand im Projekt: Band I vom 3. Oktober 2026, Band II vom 4. Oktober 2026).
Die Texte wurden unverändert übernommen. Dieser Hinweis steht bewusst in einer
eigenen Datei, damit die Logbuch-Texte selbst unverändert bleiben.

Die Originale waren nicht als Datei übertragbar. Das Projekt lieferte sie nur
als Text, die Übernahme erfolgte durch erneutes Schreiben.

## Was geprüft ist und was nicht

Zur Prüfung lag eine hochgeladene ältere Fassung von Band I vor
(Modellstand v0.9, 1. Oktober 2026, 28.023 Byte, SHA-256
`1a6da02aaa39c1f648a15f7691bb5a1db5859ec8ade9924baa8b22c88985dca9`).

| Teil | Prüfung | Ergebnis |
|---|---|---|
| Band I, Abschnitte 1 und 2 | zeilenweiser Vergleich mit der hochgeladenen Fassung | identisch |
| Band I, Einträge v0.1 bis v0.9 | zeilenweiser Vergleich | identisch |
| Band I, Abschnitt 5 (Datenbestand) | zeilenweiser Vergleich | identisch |
| Band I, Korrekturen 1 bis 14 | Vergleich je Tabellenzeile | identisch |
| Band I, v0.10 bis v3.1, Korrekturen 15 bis 30 (zweite Tabellengruppe), Abschnitte 6 und 7 | **keine Vergleichsquelle** | ungeprüft |
| Band II vollständig | **keine Vergleichsquelle** | ungeprüft |

Die ungeprüften Teile sind die jüngeren. Wer sich auf eine Zahl daraus stützt,
vergleicht sie mit dem Original im Projektraum.

## Bekannte Unstimmigkeiten im Original (nicht korrigiert)

Diese stehen so im Projekt und wurden bewusst nicht verändert:

- Der Kopf von Band I nennt „Modellstand v1.0", der Inhalt reicht bis v3.1.
- Die Korrekturnummern 15 und 16 kommen doppelt vor (Tabelle in Abschnitt 4);
  die Reihenfolge 16, 15, 14, 13 ist ebenfalls so übernommen.
- Abschnitt 2 nennt als Beispiel für den Fußbereich noch „Modellstand v0.4".
- Die Verweise in Band II auf `claude/...` meinen die Projektpfade, nicht dieses Repository.

Eine Bereinigung gehört in einen eigenen, im Logbuch vermerkten Schritt
(Versionsschema: PATCH), nicht in die Abschrift.

## Prüfsummen (SHA-256) der Abschriften

```
b50bcc15623f2cfcb632da7191f3b7e161733b1b274ddd9d3109a9bc41372dda  Versionsgeschichte-TAX-2828.md
438a4cd8210f729b360d249d5e9e6aa1974c0fc43a7fbc5bc3954de89b5f22e1  Versionsgeschichte-TAX-2828-BandII.md
```
