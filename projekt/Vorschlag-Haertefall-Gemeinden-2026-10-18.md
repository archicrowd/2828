# Härtefall und Gemeinden – Vergleich mit Dänemark und Schweden (Vorschlag, Logbuch v4.7)

Initiative 28:28 · Stand 18. Oktober 2026 · Prüfrechnung `modell/vergleich_dk_se.py` → `daten/aggregate/vergleich_dk_se.json`

**Auftrag (18.10.2026):** Das aktuelle Konzept mit den Regeln in Dänemark und Schweden vergleichen, die im System benachteiligten Gruppen
betrachten, eine Reaktion der Härtefallregel vorschlagen und klären, ob die Gemeinden sie ausgeben und welches Gestaltungsrecht sie haben.

**Status:** Vorschlag zur Entscheidung. Geltend bleibt die Regel Boden (v4.6). Im Konzept ist bisher nicht festgelegt, wer den Härtefall auszahlt.

---

## 1 | Wie Dänemark und Schweden die Mindestsicherung regeln

| | Dänemark (kontanthjælp) | Schweden (ekonomiskt bistånd / försörjningsstöd) | Konzept (Regel Boden) |
|---|---|---|---|
| Höhe festgelegt von | Folketing (Gesetz, feste Sätze) | Regierung (Riksnorm, jährlich) + „angemessene Kosten“ im Einzelfall | Land (Grundbedarf × OECD-Skala) |
| Ausgezahlt von | Kommune | Kommune (socialnämnd) | **offen** |
| Finanziert von | Kommune mit staatlicher Erstattung, die mit der Bezugsdauer sinkt (80 % in den ersten 4 Wochen, 20 % nach einem Jahr; seit 2016) | Kommune aus eigener Einkommensteuer (Mittel 2026: 32,38 %) | Netzbudget des Landes (Härtefall 0,65 % BIP) |
| Wohnkosten | im Satz enthalten; dazu Wohngeld (boligstøtte, zentral über Udbetaling Danmark) und kommunale særlig støtte (§ 34) bei hohen Wohnkosten | **außerhalb** der Norm: tatsächliche Miete, soweit „angemessen“; Maßstab der Kommune ist, was Geringverdiener am Ort zahlen; Übergangsfrist üblich 4 Monate | **pauschal** im Boden (Wohnanteil am Existenzminimum 44 %, DE ≈ 454 €/Monat für Alleinstehende) |
| Einmalige Bedarfe | §§ 81–85 Aktivlov nach kommunalem Ermessen (Einzelausgaben, Miethilfe gegen Räumung, Behandlung, Umzug) | „livsföring i övrigt“ (Möbel, Zahnbehandlung, Brille) nach kommunalen Richtlinien | nicht geregelt |
| Kinder | ein Kinderzuschlag je Versorger (2.909 kr./Monat), unabhängig von der Kinderzahl; Kindergeld zentral | Norm je Kind nach Alter (2.720–4.960 kr./Monat); ab 2027 Kürzung ab dem vierten Kind (Prop. 2025/26:201) | Kind 0,3 in der Skala, Kinderdividende voll angerechnet |
| Eigenes Arbeitseinkommen | Freibetrag 2.700 kr./Monat (erhöhter Satz), darüber 65 % Abzug | voll angerechnet; nach 6 Monaten Bezug 24 Monate lang 25 % des Nettolohns frei („jobbstimulans“) | zur Hälfte angerechnet, ab dem ersten Euro |
| Pflichten | Verfügbarkeit, Sanktionen; Arbeitspflicht bei fehlender Aufenthalts- oder Beschäftigungsdauer | ab Oktober 2026 Aktivitätspflicht bis 40 Stunden/Woche nach 3 Monaten Bezug; Kommune muss Angebote stellen | nicht geregelt |
| Zugangsbedingungen | volle Sätze erst nach 9 von 10 Jahren Aufenthalt und 2½ Jahren Vollzeitarbeit | rechtmäßiger Aufenthalt (ab 2027 ausdrücklich) | nicht geregelt |
| Rechtsschutz | Widerspruch bei der Kommune, dann Ankestyrelsen (staatlich) | Verwaltungsgericht | nicht geregelt |

**Kennzahlen (Prüfrechnung, Sätze 2026, Median EU-SILC 2025 fortgeschrieben):**

| Kennzahl | DE Boden | DE heute | DK | SE |
|---|---|---|---|---|
| Niveau je Äquivalenzerwachsenem, mit Wohnen, % des Medians | 40,3 | 42,4 (Bürgergeld mit KdU, Annahme 520 €) | 44,5 netto, Wohngeld zusätzlich | Norm + tatsächliche Miete |
| Niveau ohne Wohnen, % des Medians | 22,5 | – | – | 18,1 (alleinstehend), 26,4 (Paar + 2 Kinder) |
| Gewicht eines Kindes (Erwachsene = 1) | 0,30 | 0,63–0,84 (Regelbedarf) | – (Zuschlag je Versorger) | 0,57–1,0 (Riksnorm) |
| Belastung eines zusätzlich verdienten Euros im Bezug | 66 % | 98 % | 42 % im Freibetrag, 80 % darüber | 100 % (erste 6 Monate), 80 % mit jobbstimulans |

Lesart: Das Niveau des Bodens liegt in derselben Größenordnung wie in Dänemark und wie das deutsche Bürgergeld. Zwei Unterschiede sind
grundsätzlich: (1) Dänemark und Schweden behandeln die **Wohnkosten** getrennt und nach dem Einzelfall, der Boden pauschal; (2) beide setzen
**Kinder** deutlich höher an als die OECD-Skala (0,3). Beim Erwerbsanreiz ist die Regel Boden günstiger als alle drei Vergleichssysteme.

## 2 | Wer im Konzept benachteiligt ist

| Gruppe | Befund (Modell) | Ursache | Zuständig |
|---|---|---|---|
| Familien ohne oder mit geringem Erwerb | DE Paar + 2 Kinder ohne Erwerb: Boden 2.161 € gegen Bürgergeld 2.634 € (−473 €); bei 15 % des Durchschnittslohns −416 € | Kindergewicht 0,3 | **Parameter** (Skala), nicht Härtefall |
| Alleinerziehende mit kleinem Lohn | DE −177 € bei 15 % des Durchschnittslohns; FR nur 36 % mit mehr | Kindergewicht; FR: Wegfall prime d'activité | Parameter; FR strukturell (N24) |
| Hohe Wohnkosten | Wohnanteil im Boden ≈ 454 €; bei 700 € Warmmiete fehlen 246 €/Monat | pauschaler Boden | **Härtefall H1** |
| Mehrbedarf (Behinderung, chronische Krankheit, Schwangerschaft, Pflege Angehöriger) | im Boden nicht vorgesehen | keine Zuschläge | **Härtefall H2** |
| Einmalige Notlagen (Erstausstattung, Zahnersatz, Mietschulden) | nicht geregelt | keine Regel | **Härtefall H3** (Gemeinde) |
| Rentnerinnen und Rentner | −35 bis −123 €/Monat (v3.58) | Rentenkürzung um eingesparte Beiträge | Rentnerausgleich (offen), nicht Härtefall |
| Geringverdiener in Frankreich | Verlust der prime d'activité, Arbeitgeber sparen am SMIC keine Beiträge | Systemunterschied | N24 |

## 3 | Vorschlag: Härtefallregel

Grundsatz wie beim Boden: **eine Rechnung, dieselbe Halbanrechnung**, keine neuen Programme. Der Härtefall erhöht den Boden des Haushalts;
die Aufstockung bleibt `max(0, Boden + Härtefall − Dividenden − ½ · eigenes Einkommen)`. Damit läuft auch der Härtefall mit steigendem
Einkommen von selbst aus, und der Erwerbsanreiz (66 %) bleibt erhalten.

- **H1 Wohnkosten über dem Wohnanteil:** anerkannt wird die tatsächliche Warmmiete bis zur örtlichen Angemessenheitsgrenze; Zuschlag =
  Miete − Wohnanteil im Boden. Die Gemeinde setzt die Grenze innerhalb eines Korridors, den das Land vorgibt (Vorbild: SE „skälig hyra“,
  DE Kosten der Unterkunft). Übergangsfrist sechs Monate, danach Umzug oder Eigenanteil. Beispiel DE: 700 € Miete → +246 €/Monat.
- **H2 Mehrbedarf:** feste Zuschläge in Prozent des Grundbedarfs, landeseinheitlich (Vorbild: Mehrbedarfe im deutschen Recht). Kein Ermessen
  der Gemeinde, damit gleiche Fälle gleich behandelt werden.
- **H3 Einmalige Bedarfe und Notlagen:** Ermessen der Gemeinde aus einem Pauschalbudget je Einwohner (Vorbild: DK §§ 81–85, SE „livsföring
  i övrigt“), einschließlich Mietschulden zur Abwendung einer Räumung.

**Nicht über den Härtefall:** die Benachteiligung der Familien. Sie folgt aus dem Kindergewicht 0,3. Wenn sie behoben werden soll, ist das eine
Parameterentscheidung (Vorschlag K1): Kindergewicht 0,3 (geltend), 0,45 (DE Paar + 2 Kinder: 2.470 €) oder 0,5 (2.572 €, nahe Bürgergeld
2.634 €). Die Kosten von K1 sind noch nicht gerechnet; sie steigen, weil mehr Familien unter den Boden fallen.

## 4 | Vorschlag: Rolle der Gemeinden

Beide Vergleichsländer lassen die Kommune auszahlen, die Höhe aber national festlegen. Dänemark setzt die Kommunen über die sinkende
Erstattung finanziell unter Druck; eine Auswertung von VIVE (2020, erstes Reformjahr) fand, dass die Kommunen darauf reagierten, aber vor allem
die arbeitsmarktnahen Fälle bevorzugten und weniger arbeitsmarktnahe Empfänger schlechter abschnitten (eine Studie, kurzer Zeitraum; kritisch
zu lesen).

Vorschlag G1–G5:

- **G1 Ausgabestelle:** Die Gemeinde zahlt Aufstockung und Härtefall aus (eine Stelle vor Ort). Dividende und Mindestrente zahlt das Land
  zentral und ohne Antrag (wie Kindergeld und Wohngeld in DK/SE zentral).
- **G2 Rechtsanspruch und Höhe:** Boden, Anrechnung und H2 legt das Land fest; die Gemeinde darf sie nicht unterschreiten. Aus eigenen Mitteln
  darf sie ergänzen, sichtbar als Gemeindezuschlag.
- **G3 Ermessen der Gemeinde:** Angemessenheitsgrenze der Wohnkosten im Korridor (H1), einmalige Bedarfe (H3), Angebote zur Arbeit und
  Qualifizierung, Fristen und Nachweise.
- **G4 Finanzierung:** Rechtsanspruch (Aufstockung, H1, H2) erstattet das Land vollständig aus dem Netzbudget; H3 trägt die Gemeinde aus ihrer
  Formelzuweisung. Eine dänische Erstattungstreppe wird **nicht** empfohlen, weil die Halbanrechnung den Anreiz schon beim Einzelnen setzt und
  die dänische Erfahrung auf Benachteiligung schwer vermittelbarer Menschen hinweist. Alternative zur Entscheidung: Treppe nur für H1.
- **G5 Rechtsschutz:** Widerspruch bei der Gemeinde, danach eine unabhängige Landesstelle (Vorbild Ankestyrelsen) oder Gericht.

**Entscheidungen der Initiative:** H1–H3 annehmen? K1 (Kindergewicht 0,3 / 0,45 / 0,5)? G1–G5, insbesondere G4 (volle Erstattung oder Treppe)?
Pflichten und Zugangsbedingungen (Aktivität, Aufenthaltsdauer) bewusst offen lassen oder regeln?

## 5 | Grenzen der Prüfrechnung

- DK netto mit Personfradrag 54.100 kr., Bundskat 12,01 %, Kommunalsteuer ca. 25 % (Sekundärquelle); AM-Bidrag 8 % auf Lohn, nicht auf
  kontanthjælp (Annahme).
- SE ohne Miete (keine landesweite Größe); Grenzsteuer auf niedrige Löhne 22 % (Annahme). Jobbstimulans nach Gesetz 12 kap. 8 § SoL, Angaben
  aus einer kommunalen Richtlinie (an der Quelle zu prüfen).
- DE Existenzminimum 2026 nach dem 15. Existenzminimumbericht (über eine Spiegelung des Berichts gelesen, an der Quelle zu prüfen); Miete 700 €
  ist ein Beispiel, kein Messwert.
- Kosten von H1–H3 und K1 sind nicht gerechnet; dafür braucht es Mietdaten nach Haushaltstyp (DE: BA-Statistik KdU, EU-SILC Wohnkosten).

## Quellen

- borger.dk, Kontanthjælp (Sätze 2026): https://www.borger.dk/arbejde-dagpenge-ferie/dagpenge-kontanthjaelp-og-sygedagpenge/kontanthjaelp/kontanthjaelp
- STAR, Orientierung der Kommunen über L 13 (Reform, in Kraft 1.7.2025): https://star.dk/media/fjufyd0u/orientering-til-kommunerne-om-vedtagelse-af-l13-om-et-nyt-kontanthjaelpssystem.pdf
- Københavns Kommune, Instrumente nach §§ 34, 81–85 Aktivlov: https://www.kk.dk/sites/default/files/2025-11/Bilag%202.%20Liste%20over%20omr%C3%A5der%20hvor%20K%C3%B8benhavns%20Kommune%20inden%20for%20g%C3%A6ldende%20lovgivning%20kan%20hj%C3%A6lpe%20b%C3%B8rn%20der%20lever%20under%20fattigdomsgr%C3%A6nsen_t.pdf
- Ældre Sagen, Boligstøtte über Udbetaling Danmark (Sekundärquelle): https://www.aeldresagen.dk/viden-og-raadgivning/vaerd-at-vide/b/bolig/boligstoette/generelt-om-boligstoette
- VIVE, Refusionstrappe (2020): https://vive.dk/da/udgivelser/refusionstrappen-og-de-lavthaengende-frugter-i-jobcenteret-14736
- themis.dk, Beløbsgrænser 2026 (Sekundärquelle): https://themis.dk/synopsis/docs/Oversigt_over_beloebsgraenser_2026_.html
- Socialstyrelsen, Riksnormen 2026: https://www.socialstyrelsen.se/contentassets/91f34c410a90484ca2fb1ed0807626d7/2026-1-10012.pdf
- Socialstyrelsen, Meddelandeblad 4/2026 (Aktivitätspflicht): https://www.socialstyrelsen.se/contentassets/3984f8d7808045d9a4b2eed2c09b7356/2026-10-10447.pdf
- Regeringens proposition 2025/26:201 (Bidragstak, ab 1.1.2027): https://data.riksdagen.se/dokument/HD03201.html
- Malmö stad, Berechnung des ekonomiskt bistånd: https://malmo.se/Bo-och-leva/Stod-och-omsorg/Forsorjning-och-ekonomi/Ekonomiskt-bistand/Sa-beraknas-ekonomiskt-bistand.html
- Falköpings kommun, Riktlinjer ekonomiskt bistånd 2026 (jobbstimulans): https://www.falkoping.se/download/18.1adde54a17861a73b1e10779/1780910832477/Riktlinjer%20f%C3%B6r%20ekonomiskt%20bist%C3%A5nd%20till%20f%C3%B6rs%C3%B6rjningsst%C3%B6d%20och%20livsf%C3%B6ring%20i%20%C3%B6vrigt.pdf
- SCB, Kommunalskatterna 2026: https://www.scb.se/hitta-statistik/statistik-efter-amne/offentlig-ekonomi/finanser-for-den-kommunala-sektorn/kommunalskatterna/pong/statistiknyhet/kommunalskatterna-2026/
- Eurostat ilc_di01 (EU-SILC 2025), Abruf 18.10.2026
- 15. Existenzminimumbericht (BT-Drs. 20/13550)
