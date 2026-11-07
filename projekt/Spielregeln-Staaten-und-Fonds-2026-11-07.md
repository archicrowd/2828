# Spielregeln: Staaten, Regeln, geteilte Verantwortung

Initiative 28:28 · 7. November 2026 · Modellstand v4.74 · Entwicklungsmodus, vorläufig, kein Beschluss
Rechnung: `modell/staatenauswahl.py`, `modell/fonds_5050.py` · ersetzt die Vorlagen EV1–EV9 vom selben Tag in der Form, nicht im Inhalt

## Absicht

Jeder Staat wendet dieselben einfachen Regeln selbst an, gemessen an seinem eigenen Grundbedarf. Mitmachen kann jeder Staat, der die Grundlagen
der Vereinten Nationen achtet und rechtsstaatlich handelt. Die Altlasten aus Schulden und ungedeckten Rentenzusagen trägt jeder Staat zur
Hälfte selbst; die andere Hälfte tragen alle gemeinsam. Im Mittelpunkt stehen vier Ziele: gerechte Steuern, Gerechtigkeit zwischen den
Generationen, der Klimawandel und der Wandel der Arbeitswelt.

## Die fünf Spielregeln

1. **Wer mitmacht.** Mitglied der Vereinten Nationen; beide Menschenrechtspakte von 1966 ratifiziert (bürgerliche und politische Rechte; wirtschaftliche,
   soziale und kulturelle Rechte); Vertragsstaat des Pariser Klimaabkommens; Rule of Law Index mindestens 0,66.
   Wer die Grundlagen erfüllt, die Schwelle aber noch nicht erreicht, ist **Partner**. Ein Partner wendet die Regeln an und trägt seine Altlast
   ganz selbst.
2. **Dieselben Regeln, im eigenen Land.** Jeder Staat zieht seine Steuern selbst ein und rechnet in Vielfachen seines eigenen Grundbedarfs:
   - Tarif 0/11/19/25/33 %;
   - Mehrwertsteuer mit Label;
   - Dividende aus den eigenen Einnahmen;
   - starkes Netz;
   - Gemeindeformel;
   - Rentnerregel BS35.
3. **Altlasten: halb selbst, halb gemeinsam.** Jeder Teilnehmer trägt die Hälfte seiner Altlast mit dem Satz, den sein eigener Fonds bräuchte. Die
   andere Hälfte tragen alle Teilnehmer mit einem gemeinsamen Satz. Alles ist bis 2098 getilgt.
4. **Nachhaltig berichten.** Jeder Staat berichtet mindestens alle vier Jahre an das Forum der Vereinten Nationen zu den 17 Zielen (Freiwilliger
   Nationaler Bericht). Staaten mit hohem Einkommen gehen den Weg zu 0,7 % ihres Nationaleinkommens für Entwicklung.
5. **Offen und freiwillig.** Wer Regel 1 erfüllt, kann beitreten. Wer austritt, nimmt seine Altlast mit. Die Werte aller Staaten stehen öffentlich
   in einem Register und werden alle zwei Jahre neu festgestellt.

Bewusst nicht geregelt sind, wie im Auftrag vom 7.11.2026 vorgesehen: Kontrollen, Sanktionen, Schiedsverfahren und Stufen innerhalb der Teilnehmer.

## Was gegenüber dem bisherigen Konzept entfällt

| Bisher („Dach“) | Jetzt |
|---|---|
| Europäisches Dach zieht Steuern ein und behält höchstens 32 % | jeder Staat zieht selbst ein (Regel 2) |
| Dach entscheidet mit Mehrheit der Abgesandten | gemeinsam sind nur die Regeln; über sie entscheiden die Staaten |
| Kommunen erhalten ihren Anteil direkt vom Dach | Gemeindeformel als Regel in jedem Staat |
| gemeinsame Kasse für gemeinsame Aufgaben (2,65–3,09 % des BIP, v4.15) | nicht Gegenstand; diese Aufgaben bleiben beim Staat |
| Sicherheitsunion mit Anteil an der Mehrwertsteuer (v4.16) | nicht Gegenstand |
| Fonds voll gemeinsam nach 30 Jahren Verrechnung | dauerhaft 50/50 (Regel 3) |
| Auswahl nach Geografie (EU, EWR, Schweiz) | Auswahl nach Regel 1 |

**Für die Rechnung:** Der Wegfall des Dachs ändert keine Zahl der Haushalte. Dividende, Netz und Gemeindeformel entstehen nach denselben
Formeln, nur in jedem Staat. Die bisherigen Ausgaben für gemeinsame Aufgaben bleiben Ausgaben der Staaten. Neu gerechnet ist nur der Fonds.

## Der Fonds mit geteilter Verantwortung (Rechnung `fonds_5050.py`)

**Mechanismus.** Beitrag eines Teilnehmers = ½ × eigener Satz + ½ × gemeinsamer Satz, dauerhaft. Bisher galt: Der Beitrag beginnt 2028 nahe am
eigenen Satz und geht in 30 Jahren ganz auf den gemeinsamen Satz über. 50/50 heißt also: früher geteilt, aber nie ganz.

Zuschlag auf alle Steuern in % (Altlastenfonds, Tilgung bis 2098). Gemeinsamer Satz der 24 Teilnehmer: 15,5 % (alle 30: 15,4 %).

| Staat | eigener Fonds | **50/50** | bisher 2028 | bisher ab 2058 |
|---|---|---|---|---|
| Italien | 21,9 | **18,7** | 22,0 | 15,4 |
| Frankreich | 21,0 | **18,3** | 21,0 | 15,4 |
| Spanien | 18,1 | **16,8** | 18,4 | 15,4 |
| Deutschland | 14,6 | **15,1** | 15,0 | 15,4 |
| Polen | 13,4 | **14,5** | 13,7 | 15,4 |
| Niederlande | 8,6 | **12,0** | 8,3 | 15,4 |
| Dänemark | 1,5 | **8,5** | 1,3 | 15,4 |
| Griechenland (Partner) | 21,5 | **21,5** | 22,4 | 15,4 |
| Ungarn (Partner) | 11,8 | **11,8** | 11,2 | 15,4 |
| Bulgarien (Partner) | 7,3 | **7,3** | 7,5 | 15,4 |

Alle 30 Staaten stehen in `daten/aggregate/fonds_5050.json`. Für Deutschland ändert sich wenig (15,1 statt 15,0 % im Jahr 2028), weil seine
Altlast nahe am Mittel liegt. Haushalts- und Seitenrechnungen sind nicht neu gerechnet; sie nutzen weiter die geltende Verrechnung.

**Befunde:**
1. **Die Mechanik ist sichtbar.** Jeder Staat sieht zwei Zahlen: was er allein bräuchte und was alle gemeinsam brauchen. Sein Satz liegt genau
   in der Mitte.
2. **Wer wenig Altlast hat, zahlt für die Gemeinschaft.** Dänemark 8,5 statt 1,5 %, die Niederlande 12,0 statt 8,6 %. Der Ausgleich ist halb so
   groß wie bisher ab 2058 und dafür von Anfang an gleich.
3. **Partner geben und erhalten keine Solidarität.** Für Griechenland (21,5 %) ist das eine Last, für Bulgarien (7,3 %) ein Vorteil gegenüber der
   Teilnahme. Ein Anreiz, die Schwelle zu erreichen, entsteht so nur für Staaten mit hoher Altlast. Ob das gewollt ist, ist zu entscheiden (siehe
   unten, Punkt 3).
4. **Die Summe bleibt.** Bei voller Teilnahme ist das Mittel der Beiträge gleich dem gemeinsamen Satz; der Fonds wird nicht teurer.

## Staaten nach Regel 1 (erste Durchsicht)

| Ergebnis | Staaten |
|---|---|
| Teilnahme, Europa | AT, BE, CY, CZ, DE, DK, EE, ES, FI, FR, IE, IT, LT, LU, LV, MT, NL, NO, PL, PT, SE, SI, dazu CH und IS (ohne WJP-Wert, Annahme) |
| Teilnahme, außerhalb Europas | AU, BB, CA, CL, CR, JP, KR, NZ, UK, UY |
| Partner | BG, EL, HR, HU, RO, SK; MU |
| Grundlagen nicht erfüllt | US (Sozialpakt nicht ratifiziert, aus dem Pariser Abkommen ausgetreten), SG (beide Pakte nicht), BW (Sozialpakt nicht) |

**Recherchen dieses Schritts:**
- Beide Pakte am Vertragsregister der UN geprüft (MTDSG IV-3, IV-4, maschinell gelesen): Alle 30 Staaten des Fonds und alle oben genannten Staaten
  außerhalb Europas sind Vertragsstaaten beider Pakte, außer SG (keiner), US und BW (nur Zivilpakt; US hat den Sozialpakt 1977 gezeichnet).
  China hat den Zivilpakt nur gezeichnet.
- Pariser Abkommen: Austritt der USA mit Wirkung zum 27.1.2026 (Verwahrermitteilung C.N.71.2025). Für die übrigen Staaten eigene Kenntnis, zu
  prüfen.
- Rule of Law Index 2025 wie v4.73. Die zweite Quelle (Weltbank WGI) für Schweiz und Island war nicht abrufbar; die Seiten der Weltbank zeigen
  keine Werte, die Schnittstelle ist aus der Arbeitsumgebung gesperrt. Offen.

Die sieben Kernabkommen, der SDG Index und der UN-Mi werden weiter ausgewiesen, sind aber keine Regel mehr. Das hält Regel 1 einfach: Die beiden
Pakte sind der verbindliche Kern der Menschenrechte der Vereinten Nationen und fast überall ratifiziert.

## Zu entscheiden

1. **Die fünf Spielregeln** im Wortlaut. Vorgeschlagener Kernsatz: „Dieselben einfachen Regeln in jedem Land. Mitmachen kann, wer die
   Grundlagen der Vereinten Nationen achtet und rechtsstaatlich handelt. Altlasten tragen wir halb selbst und halb gemeinsam.“
2. **Schwelle 0,66 und der Anteil von 50 %**, oder ein anderer Anteil.
3. **Partner:** ganz selbst tragen (wie gerechnet), oder schon 25 % gemeinsam als Brücke. Die Brücke würde besonders Griechenland helfen.
4. **Wegfall des Dachs** in der vorgeschlagenen Liste, insbesondere der Sicherheitsunion und der gemeinsamen Kasse.
5. **Danach:** Seite, Konzept und Working Paper umstellen; Haushaltsrechnungen auf 50/50 übertragen (Zuschlag je Staat); Ländermodelle
   außerhalb Europas, zuerst UK, CA, AU, NZ, JP.

## Quellen

- UN Treaty Collection: MTDSG IV-3 (ICESCR) und IV-4 (ICCPR); C.N.71.2025 (Pariser Abkommen, Austritt der USA)
- World Justice Project, Rule of Law Index 2025
- SDSN, Sustainable Development Report 2026 (SDG Index, UN-Mi)
