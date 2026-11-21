# Baranteil ein Drittel des Grundbedarfs: Finanzierung ohne höhere Bodenabgabe

Initiative 28:28 · 21. November 2026 · Modellstand v4.106 (Prüfrechnung; die geltenden Zahlen bleiben unverändert)
Rechnung: `modell/anteil_drittel.py` (+ `.toml`) → `daten/aggregate/anteil_drittel.json`; Grundlage `modell_e.py`, `co2_boden_haushalte.json`, `vermoegensbasis33`.
Euro je Monat, Kaufkraft 2026, Deutschland; Anteile in % BIP.

**Vorgaben der Initiative (21.11.2026):**
- Fester Baranteil ein Drittel des Grundbedarfs (33,33 % statt 30 %). Das ist kommunikativ stimmig mit dem Goldenen Drittel.
- Keine Erhöhung der Bodenabgabe über 2 % hinaus.
- Mehrbedarf und Zinsregel über eine gleichmäßige Belastung aller Einkommensarten außer Arbeit. Die Vermögensteuer wird geprüft.
- Der Übergang wird über den Fonds finanziert.
- Sonst gelten die Empfehlungen aus v4.105: Umlageverbot, Stundung ab 65, Altersausgleich R4.

## 1 Ergebnis in Kürze

- **Das Dividendenpaket 2028** bei einem Drittel:
  - Gesamtwert 769 € je Erwachsenem: 325 € bar, 444 € Netz.
  - Gesamtwert 704 € je Kind: 260 € bar.
  - Bei 30 % wären es 293 / 235 € bar.
- **Der Mehrbedarf gegen 30 %** beträgt rund 0,46 % BIP im Jahr. Zwei Wege tragen ihn, auch eine Mischung:

| Weg | Satz Nicht-Arbeit | Vermögensteuer | BIP 2045 gegen statisch | Rücklage niedrigster Stand |
|---|---|---|---|---|
| **V1** nur Einkommensarten außer Arbeit | **44 %** (statt 38 %) | wie heute im Drittel: 1,5 % ab 2 Mio. € | +5,8 % (statt +6,4 %) | +0,37 % BIP |
| **V2** Mischung | 40 % (nach DIW 39 %) | 1,5 % ab 1 Mio. € | +6,2 % | +0,04 % BIP (knapp) |
| **V3** nur Vermögensteuer | 38 % | 2 % ab 1 Mio. € | +6,4 % | +0,7 % BIP |

- **Übergang über den Fonds:** Die Bodenabgabe steigt in drei Schritten bis 2030. Der Fonds deckt den Fehlbetrag (1,17 % BIP zusammen) und erhält ihn 2031 bis 2045 mit 0,09 % BIP im Jahr zurück, verzinst mit 2,45 %.
- **Der Zinsfall (Fonds 3,0 %)** lässt sich über Nicht-Arbeit allein nicht auffangen. Auch bei 48 % sind nur 31 % des Grundbedarfs tragbar. Mit einer Vermögensteuer von 2 % ab 1 Mio. € reichen 42 %.
- **Empfehlung:** V2 als Grundlage. Die Zinsregel hebt dann den Satz für Nicht-Arbeit in einer Spanne von 40 bis 44 % an. Die Vermögensteuer bleibt beim Satz, solange das Bundesverfassungsgericht keine engeren Grenzen setzt (Abschnitt 4).

## 2 Einheitlicher Satz auf alle Einkommensarten außer Arbeit

Der Satz gilt für Kapitalerträge, Unternehmensgewinne mit Plattformen und Erbschaften. Arbeit bleibt bei ein Drittel.

| Satz | 38 % | 40 % | 42 % | 44 % | 46 % | 48 % |
|---|---|---|---|---|---|---|
| Mehraufkommen gegen 38 %, % BIP | 0 | +0,17 | +0,32 | +0,46 | +0,60 | +0,72 |
| BIP-Niveau gegen 38 %, % (Investitionskanal) | 0 | −0,2 | −0,4 | −0,6 | −0,8 | −1,0 |

**Lesart:**
- Jeder Punkt bringt etwa 0,08 % BIP, mit abnehmendem Ertrag wegen Ausweichen (Elastizitäten aus `quote_optimum`, Annahmen).
- Jeder Punkt kostet etwa 0,1 % BIP Wachstum über den Investitionskanal (`stellschrauben.toml`, linear fortgeschrieben, Annahme).
- Bei 44 % fehlen 2045 gut 0,6 % BIP. Der Investitionskanal wirkt dann mit −1,5 statt −0,95 %.
- **Mieteinkünfte** stehen im Modell in der Position Einkommen und unterliegen dem Stufentarif. Sie sind deshalb hier nicht erhöht.
  - Eine gleichmäßige Belastung aller Einkommensarten außer Arbeit müsste sie einbeziehen. Das ist rechnerisch noch offen (R29).
  - Die Bodenabgabe belastet die Vermietung bereits (15,9 Mrd. € bei Vermietern in der Mikrosimulation, v4.105).

## 3 Übergang über den Fonds

| | bis 2030 (empfohlen) | bis 2032 |
|---|---|---|
| Fehlbetrag zusammen | 1,17 % BIP | 2,42 % BIP |
| Rückzahlung je Jahr, 15 Jahre | 0,09 % BIP (2031–2045) | 0,20 % BIP (2033–2047) |
| nötiger Satz Nicht-Arbeit (V1) | 44 % | 43 % |
| Rücklage niedrigster Stand | +0,37 % BIP | −0,78 % BIP |

- **Der Fondskredit ist vorsichtig gerechnet:** in % BIP, ohne die Entlastung durch das Wachstum. Bei 3 % nominalem Wachstum und 2,45 % Zins sinkt die Last real.
- **Warum der längere Übergang einen Punkt weniger braucht, aber die Rücklage negativ wird:** Die Fortschrittsregel hebt den Anteil 2035 auf 34,3 %, weil die Rücklage dann über dem Ziel liegt. Danach reicht sie nicht mehr.
  - Daraus folgt eine Regel: Der Anteil steigt nur, wenn die Vorschau über zehn Jahre die Rücklage nicht unter null führt (R30).

## 4 Vermögensteuer

**Heute im Modell:** 1,5 % des Nettovermögens über 2 Mio. € je Haushalt, mit 50 % Ausweichen (Annahme). Die Position beträgt 0,97 % BIP.

| Variante | betroffene Haushalte | Mehraufkommen gegen heute, % BIP | nötiger Satz Nicht-Arbeit für ein Drittel |
|---|---|---|---|
| 2 % ab 2 Mio. € | 0,7–1,1 Mio. | +0,13 bis +0,34 | 42 % (PHF) / 39 % (DIW) |
| 1,5 % ab 1 Mio. € | 2,4–2,8 Mio. | +0,24 bis +0,32 | 40 % / 39 % |
| 2 % ab 1 Mio. € | 2,4–2,8 Mio. | +0,46 bis +0,77 | 38 % / 38 % |

**Spannen:**
- Der untere Wert folgt der Vermögensbefragung der Bundesbank (PHF 2021). Sie erfasst die Spitze unvollständig.
- Der obere Wert folgt der DIW-Schätzung mit Millionärsstichprobe (2020). Das ist eine Studie.
- Schon die heutige Position des Modells (0,97 % BIP) beruht auf der DIW-Spitze. Nach der Befragung allein läge sie bei 0,40 % BIP (v4.32). Das Risiko liegt also auch im Bestand.

**Was gegen eine starke Vermögensteuer spricht oder offen ist:**
- **Recht:** Die Vermögensteuer wird seit 1997 nicht erhoben. Das Bundesverfassungsgericht verlangte 1995 eine gleichmäßige Bewertung aller Vermögensarten (BVerfG, 2 BvL 37/91). Eine Neuregelung braucht eine einheitliche, marktnahe Bewertung. Die Grundsteuerwerte und die digitale Bodenbewertung helfen dabei.
- **Ausweichen:** Die 50 % sind eine Annahme. Studien zu Dänemark und der Schweiz zeigen deutliche Reaktionen der Vermögensangaben (Jakobsen u. a. 2020; Brülhart u. a. 2022). Die Höhe ist für Deutschland nicht belegt.
- **Wachstum:** Im Modell kostet die Vermögensteuer kein Wachstum (Ansatz 0). Die OECD (2018) sieht Nettovermögensteuern als weniger effizient als Kapitalertrags- und Erbschaftsteuern. Der Vorteil von V3 beim Wachstum ist deshalb überzeichnet.
- **Doppelbelastung des Bodens:** Ab 1 Mio. € fallen viele Eigentümer zugleich unter Bodenabgabe und Vermögensteuer.
  - Vorschlag: Die Bodenabgabe auf selbst genutzten Boden wird auf die Vermögensteuer angerechnet. Dann sinkt das Mehraufkommen. Die Höhe ist noch nicht gerechnet (R29).
- **Verwaltung:** Eine niedrigere Schwelle vervielfacht die Zahl der Fälle (0,7 auf 2,4 Mio. Haushalte). Das passt nur zum Ziel der Vereinfachung, wenn die Bewertung automatisch aus Registern kommt.

## 5 Zinsregel

| Fondszins 3,0 % statt 2,45 % | tragbarer Anteil |
|---|---|
| nur Nicht-Arbeit, bis 48 % | 31,0 % (ein Drittel nicht erreichbar) |
| Nicht-Arbeit 42 % und Vermögensteuer 2 % ab 1 Mio. € (DIW) | 33,6 % |

**Vorschlag:**
- Liegt der Fondszins drei Jahre über dem nominalen Wachstum, steigt der Satz für Nicht-Arbeit um einen Punkt je Jahr, höchstens auf 44 %.
- Reicht das nicht, wird die Tilgung des Fonds gestreckt, statt den Anteil zu senken.
- Arbeit, Label und Boden bleiben unverändert.

## 6 Empfehlung

1. **Baranteil ein Drittel des Grundbedarfs** (325 € bar je Erwachsenem und 260 € je Kind 2028; Gesamtwert 769 / 704 €). Er sinkt nie und steigt mit der Fortschrittsregel bis zur Hälfte.
2. **Bodenabgabe 2 %** in drei Schritten bis 2030. Der Fonds überbrückt (1,17 % BIP, Rückzahlung 2031–2045). Es gelten Umlageverbot, Stundung ab 65 und Altersausgleich R4.
3. **V2:** Nicht-Arbeit 40 % (die Rücklage bleibt nur knapp positiv; 41 % gibt Reserve), Vermögensteuer 1,5 % ab 1 Mio. € je Haushalt mit Anrechnung der Bodenabgabe. Bleibt die Vermögensteuer rechtlich oder im Aufkommen hinter der Annahme zurück, gilt V1 (44 %).
4. **Zinsregel** in der Spanne 40 bis 44 %, danach Streckung des Fonds.
5. **Fortschrittsregel mit Vorschau:** Der Anteil steigt nur, wenn die Rücklage in der Zehnjahresvorschau nicht unter null fällt. Über 4 % BIP steigt er schneller, über 6 % BIP geht der Rest an den Fonds.

**Gesamtlast:**
- Modell E nach Korrektur 97: rund 42,8 % BIP mit Vorsorge.
- Mit einem Drittel: rund 43,2 bis 43,5 % BIP (geltend 40,6).

## 7 Grenzen

- **Haushaltswerte:**
  - Die Mikrosimulation enthält den höheren Satz auf Kapitaleinkommen der Haushalte nicht, ebenso wenig die Vermögensteuer.
  - Beide treffen vor allem das oberste Dezil. Dessen Ergebnis (−425 € in v4.105) wird dadurch negativer.
- **Wachstumswirkungen:** Annahmen der Belegstufe B/C. Vermögensteuer mit Wachstumswirkung 0.
- **Vermögensverteilung:** Pareto über P90; Haushalt als Einheit der Schwelle; Fortschreibung 3 % je Jahr. Alles Annahmen.

## Quellen

- Deutsche Bundesbank: Private Haushalte und ihre Finanzen (PHF 2021), Pressepräsentation April 2023. Amtliche Befragung, Spitze untererfasst.
- DIW Berlin: Wochenbericht 29/2020 (SOEP mit Millionärsstichprobe). Eine Studie.
- Bundesverfassungsgericht, Beschluss vom 22. Juni 1995, 2 BvL 37/91 (Vermögensteuer).
- OECD (2018): The Role and Design of Net Wealth Taxes in the OECD. OECD Tax Policy Studies No. 26.
- Jakobsen, K., Jakobsen, K., Kleven, H., Zucman, G. (2020): Wealth Taxation and Wealth Accumulation: Theory and Evidence from Denmark. Quarterly Journal of Economics 135(1).
- Brülhart, M., Gruber, J., Krapf, M., Schmidheiny, K. (2022): Behavioral Responses to Wealth Taxes: Evidence from Switzerland. American Economic Journal: Economic Policy 14(4).
- Die Literatur zu Recht, OECD und Ausweichen ist in dieser Version nicht erneut an der Quelle geprüft.
- Rechnungen des Projekts: `anteil_drittel.json`, `modell_e.json`, `co2_boden_haushalte.json`, `vermoegensbasis33.json`, `stellschrauben.json`.
