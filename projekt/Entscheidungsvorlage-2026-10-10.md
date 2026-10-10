# Entscheidungsvorlage zur nächsten Fassung (Stand v3.32, 10. Oktober 2026)

Zweck: drei Entscheidungen, die vor einer neuen Fassung des Gesamtkonzepts und der Webseite fallen müssen, dazu eine Bestätigung. Je Option: Wirkung auf Quote und Deckung, Dividende, Text. Alle Beträge Euro 2028, nominal, je Erwachsenem und Monat, soweit nicht anders angegeben. Rechnungen: `modell/nachfrage.py`, `modell/uebergang.py`, `modell/laendervarianten.py`, `modell/gesamtrechnung.py`. Die Empfehlungen sind Vorschläge; entscheidet die Initiative.

---

## E1 · Mehrwertsteuer-Label: Zuordnung der Produkte zu den Stufen (wichtigster Punkt)

**Ausgangslage.** Die Gesamtrechnung setzt das Konsumaufkommen mit 8,95 % des BIP an. Das beruht auf einem effektiven Satz von 20 %. Diesen Satz ergibt das Kernmodell nur, weil es 60 % des Konsums in die Stufen C (22 %) und D (28 %) legt (Gewichte 10/10/20/30/30 %, als Annahme gekennzeichnet). Eine Produktliste je Stufe gibt es bisher nicht. Heute liegt der effektive Satz bei etwa 16,5 % (Projektannahme; mit deutschen Sätzen auf die EU-Konsumstruktur 16,0 %).

| Option | Zuordnung | effektiver Satz | Konsumaufkommen (% BIP) | Deckungslücke (Punkte) | Preisniveau gegen heute |
|---|---|---|---|---|---|
| **A** bisher | 60 % des Konsums in C/D, unabhängig vom Produkt | 20,0 % | 8,95 | 1,73 | +3,0 % |
| **B** nach Datenblatt | Grundbedarf, Reparatur A+; Standardgüter B; Energie, Fahrzeuge, Kraftstoffe C | 14,9 % | 6,98 | 3,70 | −1,3 % |
| **C** steuernd | wie B, dazu Kleidung, Einrichtung, Freizeitgüter C; Fahrzeuge, Kraftstoffe, Alkohol/Tabak D; Gaststätten A | 16,9 % | 7,76 | 2,92 | +0,3 % |
| **D** wie B, Normalsatz angehoben | wie B, Stufe B auf 27,6 % | 20,0 % | 8,95 | 1,73 | +3,0 % |

Lesehilfe: Eine größere Deckungslücke bedeutet, dass die Steuerbasen die Quote von 31,9 % nicht voll tragen. Schließt man die zusätzliche Lücke über die Dividende, kostet jeder Punkt rund 8 % der Dividende (Dividende 11,9 % des BIP). Option C hieße dann etwa −10 % Dividende, Option B etwa −17 %, wenn nichts anderes geändert wird.

**Abwägung.**
- A hält die Zahlen, verlangt aber, dass der größte Teil des Alltagskonsums mit 22 oder 28 % besteuert wird. Das widerspricht dem Bild „Grundbedarf günstig, Luxus teuer“ und hebt das Preisniveau um etwa 3 %.
- B ist am leichtesten zu erklären, reißt aber die größte Lücke.
- C folgt der Idee des Labels (Ressourcen teurer), hält die Preise etwa stabil, öffnet aber eine zusätzliche Lücke von 1,2 Punkten.
- D macht B und D fast gleich (27,6 gegen 28 %); das Label verliert seinen Sinn.
- Die Nachfrageprüfung (v3.31, v3.32) zeigt: Das Label senkt den Ressourcenverbrauch, lenkt aber kaum Kaufkraft in die Region.

**Empfehlung: C**, mit einer verbindlichen Produktliste je Stufe (nach Ressourcen- oder CO₂-Fußabdruck je Euro, nicht nach Herkunft), und eine zweite Entscheidung, wie die zusätzliche Lücke von 1,2 Punkten geschlossen wird: (a) über die Dividende (etwa −10 %), (b) über weitere Bausteine, (c) über eine höhere Quote. Bis dahin keine neue Quote veröffentlichen.

---

## E2 · Regel der Dividende

**Ausgangslage.** Konzept und Webseite zeigen V3a (v3.20): Der Klubtopf wird nach Einwohnern × Preisniveau verteilt, die Kaufkraft ist in allen Ländern vom ersten Jahr an gleich. Die Leitlinie der Initiative (v3.29/v3.30) verlangt gleiches Recht, nationalen Ausgangspunkt und Angleichung über die Zeit, ohne Sonderregeln. Das entspricht V2.

| Land | V3a (geltend) | V2 (gleicher Anteil am eigenen BIP je Kopf) | Mindestdividende (halbes Existenzminimum am Wohnort) |
|---|---|---|---|
| DK | 773 | 823 | 701 |
| IE | 765 | 1.280 | 693 |
| NL | 655 | 762 | 594 |
| AT | 648 | 662 | 587 |
| BE | 643 | 643 | 582 |
| DE | 591 | 637 | 535 |
| FR | 584 | **524** | 529 |
| EE | 523 | **357** | 473 |
| SI | 493 | **389** | 446 |
| ES | 491 | **401** | 445 |

Fett: unter der Mindestdividende. Eigener Anreiz (Anteil eines zusätzlichen Euro BIP, der in die eigene Dividende zurückfließt): V3a DE 33 %, FR 27 %, ES 16 %, kleine Länder unter 1 %; V2 100 %.

| Option | Inhalt | Folge |
|---|---|---|
| **V3a** beibehalten | Kaufkraft sofort gleich | entspricht nicht der Leitlinie; schwacher eigener Anreiz |
| **V2**, Mindestdividende nur als Rechenkriterium im Klubschnitt | gleiches Recht, keine Sonderregel; Irland ohne Sonderbehandlung | FR, ES, SI, EE 2028 unter der Mindestdividende; mit Angleichung (Szenario) bis etwa 2045 nur noch Estland. Die Entscheidung v3.20 („die Quote sichert die Mindestdividende in jedem Jahr“) gilt dann für den Klubschnitt, nicht je Land |
| **V2B**, Mindestdividende als Zusage je Land | wie V2, Aufstockung von den übrigen Ländern getragen (1,9 % des Topfes 2028) | eine Sonderregel; widerspricht der Klarstellung v3.30 |

**Empfehlung: V2 mit Mindestdividende als Rechenkriterium im Klubschnitt.** Im Text offen sagen, dass vier Länder zu Beginn darunter liegen und Nachteile von Regionen über die Förderkulissen der EU und niedrigere Produktionskosten ausgeglichen werden.

---

## E3 · Gemeindeformel

**Ausgangslage.** Die Webseite zeigt einen klubweiten Betrag: 3.599 € je Einwohner und 12.625 € je Kind im Jahr. Die Entscheidung v3.17 nennt die Pro-Kopf-Variante je Land (10,35 % des eigenen BIP je Kopf).

| Land | je Einwohner (Land) | je Kind (Land) | Budget je Kopf (Land) |
|---|---|---|---|
| IE | 7.863 | 27.583 | 12.237 |
| DK | 5.056 | 17.738 | 7.869 |
| NL | 4.680 | 16.417 | 7.283 |
| AT | 4.064 | 14.259 | 6.326 |
| BE | 3.950 | 13.856 | 6.147 |
| DE | 3.913 | 13.729 | 6.091 |
| FR | 3.222 | 11.304 | 5.015 |
| ES | 2.463 | 8.640 | 3.833 |
| SI | 2.393 | 8.394 | 3.724 |
| EE | 2.194 | 7.698 | 3.415 |
| Klub (Webseite) | 3.599 | 12.625 | 5.601 |

**Empfehlung: Pro-Kopf-Variante je Land** (wie v3.17). Sie folgt derselben Logik wie V2 (gleiche Regel, eigener Ausgangspunkt, voller eigener Anreiz). Die Webseite zeigt dann für jede Sprachfassung die Beträge des Landes und den Klubschnitt zum Vergleich.

---

## E4 · Bestätigung: Klubquote der Staatsschulden 2028

Die Länderrechnungen für Frankreich, Spanien und die Niederlande zusammen (46 % des Klub-BIP) bewegen die Klubquote 2028 um +0,26 Punkte (81,55 statt 81,29 %). **Empfehlung: 81,3 % beibehalten**, die Länderprüfung im Text nennen.

---

## Was nach der Entscheidung folgt

1. Neurechnung der Gesamtrechnung (Konsumaufkommen, gegebenenfalls Quote und Dividende), Logbuch und Version.
2. Deutsche Fassung von Gesamtkonzept, Kurzfassung und Webseite als Entwurf zur Freigabe; neue Textteile: Länderstandard und Ländervergleich, Leitlinie zum nationalen Ausgangspunkt, Anreizwirkung über den Abgabenkeil, Label (Ressourcen sichtbar, regionale Wirkung nicht belegt).
3. Nach Freigabe: neue Version, fünf Sprachfassungen; vorher muttersprachliches Gegenlesen mindestens für Französisch und Polnisch (B16).

## Antwortbogen

| Punkt | Entscheidung |
|---|---|
| E1 Zuordnung | A / B / **C** / D |
| E1 Schließen der zusätzlichen Lücke | Dividende / weitere Bausteine / höhere Quote |
| E2 Dividende | V3a / **V2 (Klubschnitt)** / V2B |
| E3 Gemeinden | Klubformel / **je Land** |
| E4 Schuldenquote 2028 | **81,3 %** / 82,0 % |
