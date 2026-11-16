# Kurzdarstellung: Rentner, Unternehmenssteuern, Plattformen, Importe und CO₂

Initiative 28:28 · 16. November 2026 · Modellstand v4.98 (Prüfrechnungen; die geltenden Zahlen v4.97 sind unverändert)
Rechnungen: `modell/rentner_eichung.py`, `modell/co2_varianten.py` (je mit `.toml`) → `daten/aggregate/rentner_eichung.json`, `co2_varianten.json`.
Alle Eurowerte je Monat, Jahr 2028, Kaufkraft 2026; Anteile in % des BIP 2028.

## 1 Das Wichtigste

1. **Rentner verlieren nicht wegen der kleineren Dividende.**
   - Die Dividende steckt bei ihnen schon in der Bestandsrente; der Fonds zahlt nur den Anspruch darüber (Korrektur 65).
   - Die Begründung in v4.97 („die Dividende sinkt“) war falsch (Korrektur 94).
   - Die Rentner tragen die neuen Verbrauchs- und Tariflasten ohne den Ausgleich, den Erwerbstätige über die Dividende erhalten. Den größten Teil macht das Label aus.
2. **Die Unternehmenssteuer ist nicht niedriger als heute.**
   - Gewinnbezogene Steuern ohne Einkommensteuer liegen neu bei 3,77 % BIP, heute bei 3,76 %.
   - Niedrig ist das deutsche Niveau selbst: Der Anteil der Unternehmenssteuern am Steueraufkommen ist halb so groß wie im OECD-Mittel. Ein Grund ist, dass viele Betriebe Personengesellschaften sind; ihr Gewinn steht in der Position Einkommen.
3. **Bei CO₂ gibt es zwei neue Befunde.**
   - Die Position ist um 0,38 % BIP zu hoch angesetzt. Grund: Frei zugeteilte Zertifikate im EU-Emissionshandel bringen keine Einnahmen.
   - Die Haushaltsrechnungen enthalten keine CO₂-Kosten. Eine strengere CO₂-Bepreisung ist möglich, belastet aber vor allem die Rentner, solange sie keinen Ausgleich erhalten.

## 2 Rentner: Ursache und Varianten

**Ursache.** Die Bausteine von v4.97 werden in der Rechnung der Rentnerhaushalte unter der Regel BS35 nacheinander eingeführt:

| Schritt | Rentnerhaushalte mit mehr | Mittel | Wirkung |
|---|---|---|---|
| alles wie v4.96 | 64,1 % | −117 € | |
| Grundbedarf im Tarif 12.072 € | 58,9 % | −130 € | −13 € |
| Satz ein Drittel | 58,9 % | −132 € | −2 € |
| Label 7/13/19/27 (effektiv 20,61 %) | 31,5 % | −176 € | **−44 €** |
| Zuschlag DE 16,8 % (alles v4.97) | 24,0 % | −187 € | −11 € |

Die Ausgangszeile weicht um 8 € von v4.96 ab (−109 €). Grund: Der Zuschlag v4.96 ist hier vereinfacht angesetzt.

**Varianten.** R1, R2 und R4 sind so geeicht, dass das Mittel wieder −109 € beträgt (Stand v4.96).
- Spalte „Kosten“: Mindereinnahme gegenüber BS35.
- Spalte „Dividende“: Wirkung auf die Dividende je erwerbstätigem Erwachsenen, wenn die Kosten über sie getragen werden. Das ist eine Näherung.

| Variante | Regel | mit mehr | Mittel | Fünftel 1 / 2 / 3 / 4 / 5 | Kosten | Dividende |
|---|---|---|---|---|---|---|
| R0 BS35 geltend | Freibetrag 1–2 G, 27,5 / 55,1 % | 24,0 % | −187 € | +8 / 0 / −49 / −162 / −739 € | – | – |
| R1 Sätze senken | 8,1 / 16,1 % | 24,0 % | −109 € | +8 / 0 / −36 / −110 / −412 € | 0,39 % BIP (19,3 Mrd. €) | −21 € |
| R2 Freibetrag erhöhen | 1.739 € bis 3.478 € je Monat | 24,0 % | −109 € | +8 / 0 / −30 / −94 / −434 € | 0,39 % BIP | −21 € |
| R3 nur oberen Satz senken | 27,5 / 40 % | 24,0 % | −170 € | +8 / 0 / −49 / −154 / −659 € | 0,09 % BIP | −5 € |
| **R4 Altersausgleich** | **55 € je Person und Monat, steuerfrei** | **64,5 %** | **−109 €** | **+48 / +68 / +34 / −68 / −636 €** | **0,23 % BIP (11,3 Mrd. €)** | **−12 €** |

**Empfehlung: R4.**
- Die Verluste kommen aus Label, Tarif und Zuschlag. Erwerbstätige gleichen sie über die Dividende aus; Rentner haben diesen Ausgleich nicht. Ein fester Altersausgleich ersetzt ihn dort, wo er fehlt.
- R4 bringt den Anteil mit mehr auf das Niveau von v4.96 zurück (64,5 %) und kostet gut die Hälfte von R1 oder R2.
- R1 und R2 entlasten nur die oberen Fünftel, der Anteil mit mehr steigt nicht. Sie geben 70 % der Kürzung der Zusagen auf und schwächen damit die Logik der Regel BS35.
- R3 kann zusätzlich gewählt werden, wenn die Spitze (−739 €) zu hoch erscheint.

**Grenzen der Rechnung.**
- Versicherungsjahre sind zugeschätzt (Annahme, v4.69).
- Die Kosten gelten nur für Deutschland und nur für 2028; der Bestand der Altrenten sinkt danach.
- Die CO₂-Kosten fehlen (Abschnitt 6). Mit ihnen wäre ein höherer Altersausgleich nötig.

## 3 Unternehmenssteuern: Warum 2,39 % BIP plausibel sind

**Heute gegen neu, gewinnbezogene Steuern ohne Einkommensteuer:**

| | heute 2025 | neu 2028 |
|---|---|---|
| Körperschaftsteuer | 39,0 Mrd. € | Position Unternehmen (Kapitalgesellschaften, Kundenort, Plattformen, Gewinnverlagerung, Verlustregel): 2,39 % BIP |
| Gewerbesteuer (alle Rechtsformen) | 75,3 Mrd. € | entfällt; der Gewinn der Personengesellschaften wird in der Position Einkommen besteuert (Beschluss E2) |
| Steuern auf Kapitalerträge (nicht veranlagte Steuern vom Ertrag, Abgeltungsteuer) | 56,1 Mrd. € | Position Kapitalerträge: 1,38 % BIP |
| **zusammen** | **170,4 Mrd. € = 3,76 % BIP** | **3,77 % BIP** |

Quelle für heute: BMF-Datensammlung zur Steuerpolitik 2026 nach sozialpolitik-aktuell, Tabelle II.8. Das ist eine Sekundärquelle; die Werte für 2025 sind geschätzt.

**Einordnung.**
- Laut OECD lag der Anteil der Steuern auf Unternehmensgewinne am gesamten Steueraufkommen 2022 in Deutschland bei 6 %, im OECD-Mittel bei 12 %.
- Bei einer Steuerquote von rund 39 % sind das in Deutschland rund 2,4 % BIP. Diese Umrechnung habe ich selbst vorgenommen.
- Die frühere Modellzahl von 4,42 % hätte fast eine Verdopplung gegenüber heute bedeutet. Belegt war sie nicht (B23, B-1).

**Hebel, um die Position zu erhöhen:**

| Hebel | Wirkung | Bemerkung |
|---|---|---|
| Fall „hoch“ der Unternehmensbasis: Kundenort voll, Gewinnverlagerung voll angerechnet | +0,41 % BIP (2,80 %), etwa +21 € Dividende | Rechtsrisiko bei Doppelbesteuerungsabkommen; Säule 1 der OECD ist nicht in Kraft |
| Personengesellschaften in die Position Unternehmen | 0 (Umbuchung, +0,98 Punkte dort, −0,98 bei Einkommen) | nur Darstellung |
| Gewinn aus dem Abschluss als Basis (E1) | gering | Gewinn aus dem Abschluss ≈ steuerliche Basis (270 gegen 306 Mrd. €, 2023) |
| Satz über ein Drittel | nicht gewollt | widerspricht der Regel „höchstens ein Drittel“ |

**Empfehlung:**
- Die Position so belassen.
- In Texten den Vergleich „neu 3,77 % gegen heute 3,76 % BIP“ nennen, damit die Zahl nicht als Senkung gelesen wird.
- Der Fall „hoch“ bleibt ein Ziel für Verhandlungen über den Kundenort, aber kein Rechenwert.

## 4 Plattformsteuern: Wo sie stehen

- **In der Position Unternehmen**, im Hebel „Kundenort und Plattformen“ (`unternehmensbasis.json`, `faelle.mittel.basis_mrd.h1_kundenort_plattformen`). Dieser Hebel umfasst eine Basis von 37 Mrd. €.
  - Davon entfallen auf Plattformen 0,06 % BIP, rund 2,9 Mrd. € Aufkommen 2028 (`plattformen33.json`, Fall mittel).
  - Regel (Beschluss 15.11.2026): Der Konzerngewinn wird nach dem Umsatz am Ort der Nutzung verteilt, darauf ein Drittel. Als Untergrenze gilt ein Drittel auf 10 % des Umsatzes am Nutzungsort, also 3,3 % des Umsatzes.
- **In der Mehrwertsteuer:** Elektronische Leistungen sind schon heute am Ort des Kunden steuerpflichtig.
- **Warum der Betrag klein ist:** Die Umsätze großer Plattformen mit Nutzern im Land liegen bei rund 0,9 % BIP. Das ist aus dem Aufkommen der Digitalsteuern in Frankreich zurückgerechnet und eine Sekundärquelle. Selbst eine Umsatzabgabe von 5 % brächte nur rund 0,05 % BIP, etwa 2 € Dividende.
- Gewinne aus Automatisierung fließen über die Unternehmens- und Kapitalertragsbesteuerung in die Dividende, nicht über eine eigene Plattformsteuer.

## 5 Importe: Wie sie behandelt werden

| Steuer | Importe | Exporte |
|---|---|---|
| Mehrwertsteuer-Label | wie inländische Waren (Einfuhrumsatzsteuer, Bestimmungslandprinzip); Teil der Position Konsum | steuerfrei |
| Sonderstufe ein Drittel (Kraftstoffe, Alkohol, Tabak, Pestizide, Dünger) | gilt auch für eingeführte Waren | steuerfrei |
| Zölle | Einnahme der EU, nicht des Staates (Korrektur 91) | – |
| Unternehmen | Gewinne ausländischer Anbieter mit Kunden im Land über den Kundenort (Abschnitt 3) | Gewinn nach dem Anteil der Kunden im Inland |
| CO₂ | nicht im CO₂-Preis enthalten. Das CO₂-Grenzausgleichssystem der EU (CBAM, seit 2026 für Stahl, Zement, Aluminium, Dünger, Wasserstoff, Strom) wird von der EU erhoben; nach dem Vorschlag zu den Eigenmitteln fließt sein Ertrag größtenteils an die EU (nach eigenem Kenntnisstand; an der Quelle zu prüfen) | – |

Das Label belastet Importe nach ihrer Stufe. CO₂-intensive Importe lassen sich deshalb über die Einstufung im Label erfassen, auch ohne nationalen Grenzausgleich.

## 6 CO₂: Wie die Rechnung es heute abbildet und was strenger möglich ist

**Heutige Abbildung (`deckung_belegt.json`, `einnahmen_belege.toml`):**
- Menge: bepreiste Emissionen 2025 von 578 Mt (EU-ETS 1 284 Mt, nationaler Emissionshandel 294 Mt). Sie sinken um 3 % je Jahr (Annahme) auf 528 Mt im Jahr 2028.
- Preis: 100 €/t (Regel des Konzepts, nominal).
- Aufkommen: 1,07 % BIP 2028. Danach sinkt es mit den Emissionen auf 15 % des Werts von 2028 im Jahr 2060 (`projektion33.toml`, Setzung).
- Zum Vergleich die Erlöse 2025: 21,4 Mrd. € = 0,47 % BIP, davon EU-ETS 5,4 Mrd. € (73,86 €/t) und nationaler Emissionshandel 16 Mrd. € (55 €/t).

**Befund 1: Die Position ist zu hoch.**
- Für den EU-ETS 1 erhielt Deutschland 2025 Erlöse für nur rund 26 % der Mengen (5,4 Mrd. € / 73,86 €/t = 73 Mt von 284 Mt).
- Der Rest wird frei zugeteilt oder fließt in Fonds der EU. Die Rechnung setzt dagegen alle Mengen an.

**Befund 2: In den Haushalten fehlen die CO₂-Kosten.**
- Die Haushaltsrechnungen (Haushaltsbeispiele, Mikrosimulation, Rentner) enthalten keine CO₂-Kosten, weder heute noch neu.
- Die Mehrlast gegenüber 2025 beträgt in der geltenden Rechnung 0,6 % BIP.
- Für Erwerbstätige fließt sie größtenteils über die Dividende zurück, für Rentner nicht. Grob geschätzt bedeutet das −41 € je Rentnerhaushalt.

**Varianten.**
- Mengen 2028: EU-ETS 1 259 Mt, nationaler Emissionshandel bzw. ETS 2 268 Mt.
- Mengenreaktion auf den Preis mit der Elastizität −0,3 (Annahme nach Labandeira u. a. 2017).
- Rentnerlast: grobe Ableitung aus der Wirkung des Labels; die Last wird so verteilt angenommen wie beim Label.

| Variante | bezahlte Menge | Aufkommen | gegen geltend | Dividende | Mehrlast gegen 2025 | Rentner (grob) |
|---|---|---|---|---|---|---|
| K0 geltend (alle Mengen × 100 €/t) | 527 Mt | 1,07 % BIP | – | – | 0,60 % BIP | −41 € |
| K1 berichtigt (nur bezahlte Mengen) | 341 Mt | 0,69 % | −0,38 | −20 € | 0,22 % | −15 € |
| **K2 K1 + nationale Abgabe auf frei zugeteilte Mengen, 100 €/t** | **481 Mt** | **0,98 %** | **−0,09** | **−5 €** | **0,51 %** | **−34 €** |
| K3 wie K2, 150 €/t | 426 Mt | 1,30 % | +0,23 | +12 € | 0,83 % | −56 € |
| K4 wie K2, 200 €/t | 390 Mt | 1,59 % | +0,52 | +27 € | 1,12 % | −76 € |
| K5 K2 + Landwirtschaft (Methan, Lachgas), 100 €/t | 528 Mt | 1,07 % | 0,00 | 0 € | 0,60 % | −41 € |

- Zur nationalen Abgabe in K2: 75 % der frei zugeteilten Mengen werden erfasst; der Rest bleibt wegen Wettbewerb und Abwanderung ausgenommen (Annahme). Vorbilder sind die CO₂-Abgabe der Industrie in den Niederlanden und der Mindestpreis im Vereinigten Königreich.
- Zum Vergleich: Das Umweltbundesamt setzt Klimakosten von 300 €/t an (2024, Preise 2024; mit reiner Zeitpräferenz 0 % 880 €/t).

**Empfehlung:**
1. **K2 beschließen.** Dann bleibt die Position mit 0,98 % BIP fast erhalten (−5 € Dividende statt −20 € bei K1). Die nationale Abgabe und ein Preis über der Preisbremse des ETS 2 sind rechtlich zu prüfen (P1).
2. **K3 (150 €/t) nur zusammen mit dem Altersausgleich R4,** der dann um die CO₂-Last erhöht wird. Sonst steigt der Verlust der Rentner um weitere rund 20 €.
3. **Landwirtschaft eher über die Sonderstufe des Labels** (Dünger, Pestizide; tierische Produkte prüfen) als über einen eigenen Preis; K5 zeigt nur die Größenordnung.
4. **CO₂-Kosten in die Haushaltsrechnungen aufnehmen** (heute gegen neu), bevor Ergebnisse zur Verteilung veröffentlicht werden.

## 7 Zu entscheiden

1. Rentner: Altersausgleich R4 (55 € je Person, 0,23 % BIP), allein oder mit R3?
2. CO₂: K2 (nationale Abgabe auf frei zugeteilte Mengen), K1 (nur berichtigen) oder K3 (150 €/t mit höherem Altersausgleich)?
3. Sollen die CO₂-Kosten in alle Haushaltsrechnungen aufgenommen werden? Empfohlen; die Werte zur Verteilung sinken dadurch etwas.
4. Unternehmen: die Position belassen und den Vergleich mit heute in den Texten nennen?

## Quellen

- BMF-Datensammlung zur Steuerpolitik 2026 nach sozialpolitik-aktuell, Tabelle II.8 (Sekundärquelle; 2025 geschätzt).
- OECD, Revenue Statistics 2024, Länderblatt Deutschland: https://www.oecd.org/tax/revenue-statistics-germany.pdf (Anteile 2022; maschinell gelesen, an der Quelle zu prüfen).
- OECD, Pressemitteilung vom November 2025 zu den Unternehmenssteuereinnahmen (Mittel aus 131 Staaten 2022: 3,6 % BIP; andere Staatengruppe als das OECD-Mittel): https://www.oecd.org/en/about/news/press-releases/2025/11/corporate-tax-revenues-rise-as-global-corporate-tax-rates-continue-to-stabilise-new-oecd-data-show.html
- ZfK nach UBA/DEHSt, Erlöse des Emissionshandels 2025 (Sekundärquelle der amtlichen Mitteilung): https://www.zfk.de/politik/deutschland/emissionshandel-21-4-milliarden-klimafonds-2025
- Umweltbundesamt, Methodenkonvention 3.2, Empfehlung Klimakosten (26.11.2024): https://umweltbundesamt.de/sites/default/files/medien/384/bilder/dateien/6_tab_uba-empfehlung-klimakosten_2024-11-26.pdf
- Labandeira, Labeaga, López-Otero (2017): A meta-analysis on the price elasticity of energy demand, Energy Policy 102 (eigene Kenntnis, Werte an der Quelle zu prüfen).
- Rechnungen des Projekts: `unternehmensbasis.json`, `plattformen33.json`, `deckung_belegt.json`, `rentner_eichung.json`, `co2_varianten.json`.
