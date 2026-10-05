# Herkunft und Prüfstand der Logbuch-Dateien

Stand: 5. Oktober 2026

## Was diese Dateien sind

**Stand v3.8 (5. Oktober 2026).**

- `Versionsgeschichte-TAX-2828.md` (Band I) ist seit v3.8 die **Originaldatei** aus dem Export des
  Vorchats (`doku/Versionsgeschichte.md`, 1.070 Zeilen, v0.1 bis v3.4, Korrekturen 1 bis 41),
  byteweise kopiert. Davor lag eine Abschrift bis v3.1 vor (Commit `a5808b1`, von Hand neu
  geschrieben).
- `Versionsgeschichte-TAX-2828-BandII.md` (Band II) ist die Abschrift der Projektdatei
  `claude/Versionsgeschichte-TAX-2828-BandII.md` (Stand 4. Oktober 2026) und mit dem Original
  im Export **zeilengleich**. Seit v3.8 steht unter der Überschrift „Vorbemerkung zur Lücke" ein
  gekennzeichneter Berichtigungshinweis (einzige Änderung gegenüber dem Original).
- `Versionsgeschichte-TAX-2828-BandIII.md` entsteht direkt in diesem Repository.

Die Dateien im Claude-Projekt „2525" wurden in dieser Sitzung **nicht verändert**. Dort steht
Band II weiter mit der falschen Vorbemerkung (Korrektur 47).

## Was geprüft ist und was nicht

| Teil | Prüfung | Ergebnis |
|---|---|---|
| Band I vollständig | Kopie des Originals aus dem Export; zusätzlich zeilenweiser Vergleich der früheren Abschrift (bis v3.1) mit dem Original | Abschrift bis auf einen Zeilenumbruch (Zeilen 664/665) identisch; v3.2 bis v3.4 und Korrekturen 31 bis 41 fehlten |
| Band I gegen die ältere Datei v0.9 (28.023 Byte, SHA-256 `1a6da02a…dca9`) | zeilenweiser Vergleich, frühere Sitzung | Abschnitte 1, 2, 5, v0.1 bis v0.9, Korrekturen 1 bis 14 identisch |
| Band II | `diff` gegen Original im Export | identisch |
| Inhalt der Einträge | nicht geprüft | Die Logbuchtexte sind Aussagen des Verfassers; nachgerechnet sind nur die Zahlen aus v3.5 (Band III) |

**Grenze der Prüfung.** Der Vergleich zeigt, dass die Texte übereinstimmen, nicht dass die
Inhalte stimmen. Der Export ist keine unabhängige Quelle, sondern das Material desselben Vorchats.

## Bekannte Unstimmigkeiten im Original (nicht korrigiert)

Diese stehen so im Original und wurden bewusst nicht verändert:

- Der Kopf von Band I nennt „Modellstand v1.0", der Inhalt reicht bis v3.4.
- Die Korrekturnummern 15 und 16 kommen doppelt vor (Tabelle in Abschnitt 4);
  die Reihenfolge 16, 15, 14, 13 ist ebenfalls so übernommen.
- Abschnitt 2 nennt als Beispiel für den Fußbereich noch „Modellstand v0.4".
- Die Verweise in Band II auf `claude/...` meinen die Projektpfade, nicht dieses Repository.
- Band II, „Vorbemerkung zur Lücke" und „Rekonstruktion v3.2 bis v3.4": falsch, siehe
  Korrekturen 47 und 48 in Band III.

Eine Bereinigung der übrigen Punkte gehört in einen eigenen, im Logbuch vermerkten Schritt
(Versionsschema: PATCH).

## Prüfsummen (SHA-256)

```
22f51b0a45066340b147620c38d1853fa0bb68088ed44b0a79f12962321b764b  Versionsgeschichte-TAX-2828.md
533acd5c96c31b8d33f148eca3b75ea8a87200d971ce03cb302005e20fa5b336  Versionsgeschichte-TAX-2828-BandII.md   (mit Berichtigungshinweis, v3.8)
438a4cd8210f729b360d249d5e9e6aa1974c0fc43a7fbc5bc3954de89b5f22e1  Versionsgeschichte-TAX-2828-BandII.md   (Original, ohne Hinweis)
```
