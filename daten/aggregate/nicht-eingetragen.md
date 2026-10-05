# Nicht eingetragene Größen und offene Unstimmigkeiten

Stand: 5. Oktober 2026 · Modellstand v3.5

Diese Datei gehört zu `modell/parameter.toml`. Sie nennt, was **nicht** als
Parameter eingetragen wurde und warum, und welche Unstimmigkeiten bei der
Nachrechnung auffielen. Alle Angaben beruhen auf dem Logbuch (Band I bis v3.1,
Band II bis v3.5) und auf dem Gesamtkonzept im Chat „Steuerkonzept von 2525 auf
3030 umstellen". Nichts davon ist gegen Rohdaten oder Rechenskripte geprüft.

## A. Nicht eingetragen, weil Bezugsjahr, Einheit oder Bezugsgröße fehlt

| Größe | Wert | Was fehlt |
|---|---|---|
| Mindestquote | 30,61 % (ohne Wachstum), 29,97 % (bei 1,0 %) | Bezugsjahr; ist Teil der Herleitung von `steuerquote_klub` und dort im Hinweis genannt |
| Obergrenze von A | 36 % | **seit v3.7 als Parameter** `obergrenze_a_anteil_einzug` (Bezugsgröße: Einzug von A, 29,78 % des BIP; gegengerechnet gegen 11,5 % und 13,7 %) |
| Höchstbedarf | 10,49 % im Jahr 2035 | **geklärt in v3.7:** % des BIP, Ergebnis von `pfad.py`, kein Eingang. Entspricht 35,2 % des Einzugs |
| Territorialer Aufschlag | +254 bis −728 € je Kopf | **geklärt in v3.7:** EUR je Kopf und **Jahr**, nominal 2028 (aus der Rechnung abgeleitet), Ergebnis von `aufschlag.py` (+253 bis −726), kein Eingang |

## B. Unstimmigkeiten

**B1. Dividendenreihe 550 → 512 → 707 €: aufgelöst, aber im Logbuch unvollständig dokumentiert.**
Zuerst schien die Reihe nicht zur Basis von 6.072 € je Kopf und Jahr zu passen
(505 bis 506 € im Monat). Das Gesamtkonzept klärt es: Die Reihe gilt für
**Deutschland**, je Kopf und Monat, in Preisen von 2028. Der Klubschnitt steht in
der Zeitpfad-Tabelle (506 € in 2028, 472 € in 2035, 651 € in 2060). Deutschland
liegt wegen des höheren BIP je Kopf um 8,7 % darüber.

Nachrechnung: 506 × 1,087 = 550; 472 × 1,087 = 513; 651 × 1,087 = 707,6. Auch die
„49 € je BIP-Punkt und Monat" gelten für Deutschland (1 % von 4.914,9 Mrd € bei
rund 84 Mio Einwohnern). Der erste Verdacht, die Bezugsgröße sei 235 Mio Personen
statt 255,1 Mio, war damit ein Missverständnis des Logbuchs, kein Fehler im Modell.

Was bleibt: **Logbuch Band II (v3.5, Korrektur 43) nennt die Reihe ohne
Bezugsgruppe („Deutschland") und ohne Zeiteinheit („je Monat").** Wer nur das
Logbuch liest, kann sie nicht einordnen. Ob das eine Korrektur (Nummer 47) ist,
entscheidet der Verfasser.

**B2. Zwei Werte für Deutschland 2060 und 2035 im selben Dokument.**
Das Gesamtkonzept nennt im Seitentext und in Korrektur 43: **707 €** (2060) und
**512 €** (Tiefpunkt). Die Sensitivitätstabelle desselben Dokuments nennt im
Zentralfall (1,0 %): **712 €** (2060) und **513 €** (2035). Die Abweichung beträgt
0,7 % bzw. 1 €.

Welcher Wert aus dem Rechenskript stammt, ist nicht bestimmbar, weil `pfad.py`
nicht vorliegt. Nachrechnung stützt 707 (651 × 1,087 = 707,6); 712 würde einen
Klubwert von 655 statt 651 verlangen. Beide Werte stehen in `parameter.toml`
bzw. im Hinweis; als Parameter geführt ist 707.

**B3. BIP Deutschland.** Band II nennt 4.914,9 Mrd € (2028). Das Audit in Band I
(v3.0) nennt „amtlich fortgeschrieben 4.884 Mrd €", ohne Jahr. Ob beide dasselbe
Jahr meinen, ist nicht erkennbar. Eingetragen ist 4.914,9; der Abgleich bleibt offen.

**B4. Irland: BIP oder GNI\*?** Logbuch v0.2 nennt GNI\* als Bezugsgröße für Irland
(334,0 gegen 602,4 Mrd € BIP). Das Klub-BIP 2024 (12.157 Mrd €) stammt aus dem
Datensatz `nama_10_gdp`, der BIP führt. Ob Irland dort nach BIP oder GNI\* eingeht,
nennt das Logbuch nicht. Der Unterschied liegt bei 268 Mrd € (2,2 % des Klub-BIP,
bezogen auf die Zahlen aus v0.2). Ist das BIP verwendet, sind alle Quoten, die
das Klub-BIP als Nenner nutzen, für Irland anders gewichtet.

**Stand v3.7 (5. Oktober 2026): B2, B3, B5 geklärt, B4 und B6 präzisiert, siehe Logbuch
Band III, v3.7.** Die folgenden Absätze zu v3.6 sind der Zwischenstand und teils überholt:
B5 war kein Widerspruch (A-Summe 8,94 enthält Verteidigung 2,50), und die Erklärung zu B2
war unvollständig (nominales Wachstum ist in der Sensitivitätstabelle an das reale gekoppelt).

**Stand v3.6 (5. Oktober 2026), Nachtrag zu B2 und neue Punkte B5, B6.**

*B2.* Die Rekonstruktion `modell/pfad.py` erklärt beide Werte: 707 und 512 gehören zu
0,980 % realem Wachstum je Kopf (= 1,03 / 1,02 − 1), 712 und 513 zu 1,0 %. Hypothese,
am Original nicht geprüft. Die Entscheidung, welche Zahl gilt, liegt beim Verfasser.

*B5. Ebene A.* Band II (v3.2): 8,94 % des BIP. Zeitpfad-Tabelle 2028, „A gesamt": 9,04 %.
0,10 Punkte sind nicht erklärt.

*B6. Ausgangslage.* Schuldenquote 78,4 %, effektiver Zins 1,53 % und Verteidigung
1,401 % stammen aus 2024, stehen im Modell aber als Werte 2028. Sensitivität siehe
Logbuch Band III, v3.6.

Die „Mindestquote" (Abschnitt A) ist seit v3.6 reproduziert: kleinste Steuerquote, bei
der die Dividende je Kopf in jedem Jahr mindestens dem Versprechen (479 EUR für
Deutschland, 441 EUR im Klubschnitt) entspricht; maßgebend ist 2035. Die Bezugsgröße
ist damit geklärt (% des BIP). Als Parameter eingetragen wird sie nicht, weil sie
Ergebnis ist, kein Eingang.

## C. Was die Nachrechnung bestätigt hat

- 12.157 × 1,13535 = 13.802 (Logbuch: 13.803). Rundung.
- 14.227 ÷ 12.157 = 1,17027 (Logbuch: 1,17024). Rundung des alten Werts.
- 6.072 EUR je Kopf und Jahr entsprechen 11,21 % des BIP bei 255,1 Mio Personen
  (6.066 EUR) und 506 EUR je Monat.
- Deutschland liegt 8,7 % über dem Klubschnitt in allen drei Stützjahren.

## D. Nächster Schritt

Die Punkte B2 bis B4 wären als offene Punkte im Logbuch zu führen, B1 als
Dokumentationslücke. Ob eine davon eine Korrektur wird (Nummer 47 ff.), liegt beim
Verfasser. Für eine echte Prüfung von B2 fehlt das Rechenskript `pfad.py`.
