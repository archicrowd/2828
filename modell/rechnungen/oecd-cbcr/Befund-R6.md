# R6 — Position 05 unter zwei Schlüsseln und über acht Jahre

**Stand:** 1. Oktober 2026 · **Quelle:** OECD, *Corporate Tax Statistics*,
`OECD.CTP.TPS:DSD_CBCR@DF_CBCRI` (1.1), Panel `_T`, Jahre 2016–2023 ·
**Skripte:** `r6_faktoren.py`, `r6_normiert.py`

---

## Kurzfassung

Drei Ergebnisse, und alle drei ändern etwas.

**Erstens: die Zahl aus v0.4 war zu hoch.** Position 05 bringt Deutschland im
Konzernsegment nicht +13 Mrd. €, sondern im Mittel von acht Jahren **+8 Mrd. €,
mit einer Spanne von +5 bis +14.** Das Jahr 2023 liegt am oberen Rand. Eine
einzelne Jahreszahl zu zitieren wäre Rosinenpflücken.

**Zweitens: der Schlüssel ist fast gleichgültig, das Jahr nicht.** Ob nach
Umsatz allein oder nach Umsatz, Beschäftigten und Sachanlagen zu je einem
Drittel verteilt wird, ändert Deutschlands Ergebnis um rund 2 Mrd. € — die
Streuung über die Jahre ist dreimal so groß. Die Richtung ist in jedem Jahr und
unter jedem Schlüssel dieselbe.

**Drittens, und das ist der unbequeme Teil: der reine Zielort-Schlüssel ist der
schwächere und der unfairere der beiden.** Er nimmt den Niedrigsteuerplätzen nur
etwa halb so viel ab wie der Dreifaktor-Schlüssel (−31 gegen −58 Mrd. € im
Median), und er verschiebt Aufkommen von den Produktionsländern zu den reichen
Absatzmärkten. Indonesien, Mexiko, Indien und Vietnam **verlieren** bei
Besteuerung am Kundenort und **gewinnen**, sobald Beschäftigte und Sachanlagen
mitzählen.

---

## 1 | Was genau gerechnet wurde

Zwei Schlüssel, die zwei verschiedene Reformen abbilden — nicht zwei Messungen
derselben Sache:

| | Schlüssel | entspricht |
|---|---|---|
| **Einfaktor** | Umsatz mit fremden Dritten | Besteuerung am Ort der Kundschaft = **Position 05** |
| **Dreifaktor** | Umsatz, Beschäftigte, Sachanlagen zu je ⅓ | formelhafte Aufteilung nach dem Muster der EU-Richtlinienentwürfe (CCCTB, BEFIT) |

Zusätzlich gerechnet: Zweifaktor (Umsatz und Beschäftigte je ½) und ein
umsatzlastiger Schlüssel (½ Umsatz, je ¼ Beschäftigte und Sachanlagen).

Je Sitzstaat wird der Gewinn aller dort ansässigen Konzerne nach dem jeweiligen
Schlüssel auf die Tätigkeitsländer verteilt. Jeder Konzern wird genau einmal von
seinem Sitzstaat gemeldet, Doppelzählung entsteht also nicht.

**Abdeckung der Faktoren 2023:** Beschäftigte in 93,2 % der Zellen,
Sachanlagen in 93,1 %. Fehlt ein Faktor, wird er für diese Zelle nicht
gewichtet und der Schlüssel auf 1 normiert.

**Fester Kreis.** Die Zahl der meldenden Sitzstaaten wächst von 26 (2016) auf
58 (2023); absolute Beträge sind über die Jahre deshalb nicht vergleichbar. Alle
Zeitvergleiche unten beruhen auf den **26 Sitzstaaten, die in allen acht Jahren
melden.** Das war nötig: im vollen Panel erscheint 2022 für Deutschland ein
Minus von 3,7 Mrd. €, im festen Kreis ist es ein Plus von 4,7. Das Minus war ein
Abdeckungsartefakt.

---

## 2 | Deutschland: die Mengenwirkung über acht Jahre

Fester Kreis, Mrd. € Steuer bei 28 %.

| Jahr | Einfaktor | Dreifaktor |
|---|---:|---:|
| 2016 | +4,8 | +5,4 |
| 2017 | +10,2 | +7,6 |
| 2018 | +14,1 | +11,8 |
| 2019 | +10,4 | +8,2 |
| 2020 | +5,5 | +4,0 |
| 2021 | +9,7 | +7,3 |
| 2022 | +4,7 | +3,2 |
| 2023 | +6,4 | +5,1 |
| **Median** | **+8,1** | **+6,3** |
| **Spanne** | **+4,7 … +14,1** | **+3,2 … +11,8** |

**Kein einziges negatives Jahr, unter keinem Schlüssel.** Das ist der robusteste
Teil des Befunds.

### Die Gesamtwirkung auf die deutsche Unternehmensseite

Mengenwirkung und Satzwirkung zusammen (Satzwirkung aus v0.4: −3,1 bis
−8,4 Mrd. €, weil 28 % unter dem heutigen deutschen Satz liegt):

| | Mrd. € |
|---|---:|
| Mengenwirkung, Median | +6,3 bis +8,1 |
| Satzwirkung | −3,1 bis −8,4 |
| **Mittlerer Fall** | **+2 bis +3** |
| **Ungünstigster Fall** | **−5** |
| **Günstigster Fall** | **+11** |

Das ist deutlich weniger als die +4,7 bis +10,0 Mrd. € aus v0.4, und es schließt
einen Verlust nicht aus. Der Grund ist allein die Normierung über acht Jahre;
v0.4 hatte das Spitzenjahr 2023 verwendet.

---

## 3 | Der Klub der zehn: null, zuverlässig

Fester Kreis, Summe der zehn, Mrd. € bei 28 %.

| | Median | Spanne |
|---|---:|---|
| Einfaktor | **+0,5** | −11,2 … +18,3 |
| Dreifaktor | **−7,3** | −11,7 … +15,1 |

Der Befund aus v0.4 hält und wird härter: **der gemeinsame Gewinn des Klubs ist
von Null nicht zu unterscheiden**, und unter dem Dreifaktor-Schlüssel ist er
negativ. Das Vorzeichen hängt am Schlüssel und am Jahr. Für den Entwurf heißt
das: der Klub ist kein Aufkommensargument. Er ist ein Rechtsdurchsetzungs- und
Rechtsfriedensargument. So sollte er auf der Seite auch stehen.

---

## 4 | Niedrigsteuerplätze: das stärkste Ergebnis im Datensatz

Fester Kreis, 22 Niedrigsteuerjurisdiktionen, Mrd. € bei 28 %.

| | Median | Spanne |
|---|---:|---|
| Einfaktor | −31,3 | −68,8 … −4,5 |
| **Dreifaktor** | **−57,9** | **−92,3 … −25,5** |

**In jedem der acht Jahre, unter jedem Schlüssel, verlieren die
Niedrigsteuerplätze.** Kein Vorzeichenwechsel, kein Ausreißer. Und der
Dreifaktor-Schlüssel ist etwa **doppelt so wirksam** — aus dem einfachen Grund,
dass Oasen kaum Beschäftigte und kaum Sachanlagen haben. Wer nach Umsatz
verteilt, lässt ihnen den Teil des Gewinns, der auf ihre eigenen Umsätze
entfällt; wer Beschäftigte und Anlagen mitzählt, lässt ihnen fast nichts.

---

## 5 | Produktionsländer: wer bei reiner Zielortsteuer verliert

Jahr 2023, Mrd. € Differenz, Übergang vom Einfaktor- zum Dreifaktor-Schlüssel.

| | Einfaktor | Dreifaktor | Wandel |
|---|---:|---:|---:|
| Indonesien | −37,3 | **+45,4** | +82,8 |
| Mexiko | −41,2 | **+16,7** | +57,9 |
| Indien | −35,8 | **+21,9** | +57,8 |
| Vietnam | −1,6 | **+36,1** | +37,7 |
| Saudi-Arabien | −82,7 | −45,7 | +36,9 |
| Brasilien | −31,1 | −0,5 | +30,6 |
| Philippinen | +1,2 | +15,1 | +13,9 |
| | | | |
| **USA** | **+475,8** | **+283,1** | **−192,7** |
| Singapur | −9,9 | −66,1 | −56,2 |
| Hongkong | −0,0 | −29,4 | −29,4 |
| China | +56,8 | +29,7 | −27,1 |
| Schweiz | −59,7 | −81,7 | −22,0 |

Vier Länder wechseln das Vorzeichen, alle vier sind Produktionsstandorte. Unter
Position 05 in der heutigen Fassung verlieren sie, obwohl dort gearbeitet und
produziert wird. Der größte Einzelgewinner des reinen Zielort-Schlüssels sind
die USA, und zwar mit +193 Mrd. € mehr als unter dem Dreifaktor-Schlüssel.

---

## 6 | Was daraus folgt

**Position 05 trifft eine Entwurfsentscheidung, die die Seite nicht benennt.**
Der reine Zielort-Schlüssel gibt rund die Hälfte der Wirkung gegen
Niedrigsteuerplätze auf und verschiebt Aufkommen von Produktions- zu
Absatzländern. Dafür bekommt er etwas Wichtiges: **er ist einseitig
durchsetzbar.** Wo die eigene Kundschaft sitzt, kann ein Staat selbst
feststellen; wie viele Beschäftigte und Sachanlagen ein Konzern in Vietnam hat,
nicht. Der Dreifaktor-Schlüssel braucht einen Verbund, Amtshilfe und ein
Schiedsverfahren — genau das, was es nicht gibt.

Das ist ein vertretbarer Tausch. Er muss aber dastehen, und zwar mit beiden
Seiten. Drei konkrete Änderungen:

1. **Die Zahl korrigieren.** Nicht +13, sondern **+5 bis +14 Mrd. €, Median
   +8** für die Mengenwirkung, und für die Unternehmensseite insgesamt ein
   mittlerer Fall von **+2 bis +3 Mrd. €** mit der Möglichkeit eines Verlusts.
2. **Den Tausch benennen.** Ein Satz bei Position 05: einseitig durchsetzbar,
   dafür schwächer gegen Oasen und zulasten der Produktionsländer.
3. **Den Klub umwidmen.** Kein Aufkommensargument, sondern Rechtsdurchsetzung.
   Dann ist die Null kein Einwand mehr, sondern erwartbar.

**Offen bleibt:** ob ein gemischter Schlüssel — etwa ½ Umsatz, je ¼
Beschäftigte und Sachanlagen — die Durchsetzbarkeit weitgehend erhält und
dennoch mehr gegen Oasen wirkt. Für 2023 liegt er bei −249 Mrd. € gegen
−161 (Einfaktor) und −279 (Dreifaktor), für Deutschland bei +44,5 gegen +46,9
und +43,8 Mrd. € Basis. Das sieht nach dem besseren Tausch aus und gehört
geprüft.

---

## 7 | Vorbehalte

- **Alle Konzerne eines Sitzstaats werden zu einer Einheit zusammengefasst.**
  Firmengenau wäre richtiger; dafür reicht die öffentliche Datenlage nicht
  (v0.3: nur rund 70 Konzern-Jahre mit lückenlosen Angaben).
- **Beschäftigte sind Köpfe, nicht Lohnsumme.** Die Richtlinienentwürfe nehmen
  für den Arbeitsfaktor halb Köpfe, halb Lohnsumme. Lohnsummen enthält der
  Datensatz nicht.
- **Der Drittumsatz wird dort gebucht, wo die verkaufende Einheit sitzt**, nicht
  zwingend dort, wo die Kundschaft sitzt.
- **Konzerninterne Beteiligungserträge** blähen den gemeldeten Gewinn auf;
  `PROFIT_ADJ` liegt nur für 2021 vor und ist in diesem Auszug leer.
- **Verluste sind in den Summen enthalten** (Panel `_T`). Für Effektivsätze ist
  das falsch, für Aufkommensrechnungen richtig.
- **Der feste Kreis umfasst 26 Sitzstaaten**, nicht die 58 von 2023. Die
  Zeitreihe ist damit konsistent, aber kleiner als das aktuelle Bild.
- Beträge in Euro, umgerechnet mit dem EZB-Durchschnittskurs 2026
  (0,8611 EUR/USD) — für Jahre vor 2026 ist das eine Vereinfachung.
