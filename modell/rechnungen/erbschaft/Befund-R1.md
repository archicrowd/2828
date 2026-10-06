# R1 — Position 03 auf der amtlichen Erbschaftsteuerstatistik gerechnet

**Stand:** 1. Oktober 2026 · **Quelle:** Statistisches Bundesamt, Erbschaft- und
Schenkungsteuerstatistik 2024, Statistischer Bericht 73611, Festsetzungsjahr
2024, Erstfestsetzungen · **Skript:** `r1_erbschaft.py`

---

## Kurzfassung

Position 03 ist damit die zweite Position mit einer belegten Zahl — und die
Rechnung fördert drei Dinge zutage, von denen zwei nicht auf der Seite stehen.

**Erstens, der Befund, der für sich spricht.** Wer 2024 zwischen 100.000 und
200.000 € erbte, zahlte darauf effektiv **13,5 %**. Wer zwischen 10 und 20
Millionen erbte, zahlte **9,6 %**. Der Grund steht in derselben Tabelle: in der
Millionenklasse werden **61,9 % des Erwerbs verschont**, in der kleinen Klasse
**11,2 %**.

**Zweitens, was das kostet.** Die Verschonung des Betriebsvermögens nach § 13a
nimmt **17,1 Mrd. €** aus der Bemessungsgrundlage — das sind **79,4 % des
gesamten übertragenen Betriebsvermögens** und mehr als die Hälfte aller Abzüge.
Je nach unterstelltem Satz entgehen dem Staat dadurch **3,9 bis 5,1 Mrd. € im
Jahr**, bei einem Gesamtaufkommen von 13,3 Mrd. Also **30 bis 39 % des
Aufkommens**.

**Drittens, der unerwartete Teil.** Position 03 brächte **16,5 bis 18,1 Mrd. €**
statt 13,3 — nur **+24 bis +36 %**. Das liegt nicht am Satz, sondern am
Freibetrag: ein einheitlicher Freibetrag von 400.000 € je Erwerb kostet
gegenüber den heutigen gestaffelten Freibeträgen rund **3,8 Mrd. € im Jahr** und
ist damit **die grösste einzelne Entwurfsentscheidung in Position 03 — grösser
als die Abschaffung der Betriebsvermögensverschonung.**

---

## 1 | Vom Erwerb zur Steuer, 2024

245.540 festgesetzte Erwerbe. Alle Beträge in Mrd. €.

| | |
|---|---:|
| **Wert der Erwerbe vor Abzug** | **113,216** |
| abzüglich Steuerbefreiungen § 13 (u. a. Familienheim, Hausrat) | −4,356 |
| **abzüglich Betriebsvermögen § 13a** | **−17,086** |
| abzüglich Mietwohngrundstücke § 13d | −1,651 |
| abzüglich DBA-Vermögen | −0,077 |
| abzüglich Zugewinnausgleich, Versorgungsfreibetrag, Auflagen, Erwerbsnebenkosten | −9,771 |
| **Wert der Erwerbe nach Abzug** | **80,275** |
| abzüglich persönliche Freibeträge § 16 | −33,754 |
| zuzüglich Vorerwerbe und übernommene Steuer | +18,201 |
| **Steuerpflichtiger Erwerb** | **64,721** |
| **Tatsächlich festgesetzte Steuer** | **13,285** |

Die Abzüge vor dem persönlichen Freibetrag summieren sich auf **32,941 Mrd. €
= 29,1 % des Erwerbswerts.** Mehr als die Hälfte davon, 51,9 %, ist die
Betriebsvermögensverschonung.

Effektiv zahlt die Erbschaftsteuer 2024 **11,7 % des Erwerbswerts** und 20,5 %
des steuerpflichtigen Erwerbs.

---

## 2 | Der effektive Satz fällt, wo er steigen müsste

Steuer geteilt durch den Wert des Erwerbs vor Abzug.

| Größenklasse | Fälle | Erwerbswert | verschont | effektiver Satz |
|---|---:|---:|---:|---:|
| 10.000 – 50.000 € | 53.203 | 1,61 Mrd | 6,4 % | 7,3 % |
| 50.000 – 100.000 € | 37.360 | 2,65 Mrd | 8,3 % | 12,4 % |
| **100.000 – 200.000 €** | 36.482 | 5,21 Mrd | 11,2 % | **13,5 %** |
| 200.000 – 300.000 € | 22.491 | 5,50 Mrd | 15,2 % | 10,4 % |
| 300.000 – 500.000 € | 33.930 | 13,46 Mrd | 18,9 % | 6,4 % |
| 500.000 – 2,5 Mio € | 47.694 | 42,86 Mrd | 29,7 % | 8,3 % |
| 2,5 – 5 Mio € | 2.920 | 9,91 Mrd | 38,4 % | 11,7 % |
| 5 – 10 Mio € | 1.176 | 8,03 Mrd | 49,0 % | 10,8 % |
| **10 – 20 Mio €** | 491 | 6,66 Mrd | **61,9 %** | **9,6 %** |
| **über 20 Mio €** | 272 | 17,35 Mrd | 23,4 % | **25,3 %** |
| **insgesamt** | **245.540** | **113,22 Mrd** | **29,1 %** | **11,7 %** |

Zwei Dinge sind daran bemerkenswert.

**Der Verschonungsanteil steigt monoton mit der Erwerbsgrösse** — von 6,4 % bei
kleinen Erbschaften auf 61,9 % in der Klasse 10 bis 20 Mio. Das ist kein
Nebeneffekt, sondern die Wirkungsweise des § 13a: begünstigt wird
Betriebsvermögen, und Betriebsvermögen liegt bei grossen Übertragungen.

**Oberhalb von 20 Mio bricht das Muster.** Der Verschonungsanteil fällt auf
23,4 %, der effektive Satz springt auf 25,3 %. Der Grund steht im Gesetz: die
Regelverschonung des § 13a gilt nur für begünstigtes Vermögen **bis 26 Mio €
je Erwerber**; darüber greift die Verschonungsbedarfsprüfung des § 28a. Die
Daten bilden diese Schwelle sichtbar ab.

Daraus folgt der Satz, der auf die Seite gehört:

> **Wer 150.000 € erbt, zahlt effektiv 13,5 %. Wer 15 Mio € erbt, zahlt 9,6 %.**
> Eigene Auswertung der amtlichen Erbschaftsteuerstatistik 2024.

---

## 3 | Was Position 03 brächte

Bemessungsgrundlage: Wert der Erwerbe vor Abzug, keine Verschonungen,
Freibetrag je Erwerb, Satz 28 %. Die Größenklassen sind nach genau dieser
Grösse gebildet, die Zuordnung ist also exakt; nur die Klasse 300.000 bis
500.000 € wird vom Freibetrag geschnitten und dort wird Gleichverteilung
unterstellt (beobachteter Klassenmittelwert 396.746 €, Gleichverteilung ergäbe
400.000 €).

| Variante | Basis | Steuer bei 28 % |
|---|---:|---:|
| **heute** (gestaffelte Freibeträge, Verschonungen, geltender Tarif) | 64,7 Mrd | **13,28 Mrd** |
| 400.000 € je Erwerb, keine Verschonungen, echte Kosten weiter abziehbar | 59,1 Mrd | **16,54 Mrd** |
| dasselbe ohne Abzug echter Kosten | 64,6 Mrd | 18,10 Mrd |
| heutige Freibeträge, keine Verschonungen | 72,6 Mrd | **20,33 Mrd** |
| dasselbe ohne Abzug echter Kosten | 79,5 Mrd | 22,25 Mrd |

**Mehraufkommen bei der Entwurfsfassung: +3,3 bis +4,8 Mrd. €, also +24 bis
+36 %.**

Bemerkenswert ist, dass die Bemessungsgrundlage mit **64,6 Mrd. € fast genauso
gross** ist wie heute (64,7 Mrd.) — nur völlig anders zusammengesetzt. Heute
entsteht sie, indem Betriebsvermögen verschont und kleine Freibeträge gewährt
werden; unter Position 03, indem alles besteuert und ein grosser Freibetrag
gewährt wird. Der Mehrertrag kommt allein aus dem Satz.

### Wer zahlt mehr, wer weniger

| Größenklasse | heute | Position 03 | Veränderung | Steuer je Fall heute |
|---|---:|---:|---:|---:|
| alle unter 300.000 € (159.057 Fälle) | 1,82 Mrd | 0 | **−1,82** | 11.433 € |
| 300.000 – 500.000 € | 0,87 Mrd | 0,22 Mrd | −0,65 | 25.501 € |
| 500.000 – 2,5 Mio € | 3,54 Mrd | 6,09 Mrd | **+2,55** | 74.202 € |
| 2,5 – 5 Mio € | 1,16 Mrd | 2,24 Mrd | +1,08 | 396.701 € |
| 5 – 10 Mio € | 0,87 Mrd | 1,93 Mrd | +1,06 | 739.367 € |
| 10 – 20 Mio € | 0,64 Mrd | 1,65 Mrd | +1,01 | 1.305.173 € |
| über 20 Mio € | 4,39 Mrd | 4,41 Mrd | +0,02 | 16.152.151 € |

**159.057 Erwerbe unter 300.000 € zahlen heute zusammen 1,82 Mrd. € und wären
vollständig frei.** Zwischen 500.000 € und 20 Mio. verdoppelt sich die Last
etwa. Oberhalb von 20 Mio. ändert sich fast nichts — dort greift die
Deckelung schon heute.

---

## 4 | Die Stellschraube ist der Freibetrag, nicht der Satz

Position 03 nennt „400.000 € je Kind". Die Rechnung oben wendet den Betrag auf
**jeden** Erwerb an. Heute sind die Freibeträge gestaffelt: 500.000 € für
Ehegatten, 400.000 € für Kinder, 200.000 € für Enkel, **20.000 € für alle
übrigen**.

Nach Tabelle 73611-06 sind Steuerklasse II und III — Geschwister, Nichten,
Neffen, Nichtverwandte — bei Erwerben von Todes wegen **76,7 % der Fälle,
42,3 % des steuerpflichtigen Erwerbs und 50,8 % der Steuer**. Ihr effektiver
Satz liegt bei 23,6 % (II) und 30,2 % (III) gegenüber 18,7 % in Steuerklasse I.

Ein einheitlicher Freibetrag von 400.000 € entlastet also genau die Gruppe, die
heute am härtesten besteuert wird — und er kostet **rund 3,8 Mrd. € im Jahr**,
mehr als die Abschaffung der Betriebsvermögensverschonung einbringt.

**Das ist eine Entwurfsentscheidung, keine Rechengrösse.** Sie gehört
ausdrücklich auf die Seite, in beiden Richtungen: entweder als bewusste
Gleichbehandlung aller Erbenden unabhängig vom Verwandtschaftsgrad — was zur
Logik von 28:28 passt — oder als Punkt, an dem nachgesteuert wird.

---

## 5 | Zeitreihe: kein Ausreisser, sondern ein Trend

| Jahr | steuerpflichtiger Erwerb | Steuer | effektiver Satz |
|---|---:|---:|---:|
| 2007 | 28,18 Mrd | 4,22 Mrd | 15,0 % |
| 2011 | 25,23 Mrd | 4,22 Mrd | 16,7 % |
| 2015 | 35,16 Mrd | 5,50 Mrd | 15,7 % |
| 2016 | 37,82 Mrd | 6,85 Mrd | 18,1 % |
| 2019 | 39,08 Mrd | 7,15 Mrd | 18,3 % |
| 2021 | 57,56 Mrd | 11,10 Mrd | 19,3 % |
| 2023 | 59,96 Mrd | 11,83 Mrd | 19,7 % |
| **2024** | **64,79 Mrd** | **13,30 Mrd** | **20,5 %** |

Das Aufkommen hat sich seit 2007 **verdreifacht**, der effektive Satz ist von
15,0 auf 20,5 % gestiegen. **2024 ist kein Ausreisser, sondern der aktuelle
Stand einer stetigen Entwicklung.** Der Sprung 2016 fällt mit der Neufassung
der Verschonungsregeln nach dem Urteil des Bundesverfassungsgerichts von 2014
zusammen.

Für den Entwurf heisst das: die Zahl ist belastbar und muss nicht über mehrere
Jahre geglättet werden — anders als bei Position 05.

---

## 6 | Vorbehalte

- **Die festgesetzte Steuer ist nicht die gezahlte.** Die Erläuterungen des
  Bundesamts halten ausdrücklich fest: *„In den Ergebnissen sind die
  Steuererlasse nach der Verschonungsbedarfsprüfung nach § 28a ErbStG nicht
  enthalten."* Die 13,285 Mrd. € sind also ein Bruttowert vor diesen Erlassen.
  Der Staat vereinnahmt weniger. **Das Mehraufkommen von +3,3 bis +4,8 Mrd. €
  ist damit eher zu niedrig als zu hoch angesetzt.** Die Höhe der Erlasse geht
  aus dieser Statistik nicht hervor und ist nachzutragen.
- **Nur festgesetzte Erwerbe.** Übertragungen unterhalb der Freibeträge
  erscheinen in der Statistik nicht. Das tatsächliche Erbvolumen in Deutschland
  ist ein Vielfaches der 113 Mrd. €; Schätzungen der Forschung liegen bei 300
  bis 400 Mrd. € im Jahr. Position 03 mit einem Freibetrag von 400.000 €
  erfasst davon nur den oberen Teil.
- **Der einheitliche Freibetrag** ist eine Setzung, siehe Abschnitt 4.
- **Keine Verhaltensreaktion gerechnet.** Bei Erbschaften ist sie kleiner als
  bei laufenden Steuern, aber nicht null: Wegzug, vorgezogene Schenkungen,
  Umschichtung in begünstigtes Vermögen. Die Abschaffung der Verschonung würde
  den letzten Kanal schliessen, die ersten beiden nicht.
- **Die Klasse 300.000 bis 500.000 €** wird vom Freibetrag geschnitten; dort ist
  Gleichverteilung unterstellt. Der Fehler ist klein (die Klasse trägt 0,22 von
  16,54 Mrd.).
- **Der Satz, zu dem die Verschonung gegengerechnet wird**, ist nicht beobachtet,
  sondern aus dem geltenden Tarif der Steuerklasse I abgeleitet. Deshalb die
  Spanne 3,9 bis 5,1 Mrd. und nicht ein Punktwert.
- **Stundung.** Position 03 sieht vor, dass Betriebe die Steuer stunden können.
  Das ist in dieser Rechnung nicht abgebildet; es verschiebt das Aufkommen
  zeitlich, ohne es der Höhe nach zu ändern — sofern die Stundung verzinst wird.

---

## 7 | Was auf die Seite gehört

1. **Position 03 wechselt von „offen" auf „belegt".**
2. Die Zahl: **+3,3 bis +4,8 Mrd. €**, mit dem Hinweis, dass die Spanne
   wesentlich vom Freibetrag abhängt.
3. Der Satz für die Kampagne: **13,5 % bei 150.000 €, 9,6 % bei 15 Mio €.**
4. Ein Satz zur Freibetragsentscheidung — dass alle Erbenden gleich behandelt
   werden, unabhängig vom Verwandtschaftsgrad, und was das kostet.
