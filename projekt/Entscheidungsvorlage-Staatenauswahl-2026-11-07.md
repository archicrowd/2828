# Entscheidungsvorlage: Staatenauswahl nach Rechtsstaatlichkeit und den Grundlagen der Vereinten Nationen

Initiative 28:28 · 7. November 2026 · Modellstand v4.73 · Vorbereitung, kein Beschluss · Rechnung: `modell/staatenauswahl.py`

## 1 Auftrag und Ausgangslage

**Auftrag (7.11.2026):** Die Auswahl der Staaten soll sich an Rechtsstaatlichkeit ausrichten und stärker an den Übereinkommen der Vereinten
Nationen, an der UN-Charta und an den Zielen für nachhaltige Entwicklung.

**Heute:** Das Modell rechnet mit den 30 Staaten von EU, EWR und Schweiz (Fonds der 30, Beschluss 21.10.2026). Die Auswahl folgt der Geografie.
Die Regeln selbst sind nicht an Europa gebunden: Tarifstufen, Dividende, Netz und die Rentnerregel BS35 sind in Vielfachen des Grundbedarfs
jedes Staates formuliert. Die Forschungsseite nennt eine Auswahl nach Rechtsstaatlichkeit bisher nur als Möglichkeit.

**Bezugsrahmen der Vereinten Nationen:**
- UN-Charta: Art. 1 Abs. 3 (Zusammenarbeit bei wirtschaftlichen und sozialen Fragen, Achtung der Menschenrechte), Art. 55 und 56
  (Lebensstandard, Vollbeschäftigung, sozialer Fortschritt; Pflicht zur Zusammenarbeit), Art. 33 (friedliche Streitbeilegung).
- Die sieben Kernabkommen der Menschenrechte mit allgemeiner Verbreitung: ICERD, ICCPR, ICESCR, CEDAW, CAT, CRC, CRPD. Zwei weitere
  Kernabkommen sind wenig verbreitet: CMW (Wanderarbeitnehmer) und CPED (Verschwindenlassen).
- Agenda 2030 (Resolution A/RES/70/1) mit den 17 Zielen; Freiwillige Nationale Berichte (VNR) an das Hochrangige Politische Forum.
- Daneben: Pariser Abkommen (Klima), die zehn grundlegenden Übereinkommen der ILO.

Die Fundstellen der Charta sind eigene Kenntnis und am Text zu prüfen.

## 2 Erste Durchsicht (Rechnung `staatenauswahl.py`)

**Datenlage.** Alle Werte sind maschinell aus Webseiten und PDF gelesen und an der Quelle zu prüfen.
- **WJP Rule of Law Index 2025:** 143 Staaten, Gesamtwert 0–1. Nichtstaatliche Quelle (World Justice Project). Schweiz und Island sind nicht
  erfasst.
- **SDG Index 2026:** SDSN, Sustainable Development Report 2026, 193 Staaten. Nichtamtlich (SDSN arbeitet im Umfeld der UN, ist aber keine
  UN-Statistik).
- **UN-Mi 2026:** Index der Unterstützung des UN-gestützten Multilateralismus, ebenfalls SDSN.
- **Kernabkommen:** Für den ICESCR ist der Status an der UN Treaty Collection geprüft (maschinell gelesen). Die übrigen sechs Abkommen sind eigene
  Kenntnis und zu prüfen.

**Stufen nach den Vorschlagsschwellen** (Kern WJP ≥ 0,75 · Teilnahme ≥ 0,66 · Partner ≥ 0,55; alle sieben Kernabkommen ratifiziert):

| Stufe | Staaten des Fonds der 30 | Staaten außerhalb Europas (Auswahl) |
|---|---|---|
| Kern | AT, BE, DE, DK, EE, FI, IE, LT, LU, NL, NO, SE | AU, CA, JP, NZ, UK |
| Teilnahme | CY, CZ, ES, FR, IT, LV, MT, PL, PT, SI | BB*, CL, CR, KR, UY |
| Partner | BG, EL, HR, RO, SK | MU |
| unter der Partnerschwelle | HU (0,50) | – |
| ohne WJP-Wert | CH, IS | – |
| Kernabkommen nicht alle ratifiziert | – | BW (6 von 7), SG (4), US (3) |

\* Barbados: Stand der Kernabkommen unbekannt.

**Befunde:**
1. **Sechs Staaten des Fonds liegen unter 0,66:** SK 0,64, HR 0,61, RO 0,61, EL 0,60, BG 0,55, HU 0,50. Zusammen tragen sie 5,7 % des BIP der 30.
2. **Fünf Staaten außerhalb Europas erreichen den Kern:** Neuseeland, Australien, Kanada, das Vereinigte Königreich und Japan.
3. **Die Vereinigten Staaten** haben vier der sieben Kernabkommen nicht ratifiziert (ICESCR, CEDAW, CRC, CRPD; ICESCR geprüft, die übrigen eigene
   Kenntnis). Ihr UN-Mi ist 1,7 von 100, Rang 193.
4. **Der Fonds hängt an der Auswahl.**

   | Fondsvariante | Staaten | Beitrag | Zuschlag auf alle Steuern |
   |---|---|---|---|
   | alle 30 (geltend) | 30 | 5,15 % des BIP | 15,4 % |
   | ohne die sechs Staaten unter 0,66 | 24 | 5,19 % | 15,5 % |
   | nur der Kern, mit CH und IS | 14 | 4,09 % | 12,3 % |

   Der Kern ist billiger, weil Frankreich, Italien und Spanien mit hohen Altlasten wegfallen. Eine Auswahl nach Rechtsstaatlichkeit würde so
   zugleich zu einer Auswahl nach Schulden. Das ist ein Fehlanreiz.
5. **Der SDG Index bevorzugt Staaten mit hohem Einkommen.** Unter 75 Punkten liegen nur Staaten außerhalb Europas: BB, BW, CR, MU, SG.
6. **Der UN-Mi passt nicht als Schwelle.** Er bewertet einseitige Sanktionen, Rüstung und das Stimmverhalten in der Generalversammlung. Danach
   steht Frankreich auf Rang 178, das Vereinigte Königreich auf 162 und Barbados auf Rang 1. Diese Teile sind politische Wertungen, keine
   Rechtsstaats- oder Sozialstandards.

## 3 Entscheidungsvorlagen

### EV1 Leitbild der Staatengruppe

| Option | Inhalt | Bewertung |
|---|---|---|
| A | Geografie bleibt (EU, EWR, CH) | rechtlich einfach, aber nicht universell; Rechtsstaat nicht Maßstab |
| **B** | **offene Regelgemeinschaft der Staaten, die die UN-Charta, die Kernabkommen und die Agenda 2030 verbindlich umsetzen; Auswahl nach prüfbaren Kriterien** | universell, folgt dem Auftrag; braucht Daten und ein Verfahren |
| C | B, aber mit Bestandsschutz für die 30 bis zum ersten Prüfzyklus | wie B, mit weichem Übergang |

**Empfehlung: C.** Sie folgt dem Auftrag und vermeidet einen Bruch im gerechneten Fonds.

Vorgeschlagener Kernsatz: „Die Regeln gelten für jeden Staat, der die Charta der Vereinten Nationen und die Menschenrechtsabkommen einhält und
die Ziele für nachhaltige Entwicklung verfolgt.“

### EV2 Aufbau der Kriterien

| Option | Inhalt |
|---|---|
| A | nur gemessene Werte (Indizes) mit Schwellen |
| B | Punktesystem aus mehreren Indizes |
| **C** | **drei Ebenen: (1) Pflicht, völkerrechtlich und ja/nein: UN-Mitglied, Kernabkommen, Pariser Abkommen; (2) Rechtsstaat, gemessen, mit Schwellen für die Stufe; (3) Nachhaltigkeit als Verpflichtung, nicht als Rang** |

**Empfehlung: C.** Ebene 1 lässt sich am Vertragsregister prüfen. Ebene 2 trennt die Stufen. Ebene 3 benachteiligt ärmere Staaten nicht.

### EV3 Maß der Rechtsstaatlichkeit und Schwellen

| Option | Quelle | Vorteil | Nachteil |
|---|---|---|---|
| A | WJP allein | ausführlich (8 Faktoren), jährlich | nichtstaatlich, Befragung; CH und IS fehlen |
| **B** | **WJP und WGI „Rule of Law“ (Weltbank)** | **zwei unabhängige Quellen, WGI deckt alle Staaten ab** | WGI beruht ebenfalls auf Wahrnehmungen |
| C | EU-Rechtsstaatsbericht | amtlich | nur EU, kein Zahlenwert |

**Empfehlung: B**, mit der Regel: Eine Stufe gilt, wenn beide Quellen sie tragen; weichen sie ab, wird geprüft. Die WGI-Werte sind noch nicht
beschafft, die Schnittstelle der Weltbank war aus der Arbeitsumgebung nicht erreichbar.

Schwellen zur Entscheidung:
- **Kern ≥ 0,75:** 12 Staaten des Fonds, 5 außerhalb Europas.
- **Teilnahme ≥ 0,66:** weitere 10 bzw. 5.
- **Partner ≥ 0,55:** weitere 5 bzw. 1.

### EV4 UN-Abkommen als Pflicht

| Option | Inhalt | Wirkung |
|---|---|---|
| **A** | **sieben Kernabkommen ratifiziert** | alle 30 erfüllen; US, SG, BW nicht |
| B | alle neun Kernabkommen | die CMW hat kein EU-Staat ratifiziert (eigene Kenntnis, zu prüfen); schlösse ganz Europa aus |
| C | A und die Individualbeschwerde (Fakultativprotokolle zu ICCPR, CEDAW, ICESCR) für den Kern | stärker; Daten zu erheben |

Ergänzend zu entscheiden:
- **Pariser Abkommen:** Pflicht für alle.
- **ILO:** grundlegende Übereinkommen, Vorschlag mindestens 8 von 10.
- **Internationaler Gerichtshof:** Unterwerfungserklärung nach Art. 36 Abs. 2 IGH-Statut als Merkmal des Kerns (friedliche Streitbeilegung,
  Art. 33 der Charta). Noch nicht erhoben.

**Empfehlung: A**, mit dem Pariser Abkommen als Pflicht. ILO und IGH-Erklärung werden ausgewiesen, aber nicht als Pflicht verlangt, bis die Daten
vorliegen.

### EV5 Ausrichtung an den Zielen für nachhaltige Entwicklung

| Option | Maß | Bewertung |
|---|---|---|
| A | SDG Index ≥ 75 | schließt ärmere Staaten aus (BB, BW, CR, MU, SG); bevorzugt hohes Einkommen |
| **B** | **Verpflichtung: Freiwilliger Nationaler Bericht in den letzten vier Jahren; Verbesserung in den eigenen Werten; Staaten mit hohem Einkommen: Entwicklungsleistung auf dem Pfad zu 0,7 % des BNE (S6)** | universell, fördert Entwicklung statt Rang |
| C | UN-Mi als Schwelle | ungeeignet, siehe Befund 6 |

**Empfehlung: B.** SDG Index und UN-Mi werden ausgewiesen, aber nicht als Schwelle verwendet. Der Teil des UN-Mi zu ratifizierten UN-Verträgen
kann die Prüfung von EV4 stützen.

### EV6 Staaten des Fonds unter der Teilnahmeschwelle (SK, HR, RO, EL, BG, HU)

| Option | Inhalt | Wirkung auf den Fonds |
|---|---|---|
| **A** | **Bestandsschutz mit Prüfpfad: Teilnahme am Regelwerk und am Fonds bleibt; Stufe „Partner“; Ziel ≥ 0,66 binnen zweier Prüfzyklen** | keine; Fonds der 30 bleibt (5,15 %) |
| B | Teilnahme am Fonds bleibt, am Regelwerk ruht | Fonds unverändert; die Regeln gelten dort nicht |
| C | Ausschluss | Fonds der 24: 5,19 % / 15,5 %; Griechenland trägt seine Altlast (eigener Beitrag 6,81 % des BIP) allein |

**Empfehlung: A.** Für Ungarn (0,50, unter der Partnerschwelle) zusätzlich eine Auflage nach EV8.

### EV7 Regelwerk und Fonds trennen

| Option | Inhalt |
|---|---|
| A | Fondsteilnahme folgt der Stufe (nur der Kern im Fonds) |
| **B** | **Regelwerk nach Stufen, Fonds nach Währungsraum: gemeinsame Regeln, je ein Fonds je Währungsraum; Teilnahme für alle Staaten ab Stufe Partner, die den Pflichtteil (EV4) erfüllen** |

**Empfehlung: B.** Option A hätte den Fehlanreiz aus Befund 4: Ein Fonds nur des Kerns kostet 4,09 statt 5,15 % des BIP. Rechtsstaatlichkeit soll
nicht zum Mittel werden, Schulden auszulagern. Option B löst zugleich das Wechselkursrisiko mit Staaten außerhalb des Euro.

### EV8 Verfahren

Vorschlag zur Entscheidung:
- **Prüfzyklus:** alle zwei Jahre, mit den Daten des Vorjahres, öffentlich in einem Register aller Werte und Quellen.
- **Wechsel der Stufe:** erst nach zwei Zyklen in Folge. Das verhindert, dass ein Staat wegen einer einzelnen Messung die Stufe wechselt.
- **Unterschreitung des Pflichtteils** (Kündigung eines Kernabkommens, Bruch der Charta nach Feststellung eines UN-Organs oder des IGH): Die
  Stufe ruht, der Fonds bleibt bestehen.
- **Einspruch:** Der Staat kann eigene Daten vorlegen, die öffentlich geprüft werden.
- **Kriterien gelten ohne Ansehen des Staates:** Kein Staat wird genannt, Ausnahmen gibt es nicht.

### EV9 Nächste Rechen- und Datenschritte

1. WGI „Rule of Law“ für alle Staaten beschaffen (Weltbank, Datensatz WGI 2025); Status der sieben Kernabkommen, des Pariser Abkommens, der
   ILO-Übereinkommen und der IGH-Erklärung aus den amtlichen Registern (UN Treaty Collection, ILO NORMLEX).
2. Ländermodelle für den Kern außerhalb Europas, zuerst UK, CA, AU, NZ, JP. Grundlage sind OECD Taxing Wages und die amtlichen Dezile, für die
   Rentenzusagen OECD Pensions at a Glance (Lücke, Ersatz für Eurostat Tabelle 29).
3. Fonds je Währungsraum rechnen (EV7).
4. Texte: Forschungsseite, Working Paper und Webseite erst nach dem Beschluss.

## 4 Kritische Punkte

- **Indizes:** Alle sind Konstrukte mit Wertungen. WJP und SDSN sind nichtstaatlich; die WGI beruhen auf Wahrnehmungen. Zwei Quellen mindern das
  Risiko, beseitigen es nicht.
- **Ränder:** Schwellen auf zwei Stellen erzeugen Grenzfälle (PL und IT 0,66, SK 0,64). Deshalb sollen die Stufen erst nach zwei Zyklen wechseln.
- **EU-Recht:** Eine Stufung innerhalb der EU berührt Art. 2 und 7 EUV und die Gleichheit der Mitgliedstaaten. Das ist rechtlich zu prüfen (P1).
- **Europäische Rechtsstaatlichkeit:** Die WJP-Werte sind 2025 in mehr als zwei Dritteln der EU-Staaten gesunken (Euronews, 28.10.2025, nach
  WJP; Sekundärquelle). Die Auswahl kann sich also schnell ändern.

## 5 Quellen

- World Justice Project, Rule of Law Index 2025 (`worldjusticeproject.org/rule-of-law-index/downloads/WJPIndex2025.pdf`)
- SDSN, Sustainable Development Report 2026, Teil 2 (SDG Index, Abb. 2.3) und Teil 3 (UN-Mi, Abb. 3.1, 3.2)
- UN Treaty Collection, MTDSG Kapitel IV-3 (ICESCR), IV-13 (CMW), IV-16 (CPED)
- UN-Charta; A/RES/70/1
