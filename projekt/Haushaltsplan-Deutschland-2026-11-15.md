# Haushaltsplan Deutschland: heute und im Goldenen Drittel

Initiative 28:28 · 15. November 2026 · Modellstand v4.94 · Rechnung: `modell/haushaltsplan_de.py` (+ `.toml`) → `daten/aggregate/haushaltsplan_de.json`;
Seite mit Flussbildern: `dokumente/werkzeuge/haushaltsplan_seite.py` (Artefakt, privat).
Status: **Prüfrechnung.** Die Spalte „belegt“ ist intern (Prüfbefund B-1, Beschluss 15.11.2026).

**Abgrenzung.** Gesamtstaat (Bund, Länder, Gemeinden, Sozialversicherung).
- Heute: Ist 2024 nach Eurostat (vorläufig), BIP 4.386,9 Mrd. €.
- Nachher: geltende Rechnung 2028, BIP 4.914,9 Mrd. € nominal.
- Die Zuordnung heutiger Positionen zu den neuen ist eigene Arbeit (Annahme). Die deutschen Steuernamen zu den Eurostat-Kategorien sind eigene Kenntnis.
- Nicht enthalten: die private Pflichtvorsorge (4,1 % BIP, eigenes Konto).

## 1 Einnahmen nach Steuer- und Abgabenart

| Position heute → nachher | heute Mrd. € 2024 | heute % BIP | Drittel 2028 % BIP | Drittel 2028 Mrd. € | belegt (intern) % BIP | Einfluss der neuen Regeln |
|---|---|---|---|---|---|---|
| **Steuern** | | | | | | |
| Lohn- und Einkommensteuer, Soli (Haushalte), sonstige Einkommensteuern → *Einkommen* | 411,7 | 9,38 | 10,21 | 501,8 | – | Ein Tarif 0/11/19/25/33 % auf alle Einkommen einschließlich Dividende und Gewinnen der Personengesellschaften; Grundbedarf frei; keine Abzüge; Soli entfällt |
| darin heute: Kapitalertrag- und Abgeltungsteuer → *Kapitalerträge* | – | – | 1,37 | 67,3 | – | Kapitalerträge einschließlich Kursgewinnen höchstens 33 % (heute 26,375 %); je Einkommensart ein Drittel |
| Körperschaft- und Gewerbesteuer (Kapitalgesellschaften) → *Unternehmen und Plattformen* | 125,1 | 2,85 | 4,42 | 217,2 | 2,37 | Unternehmen 33 % auf den Konzerngewinn, verteilt nach Kundenumsatz; Plattformen mit Untergrenze; Gewerbesteuer entfällt (Gemeinden über feste Anteile); Altverluste 5 Jahre, Verrechnung über 1 Mio. € höchstens 50 % |
| Mehrwertsteuer → *Konsum (Label)* | 298,8 | 6,81 | 8,51 | 418,3 | – | Label 5/11/17/25 % nach Wirkung auf Gesundheit und Umwelt, Sonderstufe 33 % (Alkohol, Tabak, Kraftstoffe, Fahrzeuge 31 %); effektiv 18,8 % (heute 19/7 %) |
| Verbrauchsteuern (Energie, Strom, Tabak, Alkohol, Kaffee), Versicherung-, Grunderwerb- und Verkehrsteuern, Kfz-Steuer, übrige → *Übrige Steuern* | 126,8 | 2,89 | 3,93 | 193,2 | 3,26 | Weitgehend wie heute (Annahme der Gesamtrechnung); Lenkung über die Sonderstufe im Label. Im Modellwert steckt der Emissionshandel ein zweites Mal (Prüfbefund B-1) |
| Emissionshandel (Abgaben auf Verschmutzung) → *CO₂-Preis* | 18,6 | 0,42 | 1,67 | 82,1 | 1,36 | CO₂-Preis 100 €/t auf alle bepreisten Emissionen, Pfad bis 150 €/t; sinkt mit den Emissionen |
| Grundsteuer → *Grundstücksabgabe* | 16,2 | 0,37 | 0,82 | 40,3 | – | Bodenwertabgabe bis 1 % des Bodenwerts (Gemeinden) |
| Erbschaft- und Schenkungsteuer → *Erbschaften* | 10,0 | 0,23 | 1,16 | 57,0 | 0,97 | 33 % auf Erwerbe über 100.000 € je Erbe, ohne Verschonung von Betriebsvermögen (heute bis 50 %, viele Ausnahmen) |
| Vermögensteuer (seit 1997 nicht erhoben) → *Große Vermögen* | 0,0 | 0,00 | 0,97 | 47,7 | – | Mindeststeuer (anrechenbar) und 1 % ab 2 Mio. € |
| Abbau klimaschädlicher Subventionen (heute Ausgabe oder Steuervergünstigung) → *Subventionsabbau* | – | – | 0,48 | 23,6 | – | 20 Mrd. € nach UBA-Liste; im Modell als Einnahme geführt |
| Progression und Dynamik (2028) | – | – | 0,07 | 3,4 | – | Mehraufkommen aus dem Tarif bei wachsenden Einkommen und erwarteter Dynamik |
| **Sozialbeiträge** | | | | | | |
| Beiträge der Arbeitgeber | 302,4 | 6,89 | 0,00 | 0,0 | – | entfallen: Arbeit wird um diesen Betrag billiger |
| Beiträge der Arbeitnehmer | 280,1 | 6,39 | 0,00 | 0,0 | – | entfallen; Gesundheit und Netz aus Steuern |
| Beiträge Nichterwerbstätiger, Selbständiger, freiwillige | 126,1 | 2,87 | 0,00 | 0,0 | – | entfallen |
| unterstellte Beiträge (Beamtenversorgung) | 48,2 | 1,10 | 0,00 | 0,0 | – | entfallen; laufende Pensionen als Altlast über den Fonds |
| **Fonds** | | | | | | |
| – → *Fondsbeitrag* | – | – | 4,90 | 240,8 | – | Beitrag zum gemeinsamen Fonds für Altrenten und Altschulden (Zuschlag 14,6 % auf alle Steuern, DE 2028), bis 2098 |
| **Kredit** | | | | | | |
| Neue Schulden (Defizit) → *Fondsanleihen* | 115,3 | 2,63 | 5,29 | 260,0 | – | Laufender Haushalt ausgeglichen (Saldo +0,11); Fondsanleihen für den Teil der Altlast über dem Beitrag, getilgt bis 2098 |
| **Übrige Einnahmen** | | | | | | |
| Verkäufe, Gebühren, Vermögenserträge, Transfers | 260,5 | 5,94 | – | – | – | im Modell nicht gesondert: Ausgaben der Gemeinden und des Dachs netto nach Gebühren (Annahme) |
| **Summe** | | **48,77** | **43,80** | **2.152,7** | | |

## 2 Ausgaben nach Aufgaben

| Position heute → nachher | heute Mrd. € 2024 | heute % BIP | Drittel 2028 % BIP | Drittel 2028 Mrd. € | belegt (intern) % BIP | Einfluss der neuen Regeln |
|---|---|---|---|---|---|---|
| **Verwaltung** | | | | | | |
| Allgemeine Verwaltung, Außenbeziehungen (COFOG 01 ohne Zinsen und Grundlagenforschung) | 185,5 | 4,23 | 2,22 | 109,1 | – | Kommunalverwaltung 1,62 + Außenbeziehungen 0,30 + Standards 0,30; einfaches System, Verwaltung der Sozialversicherung (heute rund 1,1 % BIP) entfällt |
| Zinsen auf Altschulden → *Fonds: Zinsen* | 49,3 | 1,12 | 1,04 | 51,1 | – | über den Fonds (Altlast), nicht aus dem laufenden Haushalt |
| **Sicherheit** | | | | | | |
| Verteidigung | 58,6 | 1,34 | 1,40 | 68,8 | – | Pfad bis 2,5 % BIP 2035 (Verteidigung und digitale Souveränität, gemeinsam) |
| Öffentliche Ordnung und Sicherheit | 70,7 | 1,61 | 1,34 | 65,9 | – | übergeordnete Polizei 0,29 + Ordnung, Feuerwehr, Rettung 0,05 + 1,0 (Gemeinden); Gerichte und Vollzug in der Zuordnung nicht getrennt (Annahme) |
| **Wirtschaft** | | | | | | |
| Wirtschaft, Verkehr, Energie, Landwirtschaft | 234,6 | 5,35 | 3,58 | 176,0 | – | Wirtschaftsraum, Agrar, Energie, Netze 2,10 + Nahverkehr und Ortsstraßen 1,48; klimaschädliche Subventionen abgebaut |
| **Umwelt** | | | | | | |
| Umweltschutz, Wasser, Abwasser, Abfall | 24,5 | 0,56 | 0,86 | 42,3 | – | grenzüberschreitend 0,29 + Gemeinden 0,57 (netto nach Gebühren) |
| **Gemeinwesen** | | | | | | |
| Wohnen und kommunale Einrichtungen | 20,5 | 0,47 | 0,71 | 34,9 | – | Gemeinden |
| **Gesundheit** | | | | | | |
| Gesundheit | 329,3 | 7,51 | 7,36 | 361,7 | – | Grundversorgung für alle aus Steuern; keine Krankenkassenbeiträge |
| **Kultur** | | | | | | |
| Freizeit, Sport, Kultur, Religion | 46,0 | 1,05 | 1,22 | 60,0 | – | Gemeinden |
| **Bildung** | | | | | | |
| Schulen (Vorschule bis Sekundarstufe) | 132,0 | 3,01 | 3,70 | 181,9 | – | Gemeinden, Schulen 3,70 |
| Hochschulen, Grundlagenforschung, übrige Bildung | 105,8 | 2,41 | 1,51 | 74,2 | – | Hochschulen 0,74 + Grundlagenforschung 0,77 (Dach) |
| **Soziale Sicherung** | | | | | | |
| Alter und Hinterbliebene (Renten, Pensionen) → *Fonds: Altrenten über der Dividende* | 508,1 | 11,58 | 9,15 | 449,7 | – | Alte Ansprüche über der Dividende als Altlast über den Fonds; neue Ansprüche: Dividende und Pflichtvorsorge (eigenes Konto, 4,1 % BIP, privat) |
| Krankheit und Invalidität (Krankengeld, Pflege, Erwerbsminderung) | 143,9 | 3,28 | 1,14 | 56,0 | – | Pflege (Teilkasko) 0,85 + Invalidität (Grundbedarf) 0,29 |
| Arbeitslosigkeit | 71,7 | 1,64 | 0,41 | 20,2 | – | Grundbedarf; die Dividende trägt mit |
| Familie und Kinder, Wohnen, Grundsicherung, übrige | 159,4 | 3,63 | 0,70 | 34,4 | – | Waisen 0,05 + Härtefall 0,65; Kindergeld, Wohngeld und Grundsicherung gehen in der Dividende auf |
| **Dividende** | | | | | | |
| – (neu) → *Dividende* | – | – | 7,34 | 360,8 | 3,74 | Transformationsdividende für alle Erwachsenen, halb für Kinder; DE 2028 384 € je Erwachsenem und Monat (Kaufkraft 2026) |
| **Summe** | | **48,79** | **43,68** | **2.146,8** | | |

**Fonds.** Altlast Deutschland 2028: 10,19 % BIP.
- Davon Zinsen 1,04: Quote 2024, Annahme.
- Der Rest sind Altrenten über der Dividende.
- Getragen von Fondsbeitrag (4,90) und Fondsanleihen (5,29), getilgt bis 2098.

## 3 Wohin die Dividende geht (geltend, % BIP)

| Schritt | % BIP |
|---|---|
| Dividende 2028 | 7,34 |
| Verteidigung bis 2,5 % (2035) | -1,10 |
| CO₂-Preis sinkt mit den Emissionen | -1,42 |
| Verbrauchsteuern sinken | -0,81 |
| Label: weniger schädlicher Konsum | -0,42 |
| Netz: Alterung (Pflege, Grundrente, Gesundheit) | -1,31 |
| Progression (Einkommen wachsen real) | +1,26 |
| **Dividende 2060** | **3,55** |
| belegt (intern), mittlerer Fall, Dividende 2060 | -0,10 |

Euro je Erwachsenem und Monat, Kaufkraft 2026:
- geltend: 384 / 309 / 261 / 256 € (2028 / 2035 / 2045 / 2060);
- belegt, mittlerer Fall: 195 / 108 / 43 / -7 €.

## 4 Was in der Rechnung fehlt: Automatisierung und Erbe (erste Abschätzung, nicht durch die Kette gerechnet)

Unternehmensgewinne, Kapitalerträge und Erbschaften stehen im Modell als fester Anteil am BIP. Die beiden Entwicklungen, die die Initiative nennt,
sind darin nicht abgebildet.

**Automatisierung.** Verschiebt sich Einkommen von Arbeit zu Gewinnen, gewinnt das Drittel:
- Gewinne tragen 33 % beim Unternehmen und ausgeschüttet noch einmal 33 % beim Empfänger.
- Arbeitseinkommen tragen im Tarif 0 bis 33 %, im Mittel rund 19 % (Annahme).
- Ein Punkt BIP, der von Arbeit zu Gewinnen wandert, bringt daher rund +0,25 Punkte (bei hälftiger Ausschüttung; Ableitung).
- Bei −3 Punkten Lohnquote bis 2045 (Annahme; eine amtliche Projektion liegt nicht vor) wären das rund +0,75 Punkte.
- Anders als die heutigen Sozialbeiträge hängt das Drittel nicht an der Lohnsumme.

**Erbe.** Erbschaften und Schenkungen werden auf bis zu 400 Mrd. € je Jahr geschätzt (DIW und WSI 2017, Böckler Impuls 12/2017; Projektion bis
2027, Datengrundlage SOEP 2012; eine Studie, Auftraggeber Stiftung). Die Statistik erfasst davon 113 bis 150 Mrd. € (Destatis 2022–2025).
- Wächst das vererbte Vermögen schneller als das BIP (Babyboomer), steigt die Position Erbschaften.
- Annahme: +0,2 bis +0,4 Punkte bis 2045.
- Der Satz liegt mit 33 % schon an der Grenze des Drittels.

**Zusammen** wären das rund +1 Punkt um 2045. Das entspricht etwa der Ergänzung, die die Vorlage E5 (Option A+) als Ziel nennt. Die Werte sind zu
belegen und durch die Kette zu rechnen.

## 5 Prüfpunkte

- **Korrektur 91:** Zölle (5,5 Mrd. €) sind Eigenmittel der EU und keine Einnahme des Landes. Sie standen in der belegten Position „Übrige“ (v4.87).
  Übrige belegt jetzt 3,26 statt 3,39 % BIP; Lücke B-1 −3,22 statt −3,09.
- **Grundsteuer:** Steht sie zugleich in „Übrige“ (Kernmodell 165 Mrd.) und in der Grundstücksabgabe (0,82)? Im Kernmodell heißt der Baustein
  „Bodenwertabgabe statt Grundsteuer“ (+20 Modell-Mrd.). Möglich ist eine Überschneidung bis 0,37 % BIP; zu klären.
- **Gebühren und Entgelte** (heute 5,9 % BIP): Das Modell rechnet die Ausgaben von Gemeinden und Dach netto. Belegt ist das nicht.

## Quellen

- Eurostat gov_10a_taxag, gov_10a_exp (COFOG), gov_10a_main; Deutschland 2024, vorläufig; abgerufen 15.11.2026.
- Hans-Böckler-Stiftung, Böckler Impuls 12/2017: Erbschaften größer als bislang erwartet (Studie von DIW und WSI). https://www.boeckler.de/de/boeckler-impuls-erbschaften-groesser-als-bislang-erwartet-3761.htm
- DIW, Blogbeitrag vom 26.5.2026 (KI und Verteilung; nennt keine Lohnquote; Sekundärquelle). https://www.diw.de/de/diw_01.c.1008994.de/nachrichten/wenn_ki_zur_gefahr_fuer_die_mittelschicht_wird.html
