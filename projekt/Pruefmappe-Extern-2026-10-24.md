# Prüfmappe für eine externe Prüfung – Stand C „Das Goldene Drittel“

Initiative 28:28 · Modellstand v4.42, nachgeführt v4.46 (Befunde der dritten Prüfung) · 24. Oktober 2026 · Lizenz: Text CC BY 4.0

Diese Mappe ist für Prüferinnen und Prüfer geschrieben, die die Rechnung von außen nachvollziehen sollen. Sie nennt, was gilt, worauf das
Ergebnis beruht, was nur angenommen ist und wo wir selbst die größten Schwächen sehen. Sie ersetzt keine Quelle: Jede Zahl verweist auf eine
Ergebnisdatei in `daten/aggregate/` und auf das Skript, das sie erzeugt.

---

## 1 | Was geprüft werden soll

**Geprüft wird Stand C („Das Goldene Drittel“, Fassung 4.x, seit v3.43), nicht die 28:28-Gesamtrechnung (Stand B).** Eine frühere Prüfung
(19./20.10.2026) hat Stand B geprüft, weil unsere Einstiegsdokumente ihn noch als geltend auswiesen (Korrektur 66). `DATENZUGANG.md` beschreibt
den Weg der Daten noch überwiegend für Stand B; für Stand C gilt diese Mappe zusammen mit `README.md` (Abschnitt „Aktueller Stand“) und
`KENNZAHLEN.md`.

| Was | Wo |
|---|---|
| Welche Zahl gilt, mit Abgrenzung | `KENNZAHLEN.md` |
| Alle Rechenstufen in Reihenfolge (64) | `modell/alles.py` |
| Jede Version, jede bewegte Zahl, jede Korrektur (1–72) | `logbuch/Versionsgeschichte-TAX-2828-BandIII.md`, Abschnitt 4 (Korrekturen) und 7 (offene Punkte) |
| Webseite (sechs Sprachen) und Konzept | `seite/stand-c/`, `dokumente/entwurf/TAX-Drittel-Konzept.pdf` |
| Register der Bausteine und Nahtstellen | `projekt/bausteine.csv`, `projekt/nahtstellen.csv` |

**Nachrechnen:** `python3 modell/alles.py` (Python 3.11 oder neuer, `numpy`, `scipy`). Alle 64 Stufen laufen ohne Netzzugang aus den
eingecheckten Aggregaten; Rückgabe 0 = alle Selbstprüfungen bestanden. Einzelne Stufen lassen sich allein ausführen
(`python3 modell/<skript>.py`). Rohdaten Dritter (Taxplorer, SOEP, EU-SILC-Mikrodaten, Kreisdaten) liegen nicht im Repository; gerechnet wird nur
mit veröffentlichten Aggregaten. Die amtlichen Eingangswerte (Eurostat) lassen sich mit `python3 modell/eingangswerte.py --abrufen`
erneut abrufen und gegen die eingecheckten Werte vergleichen (nur dieser Schritt braucht Netzzugang).

**Zugang:** github.com/archicrowd/2828 (Sichtbarkeit laut GitHub am 24.10.2026: öffentlich; bis v4.45 stand hier „privat“, Korrektur 76).

---

## 2 | Das System in sechs Sätzen

1. Alle Einkommen (Lohn, Gewinn, Kapital, Renten) tragen denselben Stufentarif 0 / 11 / 19 / 25 / 33 %, mit Stufen am Grundbedarf (DE 12.348 € im
   Jahr, 2026); keine Sozialbeiträge; Mehrwertsteuer nach Labels (System 33R).
2. Aus dem Aufkommen werden ein „starkes Netz“ (Grundversorgung Gesundheit, Pflege, Mindestrente, Invalidität, Arbeitslosigkeit, Härtefall) und
   gemeinsame Aufgaben bezahlt; der Rest geht als Transformationsdividende an jeden Erwachsenen (Kinder 0,8).
3. Wer mit Dividende und eigenem Einkommen (zur Hälfte angerechnet) unter dem Grundauskommen liegt, erhält eine Aufstockung von der Gemeinde.
4. Betriebe geben mindestens 80 % der wegfallenden Arbeitgeberbeiträge in den Lohn, gezählt bis zum Lohn beim Sechsfachen des Grundbedarfs.
5. Staatsschulden und ungedeckte Rentenzusagen aus dem alten System (Altlasten) gehen in einen gemeinsamen Fonds der 30 Staaten, der bis 2098
   getilgt wird; Rentenzusagen werden auf den Teil über dem Grundbedarf um 15 % gekürzt.
6. Jeder Staat trägt den Fonds zunächst nach seiner eigenen Altlast; bis 2058 gleichen sich die Zuschläge an.

---

## 3 | Die tragenden Zahlen (geltend, v4.42)

| Größe | Wert | Datei |
|---|---|---|
| Dividende je Erwachsenem, DE, Kaufkraft 2026 | 373 € (2028) → 294 (2035) → 239 € (2060); mit Kinderanteil 0,8: 354 € je Erwachsenem, 283 € je Kind (2028) | `netz33.json`, `regel_boden.json` |
| Gemeinsamer Fonds der 30 | Beitrag 5,17 % BIP, Zuschlag 15,5 % auf alle Steuern, Schuldenspitze 148,1 % BIP (2055), getilgt 2098, Zins 2,45 % | `fonds_geltend.json` |
| Zuschlag je Staat 2028 nach Verrechnung | DE 15,0 / FR 21,3 / IT 22,3 / ES 18,3 / PL 13,5 % | `fonds_geltend.json → verrechnung` |
| Gesamtlast 2028 | 38,70 % BIP (Steuern 33,53 + Fonds 5,17); mit Pflichtvorsorge 42,80 %; heute 40,76 % | `gesamtlast33.json` |
| Beispiel DE: alleinstehend, 42.000 € brutto | +611 € im Monat (2028, Kaufkraft 2026) | `regel_boden.json`, `fondszins.json` |
| Mikrosimulation DE: Haushalte mit mehr | alle 69,3 %; erwerbsfähige 85,1 %; Hauptperson Vollzeit 99,1 %; Rentnerhaushalte 32 % | `mikro_de.json` |
| Länder: alleinstehend beim Durchschnittslohn | FR +390 €, IT +412 €, ES +350 €, PL +1.474 zł | `verrechnung_haushalte.json` |
| Gini 2028 (Modelländerung auf amtlichen Wert) | DE 26,1; FR 29,8; IT 26,9; ES 25,0; PL 18,8 | `gini.json` |

---

## 4 | Setzungen, die das Ergebnis tragen (Beschlüsse der Initiative)

Diese Punkte sind keine Rechenergebnisse, sondern Entscheidungen. Ändert sich eine davon, ändert sich die Aussage. Die Empfindlichkeit ist jeweils
gerechnet.

| Setzung | Geltend | Empfindlichkeit | Datei |
|---|---|---|---|
| **Weitergabe der Arbeitgeberbeiträge in den Lohn** | 80 %, bis 6 × Grundbedarf; Rest beim Betrieb; Gesetz zur Vertragsanpassung, Rückfallregel | Haushalte mit Vollzeit-Hauptperson mit mehr bei 0 / 50 / 80 / 100 %: 92,9 / 98,4 / 99,1 / 99,4 %; alle Haushalte 61,0 / 66,9 / 69,3 / 71,1 %. Empirie zur Inzidenz: eine Studie (Saez, Schoefer, Seim 2019) | `mikro_de.json → basis.ergebnis`, `weitergabe_sensitivitaet.json` |
| **Rentnerregel E** | 15 % Kürzung der Zusagen über dem Grundbedarf; Boden = heutige Grundsicherung (1.083 / 1.632 €) | effektiv 6,95 % aller Zusagen in DE; je Staat 1,9 % (IS) bis 12,1 % (LU) | `rentner_kombi.json`, `kuerzung_laender.json` |
| **Fonds: Zins und Laufzeit** | 2,45 % (Mittel Euroraum 2006–2025), Tilgung bis 2098 | Zins 3,0 / 3,5 / 4,0 %: gemeinsamer Zuschlag 17,1 / 18,7 / 20,4 %, für Deutschland 2028 nach Verrechnung 16,5 / 18,1 / 19,7 %; 42.000 € DE +590 / +570 / +548 € (Lesart seit v4.46 benannt, Korrektur 75) | `fondszins.json` |
| **Fonds: nominales Wachstum** (seit v4.46, Prüfbefund B21) | 3,0 % | Wachstum 2,5 / 2,0 % bei Zins 2,45 %: Beitrag 5,68 / 6,22 % BIP, Zuschlag 17,0 / 18,6 %; bei festem Beitrag und 2,0 % Restschuld 2098 rund 87 % BIP | `fondszins.json → zins_wachstum` |
| **Fonds der 30 aus dem Fonds der zehn skaliert** | Beschluss der zehn × Verhältnis 30/10 in der Abgrenzung des Möglichkeitsraums | nicht als Band gerechnet (siehe 5) | `fonds_klub.py` |
| **Tarif und Labels** | 0/11/19/25/33 %, Labels 5/11/17/25 % plus Sonderstufe | Deckung 2028 und Pfad in `projektion33`, `systemvarianten` | `systemvarianten.toml` |
| **Kinder** | Kinderdividende 0,8; Kindergewicht im Boden 0,55 | Varianten 0,3 / 0,45 / 0,5 | `kindergewicht.json` |
| **Beamte** | 20 % der Beihilfe-Ersparnis weitergegeben | Beamte mit mehr 56 % (+112 €); mit Versicherungszulage 83 % | `mikro_de.json → beamte_zulage` |
| **Ausweichen bei Erbschaft und Vermögen** | statisch eingerechnet | ungünstig: −1,06 % BIP, Dividende −55 € (2028) | `ausweichen33.json` |

---

## 5 | Annahmen ohne amtlichen Beleg (Auswahl, nach erwarteter Wirkung)

Alle Annahmen sind im jeweiligen Parameterfile als „Annahme“ gekennzeichnet. Die wichtigsten:

1. **Übertragung deutscher Muster auf andere Staaten.** Lohnverteilung je Land = deutsche Verteilung, skaliert mit dem Durchschnittslohn;
   Verteilungsform der Rentenzusagen = deutsche Mikrosimulation; Mietüberhang = deutsche Werte nach Grundbedarf; Mehrwertsteuer nach Einkommen
   nur für DE (EVS 2023). Die Gewinneraussagen für FR, IT, ES, PL sind dadurch unsicherer als für DE.
2. **Verhalten statisch.** Keine Rückwirkung auf Arbeitsangebot, Löhne, Preise (außer eigenen Varianten zu Preisniveau und Ausweichen).
3. **Skalierung des Fonds von zehn auf 30 Staaten** über ein Verhältnis aus einer anderen Abgrenzung (Schuld 2024, Altrenten nach Tabelle 29)
   und Verrechnung je Staat in dieser Abgrenzung.
4. **Rentner = Personen ab 65** bei der mittleren Zusage je Person (Frühverrentung verzerrt je Staat).
5. **Mikrosimulation DE:** synthetische Population aus veröffentlichten Eckwerten (keine Mikrodaten); Teilzeit lognormal ohne Dezile; Beamtenbezüge
   und PKV-Beiträge gesetzt; Selbständige aus einem Online-Panel (WSI); Kapitaleinkünfte lognormal aus EU-SILC-Quartilen (untererfasst, Varianten ×2 / ×4).
6. **Mehrwertsteuer:** Rest zwischen sichtbarer Steuer und Durchschnittsbelastung gleichmäßig je Euro Konsum verteilt.
7. **Härtefall:** H2 (Mehrbedarf 0,03 % BIP) und H3 (15 € je Einwohner) gesetzt; H1 aus Mietdaten (DE), Streuung gesetzt.
8. **Gini:** Rückrechnung beobachteter Nettoeinkommen auf Löhne über das heutige Netto; bei Mindestsicherung mit flachem Verlauf (ES) mehrdeutig.

---

## 6 | Was bisher gegen amtliche Zahlen geprüft ist

| Prüfung (ohne Eichung auf diese Größe) | Modell | amtlich | Datei |
|---|---|---|---|
| Bruttolohnsumme DE 2025 | 1.969 Mrd. € | 2.026,5 Mrd. € (−2,8 %) | `mikro_de.json → basis.validierung_2025` |
| Lohnsteuer + Kindergeld DE 2025 | 300,9 Mrd. € | 318,0 Mrd. € (−5,4 %) | dto. |
| Kindergeld DE 2025 | 54,6 Mrd. € | 55,3 Mrd. € | dto. |
| Haushalte mit Bürgergeld, Wohngeld oder Kinderzuschlag | Anspruch 4,7 Mio. | beobachtet rund 4,0 Mio. (Inanspruchnahme 85 %) | dto., Korrektur 72 |
| Rentner: Äquivalenzeinkommen Paare (Mittel) | 32.535 € | 31.053 € (EU-SILC) | `mikro_de.json → pruefung_rentner` |
| Steuer- und Abgabenkeil bei Durchschnittslohn | FR 45,6 / IT 43,7 / ES 42,1 / PL 40,0 % | OECD 47,2 / 47,1 / 40,6 / 34,7 % | `heute_laender.json → pruefung_oecd` |
| Selbstprüfungen der Rechenkette | Gegenproben Haushaltsformeln, Rechner der Seite = Modell, Übertrag Rentnerregel in den Fonds | – | `alles.py` |

**Nicht geprüft:** das Aufkommen der neuen Steuern gegen eine unabhängige Rechnung; die Länderrechnungen gegen nationale Mikrosimulationen
(z. B. EUROMOD); die Deckung je Staat im Möglichkeitsraum. Polen weicht beim Abgabenkeil um gut 5 Punkte vom OECD-Wert ab (Modell zu hoch).

---

## 7 | Bekannte Schwächen und offene Punkte

Vollständig im Logbuch, Abschnitt 7. Die für eine Prüfung wichtigsten:

- **R4:** Renditen, COFOG-Neuabruf und Zuordnung der Posten (B19) offen; BIP-Neuabruf 2024 liegt als Schalter vor, ist aber nicht geltend.
- **R5:** Mehrwertsteuer nach Einkommen für FR, IT, ES, PL fehlt; feinere Lohnverteilungen fehlen; RSA (FR) nicht eingerechnet.
- **R6:** Boden B1 im Fonds weiter deutsch skaliert.
- **R7:** Mietdaten nur für DE; H2/H3 nicht belegt.
- **R8:** Teilzeit-Dezile, Alterseinkommen nach Einkommenshöhe, Rentner mit Minijob.
- **R9:** Altersprofil je Staat (Ageing Report), Preisniveau mit Zweitrundeneffekten, CO₂-Pfad.
- **R10/R11:** Staaten außerhalb der Referenzländer; Gemeindehaushalte.
- **P1:** rechtliche Prüfung (Eigentumsschutz der Anwartschaften, Art. 125 AEUV, Europarecht der Dividende, WTO).

---

## 8 | Prüffragen an Sie (nach Gewicht)

1. **Weitergabe:** Ist eine gesetzliche Pflicht zur Vertragsanpassung mit 80 % bis zum Sechsfachen des Grundbedarfs durchsetzbar, und wie
   belastbar ist die Annahme, dass sie in den Löhnen ankommt? Was folgt aus der Inzidenz-Literatur über die Schwedenstudie hinaus?
2. **Aufkommen 33R:** Trägt der Tarif mit Labels die Deckung 2028 (Quote 33,53 % BIP Steuern)? Prüfbar über `systemvarianten.py` und `projektion33.py`.
3. **Altlasten:** Sind Z (Altrenten über der Dividende, 9,42 % BIP 2028 im Klubschnitt; bis v4.45 hier 9,45, Korrektur 74) und die Übertragung von zehn auf 30 Staaten sachgerecht
   abgegrenzt? Ist der Fondszins (Mittel 2006–2025 statt Marktzins) vertretbar?
4. **Länder:** Wie weit tragen die vereinfachten Steuer- und Abgabenmodelle FR, IT, ES, PL (Abgleich nur mit OECD Taxing Wages)? Welche
   Leistungen fehlen „heute“?
5. **Mikrosimulation DE:** Ist die synthetische Population für Aussagen über Anteile mit mehr Geld geeignet? Wo würde eine Rechnung mit Mikrodaten
   (SOEP, EU-SILC) am ehesten abweichen?
6. **Verteilung:** Ist die Gini-Rückrechnung methodisch haltbar?

**Form der Rückmeldung:** je Befund: Datei und Zeile oder Kennzahl, was falsch ist, was richtig wäre, Quelle. Externe Rechnungen bitte im Format
`schnittstelle/ergebnis-schema.csv` (Beschreibung `schnittstelle/MIKROSIMULATION.md`); wir prüfen sie mit `schnittstelle/pruefe_beitrag.py`
und führen jede Übernahme im Logbuch.
Befunde, die zutreffen, werden als Korrektur mit Nummer geführt (nächste freie: 77). Antwort auf die dritte Prüfung: `projekt/Stellungnahme-Pruefung4-2026-10-24.md`.

---

*Quelle aller Zahlen: Repository der Initiative 28:28, Modellstand v4.42. Werte in Euro: Kaufkraft 2026, wenn nicht anders angegeben; PL in Złoty.*
