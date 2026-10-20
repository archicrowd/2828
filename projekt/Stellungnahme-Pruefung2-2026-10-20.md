# Stellungnahme zur zweiten Prüfung (Stand C, 20.10.2026)

Initiative 28:28 · 20. Oktober 2026 · Logbuch v4.14

Die zweite Prüfung hat den Rechenkern von Stand C unabhängig nachgebaut und bestätigt:
- Haushaltsformeln;
- Fonds-Rekursion;
- Weitergabe-Empfindlichkeit;
- Grundauskommen, Netz, Polen.

Den früheren Vorbehalt zum Altlastenfonds nimmt sie zurück. Hier unsere Antwort auf die sechs neuen Befunde.

| Befund | Bewertung | Umsetzung v4.14 |
|---|---|---|
| **B11** Website-Fondszahlen 6,65 % / 20,3 % / 196 % (2054) | **Teilweise.** Die Werte sind nicht veraltet: Es ist der **eigene Fonds Frankreichs** (`laenderseiten.json`, FR), auf der französischen Seite als „fonds propre“ bezeichnet. Der Beschluss 5,28 / 15,8 / 149,6 % gilt für den gemeinsamen Fonds der zehn gerechneten Staaten. Richtig ist: Die deutsche Seite nutzt den gemeinsamen Fonds, die übrigen Länderseiten den eigenen. Das ist uneinheitlich. | Glossar `KENNZAHLEN.md`. **Entscheidung offen:** auch DE mit eigenem Fonds (4,76 % / 14,2 %) oder alle Seiten mit gemeinsamem Fonds |
| **B12** zwei Dividendenpfade ohne Kennzeichnung | **Trifft zu (Korrektur 67).** Geltend ist `netz33` (373 → 239 €, mit Kinderanteil 0,8: 354 → 227 €). `projektion33` (296 €) ist eine Vorstufe. Das „Mindestniveau“ stammt aus Stand B und ist in Stand C keine Zusage: Die Dividende ist ein Rest, die Sicherung leistet das Grundauskommen. | `projektion33.json` trägt einen Statusvermerk; `KENNZAHLEN.md` nennt die Empfindlichkeit (2060: rund 7 € je Zehntelpunkt BIP) |
| **B13** Rentenkürzung 7,5 % nicht kommuniziert | **Trifft zu.** | Auf der Seite (sechs Sprachen, Abschnitt „Altlasten“): Kürzung 7,5 %, weniger als die entfallenden KV- und PV-Beiträge (12,35 %); kleine Renten erhalten das Grundauskommen |
| **B14** Spitzenverdiener-Aussage mische Vorsorgevarianten | **Ursache anders, Befund berechtigt.** Beide Zahlen stammen aus derselben Beschlussvariante (Pflichtvorsorge 10 %). Die Basis war aber der Durchschnittslohn nach OECD Taxing Wages (63.288 €), nicht 50.000 €: 3× = 189.864 € → +5,8 %; 8× = 506.304 € → −2,1 %. Mit 50.000 € als Basis: 150.000 € +10,0 %, 400.000 € −1,3 % (beides bestätigt). Unser Fehler: Wir haben die Basis nicht genannt. | Basis in Stellungnahme und Rückmeldung ergänzt; Lohnbasis im Glossar |
| **B15** Gesamtlast 2028 bei 45,5 / 49,6 % gegen 40,8 % heute | **Abgrenzung anders, Hinweis berechtigt.** Die 45,46 % zählen die Altlasten so, als würden sie im selben Jahr voll bezahlt (12,04 % BIP, ohne Fonds). Mit dem beschlossenen Fonds: Steuern 33,53 + Fonds 5,28 = **38,81 %**, mit Pflichtvorsorge aufs eigene Konto **42,91 %**, gegen 40,76 % heute. Preis der Streckung: Fondsschuld bis 149,6 % BIP (2056). | `modell/gesamtlast33.py`; Zeile in der Kurzfassung des Konzepts; Glossar |
| **B16** Z 2028 = 9,38 / 10,23 / 8,6 % | **Trifft zu (Kennzeichnung).** 9,38 = Klub nach Kürzung 7,5 % (geltend); 10,23 = Variantenvergleich v3.43 ohne Kürzung; 8,6 = Deutschland allein. | `KENNZAHLEN.md` |

**Zur Weitergabe (B14, Ergänzung).** Der Vorschlag der Prüfung verdient Übernahme:
- **Monitoring:** unabhängiges Monitoring der Bruttolöhne je Sektor in den ersten Jahren.
- **Rückfallregel:** Wer die Vertragsanpassung unterlässt, zahlt die Differenz in den Altlastenfonds.

Damit trägt das Modell auch bei geringerer tatsächlicher Weitergabe. Die Regel ergänzt das beschlossene Gesetz zur Vertragsanpassung.
**Entscheidung offen.**

**Zu den offenen Punkten.** Preisniveauschub und Ausweichreaktionen bei Erbschaft und Vermögen nehmen wir als nächste Rechnungen auf:
- **Preise:** Der effektive Mehrwertsteuersatz steigt von 15,97 auf 18,82 %. Das ergibt auf den mehrwertsteuerpflichtigen Konsum einen einmaligen Preisniveauschub
  von rund 2,5 % bei voller Überwälzung (Überschlag: 1,1882 / 1,1597 − 1); gerechnet ist das noch nicht.
- **Handelsrecht:** Für die Besteuerung am Kundenort ziehen wir die DBCFT-Literatur (Auerbach, Devereux u. a.) als Prüfrahmen heran.

Wir nehmen das Angebot einer dritten Prüfung nach diesen Nacharbeiten gern an.
