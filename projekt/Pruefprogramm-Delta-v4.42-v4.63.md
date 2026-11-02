# Prüfprogramm: Nachprüfung der Änderungen v4.42 → v4.63

Initiative 28:28 · 2. November 2026 · Modellstand v4.63 (Commit `f8fc0f3`) · erweitert aus der Fassung v4.58 vom 1. November 2026

## 1 Zweck

Die dritte Prüfung (24.10.2026) erfasste den Modellstand v4.42 (Commit `43f7888`). Die Forschungsseite und das Working Paper zeigen v4.63. Diese Nachprüfung
soll nur die Änderungen dazwischen prüfen und keine vollständige Prüfung wiederholen. Das Ziel ist die Aussage: „Die veröffentlichten
Zahlen entsprechen einem geprüften Modellstand.“

Vergleichsbasis: `git diff 43f7888 f8fc0f3`. Seit v4.42 haben sich 18 Dateien unter `modell/` geändert (Skripte und Parameter, ohne `alles.py`) und
20 Ergebnisdateien (davon `projektstatus.md` und `ergebnis.json` nur Stand und Ausweis). Zwischen v4.58 und v4.63 hat sich keine Rechnung
geändert; neu sind nur Ausgaben (Zenodo-DOI, Working Paper).

**Tags:** Die Tags `v4.43` bis `v4.63` liegen nur in der Arbeitsumgebung; der Push von Tags wird über deren Proxy abgebrochen (Logbuch v4.58).
Maßgeblich sind daher die Commit-Kennungen: v4.42 = `43f7888`, v4.63 = `f8fc0f3`.

## 2 Was sich nicht geändert hat (nicht nachprüfen)

Maschinell geprüft mit `git diff --quiet 43f7888 f8fc0f3` (2. November 2026):

| Ergebnisdatei | Inhalt | Stand |
|---|---|---|
| `fonds_geltend.json` | Fonds der 30: Beitrag 5,17 % BIP, Zuschlag 15,5 %, Spitze 148,1 % (2055), Tilgung 2098 | unverändert seit v4.26 |
| `netz33.json` | Kosten des starken Netzes 9,63 % BIP (DE 2028) | unverändert |
| `haushalte33.json` | Fälle 42.000 € (DE) | unverändert |
| `rentner_kombi.json` | Rentnerregel E | unverändert |
| `mikro_de.json` | Mikrosimulation DE | nur Rundungsrest der Eichung (4,006·10⁻¹² → 4,029·10⁻¹²) |
| `dynamik33.json` | Szenarien Beschäftigung und Automatisierung (Working Paper, Tabelle 12) | unverändert seit v4.41 |
| `ausweichen33.json`, `preisniveau33.json`, `mwst_verteilung.json` | Ausweichen an der Spitze, Preisniveau, Mehrwertsteuer DE | unverändert |

Hinweis zur Rückmeldung vom 01.11.2026: Die Fondsspitze 149,6 % (2056) war der Wert des Fonds der zehn Staaten bis v4.19. Seit v4.20/v4.26
gilt 148,1 % (2055), auch schon in v4.42. Sie gehört deshalb nicht zum Prüfumfang. Die Staaten außerhalb Europas (Australien, Kanada,
Japan u. a.) erscheinen nur im Text der Seite als Beispiel für einen möglichen Maßstab (WJP Rule of Law Index 2025). Gerechnet werden sie
nicht.

## 3 Prüfpunkte

| Nr. | Version | Änderung | Skripte und Dateien | Prüffrage |
|---|---|---|---|---|
| D1 | v4.46 | Korrekturen 73–76 (Gesamtlast-Summe, Z = 9,42 % BIP, Zinsband mit beiden Zuschlagssätzen, Sichtbarkeit), Raster Zins × Wachstum | `gesamtlast33.py`, `fondszins.py` | Sind die Befunde B17, B18 und B24 der dritten Prüfung so behoben, wie die Stellungnahme sagt? Stimmt das Raster mit eigener Rekursion? |
| D2 | v4.47 | Grenzbelastung bereinigt um Gegenwerte (Z17: 48,8 → 40,0 % bei 60.000 €) | `grenzbelastung33.py/.toml` | Ist die Bereinigung um den äquivalenten Teil des Rentenbeitrags (Band 0,5 / 1) sachgerecht? Sind die Ableitungen numerisch richtig? |
| D3 | v4.51 | Ländermodelle gegen OECD Taxing Wages 2026; prime d'activité 59,85 % und forfait logement (Korrekturen 77–79) | `heute_laender.py/.toml`, `sozial_laender.py/.toml`, `validierung_laender.py/.toml` | Stimmen Satz und forfait mit DREES (Minima sociaux 2025, Fiche 30)? Sind die Abweichungen zur OECD für Polen (+5,3 / +6,5 Pp) und für das französische Paar (−5,6 Pp) richtig erklärt? |
| D4 | v4.52 | Weitergabe nur aus den entfallenden Beiträgen zur sozialen Sicherung (E16); FR +390 → +286 €, ES +350 → +321 €, PL +1.474 → +1.404 zł | `heute_laender.py` (`ag_entfaellt`, `fr_ag_entfaellt`), `deckel_einheitlich.py`; Ergebnis auch in `weitergabe_sensitivitaet.json` (Working Paper, Tabelle 8) | Ist die Abgrenzung der Arbeitgeberabgaben je Land richtig (welche Abgaben gehören zur sozialen Sicherung, welche nicht)? |
| D5 | v4.53 | Kennzahlenprüfung, Korrektur 81 | `pruefe_kennzahlen.py/.toml` | Prüft die Stufe die tragenden Werte vollständig? Stichprobe: 5 Werte aus `KENNZAHLEN.md` gegen die Ergebnisdateien |
| D6 | v4.54 | Mehrwertsteuer nach Einkommen FR (Eurostat HBS 2020); FR +286 → +276 € | `mwst_laender.py/.toml` | Sind die Zuordnung der Quintile zum Äquivalenzeinkommen und die Sätze je Gütergruppe vertretbar (beides Annahmen)? |
| D7 | v4.57 | Haushaltstypen je Land (Z20–Z34) | `verrechnung_haushalte.py` | Stichprobe: FR Paar bei 2 × Durchschnittslohn ≈ 0 € (Schnittpunkt), DE Paar +78 €, FR allein bei 0,5 × −148 €. Ist die Übertragung der deutschen Lohnverteilung auf den Anteil „better off“ als Annahme ausreichend gekennzeichnet? |
| D8 | v4.56–v4.59 | Forschungsseite und Kit | `seite/werkzeuge/forschung_bau.py`, `forschung_en.py` | Entsprechen alle 34 Zahlen zum Zitieren den Ergebnisdateien (Datei und Pfad stehen in `figures-to-cite.csv`)? |
| D9 | v4.60–v4.63 | Working Paper (14 Seiten, englisch) | `dokumente/werkzeuge/working_paper_bau.py` | Alle Zahlen werden aus den Ergebnisdateien gesetzt; zu prüfen sind die Aussagen, die über die Zahlen hinausgehen: (a) Bewertung an den Zielen (Abschnitt 7, Tabelle 11) – tragen die Kennzahlen die Aussagen, sind die Zielkonflikte vollständig? (b) Preissignal des Labels (Tabelle 13, reine Satzarithmetik) und die Aussagen zum EU-Recht (Richtlinie 2022/542, EuGH C-515/20 nur nach Sekundärquellen); (c) Wiedergabe der Literatur (27 Quellen); (d) die effektive Belastung je Euro Arbeit/Kapital (heute 47,9 / 26,4 %, neu 21 / 32 %) ist eine Näherung aus `dynamik33.toml` – ist der Vergleich zulässig? |

Gestaltungsentscheidungen ohne Rechenwirkung (v4.49/v4.50: E12–E15) gehören nicht zum Prüfumfang, ebenso reine Ausweisänderungen (v4.43–v4.45,
v4.48, v4.55, v4.58, v4.59).

## 4 Vorgehen

1. Repository auf Commit `f8fc0f3` (v4.63) auschecken, `python3 modell/alles.py` ausführen. Erwartet: alle Stufen ohne Fehler.
2. Je Prüfpunkt `git diff 43f7888 f8fc0f3 -- <Dateien>` lesen und die Stellen im Logbuch (Band III, Einträge v4.46 bis v4.63) dagegenhalten.
3. D3, D4 und D7 nachrechnen, mindestens für einen Haushalt je Land und eigenständig programmiert, wie bei der dritten Prüfung.
4. Befunde fortlaufend ab B25 nummerieren, im Format der dritten Prüfung (`befunde.csv`).

Aufwand (Schätzung, nicht belegt): Schwerpunkte sind D3, D4, D7 und D9. Grob ein Drittel bis die Hälfte des Aufwands der dritten Prüfung;
D9 ist überwiegend Lesearbeit.

**Während der Prüfung** bleiben die Zahlen eingefroren: Änderungen an der Rechnung erst nach Abschluss, als eigene Version mit eigener
kleiner Nachprüfung (Empfehlung an die Initiative, 01.11.2026).

## 5 Bezeichnung der Prüfungen

Auf der Seite stehen die Prüfungen als „im Auftrag der Initiative“. „Unabhängig“ steht dort nur für erwünschte weitere Prüfungen. Die
Formulierung „unabhängig in der Ausführung, im Auftrag der Initiative“ ist nur tragfähig, wenn keine personelle oder organisatorische
Verbindung zwischen Prüfenden und Initiative besteht. Das ist vor der Verwendung je Prüfung zu klären und offen anzugeben.

## 6 Nach der Prüfung

`GEPRUEFT` in `seite/werkzeuge/forschung_bau.py` auf den geprüften Stand setzen. Die Liste `SEIT_PRUEFUNG` (deutsch und englisch) leeren
bzw. kürzen. Seite und Working Paper neu bauen. Release mit DOI für diesen Stand.
