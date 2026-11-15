# Beleg der vier Einnahmepositionen (Prüfbefund B-1): Ergebnis und Entscheidungsvorlage

Initiative 28:28 · 15. November 2026 · Modellstand v4.87 · Rechnung: `modell/einnahmen_belege.py` (+ `.toml`) → `daten/aggregate/einnahmen_belege.json`
Status: **Prüfrechnung; die geltende Deckung ist unverändert. Entscheidung der Initiative offen.**

## 1 Ergebnis in einem Satz

Die vier Positionen sind nach den amtlichen Daten zusammen um rund **2,1 Punkte des BIP** (Spanne 1,5 bis 2,5) zu hoch angesetzt. Das entspricht
2028 rund **108 € Dividende je Erwachsenem und Monat** (Spanne 77 bis 130 €; ohne Kinderanteil, Kaufkraft 2026). Die Dividende mit Kinderanteil
läge 2028 bei rund 262 € statt 364 €. Der Prüfer hatte 1 bis 2 Punkte geschätzt; das Ergebnis liegt am oberen Rand.

## 2 Je Position (% BIP; mittlerer Fall, Spanne in Klammern)

| Position | Modell | belegt | Lücke | Grundlage |
|---|---|---|---|---|
| Unternehmen und Plattformen | 4,42 | 3,41 (3,19–3,76) | −1,01 | Eurostat: Steuern der Kapitalgesellschaften 2024 125,1 Mrd. € ÷ heutiger Satz rund 30 % = Basis rund 417 Mrd. €; darauf 33 %; dazu Kundenort (R6) und Plattformen |
| Übrige Steuern | 3,93 | 3,39 | −0,54 | Eurostat: Einfuhrabgaben, Produktsteuern ohne Mehrwertsteuer, sonstige Produktions- und laufende Steuern 2024 = 3,81 % BIP, **abzüglich Emissionshandel 0,42 %** |
| CO₂-Preis 2028 | 1,38 | 1,07 (1,04–1,11) | −0,31 | bepreiste Emissionen 2025 rund 578 Mt (DEHSt, UBA), 2028 rund 528 Mt × 100 €/t = 52,8 Mrd. € |
| Erbschaft | 1,16 | 0,97 (0,79–1,15) | −0,19 | Destatis: Mittel 2022–2025 121,7 Mrd. €, fortgeschrieben 139 Mrd. € (2028), Anteil über dem Freibetrag, Zuschlag für nicht erfasste Erwerbe |
| **zusammen** | | | **−2,06 (−1,48 bis −2,48)** | |

## 3 Die Befunde im Einzelnen

**Übrige Steuern sind belegt, enthalten aber den Emissionshandel (wahrscheinliche Doppelzählung).** Die 165 Modell-Mrd. (3,93 % BIP)
entsprechen fast genau der VGR-Summe dieser Steuern 2024 (167,1 Mrd. €, 3,81 %). Darin stehen die heutigen Erlöse aus dem Emissionshandel
(18,6 Mrd. €, 0,42 % BIP). Der CO₂-Preis von 100 €/t auf alle bepreisten Emissionen zählt sie ein zweites Mal. Der Prüfer hatte die
Kassenstatistik verglichen (rund 100–110 Mrd. €). Das ist zu eng gefasst: Die VGR zählt Zölle, Grundsteuer, Grunderwerbsteuer und weitere
Abgaben mit. Wird die Doppelzählung bestätigt, ist sie ein eigener Fehler (Korrektur bei Übernahme).

**Unternehmen: größte Lücke, und eine Frage der Definition.**
- **Was das Modell unterstellt:** eine Basis von rund 563 Mrd. € (13,4 % der Modellbasis). Belegt ist das heute besteuerte Gewinnaufkommen
  der Kapitalgesellschaften: rund 417 Mrd. € (Eurostat, aus Aufkommen und Satz zurückgerechnet).
- **Was der Kundenort bringt:** Kundenort (R6) und Plattformen schließen die Lücke nur zu einem kleinen Teil (+0,27 % BIP).
- **Wie die Differenz zu schließen wäre:** nur mit einer breiteren Gewinndefinition, etwa ohne Steuerfreiheit ausländischer Dividenden, mit
  Begrenzung von Verlustvorträgen oder mit Einbeziehung der Personengesellschaften. Diese Definition fehlt bisher (Prüfbefund B23). Wird
  sie beschlossen, muss die Position Einkommen um die dann doppelt erfassten Gewinne bereinigt werden.

**CO₂-Preis: der Wert gilt als Anteil am BIP, die Emissionen sinken aber in Tonnen.** Die Gesamtrechnung führt 55 Modell-Mrd. (1,31 % BIP).
- 100 €/t auf rund 528 Mt im Jahr 2028 ergeben 52,8 Mrd. €.
- Das sind 1,07 % des BIP 2028, weil die Wirtschaft nominal wächst und die Menge nicht.
- Dazu kommt die Doppelzählung bei den übrigen Steuern (siehe oben).

**Erbschaft: Basis offen, Lücke klein bis mittel.**
- 2025 war ein Rekordjahr. Mit dem Mittel 2022–2025 fehlen im mittleren Fall 0,19 Punkte.
- Die Statistik zeigt nur Fälle mit festgesetzter Steuer. Erwerbe über 100.000 € innerhalb der heutigen Freibeträge fehlen; das ist als
  Zuschlag von 0 / 15 / 30 % angesetzt (Annahme).

## 4 Grenzen

- **Eurostat-Werte:** über die Eurostat-Schnittstelle in einem Sammelabruf gelesen, vorläufig. Die Summen gehen auf. Einzelabrufe stehen noch aus
  (`eingangswerte.csv`, Spalte `getestet = nein`).
- **Heutiger Unternehmenssatz:** 29–31 % (eigene Kenntnis, Hebesatz im Mittel).
- **Gewerbesteuer:** Die Aufteilung zwischen Kapital- und Personengesellschaften ist nicht geprüft; die VGR ordnet die Gewerbesteuer nach dem
  zahlenden Sektor zu.
- **Emissionen:** Rückgang 2 bis 4 % je Jahr (Annahme). Seeverkehr nur 2024.
- **Erbschaft 2022 und 2024:** rechnerisch aus den Veränderungsraten. 2023 nach einer Sekundärquelle.
- **Verhalten:** Ausweichen ist nicht zusätzlich gerechnet. Die Modellwerte enthalten es zum Teil (Abschläge im Kernmodell).

## 5 Zur Entscheidung

| Option | Was sie bedeutet | Dividende 2028 (mit Kinderanteil) |
|---|---|---|
| **A Belegte Werte übernehmen (Empfehlung)** | mittlerer Fall in die Deckung; Doppelzählung CO₂ korrigiert; Spanne ausgewiesen | rund 262 € statt 364 € |
| B Teilweise übernehmen | nur Doppelzählung CO₂ (−0,42) und CO₂-Menge (−0,31) korrigieren; Unternehmen und Erbschaft bis zur Definition als Spanne | rund 328 € (0,73 Punkte zu je rund 50 €) |
| C Lücke durch Regeln schließen | Unternehmensbasis verbreitern (Definition beschließen, Position Einkommen bereinigen) und belegen | offen, erst nach Rechnung |

**Empfehlung: A, verbunden mit dem Auftrag C.** Ein Wert, der sich nicht belegen lässt, sollte nicht in der Deckung stehen. Wird die
Unternehmensdefinition beschlossen und belegt, kann der Wert wieder steigen. Für die Erzählung heißt das: Die Dividende ist kleiner, die
übrigen Bausteine (Tarif, Grundauskommen, Netz, Fonds) bleiben.

## 6 Quellen (abgerufen 15.11.2026)

- Eurostat, gov_10a_taxag, Deutschland 2024 (S13_S212, Mio. €). [Eurostat-API](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10a_taxag?format=JSON&geo=DE&time=2024&unit=MIO_EUR&sector=S13_S212)
- Umweltbundesamt (Januar 2026): Emissionshandel – 21 Milliarden Euro fließen in den Klima- und Transformationsfonds. [UBA](https://www.umweltbundesamt.de/presse/pressemitteilungen/emissionshandel-21-milliarden-euro-fliessen-in-den)
- Umweltbundesamt / BMUKN (14.3.2026): Treibhausgasdaten 2025. [UBA](https://www.umweltbundesamt.de/presse/pressemitteilungen/treibhausgasdaten-zeigen-klimaschutz-braucht-neuen)
- Solarserver (8.7.2026): EU-ETS 1 – deutsche Emissionen sinken 2025 um 3,2 % (nach DEHSt; Sekundärquelle). [Solarserver](https://www.solarserver.de/2026/07/08/eu-ets-1-deutsche-emissionen-sinken-2025-um-32-prozent/)
- Destatis, PM 306 vom 26.8.2026 (Erbschaft- und Schenkungsteuer 2025). [Destatis](https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/08/PD26_306_736.html)
- evangelisch.de (16.7.2024): Finanzämter melden Höchstwert bei Erbschaften und Schenkungen (2023: 121,5 Mrd. €, nach Destatis; Sekundärquelle). [evangelisch.de](https://www.evangelisch.de/inhalte/231901/16-07-2024/finanzaemter-melden-hoechstwert-bei-erbschaften-und-schenkungen)
- sozialpolitik-aktuell, Tab. II.8 (Stand 20.8.2026), nach BMF-Datensammlung zur Steuerpolitik 2026 (Sekundärquelle, Gegenprobe Kasse). [PDF](https://www.sozialpolitik-aktuell.de/files/sozialpolitik-aktuell/_Politikfelder/Finanzierung/Datensammlung/PDF-Dateien/tabII8.pdf)
- Wirtschaftsdienst 1/2024: Rückläufige Einnahmen aus der Erbschaft- und Schenkungsteuer (Erlass bei Großerwerben). [Wirtschaftsdienst](https://www.wirtschaftsdienst.eu/inhalt/jahr/2024/heft/1/beitrag/ruecklaeufige-einnahmen-aus-der-erbschaft-und-schenkungsteuer.html)
