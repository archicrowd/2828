# Rentner: Varianten zur Regel E (Entwicklungsmodus)

Initiative 28:28 · 4. November 2026 · Modellstand v4.68 · vorläufig, kein Beschluss · Rechnung: `modell/rentner_varianten.py`

## Auftrag

Hohe Erwartungen aus ungedeckten Zusagen sollen im Sinne der Generationengerechtigkeit eher zurücktreten; Rentner mit langen Beitragszeiten
und niedrigen Erwartungen sollen sicher ins Plus kommen. Keine neuen Abgaben, keine Sonderregeln; die Regel soll international übertragbar sein.

## Ausgangslage (Deutschland, 2028, Kaufkraft 2026)

- **Regel E:** 15 % Kürzung auf den Teil der Zusage über dem Grundbedarf G (1.029 € im Monat); Boden = heutige Grundsicherung.
  32 % der Rentnerhaushalte haben mehr, im Mittel −121 € im Monat; Entlastung des Fonds 25,1 Mrd. € (Kürzung minus Boden).
- **Ohne jede Kürzung** wären 67 % im Plus, im Mittel −3 €. Die Verluste des oberen Fünftels (−124 €) kommen dann aus Steuer, Label und
  Zuschlag. Wer verliert, verliert also vor allem durch die Kürzung.
- **Wo E trifft:** Zusagen zwischen 1 und 2 G (49 % der Personen) – darunter die typische Rente nach langer Erwerbszeit mit
  Durchschnittsverdienst (rund 1,75 G; Standardrente 2025 rund 1.800 € brutto, eigene Kenntnis, zu prüfen). Bei 1,5–2 G hat unter E niemand mehr.

## Grundgedanke

Die Kürzung folgt derselben Logik wie der Tarif: **Stufen in Vielfachen des Grundbedarfs des jeweiligen Staates.** Das ist keine neue Regel,
sondern die vorhandene, auf die Zusage angewandt, und es gilt in jedem Staat ohne nationale Beträge. Untere Stufen bleiben frei, obere
tragen mehr.

## Varianten, gerechnet (gleiche Entlastung des Fonds wie E, wo „neutral“)

| Variante | Kürzungsstufen | Anteil mit mehr | 1–1,5 G | 1,5–2 G | 2–3 G | über 3 G | Fonds gegen E |
|---|---|---|---|---|---|---|---|
| E (geltend) | 15 % ab 1 G | 32 % | +11 € (57 % im Plus) | −89 € (0 %) | −254 € | −649 € | 0 |
| T – wie der Tarif | 0 / 15 / 25 / 33 % ab 1,5 / 2 / 3 G | 52 % | +51 € (100 %) | −12 € (37 %) | −222 € | −856 € | −1,1 Mrd. € |
| N1,5/3 – neutral | 0 % bis 1,5 G, 19,4 % bis 3 G, 38,7 % darüber | 51 % | +51 € (100 %) | −22 € (32 %) | −221 € | −883 € | 0 |
| **N2/3 – neutral** | 0 % bis 2 G, 27,7 % bis 3 G, 55,4 % darüber | **65 %** | +51 € (100 %) | **+24 € (100 %)** | −162 € | −1.042 € | 0 |

Werte: Änderung des Haushaltsnettos je Monat im Mittel der Gruppe nach Zusage je Person; in Klammern Anteil im Plus. Personenanteile:
bis 1 G 21 %, 1–1,5 G 30 %, 1,5–2 G 19 %, 2–3 G 19 %, über 3 G 11 %. Bis 1 G sind 71 % im Plus, unabhängig von der Variante (Kürzung greift dort
nicht; kleine Verluste aus dem Label).

**Lesart.** N2/3 erfüllt den Auftrag am deutlichsten: Alle Zusagen bis zum doppelten Grundbedarf – also auch die Rente nach langer Erwerbszeit
mit Durchschnittsverdienst – kommen ins Plus, ohne dass der Fonds weniger erhält. Der Preis: Zusagen über 3 G (11 % der Rentner, vor allem hohe
Versorgungszusagen) verlieren im Mittel gut 1.000 € im Monat; der Grenzsatz der Kürzung liegt dort bei 55 %. T ist die einfachste, weil mit dem
Tarif gleichlaufende Fassung; sie belässt die Grenze bei 1,5 G und kostet den Fonds 1,1 Mrd. € (≈ 0,02 % des BIP).

## Weitere Varianten, noch nicht gerechnet

1. **Nominalschutz statt Kürzung:** Zusagen über der Schwelle werden nicht gekürzt, aber nicht mehr an die Preise angepasst, bis ihr realer Wert
   um den Kürzungssatz gesunken ist (bei 2 % Teuerung: 15 % nach rund 8 Jahren, 25 % nach rund 14 Jahren). Verlustaversion fällt geringer aus,
   weil kein Betrag sinkt. Nachteil: Die Entlastung kommt später; in den ersten Jahren trägt der Fonds mehr, also alle über den Zuschlag – das
   schwächt die Generationengerechtigkeit.
2. **Kürzung nach Zusage je Beitragsjahr:** Maßstab ist nicht die Höhe der Zusage, sondern ihre Höhe je Versicherungsjahr im Verhältnis zum
   Landesmittel. Lange Beitragszeiten mit niedriger Zusage bleiben frei, Zusagen ohne oder mit kurzer Beitragszeit (etwa Versorgungszusagen) tragen
   mehr. Am genauesten auf den Auftrag zugeschnitten und international übertragbar (jedes Rentensystem führt Versicherungsjahre), aber die
   Daten fehlen im Modell (EU-SILC und ASID ohne Beitragsjahre).
3. **Boden nach der allgemeinen Regel:** Der Boden der Rentner ist heute die deutsche Grundsicherung (1.083 / 1.632 €). Universal wäre das
   Grundauskommen aller (G × Äquivalenzskala, Wohnkosten über den Härtefall H1). Das ändert für Deutschland wenig, macht die Regel aber ohne
   nationale Beträge anwendbar.
4. **Aufschlüsselung des Rentenbescheids:** Jede Rente in drei Teilen ausweisen – Gemeinsames (Dividende), Eigenes (ungekürzt), Zugesagtes (Teil
   des Fonds). Kein Geldfluss, aber nachvollziehbar, wofür gekürzt wird.

## Folgen für andere Bausteine (zu prüfen)

- Armutsquote SDG 1.2: Mit N2/3 gewinnen die unteren und mittleren Rentnerhaushalte; die Quote dürfte sinken (neu zu rechnen, v4.67 rechnet
  Rentner unverändert).
- Kürzungssatz je Staat (`kuerzung_laender`): leitet sich bisher aus 15 % über G ab; bei Stufen ändert sich die Verteilung zwischen den Staaten.
- Verfassungsrecht (Eigentumsschutz von Anwartschaften, P1): hohe Grenzsätze der Kürzung sind rechtlich angreifbarer als ein einheitlicher Satz.

## Zu entscheiden

Grenze der freien Stufe (1,5 G oder 2 G), Höhe der oberen Sätze (Obergrenze z. B. 33 % wie im Tarif), Nominalschutz als Übergang, Datenweg
für die Beitragsjahre.
