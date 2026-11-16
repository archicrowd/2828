# Haushaltsplan Deutschland: heute und im Goldenen Drittel

Initiative 28:28 · 16. November 2026 · Modellstand v4.95 · Rechnung: `modell/haushaltsplan_de.py` (+ `.toml`) → `daten/aggregate/haushaltsplan_de.json`;
Seite mit Flussbildern: `dokumente/werkzeuge/haushaltsplan_seite.py` (Artefakt, privat).
> **Überholt durch v4.97 (16.11.2026):** Die Zahlen dieses Papiers stehen auf Stand v4.95 (Modellwerte, alte Regeln). Geltend sind seit v4.97 die belegten Einnahmen und die Regeln vom 16.11.2026; maßgeblich ist `daten/aggregate/haushaltsplan_de.json` (Spalte „neu“) und der Abschnitt „Wohin das Geld fließt“ der Webseite. Dividende 2028 jetzt 245 € je Erwachsenem (Kaufkraft 2026). Die Fortschreibung dieses Papiers ist offen (Logbuch 7.1, R16).

Status: **Prüfrechnung.** Die Spalte „belegt“ ist intern (Prüfbefund B-1, Beschluss 15.11.2026).
Seit v4.95 sind Aufkommen, Ausgaben und Finanzierung getrennt; der Gemeinschaftsfonds hat ein eigenes Konto (Korrektur 93).

**Abgrenzung.**
- **Heute:** Gesamtstaat (Bund, Länder, Gemeinden, Sozialversicherung), Ist 2024 nach Eurostat (vorläufig), BIP 4.386,9 Mrd. €.
- **Nachher:** Landeshaushalt Deutschland (Dach, Gemeinden, Netz) und Gemeinschaftsfonds (Anteil Deutschlands), geltende Rechnung 2028,
  BIP 4.914,9 Mrd. € nominal.
- **Zuordnung:** Die Zuordnung heutiger Positionen zu den neuen ist eigene Arbeit (Annahme). Die deutschen Steuernamen zu den Eurostat-Kategorien
  sind eigene Kenntnis.
- **Nicht enthalten:** die private Pflichtvorsorge (4,1 % BIP, eigenes Konto).

## 1 Übersicht (% BIP)

| Konto | Aufkommen | Ausgaben | Saldo | Finanzierung |
|---|---|---|---|---|
| Heute 2024: Gesamtstaat | 46,15 | 48,77 | -2,63 | neue Kredite 2,63 |
| Nachher 2028: Landeshaushalt | 38,51 (Steuern 33,61 + Altlastenzuschlag 4,90) | 38,39 (darin Beitrag an den Fonds 4,90) | +0,12 | keine |
| Nachher 2028: Gemeinschaftsfonds, Anteil DE | 4,90 (Beitrag) | 10,19 (Altrenten 9,15, Zinsen 1,04) | -5,29 | Fondskredite 5,29, Tilgung bis 2098 |

Konsolidiert (der Beitrag fließt nur von einem Konto ins andere): Ausgaben 2028 **43,68 % BIP** gegen 48,77 % heute.

Die Summen sind nur eingeschränkt vergleichbar:
- Heute sind Ausgaben und Aufkommen brutto, also mit Gebühren, Entgelten und Vermögenserträgen (5,94 %).
- Das Modell rechnet Gemeinden und Dach netto.

## 2 Aufkommen nach Steuer- und Abgabenart

| Position heute → nachher | heute Mrd. € 2024 | heute % BIP | Drittel 2028 % BIP | Drittel 2028 Mrd. € | belegt (intern) % BIP | Einfluss der neuen Regeln |
|---|---|---|---|---|---|---|
| **Steuern** | | | | | | |
| Lohn- und Einkommensteuer, Soli (Haushalte), sonstige Einkommensteuern → *Einkommen* | 411,7 | 9,38 | 10,21 | 501,8 | – | Ein Tarif 0/11/19/25/33 % auf alle Einkommen einschließlich Dividende und Gewinnen der Personengesellschaften; Grundbedarf frei; keine Abzüge; Soli entfällt |
| darin heute: Kapitalertrag- und Abgeltungsteuer → *Kapitalerträge* | – | – | 1,37 | 67,3 | – | Kapitalerträge einschließlich Kursgewinnen höchstens 33 % (heute 26,375 %); je Einkommensart ein Drittel |
| Körperschaft- und Gewerbesteuer (Kapitalgesellschaften) → *Unternehmen und Plattformen* | 125,1 | 2,85 | 4,42 | 217,2 | 2,37 | Unternehmen 33 % auf den Konzerngewinn, verteilt nach Kundenumsatz; Plattformen mit Untergrenze; Gewerbesteuer entfällt (Gemeinden über feste Anteile); Altverluste 5 Jahre, Verrechnung über 1 Mio. € höchstens 50 % |
| Mehrwertsteuer → *Konsum (Label)* | 298,8 | 6,81 | 8,51 | 418,3 | – | Label 5/11/17/25 % nach Wirkung auf Gesundheit und Umwelt, Sonderstufe 33 % (Alkohol, Tabak, Kraftstoffe, Fahrzeuge 31 %); effektiv 18,8 % (heute 19/7 %) |
| Verbrauchsteuern (Energie, Strom, Tabak, Alkohol, Kaffee), Versicherung-, Grunderwerb- und Verkehrsteuern, Kfz-Steuer, übrige → *Übrige Steuern* | 126,8 | 2,89 | 3,93 | 193,2 | 2,89 | Weitgehend wie heute (Annahme der Gesamtrechnung); Lenkung über die Sonderstufe im Label. Der Modellwert 3,93 enthält den Emissionshandel (eigene Position CO₂-Preis) und die Grundsteuer (geht in der Grundstücksabgabe auf) ein zweites Mal (Prüfbefund B-1, Korrektur 92) |
| Emissionshandel (Abgaben auf Verschmutzung) → *CO₂-Preis* | 18,6 | 0,42 | 1,67 | 82,1 | 1,36 | CO₂-Preis 100 €/t auf alle bepreisten Emissionen, Pfad bis 150 €/t; sinkt mit den Emissionen |
| Grundsteuer → *Grundstücksabgabe* | 16,2 | 0,37 | 0,82 | 40,3 | – | Bodenwertabgabe bis 1 % des Bodenwerts (Gemeinden) |
| Erbschaft- und Schenkungsteuer → *Erbschaften* | 10,0 | 0,23 | 1,16 | 57,0 | 0,97 | 33 % auf Erwerbe über 100.000 € je Erbe, ohne Verschonung von Betriebsvermögen (heute bis 50 %, viele Ausnahmen) |
| Vermögensteuer (seit 1997 nicht erhoben) → *Große Vermögen* | 0,0 | 0,00 | 0,97 | 47,7 | – | Mindeststeuer (anrechenbar) und 1 % ab 2 Mio. € |
| Abbau klimaschädlicher Subventionen (heute Ausgabe oder Steuervergünstigung) → *Subventionsabbau* | – | – | 0,48 | 23,6 | – | 20 Mrd. € nach UBA-Liste, überwiegend Steuervergünstigungen (Mehraufkommen) und zum Teil Finanzhilfen (weniger Ausgaben); im Modell als Einnahme geführt. Prüfpunkt: Entfernungspauschale und Dienstwagen fallen schon mit „ohne Abzüge“ im Einkommen weg |
| Progression und Dynamik (2028) | – | – | 0,07 | 3,4 | – | Mehraufkommen aus dem Tarif bei wachsenden Einkommen und erwarteter Dynamik |
| **Sozialbeiträge** | | | | | | |
| Beiträge der Arbeitgeber | 302,4 | 6,89 | 0,00 | 0,0 | – | entfallen: Arbeit wird um diesen Betrag billiger |
| Beiträge der Arbeitnehmer | 280,1 | 6,39 | 0,00 | 0,0 | – | entfallen; Gesundheit und Netz aus Steuern |
| Beiträge Nichterwerbstätiger, Selbständiger, freiwillige | 126,1 | 2,87 | 0,00 | 0,0 | – | entfallen |
| unterstellte Beiträge (Beamtenversorgung) | 48,2 | 1,10 | 0,00 | 0,0 | – | entfallen; laufende Pensionen als Altlast über den Fonds |
| **Abgabe für Altlasten** | | | | | | |
| – (neu) → *Altlastenzuschlag* | – | – | 4,90 | 240,8 | – | Altlastenzuschlag auf alle Steuern (DE 2028 14,6 %), zweckgebunden: fließt vollständig als Beitrag an den Gemeinschaftsfonds (Ausgabe), bis 2098 |
| **Übrige Einnahmen** | | | | | | |
| Verkäufe, Gebühren, Vermögenserträge, Transfers | 260,5 | 5,94 | – | – | – | im Modell nicht gerechnet: Ausgaben der Gemeinden und des Dachs sind netto nach Gebühren angesetzt (Annahme); heute brutto. Vergleich der Summen deshalb nur eingeschränkt |
| **Summe** | | **46,14** | **38,51** | **1.892,7** | | |

Nicht im Aufkommen: neue Kredite heute (2,63 % BIP) und Fondskredite nachher (5,29 %). Sie sind Finanzierung (Abschnitt 1).

## 3 Ausgaben nach Aufgaben (Landeshaushalt)

| Position heute → nachher | heute Mrd. € 2024 | heute % BIP | Drittel 2028 % BIP | Drittel 2028 Mrd. € | belegt (intern) % BIP | Einfluss der neuen Regeln |
|---|---|---|---|---|---|---|
| **Verwaltung** | | | | | | |
| Allgemeine Verwaltung, Außenbeziehungen (COFOG 01 ohne Zinsen und Grundlagenforschung) | 185,5 | 4,23 | 2,22 | 109,1 | – | Kommunalverwaltung 1,62 + Außenbeziehungen 0,30 + Standards 0,30; einfaches System, Verwaltung der Sozialversicherung (heute rund 1,1 % BIP) entfällt |
| Zinsen (Schuldendienst) | 49,3 | 1,12 | 0,00 | 0,0 | – | Ausgabe des Gemeinschaftsfonds, nicht des Landeshaushalts (1.04 % BIP, siehe Fondskonto) |
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
| Alter und Hinterbliebene (Renten, Pensionen) | 508,1 | 11,58 | 0,00 | 0,0 | – | Landeshaushalt: keine eigene Position. Alte Ansprüche bis zur Höhe der Dividende trägt die Dividende, darüber der Gemeinschaftsfonds (9.15 % BIP, siehe Fondskonto); neue Ansprüche: Dividende und Pflichtvorsorge (eigenes Konto, 4,1 % BIP, privat) |
| Krankheit und Invalidität (Krankengeld, Pflege, Erwerbsminderung) | 143,9 | 3,28 | 1,14 | 56,0 | – | Pflege (Teilkasko) 0,85 + Invalidität (Grundbedarf) 0,29 |
| Arbeitslosigkeit | 71,7 | 1,64 | 0,41 | 20,2 | – | Grundbedarf; die Dividende trägt mit |
| Familie und Kinder, Wohnen, Grundsicherung, übrige | 159,4 | 3,63 | 0,70 | 34,4 | – | Waisen 0,05 + Härtefall 0,65; Kindergeld, Wohngeld und Grundsicherung gehen in der Dividende auf |
| **Dividende** | | | | | | |
| – (neu) → *Dividende* | – | – | 7,34 | 360,8 | 3,53 | Transformationsdividende für alle Erwachsenen, halb für Kinder; DE 2028 384 € je Erwachsenem und Monat (Kaufkraft 2026) |
| **Gemeinschaftsfonds** | | | | | | |
| – (neu) → *Beitrag an den Fonds* | – | – | 4,90 | 240,8 | – | Beitrag Deutschlands an den Gemeinschaftsfonds, finanziert aus dem Altlastenzuschlag |
| **Summe** | | **48,79** | **38,39** | **1.886,8** | | |

Ausgaben des Gemeinschaftsfonds (Anteil Deutschland):
- Altrenten über der Dividende 9,15 % BIP.
- Zinsen auf übernommene Altschulden 1,04 % BIP, angesetzt mit der Quote von 2024 (Annahme).

## 4 Prüfung jeder Position: Aufkommen, Ausgabe oder Finanzierung

| Position | Art | Konto | Befund |
|---|---|---|---|
| Einkommen | Aufkommen (Steuer) | Landeshaushalt | Wert aus der Tarifrechnung, nicht amtlich belegt; enthält die Steuer auf die Dividende selbst, weil sie steuerpflichtig ist |
| Kapitalerträge | Aufkommen (Steuer) | Landeshaushalt | heute in den Einkommensteuern der Haushalte enthalten; getrennt nicht gelesen |
| Unternehmen und Plattformen | Aufkommen (Steuer) | Landeshaushalt | Modellwert 4,42 nicht belegt, belegt 2,37 (Prüfbefund B-1) |
| Konsum (Label) | Aufkommen (Steuer) | Landeshaushalt | heute Mehrwertsteuer 6,81; Anstieg aus Sonderstufe und Labelstufen (Modell) |
| Übrige Steuern | Aufkommen (Steuer) | Landeshaushalt | Modellwert 3,93 enthält Emissionshandel und Grundsteuer, die eigene Positionen haben (Korrektur 92); wie heute: 2,89 |
| CO₂-Preis | Aufkommen (Abgabe) | Landeshaushalt | heute Emissionshandel 0,42; 100 €/t auf alle bepreisten Emissionen; sinkt mit den Emissionen |
| Grundstücksabgabe | Aufkommen (Abgabe) | Landeshaushalt (Gemeinden) | ersetzt die Grundsteuer (0,37); 0,82 ist der Gesamtbetrag |
| Erbschaften, Große Vermögen | Aufkommen (Steuer) | Landeshaushalt | Erbschaft belegt 0,97 statt 1,16 |
| Subventionsabbau | überwiegend Aufkommen (Wegfall von Steuervergünstigungen), zum Teil weniger Ausgaben | Landeshaushalt | Mischposition; mögliche Überschneidung mit „Einkommen ohne Abzüge“ (Entfernungspauschale, Dienstwagen) und mit dem Label; zu prüfen |
| Progression und Dynamik | Aufkommen (Steuer) | Landeshaushalt | Mehraufkommen aus dem Tarif 2028 |
| Altlastenzuschlag | Aufkommen (zweckgebundene Abgabe) | Landeshaushalt | Durchlauf: geht vollständig als Beitrag an den Fonds; bis v4.94 ohne Gegenbuchung als Einnahme geführt (Korrektur 93) |
| Sozialbeiträge (heute) | Aufkommen (Abgabe) | Gesamtstaat (Sozialversicherung) | entfallen nachher; unterstellte Beiträge der Beamtenversorgung stehen heute zugleich in Aufkommen und Ausgaben |
| Gebühren, Erträge, Transfers (heute) | Aufkommen | Gesamtstaat | nachher nicht gerechnet, Ausgaben netto (Annahme); Summen deshalb nur eingeschränkt vergleichbar |
| Neue Kredite (heute) | Finanzierung | Gesamtstaat | keine Einnahme; deckt den Finanzierungssaldo; bis v4.94 als Einnahme geführt (Korrektur 93) |
| Kredite des Fonds | Finanzierung | Gemeinschaftsfonds | keine Einnahme des Landes; bis v4.94 in den Einnahmen des Landes (Korrektur 93) |
| Dach und Gemeinden | Ausgabe | Landeshaushalt | Werte netto nach Gebühren (Annahme); Zuordnung zu COFOG eigene |
| Netz (Gesundheit, Pflege, Invalidität, Arbeitslosigkeit, Waisen, Härtefall) | Ausgabe | Landeshaushalt | aus Steuern statt Beiträgen |
| Dividende | Ausgabe (Transfer) | Landeshaushalt | Rest nach allen anderen Ausgaben; steuerpflichtig |
| Beitrag an den Gemeinschaftsfonds | Ausgabe (Transfer) | Landeshaushalt | Gegenbuchung zum Altlastenzuschlag; neu seit v4.95 |
| Altrenten über der Dividende | Ausgabe | Gemeinschaftsfonds | bis v4.94 im Landeshaushalt geführt (Korrektur 93) |
| Zinsen (Schuldendienst) | Ausgabe | heute Gesamtstaat, nachher Gemeinschaftsfonds | nachher für übernommene Altschulden; Zinsquote 2024 angenommen; bis v4.94 im Landeshaushalt geführt (Korrektur 93) |

## 5 Wohin die Dividende geht (geltend, % BIP)

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
| belegt (intern), mittlerer Fall, Dividende 2060 | -0,33 |

Euro je Erwachsenem und Monat, Kaufkraft 2026:
- geltend: 384 / 309 / 261 / 256 € (2028 / 2035 / 2045 / 2060);
- belegt, mittlerer Fall: 185 / 97 / 29 / -24 €.

## 6 Was in der Rechnung fehlt: Automatisierung und Erbe (erste Abschätzung, nicht durch die Kette gerechnet)

Unternehmensgewinne, Kapitalerträge und Erbschaften stehen im Modell als fester Anteil am BIP.

**Automatisierung.** Gewinne tragen 33 % beim Unternehmen und ausgeschüttet noch einmal 33 %. Arbeitseinkommen tragen im Tarif im Mittel rund
19 % (Annahme).
- Ein Punkt BIP, der von Arbeit zu Gewinnen wandert, bringt rund +0,25 Punkte (bei hälftiger Ausschüttung; Ableitung).
- Bei −3 Punkten Lohnquote bis 2045 wären das rund +0,75 Punkte (Annahme; eine amtliche Projektion liegt nicht vor).

**Erbe.** Erbschaften und Schenkungen werden auf bis zu 400 Mrd. € je Jahr geschätzt (DIW und WSI 2017, Böckler Impuls 12/2017; eine Studie,
Projektion bis 2027). Die Statistik erfasst davon 113 bis 150 Mrd. € (Destatis 2022–2025).
- Wächst das vererbte Vermögen schneller als das BIP, sind +0,2 bis +0,4 Punkte bis 2045 möglich (Annahme).

**Zusammen** wären das rund +1 Punkt um 2045. Die Werte sind zu belegen und durch die Kette zu rechnen.

## 7 Korrekturen in v4.95

- **Korrektur 92: Grundsteuer doppelt.** Die Modellposition „Übrige Steuern“ (165 Modell-Mrd., 3,93 % BIP) entspricht der heutigen Summe
  dieser Steuern einschließlich Grundsteuer und Emissionshandel (161,6 Mrd. € 2024).
  - Die Grundsteuer geht aber in der Grundstücksabgabe (0,82, Gesamtbetrag) auf.
  - Belegt sind „Übrige“ deshalb 2,89 statt 3,26 % BIP.
  - Die Lücke B-1 wächst auf −3,59 % BIP (mittel).
- **Korrektur 93: Buchung im Haushaltsplan v4.94.** Neue Kredite (heute) und Fondsanleihen standen unter den Einnahmen. Der Fondsbeitrag stand dort
  ohne Gegenbuchung. Altrenten und Zinsen standen im Landeshaushalt.
  - Jetzt: Kredite als Finanzierung.
  - Altlastenzuschlag als Aufkommen und Beitrag an den Fonds als Ausgabe des Landeshaushalts.
  - Altrenten, Zinsen und Fondskredite im eigenen Konto des Gemeinschaftsfonds.

## Quellen

- Eurostat gov_10a_taxag, gov_10a_exp (COFOG), gov_10a_main; Deutschland 2024, vorläufig; abgerufen 15.11.2026.
- Hans-Böckler-Stiftung, Böckler Impuls 12/2017: Erbschaften größer als bislang erwartet (Studie von DIW und WSI). https://www.boeckler.de/de/boeckler-impuls-erbschaften-groesser-als-bislang-erwartet-3761.htm
