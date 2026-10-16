# Zusammenführung: Sozialschutz, Übergang und die Finanzierungsregel 28:28 (Stand v3.42, 16. Oktober 2026)

**Status: Prüfung und Vorbereitung einer Modellrechnung. Keine Zahl der Gesamtrechnung (Quote 30,2 %, Dividende) bewegt; entscheidet die Initiative.**
Grundlage: `Vorschlag-Generationenbaustein-2026-10-16.md` (Gemeinsames, Eigenes E, Zugesagtes Z), `Vorschlag-Huette-Route-Seil-Finanzierung-2026-10-16.md`
(Hütte, eigene Route, Seil), Rechnung `modell/sozialschutz.py` (+ `sozialschutz.toml`), Daten `daten/aggregate/sozialschutz_2024.json`, Faktencheck
`projekt/faktencheck_vorschlaege_2026-10-16.json`. Alle Eurostat-Werte über Web-Abruf am 16.10.2026, **maschinell aus dem Abruf gelesen, an der Quelle zu prüfen**.
Prozent des BIP, Durchschnitt der zehn Staaten BIP-gewichtet, soweit nicht anders angegeben.

---

## 1 | Ergebnis in fünf Sätzen

1. Beide Vorschläge treffen eine echte Lücke: Seit v3.1 liegt der Sozialschutz außerhalb des Rahmens (**20,07 %** des BIP, COFOG GF10, 2024); die Dividende ersetzt davon **11,86 %**. Bestandsgarantie und Härtefallfonds sind in keinem Rechenskript finanziert.
2. Der Engpass ist der Übergang, nicht der Dauerzustand: Nach dem Auslauf der Altansprüche kosten Dividende, eigene Route, Seil und Härtefall zusammen **19,33 %**, etwa so viel wie der Sozialschutz heute (20,07 %).
3. Die Altansprüche über der Dividende (Z) betragen 2028 rund **8,9 %** des BIP (Schätzung), bleiben bis etwa 2040 über 8 %, laufen bis etwa 2075 aus; das entspricht **60 %** aller heutigen Sozialbeiträge (14,88 %).
4. Die Regel 28:28 (höchstens 28 % auf Einkommen und auf Unternehmensgewinne) **kann bleiben, wenn Z und die Gesundheit nicht über die Steuern laufen**; über Steuern wären es 2028 rund 39,7 % Quote mit einer Deckungslücke von 9,3 Punkten, mit 65 % Gesundheit in der Hütte 44,8 % – mit den Sätzen von 28:28 nicht zu decken. Über neue Schuld finanziert, stiege die Schuldenquote bis 2069 um rund **223 Punkte**: nicht tragfähig.
5. Die veröffentlichte Aussage „Gesamtlast sinkt um 2,81 Punkte“ ist unvollständig, weil sie Z nicht enthält (**Korrektur 60**); mit Z, Pflicht-Route, Seil und Härtefall liegt die Last 2028 bei rund **54 %** gegen 40,76 % heute.

---

## 2 | Prüfung der beiden Vorschläge

### 2.1 Anwendbarkeit und Sinn

| Punkt | Generationenbaustein (E/Z) | Hütte · Route · Seil | Urteil |
|---|---|---|---|
| Lücke Rentenübergang benannt | ja, mit Rechenauftrag R-Z1 | ja, Schätzung 168 Mrd €/Jahr (DE) | **trifft zu**; Größenordnung siehe 3.2 (Z ist größer, weil die Dividende nur das halbe Existenzminimum deckt) |
| Gesamtlast-Aussage unvollständig | ja (1.3) | ja (Abschnitt 7) | **bestätigt**, Korrektur 60 |
| Dividende als Basisrente | ja | ja | **sinnvoll**, aber: die Hütte-Zuordnung (Alter 60 %, Hinterbliebene 60 %) verlangt **7,0 %** BIP für Ältere, die Dividende bringt den über 65-Jährigen nur rund **2,7 %**. Entweder Route größer oder Basisrente über der Dividende (Sonderregel nach Alter, entscheiden) |
| Keine neuen Z-Ansprüche ab Stichtag, auch keine Beamtenpensionen | ja | – | **folgerichtig** (sonst wächst Z weiter); rechtlich offen (Art. 33 Abs. 5 GG) |
| Z territorial beim Ausgangsstaat | ja | nein (gemeinsames Aufkommen + Schuld) | **territorial empfohlen**: gleiche Logik wie Altschulden (Aufschlag) und Leitlinie „nationaler Ausgangspunkt“; Z 2028 je Land zwischen 0 (DK) und 14,0 % (AT) – gemeinsam getragen wäre das ein großer Transfer zwischen Staaten |
| Bilanzregel 50:50, Ankündigungsregel 15/5 Jahre | ja | Kandidat (c) | **übernehmen** als Regel für Z; Belege Schweden und Dänemark bestätigt (Faktencheck 5, 6) |
| Seil: Pflichtversicherung mit Aufnahmezwang | – | ja | **sinnvoll**; nicht Steuer, aber Pflichtzahlung: gehört in jede Gesamtlast-Aussage |
| Gesundheit „mitteleng“ (65 % über Hütte) | – | ja | **nicht mit 28:28 vereinbar**, wenn die Hütte aus Steuern zahlt (+5,0 Punkte Quote). Vereinbar, wenn der Hütte-Anteil über eine eigene, zweckgebundene Gesundheitsabgabe oder einen Hochkostenpool im Seil läuft |
| Härtefall H1–H4 | – | ja | **notwendig** (heute unfinanziert). H2 (50 % Anrechnung) wirkt als Grenzbelastung von 50 % im Leistungsbezug und widerspricht der Aussage „von jedem Euro bleiben mindestens 72 Cent“ – Satz oder Aussage anpassen |
| Rechtliche Einordnung | Art. 14, 33 GG | Art. 14 GG | juristisch zu prüfen; BVerfGE 53, 257 präzisiert (Faktencheck 16) |

### 2.2 Faktencheck der Sekundärangaben (Auszug; vollständig in der JSON-Datei)

| Angabe in den Vorschlägen | Verdikt | Richtig / Hinweis |
|---|---|---|
| Sozialbudget 2024: 1.345,4 Mrd €, 31,2 % | nur Sekundärquelle | BMAS-Original nicht gelesen; Werte vorläufig |
| Nicht beitragsgedeckte Leistungen 68 / 124 Mrd €, Bundeszuschuss 84 Mrd € | bestätigt | 2023: 68,3 / 124,2 / 84,3 Mrd € (WD 6, 21.07.2026, nach DRV Bund) |
| Beitragssatz 18,6 → 19,8 → 20,1 → 21,2 % | bestätigt | Rentenversicherungsbericht 2025 (dazu 20,0 % 2029) |
| Beamtenversorgung > 63 Mrd € | bestätigt | Destatis PM 455/2025: 2024 56,9 Mrd € Pensionen + 9,0 Mrd € Hinterbliebene; Abgrenzung 63,4 gegen 65,9 Mrd € offen |
| Schweden 1,1695 | bestätigt | Berechnungsjahr 2024, Bremse nicht aktiv |
| Dänemark 70 ab 2040, 81:21 | bestätigt | Stimmenzahl nur aus Agenturmeldung |
| Frankreich: Einfrieren bei 62 J. 9 Mon. | **abweichend** | Gesetz 2025-1403, Art. 105: ein Quartal weniger für die Jahrgänge 1964–1968, Pause bis 1.1.2028 |
| Teuerste 10 % ≈ 60 % der Ausgaben | bestätigt | bifg (Wende/Schmitt 2021, BARMER-Daten) |
| RAND (Manning u. a. 1987) | **abweichend** | Aussagen stimmen, Quellen sind Lohr u. a. 1986 und Brook u. a. 1983 |
| NL Eigenrisiko 385 €, keine Mortalitätswirkung | bestätigt | Ayyagari/Salm/Sargent 2026, IZA DP 18420, nicht begutachtet |
| Genf 13,5 % gegen 8,7 % | bestätigt | Querschnitt, keine Kausalität |
| Patientenquittung wenig genutzt | nicht belegt | § 305 SGB V existiert; Nutzung: Annahme |
| Nichtinanspruchnahme 40–60 % (DIW) | **abweichend** | DIW: rund 60 % Grundsicherung im Alter; 55,7 % ALG II (Harnisch 2019) |
| Chile 5 % → 1,6 % | bestätigt | Diamond 2016; amtlicher Wert 2012 nicht gefunden |
| Nächste Korrekturnummer 59 | **falsch** | nächste freie Nummer laut CLAUDE.md: 60 |
| Projektsteuerung „Geltende Fassung“ veraltet | **bestätigt**, behoben (v3.42) | |

---

## 3 | Rechnung (Vorbereitung, `modell/sozialschutz.py`)

### 3.1 Sozialschutz heute und die Schichten (Setzung der Zuordnung nach dem Hütte-Vorschlag)

| COFOG | Inhalt | % BIP 2024 | Hütte / Route / Seil (%) |
|---|---|---|---|
| GF1001 | Krankheit und Invalidität (Geldleistungen) | 3,14 | 70 / 0 / 30 |
| GF1002 | Alter | 10,24 | 60 / 40 / 0 |
| GF1003 | Hinterbliebene | 1,45 | 60 / 0 / 40 |
| GF1004 | Familie und Kinder | 2,00 | 95 / 0 / 5 |
| GF1005 | Arbeitslosigkeit | 1,46 | 25 / 0 / 75 |
| GF1006–1009 | Wohnen, soziale Ausgrenzung, Übriges | 1,77 | 100 / 0 / 0 |
| **GF10** | **Sozialschutz** | **20,07** | **Hütte 13,26 · Route 4,10 · Seil 2,72** |

Dividende 11,86 % gegen Hütte-Bedarf 13,26 %: Differenz 1,40 Punkte, vor allem weil die Dividende allen gleich zahlt und Ältere nur ihren Anteil erhalten.
Gesundheit (GF07) 7,75 % liegt heute vollständig außerhalb der Steuern.

### 3.2 Zugesagtes (Z): Pfad der Altansprüche (Rechenauftrag R-Z1, vereinfacht)

Methode (Schätzung): Rentenausgaben (GF1002 + GF1003) je Person über 65; je Rentnerjahrgang der Anteil der Erwerbsjahre vor dem Stichtag 2028
(Erwerb 20–65, Bezug 22 Jahre, Annahmen); Z = erworbener Anspruch über der Dividende eines Erwachsenen; Zahl der Rentner nach dem Ageing Report 2024
(Länderberichte); Skalierung auf die erworbenen Ansprüche der Volkswirtschaftlichen Gesamtrechnungen (Tabelle 29, 2021), wo diese kleiner sind (Dänemark 0,12).
Gegenprobe: Der Barwert der vor dem Stichtag erworbenen Renten (1 % Diskont) liegt für DE bei 329 % des BIP, FR 413 %, AT 438 % – Tabelle 29: 320 / 397 / 450 %.

| Jahr | 2028 | 2030 | 2035 | 2040 | 2045 | 2050 | 2060 | 2070 | 2075 |
|---|---|---|---|---|---|---|---|---|---|
| Z, % BIP | 8,86 | 8,93 | 8,78 | 8,31 | 7,39 | 6,16 | 3,46 | 0,90 | 0,02 |

Z 2028 je Land: AT 14,0 · FR 11,4 · ES 10,6 · BE 9,3 · SI 9,2 · DE 9,0 · EE 5,8 · NL 3,8 · IE 1,4 · DK 0,0 % des eigenen BIP.
**Grenze:** Durchschnittsrentner statt Verteilung; Z wird in späteren Jahren unterschätzt (Einzelne mit hohen Ansprüchen bleiben über der Dividende).

### 3.3 Wirkung auf Quote und Gesamtlast (2028)

| Finanzierung | Quote 2028 | Deckungslücke | Urteil |
|---|---|---|---|
| bisher (ohne Z, ohne Härtefall) | 30,2 | −0,24 (Überschuss) | Gesamtrechnung |
| Z und Härtefall aus Steuern, Gesundheit außerhalb | 39,7 | 9,3 | mit 28:28 nicht zu decken |
| dazu Gesundheit 50 / 65 / 90 % über Hütte (Steuern) | 43,6 / 44,8 / 46,7 | 13,2 / 14,3 / 16,3 | nicht zu decken |
| Z über neue Schuld | 30,9 (nur Härtefall) | 0,4 | Schuldenquote +223 Punkte bis 2069: nicht tragfähig |
| **Z über einen eigenen, sinkenden Übergangsbeitrag (territorial), Gesundheit und Seil als Prämien** | **30,2 + Härtefall** | **Härtefall zehrt Überschuss und Reserve auf** | **28:28 bleibt; ehrliche Gesamtlast nötig** |

Gesamtlast: heute 40,76 %; bisherige Aussage 37,95 %; mit Z, Pflicht-Route, Seil und Härtefall **2028 rund 54 %**; nach dem Auslauf von Z im Sozialschutz etwa wie heute.
Zum Vergleich: Ein Punkt Quote entspricht im Label rund 2,6 Punkten aller Mehrwertsteuersätze (Label +1 = 0,38 % BIP, `justierung.json`).

---

## 4 | Zusammengeführter Baustein (Vorschlag)

**Bild und Fachbegriffe:** Hütte · eigene Route · Seil als Bild der Gesamtstruktur; **Gemeinsames = Hütte = Dividende** (plus Härtefall); **Eigenes (E) = eigene Route**;
**Seil** = Pflichtversicherung; **Zugesagtes (Z)** als Fachbegriff für den Übergang. Keine Kollision mit Dach, Gemeinde, Mindestniveau.

| Schicht | Inhalt | Finanzierung | in der Quote? |
|---|---|---|---|
| Hütte | Dividende (alle, auch Basisrente); Härtefall-Tür (H1–H4) | Steuern | **ja** (Härtefall neu: 0,3–1,0 % BIP, zu rechnen) |
| eigene Route (E) | kapitalgedeckte Vorsorge, Standardweg mit Austrittsrecht oder Pflicht (H-6) | eigene Beiträge, Arbeitgeber | nein; als Pflicht in der Gesamtlast |
| Seil | Gesundheit (gewöhnliche Behandlung, Selbstbehalt mit Belastungsgrenze), Hochkostenpool, Invalidität und Hinterbliebene über der Dividende, Lohnersatz bei Arbeitslosigkeit | Pflichtprämie, Aufnahmezwang | nein; in der Gesamtlast |
| Zugesagtes (Z) | Altansprüche zum Stichtag (Rentenversicherung, Beamtenversorgung), keine neuen | **Übergangsbeitrag beim Ausgangsstaat**, sinkend mit Z, Bilanzregel 50:50, Ankündigungsregel 15/5 | nein; eigener, sichtbarer Posten |

---

## 5 | Was das für die Finanzierungsregel 28:28 bedeutet

1. **Die Regel bleibt haltbar** – höchstens 28 % auf Einkommen, 28 % auf Unternehmensgewinne –, aber nur als Regel für die **Steuern**. Sie trägt die Hütte (Dividende, Gemeinden, Dach), nicht den Übergang und nicht die Gesundheit.
2. **Der Übergang braucht eine dritte, befristete Finanzierung**: Z kostet anfangs so viel wie heute 60 % aller Sozialbeiträge und sinkt bis etwa 2075 auf null. Der Satz „keine Sozialabgaben“ gilt deshalb erst im Dauerzustand; bis dahin: „ein sinkender Übergangsbeitrag für alte Zusagen, offen ausgewiesen“.
3. **Wer heute jung ist, zahlt doppelt** (eigene Route und Übergangsbeitrag). Das ist die bekannte Last jedes Systemwechsels (Chile, Schweden); Bilanzregel und Kohortenregel verteilen sie, beseitigen sie nicht.
4. **Die Aussage zur Gesamtlast ist zu ersetzen** (Korrektur 60): statt „sinkt um 2,81 Punkte“ ein Vergleich, der Z, Pflicht-Route und Seil enthält.
5. **Härtefall in die Quote**: Mit 0,3 bis 1,0 % BIP zehrt er Überschuss (0,24) und Stabilitätsreserve (0,84) auf; Stabilitätskriterium neu prüfen.

---

## 6 | Vorbereitete Modellrechnung und nächste Schritte

| Schritt | Inhalt | Status |
|---|---|---|
| R-Z1 | `modell/sozialschutz.py`, `daten/aggregate/z_pfad.csv` (je Land und Jahr) | Schätzung vorhanden; verfeinern: Rentenverteilung, Rentenzugänge (`spr_pns_*`), Sterbetafeln |
| Übergangsbeitrag | Satz in % der Lohnsumme je Land und Jahr | Arbeitnehmerentgelt je Land fehlt (Eurostat `nama_10_gdp`, D1) |
| Härtefall | Grundsicherung über der Dividende aus GF1006/GF1007 und Leistungsstatistik | Annahme 0,3–1,0 |
| Seil-Prämie | je Kopf aus Seil-Anteil und Gesundheit, mit Belastungsgrenze | Vorschlag: ≈121 €/Monat (DE, ungeprüft) |
| Gesamtrechnung | Z als eigener territorialer Posten neben dem Aufschlag; Härtefall als Posten des Daches oder der Gemeinde | nach Entscheidung |
| Texte | Gesamtlast-Aussage, „keine Sozialabgaben“, Rechner („Sozialabgaben 0“), Steuerpflicht der Dividende (offen seit v3.41) | nach Entscheidung |

### Antwortbogen (zusammengeführt aus G1–G9 und H-1–H-10)

| Punkt | Entscheidung |
|---|---|
| S1 Zusammengeführten Baustein aufnehmen (Abschnitt 4) | ja / überarbeiten |
| S2 Begriffe: Hütte/Route/Seil als Bild, E/Z als Fachbegriffe | ja / andere |
| S3 Stichtag | 2028 / 2030 / mit Beitritt |
| S4 Keine neuen Z-Ansprüche, auch keine neuen Beamtenpensionen | ja / nein |
| S5 Finanzierung Z: Übergangsbeitrag territorial (empfohlen) / Steuern / Mischung mit Schuld (Anteil ___) | |
| S6 Bilanzregel 50:50, Ankündigungsregel 15/5 Jahre, Generationenprüfung mit aufschiebendem Veto | ja / andere |
| S7 Basisrente = Dividende (gleiches Recht) oder Aufstockung für Ältere über der Dividende | Dividende / Aufstockung |
| S8 Gesundheit: Hütte-Anteil über Steuern (Quote +3,9 bis +7,0) oder über Prämie/Gesundheitsabgabe | Steuern / Prämie |
| S9 Selbstbehalt mit Belastungsgrenze; keine Selbstbehalte für Kinder und Prävention | ja / ___ |
| S10 Eigene Route: Pflicht oder Standardweg mit Austrittsrecht | Pflicht / Standardweg |
| S11 Härtefall H1–H4; Anrechnungssatz H2 (50 % widerspricht „72 Cent“) | 50 % / ___ |
| S12 Gesamtlast-Aussage bis zur Rechnung zurückziehen (Korrektur 60) | ja / nein |
| S13 Rechnung freigeben (R-Z1 verfeinert, Übergangsbeitrag, Härtefall, Seil-Prämie) | ja / nein |
