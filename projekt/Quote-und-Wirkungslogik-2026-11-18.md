# Wo läge die richtige Quote? Und was die Wirkungslogik der Vereinten Nationen für das Konzept bedeutet

Initiative 28:28 · 18. November 2026 · Modellstand v4.100 (Prüfrechnung; die geltenden Zahlen bleiben unverändert)
Rechnung: `modell/quote_optimum.py` (+ `.toml`) → `daten/aggregate/quote_optimum.json`.
Euro je Erwachsenem und Monat, Kaufkraft 2026, Deutschland, mit erwarteter Dynamik; Anteile in % des BIP.

## Teil 1: Satz, Puffer und eine auf Dauer leicht steigende Dividende

### 1.1 Ergebnis in Kürze

- **Der Satz allein löst das Problem nicht.** Solange die Dividende den Rest erhält, fällt sie bei jedem Satz von 2028 bis 2060 um rund 2,6 Punkte des BIP. Ein höherer Satz hebt nur ihr Niveau, nicht ihren Verlauf.
- **Zuerst braucht es eine Regel, dann die Quote.**
  - Regel L: Die Lenkungsabgaben (CO₂, Sonderstufen, Verbrauchsteuern) gehen an den Fonds, der ebenfalls ausläuft.
  - Die Dividende erhält dafür einen festen Anteil von 1,24 % BIP aus dem Altlastenzuschlag. Er ist barwertgleich zum Weg der Lenkungsabgaben bis 2098.
  - Mit Regel L steigt die Dividende ab 2035 jedes Jahr. Vorher drückt sie der Aufbau der Verteidigung (+1,1 % BIP bis 2035). Eine Rücklage glättet das.
- **Empfohlene Quote: 37 % einheitlicher Satz,** mit festem Label (7/13/19/27), Regel L, Puffer 0,5 % BIP je Jahr und Glättung.
  - Die Dividende beginnt bei rund 100 € und steigt real um 1 % je Jahr auf rund 137 € im Jahr 2060.
  - Steuern 32,4 % BIP, mit Fondsbeitrag 37,7 % BIP (heute in Deutschland 40,2 %, EU-27 39,4 %).
  - Der Spitzensatz einschließlich Altlastenzuschlag beträgt 43,1 %.
- **Kommt die Staatsebene hinzu** (Verwaltung, +1,2 % BIP; Strukturanalyse v4.99), sind für dieselbe Wirkung rund 40 % nötig. Die Dividende liegt dann bei 86 € und steigt bis 2060 auf 118 €.
- **Zur „heiligen“ Drittelregel:**
  - Schon heute rechnet das Konzept mit einem wirksamen Spitzensatz von 39 %, nämlich ein Drittel mit 17 % Altlastenzuschlag.
  - Mit ein Drittel, Regel L und Puffer bleiben nur rund 34 bis 47 € Dividende. Mit Staatsebene bleibt keine.
  - Die Drittelregel ist ohne Kürzung der Ausgaben nicht mit einer tragenden Dividende vereinbar.

### 1.2 Die Rechnung

Jeder Satz s gilt für die oberste Einkommensstufe, Kapitalerträge, Unternehmen und Erbschaften; die unteren Stufen werden im Verhältnis s/33⅓ skaliert. Das Verhalten ist über die Elastizitäten des Kernmodells erfasst (Szenario Robust):

| Bemessung | Verhaltensfaktor |
|---|---|
| Einkommen | eti 0,35 |
| Kapitalerträge | ((1 − t)/(1 − t₀))^0,8 |
| Unternehmen | exp(−Δ/100) |
| Erbschaft | exp(−Δ/100) |

Für das Label ist keine Verhaltensreaktion angesetzt (Annahme). Die Ausgaben (Gemeinwesen, Netz, Verwaltung) bleiben wie geltend.

**Dividende ohne Glättung, Label fest, Puffer 0,5 % BIP:**

| Satz | Regel | Steuern 2028 | 2028 | 2035 | 2040 | 2050 | 2060 | Kriterium |
|---|---|---|---|---|---|---|---|---|
| geltend (33⅓, Puffer 0,23) | Rest | 31,2 | 174 € | 102 € | 81 € | 47 € | 48 € | nein |
| 33⅓ | Rest | 31,2 | 160 € | 87 € | 65 € | 29 € | 29 € | nein |
| 33⅓ | L | 31,2 | 79 € | 26 € | 28 € | 36 € | 50 € | nein |
| 36 | L | 32,1 | 125 € | 76 € | 82 € | 98 € | 120 € | nein |
| **37** | **L** | **32,4** | **141 €** | **95 €** | **101 €** | **120 €** | **145 €** | **ja** |
| 37 | Rest | 32,4 | 222 € | 156 € | 138 € | 113 € | 124 € | nein |
| 38 | L | 32,7 | 157 € | 112 € | 120 € | 142 € | 170 € | ja |
| 40 | L | 33,3 | 188 € | 146 € | 157 € | 183 € | 217 € | ja |

**Kriterium:** ab 2035 in keinem Jahr fallend und 2060 nicht unter 2028. Jeder Prozentpunkt Satz bringt bei festem Label rund 0,3 % BIP oder etwa 17 € Dividende.

**Mit Glättung** (Dividende wächst real um 1 % je Jahr; Überschüsse der ersten Jahre gehen ohne Zins in eine Rücklage, die nie negativ wird):

| Satz, Regel L | Label fest: Start → 2060 | Label mit s skaliert: Start → 2060 | höchster Stand der Rücklage | mit Staatsebene (+1,2 % BIP), Label fest |
|---|---|---|---|---|
| 33⅓ | 34 → 47 € | 34 → 47 € | 2,9 % BIP | 0 € |
| 36 | 82 → 113 € | 113 → 156 € | 2,7 % BIP | 19 → 27 € |
| **37** | **100 → 137 €** | 142 → 195 € | 2,6 % BIP | 37 → 50 € |
| 38 | 116 → 160 € | 170 → 234 € | 2,6 % BIP | 53 → 73 € |
| 40 | 149 → 204 € | 224 → 308 € | 2,4 % BIP | 86 → 118 € |

Das skalierte Label läge über dem Beschluss vom 16.11.2026 (höchstens +2 Punkte) und ist nur zum Vergleich gezeigt.

### 1.3 Einordnung und Grenzen

- **Mit Puffer:** 0,5 % BIP je Jahr als Ausgleichsrücklage, dazu die Glättungsrücklage (bis 2,6 % BIP). Zusammen fangen sie Schwankungen auf, ohne dass die Dividende sinkt. Die Höhe des Puffers ist eine Setzung.
- **Verhalten:** Bei 37 bis 40 % liegen die Sätze für Kapital und Unternehmen deutlich über dem europäischen Mittel. Die Elastizitäten des Kernmodells erfassen Verlagerung nur grob. Der Steuerwettbewerb ist das größte Risiko dieser Variante (Prüfung mit `ausweichen33`, offen).
- **Mischland:** Die Ausgaben sind der Schnitt der zehn Staaten, die Einnahmen stehen auf deutscher Basis (v4.99, S6).
- **Nicht eingerechnet:**
  - Trends bei Kapitaleinkommen und Erbschaften. Wachsen sie, sinkt die nötige Quote; das ist offen (R21).
  - Die Befunde zu CO₂ (B-3, −0,38 % BIP ohne nationale Abgabe) und der Altersausgleich der Rentner (R4, 0,23 % BIP). Beide erhöhen die nötige Quote um zusammen rund 1 bis 2 Punkte des Satzes.
- **Empfehlung:**
  1. Regel L und die Glättung zuerst beschließen.
  2. Dann zwischen 37 % (ohne Staatsebene) und 40 % (mit Staatsebene) entscheiden, nachdem die Staatsebene belegt ist (R20).
  3. Der Name „Goldenes Drittel“ kann bleiben, wenn er das Ziel bezeichnet (ein Drittel nach Tilgung der Altlasten). Der heutige Satz einschließlich Zuschlag liegt schon darüber. Das sollte offen gesagt werden.

## Teil 2: Was die Wirkungslogik der Vereinten Nationen für das Konzept bedeutet

**Das Dokument:** UNDG, *Theory of Change – UNDAF Companion Guidance* (2017, 15 Seiten). Es beschreibt, wie ein Programm erklärt, warum seine Maßnahmen zu einem Ziel führen.

**Vier Schritte:**
1. Fokus auf die übergeordnete Veränderung.
2. Ursachenanalyse mit Problem- und Lösungsbaum.
3. Annahmen und Risiken offenlegen, nach dem Muster „wenn X, dann Y, weil Z“.
4. Partner und Akteure benennen.

Dazu kommen drei Grundsätze: beteiligen, belegen, laufend lernen. Am Ende steht eine Prüfliste mit 17 Punkten.

**Einordnung:** Nach meinem Kenntnisstand wurde der UNDAF 2019 vom „Cooperation Framework“ der Vereinten Nationen abgelöst; das ist an der Quelle zu prüfen. Die Methode der Wirkungslogik gilt dort weiter.

### 2.1 Was das für das Konzept bedeutet

| Element der Wirkungslogik | Stand im Projekt | Bedeutung, Vorschlag |
|---|---|---|
| **Fokus**: eine übergeordnete Veränderung | Viele Ziele nebeneinander: Dividende, Entlastung der Arbeit, Altlasten, Klima, Gemeinden | Ein Satz als Ziel, z. B. „Jeder Mensch hat seinen Grundbedarf sicher, und die Lasten der Vergangenheit sind bis 2098 getragen“. Alle Regeln werden daran gemessen. |
| **Problembaum**: unmittelbare, zugrunde liegende und strukturelle Ursachen | Nur teilweise (Abgabenkeil, Altlasten, Steuerflucht) | Problembaum schreiben, z. B. „Arbeit zu hoch belastet“ ← Sozialbeiträge ← umlagefinanzierte Zusagen ← Demografie. Dann den Lösungsbaum spiegeln. |
| **Annahmen**: „wenn X, dann Y, weil Z“, mit den Fragen „erklärt es ganz?“, „plausibel?“, „zu testen?“ | Viele Annahmen, verstreut im Logbuch und in den Parameterdateien | **Ein Register der Annahmen** mit den drei Fragen. Die immer neuen Lücken (belegte Einnahmen, CO₂-Zuteilung, Rentner, Staatsebene) waren ungeprüfte Annahmen; ein Register hätte sie früher sichtbar gemacht. |
| **Risiken**: politisch und Umwelt, Chancen, Gestaltung | Einzeln (Zins des Fonds, Rechtsfragen P1, Verhalten) | Das Register um die Risiken ergänzen: EU-Recht (Emissionshandel, Mehrwertsteuer-Richtlinie), Steuerwettbewerb, Zins, Alterung, Annahme durch die Menschen. Je Risiko eine Gegenmaßnahme, z. B. den Puffer. |
| **Partner und Akteure** | Staaten, Fonds, Gemeinden benannt | Wer welche Ergebnisse trägt: EU (Emissionshandel, CBAM), Sozialversicherungen (Übergang), Finanzverwaltungen, Tarifparteien. |
| **Prüfliste: die Verletzlichsten zuerst** („niemanden zurücklassen“) | Rentnerbefund v4.97/v4.98 | Bestätigt die Priorität des Altersausgleichs R4. Jede Variante zuerst an den unteren Fünfteln und den Rentnern prüfen. |
| **Prüfliste: Frauen und Mädchen gezielt** | Nicht untersucht | **Lücke.** Wirkung nach Geschlecht fehlt (Alleinerziehende, Frauenrenten, Teilzeit). Mit der Mikrosimulation prüfbar. |
| **Prüfliste: Widerstandskraft gegen Schocks** (Klima, Seuchen, Konflikte) | Kein Puffer bisher | Der Puffer aus Teil 1 ist genau das: Rücklage und Glättung. |
| **Prüfliste: Belege und Grenzen der Belege benennen** | Stark (Logbuch, Korrekturen, Quellenkennzeichnung) | Stärke des Projekts beibehalten; die Grenzen der Belege als Grundlage der Bewertung ausweisen. |
| **Diagramm und Erzählung** | Geldfluss-Diagramm auf der Webseite | Ein Bild der Wirkungslogik (Ursachen → Regeln → Ergebnisse → Ziel) für Konzept und Seite. |
| **Überwachen und Bewerten** | Kennzahlenprüfung, keine Wirkungsindikatoren | Wenige Indikatoren je Ergebnis, z. B. Dividende real, Anteil der Rentner mit mehr, Gini, Emissionen, Fondsschuld. Dazu Schwellen, ab denen eine Regel greift. |

### 2.2 Empfehlung

1. **Register der Annahmen und Risiken** anlegen (`projekt/annahmen.csv`, maschinell prüfbar in `alles.py`). Je Annahme: Aussage, Beleg, Status, betroffene Zahl, Test. Das ist der größte Nutzen für das Projekt, weil es das Muster der Lücken bricht.
2. **Wirkungslogik auf einer Seite** für das Konzept: Ziel, Problembaum, Lösungsbaum, die zehn wichtigsten Annahmen, Indikatoren.
3. **Wirkung nach Geschlecht** in der Mikrosimulation ergänzen.
4. **Beteiligung:** Das Dokument verlangt, Betroffene einzubeziehen. Eine Prüfung mit Rentnerinnen und Rentnern, Alleinerziehenden, Gemeinden und Steuerfachleuten vor der Veröffentlichung.

## Quellen

- United Nations Development Group (2017): Theory of Change – UNDAF Companion Guidance (von der Initiative bereitgestellt, vollständig gelesen).
- Rechnungen des Projekts: `quote_optimum.json`, `projektion33.json`, `systemvarianten.json` (33R), `gesamtlast33.json`, `fonds_geltend.json`, `struktur_vergleich.json`.
- Elastizitäten: Kernmodell `modell/kern/modell-2828.py`, Szenario Robust (Annahmen des Projekts, Herkunft im Logbuch Band I).
