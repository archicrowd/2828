# CO₂ und Bodenabgabe in den Haushalten: Hintergrundrechnung zu Modell E mit festem Anteil 30 %

Initiative 28:28 · 21. November 2026 · Modellstand v4.105 (Prüfrechnung; die geltenden Zahlen bleiben unverändert)
Rechnung: `modell/co2_boden_haushalte.py` (+ `.toml`) → `daten/aggregate/co2_boden_haushalte.json`.
Euro je Haushalt und Monat, 2028, Kaufkraft 2026, Deutschland, gegen heute. Anteile in % BIP.

**Beschluss der Initiative (21.11.2026):**
- Fester Baranteil 30 % des Grundbedarfs: 293 € je Erwachsenem, 235 € je Kind, Gesamtwert des Pakets 739 / 680 € (2028).
- Die Empfehlungen aus Modell E werden übernommen: Modell E als Arbeitsgrundlage, Zinsregel, Obergrenze der Rücklage, Bodenabgabe durchrechnen.

## 1 Ergebnis in Kürze

- **Eine eigene Berichtigung vorab (Korrektur 97):** Die Bodenabgabe war gegen den Satz von Stand C kapitalisiert. Der beobachtete Bodenwert enthält aber nur die heutige Grundsteuer (0,24 % des Bodenwerts).
  - Die Abgabe von 2 % bringt deshalb +1,13 statt +1,25 % BIP. Der Bodenwert sinkt um 37 statt 33 %.
  - Modell E trägt dauerhaft 33,7 statt 34,5 % des Grundbedarfs. Der Beschluss von 30 % bleibt im Rahmen.
- **CO₂ (150 €/t, K3):** im Mittel 62 € mehr je Haushalt und Monat als heute, 32 € im untersten und 98 € im obersten Dezil.
  - Die Last ist regressiv: 2,2 % des Nettoeinkommens im untersten Dezil gegen 1,0 % im obersten.
  - Der feste Baranteil gleicht das unten mehrfach aus.
- **Bodenabgabe (2 %):** Eigentümer zahlen im Mittel 166 € im Monat mehr als heute.
  - Mieter sparen die heutige Umlage der Grundsteuer (21 €), wenn die Abgabe nicht umgelegt werden darf.
  - Vermieter tragen 15,9 Mrd. € im Jahr.
- **Haushalte mit allem zusammen** (Baranteil 30 %, CO₂, Boden, Stundung ab 65, keine Umlage, Altersausgleich R4):
  - 70 % der Haushalte stehen besser da, im Mittel +182 €; im Erwerbsalter 76 %, im Mittel +321 €.
  - Rentnerhaushalte: 57 % besser, im Mittel −147 €.
- **Drei Regeln entscheiden über die Verteilung:**
  1. **Keine Umlage auf Mieter.** Mit Umlage sinkt der Anteil der Haushalte mit mehr auf 59 %, bei Mietern im Ruhestand auf 13 %.
  2. **Stundung für Eigentümer ab 65.** Ohne Stundung stehen nur 5 % der Rentner mit Wohneigentum besser da.
  3. **Altersausgleich R4.** Ohne ihn stehen 15 % der Rentnerhaushalte besser da statt 57 %.
- **Fiskalisch:**
  - Mit Altersausgleich und Stundung trägt Modell E 30,7 % des Grundbedarfs. Der Beschluss von 30 % hält, die Rücklage bleibt positiv (mindestens 0,25 % BIP).
  - Der Spielraum ist klein. Ein Übergang der Bodenabgabe über mehrere Jahre oder ein Fondszins von 3 % braucht zusätzliche Regeln (Abschnitt 5).

## 2 CO₂: Kosten je Haushalt

**Ansatz:**
- **Direkt (Heizen, Kraftstoffe):** 160 Mt im Jahr 2024, das sind 10,4 Mrd. € bei 65 €/t.
  - Quelle: DIW Wochenbericht 42/2024, SOEP-Mikrosimulation; eine Studie. Die Mengen sind eigene Ableitung.
  - Fortschreibung: −3 % je Jahr, 2028 also 141,6 Mt.
  - Aufschlag von 65 auf 150 €/t, mit 19 % Label (Annahme: Stufe C).
  - Verteilung nach dem Emissionsprofil je Quintil, Q1 3,0 t bis Q5 6,2 t je Haushalt (Ariadne/PIK-MCC, November 2023, EVS 2018; maschinell aus dem PDF gelesen, an der Quelle zu prüfen; Q2 und Q4 interpoliert).
- **Indirekt (über die Preise):** CO₂-Aufkommen von 1,30 % BIP (K3) gegen 0,47 % BIP heute, ohne den direkten Teil, also 27 Mrd. €.
  - Davon tragen inländische Haushalte 60 % (Annahme), verteilt nach dem Konsum: 16,3 Mrd. €.

| Dezil | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| € je Monat | 32 | 39 | 49 | 53 | 63 | 66 | 72 | 76 | 83 | 98 |
| % des Nettoeinkommens heute | 2,2 | 1,8 | 1,9 | 1,7 | 1,7 | 1,6 | 1,5 | 1,4 | 1,3 | 1,0 |

- **Zusammen 30,6 Mrd. € im Jahr**, im Mittel 62 € je Haushalt und Monat; Rentnerhaushalte 52 €.
- **Zum Vergleich der Ausgleich:** Der Baranteil beträgt 293 € je Erwachsenem. Nach Regel L fließen die CO₂-Einnahmen an den Fonds, die Dividende erhält dafür einen festen Betrag (1,24 % BIP).
- **Befund:** Die frühere Schätzung von rund 0,6 % BIP Mehrlast (R18, v4.98) bestätigt sich in der Größenordnung (30,6 Mrd. € ≈ 0,65 % BIP).

## 3 Bodenabgabe: wer zahlt wie viel

**Ansatz:**
- **Bodenwert 2024 ohne Staat:** 6.777,6 Mrd. €, davon Haushalte 5.179,1 Mrd. € (Bundesbank, Vermögensbilanzen; maschinell gelesen, an der Quelle zu prüfen). Fortgeschrieben mit dem BIP bis 2028.
- **Kapitalisierung:** Der Wert fällt auf r / (r + τ − τ₀), mit r = 3 % (Annahme), τ = 2 % und τ₀ = 0,24 % (heutige Grundsteuer 16,2 Mrd. €).
  - Bezogen auf den heutigen Wert sind das 1,26 % im Jahr, 1,02 Punkte mehr als heute.
- **Eigentümerquote:** 41,8 % der Haushalte (Mikrozensus 2022, nach Haus & Grund; Destatis 41,9 %).
  - Nach Alter: 51,3 % bei Haushalten ab 65 und 37,8 % darunter. Das ist abgeleitet aus dem Anteil der 65-Jährigen und Älteren an Eigentümern (36,1 %) und an Mietern (24,6 %); aus der Grafik gelesen, an der Quelle zu prüfen.
  - Nach Einkommen steigt die Quote logistisch mit dem Rang, vom unteren Fünftel mit rund 20 % bis zum oberen mit rund 65 %. **Annahme:** Amtliche Werte nach Einkommen habe ich nicht gefunden.
- **Selbst genutzter Boden:** 60 % des Bodens der Haushalte (Annahme, Spanne 50 bis 70 %). Er ist auf Eigentümer verteilt, proportional zur Wurzel des Äquivalenzeinkommens (Annahme).
- **Vermieteter Boden:** 40 %. Davon sind 70 % den Haushalten mit Mieteinkünften in der Mikrosimulation zugeordnet (Annahme).

| je Monat, 2028 | |
|---|---|
| Bodenwert je Eigentümerhaushalt (heute, Mittel) | 194.800 € |
| Mehr je Eigentümerhaushalt (2 % auf den neuen Wert − heutige Grundsteuer) | 166 € |
| davon Eigentümer ab 65 | 152 € (gestundet) |
| Mieter: heutige Umlage der Grundsteuer | 21 € (entfällt ohne Umlage) |
| Mieter: Umlage, falls erlaubt | 112 € |
| Vermieter in der Mikrosimulation, Jahr | 15,9 Mrd. € |
| Eigentümer im Modell | 17,2 Mio. Haushalte |

**Vermögenswirkung:**
- Der Bodenwert sinkt durch die Kapitalisierung um 37 %, im Mittel um 72.000 € je Eigentümerhaushalt.
- Das sind zusammen 2.063 Mrd. € bei den Haushalten und 2.699 Mrd. € mit Unternehmen.
- Der Wertverlust ist die Kehrseite der dauerhaften Einnahme. Er trifft vor allem die Eigentümer im Zeitpunkt der Einführung. Künftige Käufer zahlen weniger für den Boden und dafür die Abgabe.
- Literatur: Kapitalisierung von Grundsteuern als Standardergebnis seit Oates (1969). Die Höhe hängt von r ab: Bei r = 2 % (Stresstest) wäre der Verlust größer.

## 4 Haushalte mit allem zusammen

**Fälle**, alle mit Baranteil 30 % (Mikrosimulation mit Kinderanteil 0,8, Zuschlag von Modell E):

| Fall | Haushalte mit mehr | Mittel | Erwerbsalter | Rentner | Rentner mit Eigentum | Rentner zur Miete |
|---|---|---|---|---|---|---|
| ohne CO₂ und Boden (wie bisherige Mikrosimulation, mit R4) | 78 % | +311 € | 82 % / +485 € | 70 % / −106 € | 58 % / −197 € | 81 % / −9 € |
| mit CO₂ | 72 % | +249 € | 80 % / +419 € | 53 % / −157 € | 41 % / −254 € | 65 % / −55 € |
| **mit CO₂ und Boden** (Stundung ab 65, keine Umlage) | **70 %** | **+182 €** | **76 % / +321 €** | **57 % / −147 €** | **41 % / −254 €** | **74 % / −34 €** |
| ohne Stundung | 65 % | +159 € | 76 % / +321 € | 39 % / −225 € | 5 % / −406 € | 74 % / −34 € |
| Umlage auf Mieter erlaubt | 59 % | +117 € | 72 % / +251 € | 28 % / −202 € | 41 % / −254 € | 13 % / −146 € |
| ohne Altersausgleich R4 | 58 % | +158 € | 76 % / +321 € | 15 % / −228 € | 7 % / −338 € | 24 % / −113 € |

**Nach Dezilen** (Anteil mit mehr / Mittel):

| Dezil | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| ohne CO₂ und Boden | 53 % / +38 | 99 % / +278 | 99 % / +325 | 97 % / +381 | 86 % / +434 | 83 % / +465 | 81 % / +499 | 69 % / +470 | 67 % / +385 | 56 % / −51 |
| **mit CO₂ und Boden** | **49 % / +10** | **97 % / +239** | **92 % / +271** | **82 % / +312** | **80 % / +341** | **75 % / +350** | **67 % / +355** | **63 % / +299** | **60 % / +164** | **42 % / −425** |
| mit Umlage auf Mieter | 21 % / −78 | 76 % / +156 | 71 % / +194 | 69 % / +239 | 71 % / +273 | 68 % / +287 | 65 % / +298 | 62 % / +248 | 59 % / +119 | 41 % / −465 |

**Lesart:**
- **Die Bodenabgabe wirkt progressiv, CO₂ regressiv.** Zusammen bleibt die Verteilung progressiv. Das oberste Dezil trägt mit −425 € den größten Teil.
- **Eigentümer im Erwerbsalter** liegen im Mittel bei +37 €. Mieter liegen bei +287 €.
- **Das unterste Dezil** liegt schon ohne CO₂ und Boden nur knapp über null: 53 % mit mehr, im Mittel +38 €. Ursache sind Haushalte mit hohen heutigen Bedarfsleistungen; das ist ein bekannter Befund der Mikrosimulation (R7, R8), nicht der neuen Abgaben.
  - Die CO₂-Kosten drücken dieses Dezil auf +10 €. Die Bodenabgabe wirkt dort kaum, weil wenige Eigentümer sind und Mieter entlastet werden.
- **Rentner mit Wohneigentum** bleiben mit Stundung bei −254 €. Ohne Stundung wären es −406 €.
  - Die Stundung verschiebt die Last nur, sie hebt sie nicht auf. Nach zwölf Jahren stehen im Mittel rund 22.000 € plus Zins von 1 % als Forderung auf dem Grundstück (152 € × 12 × 12 Jahre; Annahme zur Laufzeit).
  - Fällig wird die Forderung beim Verkauf oder im Erbfall.

## 5 Fiskalische Prüfung des festen Anteils 30 %

| Fall | Rücklage niedrigster Stand | höchstens | größter tragbarer Anteil | Anteil 2060 (Fortschrittsregel) | bar 2060 Erw. / Kind |
|---|---|---|---|---|---|
| Modell E, 30 % ohne Zusatzkosten | +0,69 % BIP | 5,1 % BIP | 33,7 % | 45 % | 494 / 396 € |
| **mit Altersausgleich R4 und Stundung** | **+0,25 % BIP** | **8,0 % BIP** | **30,7 %** | **49 %** | **538 / 431 €** |
| dazu Boden eingeschliffen bis 2030 | −0,66 % BIP | 10,5 % BIP | 27,1 % | 47 % | 516 / 413 € |
| dazu Boden eingeschliffen bis 2032 | −1,44 % BIP | 11,4 % BIP | 26,3 % | 46 % | 505 / 404 € |
| dazu Boden eingeschliffen bis 2037 | −4,09 % BIP | 14,1 % BIP | 25,6 % | 43 % | 472 / 378 € |
| Fondszins 3,0 %, mit R4 und Stundung | −5,96 % BIP | | 26,8 % | | |
| Fondszins 3,0 %, mit Zinsregel (+0,52 % BIP) | −0,07 % BIP | | 30,0 % | | |

**Kosten im Einzelnen (2028):**
- Altersausgleich R4: 55 € je Person und Monat, 0,23 % BIP.
- Stundung: Zufluss 11,3 Mrd. € im Jahr (0,24 % BIP). Der Bestand im eingeschwungenen Zustand beträgt 136 Mrd. € (2,9 % BIP), bei zwölf Jahren Laufzeit (Annahme).
  - Der Zinsvorteil kostet 2,0 Mrd. € im Jahr (Fondszins 2,45 % gegen 1 %).
  - Vorsichtig gerechnet: Die Rückflüsse aus Verkauf und Erbfall sind nicht gegengerechnet.

**Lesart und Folgerungen:**
1. **30 % halten**, wenn die Bodenabgabe zum Start voll gilt. Altersausgleich und Stundung passen in den Spielraum zwischen 33,7 und 30 %.
2. **Ein Übergang kostet Geld, weil die Dividende ab 2028 voll gezahlt wird.** Schleift man die Abgabe bis 2030 ein, fehlt eine Brücke von 0,66 % BIP; bis 2037 sind es 4,1 % BIP.
   - **Vorschlag:** Einführung in drei Schritten bis 2030. Die Brücke von höchstens 0,7 % BIP stellt der Fonds als Kassenkredit, der aus der Rücklage zurückgeführt wird.
   - Ein langer Übergang bis 2037 ist mit 30 % nicht vereinbar. Er ginge nur mit einem niedrigeren Start, etwa 25 % steigend.
3. **Zinsregel:** Bei einem Fondszins von 3,0 % fehlen 0,52 % BIP im Jahr.
   - Allein über den Boden wäre dafür ein Satz von 3,15 % nötig. Das lässt den Bodenwert weiter fallen.
   - **Vorschlag für die Spanne:** Boden bis 2,5 % (+0,26 % BIP), den Rest über Kapitalerträge und Erbschaft.
   - **Berichtigt in v4.106 (Korrektur 99):** Hier stand, die Rechnung für die Kapitalseite liefere über 38 % keine plausible Abstufung. Das war ein Bedienfehler meinerseits (Satz als 0,38 statt 38 übergeben). Richtig: Jeder Punkt über 38 % bringt rund +0,08 % BIP und kostet rund 0,1 % BIP Wachstum (`anteil_drittel.json`). Die Initiative hat am 21.11.2026 entschieden, den Boden nicht über 2 % anzuheben (`projekt/Baranteil-ein-Drittel-2026-11-21.md`).
4. **Obergrenze der Rücklage:** Mit der Fortschrittsregel (Ziel 2 % BIP, +1 Punkt je Jahr darüber) steigt die Rücklage bis auf 8 % BIP. Die Regel bremst zu langsam.
   - **Vorschlag:** Über 4 % BIP steigt der Anteil um 2 Punkte je Jahr. Über 6 % BIP fließt der Überschuss an den Fonds zur schnelleren Tilgung.
   - Der Pfad der Fortschrittsregel hängt vom zeitlichen Verlauf der Rücklage ab. Er ist deshalb nicht in jedem Fall monoton im Aufwand: Mit R4 und Stundung liegt der Anteil 2060 höher als ohne, weil der Zufluss der Stundung nach zwölf Jahren endet.

## 6 Empfehlungen

1. **Bodenabgabe 2 % mit drei Regeln:** keine Umlage auf Mieter (Ausschluss aus den Betriebskosten, heute § 2 Nr. 1 BetrKV), Stundung für selbst nutzende Eigentümer ab 65 zu 1 %, Einführung in drei Schritten bis 2030 mit Kassenkredit des Fonds.
   - Nach der Theorie lässt sich eine Abgabe auf den Boden wirtschaftlich nicht überwälzen, weil das Angebot fest ist. Die rechtliche Umlage über die Betriebskosten wäre aber möglich, wenn das Gesetz sie erlaubt. Deshalb braucht es den Ausschluss.
2. **Altersausgleich R4 beschließen** (55 € je Person, 0,23 % BIP). Ohne ihn verliert die Mehrheit der Rentnerhaushalte, mit ihm stehen 57 % besser da.
3. **Härtefall für Eigentümer im Erwerbsalter mit geringem Einkommen prüfen:** etwa eine Stundung auf Antrag, wenn die Abgabe 10 % des Nettoeinkommens übersteigt. Wie viele Haushalte das betrifft, hängt an der Eigentümerquote nach Einkommen; diese ist eine Annahme.
4. **Zinsregel und Obergrenze** wie in Abschnitt 5 beschließen.
5. **Kommunikation des Pakets:** „Ihr Dividendenpaket: 739 € im Monat. Davon tragen 446 € Ihre Gesundheit, Pflege und Absicherung, 293 € erhalten Sie auf Ihr Konto.“

## 7 Grenzen

- **Annahmen mit großer Wirkung:**
  - Eigentümerquote nach Einkommen; Bodenwert je Eigentümer (Wurzel des Einkommens);
  - Anteil des selbst genutzten Bodens (60 %); Zuordnung der Vermieter (70 %);
  - Überwälzung der indirekten CO₂-Kosten (60 %); Laufzeit der Stundung (12 Jahre).
- **Nicht enthalten:**
  - Kapital 38 % auf Kapitaleinkommen der Haushalte;
  - Abgabe auf Boden von Unternehmen (sie wirkt über Preise und Gewinne);
  - Bodenwert in Regionen. In Städten mit hohen Bodenwerten liegt die Abgabe ein Vielfaches über dem Mittel, auf dem Land darunter (R28).
- **Haushaltswerte** gelten für die voll eingeführte Abgabe im Jahr 2028.
- **Eigentümer und Mieter** sind als gewichtete Teilfälle jedes Haushalts der Mikrosimulation gerechnet, nicht als eigene Haushalte mit eigener Einkommensverteilung.

## Quellen

- DIW Berlin: Wochenbericht 42/2024, CO₂-Preis und Klimageld (SOEP 2020, Mikrosimulation). Eine Studie; Mengen eigene Ableitung.
- Kopernikus-Projekt Ariadne (PIK, MCC): Verteilungswirkungen der CO₂-Bepreisung, November 2023 (EVS 2018). Maschinell aus dem PDF gelesen, an der Quelle zu prüfen.
- Deutsche Bundesbank: Sektorale und gesamtwirtschaftliche Vermögensbilanzen, Datenblatt Bodenwert 2024. Maschinell gelesen, an der Quelle zu prüfen.
- Statistisches Bundesamt: Mikrozensus 2022, Wohnen (Eigentümerquote 41,9 %). Altersverteilung nach Haus & Grund auf Basis Mikrozensus 2022: Sekundärquelle einer Interessenvertretung, aus der Grafik gelesen.
- Grundsteuer 2024: 16,222 Mrd. € (Destatis, Realsteuern; `einnahmen_belege.toml`, D29A).
- Betriebskostenverordnung (BetrKV), § 2 Nr. 1: laufende öffentliche Lasten des Grundstücks, namentlich die Grundsteuer.
- Oates, W. E. (1969): The Effects of Property Taxes and Local Public Spending on Property Values. Journal of Political Economy 77(6). Hier nicht erneut an der Quelle geprüft.
- Rechnungen des Projekts: `modell_e.json`, `stellschrauben.json`, `rentner_eichung.json` (R4), `co2_varianten.json` (K3), `mikro_de.json`.
