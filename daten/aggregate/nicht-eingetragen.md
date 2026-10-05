# Nicht eingetragene Größen und offene Unstimmigkeiten

Stand: 5. Oktober 2026 · Modellstand v3.5

Diese Datei gehört zu `modell/parameter.toml`. Sie nennt, was **nicht** als
Parameter eingetragen wurde und warum. Alle Angaben beruhen auf dem Logbuch
(Band I bis v3.1, Band II bis v3.5) und sind nicht gegen Rohdaten geprüft.

## A. Nicht eingetragen, weil Bezugsjahr oder Einheit im Logbuch fehlt

| Größe | Logbuch-Wert | Was fehlt |
|---|---|---|
| Steuerquote | 30,6 % | Bezugsgröße und Jahr; „abgeleitet aus dem Pfad" |
| Mindestquote | 30,61 % (ohne Wachstum), 29,97 % (bei 1,0 %) | Bezugsjahr |
| Schuldenquote | 78,4 % | Bezugsjahr (Datenstand 2024 oder Startjahr des Pfads?) |
| Obergrenze von A | 36 % | Bezugsgröße (Schuldenstand? Einnahmen?). Korrektur 45 nennt „13,7 % an der Obergrenze von 36 %" |
| Höchstbedarf | 10,49 % im Jahr 2035 | Bezugsgröße |
| Verteidigungsziel | 2,5 % (NATO-Systematik) | Zieljahr |
| Dividende je Kopf | 550 → 512 (2035) → 707 € (2060) | Zeitbezug (Monat oder Jahr?), siehe B1 |
| Territorialer Aufschlag | +254 bis −728 € je Kopf | Zeitbezug und Preisbasis |

## B. Unstimmigkeiten im Logbuch, die bei der Nachrechnung auffielen

**B1. Die Dividendenreihe 550 → 512 → 707 € passt nicht zur Basis von 6.072 € je Kopf und Jahr.**
Nachrechnung mit den Werten des Logbuchs:

- 11,21 % von 13.803 Mrd EUR bei 255,1 Mio Personen = 6.066 EUR je Jahr = 505 EUR je Monat.
  Das stimmt mit den 6.072 EUR des Logbuchs überein (Abweichung 0,1 %).
- Die Reihe beginnt aber bei **550** (Preise 2028). Das sind rund 8,7 % mehr als 505 bis 506.
- Dasselbe Verhältnis zeigt sich bei der Aussage „ein Punkt des BIP sind 49 € Dividende im
  Monat": gerechnet ergeben 1 % von 13.803 Mrd EUR bei 255,1 Mio Personen **45,1** EUR im Monat.
  Beide Zahlen (550 und 49) passen zueinander, aber nicht zur Basis von 255,1 Mio.
- Rückgerechnet entspricht 49 EUR je Punkt und Monat einer Bezugsgröße von rund
  **235 Mio Personen** statt 255,1 Mio.

Mögliche Erklärungen, **keine davon belegt**: eine andere Bezugsgruppe (etwa nur
Anspruchsberechtigte), eine andere Bevölkerungszahl für 2028, oder ein anderer
Zeitbezug. Das Logbuch nennt dazu nichts. Solange das offen ist, werden die
Werte 550, 512 und 707 nicht als Parameter geführt.

**B2. Zwei Werte für die Dividende 2060.** Der Zeitpfad nennt 707 € (bei 1,0 % realem Wachstum),
der Punkt „Wachstumsannahme" nennt 712 € als Vergleichswert bei 1,0 %. Der Unterschied beträgt
0,7 %. Welcher Wert gilt, ist nicht bestimmt.

**B3. Das BIP von Deutschland 2028.** Band II nennt 4.914,9 Mrd EUR. Das Audit in Band I (v3.0)
nennt als „amtlich fortgeschrieben" 4.884 Mrd EUR, ohne Jahr. Ob beide dasselbe Jahr meinen,
ist nicht erkennbar. Der Wert 4.914,9 ist eingetragen, der Abgleich bleibt offen.

## C. Was die Nachrechnung bestätigt hat

- 12.157 × 1,13535 = 13.802 (Logbuch: 13.803). Rundungsdifferenz.
- 14.227 ÷ 12.157 = 1,17027 (Logbuch: 1,17024). Rundung des alten Werts 14.227.
- 6.072 EUR je Kopf und Jahr stimmen mit 11,21 % des BIP überein (siehe B1).

## D. Nächster Schritt

Die Punkte B1 bis B3 wären als offene Punkte im Logbuch zu führen. Ob eine davon
eine Korrektur ist (Nummer 47 ff.), lässt sich erst entscheiden, wenn die
Bezugsgröße der Dividendenreihe geklärt ist.
