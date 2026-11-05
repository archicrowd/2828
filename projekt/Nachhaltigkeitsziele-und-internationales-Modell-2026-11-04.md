# Nachhaltigkeitsziele der UN und Weg zu einem internationalen Modell

Initiative 28:28 · 4. November 2026 · Modellstand v4.67, Nachtrag v4.72 · Arbeitspapier (Rechnung: `modell/sdg_kennzahlen.py`)

## 1 Entscheidung: Pestizide und mineralische Dünger in der Sonderstufe 33 %

Beschluss der Initiative (4.11.2026): chemische Pflanzenschutzmittel und mineralische Dünger gehören ausdrücklich zur Sonderstufe S 33 %.
Umgesetzt im Konzept (Abschnitt Konsum) und im Working Paper (Tabelle 13, Abschnitt 7).

**Was das bewirkt und was nicht.** Die Mehrwertsteuer ist eine Steuer auf den Endverbrauch. Landwirtschaftliche Betriebe ziehen sie als
Vorsteuer ab; für sie ändert die Sonderstufe den Preis nicht. Sie wirkt beim privaten Kauf (Haus und Garten) und bei Betrieben ohne
Vorsteuerabzug (in Deutschland pauschalierende Landwirte nach § 24 UStG, Größenordnung nicht geprüft). Die Rechnung bewegt sich nicht: Der
Anteil dieser Käufe am Konsum der Haushalte ist klein und nicht beziffert.

**Vorschlag (offen): Lenkungsabgabe für die berufliche Verwendung**, nach der Schädlichkeit gestaffelt, Vorbild Dänemark. Dort gilt seit 2013
eine Abgabe nach dem Indikator „Pesticide Load“ (Gesundheit, Ökotoxizität, Verbleib in der Umwelt); die Belastung nach Absatz fiel 2011–2021
um 46 %, die Ursache ist aber nicht allein der Abgabe zuzuschreiben (Nordischer Ministerrat, TemaNord 2025:523). Größenordnung für
Deutschland: Inlandsumsatz Pflanzenschutzmittel 2024 rund 1,22 Mrd. € (Industrieverband Agrar, Verbandsangabe, Sekundärquelle). Eine
Abgabe von einem Drittel des Werts brächte vor Verhaltensänderung rund 0,4 Mrd. € (Überschlag, ≈ 0,01 % des BIP, unter 1 € je
Erwachsenem und Monat). Die Abgabe ist ein Lenkungs-, kein Finanzierungsinstrument; in Dänemark fließt das Aufkommen weitgehend an die
Landwirtschaft zurück. Zu entscheiden: Abgabe ja/nein; Rückgabe über die Dividende oder an die Betriebe; Dünger einbeziehen.

## 2 Kennzahlen der UN-Ziele, gerechnet (2028, statisch)

Verfahren wie beim Gini (Rekonstruktion aus EU-SILC-Dezilen, Abbildung heute → neu). Hauptvariante: Rentnerhaushalte (ein Viertel)
unverändert. Die Variante, die alle wie Erwerbstätige abbildet, ist eine obere Grenze der Wirkung, weil Rentner im Modell verlieren
(Deutschland im Mittel −121 € im Monat).

| Land | Armutsquote 2025 (amtlich*) | 2028 relativ | 2028 verankert | untere 40 % | alle |
|---|---|---|---|---|---|
| Deutschland | 16,1 % | 16,7 % | 10,5–13,1 % | +27 bis +28 % | +18 % |
| Frankreich | 16,3 % | 14,7 % | 9,5–10,9 % | +10 bis +11 % | +10 % |
| Italien | 18,6 % | 14,3 % | 6,2 % | +32 % | +20 % |
| Spanien | 19,5 % | 13,4 % | 7,7–9,8 % | +30 bis +31 % | +15 % |
| Polen | 13,2 % | 8,0 % | 3,3 % | +36 % | +20 % |

\* Eurostat ilc_li02 (EU-SILC 2025) über eupublicdata.eu – Sekundärquelle, an der Eurostat-Schnittstelle zu prüfen.

- **SDG 1.2 (Armutsgefährdung, 60 % des Medians):** Relativ sinkt die Quote in Frankreich, Italien, Spanien und Polen deutlich, in **Deutschland
  nicht** (16,1 → 16,7 %). Grund: Erwerbstätige gewinnen, der Median steigt, unveränderte Rentnerhaushalte fallen unter die neue Grenze. Da Rentner
  tatsächlich verlieren, ist die Quote für Deutschland eher höher. Verankert an der heutigen Grenze sinkt sie überall.
- **SDG 10.1 (untere 40 % wachsen schneller als der Durchschnitt):** in allen fünf Ländern erfüllt, in Frankreich knapp (+10 bis +11 % gegen +10 %).
- **Grenzen:** statisch, ohne Preisniveauschub (1,2–2,1 %), ohne Kapitaleinkommen; Rentner nur als unveränderte Gruppe, nicht mit ihren Verlusten.
  Für Deutschland wäre die Mikrosimulation mit Rentnerhaushalten die bessere Grundlage (nächster Schritt).

**Nachtrag v4.72 (Mikrosimulation Deutschland mit Rentnerhaushalten, Regel BS35):** Modellquote heute 18,3 % (amtlich 16,1 %), neu relativ
18,1 %, verankert 12,5 %. Rentner: heute 22,3 %, neu relativ 30,3 %, verankert 20,3 % (unter E 30,8 / 20,8 %). Erwerbsfähige: 17,1 → 14,7 / 10,3 %.
Untere 40 % +13,6 % gegen alle +10,8 % (SDG 10.1 erfüllt). Die Rentnerregel bewegt die Quote kaum; sie wirkt in der Mitte und oben. Die relative
Quote der Rentner steigt, weil ihr Boden (Grundsicherung) unter der neuen Schwelle von 60 % des gestiegenen Medians liegt.

**Folgerung (bis v4.71):** Für SDG 1 ist die Rentnerregel E die Schwachstelle. Eine Armutsquote, die bei Rentnern steigt, widerspricht dem Ziel; zu prüfen ist
ein höherer Boden für Rentner oder eine Kürzung erst oberhalb eines höheren Betrags.

## 3 Globale Teilziele

**Berichtigung:** In der Durchsicht vom 4.11.2026 hatte ich Teilziel 10.c als „Ungleichheit zwischen Ländern“ genannt. 10.c betrifft die
Kosten von Rücküberweisungen von Migrantinnen und Migranten (unter 3 %). Unser Konzept berührt es nicht. Für die Ungleichheit zwischen Staaten
einschlägig sind 10.4 (Fiskalpolitik für mehr Gleichheit), 17.1 (Mobilisierung eigener Einnahmen) und 17.2 (öffentliche Entwicklungsleistungen).

- **17.1 – eigene Einnahmen stärken:** Das Regelwerk ist einfach und an den Grundbedarf jedes Staates gebunden; es ließe sich als Vorlage für
  Staaten mit schwacher Steuerverwaltung nutzen. Gegenläufig: Besteuerung am Ort der Kunden verlagert Steuerbasis zu den Absatzmärkten. Für
  exportierende Staaten mit niedrigem Einkommen kann das Einnahmen kosten (in der Literatur zur Bestimmungslandbesteuerung diskutiert; für
  unser Modell nicht gerechnet).
- **17.2 – Entwicklungsleistungen 0,7 % des Bruttonationaleinkommens:** Die Gesamtrechnung führt „Außenbeziehungen“ mit 0,30 % des BIP
  (`gesamtrechnung.json`, Tabelle A; für Stand C übernommen – zu prüfen). Das liegt unter dem Ziel. 2025 sind die Entwicklungsleistungen der
  OECD-Geber nach vorläufigen Zahlen real um 23,1 % gesunken (OECD, Pressemitteilung April 2026).
  **Vorschlag (offen): Entwicklungsbaustein** als gemeinsame Regel der Staatengruppe: mindestens 0,7 % des BNE, davon 0,15–0,20 % an die am
  wenigsten entwickelten Länder; vorrangig für Aufbau von Steuerverwaltungen (17.1) und für Staaten, die durch die Besteuerung am Ort der Kunden
  Einnahmen verlieren. Größenordnung: zusätzlich rund 0,4 BIP-Punkte; aus der Dividende finanziert wären das in Deutschland 2028 rund 20 € je
  Erwachsenem und Monat (Überschlag: 0,4 / 7,25 × 354 €; nicht gerechnet).
- **10.c:** nicht berührt (s. o.).

## 4 Vom europäischen zum internationalen Modell: Staaten, die Standards sichern

**Was schon trägt.** Die Regeln sind nicht an Europa gebunden: Tarifstufen am Grundbedarf jedes Staates, Dividende aus den eigenen
Einnahmen, Netz und Grundauskommen je Land. Bisher entwickelt (v4.55–v4.57): Auswahl nach Rechtsstaatlichkeit statt Geografie; auf dem WJP Rule
of Law Index 2025 liegen Australien, Kanada, Neuseeland, das Vereinigte Königreich und Japan auf der Höhe der stärksten europäischen Staaten.
Offen geblieben: die Schwellen 0,75 (Kern) und 0,66 (Kandidaten).

**Vorschlag für die Standards einer Teilnahme** (Kriterien prüfbar, Datenquellen öffentlich):

| Nr. | Standard | Maß | Quelle |
|---|---|---|---|
| S1 | Rechtsstaat | Rule of Law Index ≥ 0,75 (Kern) bzw. ≥ 0,66 | World Justice Project |
| S2 | Steuertransparenz | Informationsaustausch auf Ersuchen mindestens „largely compliant“; automatischer Austausch (CRS) in Kraft | OECD Global Forum |
| S3 | Rechenbarkeit | Einkommensverteilung (Dezile), Steuer-Abgaben-Modell, Gesamtrechnung, Rentenzusagen verfügbar | OECD Taxing Wages, OECD Income Distribution Database, LIS |
| S4 | Arbeits- und Sozialstandards | ILO-Kernübereinkommen ratifiziert | ILO NORMLEX |
| S5 | Klima | CO₂-Preis oder verbindlicher Pfad; NDC nach Paris | nationale Angaben, World Bank Carbon Pricing Dashboard |
| S6 | Entwicklungsbeitrag | 0,7 % des BNE (Übergangsfrist) | OECD DAC |

**Was das Modell dafür braucht.**
1. **Daten außerhalb Eurostats:** Rentenzusagen (Z) gibt es als Tabelle 29 nur für EU/EWR; für andere Staaten Ersatz aus OECD „Pensions at a
   Glance“ oder IMF (Lücke).
2. **Fonds über Währungen:** Ein gemeinsamer Altlastenfonds mit Staaten außerhalb des Euro trägt Wechselkursrisiko. Vorschlag: Fonds je
   Währungsraum, gemeinsame Regeln, Verrechnung nur innerhalb eines Raums (zu rechnen).
3. **Referenzländer:** zuerst Staaten mit OECD Taxing Wages und amtlichen Dezilen, z. B. Kanada, Australien, Neuseeland, Vereinigtes Königreich,
   Japan (Ländermodelle nach dem Muster FR/IT/ES/PL).
4. **Verhältnis zu Nichtmitgliedern:** Grenzausgleich der Kundenort-Besteuerung und des CO₂-Preises; Handelsrecht (offen, P1).

## 5 Zu entscheiden

1. Lenkungsabgabe Pflanzenschutz und Dünger (Abschnitt 1).
2. Rentnerregel mit Blick auf SDG 1.2 (Abschnitt 2).
3. Entwicklungsbaustein 0,7 % (Abschnitt 3).
4. Standards S1–S6 und Schwellen; erste außereuropäische Referenzländer (Abschnitt 4).

**Quellen:** Eurostat ilc_li02 über eupublicdata.eu (Sekundärquelle); Industrieverband Agrar, Pflanzenschutzmarkt 2024 (Verbandsangabe);
Nordischer Ministerrat, TemaNord 2025:523; Vereinte Nationen, Ziel 17 (sdgs.un.org/goals/goal17); OECD, Pressemitteilung „International aid
fell sharply in 2025“ (April 2026); World Justice Project, Rule of Law Index 2025.
