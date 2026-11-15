# Entscheidungsvorlage E5: Was trägt die Lücke der Einnahmen?

Initiative 28:28 · 15. November 2026 · Modellstand v4.94 (Zahlen nach Korrektur 91) · Rechnung: `modell/e5_varianten.py` (+ `.toml`) → `daten/aggregate/e5_varianten.json`
Status: **interne Vorlage** (Beschluss 15.11.2026: Rechnungen bis zum Abschluss von Weg C intern). Grundlage: `einnahmen_belege.json`,
`unternehmensbasis.json`, Vorlagen `Einnahmen-Belege-2026-11-15.md` und `Unternehmensbasis-Entscheidungen-2026-11-15.md`.

## 1 Ausgangslage

Vier Einnahmepositionen der geltenden Deckung (33,53 % BIP) lassen sich nach amtlichen Daten nicht in voller Höhe belegen.

| Position | Modell | belegt (mittel) | Lücke | Grund |
|---|---|---|---|---|
| Unternehmen und Plattformen | 4,42 | 2,37 | −2,05 | heutige Basis der Kapitalgesellschaften 6,0 % BIP statt 13,4 %; alle beschlossenen Hebel eingerechnet |
| Übrige Steuern | 3,93 | 3,26 | −0,67 | Emissionshandel doppelt gezählt (auch im CO₂-Preis); Zölle sind Einnahmen der EU (Korrektur 91) |
| CO₂-Preis 2028 | 1,38 | 1,07 | −0,31 | die Emissionen sinken in Tonnen, das BIP wächst |
| Erbschaft | 1,16 | 0,97 | −0,19 | Basis 2022–2025 im Mittel |
| **zusammen** | | | **−3,22** (−2,57 bis −3,72) | |

## 2 Was die belegten Werte bewirken, mit allen Rückwirkungen

Die belegten Werte sind durch die ganze Kette gerechnet: Systemvarianten, Altlasten, Dynamik, Projektion, Netz, Fonds. Die Rechnung läuft
in einer Arbeitskopie, die geltende Rechnung ist unverändert.

Dividende je Erwachsenem und Monat in € (Kaufkraft 2026, ohne Kinderanteil; mit Kinderanteil × 0,948):

| | 2028 | 2035 | 2045 | 2060 | Fondsbeitrag |
|---|---|---|---|---|---|
| geltend | 384 | 309 | 261 | 256 | 5,04 % BIP |
| belegt, hoch | 235 | 149 | 87 | 50 | 5,34 |
| **belegt, mittel** | **195** | **108** | **43** | **−7** | **5,42** |
| belegt, vorsichtig | 168 | 80 | 10 | **−47** | 5,47 |

**Drei Befunde:**
1. **Die Dividende fällt stärker als die Lücke.**
   - Ein Punkt weniger Deckung kostet die Dividende etwa 1,08 Punkte.
   - Der Grund: Alte Rentenzusagen werden oberhalb der Dividende abgegolten. Sinkt die Dividende, steigt diese Altlast, und der Fondsbeitrag
     wächst von 5,04 auf 5,42 % BIP.
2. **Langfristig verschwindet die Dividende.** Im mittleren Fall sind es 2045 noch 43 €; 2060 wäre sie negativ (−7 €). Im vorsichtigen Fall
   ist sie schon 2045 fast null.
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
- Zwischen hohem und mittlerem Fall bringt jeder Punkt Deckung der Dividende 2060 rund 88 € (Ableitung, linear angenommen).
- Für mindestens 100 € im Jahr 2060 (mittel) braucht es **rund 1,2 Punkte BIP** mehr. Die Dividende 2028 läge dann bei rund 270 €.
- Für die geltende Dividende braucht es die ganzen 3,2 Punkte. Allein über das Label wären das gut 8 Punkte mehr; das ist nicht plausibel.

## 4 Optionen

| Option | Inhalt | Dividende 2028 / 2060 (mittel) | Bewertung |
|---|---|---|---|
| A | belegte Werte, Dividende als Rest | 195 / −7 € | ehrlich, aber 2060 nicht tragfähig |
| **A+ (Empfehlung)** | belegte Werte und eine Ergänzung um rund 1,2 Punkte BIP aus Tarif und Label, beide innerhalb des Drittels | rund 270 / 100 € (Ableitung) | tragfähig, mit Puffer; die Dividende bleibt ein spürbarer Rest |
| A++ | belegte Werte und volle Ergänzung um 3,2 Punkte | 384 / 256 € | verlangt starke Eingriffe in Tarif und Label |
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
