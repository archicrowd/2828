# Modell E: Dividendenpaket, Dynamik und Stabilität

Initiative 28:28 · 21. November 2026 · Modellstand v4.104 (Prüfrechnung; die geltenden Zahlen bleiben unverändert)
Rechnung: `modell/modell_e.py` (+ `.toml`) → `daten/aggregate/modell_e.json`. Euro je Monat, Kaufkraft 2026, Deutschland; Anteile in % BIP.

**Vorgabe der Initiative (21.11.2026):**
- Die Dividende ist ein Paket aus den steuerfinanzierten Sozialleistungen (Netz) und einem Baranteil von mindestens 100 € für Erwachsene und Kinder.
- Kommuniziert wird der Gesamtwert, von dem die Summe X für das Netz abgezogen wird.
- Modell E wird auf Dynamik und Stabilität geprüft.

**Modell E:**
- Arbeit ein Drittel, Label 7/13/19/27 %.
- Boden 2 % des Bodenwerts, Kapital (Kapitalerträge, Unternehmen, Erbschaft) 38 %.
- Weiterer Subventionsabbau, CO₂ 150 €/t über Regel L.
- Gesundheit digital (4 % des Netzpostens), Staatsebene digital (0,6 % BIP), Bürokratieabbau 40 %.
- Erbschaftswelle und KI als Trends.
- Altlastenfonds gestreckt bis 2125, Puffer 0,5 % BIP.

## 1 Ergebnis in Kürze

- **Dividendenpaket 2028:** Gesamtwert 781 € je Erwachsenem (bar 337 €, Netz 444 €), 714 € je Kind (bar 270 €).
  - Der Baranteil liegt in allen Jahren und allen Stresstests über 100 €. Der niedrigste Wert ist 197 € je Kind, wenn alle Belastungen zusammenkommen.
- **Stabil und steigend:**
  - Der Baranteil beträgt 34,5 % des Grundbedarfs, fest und nie sinkend.
  - Mit der Fortschrittsregel steigt er ab etwa 2044 und erreicht 2060 den halben Grundbedarf: 549 € bar je Erwachsenem, Gesamtwert 1.254 €.
  - Ohne den KI-Trend sind es 2060 43 % des Grundbedarfs (468 € bar).
- **Dynamik:**
  - Das BIP liegt 2045 um 6,4 % über dem statischen Pfad, davon 4,4 Punkte KI-Trend.
  - Ohne KI sind es +1,9 %, etwa so viel wie im geltenden Stand (+1,7 %). Weniger Bürokratie (+1,35) gleicht die höhere Kapitalbelastung (−0,95) aus.
- **Stabilität:**
  - Das größte Risiko ist der Zins des Fonds. Bei 3,5 % statt 2,45 % sinkt der feste Anteil auf 26,8 % des Grundbedarfs (262 € bar).
  - Die Schuld des Fonds steigt bis 2125 auf 181 % BIP, im Zinsfall auf 196 %, wenn alles zusammenkommt auf 204 %.
- **Zum Vergleich der geltende Stand:** Der Gesamtwert ist ähnlich (700 € je Erwachsenem 2028), aber der Baranteil fällt bis 2060 auf 99 € je Erwachsenen und schon 2045 auf 97 € je Kind. Die neue Mindestregel wäre damit verletzt.

## 2 Das Dividendenpaket

| je Monat | 2028 | 2035 | 2045 | 2060 |
|---|---|---|---|---|
| Anteil am Grundbedarf (Baranteil, mit Fortschrittsregel) | 34,5 % | 34,5 % | 35,5 % | 50,0 % |
| **Gesamtwert je Erwachsenem** | **781 €** | **847 €** | **954 €** | **1.254 €** |
| davon Netz X (je Einwohner) | 444 € | 500 € | 583 € | 705 € |
| davon bar | 337 € | 348 € | 371 € | 549 € |
| **Gesamtwert je Kind** | **714 €** | **778 €** | **880 €** | **1.144 €** |
| davon bar (0,8 × Erwachsene) | 270 € | 278 € | 297 € | 439 € |
| zum Vergleich: ½ Grundbedarf | 516 € | 531 € | 551 € | 579 € |
| geltend: Gesamtwert / bar Erwachsene / bar Kind | 700 / 232 / 186 € | 685 / 166 / 133 € | 721 / 121 / 97 € | 839 / 99 / 79 € |

**Netz X** umfasst Gesundheit (Grundversorgung), Pflege (Teilkasko), Mindestrente, Invalidität, Arbeitslosigkeit, Waisen und Härtefall, steuerfinanziert und je Einwohner gemittelt. Es ist ein Versicherungswert, keine Auszahlung; der Wert für den Einzelnen hängt von Alter und Bedarf ab.

**Vorschlag für die Kommunikation:** „Ihr Dividendenpaket: 781 € im Monat. Davon tragen 444 € Ihre Gesundheit, Pflege und Absicherung, 337 € erhalten Sie auf Ihr Konto.“

## 3 Dynamik von Modell E

| BIP gegen den statischen Pfad | 2028 | 2030 | 2035 | 2045 | 2060 |
|---|---|---|---|---|---|
| **Modell E** | +0,7 % | +1,8 % | +4,0 % | +6,4 % | +8,8 % |
| davon KI-Trend | 0,0 | +0,6 | +2,1 | +4,4 | +6,8 |
| davon Bürokratieabbau 40 % | 0,0 | +0,4 | +1,35 | +1,35 | +1,35 |
| davon Beschäftigung | 0,0 | +0,2 | +0,6 | +0,6 | +0,6 |
| davon Investition (Kapital 38 %) | 0,0 | −0,2 | −0,6 | −0,95 | −0,95 |
| davon Nachfrage | +0,6 | +0,6 | 0,0 | 0,0 | 0,0 |
| Modell E ohne KI | | | | +1,9 % | |
| geltend, Stand v4.97 | +0,9 % | +1,3 % | +1,5 % | +1,7 % | +1,7 % |

**Die vier Eingaben der Dynamik:**

| Eingabe | Wert in E | Herleitung |
|---|---|---|
| Nachfrageimpuls | 1,82 % BIP | Mittel der Haushalte mit Baranteil E aus der Mikrosimulation, abzüglich der Lasten, die sie nicht enthält (Boden, Kapital, Subventionen, CO₂: 1,64 % BIP; Anteile der Haushalte angenommen) |
| Arbeitsvolumen | +1,2 % | Arbeit bleibt ein Drittel; der höhere Baranteil mindert das Volumen etwas (Einkommenseffekt, Annahme) |
| Investition | −0,95 % | wie bei 38 % |
| Netto-Anreiz Fachkräfte | ln 0,146 | geltend 0,135 |

## 4 Stabilität: Stresstests

| Test | fester Anteil am Grundbedarf | bar 2028 Erw. / Kind | 2060 mit Fortschrittsregel | Fondsschuld höchstens |
|---|---|---|---|---|
| **Modell E** | **34,5 %** | **337 / 270 €** | **50,0 % (549 €)** | **181 % BIP** |
| Fondszins 3,0 % (Rendite Euroraum 2025: 3,1 %) | 30,7 % | 300 / 240 € | 45,7 % | 189 % |
| Fondszins 3,5 % | 26,8 % | 262 / 209 € | 41,8 % | 196 % |
| ohne KI-Trend | 32,4 % | 317 / 253 € | 43,4 % | 193 % |
| Rezession 2032 (BIP −4 %, Netz +0,2 % BIP) | 34,1 % | 333 / 267 € | 50,0 % | 182 % |
| Bodenrendite 2 % (stärkere Kapitalisierung) | 32,7 % | 320 / 256 € | 48,7 % | 183 % |
| Kapital: nur halbes Mehraufkommen (Ausweichen) | 33,2 % | 325 / 260 € | 49,2 % | 182 % |
| **alles zusammen** (Zins 3,0, ohne KI, Boden 2 %, Ausweichen) | **25,2 %** | **246 / 197 €** | **34,2 %** | **204 %** |

**Lesart:**
- Die Rücklage fängt eine Rezession ohne Kürzung auf. Der Anteil sinkt dann nur um 0,4 Punkte, weil die Startdividende etwas vorsichtiger gewählt ist.
- Der Zins wirkt am stärksten, weil der Fonds bis 2125 große Schulden trägt.
- **Regel für den Zinsfall (Vorschlag):** Steigt der Fondszins dauerhaft über das Wachstum, werden zuerst Boden- und Kapitalsätze in einer festen Spanne angehoben. Arbeit und Baranteil bleiben.
- **Die Rücklage braucht eine Obergrenze.** Mit der Fortschrittsregel steigt sie bis 2060 auf rund 8 % BIP. Ein Ziel von 2 % mit jährlicher Anhebung des Anteils, solange sie darüber liegt, begrenzt das; schneller ginge es mit größeren Schritten.

## 5 Gesamtlast

| % BIP, 2028 | geltend | Modell E |
|---|---|---|
| Steuern | 31,2 | 33,5 (Boden +1,25, Kapital +0,43, Subventionen +0,3, CO₂ +0,32) |
| Altlastenzuschlag | 5,3 | 5,3; davon 3,1 an den Fonds, 2,2 an die Dividende (gestreckt bis 2125, kleinere Altrenten über der Dividende) |
| Pflichtvorsorge (eigenes Konto) | 4,1 | 4,1 |
| **zusammen** | **40,6** | **42,9** |

## 6 Bewertung und Empfehlung

- **Modell E erfüllt die neuen Vorgaben:**
  - Der Baranteil liegt stets über 100 € für Erwachsene und Kinder.
  - Der Gesamtwert ist auf Dauer steigend.
  - Arbeit bleibt bei ein Drittel.
  - Die Stabilität kommt aus Regel L, Puffer, Rücklage und Fortschrittsregel.
- **Der Preis:**
  - eine um 2,3 Punkte höhere Gesamtlast als geltend, vor allem durch die Bodenabgabe;
  - eine lange Laufzeit des Fonds mit Schulden bis 181 % BIP;
  - Abhängigkeit vom Zins.
- **Empfehlung:**
  1. Modell E als Arbeitsgrundlage nehmen, mit festem Anteil von 30 % des Grundbedarfs statt 34,5 %. Das hält die Mindestregel auch bei Fondszins 3,0 % ohne Abstriche und lässt Raum für die Fortschrittsregel.
  2. Die Zinsregel und eine Obergrenze der Rücklage beschließen.
  3. Die Bodenabgabe mit Übergang, Stundung für Rentner mit Wohneigentum und Wirkung auf Mieten durchrechnen. Sie ist der größte neue Baustein und in der Mikrosimulation noch nicht enthalten.

## 7 Grenzen

- **Die Haushaltswerte enthalten nicht:** Bodenabgabe, Kapital 38 % auf Kapitaleinkommen der Haushalte, CO₂-Kosten. Sie sind nur im Nachfrageimpuls pauschal abgezogen (Annahme).
- **KI-Trend:** Annahme in der Spanne Acemoglu 2024 bis OECD 2024; der Test ohne KI zeigt die Abhängigkeit.
- **Netz X:** Durchschnitt je Einwohner. Netz und Gesundheit sind auf Basis der zehn Staaten gerechnet, die Einnahmen auf deutscher Basis (Mischland).
- **Rücklage:** ohne Zins; Fonds mit Zins 2,45 % und nominalem Wachstum 3 %.

## Quellen

- Rechnungen des Projekts: `modell_e.json`, `stellschrauben.json` (v4.103, mit den Quellen zu Bodenwert und Subventionen), `dynamik_satz.json`, `netz33.json`, `altlasten.toml` (Zinsreihe Euroraum), `regel_boden.toml` (Kinderanteil 0,8).
