# Stabile Dividende als Maxime: was die übrigen Stellschrauben leisten

Initiative 28:28 · 21. November 2026 · Modellstand v4.103 (Prüfrechnung; die geltenden Zahlen bleiben unverändert)
Rechnung: `modell/stellschrauben.py` (+ `.toml`) → `daten/aggregate/stellschrauben.json`.
Euro je Erwachsenem und Monat, Kaufkraft 2026, Deutschland; Anteile in % BIP.

**Vorgaben (Auftrag 21.11.2026):**
- Maxime: eine stabile Dividende von ½ Grundbedarf.
- Arbeit bleibt bei ein Drittel, das Label bleibt bei 7/13/19/27 %.
- Für Stabilität sorgen andere Regeln: Regel L (Lenkungsabgaben an den Fonds), Puffer 0,5 % BIP, Rücklage.
- Digitalisierung und Vereinfachung im festen Blick.

## 1 Ergebnis in Kürze

1. **½ Grundbedarf sind 516 € (2028).** Der Grundbedarf folgt zu 30 % den Löhnen; 2060 sind es 568 €.
   - Mit den jetzigen Einnahmen fehlen dafür 6,1 % BIP (2028) bis 5,1 % BIP (2060).
   - Darin schon gegengerechnet: weniger Aufstockung im Netz (0,4 bis 0,8 % BIP) und kleinere Altrenten über der Dividende im Fonds (0,7 % BIP).
2. **Keine einzelne Stellschraube und kein Paket ohne Streckung des Fonds trägt ½ Grundbedarf.**
   - Das stärkste Paket ohne Streckung (D) trägt dauerhaft 22,5 % des Grundbedarfs (233 € steigend auf 256 €), 2060 erreichbar sind 31 % (351 €).
   - Mit Streckung des Fonds bis 2125 (E) sind es 33,7 % (348 → 383 €), 2060 erreichbar 47 %. Die Schuld des Fonds steigt dann aber auf 206 % BIP.
3. **Warum der ursprüngliche Ansatz leichter aussah:** Der halbe Grundbedarf (535 €, v3.43) war ein Bruttobetrag. Davon gingen Prämien für Gesundheit und Seil ab (472 € je Einwohner, v3.44); netto blieben 63 €.
   - Im Goldenen Drittel sind Gesundheit, Pflege und Netz steuerfinanziert und je Einwohner rund 468 € im Monat wert.
   - Zusammen mit 245 € Dividende ist das heute schon mehr als der ursprüngliche halbe Grundbedarf. Ein halber Grundbedarf in bar ist ein neues, deutlich höheres Ziel.
4. **Am besten wirken:**
   - Grundstücksabgabe auf den Bodenwert (bis +1,25 % BIP, ohne Wachstumsverlust);
   - Streckung des Fonds (+1,77 % BIP, Risiko);
   - Kapital 38–40 % (+0,4 bis +0,6, kostet 0,5 bis 0,7 % BIP Wachstum);
   - Digitalisierung im Gesundheitswesen (+0,3);
   - weiterer Subventionsabbau (+0,3).
5. **Digitalisierung und Vereinfachung** wirken vor allem über Wachstum (Bürokratie +0,7 % BIP, KI +4,4 % BIP 2045) und über eine schlanke Staatsebene.
   - In die Dividende kommt das Wachstum nur über eine Regel, die Wachstumsgewinne in den Anteil am Grundbedarf weitergibt.
   - Ohne digitale Verwaltung droht dagegen die nächste Lücke: Die Staatsebene fehlt im Modell, nötig sind 0,6 bis 1,2 % BIP.

## 2 Bedarf für ½ Grundbedarf

| | 2028 | 2035 | 2045 | 2060 |
|---|---|---|---|---|
| ½ Grundbedarf | 516 € | 527 € | 543 € | 568 € |
| Bedarf in % BIP | 9,95 | 9,45 | 8,81 | 7,95 |
| Lücke gegen das Verfügbare | 6,13 | 6,67 | 6,02 | 5,05 |
| davon schon abgezogen: Netz entlastet | 0,41 | 0,47 | 0,57 | 0,81 |

- **Verfügbar heißt:** geltende Einnahmen mit Regel L, Puffer 0,5 % BIP und Dynamik auf Stand v4.97 (Korrektur 96).
- **Fonds:** Steigt die Dividende auf ½ Grundbedarf, sinken die Altrenten über der Dividende; der Fondsbeitrag sinkt um 0,69 % BIP. Dieser Betrag geht bei gleicher Gesamtlast an die Dividende.
- **Ohne weitere Stellschrauben** trägt das Verfügbare mit Rücklage dauerhaft nur 8,3 % des Grundbedarfs, 86 € steigend auf 94 €.
  - Ein großer Teil der geltenden 245 € im Jahr 2028 stammt aus Lenkungsabgaben, die wegfallen; ein anderer aus dem Puffer, der jetzt zurückgelegt wird.

## 3 Die Stellschrauben einzeln

| Stellschraube | 2028 | 2045 | 2060 | Dividende 2028 | Wachstum (BIP 2045) | Verteilung | Einfachheit, Digitalisierung |
|---|---|---|---|---|---|---|---|
| **Boden 1,5 %** des Bodenwerts | +0,93 | +0,93 | +0,93 | +48 € | 0 | Eigentümer; Rentner mit Wohneigentum brauchen eine Stundung | eine Bemessung, digital aus Kataster und Grundsteuerwerten |
| Boden 2,0 % | +1,25 | +1,25 | +1,25 | +65 € | 0 | wie oben | wie oben |
| Boden 1,0 % | +0,52 | +0,52 | +0,52 | +27 € | 0 | wie oben | wie oben |
| Kapital 38 % (Arbeit bleibt ein Drittel) | +0,43 | +0,40 | +0,40 | +22 € | −0,49 % | oberes Zehntel | einfach, aber Ausweichen |
| Kapital 40 % | +0,60 | +0,55 | +0,56 | +31 € | −0,69 % | oberes Zehntel | wie oben |
| Subventionen, weiterer Abbau (mittel) | +0,30 | +0,30 | +0,30 | +16 € | 0 | je Posten | weniger Ausnahmen |
| CO₂ 150 €/t (über Regel L) | +0,14 | +0,14 | +0,14 | +7 € | 0 | Konsum, Rentner belastet | ein Preis |
| Gesundheit digital (mittel, 4 %) | +0,31 | +0,33 | +0,34 | +16 € | 0 | neutral | Akte, Telemedizin, Abrechnung |
| Bürokratieabbau 40 % (digital) | 0,00 | +0,04 | +0,04 | 0 € | +0,67 % | breit | Lohn, Steuer, Leistungen automatisch |
| KI und Automatisierung (Trend) | 0,00 | +0,44 | +0,69 | 0 € | +4,44 % | Kapitalseite | unsicher |
| Erbschaftswelle (Trend) | 0,00 | +0,33 | +0,33 | 0 € | 0 | große Erbschaften | – |
| **Fonds gestreckt bis 2125** | +1,77 | +1,77 | +1,77 | +92 € | 0 | künftige Generationen | **Risiko:** Schuld 206 % BIP statt 154 % |
| Staatsebene nötig (EU-Maß) | −1,20 | −1,20 | −1,20 | −62 € | – | – | heute nicht abgebildet |
| Staatsebene digital verschlankt | −0,60 | −0,60 | −0,60 | −31 € | – | – | Steuer ohne Erklärung, ein Register |

Die Wirkungen der Stellschrauben sind überwiegend Annahmen mit Spannen (`stellschrauben.toml`). Wachstum wirkt in der Rechnung nur über den Bedarf, weil der Grundbedarf langsamer wächst als das BIP; Mehraufkommen in % BIP ist nicht angesetzt.

## 4 Pakete

| Paket | stabil, fester Anteil am Grundbedarf | Dividende 2028 → 2060 | 2060 erreichbar | Lücke 2060 zu ½ |
|---|---|---|---|---|
| ohne Stellschrauben (Regel L, Puffer) | 8,3 % | 86 → 94 € | 7,4 % | – |
| **A** Boden 1,5 %, Subventionen, CO₂ 150, Gesundheit digital, Staatsebene digital, Bürokratie digital | 16,0 % | 165 → 182 € | 17,1 % | 3,9 % BIP |
| **B** wie A, dazu Kapital 38 % | 18,8 % | 194 → 214 € | 20,7 % | 3,5 |
| **C** wie A, dazu Trends KI und Erbschaftswelle | 17,8 % | 183 → 202 € | 24,2 % | 2,9 |
| **D** wie C, Boden 2 % und Kapital 38 % | 22,5 % | 233 → 256 € | 30,9 % | 2,2 |
| **E** wie D, Fonds gestreckt bis 2125 | 33,7 % | 348 → 383 € | 46,6 % | 0,4 |

- **„Stabil“** heißt: ein fester Anteil am Grundbedarf von 2028 bis 2060, der nie sinkt. Eine Rücklage ohne Zins gleicht die Jahre aus.
- **„Erreichbar“** ist der Anteil, den das jeweilige Jahr allein trägt.
- **Was der Abstand zeigt:** Bei C, D und E liegt das Erreichbare 2060 deutlich über dem stabilen Anteil, weil die Trends wirken. Eine Fortschrittsregel, die den Anteil anhebt, sobald die Rücklage es erlaubt, gibt diesen Zuwachs weiter. Ohne sie würde die Rücklage bis 2060 auf 8 bis 19 % BIP wachsen.

## 5 Vorschlag für die Maxime und die Regeln zur Stabilität

**Maxime (Vorschlag):** „Die Dividende ist ein fester Anteil des Grundbedarfs. Er sinkt nie und steigt, sobald die Rücklage es erlaubt, bis zur Hälfte des Grundbedarfs.“

**Regeln zur Stabilität:**
1. **Regel L:** Lenkungsabgaben gehen an den Fonds, der selbst ausläuft.
2. **Puffer und Rücklage:** 0,5 % BIP je Jahr als Ausgleichsrücklage. Überschüsse gehen zuerst in die Rücklage.
3. **Fortschrittsregel:** Liegt die Rücklage drei Jahre über einem Ziel (z. B. 2 % BIP), steigt der Anteil um einen Punkt. Bei Unterschreiten steigen zuerst Boden- und Kapitalsätze innerhalb einer festen Spanne. Arbeit bleibt bei ein Drittel, die Dividende wird nicht gekürzt.

**Empfohlene Stellschrauben:**
- **Zuerst Paket A** (16 %, 165 € steigend). Es belastet Arbeit nicht zusätzlich, ist am einfachsten und schont das Wachstum. Die Bodenabgabe ist der stärkste Einzelhebel ohne Wachstumsverlust; mit der Grundsteuerreform liegen Flächen und Bodenrichtwerte für über 35 Mio. Einheiten bereits digital vor (Destatis 2026; nicht alle Länder bewerten nur den Boden).
- **Dann Boden 2 %** als nächste Stufe. Kapital 38 % nur, wenn die Wachstumskosten (−0,5 % BIP) bewusst getragen werden.
- **Den Fonds nicht strecken**, solange der Zins nicht deutlich unter dem Wachstum liegt.
- **Die Staatsebene digital** und schlank aufbauen (0,6 statt 1,2 % BIP). Sie ist die größte Gefahr für die Dividende.

**Was offen ist:** Ein halber Grundbedarf in bar ist mit diesen Stellschrauben erst nach 2060 und nur mit gestrecktem Fonds erreichbar. Wer ihn früher will, muss eine der Festlegungen öffnen:
- Arbeit bleibt bei ein Drittel;
- das Label höchstens +2 Punkte;
- Gesundheit und Netz vollständig aus Steuern (im ursprünglichen Ansatz: Prämien).

## 6 Grenzen

- **Bodenwert:** 6.778 Mrd. € ohne Staat, 2024 (Bundesbank, maschinell aus dem PDF gelesen, an der Quelle zu prüfen).
  - Der Wert sinkt mit der Abgabe; angesetzt ist eine Rendite von 3 % (Annahme).
  - Übergang und Verteilung sind nicht gerechnet: Rentner mit Wohneigentum, Mieten.
- **Wachstumswirkungen** sind Annahmen der Belegstufe B/C (wirtschaftsdynamik, dynamik33).
- **Gesundheit digital:** Die Spanne 2 bis 6 % ist eine Annahme. Die Zahlen von Beratungsunternehmen (bis 42 Mrd. €) sind eine Sekundärquelle mit eigenem Interesse.
- **Subventionen:** UBA 65,4 Mrd. € (2018, Untergrenze, neuere Werte fehlen); der zusätzlich erreichbare Teil ist eine Annahme.
- **Rücklage:** ohne Zins gerechnet.
- **Mischland:** Ausgaben der zehn Staaten, Einnahmen auf deutscher Basis.

## Quellen

- Deutsche Bundesbank: Sektorale und gesamtwirtschaftliche Vermögensbilanzen, Datenblatt: https://www.bundesbank.de/resource/blob/615796/172470bf10b3ab18f11160d7749b1bef/mL/sektorale-und-gesamtwirtschaftliche-vermoegensbilanzen-data.pdf
- Umweltbundesamt: Umweltschädliche Subventionen in Deutschland: https://www.umweltbundesamt.de/daten/umwelt-wirtschaft/umweltschaedliche-subventionen-in-deutschland
- Destatis, Pressemitteilung 395/2026 (Statistik der Grundsteuerwerte, Stichtag 1.1.2022): https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/11/PD26_395_73.html
- Projekt: `Loesung-Drittel-2026-10-17.md` und `Systemvarianten-25-33-2026-10-17.md` (ursprünglicher Ansatz, v3.43/v3.44); `stellschrauben.json`, `dynamik_satz.json`, `netz33.json`, `quote_optimum.json`, `co2_varianten.json`, `wirtschaftsdynamik.toml`, `dynamik33.toml`.
