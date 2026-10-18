# Freigabevorlage Fassung 4.8 (fortgeschrieben bis v4.11)

> v4.11: Der Begriff „Boden“ heißt jetzt **Grundauskommen** (Auftrag der Initiative). Rentnerpaket eingerechnet (Abschnitt 4); Altlastenzuschlag 13,7 → 15,8 %, Beispiel 42.000 € +630 → +602 €.

# – Kindergewicht, Härtefall, Gemeinden, Gini, Webseite

Initiative 28:28 · 18. Oktober 2026 · Logbuch Band III, v4.8 · Status: **zur Freigabe**

**Auftrag (18.10.2026):** Kindergewicht 0,3 fair anpassen (auch 0,7–0,8 prüfen). Im Übrigen den Empfehlungen aus v4.7 folgen: Härtefall H1–H3,
Gemeinderolle G1–G5. Alles rechnen und zur Freigabe vorlegen. Webseite überarbeiten: Bildung und Gemeinden, Anreize für Bildung, Arbeit,
Forschung, Innovation und Kultur, Sicherheit mit Freiheit, Gini-Grafik; die Grafiken zur Dividende und zu den Staatsschulden zurücknehmen;
Anwendbarkeit auf anderen Kontinenten mit Vorbehalt nennen.

---

## 1 | Kindergewicht im Grundauskommen – Vorschlag 0,55

| Maßstab | Gewicht eines Kindes (Erwachsene = 1) | Quelle |
|---|---|---|
| bisher (OECD-modifiziert) | 0,30 | Eurostat/OECD |
| Bürgergeld mit Unterkunft je Kind | ≈ 0,46 | sozial_laender.toml (Annahme KdU) |
| weitere Erwachsene im Grundauskommen | 0,50 | Regel Grundauskommen |
| **sächliches Existenzminimum Kind / Grundbedarf** | **0,55** (6.828 / 12.348 €) | Kinderfreibetrag 2026 (Sekundärquelle) |
| Existenzminimum mit Betreuung, Erziehung, Ausbildung | 0,79 | Grundlage von R1 (Dividende 0,8) |
| Riksnorm Schweden, ohne Wohnen | 0,57–1,0 | Socialstyrelsen 2026 |

**Begründung für 0,55:** Das Grundauskommen deckt den sachlichen Bedarf des Kindes. Betreuung, Erziehung und Ausbildung (der Unterschied zu 0,79)
erhalten die Kinder als Sachleistung der Gemeinde. Dafür bekommt die Gemeinde je Kind einen festen Betrag, in Deutschland 13.729 € im Jahr.
Damit passen Grundauskommen, Kinderdividende (0,8) und Gemeindeauftrag zusammen.

**Varianten, 2028, Monatsbeträge (Deutschland) und Kosten der Aufstockung (% BIP, Band) gegen das Netzbudget:**

| Kindergewicht | Paar + 2 Kinder ohne Erwerb | dito mit Vollzeit-Mindestlohn | Alleinerziehend + 1 ohne Erwerb | Kosten DE | FR | IT | ES | PL |
|---|---|---|---|---|---|---|---|---|
| 0,3 | 2.105 € | 3.169 € | 1.310 € | 0,13–0,59 | 0,48–1,25 | 0,33–0,96 | 0,50–1,20 | 0,44–1,29 |
| 0,45 | 2.414 € | 3.301 € | 1.464 € | 0,17–0,70 | 0,60–1,38 | 0,42–1,09 | 0,63–1,33 | 0,56–1,45 |
| 0,5 | 2.517 € | 3.403 € | 1.515 € | 0,19–0,73 | 0,64–1,42 | 0,46–1,13 | 0,68–1,38 | 0,61–1,51 |
| **0,55** | **2.620 €** | **3.506 €** | **1.567 €** | **0,21–0,77** | **0,69–1,47** | **0,50–1,18** | **0,73–1,43** | **0,66–1,56** |
| 0,7 | 2.929 € | 3.815 € | 1.721 € | 0,27–0,88 | 0,84–1,62 | 0,62–1,31 | 0,89–1,60 | 0,84–1,73 |
| 0,8 | 3.134 € | 4.021 € | 1.824 € | 0,31–0,96 | 0,95–1,73 | 0,72–1,40 | 1,02–1,72 | 0,97–1,87 |
| Netzbudget | | | | 1,17 | 1,74 | 1,37 | 2,05 | 1,23 |

Bürgergeld heute für Paar + 2 Kinder ohne Erwerb: 2.634 €. Bei 0,55 liegt das Grundauskommen praktisch gleichauf (−14 €). Bei allen Gewichten bleibt der
Abstand zur Arbeit erhalten: Vollzeit-Mindestlohn bringt 28–51 % mehr als kein Erwerb (Halbanrechnung). Bei 0,7–0,8 reicht das Budget in der
oberen Schätzung in Italien und Polen nicht, Frankreich liegt an der Grenze, und für den Härtefall bleibt kaum Raum.

**Wirkung von 0,55:** Beschäftigte mit mehr im Geldbeutel (heute mit Bürgergeld): DE 100 / 100 / 98 % (alleinstehend / alleinerziehend /
Paar + 2). Die Aussage „9 von 10“ ist in Deutschland damit wieder gedeckt (Korrektur 63 galt für Kindergewicht 0,3). FR 73 / 100 / 100 %;
IT, ES, PL 100 %. Dort fehlen heutige Bedarfsleistungen im Modell (ADI, IMV, Sozialhilfe), deshalb ist der Wert dort zu hoch angesetzt.

## 2 | Härtefall und Gemeinden (nach Empfehlung angenommen, gerechnet)

Regeln: H1 Wohnkosten über dem Wohnanteil bis zur örtlichen Grenze, H2 Mehrbedarf landeseinheitlich, H3 Einmalbedarfe nach Ermessen der Gemeinde.
Die Rechnung bleibt eine einzige: Aufstockung = Grundauskommen + H1 + H2 − Dividenden − ½ × eigenes Einkommen. Für die Gemeinden gelten G1–G5:
- Die Gemeinde zahlt aus.
- Das Land setzt Höhe und Anrechnung; die Gemeinde darf ergänzen, aber nicht unterschreiten.
- Ermessen hat die Gemeinde bei der Mietgrenze, den Einmalbedarfen und den Angeboten.
- Das Land erstattet den Rechtsanspruch vollständig; eine dänische Erstattungstreppe gibt es nicht.
- Rechtsschutz: Widerspruch, danach eine unabhängige Landesstelle.

| % BIP 2028 | DE | FR | IT | ES | PL |
|---|---|---|---|---|---|
| Grundauskommen + H1–H3, untere / obere Schätzung | 0,35 / 1,00 | 0,97 / 1,75 | 0,74 / 1,44 | 1,03 / 1,73 | 0,98 / 1,88 |
| Netzbudget (Härtefall, Arbeitslosigkeit, Invalidität) | 1,17 | 1,74 | 1,37 | 2,05 | 1,23 |
| Reserve, obere Schätzung | 0,17 | −0,01 | −0,07 | 0,32 | −0,65 |

Wo die Reserve negativ ist, sinkt die Erwachsenendividende: FR −0,5 €, IT −2,7 €, PL −63 zł im Monat (jeweils obere Schätzung).
H1 ist mit Annahmen gerechnet: Die Hälfte der Aufgestockten hat einen Mietüberhang von durchschnittlich 150 € (DE). Für eine belastbare Zahl
fehlen Mietdaten nach Haushaltstyp.

## 3 | Gini-Koeffizient (neu gerechnet)

| Gini (0–100) | DE | FR | IT | ES | PL |
|---|---|---|---|---|---|
| heute 2025 (amtlich, Eurostat) | 30,1 | 30,4 | 31,0 | 30,8 | 24,9 |
| Goldenes Drittel 2028 | 26,5 | 32,4 | 28,8 | 25,3 | 19,3 |
| Goldenes Drittel 2060 | 26,9 | 32,3 | 29,0 | 25,3 | 19,4 |
| 2028, Rentnerhaushalte unverändert | 27,7 | 32,1 | 29,9 | 26,9 | 21,4 |

Zum Vergleich heute: Dänemark 28,2, Schweden 28,6.

Die Rechnung ist statisch und läuft je Äquivalenzerwachsenem. Die Rekonstruktion der heutigen Verteilung trifft den amtlichen Gini auf
0,1–0,3 Punkte. **In Frankreich steigt der Gini** um 2 Punkte. Die Erklärung wurde in v4.9 berichtigt (Korrektur 64):
- **Hauptursache:** Die 80-%-Weitergabe der in Frankreich ungedeckelten Arbeitgeberbeiträge hebt hohe Löhne um 24–41 %.
- **Dazu kommen:** die Delle beim SMIC (keine Beiträge wegen RGDU, Wegfall der prime d'activité) und die kleinste Dividende (8 % des Medians).
- **Spannweite:** Mit einem Deckel der Weitergabe sinkt der Gini auf 27,6–29,8; mit Familienabbildung liegt er bei 29,5 (`modell/gini_frankreich.py`).

Entscheidung über den Deckel offen (N28).

## 4 | Rentner (v4.11 eingerechnet)

Beschlossen sind vier einfache Regeln:
- **A:** Bestandsrenten werden um 7,5 % gekürzt, nicht um 12,35 %.
- **T1:** Der Altanspruch wird anteilig verrechnet.
- **B1:** Auch kleine Bestandsrenten erhalten das Grundauskommen; die Rente wird dabei voll angerechnet.
- **L1:** Der Rentenbeginn liegt bei 67 Jahren und folgt zu ⅔ der Lebenserwartung.

Rentner haben damit im Monat 33 bis 54 € weniger als heute, vorher 35 bis 123 €. Der Vergleich rechnet heute einschließlich der Grundsicherung
im Alter. Der Fondsbeitrag steigt von 4,64 auf 5,28 % BIP, der Altlastenzuschlag von 13,7 auf 15,8 %. Einzelheiten: `Vorschlag-Rentnerausgleich-2026-10-18.md`.

## 5 | Webseite Fassung 4.8 (sechs Sprachen) und Konzept

- **Kennzahlen oben:** Dividende 354 € je Erwachsenem und 283 € je Kind. „9 von 10“ ist neu belegt (Regel Grundauskommen, heute mit Bürgergeld). Das
  Beispiel zeigt +630 € statt +642 €.
- **Rechner:** Kinder 80 %, Aufstockung bis zum Grundauskommen mit Halbanrechnung, heute mit Bürgergeld (DE), APL (FR) und CAPI (ES). Das Ergebnis
  stimmt mit dem Modell überein (20 Stichproben, Abweichung höchstens 1 €).
- **Neuer Abschnitt „Ein Netz, das trägt – und Wege öffnet“** mit vier Karten:
  - Bildung und Betreuung: die Gemeinde, je Kind;
  - eigene Bildung und Arbeit;
  - Forschung und Innovation: das Dach;
  - Kultur und Gemeinschaft: die Gemeinde.
- **Tabelle „Mehr Sicherheit und mehr Freiheit zugleich“ je Land:**
  - verfügbares Einkommen bei halbem Mindestlohn;
  - was von einem Zusatzeuro bleibt;
  - Gini;
  - Antrag gegen ohne Antrag.

  Verschlechterungen erscheinen rot: In IT, ES und PL bleibt von einem Zusatzeuro weniger als heute, weil das Grundauskommen dort neu ist. In FR gilt
  das ebenso, und der Gini steigt.
- **Gini-Grafik:** fünf Länder mit den Werten heute, 2028 und 2060, dazu Dänemark und Schweden zum Vergleich.
- **Grafiken zurückgenommen:** Die Dividendengrafik ist aufklappbar. In „Wohin die Reise geht“ steht CO₂ zuerst, die Staatsschulden als zweiter Reiter.
- **Über Europa hinaus:** neue Karte mit dem Vorbehalt „wegen des vorliegenden Datenbestands und Modellstands noch nicht weiter bearbeitet“.
- **Konzept und Kurzfassung (Fassung 4.8, PDF):**
  - Kinder 80 %, Begriffe Grundauskommen und Härtefall, Gemeinderolle;
  - Kostentabelle, neuer Abschnitt 3.7 Gini, Haushaltstabelle mit Bürgergeld;
  - Absatz über Europa hinaus, Vorbilder Dänemark und Schweden.

**Zu prüfen vor Upload:**
- Die Übersetzungen der neuen Texte sind maschinell (EN, FR, IT, ES, PL); sie sollten muttersprachlich gegengelesen werden.
- Die anderen Sprachfassungen duzen weiter wie bisher (IT, ES, PL).
- Den Vergleichswert 10.500 € je Schüler (Destatis, über Sekundärquelle) an der Quelle prüfen.

## Zur Freigabe

1. Kindergewicht **0,55** (oder 0,45 / 0,5 / 0,7 / 0,8)?
2. Härtefall H1–H3 und Gemeinderolle G1–G5 wie gerechnet?
3. Webseite und Konzept Fassung 4.8 zum Upload (Paket `Webseite-v4.8.zip`)?

Quellen: Eurostat ilc_di01 und ilc_di12 (EU-SILC 2025, Abruf 18.10.2026); Kinderfreibetrag 2026 (Sekundärquelle, sozial_laender.toml);
Socialstyrelsen, Riksnorm 2026; VIVE 2020; Destatis über Münster Aktuell (12.3.2026, Sekundärquelle); eigene Rechnungen kindergewicht,
haertefall, gini, regel_boden.
