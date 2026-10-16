# Beschlüsse vom 17. Oktober 2026: prämienfreies Drittel und Altlastenfonds (Stand v3.46)

**Status: Beschlüsse der Initiative, in einer Prüfrechnung umgesetzt. Die Gesamtrechnung (28:28) und die Texte sind noch nicht umgestellt.**
Rechnungen `modell/systemvarianten.py` (System 33F) und `modell/altlasten.py` (Abschnitt „beschluss“), Ergebnisse `daten/aggregate/systemvarianten.json`,
`altlasten.json`. Prozent des BIP, Durchschnitt der zehn Staaten; Euro im Monat, Preise 2028; Deckung auf deutscher Basis; Altrenten Z als Schätzung.

## 1 | Die Beschlüsse und wie sie gerechnet sind

| Beschluss | Umsetzung in der Rechnung |
|---|---|
| Prämienfrei | Gesundheit (7,75 %) und Seil (2,72 %) ganz aus Steuern; keine Prämie, keine Belastungsgrenze |
| 33 % Mehrwertsteuer für umwelt- und gesundheitsschädliche Produkte | Label 5/11/17/22/28; Sonderstufe 33 % für Alkohol und Tabak, Kraftstoffe und Fahrzeuge mit Verbrennungsmotor (Mischsatz 32 % für Fahrzeuge, Annahme 80 % Verbrenner einschließlich Hybride); Haushaltsenergie bleibt 22 % (CO₂-Preis wirkt dort) |
| Altrenten: anlagegedeckte voll, der Rest zur Hälfte, die andere Hälfte der Verhandlung der Generationen | Die staatlichen Systeme sind praktisch ungedeckt (Tabelle 29: S13PU ≈ alle staatlichen Ansprüche), anlagegedeckt ≈ 0; im Fonds daher **50 % von Z** |
| Streckung höchstens 70 Jahre | Fonds bis **2098 vollständig getilgt** |
| Gemeinsamer Fonds mit Verrechnung je Staat, abschmelzend | Jeder Staat trägt den gemeinsamen Beitrag im Verhältnis seiner eigenen Altlast 2028 zum Durchschnitt; das Verhältnis schmilzt in 30 Jahren auf den gleichen Satz für alle ab (wie der Aufschlag für die Altschulden) |

## 2 | Das System (33F)

| Größe | Wert |
|---|---|
| Höchstsätze | Einkommen 0/11/19/25/33 % (am 1-, 1,5-, 2-, 3-fachen Grundbedarf), Kapital, Gewinne, Erbschaft 33 %; Mehrwertsteuer 5–28 %, 33 % nur für Schädliches |
| Effektiver Mehrwertsteuersatz | 17,6 % |
| Steuern brauchen / bringen | 32,92 / 33,04 % des BIP (Überschuss +0,12) |
| Mindestniveau der Dividende | 201 € (19 % des Grundbedarfs) |
| **Dividende 2028 (DE, Erwachsene)** | **281 €**, Kinder die Hälfte; dazu Gesundheit und Absicherung für alle ohne Prämie |
| Altrenten Z 2028 (voll / im Fonds zur Hälfte) | 10,39 / 5,20 |
| Gesamtlast im Dauerzustand | 33,7 % (heute 40,76 %) |

## 3 | Der Altlastenfonds

| Größe | Wert |
|---|---|
| Übernimmt | Staatsschulden 2028 (81,3 %) und die Hälfte der Altrenten über der Dividende |
| Gemeinsamer Beitrag, gleichbleibend bis 2098 | **3,15 % des BIP** |
| als Zuschlag auf alle Steuern | **9,6 %** – rund ein Zehntel |
| zum Vergleich: als Abzug von der Dividende | 142 € je Einwohner und Monat (bei 237 € Dividende je Einwohner im Durchschnitt) |
| Schuldenquote des Fonds | 2030 85 % · 2040 100 % · **Spitze 109 % (2052)** · 2070 88 % · 2080 59 % · 2090 26 % · **2098 0 %** |
| Risikofall Zins = Wachstum (3 %) | Beitrag 3,53 % (10,7 % Zuschlag), Spitze 112 % |
| Wenn die Verhandlung mehr zuspricht | 75 % von Z: 4,24 % BIP (12,9 % Zuschlag), Spitze 140 %; 100 %: 5,33 % (16,2 %), Spitze 171 % |
| Tilgung bei Einnahmenspitzen | Mehreinnahmen über dem gleitenden Fünfjahresdurchschnitt tilgen zusätzlich und verkürzen die Laufzeit (nicht beziffert) |

**Zuschlag je Staat (Verrechnung, abschmelzend), % auf alle Steuern:**

| Staat | Altlast 2028 (% BIP) | 2028 | 2040 | 2050 | ab 2058 |
|---|---|---|---|---|---|
| Österreich | 9,55 | 13,2 | 11,7 | 10,5 | 9,6 |
| Frankreich | 8,97 | 12,4 | 11,3 | 10,3 | 9,6 |
| Spanien | 8,36 | 11,5 | 10,8 | 10,1 | 9,6 |
| Belgien | 7,69 | 10,6 | 10,2 | 9,8 | 9,6 |
| Slowenien | 6,94 | 9,6 | 9,6 | 9,6 | 9,6 |
| Deutschland | 6,70 | 9,2 | 9,4 | 9,5 | 9,6 |
| Estland | 4,18 | 5,8 | 7,3 | 8,6 | 9,6 |
| Niederlande | 3,66 | 5,1 | 6,9 | 8,4 | 9,6 |
| Irland | 2,15 | 3,0 | 5,6 | 7,8 | 9,6 |
| Dänemark | 0,68 | 0,9 | 4,4 | 7,3 | 9,6 |

Altlast 2028 = Hälfte der Altrenten über der Dividende + Zinsen auf die eigene Schuld. Ab 2058 zahlen alle denselben Zuschlag; Staaten mit geringen Altlasten
tragen dann die Altlasten anderer mit. Dafür erhalten alle die gemeinsame Zinsgarantie.

## 4 | Empfehlung zur Quelle des Beitrags: Zuschlag auf alle Steuern

1. **Tragfähigkeit:** Als Abzug von der Dividende würde der Beitrag 142 € von im Durchschnitt 237 € je Einwohner wegnehmen; die Dividende wäre kaum noch sichtbar.
2. **Gerechtigkeit:** Ein Zuschlag folgt der Leistungsfähigkeit (Einkommen, Kapital, Gewinne, Erbschaft, Konsum); ein gleicher Abzug je Kopf trifft Arme am stärksten.
3. **Breite:** Der Zuschlag liegt auf allen Steuern, nicht nur auf den Löhnen; Unternehmen und Kapital tragen mit (Vorgabe der Initiative).
4. **Sichtbarkeit:** Ein eigener Posten auf jedem Steuerbescheid und jedem Kassenbon zeigt, was das Alte kostet, und dass es endet.
5. **Folge für die Marke:** Mit dem Zuschlag liegt der höchste Einkommensteuersatz rechnerisch bei rund 36 %. Ehrlich erzählt: „33 für das Neue, ein Zehntel dazu für das Alte – höchstens bis 2098.“

## 5 | Was ehrlich dazugehört

- **Altrenten:** Der Fonds plant nur die Hälfte der Ansprüche über der Dividende. Wenn die Verhandlung der Generationen nichts weiter zuspricht, sinkt der Teil
  einer heutigen Rente, der über der Dividende liegt, um die Hälfte; die Untergrenze Grundbedarf (Härtefall) gilt. Beispiel (grob): eine Rente von 1.200 €
  hieße 281 € Dividende + 460 € Altrente = 741 €, aufgestockt auf den Grundbedarf von 1.071 €. Das ist ein großer Eingriff; Vertrauensschutz und Eigentumsschutz
  (Art. 14 GG) sind juristisch zu prüfen. Jeder zusätzliche Viertelanteil kostet rund 1,1 Punkte des BIP im Jahr.
- **Schulden:** Die Schuldenquote steigt bis 2052 auf rund 109 %, bevor sie sinkt. Das trägt, solange der Zins nicht über dem Wachstum liegt.
- **Dividende:** 281 € sind wenig auf dem Konto; dafür sind Gesundheit, Arbeitslosigkeit, Invalidität und Hinterbliebene ohne Prämie abgesichert.
- **Mehrwertsteuer:** Die Sonderstufe trifft Kraftstoffe und Verbrennerfahrzeuge; Pendler auf dem Land spüren das. Der Nachfragerückgang ist nicht eingerechnet
  (die Einnahmen der Sonderstufe sinken mit dem Erfolg).

## 6 | Erzählung

**Ein Satz:**
> Höchstens ein Drittel auf jeden Euro, alle gesund versorgt und abgesichert ohne Prämie, jeden Monat eine Dividende – und für das, was frühere Generationen
> hinterlassen haben, ein Zehntel dazu, gemeinsam getragen und spätestens 2098 abbezahlt.

**Drei Zahlen:** 33 % höchstens · 0 € Prämie · ein Zehntel für das Alte, bis 2098.

## 7 | Nächste Schritte

1. Gesamtrechnung auf 33F umstellen (neue Version mit Logbuch), Altlastenfonds als eigener Teil.
2. Härtefall rechnen (Untergrenze Grundbedarf für Rentner und Menschen ohne Einkommen) – mit der kleineren Dividende wird er größer als 0,65 % angenommen.
3. Haushaltswirkung je Einkommen mit Zuschlag rechnen.
4. Texte (Gesamtkonzept, Kurzfassung, Webseite) nach Freigabe.
