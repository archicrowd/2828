# Drittellösung weitergedacht: Mehrwertsteuer, prämienfreie Variante, Altlastenfonds (Stand v3.45, 17. Oktober 2026)

**Status: Prüfrechnung; die Gesamtrechnung bleibt bei 28:28, bis die Initiative entscheidet.** Rechnungen `modell/systemvarianten.py`
(Systeme 33M, 33N, 33P) und `modell/altlasten.py` (+ `.toml`), Ergebnisse `daten/aggregate/systemvarianten.json`, `altlasten.json`.
Prozent des BIP, Durchschnitt der zehn Staaten; Euro im Monat, Preise 2028; Deckung auf deutscher Basis; Altrenten Z als Schätzung (v3.42).

## 1 | Vorgaben der Initiative (17.10.2026)

1. 33 % Mehrwertsteuer nur für die ganz schädlichen Produkte, kein Regelfall.
2. Die prämienfreie Lösung prüfen.
3. Der Altlastenbeitrag geht nicht einseitig und nicht länderbezogen auf die Löhne; maximale Streckung, Tilgung bei Einnahmenspitzen.

## 2 | Mehrwertsteuer: 33 % nur als Sonderstufe

Label wie bisher **5 / 11 / 17 / 22 / 28 %**, dazu eine Sonderstufe **33 % nur für Alkohol und Tabak** (in den gerechneten Produktgruppen die einzige
dieser Art; Setzung). Fahrzeuge und Kraftstoffe bleiben bei 28 %. Effektiver Satz **17,1 %** statt 20,0 % bei durchgehend skalierten Stufen.
Die Steuern bringen damit **32,85 %** statt 33,96 % des BIP. Die Drittellösung aus v3.44 (Dividende ⅓, 618 €) hätte so einen Fehlbetrag von 0,95 Punkten.

## 3 | Zwei ausgeglichene Drittel-Varianten

| | **mit Prämie (33N)** | **prämienfrei (33P)** |
|---|---|---|
| Höchstsätze | Einkommen, Kapital, Gewinne, Erbschaft 33 %; Mehrwertsteuer 28 %, nur Alkohol/Tabak 33 % | gleich |
| Aus Steuern | Dach, Gemeinden, Dividende, Härtefall, Seil, 30 % der Gesundheit | Dach, Gemeinden, Dividende, Härtefall, Seil, **die ganze Gesundheit** |
| Mindestniveau der Dividende | 30 % von Grundbedarf + Sozialabdeckung: 460 € | 18 % des Grundbedarfs: 192 € |
| **Dividende 2028 (DE, Erwachsene)** | **560 €** | **265 €** |
| Gesundheitsprämie (Durchschnitt je Einwohner) | 245 € | 0 € |
| **Dividende nach Prämien je Einwohner (Durchschnitt)** | **227 €** | **224 €** |
| Steuern brauchen / bringen / Saldo | 32,70 / 32,85 / +0,15 | 32,62 / 32,85 / +0,23 |
| Altrenten Z 2028 | 9,19 | 10,46 |
| Gesamtlast im Dauerzustand (ohne eigene Vorsorge) | 38,9 | 33,4 |

**Befund:** Beide Wege kosten fast dasselbe und lassen dem Einzelnen fast dasselbe übrig (227 gegen 224 € je Einwohner). Der Unterschied liegt in der Form:
- **Prämienfrei** ist einfacher: keine Prämie, keine Belastungsgrenze, kein Selbstbehalt, also keine Sonderfälle in der Gesundheit; jeder ist versorgt.
  Dafür ist die Zahl auf dem Konto klein (265 €), und die Altrenten über der Dividende sind größer (10,5 % statt 9,2 %).
- **Mit Prämie** zeigt eine größere Dividende, verlangt aber für Geringverdiener eine Belastungsgrenze.
- Die prämienfreie Gesamtlast ist niedriger, weil die Dividende kleiner ist; die Versorgung (Gesundheit, Seil) ist dieselbe.

## 4 | Altlastenfonds: breit finanziert, maximal gestreckt

**Konstruktion:** Ein gemeinsamer Fonds übernimmt die Staatsschulden (81,3 % 2028) und die Altrenten über der Dividende. Er erhält einen gleichbleibenden
Beitrag aus einer breiten Quelle – nicht aus den Löhnen allein: entweder als **Zuschlag auf alle Steuern** (wie ein Solidaritätszuschlag) oder als
**gleicher Abzug je Einwohner** von der Dividende. Was in Jahren mit Einnahmenspitzen über dem gleitenden Fünfjahresdurchschnitt liegt, geht in die Tilgung.

| Variante (Zins 2,5 %, Wachstum nominal 3 %) | Beitrag % BIP | Zuschlag auf alle Steuern | je Einwohner und Monat | Schuldenquote: Spitze |
|---|---|---|---|---|
| prämienfrei, Z voll, auf 60 % bis 2125 | 2,85 | 8,7 % | 128 € | 249 % (2065) |
| prämienfrei, Z halb, auf 60 % bis 2125 | 1,36 | 4,2 % | 61 € | 160 % (2064) |
| mit Prämie, Z voll, auf 60 % bis 2125 | 2,24 | 6,9 % | 101 € | 224 % (2062) |
| mit Prämie, Z halb, auf 60 % bis 2125 | 1,06 | 3,2 % | 48 € | 149 % (2061) |
| mit Prämie, Z halb, Deckel 120 % | 2,08 | 6,3 % | 94 € | 120 %; 2100 bei 34 % |
| prämienfrei, Z halb, Deckel 120 % | 2,75 | 8,4 % | 124 € | 120 %; 2100 bei 20 % |
| mit Prämie, Z voll, Deckel 120 % | 6,24 | 19,1 % | 282 € | 120 % |

Bei einem Zins in Höhe des Wachstums (3 %) steigt der Beitrag um 0,55 bis 0,85 Punkte.

**Was das bedeutet:**
1. **Maximale Streckung ist billig im Jahr, aber teuer im Risiko.** Bis 2125 gestreckt, liegt der Beitrag bei 1 bis 3 % des BIP, die Schuldenquote steigt aber
   um 2060 auf 150 bis 250 %. Das trägt nur, solange der Zins unter dem Wachstum liegt; steigt er darüber, wächst die Schuld von selbst. Ein **Deckel bei
   120 %** ist der vorsichtigere Weg und mit halber Einrechnung der Altrenten bezahlbar (6 bis 8 % Zuschlag auf alle Steuern).
2. **Die Altrenten nur zur Hälfte einzurechnen, halbiert den Beitrag ungefähr.** Das ist die entscheidende politische Frage: wie viel der Zusagen ohne
   angesparte Anlagen gekürzt wird (Bilanzregel, Untergrenze Grundbedarf, Vertrauensschutz; juristisch zu prüfen).
3. **Ein gemeinsamer, nicht länderbezogener Fonds ist ein großer Ausgleich zwischen den Staaten.** Altlast 2028 (Altrenten + Zinsen) gegen den Durchschnitt
   von 12,2 % des BIP: Österreich +5,2, Frankreich +3,3, Spanien +2,3, Belgien +0,9, Slowenien +0,3, Deutschland −0,1, Estland −4,3, Niederlande −5,8,
   Irland −8,7, Dänemark −11,5 Punkte des eigenen BIP. Dänemark, Irland und die Niederlande würden die Altlasten anderer mittragen. Für den Beitritt dieser
   Staaten ist das eine hohe Hürde. Ein Mittelweg: gemeinsamer Fonds (eine Zinsgarantie, ein Beitrag), aber Verrechnung je Staat über einen abschmelzenden
   Aufschlag auf den Anteil des Daches – so wie das Konzept die Altschulden schon heute behandelt.
4. **„33 höchstens“ und der Zuschlag:** Ein Zuschlag von 6 % auf alle Steuern hebt den Spitzensatz der Einkommensteuer rechnerisch auf rund 35 %.
   Das muss als befristeter, sinkender Generationenzuschlag erzählt werden – oder der Beitrag läuft als gleicher Abzug je Einwohner von der Dividende.

## 5 | Erzählung (Vorschlag, prämienfreie Variante)

> Höchstens ein Drittel auf jeden Euro. Dafür sind alle versorgt – Gesundheit, Arbeitslosigkeit, Invalidität – ohne Prämie und ohne Antrag, und jeder bekommt
> jeden Monat eine Dividende. Was frühere Generationen geliehen und versprochen haben, tragen wir gemeinsam, langsam und offen ab: ein kleiner, befristeter
> Zuschlag, und was in guten Jahren mehr hereinkommt, tilgt die alte Last.

## 6 | Zu entscheiden

| Punkt | Entscheidung |
|---|---|
| E1 Drittel mit Prämie (Dividende 560 €) oder prämienfrei (265 €) | |
| E2 Sonderstufe 33 % Mehrwertsteuer: nur Alkohol und Tabak, oder weitere Produkte (welche?) | |
| E3 Anteil der Altrenten im Fonds | 100 % / 50 % / ___ |
| E4 Streckung | bis 2125 ohne Deckel / Deckel 120 % / ___ |
| E5 Quelle des Beitrags | Zuschlag auf alle Steuern / Abzug je Einwohner von der Dividende |
| E6 Fonds gemeinsam ohne Verrechnung oder mit Verrechnung je Staat | |

## 7 | Grenzen

Deckung auf deutscher Basis, ohne Ausweichreaktionen; Mehrwertsteuer-Gruppen grob (Alkohol und Tabak als einzige Gruppe der Sonderstufe); Altrenten Z mit
Durchschnittsrentnern; konstanter Zins und konstantes Wachstum; Tilgung bei Einnahmenspitzen nicht beziffert; keine Rückwirkung einer hohen Schuldenquote
auf den Zins. Alle Zahlen Prüfrechnung, keine Prognose.
