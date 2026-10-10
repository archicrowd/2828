# Standard für Länderrechnungen (Fassung 1.2, Modellstand v3.26)

Fassung 1 (v3.24): Eingaben, drei Pfade, Gewichtung. Fassung 1.1 (v3.25): Interpolation einzelner Prognosejahre, Bestandsanpassung, Abschnitt Wohnort (2.6). Fassung 1.2 (v3.26): gemeinsame Wirkung mehrerer Länder auf die Klubquote (2.4).

**Zweck.** Jede länderspezifische Rechnung der Initiative 28:28 folgt diesem Standard. Dadurch sind die Rechnungen untereinander vergleichbar, und das Rechenmodell insgesamt wird an einzelnen Ländern geprüft. Der Standard legt fest, was eingegeben, wie gerechnet und wie ausgegeben wird. Er legt nicht fest, welche Länder betrachtet werden.

**Geltungsbereich.** Gilt für alle Länder gleich. Eine Einteilung der Länder in Gruppen gibt es in diesem Standard nicht.

## 1. Eingaben

1.1 Jede Eingabe steht in `modell/laender/<cc>.toml` mit Wert, Bezugsjahr, Preisbasis, Quelle und Quellenstatus. Die Pflichtfelder prüft `modell/laender/rechne.py`. Freiwillige Felder: `preisniveau_2024`, `wachstum_nominal_regierung`, `quote_regierung_hinweis`.

1.2 Quellenstatus, eine der folgenden Angaben:
- **amtlich, Original geprüft:** Wert gegen die Veröffentlichung der nationalen Statistik oder Regierung geprüft.
- **amtlich, maschinell:** aus einer Datenbank oder Veröffentlichung abgerufen und maschinell gelesen, nicht gegen das Original geprüft.
- **Sekundärquelle:** Presse, Vergleichsseite, Zusammenfassung. Nicht amtlich.
- **Prognose:** Regierungs- oder Institutsprognose.
- **Annahme:** eigene Setzung, mit Begründung.
- **Lücke:** nicht eingetragen, mit Angabe, was fehlt.

1.3 Staatsschuld und Finanzierungssaldo stammen für alle Länder aus derselben Quelle: Eurostat, Tabelle `gov_10dd_edpt1`, Gesamtstaat (S13), % des BIP. Weicht ein amtlicher nationaler Wert ab, gilt der Eurostat-Wert, und die Abweichung wird in der Eingabe vermerkt.

1.4 Eine Eingabe, die nur aus einer einzigen Quelle stammt, ist als solche zu kennzeichnen. Eine Sekundärquelle wird nie als amtlich geführt.

1.5 Jede Länderrechnung hat eine Eingabedatei `daten/aggregate/laender/<cc>_eingaben.md`. Sie enthält je Größe Wert, Bezugsjahr, Preisbasis, Quelle, Status und Prüfung.

## 2. Rechnung

2.1 Schuldenquote: d(t) = d(t−1) / (1 + g) − s(t). s ist der Finanzierungssaldo in % des BIP, ein Defizit ist negativ. Dies entspricht `modell/schuldenpfad.py`.

2.2 Nominales Wachstum g = 3,0 % (Parameter `wachstum_nominal` in `modell/gesamtrechnung.toml`). Die Annahme gilt für alle Länder gleich. Eine Abweichung braucht eine eigene Begründung in der Eingabe.

2.3 Drei Pfade, 2026 bis 2028:
- **A, Status quo:** Der Saldo von 2025 bleibt in allen Jahren gleich.
- **B, Regierungsdefizit:** Der Saldo aus der Haushaltsplanung des Landes. Fehlt ein Jahreswert, wird eine Annahme gesetzt und als Annahme gekennzeichnet.
- **C, Regierungsschuldenquote:** nur, wenn eine Schuldenquoten-Prognose vorliegt. Das implizite Wachstum ist dann so gewählt, dass die Prognose reproduziert wird. Fehlt die Prognose, entfällt C, und der Grund steht im Ergebnis.
  Fehlt ein einzelnes Jahr zwischen zwei Prognosejahren, darf es linear interpoliert werden. Das ist eine Annahme und steht im Ergebnis (`quote_regierung_hinweis`).
  Das implizite Wachstum enthält alles, was die Quote außer dem Saldo bewegt, auch Bestandsanpassungen (z. B. Vorfinanzierung, Schulden außerhalb des Haushalts). Es ist deshalb nicht als Wachstumsprognose zu lesen. Liegt das nominale Wachstum der Regierung vor (`wachstum_nominal_regierung`), weist das Ergebnis die Bestandsanpassung aus: Regierungsquote minus Fortschreibung mit Regierungssaldo und Regierungswachstum.

2.4 Gewichtung: Liegt das Land im Gewichtsbestand der Gesamtrechnung (`modell/rahmen/basis.py`), rechnet der Standard zusätzlich die Wirkung auf die Klubquote 2028 aus. Das ist eine Sensitivität und kein Ersatz für die Gesamtrechnung. Liegt das Land dort nicht, entfällt dieser Schritt, und der Grund steht im Ergebnis. Es ist ein Rechenschritt und keine Einteilung der Länder.
   Gemeinsame Wirkung: Alle Länder im Gewichtsbestand, die einen Pfad C haben, stehen zugleich auf ihrem Regierungspfad. Die übrigen Länder tragen den Rest-Saldo, sodass der Klub-Gesamtsaldo gleich bleibt. Ausgabe: `daten/aggregate/laender_klub.json`.

2.5 Gültig ist ein Ergebnis nur dann, wenn Pfad C die Regierungsquote reproduziert. Diese Prüfung läuft in `rechne.py`.

2.6 Wohnort: Ist das Preisniveau des Landes eingetragen (`preisniveau_2024`, Eurostat `prc_ppp_ind`, `na_item` PLI_EU27_2020, `ppp_cat` A01 Individualverbrauch, EU27 = 100), gibt der Standard aus:
- Dividendenboden: halbes Existenzminimum am Wohnort = Ankerwert Deutschland (`anker_de`, Euro 2028 nominal je Erwachsenem und Monat) × Preisniveau des Landes / Preisniveau Deutschland. Kinder erhalten die Hälfte. Grundlage ist die Entscheidung v3.20 (V3b).
- Tarifstufen: 1- bis 4-facher Grundbedarf am Wohnort (Grundbedarf Deutschland 2028 × Preisniveau des Landes / Preisniveau Deutschland), Sätze 0 / 9 / 16 / 21 / 28 % (v3.22).
- Ausgezahlte Dividende (V3a, Klubtopf nach Einwohnern × Preisniveau): nur für Länder im Gewichtsbestand, sonst leer mit Hinweis.
Steht ein Land in `preisniveau_2024.csv`, muss der eingetragene Wert damit übereinstimmen, und Dividendenboden und Tarifstufen müssen `laendervarianten.json` und `tarif_grundbedarf.json` reproduzieren. Andernfalls schlägt die Stufe fehl. Das Preisniveau eines weiteren Landes wird nur in seiner Länderdatei geführt und nicht in `preisniveau_2024.csv`. Die Tabelle speist die Gesamtrechnung.

## 3. Ausgabe

3.1 Je Land `daten/aggregate/laender/<cc>.json` mit festen Schlüsseln. Übersicht aller Länder in `daten/aggregate/laender_vergleich.csv`.

3.2 Jede Euro-Zahl trägt Bezugsjahr und Preisbasis (nominal oder real). Quoten verschiedener Länder werden nicht ohne gemeinsame Bezugsgröße nebeneinandergestellt (Korrekturen 42 bis 46).

3.3 Das Ergebnis ist eine Fortschreibung mit den eingetragenen Eingaben. Es ist keine eigene Prognose der Initiative. Prognosen anderer werden als solche bezeichnet.

## 4. Prüfung

- `python3 modell/alles.py` führt `modell/laender/rechne.py` aus. Die Stufe schlägt fehl bei fehlenden Pflichtfeldern, bei einer Abweichung der Schuld 2025 von der Tabelle `schulden_2010_2025.csv` um mehr als 0,05 Punkte und bei einer nicht reproduzierten Regierungsquote.
- Vor einer Veröffentlichung sind die Eingaben gegen das Original geprüft oder als offen geführt.

## 5. Verhältnis zum Gesamtkonzept

Das Gesamtkonzept rechnet mit einem Wert für die Klubquote. Die Länderrechnungen prüfen die Annahmen an einzelnen Ländern. Sie ändern die Gesamtrechnung nicht. Ob eine Annahme geändert wird, entscheidet die Initiative, nachdem die Länderprüfung abgeschlossen ist. Bis dahin gilt die Elastizität der Annahmen.

## 6. Kommunikation

Die länderspezifische Darstellung von 28:28 übernimmt Zahlen nur aus `daten/aggregate/laender/<cc>.json`, zusammen mit Quellenstatus und Bezugsjahr. Zwischenstände werden nicht übernommen. Die Umsetzung in Webseite und Konzepttexten ist offen.
