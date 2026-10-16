# Die Drittellösung: Rechnung und Erzählung (Stand v3.44, 17. Oktober 2026)

**Status: Lösungsvorschlag aus einer Prüfrechnung; die Gesamtrechnung bleibt bis zur Entscheidung bei 28:28.** Rechnung `modell/systemvarianten.py`
(+ `.toml`), Ergebnis `daten/aggregate/systemvarianten.json`. Prozent des BIP, Durchschnitt der zehn Staaten; Euro im Monat, Preise 2028.
Deckung auf deutscher Basis, Altansprüche Z als Schätzung (v3.42). Annahmen und Setzungen wie in `Systemvarianten-25-33-2026-10-17.md`.

## 1 | Antwort auf die Frage

**Nein.** Die Drittellösung in v3.43 hatte die Dividende „wie gehabt“: Mindestniveau die Hälfte des Grundbedarfs (535 €), Dividende Deutschland 634 €
je Erwachsenem. Mit einem Drittel des Existenzminimums ist jetzt nachgerechnet, in zwei Lesarten (Abschnitt 2).

## 2 | Gleiche Regel für alle Marken: Altlasten außerhalb

Neu gegenüber v3.43: Die **Altlasten** – Zinsen auf die bestehenden Staatsschulden und die Rentenansprüche über der Dividende (Z) – laufen außerhalb
der Steuern, in einem eigenen **Altlastenbeitrag** beim jeweiligen Staat. Die Quote enthält damit keinen Zinsdienst mehr.

| | 28:28 | 25:25 | 33:33, Dividende ⅓ von Grundbedarf + Sozialabdeckung | 33:33, Dividende ⅓ des Grundbedarfs | **33:33 Lösung** |
|---|---|---|---|---|---|
| Mindestniveau der Dividende (DE, Erw.) | 535 € (½ GB) | 387 € (¼ GB+S) | 516 € (⅓ GB+S) | 357 € (⅓ GB) | **516 € (⅓ GB+S)** |
| Dividende 2028 (DE, Erw.) | 640 € | 479 € | 618 € | 447 € | **618 €** |
| Aus Steuern außerdem | Härtefall | Härtefall | Härtefall, Gesundheit, Seil | Härtefall, Gesundheit, Seil | **Härtefall, Seil, 30 % der Gesundheit** |
| Steuern brauchen | 29,15 | 26,15 | 39,22 | 36,02 | **33,80** |
| Steuern bringen | 30,44 | 28,30 | 33,96 | 33,96 | **33,96** |
| **Saldo** | +1,29 | +2,15 | −5,26 | −2,06 | **+0,16** |
| Prämien je Einwohner (Gesundheit + Seil, Durchschnitt) | 472 € | 472 € | 0 | 0 | **245 €** |
| Dividende je Einwohner nach Prämien | 67 € | −68 € | 521 € | 377 € | **277 €** |
| Altlastenbeitrag 2028 (Zinsen + Z) | 10,64 | 11,34 | 10,73 | 11,48 | **10,73** |
| Altlastenbeitrag 2028, Z zur Hälfte | 6,22 | 6,57 | 6,27 | 6,64 | **6,27** |
| Gesamtlast im Dauerzustand (ohne eigene Vorsorge) | 40,41 | 37,41 | 40,01 | 36,81 | **40,01** |

GB = Grundbedarf (Existenzminimum, DE 2028: 1.071 € im Monat); S = Sozialabdeckung (Gesundheit und Seil je Kopf: 476 €). Gesamtlast heute: 40,76 %.

**Was die Tabelle zeigt:**
1. Mit den Altlasten außerhalb wird auch 28:28 bequemer (+1,29). Aber: Wer kein Einkommen hat, behält nach den Prämien für Gesundheit und Seil
   im Durchschnitt nur **67 €** (bei 25:25 sogar weniger als nichts). Ohne Belastungsgrenzen und Härtefall geht das nicht – genau die Sonderfälle,
   die das System vermeiden soll.
2. 33:33 mit der ganzen Gesundheit in den Steuern trägt sich bei einer Dividende von einem Drittel nicht (−5,26 bzw. −2,06).
3. Die **Lösung** liegt dazwischen: Gesundheit zu 30 % gemeinsam (Kinder, Prävention, Hochkostenpool), Seil ganz gemeinsam. Dann trägt sich die
   Drittelmarke (+0,16), und die Steuern machen zusammen **33,8 % des BIP** aus – ein Drittel.
4. Gleich teuer, aber ohne jede Prämie: Gesundheit und Seil ganz aus Steuern, dafür eine Dividende von einem Viertel des Grundbedarfs
   (DE rund 350 €; Saldo −0,26). Einfacher in der Regel, kleiner in der Zahl auf dem Konto; die Kaufkraft nach Prämien ist fast gleich (rund 300 € je Einwohner gegen 277 €).

## 3 | Die Lösung in Regeln

| Regel | Inhalt |
|---|---|
| **Ein Drittel höchstens** | Kein Satz über 33 %: Einkommen (0/11/19/25/33 % am 1-, 1,5-, 2-, 3-fachen Grundbedarf), Kapitalerträge, Unternehmensgewinne, Erbschaften, oberste Stufe der Mehrwertsteuer (6/13/20/26/33 %). |
| **Ein Drittel gemeinsam** | Alle Steuern zusammen rund ein Drittel der Wirtschaftsleistung (33,8 %). |
| **Ein Drittel für jeden** | Jeden Monat eine Dividende von einem Drittel dessen, was ein Mensch zum Leben einschließlich Absicherung braucht (DE: 516 € Mindestniveau, 2028 618 €); Kinder die Hälfte. |
| **Gemeinsam abgesichert** | Arbeitslosigkeit, Invalidität, Hinterbliebene (Seil) und die gemeinsamen Teile der Gesundheit (Kinder, Vorsorge, große Krankheitskosten) zahlen die Steuern. Der übrige Teil der Gesundheit ist eine Prämie (im Durchschnitt 245 € je Einwohner und Monat). |
| **Eigene Route** | Vorsorge über das Gemeinsame hinaus ist Eigentum, nicht Steuer. |
| **Altlasten getrennt** | Zinsen auf alte Schulden und alte Rentenzusagen trägt jeder Staat selbst, in einem sichtbaren, sinkenden Altlastenbeitrag: 2028 rund 10,7 % des BIP, ab etwa 2075 nur noch die Zinsen (0,8 %). Werden die Zusagen, die keine angesparten Anlagen sind, zur Hälfte gekürzt (Bilanzregel), sind es 2028 rund 6,3 %. |

## 4 | Die Erzählung

**Ein Satz:**
> Ein Drittel höchstens, ein Drittel gemeinsam, ein Drittel für jeden – und was frühere Generationen geliehen und versprochen haben, tragen wir getrennt und offen ab.

**Dreißig Sekunden:**
> Kein Steuersatz liegt über einem Drittel – nicht auf Lohn, nicht auf Kapital, nicht auf Gewinne, nicht auf den Einkauf. Zusammen trägt das ein Drittel
> unserer Wirtschaftsleistung. Davon bekommt jeder Mensch jeden Monat eine Dividende von einem Drittel dessen, was man zum Leben samt Absicherung braucht,
> und wir sind gemeinsam gegen Arbeitslosigkeit, Invalidität und schwere Krankheit abgesichert. Was darüber hinausgeht, gehört dir. Die alten Schulden und
> die alten Rentenversprechen stehen auf einer eigenen Rechnung, werden jedes Jahr kleiner und enden.

**Drei Zahlen:** 33 % höchstens · 33 % gemeinsam · ⅓ des Lebensbedarfs für jeden.

**Was ehrlich dazugehört:**
- Im Übergang zahlen alle mehr als heute (Gesamtlast 2028 rund 50 % mit dem Altlastenbeitrag, heute 40,76 %), weil alte Zusagen weiterlaufen, während
  die Dividende schon allen zusteht. Nach dem Auslauf liegt die Last bei rund 40 %, etwa wie heute.
- Die Dividende allein deckt nicht das ganze Existenzminimum; dafür bleibt der Härtefall (eine Tür je Gemeinde).
- Die Gesundheitsprämie braucht eine Belastungsgrenze; die Alternative ohne Prämie (Abschnitt 2, Punkt 4) hat eine kleinere Dividende.

## 5 | Grenzen

Deckung auf deutscher Basis; keine Ausweichreaktionen bei Kapital, Unternehmen und Erbschaft (bei 33 % eher zu günstig); Z als Schätzung mit
Durchschnittsrentnern; Hochkostenpool mit 30 % der Gesundheitsausgaben als Setzung (Größenordnung gestützt durch die Kostenkonzentration: teuerste 10 %
der Versicherten ≈ 60 % der Ausgaben, bifg 2021); Härtefall 0,65 % als Annahme; Überschuss der Lösung nur 0,16 – Stabilitätsreserve neu prüfen.

## 6 | Zu entscheiden

| Punkt | Entscheidung |
|---|---|
| D1 Marke | 33:33 Lösung / 33:33 ohne Prämie (Dividende ¼ GB) / 28:28 / 25:25 |
| D2 Altlastenbeitrag (Zinsen + Z) getrennt, beim Ausgangsstaat, sinkend | ja / nein |
| D3 Anteil der Zusagen ohne angesparte Anlagen im Altlastenbeitrag | 100 % / 50 % (Bilanzregel) / ___ |
| D4 Gemeinsamer Teil der Gesundheit | 30 % (Kinder, Vorsorge, Hochkostenpool) / ___ |
| D5 Übernahme in Gesamtrechnung und Texte | nach D1–D4 |
