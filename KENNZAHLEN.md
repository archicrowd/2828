# Kennzahlen Stand C – welche Zahl gilt, und was sie bedeutet

Angelegt mit v4.21 (21. Oktober 2026), fortgeschrieben bis v4.51 (24. Oktober 2026). Anlass: Prüfbericht vom 20.10.2026, Befunde B11, B12, B15 und B16. Dieselbe Größe erscheint in mehreren Dateien
mit verschiedenen Werten, weil die Abgrenzungen verschieden sind. Hier steht je Größe, **welcher Wert gilt** und wie die anderen zu lesen sind.
Wer eine Zahl zitiert, nennt die Zeile dieser Tabelle.

## Transformationsdividende

| Wert | Datei | Bedeutung | Status |
|---|---|---|---|
| **373 € (2028) → 294 (2035) → 235 (2050) → 239 € (2060)** je Erwachsenem, ohne Kinderanteil 0,8 | `netz33.json`, `beschluss.reihe` | Dividende nach dem Netz-Beschluss (v3.51), Kaufkraft 2026, DE; Kinder rechnerisch zur Hälfte | **geltender Pfad** |
| **354 € je Erwachsenem, 283 € je Kind (2028)** | `netz33.json` × Topf `regel_boden.json: topf` = 0,948 | derselbe Pfad mit Kinderanteil 0,8 (R1): gleicher Topf, anders verteilt | **geltend auf Seite und im Konzept** |
| 296 € (2028) → 217 (2035) → 161 € (2050) | `projektion33.json` | Vorstufe vor dem Netz-Beschluss (v3.47/v3.48), ohne Gesundheitskatalog −5 % und ohne Mindestrente | **archiviert**, nur Zwischenschritt der Rechenkette |
| Mindestniveau 217–239 € | `projektion33.json`, `systemvarianten.json` | Prüfgröße aus Stand B („Mindestdividende“). In Stand C ist die Dividende ein Rest, ihr Sinken ist gewollt; die Sicherung leistet das Grundauskommen | **keine Zusage**, Information |

Empfindlichkeit: Der geltende Pfad liegt 2060 mit 239 € genau auf der alten Prüfgröße; mit Kinderanteil 0,8 sind es 227 € je Erwachsenem. Je
Zehntelpunkt BIP mehr oder weniger Netz ändert sich die Dividende 2060 um rund 7 € je Erwachsenem (2060: 3,4 % BIP = 239 €, `netz33`).

## Altlasten

| Wert | Datei | Bedeutung | Status |
|---|---|---|---|
| **Fondsbeitrag 5,17 % BIP, Zuschlag 15,5 % auf alle Steuern, Spitze 148,1 % (2055), getilgt 2098 (v4.26, Rentnerregel E; vorher 5,14 / 15,4 / 147,3); Zins 2,45 % (Mittel Euroraum 2006–2025)** | `fonds_geltend.json` | gemeinsamer Fonds der 30 Staaten (Beschluss 21.10.2026): Beschluss der zehn × Verhältnis 30/10 aus dem Möglichkeitsraum (Annahme). Bis v4.19: zehn Staaten, 2,5 %, 5,28 / 15,8 / 149,6 % (`altlasten.json`, `beschluss`; bei 2,45 % und Regel E: 5,26 / 15,7 / 150,2 %), Rentenregel E (v4.26; vorher Kürzung 7,5 %), anteilige Verrechnung, Grundauskommen im Bestand, gekoppelter Rentenbeginn | **geltend auf allen Seiten und im Konzept** (Beschluss 20.10.2026 zu B11, v4.17); Länderrechnungen FR, IT, ES, PL mit demselben Zuschlag 15,8 % |
| DE 4,76 % / 14,2 % / 138 % (2055); FR 6,65 / 20,3 / 196 (2054); IT 6,88 / 20,7 / 206; ES 5,52 / 16,5 / 161; PL 4,20 / 12,7 / 122 | `laenderseiten.json`, `staaten.*.fonds_eigen` | **eigener Fonds je Staat** zum gemeinsamen Zins 2,5 % (Altlasten Sache der Staaten) | **Vergleich** („allein trüge …“), `staaten.*.fonds_eigen`; bis v4.16 auf den Länderseiten FR, IT, ES, PL geltend |
| Z 2028 = 9,42 % BIP | `altlasten.json`, `beschluss.verhandlungsmasse_z_2028_pct_bip` | Altrentenansprüche über der Dividende im Klubschnitt, nach Regel E mit Kürzungssatz je Staat (v4.37; Kennzahl bis v4.45 nicht nachgezogen, Korrektur 74; v4.26: 9,45 bei 6,95 % für alle; vorher 9,38 bei 7,5 %) | geltend |
| Z 2028 = 10,23 % BIP | `systemvarianten.json` | dieselbe Größe im Variantenvergleich v3.43, **ohne** Rentenkürzung | Variantenvergleich |
| Z 2028 = 8,6 % BIP | `laenderseiten.json`, `DE.fonds.z_2028` | Deutschland allein, eigenes BIP | Länderwert |

## Gesamtlast

| Wert (2028, % BIP) | Datei | Bedeutung | Status |
|---|---|---|---|
| heute 40,76 | `gesamtrechnung.json` | Steuern und Sozialbeiträge 2024 (Eurostat, ohne D995) | Vergleichswert |
| **38,70** | `gesamtlast33.json`, A | Steuern 33,53 + Fondsbeitrag 5,17 (v4.26; vorher 38,67) | **geltend** |
| **42,80** | `gesamtlast33.json`, B | A + Pflichtvorsorge 4,10 (eigenes Konto, vererbbar) | **geltend**, alle Pflichtzahlungen |
| 45,58 / 49,68 | `gesamtlast33.json`, `c_ohne_fonds_2028` | Steuern 33,53 + Altlasten im selben Jahr 12,05 (ohne Streckung), mit Pflichtvorsorge 4,10 (v4.46, Korrektur 73; vorher 45,46/49,56 hier und 45,47/49,57 in den Dateien) | Vergleich „ohne Fonds“ |
| 45,47 / 49,57 | `systemvarianten.json`, `gesamtlast_ohne_route` / `_mit_route` | dieselbe Größe mit dem Steuerbedarf 33,42 statt der Deckung 33,53 (Variantenvergleich) | Variantenvergleich |

Die Streckung über den Fonds senkt die laufende Last; ihr Preis ist die Fondsschuld bis 148,1 % BIP (2055).

## Haushalte

| Größe | Basis |
|---|---|
| „Durchschnittslohn“ in Aussagen über Vielfache (z. B. „3-facher Durchschnittslohn“) | OECD Taxing Wages 2025, DE 63.288 € (Vollzeit, Alleinstehende). Wer das Durchschnittsentgelt der Rentenversicherung (~50.000 €) nimmt, kommt auf andere Prozentzahlen (Prüfbericht B14) |
| Grenzbelastung je Euro Bruttolohn, alleinstehend (v4.47): heute / neu 2028 / neu nach Tilgung | 42.000 €: 43,8 / 40,3 / 34,2 %; 60.000 €: 48,8 (bereinigt um den Rentenanspruch 44,1–39,5) / 40,0 / 34,1 %; 100.000 €: 53,1 / 39,1 / 33,6 %; 150.000 €: 44,3 / 40,0 / 34,1 %; 500.000 €: 47,5 / 40,0 / 34,1 %. Mit Pflichtvorsorge (Ersparnis, kein Abgabe) neu jeweils rund 9–10 Punkte mehr | `grenzbelastung33.json` | Prüfrechnung; Äquivalenz des Rentenbeitrags als Band (Annahme) |
| Vorsorge in Vergleichen | geltend: Pflichtvorsorge 10 % ab dem ersten Euro. Variante „Vorsorge wie heute“ (18,6 % bis zur Beitragsbemessungsgrenze) nur in `haushalte33.json` zum Vergleich |
| Grundauskommen | Grundbedarf × 1 / 0,5 je weitere/n Erwachsene/n / 0,55 je Kind; DE 1.029 € (allein), 2.675 € (Paar + 2) im Monat, 2028, Kaufkraft 2026 |
| Bestandsrenten | Regel E (Beschluss 22.10.2026): Zusagen (GRV, Beamtenversorgung) auf den Teil über dem Grundbedarf (1.029 € je Person) um 15 % gekürzt, eigene Vorsorge ungekürzt; Grundauskommen im Bestand = heutige Grundsicherung (1.083 € allein, 1.632 € Paar); KV- und PV-Beiträge entfallen |

## Preise und Ausweichreaktionen (v4.18)

| Größe | Wert | Datei | Status |
|---|---|---|---|
| Preisniveauschub 2028 durch die Mehrwertsteuer | +1,2 bis +2,1 % (mechanisch +2,47 %) | `preisniveau33.json` | Prüfrechnung, Annahmen zu Überwälzung und Anteil |
| netto mit halber Weitergabe der Arbeitskostensenkung | +0,3 bis +1,3 % | `preisniveau33.json` | Prüfrechnung |
| Ausweichen ungünstig (Erbschaft 50 %, Vermögen 75 %) | −1,06 % BIP; Dividende −55 € (2028), −75 € (2060) | `ausweichen33.json` | Empfindlichkeit |
| Rückfluss an den Fonds bei 50 % tatsächlicher Weitergabe | 2,4 bis 2,8 % BIP | `weitergabe_rueckfall.json` | Prüfrechnung |

## Fondszins und Abgrenzung des Fonds (v4.19)

| Größe | Wert | Datei | Status |
|---|---|---|---|
| Zuschlag bei Fondszins 2,45 / 3,0 / 3,5 / 4,0 % (Fonds der 30, v4.20) | 15,5 / 17,1 / 18,7 / 20,4 % (Beitrag 5,17 / 5,73 / 6,27 / 6,82 % BIP; v4.26) | `fondszins.json` | Empfindlichkeit; Marktzins Oktober 2026: Bund 3,46 %, EU 3,95 % (Sekundärquellen) |
| Vorteil alleinstehend, 42.000 € brutto, DE 2028 | 611 / 590 / 570 / 548 € im Monat (v4.38 Zuschlag DE nach Verrechnung 15,0 %; v4.29: 604 / 583 / 562 / 539) | `fondszins.json` | Kaufkraft 2026 |
| Gemeinsamer Satz mit Italien und Polen / alle 30 Staaten | 16,6 % / 15,5 % | `fonds_klub.json` | skaliert auf den Beschluss (Annahme) |

| Zins × nominales Wachstum (v4.46, Prüfbefund B21): Beitrag / Zuschlag bei Zins 2,45 % und Wachstum 3,0 / 2,5 / 2,0 % | 5,17 / 5,68 / 6,22 % BIP; 15,5 / 17,0 / 18,6 %; Spitze (zehn) 149,9 / 152,2 / 154,1 %. Bei festem Beschlussbeitrag und 2,0 % Wachstum Restschuld 2098 rund 87 % BIP (zehn), Spitze 191 % (2064) | `fondszins.json → zins_wachstum` | Empfindlichkeit; Z in % BIP unverändert (Annahme) |
| Zinsband 42.000 € DE (v4.38 mit Verrechnung) | Zuschlag gemeinsam 15,5 / 17,1 / 18,7 / 20,4 % = für Deutschland 2028 15,0 / 16,5 / 18,1 / 19,7 %; +611 / +590 / +570 / +548 € | `fondszins.json → varianten` | Lesart geklärt v4.46 (Prüfbefund B24, Korrektur 75) |

## Mikrosimulation (im Auftrag der Initiative, v4.21; eigene, v4.22)

| Größe | Wert | Datei | Status |
|---|---|---|---|
| Eigene Population: Haushalte mit mehr, Hauptperson Vollzeit / Teilzeit / Minijob, Weitergabe 80 % | 99,3 / 99,8 / 47,6 % | `mikro_de.json` | Prüfrechnung, synthetisch geeicht (v4.22) |
| Eigene Population: Bürgergeld ohne Erwerb / Rentnerhaushalte mit mehr | 14,7 % (−45 €) / 29,6 % (−129 € im Monat; allein −106, Paar −153; v4.26 Regel E, vorher 5,4 % / −145 €) | `mikro_de.json` | Prüfrechnung; Rentner mit Haushaltseinkommen (EU-SILC, ASID) |
| Eigene Population: erwerbsfähige Haushalte / alle Haushalte / alle Personen mit mehr | 85,1 / 69,3 / 76,7 % (v4.38 Verrechnung; v4.36 Deckel: 84,9 / 68,9 / 76,3; v4.31: 85,1 / 69,0 / 76,5; v4.26: 89,2 / 69,6 / 78,3) | `mikro_de.json` | Prüfrechnung; Spanne der Ziehungen < 0,5 Punkte |
| Nicht-Inanspruchnahme (v4.40, Variante): Quote bei Haushalten mit Erwerb / alle Haushalte mit mehr / Minijob / unterstes Zehntel | 69 % (beobachtet 4,0 Mio. gegen Anspruch 4,7 Mio.) / 69,3 → 69,6 % / 49 → 64 % / 39,8 → 42,6 % (+21 → +63 €; neu voll +96 €) | `mikro_de.json` → `inanspruchnahme` | Prüfrechnung; geltend volle Inanspruchnahme (vorsichtig) |
| Validierung 2025: Bruttolohnsumme / Lohnsteuer ohne Eichung | −3,2 / −4,8 % gegen amtlich | `mikro_de.json` | Prüfrechnung |
| Rentnerregel E (Beschluss 22.10.2026, v4.26): Boden 1.083 / 1.632 €, 15 % auf Zusagen über dem Grundbedarf | Rentnerhaushalte mit mehr 30,7 %, Mittel −124 €; Fünftel +21 / −1 / −33 / −134 / −479 € (Zuschlag 15,5 %); gegen bisherige Regel −0,05 % BIP | `rentner_kombi.json` | **geltend** (Beschluss 22.10.2026) |
| Eigene Population: Beamte, 20 % der Beihilfe-Ersparnis (geltend, v4.31) / mit Versicherungszulage (Variante) / Selbständige mit mehr | 56,4 % (+112 €) / 82,8 % (+389 €) / 77,7 % (+315 €) (v4.38; v4.36: 55,9 / 81,3 / 76,9 %; v4.31: 56,0 / 81,4 / 77,0 %) | `mikro_de.json` | Prüfrechnung; Bezüge, PKV und Haushaltsform Annahmen |
| Mehrwertsteuer nach Einkommen (v4.29): sichtbare Mehrbelastung / gezahlte Steuer im Mittel | 1,54 % / 10,76 % des Konsums gegen bisher einheitlich 2,48 % / 15,85 %; Faktor je Einkommen 0,87 (unter 1.000 €) bis 1,07 (über 5.000 €) | `mwst_verteilung.json` | geltend: Rest gleichmäßig je Euro Konsum (Annahme); Band: nur sichtbare Steuer hebt 42.000 € um rund +50 € |
| Basis Große Vermögen statisch 2028 (v4.32): Bundesbank-Befragung / DIW mit Spitze / Deckung | 0,79 / 2,06 / 1,94 % BIP | `vermoegensbasis33.json` | Prüfrechnung; je eine Studie, Pareto-Annahme |
| Verrechnung je Staat im Fonds der 30 (E11, v4.38): Zuschlag 2028 DE / FR / IT / ES / PL | 15,0 / 21,3 / 22,3 / 18,3 / 13,5 % (gemeinsamer Satz 15,5 %, Angleichung bis 2058); FR alleinerziehend mit mehr 100 → 73 % (v4.51 nach Korrektur 78: 100 %), Durchschnittslohn FR +480 → +390 €, IT +494 → +412 € | `fonds_geltend.json`, `verrechnung_haushalte.json` | geltend (Beschluss 24.10.2026) |
| Deckel der Weitergabe, einheitlich 6 × Grundbedarf (v4.36, E2; DE 74.088 €): allein bei 2× / 3× Durchschnittslohn DE / FR / IT | +689 / +400 € · +849 / +717 € · +941 / +999 € (vorher DE +804 / +515, IT +1.060 / +1.574; FR v4.33 +887 / +755) ; Gini 2028 DE 26,1, FR 29,5 (amtlich heute 30,4), IT 26,9 (v4.51, Korrektur 79: hier stand bis v4.50 der Stand v4.36, FR 30,4 / IT 27,4) | `deckel_einheitlich.json`, `gini.json` | geltend (Beschluss E2, einheitliche Regel; v4.33 nur FR) |
| Validierung Rentner (v4.23, ohne Eichung): Netto je Haushalt / GRV je Person / unter Grundsicherungsbedarf | +4 % gegen ASID 2023 / 1.311 € gegen DRV ≈ 1.317 € / 1,13 Mio. gegen 0,76 Mio. Empfänger | `mikro_de.json` | Rückrechnung und DRV-Bruttowert als Annahme |
| Vollzeitbeschäftigte mit mehr verfügbarem Einkommen, Beschluss / halbe / keine Weitergabe | 99,0 / 98,4 / 92,0 % | `beitraege/kvribbeck-2028/ergebnis.csv` | Rechnung im Auftrag der Initiative (Kulturverein Ribbeck e.V.), eine Quelle; Formprüfung bestanden; Grenzen in der LIESMICH.md |
| Beispielhaushalte des Repositorys, Beschluss | 97,8 bis 100 % je Haushaltstyp (`haushalte33`), 98 % (`regel_boden`, mit Grundauskommen und Bedarfsleistungen) | `haushalte33.json`, `regel_boden.json` | Prüfrechnung |

## Deckungspositionen 33R 2028: Herkunft, Basis, Satz (v4.46, Prüfbefunde B22/B23)

Summe 33,53 % BIP (`systemvarianten.json`, Variante 33R, `deckung_positionen`). Die Positionen stammen aus dem nationalen Modell (Stand A,
`modell/kern/modell-2828.py`, Modellbasis 4.200 Mrd. € BIP) und dem Rahmen der Gesamtrechnung (`modell/gesamtrechnung.py`, Zeilen 01–07),
umgerechnet vom Satz 28 % auf 33 % (Faktor 33/28) bzw. auf den Tarif am Grundbedarf.

| Position | % BIP | Herkunft | Basis und Satz | Status |
|---|---|---|---|---|
| Einkommen | 10,21 | Tarifrechnung am Grundbedarf (`tarif_grundbedarf.py`, Einkommensverteilung des Kernmodells) | alle Einkommen einschließlich Dividende, Tarif 0/11/19/25/33 % | geltend; Eichung gegen Lohn- und Einkommensteuerstatistik offen (dritte Prüfung) |
| Kapitalerträge | 1,37 | Kernmodell: 45 Mrd. € bei 25 % | Basis rund 180 Mrd. € Kapitalerträge (Modellbasis), Satz 33 % | Basis im Kernmodell gesetzt; extern plausibel (dritte Prüfung: Ist ≈ 1,26 % BIP) |
| Konsum (Label) | 8,51 | MwSt-Basis des Kernmodells (350 Mrd. € bei 18 %), effektiver Labelsatz 18,84 % | steuerpflichtiger Konsum, Labels 5/11/17/25 % + Sonderstufe | geltend; Basis +5 % gegen heutige USt-Basis (dritte Prüfung) |
| Unternehmen und Plattformen | 4,42 | Kernmodell: 145 Mrd. € bei 25 % | implizite Basis rund 580 Mrd. € (13,8 % der Modellbasis), Satz 33 %; ersetzt Körperschaft- und Gewerbesteuer (Annahme) | **Basis nicht belegt** (B23): heute alle gewinnabhängigen Steuern ≈ 3,8 % BIP; Definition (Gewinn, Kundenort, Plattformen) offen |
| Erbschaften | 1,16 | Kernmodell 33 Mrd. € bei 25 % + Baustein Freibetrag 100.000 € | Erwerbe über 100.000 € ohne Verschonung, Satz 33 %; nötige Basis 2028 173 Mrd. € gegen steuerpflichtigen Erwerb 2025 150,5 Mrd. € (fortgeschrieben 164 Mrd. €; `vermoegensbasis33.json`) | Basis im Bereich der Daten (v4.32); Schenkungen gleich behandeln (Parität) und reale Übertragungen (Schätzung IMK rund 400 Mrd. €) als Obergrenze nennen – offen (B22) |
| Große Vermögen | 0,97 | Mindeststeuer (anrechenbar) + Vermögensteuer 1 % ab 2 Mio. € | statisch 1,94 % BIP mit DIW-Spitze, 0,79 % nach Bundesbank-Befragung (`vermoegensbasis33.json`) | Ausweichen als Empfindlichkeit (`ausweichen33.json`); oberer Rand der Literatur nicht gedeckt (dritte Prüfung, M3) |
| CO₂-Preis | 1,67 | 100 €/t netto + Pfad bis 150 €/t | Emissionspfad der Gesamtrechnung | geltend |
| Subventionsabbau | 0,48 | Abbau klimaschädlicher Subventionen (20 Mrd. €) | UBA-Liste (Annahme zur Abbauquote) | geltend |
| Übrige Steuern | 3,93 | Energie, Tabak, Alkohol u. a. (165 Mrd. €) | heutige Verbrauchsteuern | geltend |
| Grundstücksabgabe | 0,82 | Bodenwertabgabe (Ebene B, Satz bis 1 %) | Bodenwert | geltend |

## Archivierte Dateien in `daten/aggregate/` (v4.46, Prüfbefund B19)

`deckung_quote.csv`, `gesamtrechnung.json` und ihre Begleitdateien sind Ergebnisse von **Stand B** (`modell/gesamtrechnung.py`, Quote 30,2 %,
Tarif 0/9/16/21/28 %). Sie bleiben als Regressionsprüfung in der Rechenkette, gelten aber nicht. Die geltende Deckung 33R steht in
`systemvarianten.json`.


## Validierung international (v4.51)

| Größe | Wert | Datei | Status |
|---|---|---|---|
| Steuer- und Abgabenkeil Modell (Recht 2026) gegen OECD Taxing Wages 2026 (Daten 2025): allein 100 % / Paar, ein Einkommen, 2 Kinder | DE −0,4 / −0,2; FR −1,2 / −5,6; IT −1,4 / −1,3; ES +1,0 / +1,0; PL +5,3 / +6,5 Pp | `validierung_laender.json` | Prüfrechnung; 7 von 10 Typen ±2 Pp; FR-Paar: prime d'activité (OECD offenbar ohne), PL: Abgrenzung der Beiträge (R13) |
| prime d'activité FR gegen Fälle des Arbeitsministeriums (Reform 1.4.2026), €/Monat | allein 1,15 / 1,2 / 1,4 SMIC: 211 / 182 / 66 (Ministerium 212 / 184 / 70); Paar 2 Kinder mit forfait 1,15 / 1,2: 572 / 543 (568 / 539) | `validierung_laender.json → varianten` | nach Korrekturen 77/78 |
| FR heute, halber SMIC Vollzeit, allein | 1.136 € im Monat (bis v4.50: 1.219 €); neu 1.299 € | `verrechnung_haushalte.json` | geltend |
