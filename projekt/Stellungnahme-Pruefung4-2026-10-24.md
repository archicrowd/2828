# Stellungnahme zur dritten Prüfung (Modellstand v4.42, 24.10.2026)

Initiative 28:28 · 24. Oktober 2026 · Logbuch v4.46 · Antwort auf Issue #2 („Prüfbericht vom 24.10.26“), Prüfer: Kulturverein Ribbeck e.V.

Vielen Dank für die Prüfung nach unseren eigenen Prüffragen und die Lieferung in maschinenlesbarer Form. Die Beilagen (`befunde.csv`,
`grenzbelastung.csv`, `fondsstress.csv`, Stellungnahme) liegen unter `beitraege/kvribbeck-2028/pruefung3/`. Jeden Befund haben wir gegen
Rechnung und Dateien geprüft; Ergebnis und Umsetzung stehen hier. Vier Befunde treffen und werden als Korrekturen geführt (73 bis 75), dazu
eine eigene (76), die beim Nachsehen auffiel.

## 1 | Befunde B17 bis B24

| Befund | Prüfung | Umsetzung (v4.46) |
|---|---|---|
| **B17** Gesamtlast ohne Fonds: drei Werte | **trifft.** `gesamtlast33.json` wies „Steuern 33,53“ aus, die Summe 45,47 stammte aber aus dem Steuerbedarf 33,42 (`systemvarianten.json`); `KENNZAHLEN.md` nannte 45,46/49,56 | **Korrektur 73:** Summe aus den ausgewiesenen Teilen: 33,53 + 12,05 = **45,58**, mit Pflichtvorsorge **49,68**; der Wert mit Steuerbedarf (45,47/49,57) steht daneben als Variantenvergleich |
| **B18** Z 2028: 9,45 gegen 9,42 | **trifft.** Mit dem Kürzungssatz je Staat (v4.37) sank Z auf 9,42; Kennzahl und Prüfmappe wurden nicht nachgezogen | **Korrektur 74:** 9,42 % BIP in `KENNZAHLEN.md` und Mappe |
| **B19** `deckung_quote.csv` unmarkiert | trifft (Hinweis) | Abschnitt „Archivierte Dateien“ in `KENNZAHLEN.md`: Stand B, bleibt als Regressionsprüfung in der Kette, gilt nicht |
| **B20** Hinweistext „Klub der zehn“ | trifft (Hinweis) | Text in `gesamtlast33.json` auf den Fonds der 30 berichtigt |
| **B21** Fondssensitivität ohne Wachstum | **trifft, gerechnet.** | `fondszins.json → zins_wachstum`: Zins 2,45 / 3,0 / 3,5 / 4,0 % × Wachstum 3,0 / 2,5 / 2,0 %. Bei 2,45 % Zins und 2,0 % Wachstum Beitrag 6,22 statt 5,17 % BIP (+1,05), Zuschlag 18,6 statt 15,5 % (+3,1); bei festem Beitrag Restschuld 2098 rund 87 % BIP (zehn), Spitze 191 % im Jahr 2064 statt 150 % im Jahr 2056. Ihre Näherung (+0,9 / +2,6; Restschuld ~90) bestätigt sich in der Richtung; mit unserer Z-Reihe fällt der Mehrbedarf etwas größer aus, die Verschiebung der Spitze kleiner (8 statt ~15 Jahre). Annahme: Z in % des BIP unabhängig vom Wachstum (Renten mit den Löhnen fortgeschrieben) |
| **B22** Erbschaft 4,3 × Ist | teilweise. Die Basis ist seit v4.32 gegen Daten gestellt (`vermoegensbasis33.json`): nötig 173 Mrd. € Erwerbe über 100.000 € (2028) gegen 150,5 Mrd. € steuerpflichtigen Erwerb 2025 (Destatis, fortgeschrieben 164 Mrd. €). Ihr Vergleich mit 113 Mrd. € (2024) unterschätzt die Datenlage 2025 (Rekordjahr, +32,9 %). Nicht benannt waren Satz, Basis und Schenkungs-Parität | Definitionstabelle in `KENNZAHLEN.md`; Schenkungs-Parität und reale Übertragungen als Obergrenze als offener Punkt (R4) |
| **B23** Unternehmensposition ohne Definition | **trifft.** Die Position stammt aus dem nationalen Modell (Stand A: 145 Mrd. € bei 25 %, implizite Basis rund 580 Mrd. €), deren Basis nirgends belegt ist | Definitionstabelle mit Status „Basis nicht belegt“; Definition (Gewinnbegriff, Kundenort, Plattformen, ersetzte Steuern) und Beleg der Basis als offener Punkt (R4) – für die Deckung die größte unbelegte Position |
| **B24** Zinsband 590/570/548 gegen 604/583/562 € | **Unschärfe der Mappe, kein Rechenfehler.** Seit v4.38 trägt Deutschland 2028 den Zuschlag nach Verrechnung: 15,0 / 16,5 / 18,1 / 19,7 % statt 15,5 / 17,1 / 18,7 / 20,4 %. Unsere Bandwerte gelten für diese Sätze; Ihre Werte für die gemeinsamen Sätze. Die Mappe stellte die gemeinsamen Sätze neben die deutschen Haushaltswerte | **Korrektur 75:** beide Sätze in Mappe und `KENNZAHLEN.md` benannt |

**Korrektur 76 (eigene):** `DATENZUGANG.md` und die Prüfmappe nannten das Repository „privat“; GitHub weist es am 24.10.2026 als öffentlich aus.
Text berichtigt. Ob es öffentlich bleiben soll, entscheidet die Initiative.

## 2 | Zu den Antworten auf die Prüffragen und zur Plausibilitätsprüfung

- **Frage 1 (Weitergabe):** Wir übernehmen Benzarti u. a. (JPE 2020) als Primärquelle der Asymmetrie und geben der Rückfallregel in der Mappe
  einen eigenen Abschnitt (offen, nächste Fassung der Mappe). Ihr Urteil „als Setzung unplausibel, als Gesetz mit Rückfallregel plausibel“
  entspricht der Konstruktion.
- **Frage 2 (Aufkommen):** Die Eichung der Einkommensposition gegen die Lohn- und Einkommensteuerstatistik nehmen wir als offenen Punkt auf (R4).
- **Frage 3:** Band für die Skalierung 10 → 30 bleibt offen (R6); jetzt mit Wachstumsdimension (B21).
- **M1 Grenzbelastung:** Ihr Befund, dass der Spitzen-Grenzsatz einschließlich Zuschlag (~50 %) zunächst über dem heutigen (44,3 %) liegt, ist
  für die Darstellung wichtig; er gehört in Konzept und Seite (offen).
- **M3/M4:** Oberes Ausweichband bei Vermögen, Exit-Regeln und Register sowie ein handelsrechtliches Gutachten (WTO, Finanzsektor) führen wir unter
  P1 und R4.

## 3 | Was sich an den Zahlen bewegt

Keine geltende Haushalts- oder Fondszahl. Neu ausgewiesen: Gesamtlast ohne Fonds 45,58 / 49,68 % BIP (statt 45,46 / 49,56), Z 2028 9,42 % BIP,
das Raster Zins × Wachstum. Alle 64 Rechenstufen ohne Fehler.
