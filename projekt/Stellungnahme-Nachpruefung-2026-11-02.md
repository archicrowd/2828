# Stellungnahme zur Nachprüfung v4.42 → v4.63 (Zwischenstand vom 2. November 2026)

Initiative 28:28 · 2. November 2026 · Modellstand v4.65

Gegenstand: Prüfbericht des Kulturvereins Ribbeck e.V., Abschnitt 10 „Nachprüfung der Änderungen v4.42 → v4.63“ (Prüflog 1–17,
Befunde B25–B29, Abdeckungsmatrix Z01–Z34). Die Nachprüfung läuft; geprüft und bestanden sind D1 und D2, offen sind D3 bis D7 und D9.

## 1 Was die Nachprüfung bisher bestätigt

- **D1 bestanden:** Das Raster Zins × Wachstum ist in eigener Rekursion vollständig reproduziert (84/84 Werte), ebenso die sechs Zinsvarianten
  (30/30) und der ungerundete Beschlussbeitrag (Abweichung 0). Z 2028 = 9,42 % BIP (Korrektur 74) bestätigt; B17, B18, B21 und B24 behoben.
- **D2 bestanden:** Grenzbelastung bereinigt um Gegenwerte, 77/77 Werte exakt; die Bereinigung wird als sachgerecht bewertet.
- **Umfang (R2):** Die als unverändert gemeldeten Ergebnisdateien sind byte-identisch; `mikro_de.json` weicht genau in dem gemeldeten
  Rundungsrest ab; `parameter.toml` ändert nur die Versionszeile; `alles.py` nur neue Stufen.
- **Korrekturen (R3):** Alle Korrekturen 73–83 sind zugeordnet.

Die sieben Abweichungen vom Prüfprogramm (R1–R7) nehmen wir an. Zu R7: Die Liste der Änderungen seit der letzten Prüfung bleibt nach Abschluss
öffentlich, mit dem Prüfstand je Eintrag.

## 2 Befunde B25–B29

| Nr. | Befund | Bewertung | Umsetzung (v4.65) |
|---|---|---|---|
| B25 | Für Z13–Z16 sind die Quelldateien nicht veröffentlicht | zutreffend | `altlasten.json`, `gesamtlast33.json`, `netz33.json`, `regel_boden.json` liegen jetzt im Datenordner der Forschungsseite; alle 34 Zahlen sind öffentlich nachvollziehbar |
| B26 | Korrektur 75 ist in `fondszins.json` nicht erkennbar | zutreffend | je Variante neues Feld `haushalt_de.zuschlag_de_pct` (15,0 / 16,5 / 18,1 / 19,7 % sowie 17,9 / 19,4 % in den Übergangsfällen); alle übrigen Werte der Datei unverändert (geprüft) |
| B27 | Versionsfelder veraltet | zutreffend | Feld je Datei auf den Stand der letzten inhaltlichen Änderung gesetzt (per `git log` ermittelt): `verrechnung_haushalte` v4.57, `laenderseiten` v4.38, `haushalte33` v4.38, `gesamtlast33` v4.46. Dem Vorschlag, Nachweise nur per Git-Diff zu führen, folgen wir |
| B28 | Repository nicht erreichbar | behoben | Das Repository ist seit dem 2.11.2026 wieder öffentlich (GitHub, abgerufen 2.11.2026). Die Angaben „privat, Zugang auf Anfrage“ in `DATENZUGANG.md`, Prüfmappe, Forschungsseite und Working Paper sind damit überholt (Korrektur 84) |
| B29 | Standwechsel während der Prüfvereinbarung; Zitierzeile v4.64 gegen Archiv v4.58 | teilweise zutreffend | Seit v4.63 gibt es ein weiteres Release mit Zenodo-Fassung; der DOI dieser Fassung ist bei der Initiative nachzutragen. Neue Releases erst nach Abschluss der Nachprüfung; Versionen ohne Rechenwirkung (wie v4.64, v4.65) erhalten keinen Release. Die Zitierzeile nennt den Concept-DOI und zusätzlich die archivierten Fassungen |

Bewegte Zahl: keine. `fondszins.json` erhält ein Feld, vier Ergebnisdateien ein neues Versionsfeld.

## 3 Bezeichnung der Prüfungen

Der Bericht trägt die Überschrift „Drei unabhängige Prüfungen“. Auf der Forschungsseite und im Working Paper bezeichnen wir die Prüfungen als „im
Auftrag der Initiative“. Für eine Veröffentlichung des Berichts ist zu klären, ob zwischen Prüfenden und Initiative eine personelle oder
organisatorische Verbindung besteht (Prüfprogramm, Abschnitt 5). Bis dahin veröffentlichen wir nur diese Stellungnahme und den Prüfstand, nicht den
Bericht selbst.

## 4 Weiter offen

D3 bis D7 und D9 (Prüfprogramm); die inhaltlichen Bedingungen B22, B23, M3 und M4 aus der dritten Prüfung.
