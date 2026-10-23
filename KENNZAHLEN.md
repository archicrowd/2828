# Kennzahlen Stand C – welche Zahl gilt, und was sie bedeutet

Stand v4.21 (21. Oktober 2026). Anlass: Prüfbericht vom 20.10.2026, Befunde B11, B12, B15 und B16. Dieselbe Größe erscheint in mehreren Dateien
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
| Z 2028 = 9,45 % BIP | `altlasten.json`, `beschluss.verhandlungsmasse_z_2028_pct_bip` | Altrentenansprüche über der Dividende im Klubschnitt, nach Regel E (effektiv 6,95 %; v4.26, vorher 9,38 bei 7,5 %) | geltend |
| Z 2028 = 10,23 % BIP | `systemvarianten.json` | dieselbe Größe im Variantenvergleich v3.43, **ohne** Rentenkürzung | Variantenvergleich |
| Z 2028 = 8,6 % BIP | `laenderseiten.json`, `DE.fonds.z_2028` | Deutschland allein, eigenes BIP | Länderwert |

## Gesamtlast

| Wert (2028, % BIP) | Datei | Bedeutung | Status |
|---|---|---|---|
| heute 40,76 | `gesamtrechnung.json` | Steuern und Sozialbeiträge 2024 (Eurostat, ohne D995) | Vergleichswert |
| **38,70** | `gesamtlast33.json`, A | Steuern 33,53 + Fondsbeitrag 5,17 (v4.26; vorher 38,67) | **geltend** |
| **42,80** | `gesamtlast33.json`, B | A + Pflichtvorsorge 4,10 (eigenes Konto, vererbbar) | **geltend**, alle Pflichtzahlungen |
| 45,46 / 49,56 | `systemvarianten.json`, `gesamtlast_ohne_route` / `_mit_route` | Altlasten im selben Jahr bezahlt (12,04 % ohne Streckung) | Vergleich „ohne Fonds“ |

Die Streckung über den Fonds senkt die laufende Last; ihr Preis ist die Fondsschuld bis 148,1 % BIP (2055).

## Haushalte

| Größe | Basis |
|---|---|
| „Durchschnittslohn“ in Aussagen über Vielfache (z. B. „3-facher Durchschnittslohn“) | OECD Taxing Wages 2025, DE 63.288 € (Vollzeit, Alleinstehende). Wer das Durchschnittsentgelt der Rentenversicherung (~50.000 €) nimmt, kommt auf andere Prozentzahlen (Prüfbericht B14) |
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
| Vorteil alleinstehend, 42.000 € brutto, DE 2028 | 604 / 583 / 562 / 539 € im Monat (v4.29 Mehrwertsteuer nach Einkommen; v4.26: 606 / 585 / 564 / 541) | `fondszins.json` | Kaufkraft 2026 |
| Gemeinsamer Satz mit Italien und Polen / alle 30 Staaten | 16,6 % / 15,5 % | `fonds_klub.json` | skaliert auf den Beschluss (Annahme) |

## Mikrosimulation (extern, v4.21; eigene, v4.22)

| Größe | Wert | Datei | Status |
|---|---|---|---|
| Eigene Population: Haushalte mit mehr, Hauptperson Vollzeit / Teilzeit / Minijob, Weitergabe 80 % | 99,3 / 99,8 / 47,6 % | `mikro_de.json` | Prüfrechnung, synthetisch geeicht (v4.22) |
| Eigene Population: Bürgergeld ohne Erwerb / Rentnerhaushalte mit mehr | 14,7 % (−45 €) / 29,6 % (−129 € im Monat; allein −106, Paar −153; v4.26 Regel E, vorher 5,4 % / −145 €) | `mikro_de.json` | Prüfrechnung; Rentner mit Haushaltseinkommen (EU-SILC, ASID) |
| Eigene Population: erwerbsfähige Haushalte / alle Haushalte / alle Personen mit mehr | 85,1 / 69,0 / 76,5 % (v4.31; v4.26: 89,2 / 69,6 / 78,3) | `mikro_de.json` | Prüfrechnung; Spanne der Ziehungen < 0,5 Punkte |
| Validierung 2025: Bruttolohnsumme / Lohnsteuer ohne Eichung | −3,2 / −4,8 % gegen amtlich | `mikro_de.json` | Prüfrechnung |
| Rentnerregel E (Beschluss 22.10.2026, v4.26): Boden 1.083 / 1.632 €, 15 % auf Zusagen über dem Grundbedarf | Rentnerhaushalte mit mehr 30,7 %, Mittel −124 €; Fünftel +21 / −1 / −33 / −134 / −479 € (Zuschlag 15,5 %); gegen bisherige Regel −0,05 % BIP | `rentner_kombi.json` | **geltend** (Beschluss 22.10.2026) |
| Eigene Population: Beamte, 20 % der Beihilfe-Ersparnis (geltend, v4.31) / mit Versicherungszulage (Variante) / Selbständige mit mehr | 56,0 % (+106 €) / 81,4 % (+381 €) / 77,0 % (+306 €) | `mikro_de.json` | Prüfrechnung; Bezüge, PKV und Haushaltsform Annahmen |
| Mehrwertsteuer nach Einkommen (v4.29): sichtbare Mehrbelastung / gezahlte Steuer im Mittel | 1,54 % / 10,76 % des Konsums gegen bisher einheitlich 2,48 % / 15,85 %; Faktor je Einkommen 0,87 (unter 1.000 €) bis 1,07 (über 5.000 €) | `mwst_verteilung.json` | geltend: Rest gleichmäßig je Euro Konsum (Annahme); Band: nur sichtbare Steuer hebt 42.000 € um rund +50 € |
| Validierung Rentner (v4.23, ohne Eichung): Netto je Haushalt / GRV je Person / unter Grundsicherungsbedarf | +4 % gegen ASID 2023 / 1.311 € gegen DRV ≈ 1.317 € / 1,13 Mio. gegen 0,76 Mio. Empfänger | `mikro_de.json` | Rückrechnung und DRV-Bruttowert als Annahme |
| Vollzeitbeschäftigte mit mehr verfügbarem Einkommen, Beschluss / halbe / keine Weitergabe | 99,0 / 98,4 / 92,0 % | `beitraege/kvribbeck-2028/ergebnis.csv` | externe Rechnung (Kulturverein Ribbeck e.V.), eine Quelle; Formprüfung bestanden; Grenzen in der LIESMICH.md |
| Beispielhaushalte des Repositorys, Beschluss | 97,8 bis 100 % je Haushaltstyp (`haushalte33`), 98 % (`regel_boden`, mit Grundauskommen und Bedarfsleistungen) | `haushalte33.json`, `regel_boden.json` | Prüfrechnung |
