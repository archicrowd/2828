# Systemvarianten: Viertellösung 25:25 und Drittellösung 33:33 gegen 28:28 (Stand v3.43, 17. Oktober 2026)

**Status: Prüfrechnung. Die Gesamtrechnung bleibt bei 28:28; entscheidet die Initiative.** Rechnung `modell/systemvarianten.py` (+ `.toml`),
Ergebnis `daten/aggregate/systemvarianten.json`. Grundlage: Gesamtrechnung v3.42, Sozialschutz-Rechnung v3.42 (Schätzung des Zugesagten Z),
deutsche Basis für die Deckung. Prozent des BIP, Durchschnitt der zehn Staaten; Euro je Erwachsenem und Monat, Deutschland, Preise 2028.

## 1 | Die beiden Wege, wie gerechnet

| | 28:28 (geltend) | 25:25 Viertellösung | 33:33 Drittellösung |
|---|---|---|---|
| Spitzensatz Einkommen, Kapital, Unternehmen, Erbschaft, Label | 28 % | 25 % | 33 % |
| Einkommensteuer-Stufen (1 / 1,5 / 2 / 3-facher Grundbedarf) | 0/9/16/21/28 | 0/8/14/19/25 | 0/11/19/25/33 |
| Mehrwertsteuer-Label A+ bis D | 5/11/17/22/28 | 4/10/15/20/25 | 6/13/20/26/33 |
| Effektiver Mehrwertsteuersatz | 16,9 % | 15,1 % | 20,0 % |
| Mindestniveau der Dividende | 50 % des Grundbedarfs: 535 € | 25 % von Grundbedarf + Sozialabdeckung (1.071 + 476 €): **387 €** | wie 28:28: 535 € |
| Dividende 2028 | 634 € | **479 €** | 634 € |
| Aus Steuern finanziert | Dach, Gemeinden, Dividende, Härtefall | wie 28:28 | dazu **Gesundheit, Seil, Altansprüche Z** |
| Außerhalb der Steuern | Gesundheit, Seil (Prämien), Z (Übergangsbeitrag) | wie 28:28 | nichts (außer eigener Vorsorge) |

Setzungen: alle übrigen Sätze im Verhältnis zum Spitzensatz (gerundet); „Sozialabdeckung“ = Gesundheit und Seil je Kopf (10,47 % des BIP je Kopf,
476 € im Monat); Härtefall 0,65 % BIP in allen Varianten (Annahme). Kapital, Unternehmen, Erbschaft, Label statisch, ohne Ausweichen.

## 2 | Ergebnis

| | 28:28 | 25:25 | 33:33 |
|---|---|---|---|
| Steuern brauchen 2028 (Quote) | 30,85 | 27,95 | 50,18 |
| Steuern bringen (Deckung) | 30,44 | 28,30 | 33,96 |
| **Saldo 2028** | **−0,41** | **+0,35** | **−16,22** |
| Saldo 2050 | −0,41 | +0,35 | −13,52 |
| **Saldo im Dauerzustand** (nach Auslauf von Z, ≈ 2075) | −0,41 | +0,35 | **−7,36** |
| Außerhalb der Steuern 2028 (Gesundheit + Seil + Z) | 19,33 | 20,01 | 0 |
| davon Altansprüche Z 2028 | 8,86 | 9,54 | (in den Steuern) |
| Gesamtlast 2028 (ohne / mit Pflicht-Vorsorge) | 50,2 / 54,3 | 48,0 / 52,1 | 50,2 / 54,3 |
| Gesamtlast im Dauerzustand | 41,3 / 45,4 | 38,4 / 42,5 | 41,3 / 45,4 |
| zum Vergleich heute | 40,76 | 40,76 | 40,76 |
| Beispiel: Alleinstehend, 42.000 € brutto: Dividende − Einkommensteuer im Jahr | +205 € | −408 € | −1.183 € |

**Viertellösung 25:25: steuerlich tragfähig.** Die niedrigere Dividende (479 statt 634 €) senkt den Bedarf stärker als die niedrigeren Sätze die
Einnahmen: Überschuss 0,35 Punkte (28:28: −0,41 mit Härtefall). Aber: Die Altansprüche über der Dividende werden größer (Z 9,54 statt 8,86), und
der Abstand zwischen Dividende und Existenzminimum wächst – mehr Menschen brauchen den Härtefall. Das widerspricht dem Ziel „wenig Sonderfälle“;
die 0,65 % für den Härtefall sind hier eher zu niedrig. Gesamtlast im Dauerzustand 38,4 % (ohne Pflicht-Vorsorge), 2,3 Punkte unter heute.

**Drittellösung 33:33: nicht tragfähig in der gerechneten Form.** Höhere Sätze bringen +3,5 Punkte, Gesundheit, Seil und Z kosten anfangs +19,3.
Auch nach dem Auslauf von Z fehlen 7,4 Punkte. Um Gesundheit und Seil dauerhaft aus Steuern zu tragen, müssten alle Spitzensätze bei rund
**45 %** liegen (Deckung 40,9 % bei 44 %, 43,1 % bei 48 %). Das entspricht dem dänischen Weg (Sozialstaat aus Steuern), nicht einer Drittelmarke.

**Was 33:33 tragen kann:** das Seil (Invalidität, Hinterbliebene, Lohnersatz; 2,72 %), wenn Gesundheit als Prämie und Z als Übergangsbeitrag
außerhalb bleiben: Bedarf 33,57 gegen Deckung 33,96, Saldo +0,39. Das wäre eine schlichte Variante: „33 % höchstens, dafür keine
Arbeitslosen-, Invaliditäts- und Hinterbliebenenversicherung mehr“.

## 3 | Gemeinsam für alle drei Wege

1. **Der Übergang (Z) passt in keine der Marken.** Er kostet anfangs 8,9 bis 9,5 % des BIP und läuft bis etwa 2075 aus. Er braucht in jedem Weg einen
   eigenen, sichtbaren, sinkenden Übergangsbeitrag (Zusammenführung v3.42, S5).
2. **Gesundheit (7,75 %) passt nur bei Sätzen um 45 % in die Steuern.** In 25:25 und 28:28 bleibt sie Prämie.
3. **Die Marke ist eine Regel der Steuersätze**, nicht der Gesamtlast. Die Gesamtlast liegt in allen Wegen im Übergang über heute und im Dauerzustand
   zwischen 38 und 41 % (ohne Pflicht-Vorsorge).

## 4 | Grenzen der Rechnung

Deckung auf deutscher Basis (sieben Einkommensgruppen); keine Ausweichreaktion bei Kapital, Unternehmen und Erbschaft (bei 33 % zu günstig, bei 25 %
zu ungünstig); Z als Schätzung mit Durchschnittsrentnern; Härtefall ohne eigene Rechnung; Nachfragewirkung des niedrigeren oder höheren Labels
nicht eingerechnet. Alle Zahlen sind Prüfrechnung, keine Prognose.

## 5 | Zu entscheiden

| Punkt | Entscheidung |
|---|---|
| V1 Marke | 28:28 / 25:25 / 33:33 / 33:33 nur mit Seil |
| V2 Mindestniveau | 50 % Grundbedarf / 25 % Grundbedarf + Sozialabdeckung |
| V3 Übergangsbeitrag für Z (in allen Wegen nötig) | ja / andere Finanzierung |
| V4 Gesundheit | Prämie (empfohlen) / Steuern (nur mit Sätzen ≈ 45 %) |
