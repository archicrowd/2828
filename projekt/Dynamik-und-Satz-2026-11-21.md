# Dynamik und Satz: Führt der höhere Satz zu weniger wirtschaftlicher Belebung?

Initiative 28:28 · 21. November 2026 · Modellstand v4.102 (Prüfrechnung; die geltenden Zahlen bleiben unverändert)
Rechnung: `modell/dynamik_satz.py` (+ `.toml`) → `daten/aggregate/dynamik_satz.json`. BIP-Werte als Niveau gegen den statischen Pfad in %;
Euro je Erwachsenem und Monat, Kaufkraft 2026, Deutschland.

## 1 Antwort

- **Die Dynamik war nicht angemessen eingerechnet, in zweifacher Hinsicht.**
  1. Szenario 38 (v4.101) und die Quotenrechnung (v4.100) haben die Dynamik des geltenden Stands übernommen, als hinge sie nicht vom Satz ab.
  2. Auch die geltende Dynamik beruht auf festen Eingangswerten der Rechnung v4.84, also aus der Zeit vor der Umstellung auf belegte Einnahmen (v4.97). Seitdem haben die Haushalte im Mittel weniger mehr (214 statt 442 €), und die Grenzbelastung ist höher.
  - Beides überzeichnet die Belebung (Korrektur 96).
- **Der höhere Satz bremst die Belebung, er beschleunigt sie nicht.** Bei 38 % liegt die Grenzbelastung eines Arbeitnehmers mit 55.000 € bei 47,0 %. Das ist so viel wie heute (46,8 %), Arbeit lohnt sich an der Grenze also nicht mehr als heute. Dazu belastet der Satz Investitionen stärker, und Fachkräfte haben einen kleineren Anreiz.
- **Wirkung auf die Dividende: spürbar, aber begrenzt.**
  - Szenario 38: 142 → 196 € (2028 → 2060) statt 150 → 207 €.
  - Geltend, auf Stand v4.97 gebracht: 241 / 170 / 149 / 108 / 98 € statt 245 / 175 / 153 / 112 / 104 €.

## 2 Kanäle der Dynamik je Fall

**Eingangswerte**, mittlerer Fall (Beschluss 14.11.2026); die übrigen Kanäle (Bürokratie +0,67, Markt +0,70, Zuversicht 0) hängen nicht vom Satz ab:

| | geltend (Eingaben v4.84) | geltend, Stand v4.97 | Satz 38 |
|---|---|---|---|
| Mittel aller Haushalte 2028 | +442 € | +214 € | −67 € |
| Nachfrageimpuls | 5,08 % BIP | 2,46 % BIP | −0,77 % BIP |
| Grenzbelastung 55.000 € (heute 46,8 %) | 36 % (Annahme v3.49, andere Abgrenzung) | 41,9 % | 47,0 % |
| Arbeitsvolumen | +2,8 % | +1,3 % | +0,9 % |
| Investition (BIP) | −0,5 % | −0,5 % | −0,95 % |
| Netto-Anreiz Fachkräfte 75.000 € (ln neu/heute) | 0,184 | 0,135 | 0,054 |

**BIP gegen den statischen Pfad:**

| | 2028 | 2030 | 2035 | 2045 | 2060 |
|---|---|---|---|---|---|
| geltend (Eingaben v4.84) | +1,8 % | +2,5 % | +2,5 % | +2,7 % | +2,7 % |
| geltend, Stand v4.97 | +0,9 % | +1,3 % | +1,5 % | +1,7 % | +1,7 % |
| **Satz 38** | **−0,3 %** | **0,0 %** | **+0,8 %** | **+0,9 %** | **+0,9 %** |

**Beiträge 2045, Satz 38:** Beschäftigung +0,38, Bürokratie +0,67, Markt +0,70, Investition −0,95, Fachkräfte +0,05. Geltend sind es Beschäftigung +1,65, Investition −0,50, Fachkräfte +0,18.

**Am Anfang wirkt das Szenario bremsend.** Die Haushalte haben 2028 im Mittel weniger als heute, und der Staat legt einen Teil der Einnahmen in die Rücklage. Beides senkt die Nachfrage, zusammen −0,27 % BIP bis 2030.

## 3 Szenario 38 mit eigener Dynamik

| | ohne eigene Dynamik (v4.101) | mit eigener Dynamik |
|---|---|---|
| Dividende 2028 / 2035 / 2040 / 2050 / 2060 | 150 / 161 / 169 / 187 / 207 € | 142 / 153 / 160 / 177 / 196 € |
| Fondsbeitrag | 5,32 % BIP | 5,39 % BIP |
| Altlastenzuschlag | 16,3 % | 16,5 % |
| Haushalte mit mehr, alle / Erwerbsalter | 52 % / 66 % | 51 % / 65 % |
| Mittel alle Haushalte | −57 € | −67 € |
| oberstes Dezil | −959 € | −980 € |
| Beispiel 42.000 €, alleinstehend | +281 € | +274 € |

Das Muster bleibt: Die Dividende steigt auf Dauer, 2028 stehen weniger Haushalte besser da als im geltenden Stand.

## 4 Warum die Wirkung auf die Dividende klein ist und was das Modell nicht abbildet

- Das Aufkommen ist in % des BIP gerechnet. Mehr Wachstum hebt die Dividende in Euro, aber nicht ihren Anteil am BIP. Mehr nur über die kalte Progression und das Netz je Kopf.
- **Nicht abgebildet:** Mehr Beschäftigung senkt im Modell nicht die Kosten der Arbeitslosigkeit im Netz, denn der Anteil der Arbeitslosen ist fest. Damit fehlt ein Teil des Ertrags der Belebung, in beide Richtungen: Die Abschwächung bei 38 % kostet in Wirklichkeit eher mehr.
- Die Kanäle sind Annahmen mit schwachen Belegen (Stufe B und C, `wirtschaftsdynamik.toml`).
  - Der Investitionskanal bei 38 % ist linear im Abstand der Sätze zu heute fortgeschrieben (Annahme).
  - Die Grenzbelastung gilt aus Sicht der Beschäftigten (`grenzbelastung33`). Die Arbeitgeberseite steckt im Nachfragekanal (+0,9 %).

## 5 Folgerung und Empfehlung

1. **Ein einheitlich höherer Satz auf Arbeit nimmt dem Konzept seinen stärksten Wachstumskanal.** Das spricht für die Variante, 38 % nur auf Kapital, Unternehmen und Erbschaft zu legen und Arbeit bei ein Drittel zu lassen (R24). Sie schont die Grenzbelastung der Arbeit; der Investitionskanal wird dafür schwächer. Ich empfehle, diese Variante als Nächstes mit eigener Dynamik zu rechnen.
2. **Die geltende Dynamik auf Stand v4.97 bringen** (Korrektur 96): Impuls 2,46 % BIP, Arbeitsvolumen +1,3 %, Netto-Anreiz 0,135. Die geltende Dividende sinkt dadurch um 4 bis 6 € (245 → 241 €, 2060 104 → 98 €). Das braucht einen Beschluss, weil es die geltenden Zahlen und die Webseite bewegt.
3. **Die Rückwirkung der Beschäftigung auf das Netz** (Arbeitslose) ins Modell aufnehmen. Dann misst die Rechnung den Wert der Belebung vollständiger.

## Quellen

- Rechnungen des Projekts: `dynamik_satz.json`, `dynamik_geltend.json`, `wirtschaftsdynamik.toml` (Kanäle, Belege, Literatur), `dynamik33.toml`, `grenzbelastung33.json`, `szenario38.json`, `mikro_de.json`.
- Literatur zu den Kanälen wie in `wirtschaftsdynamik.toml` und `dynamik33.toml` angegeben, u. a. Gechert (2015), Lichter/Peichl/Siegloch (2015), Keane (2011), Chetty u. a. (2011), Heady u. a. (2009, OECD), ifo (2024, eine Studie, Auftraggeber Interessenvertretung), IWF (2025, Sekundärquelle). In dieser Version nicht erneut an der Quelle geprüft.
