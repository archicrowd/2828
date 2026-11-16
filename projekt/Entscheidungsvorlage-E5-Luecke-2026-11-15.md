# Entscheidungsvorlage E5: Was trägt die Lücke der Einnahmen?

Initiative 28:28 · 15. November 2026 · Modellstand v4.96 (Zahlen nach Korrekturen 91 und 92; Hebel nach Vorgaben vom 16.11.2026 in Abschnitt 9) · Rechnung: `modell/e5_varianten.py` (+ `.toml`) → `daten/aggregate/e5_varianten.json`
Status: **interne Vorlage** (Beschluss 15.11.2026: Rechnungen bis zum Abschluss von Weg C intern). Grundlage: `einnahmen_belege.json`,
`unternehmensbasis.json`, Vorlagen `Einnahmen-Belege-2026-11-15.md` und `Unternehmensbasis-Entscheidungen-2026-11-15.md`.

## 1 Ausgangslage

Vier Einnahmepositionen der geltenden Deckung (33,53 % BIP) lassen sich nach amtlichen Daten nicht in voller Höhe belegen.

| Position | Modell | belegt (mittel) | Lücke | Grund |
|---|---|---|---|---|
| Unternehmen und Plattformen | 4,42 | 2,37 | −2,05 | heutige Basis der Kapitalgesellschaften 6,0 % BIP statt 13,4 %; alle beschlossenen Hebel eingerechnet |
| Übrige Steuern | 3,93 | 2,89 | −1,04 | Emissionshandel und Grundsteuer doppelt gezählt (eigene Positionen CO₂-Preis und Grundstücksabgabe; Korrektur 92); Zölle sind Einnahmen der EU (Korrektur 91) |
| CO₂-Preis 2028 | 1,38 | 1,07 | −0,31 | die Emissionen sinken in Tonnen, das BIP wächst |
| Erbschaft | 1,16 | 0,97 | −0,19 | Basis 2022–2025 im Mittel |
| **zusammen** | | | **−3,59** (−2,94 bis −4,09) | |

## 2 Was die belegten Werte bewirken, mit allen Rückwirkungen

Die belegten Werte sind durch die ganze Kette gerechnet: Systemvarianten, Altlasten, Dynamik, Projektion, Netz, Fonds. Die Rechnung läuft
in einer Arbeitskopie, die geltende Rechnung ist unverändert.

Dividende je Erwachsenem und Monat in € (Kaufkraft 2026, ohne Kinderanteil; mit Kinderanteil × 0,948):

| | 2028 | 2035 | 2045 | 2060 | Fondsbeitrag |
|---|---|---|---|---|---|
| geltend | 384 | 309 | 261 | 256 | 5,04 % BIP |
| belegt, hoch | 212 | 124 | 62 | 16 | 5,38 |
| **belegt, mittel** | **185** | **97** | **29** | **−24** | **5,44** |
| belegt, vorsichtig | 151 | 58 | **−10** | **−72** | 5,51 |

**Drei Befunde:**
1. **Die Dividende fällt stärker als die Lücke.**
   - Ein Punkt weniger Deckung kostet die Dividende etwa 1,08 Punkte.
   - Der Grund: Alte Rentenzusagen werden oberhalb der Dividende abgegolten. Sinkt die Dividende, steigt diese Altlast, und der Fondsbeitrag
     wächst von 5,04 auf 5,44 % BIP.
2. **Langfristig verschwindet die Dividende.** Im mittleren Fall sind es 2045 noch 29 €; 2060 wäre sie negativ (−24 €). Im vorsichtigen Fall
   ist sie schon 2045 negativ.
3. **Allein trägt Option A nicht.** Die belegten Werte sind die ehrliche Grundlage. Ohne Ergänzung bleibt aber kein Puffer, und die
   Transformationsdividende verliert ab etwa 2045 ihren Sinn.

## 3 Hebel innerhalb der beschlossenen Regeln

| Hebel | Größe | Stand |
|---|---|---|
| **Label (Mehrwertsteuer):** effektiver Satz +1 Punkt, Stufen weiter höchstens 33 % | +0,38 % BIP je Punkt (statisch, `systemvarianten.konsum`) | gerechnet, erste Ordnung. Preise steigen; die Verteilung ist zu prüfen (`mwst_verteilung`) |
| **Einkommenstarif:** Grenzen der Stufen 19/25/33 % näher am Grundbedarf, Satz höchstens 33 % | nicht gerechnet; die Position ist mit 10,21 % BIP die größte | zu rechnen (`tarif_grundbedarf.py`) |
| **Erbschaft:** Freibetrag unter 100.000 € | nicht gerechnet | zu rechnen |
| **Fonds:** Tilgung nach 2098 strecken | senkt den Beitrag von 5,04 % BIP | widerspricht dem Ziel der Generationengerechtigkeit (Beschluss Tilgung bis 2098) |
| **Netz und Gemeinden** | | berührt beschlossene Bausteine |
| **Satz über 33 %** | | ausgeschlossen (E3) |

**Korrektur 90 (eigener Fehler):** Die Vorlage zur Unternehmensbasis (v4.90) nannte als Option C „weitere Einnahmen, z. B.
Bodenwertabgabe, Abbau klimaschädlicher Subventionen“. Beide stehen schon in der Deckung (Grundstücksabgabe 0,82, Subventionsabbau 0,48 %
BIP) und sind keine zusätzlichen Einnahmen.

**Größenordnung der Ergänzung:**
- Zwischen hohem und mittlerem Fall bringt jeder Punkt Deckung der Dividende 2060 rund 62 € (Ableitung, linear angenommen).
- Für mindestens 100 € im Jahr 2060 (mittel) braucht es **rund 2 Punkte BIP** mehr. Die Dividende 2028 läge dann bei rund 270 €.
- Für die geltende Dividende braucht es die ganzen 3,6 Punkte. Allein über das Label wären das gut 8 Punkte mehr; das ist nicht plausibel.

## 4 Optionen

| Option | Inhalt | Dividende 2028 / 2060 (mittel) | Bewertung |
|---|---|---|---|
| A | belegte Werte, Dividende als Rest | 185 / −24 € | ehrlich, aber 2060 nicht tragfähig |
| **A+ (Empfehlung)** | belegte Werte und eine Ergänzung um rund 2 Punkte BIP: Automatisierung und Erbe (rund 1 Punkt, zu belegen), dazu Tarif und Label, alles innerhalb des Drittels | rund 270 / 100 € (Ableitung) | tragfähig, mit Puffer; die Dividende bleibt ein spürbarer Rest |
| A++ | belegte Werte und volle Ergänzung um 3,6 Punkte | 384 / 256 € | verlangt starke Eingriffe in Tarif und Label |
| D | Fonds strecken | höher | verschiebt die Last auf spätere Generationen |

**Empfehlung A+.** Beschlossen würden die belegten Werte und ein Ziel: Die Dividende bleibt im mittleren Fall bis 2060 bei mindestens
rund 100 € (Kaufkraft 2026).
- Als Nächstes rechne ich die beiden Hebel Tarif und Label durch die Kette, mit Wirkung auf Haushalte und Preise.
- Danach legt die Initiative die Mischung fest.
- Erst dann werden Deckung, Webseite, Konzept und Working Paper umgestellt.

## 5 Zu entscheiden

1. Werden die belegten Werte (mittlerer Fall) Grundlage der Deckung? Empfehlung: ja.
2. Ziel für die Dividende: mindestens rund 100 € im Jahr 2060, oder ein anderer Wert.
3. Welche Hebel sollen gerechnet werden: Tarif, Label, Erbschaftsfreibetrag (Empfehlung: Tarif und Label).

## 6 Grenzen

- CO₂: Die Änderung wirkt nur 2028. Die Projektion rechnet den Pfad selbst, die Lücke danach ist nicht fortgeschrieben.
- Lösungsbereich: Die Verfahren für Mindestniveau und Quote suchen in festen Bereichen. Für diese Varianten ist der Bereich in der
  Arbeitskopie erweitert (`e5_varianten.toml`, `loeserbereich`).
- Ableitungen: Der Wert von rund 70 € je Punkt und der Bedarf von 1,2 Punkten sind linear abgeleitet, nicht durch die Kette gerechnet.

## 7 Nachtrag v4.94

- **Korrektur 91:** Zölle (Eigenmittel der EU) aus „Übrige“ herausgenommen. Die Lücke beträgt −3,22 statt −3,09 % BIP. Die Varianten lesen die
  Lücken jetzt direkt aus `einnahmen_belege.json`.
- **Automatisierung und Erbe** (Hinweis der Initiative): erste Abschätzung rund +1 Punkt BIP um 2045, also in der Größe der Ergänzung A+. Siehe
  `Haushaltsplan-Deutschland-2026-11-15.md`, Abschnitt 4. Noch nicht durch die Kette gerechnet.

## 8 Nachtrag v4.95

- **Korrektur 92:** Die Grundsteuer steckt in „Übrige“ und geht zugleich in der Grundstücksabgabe auf. Übrige belegt 2,89; die Lücke beträgt
  −3,59 % BIP.
- **Folge:** Für mindestens 100 € im Jahr 2060 braucht es jetzt rund 2 Punkte Ergänzung. Automatisierung und Erbe (rund 1 Punkt) decken etwa
  die Hälfte.

## 9 Hebel nach den Vorgaben der Initiative (16.11.2026), gerechnet in v4.96

Rechnung: `modell/e5_hebel.py` (+ `.toml`) → `e5_hebel.json`; Kette: `e5_varianten.py`, Varianten `Aplus_*`.

| Hebel | Vorgabe der Initiative | Umsetzung | Wirkung 2028, % BIP | Stand |
|---|---|---|---|---|
| Label | ungern, höchstens +2 Punkte; Produkte wandern mit dem Klimapfad in höhere Stufen | effektiver Satz 18,8 → 20,8 %; Stufenwanderung: der effektive Satz fällt nicht unter den Ausgangswert | +0,75; im Pfad zusätzlich bis +0,4 (2060) | gerechnet; Verteilung auf Haushalte noch zu prüfen (`mwst_verteilung`) |
| Grundbedarf | Ansatz hinterfragen, ggf. knapper; Begründung: mehr Grundvorsorge durch den Staat | ohne die Abteilungen Gesundheitspflege (21 €) und Bildung (2 € im Monat): 12.348 → 12.072 € (−2,2 %) | +0,14 | gerechnet; mit Verkehr (nur bei freiem Nahverkehr, nicht beschlossen) −7,3 % und +0,45 |
| Erbschaft | Freibetrag = 2 × jährlicher Grundbedarf | 25.694 € (2028) statt 100.000 € je Erbe | +0,47 (Spanne der Ableitung +0,3 bis +0,7) | gerechnet, Verteilung angenommen |
| Satz | 33,33 % | Spitzensatz aller Drittel-Positionen genau ein Drittel | +0,10 | gerechnet |
| Fonds, Netz, Gemeinden | bleiben | – | – | – |
| **zusammen** | | | **+1,46** und Stufenwanderung | |

**Dividende je Erwachsenem und Monat** (Kaufkraft 2026, ohne Kinderanteil; belegte Werte plus Hebel):

| Fall | 2028 | 2035 | 2045 | 2060 | Fondsbeitrag 2028 |
|---|---|---|---|---|---|
| geltend | 384 | 309 | 261 | 256 | 5,04 % BIP |
| **A+ mittel** | **262** | **194** | **150** | **131** | **5,29** |
| A+ vorsichtig | 230 | 158 | 111 | 81 | 5,35 |
| A+ hoch | 296 | 229 | 189 | 179 | 5,22 |
| nur belegt (A), mittel | 185 | 97 | 29 | −24 | 5,44 |

**Ergebnis:** Mit den Vorgaben der Initiative bleibt die Dividende im mittleren Fall dauerhaft über 100 €; 2060 sind es 131 €. Im vorsichtigen
Fall sind es 81 €. Automatisierung und Erbschaftswelle sind darin noch nicht enthalten (Haushaltsplan, Abschnitt 6: rund +1 Punkt um 2045).

**Was zu den Hebeln noch zu sagen ist:**
- **Erbschaft:**
  - Der Wert für 2 × Grundbedarf beruht auf einer angenommenen Lognormalverteilung der Erbschaften, angepasst an Mittelwert und Median im SOEP
    2002–2017. Die Gegenprobe am 99. Perzentil passt: 825.000 gegen 772.000 € (Preise 2015).
  - Der Median einer Erbschaft liegt in Preisen von 2028 bei rund 44.000 €. Mit dem neuen Freibetrag zahlt damit gut die Hälfte der Erben.
  - Offen ist, ob das selbst genutzte Elternhaus gesondert behandelt wird.
- **Grundbedarf:**
  - Das Bundesverfassungsgericht verlangt, dass das Existenzminimum steuerfrei bleibt.
  - Eine Kürzung lässt sich nur mit Leistungen begründen, die der Staat im Drittel tatsächlich stellt, etwa die Grundversorgung bei Gesundheit.
    Die Abteilungsbeträge stammen aus einer Modellrechnung nach EVS (Sekundärquelle) und sind an der Regelbedarfsermittlung zu prüfen.
  - Wird der Grundbedarf auch im Netz gekürzt (Arbeitslosigkeit, Invalidität), sinken dort zusätzlich die Ausgaben. Das ist nicht gerechnet,
    weil das Netz bleibt.
- **Label:**
  - +2 Punkte heben die Preise im Mittel um rund 1,7 % (2 / 120, Ableitung).
  - Die Stufenwanderung ist eine Regel; ihre Wirkung ist als Untergrenze angesetzt (Annahme).

**Zu entscheiden:**
1. Die Hebel so übernehmen?
2. Die Regel zur Stufenwanderung im Label beschließen?
3. Das Elternhaus bei der Erbschaft regeln?

## 10 Beschluss (16.11.2026) und Umsetzung in v4.97

**Beschluss der Initiative:**
1. Die Hebel werden übernommen: Satz ein Drittel, Grundbedarf im Tarif 12.072 € (2026), Label 7/13/19/27 % mit Sonderstufe ein Drittel,
   Erbschaftsfreibetrag 2 × jährlicher Grundbedarf.
2. Die Stufenwanderung im Label gilt: Produkte wandern mit dem Klimapfad in höhere Stufen.
3. Für das selbst bewohnte Elternhaus gibt es einen Stundungskredit zu 1 % fest, bis 20 Jahre.
4. Die Umstellung auf die belegten Einnahmen erfolgt sofort.

**Umsetzung (Logbuch v4.97, `modell/deckung_belegt.py`):**
- Belegte Positionen (2028, % BIP): Unternehmen 2,39; Übrige 2,89; CO₂-Abzug −0,31; Erbschaften 1,31.
- Stundung: Als Kassenausfall ist −0,145 % BIP vorsichtig dauerhaft angesetzt, als Zinsvorteil gegen den Fondszins 2,45 % −0,021 % BIP.
  Der Anteil der Elternhäuser (10 %) und die mittlere Dauer (10 Jahre) sind Annahmen.

**Ergebnis (geltend, Kaufkraft 2026):**
- Dividende je Erwachsenem 245 / 175 / 112 / 104 € (2028/2035/2050/2060); bis v4.96 384 / 309 / 249 / 256 €.
  - Die Werte liegen unter A+ aus Abschnitt 9 (262 / 194 / 150 / 131 €). Ursache ist der einheitlich durchgerechnete Tarif mit Grundbedarf 12.072 €
    in allen Haushaltsrechnungen und die vorsichtig angesetzte Stundung.
- Fondsbeitrag 5,32 % BIP.
- **Rentnerhaushalte mit mehr: 23,1 % (vorher 63,7 %), im Mittel −197 € im Monat.** Die Rentnerregel BS35 ist auf die frühere Dividende geeicht
  und muss neu bewertet werden (Logbuch 7.1, R16).
