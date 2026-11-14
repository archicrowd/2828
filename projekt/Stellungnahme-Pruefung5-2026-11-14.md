# Stellungnahme zur Dokumentenprüfung vom 14. November 2026

Initiative 28:28 · 14. November 2026 · Modellstand v4.82 · Bezug: `Pruefbericht-Dokumentenpruefung-2026-11-14.md` (KI-Prüfung im Projektraum,
Gegenstand Stand v4.72; interne Prüfung).

## 1 Entscheidungen der Initiative (14.11.2026)

1. **Fondszins:** 2,45 % bleibt Grundpfad. Der Satz ist aus dem Mittel 2006–2025 hergeleitet; ein kurzfristiger Marktwert gibt den Zins über die
   Laufzeit bis 2098 nicht besser wieder. 3,0 / 3,5 / 4,0 % bleiben als Empfindlichkeit ausgewiesen (Empfehlung 2 nicht übernommen).
2. **Ort der Präzisierungen:** Kennzahlen, Konzept, Working Paper und Prüfunterlagen. Die Webseite dient der Erstinformation und bleibt ohne diese
   Einzelheiten (Empfehlungen 3 und 4 dort nicht umgesetzt).

## 2 Befunde und Umsetzung

| Befund | Bewertung | Umsetzung |
|---|---|---|
| B-1 Aufkommen in vier Positionen nicht gedeckt (hoch) | berechtigt; Größe offen | v4.82: in Kennzahlen, Konzept (Abschnitt 8) und Working Paper als offen gekennzeichnet. Beleg gegen Kassenstatistik und Eurostat einzeln, danach Dividende als Band: nächster Schritt |
| B-2 Erbschaftsbasis falsch bezeichnet, Basisjahr Ausreißer (mittel) | **zutreffend, eigener Fehler (Korrektur 88)**; an Destatis PM 306/2026 nachgelesen: 150,5 Mrd. € = steuerlich berücksichtigtes Vermögen (nach Nachlassverbindlichkeiten, vor Freibeträgen, nur Fälle mit festgesetzter Steuer); Anstieg vor allem durch Übertragungen ab 20 Mio. € (+146,8 % Steuer) | v4.82: Bezeichnung korrigiert (`vermoegensbasis33`), Status „offen“; aus 2024 fortgeschrieben 127 statt 164 Mrd. € gegen nötige 173 Mrd. €. Mehrjahresmittel: nächster Schritt |
| B-3 Umrechnung nicht dokumentiert (mittel) | **zutreffend, Fehler der Dokumentation (Korrektur 87)**, nicht der Rechnung: Die Rechnung nutzt die Werte des Kernmodells beim Satz 28 % (48,8 / 157,6 / 35,9 Mrd. €, Konsum 375,9 Mrd. € bei 20 % brutto) und hebt mit 33/28; die Kennzahlen nannten ältere Werte (45 / 145 / 33 Mrd. € bei 25 %, 350 Mrd. € bei 18 %). Daraus erklären sich 1,37 / 4,42 / 8,51 | v4.82: Herleitung in `KENNZAHLEN.md` |
| B-4 Gesamtlast nur als Kassenvergleich richtig (hoch) | zutreffend | v4.82: Zitierregel in den Kennzahlen; Konzept und Working Paper nennen die Neuaufnahme des Fonds 2028 (6,90 % BIP) und 45,58 % ohne Streckung |
| B-5 Fondszins unter Marktniveau (hoch) | Einwand verstanden, nicht übernommen (Entscheidung 1) | Lesart in den Kennzahlen: Bei Zins unter dem Wachstum entlastet die Streckung, sonst verschiebt sie Last |
| B-6 Drei Kernaussagen zu weit gefasst (mittel) | zutreffend für die ausführlichen Papiere | v4.82: Tabelle „Geltungsbereich der Kernaussagen“ in den Kennzahlen; Konzept (Kurzfassung, Abschnitt 8) und Working Paper |
| B-7 Allgemeingültigkeit nicht gezeigt (mittel) | zutreffend; bekannt als R4–R6 | offen; die Länderwerte v3.53 (eigene Steuerbasis) sind vor Stand C entstanden und neu zu rechnen |
| B-8 Reichweite der Prüfungen (Hinweis) | zutreffend | spricht für eine externe Prüfung der Eingangswerte |

## 3 Hinweise zum Prüfbericht

- Der Bericht prüft v4.72. Seitdem gelten der Fonds 50/50 und die Gemeinschaft der Staaten (v4.74–v4.80); die Fondszahlen je Staat sind noch nicht in
  die Haushaltsrechnungen übernommen (R1).
- Rentnerhaushalte: Der Bericht nennt −116 € (Rechnung der Rentnerregel, `rentner_kombi.json`); die eigene Population zeigt −125 € (`mikro_de.json`).
  Beide gelten unter BS35; die Abgrenzungen sind verschieden.
- Die externen Werte des Berichts zur Kassenstatistik und zur Anleiherendite sind Sekundärquellen und hier noch nicht nachgelesen.

## 4 Nächste Schritte

1. Vier Positionen aus B-1 einzeln belegen (Kassenstatistik BMF 2024/2025, Eurostat `gov_10a_taxag`); Dividende als Band.
2. Erbschaften: Mittel der Jahre 2021–2025 als Basis.
3. Konzept nach den Spielregeln v4.80 nachführen: Abschnitt 3.6, 4 und 8 sprechen noch vom „gemeinsamen Dach“.
