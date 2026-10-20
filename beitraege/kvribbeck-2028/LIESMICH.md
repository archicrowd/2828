# Beitrag kvribbeck-2028: Mikrosimulation „9 von 10 Beschäftigte"

Kulturverein Ribbeck e.V. · 20.10.2026 · geprüfter Modellstand: v4.18 (Commit 41b0b285), Stand C
Lizenz: Rechenweg MIT, Texte und Ergebnisdateien CC BY 4.0

Synthetische Population: 60.000 Vollzeitbeschäftigte auf Haushaltsebene. Lohnverteilung geeicht auf
die Verdiensterhebung 2024 des Statistischen Bundesamts (P10 32.526, P30 42.000, P50 52.159,
P70 66.000, P90 97.680, P99 213.286 EUR; Pareto-Schwanz alpha 2,95 ueber P99). Haushalte nach
Mikrozensus 2024 (Annahmen): 32 % Alleinstehende, 22 % Paare ohne Kinder, 28 % Paare mit Kindern
(1/2/3 Kinder: 45/40/15 %), 8 % Alleinerziehende (1/2 Kinder: 70/30 %), 10 % Sonstige
(Zwei-Erwachsenen-Haushalte, kein Splitting); Zweitverdienerquoten 75/70/75 %,
Partner-Einkommenskorrelation rho 0,35 (Gauss-Kopula).

Regelwerk (modell/haushalte33.py v4.18): ESt 2026 mit Splitting, Soli (Freigrenze 20.350 EUR),
SV-Bemessungsgrenzen (KV 69.750, RV 101.400 EUR), Kindergeld 259 EUR; 33R-Stufentarif 0/11/19/25/33 %
auf 12.348/18.522/24.696/37.044 EUR; Dividende 354 EUR je Erwachsenem (steuerpflichtig) und 283 EUR
je Kind (steuerfrei; Kinderanteil 0,8, geltend seit v4.5); Altlastenzuschlag 15,8 % auf Einkommen- und
Mehrwertsteuer; effektiver MwSt-Satz 15,97 -> 18,84 %; Konsumquote 95/85/75/60 % (geglättet);
Weitergabe der Arbeitgeberanteile 80/80/50/0 %; Vorsorge 10 % (Beschluss) bzw. 18,6 % bis BBG (Vergleich).

Szenarien in ergebnis.csv: beschluss (0,8/0,10), vergleich (0,8/0,186), weitergabe_50 (0,5/0,10),
weitergabe_0 (0,0/0,10). Unsicherheitsband: 12 Monte-Carlo-Laeufe mit +/-2 % jitterten Lohnankern
(nur fuer alle_beschaeftigte, P5/P95).

Validierung: Alle 96 publizierten Zeilen der daten/aggregate/haushalte33.json reproduziert
("heute" +/-1 EUR Rundung, "neu" 0 EUR). Verteilungsanker der Population: P10 32.549, P50 52.158,
P90 97.375, P99 216.259 EUR, Mittelwert 64.215 EUR, 9,46 % ueber der RV-Bemessungsgrenze.

Grenzen: nur Vollzeitbeschaeftigte; "heute" ohne bedarfsgepruefte Leistungen, "neu" ohne
Grundauskommen; statisch, keine Verhaltensreaktionen. Dezile nach Erwerbseinkommen des Erstbeschaeftigten.
