# Polen: Eingangsdaten für die Länderrechnung (Standard, Modellstand v3.24)

Stand: 10. Oktober 2026. Rechnung: `modell/laender/rechne.py`; Parameter: `modell/laender/pl.toml`; Ergebnis: `daten/aggregate/laender/pl.json`.

Die Angaben stammen aus Abrufen am 10.10.2026. „WebFetch“ bedeutet: Die Seite wurde abgerufen und der Wert maschinell aus dem Text oder der Datenbankausgabe gelesen. Daran ist die Richtigkeit nicht vollständig geprüft. Polen steht nicht im Gewichtsbestand der Gesamtrechnung. Die Gewichtungsrechnung entfällt deshalb (Standard 2.4).

## 1. Staatsschuld und Defizit

| Größe | Wert | Bezugsjahr | Preisbasis | Quelle | Status | Prüfung |
|---|---|---|---|---|---|---|
| Schuldenquote, Gesamtstaat (Maastricht) | 59,7 % BIP | 2025 | Verhältniszahl | Eurostat `gov_10dd_edpt1`, GD, S13 | amtlich, maschinell | WebFetch 10.10.2026. Stimmt mit GUS überein (unten). |
| Schuldenquote, Gesamtstaat | 59,7 % BIP | 2025 | Verhältniszahl | GUS, Veröffentlichung 01.04.2026 (Seite „Preliminary information about general government deficit and debt 2025“) | amtlich, Original (Seite abgerufen) | WebFetch 10.10.2026 |
| Finanzierungssaldo (B9) | −7,3 % BIP | 2025 | Verhältniszahl | Eurostat `gov_10dd_edpt1`, B9, S13 | amtlich, maschinell | WebFetch 10.10.2026 |
| Finanzierungssaldo, vorläufig | −7,2 % BIP | 2025 | Verhältniszahl | GUS, 01.04.2026 | amtlich, vorläufig | WebFetch 10.10.2026 |
| Schuldenquote, 1. Quartal 2026 (EU-Methode) | 61,6 % BIP; 2,44 Bio. Zł | 1. Quartal 2026 | laufende Preise | Finanzministerium, über Notes from Poland, 12.06.2026 | **Sekundärquelle**, Quartalswert | nicht am Original geprüft |
| Defizit, Regierungsprognose | 7,1 % BIP (2026 und 2027); 282,6 Mrd. Zł (2027) | 2026, 2027 | laufende Preise | Haushaltsentwurf 2027, Ministerrat 28.08.2026, über Notes from Poland, 28.08.2026 | **Prognose, Sekundärquelle** | Entwurf nicht am Original geprüft |
| Defizit 2028 | Annahme: 7,1 % BIP (gleich 2027) | 2028 | — | keine Quelle; Setzung | **Annahme** | Die Regierung nennt keinen Wert für 2028. |
| Schuldenquote, Regierungsprognose 2026–2028 | nicht gefunden | — | — | — | **Lücke** | Pfad C entfällt (Standard 2.3). |
| Mittelfristplan 2025–2028 (Ziele) | Defizit unter 3 % BIP bis 2028; Schuld mittelfristig unter 60 % | — | — | gov.pl, Plan vom 08.10.2024 (Seite abgerufen) | Ziel, **veraltet** | Der Plan stammt aus 2024 und ist durch den Haushaltsentwurf überholt. Nicht eingerechnet. |

Widerspruch: GUS nennt das Defizit 2025 mit 7,2 %, Eurostat mit 7,3 %. Der Standard nimmt Eurostat (1.3). Die Differenz ist mit 0,1 Punkten klein. Ursache nicht geprüft. Vermutung: Fassung vor der Eurostat-Meldung vom 22.04.2026, auf die GUS verweist. An der Quelle zu prüfen.

Kontrollwert: Der Quartalswert 61,6 % (1. Quartal 2026) liegt zwischen dem Stand 2025 (59,7 %) und dem Pfad B für 2026 (65,1 %). Ein Quartalswert ist kein Jahresendwert. Er wird nur als Plausibilität genannt und geht nicht in die Rechnung ein.

## 2. Bruttoinlandsprodukt, Bevölkerung, Preisniveau

| Größe | Wert | Bezugsjahr | Preisbasis | Quelle | Status | Prüfung |
|---|---|---|---|---|---|---|
| BIP, nominal | 852.229,8 Mio. € | 2024 | laufende Preise | Eurostat `nama_10_gdp`, B1GQ, CP_MEUR | amtlich, maschinell | WebFetch 10.10.2026. Nicht im Repository-Gewicht (Standard 2.4). |
| Bevölkerung, Jahresdurchschnitt | 36.559.233 | 2024 | Personen | Eurostat `demo_gind`, AVG | amtlich, maschinell | WebFetch 10.10.2026. Stimmt mit dem Wert aus der Vorchat-Quelle (36,559 Mio., Sekundärquelle) überein. Vorher als Sekundärquelle geführt. |
| Preisniveau, PLI (EU27 = 100) | **nicht eingetragen** | 2024 | — | Eurostat `prc_ppp_ind`, PLI_EU27_2020, A01 | **Lücke** | Zwei Abrufe der Datenbank schlugen fehl. Die Übersichtsseite `tec00120` (db.nomics) zeigt nur 10 von 42 Reihen und lieferte keinen Wert für Polen. |

Folge: Ohne Preisniveau ist die Dividendenrechnung für Polen nach Standard nicht möglich. Die Schuldenrechnung ist davon nicht betroffen.

## 3. Lücken und offene Punkte

1. Preisniveau Polen (PLI) fehlt. Abruf der Datenbank am 10.10.2026 nicht erfolgreich, erneuter Abruf nötig.
2. Schuldenquoten-Prognose der Regierung für 2026 bis 2028 fehlt. Der Mittelfristplan enthält nur Ziele.
3. Defizit 2028: Annahme, keine Regierungsangabe.
4. Verlauf der Schuldenquote 2010 bis 2024: nicht eingetragen.
5. Verfassung (Selbstverwaltung der Gemeinden und Regionen, Finanzautonomie): nicht geprüft.
6. Kopie des Haushaltsentwurfs 2027 und des Haushaltsgesetzes 2026: nicht am Original abgerufen. Der Haushalt 2026 selbst ist im Rechercheergebnis nicht enthalten.

## 4. Abrufe am 10.10.2026

- Eurostat `gov_10dd_edpt1`, PL, GD, S13, 2025 (WebFetch): 59,7 %.
- Eurostat `gov_10dd_edpt1`, PL, B9, S13, 2025 (WebFetch): −7,3 %.
- Eurostat `nama_10_gdp`, PL, B1GQ, CP_MEUR, 2024 (WebFetch): 852.229,8 Mio. €.
- Eurostat `demo_gind`, PL, AVG, 2024 (WebFetch): 36.559.233.
- GUS, Veröffentlichung 01.04.2026 (WebFetch): Defizit 7,2 %, Schuld 59,7 %.
- Notes from Poland, 12.06.2026 (WebFetch): 61,6 % im 1. Quartal 2026.
- Notes from Poland, 28.08.2026 (WebFetch): Defizit 7,1 % (Entwurf 2027).
- gov.pl, Mittelfristplan (WebFetch): nur Ziele.
- Eurostat `prc_ppp_ind`, PL, PLI_EU27_2020, A01 (WebFetch, zweimal): Fehler.
