# -*- coding: utf-8 -*-
"""
patch_anhang.py — Anhang "Annahmen und Quellen" nach dem Haushaltsabgleich

Nur de und en führen src_text eigenständig; die übrigen sechs Sprachen
greifen auf den englischen Fallback zurück. Geändert wird:
  - Abschnitt 2: Tarif- und Mehrwertsteuerzeile, Bodenwertabgabe ergänzt
  - neuer Abschnitt 5 HAUSHALTSABGLEICH, die alten 5 und 6 werden 6 und 7
"""
import json, pathlib, re

PAR = {
'de': [("  Stufentarif 0 / 9 / 16 / 21 / 26 / 28 %",
        "  Stufentarif 0 / 9 / 19 / 24 / 27 / 28 %"),
       ("  Mehrwertsteuer-Label 5 / 11 / 17 / 22 / 28 %, Effektivsatz 20,0 %",
        "  Mehrwertsteuer-Label 5 / 11 / 20 / 25 / 28 %, Effektivsatz 21,5 %")],
'en': [("  Bracket tariff 0 / 9 / 16 / 21 / 26 / 28 %",
        "  Bracket tariff 0 / 9 / 19 / 24 / 27 / 28 %"),
       ("  VAT label 5 / 11 / 17 / 22 / 28 %, effective rate 20.0 %",
        "  VAT label 5 / 11 / 20 / 25 / 28 %, effective rate 21.5 %")]}

# An Abschnitt 2 angehängt, vor der Digitaldividende-Zeile
BODEN = {
'de': ("""  Grundsteuer: nur auf den Boden, aufkommensneutral. Bodenwert
    3.529 Mrd. EUR aus den sektoralen Vermögensbilanzen; ein Satz von
    0,22 bis 0,44 % tragt die heutigen 15,5 Mrd. EUR. KEINE Mehreinnahme.
""", "  Digitaldividende 50 % des Existenzminimums"),
'en': ("""  Property tax: on land only, revenue-neutral. Land value
    3,529 bn EUR from the sectoral balance sheets; a rate of 0.22 to
    0.44 % carries today's 15.5 bn EUR. NOT additional revenue.
""", "  Digital dividend 50 % of subsistence income")}

NEU = {
'de': """5 | HAUSHALTSABGLEICH
  Die Prüfungen R1 bis R6 haben sechs Posten des Modells korrigiert.
  Nach unten: Erbschaft 35,9 auf 21,0 (Freibetrag 200.000 statt 0);
  CO2 70,0 auf 33,0 (Preiskorridor des BEHG statt 100 bis 150 EUR);
  Bodenwertabgabe 20,0 auf 0,0 (aufkommensneutral, siehe Abschnitt 2);
  Unternehmen 157,6 auf 152,0; Vermögen 32,7 auf 30,0. Zusammen
  −80,2 Mrd. EUR. Der Saldo des ersten Jahres fällt damit von +67,3
  auf −12,9 Mrd. EUR.
  Der Pfad trägt das dennoch: der Fonds startet mit 100 Mrd. EUR, und
  investiert wird nach Regel 1 aus dem Fonds, nicht aus dem Jahressaldo.
  Geprüft wurde deshalb nicht der Jahressaldo, sondern der Pfad über
  20 Jahre. Ohne Gegenmaßnahme bleibt er in den ersten beiden Szenarien
  ohne Lückenjahr, im Stress-Szenario entstehen fünf.
  GEGENMASSNAHME: die mittleren Stufen beider Steuern steigen um
  3 Punkte — Einkommensteuer 16/21/26 auf 19/24/27 %, Mehrwertsteuer
  17/22 auf 20/25 %. Das bringt 38,9 Mrd. EUR bei einem Bedarf von
  36,1. Danach hat kein Szenario ein Lückenjahr; das vorsichtige
  erreicht 99,5 % des Investitionsziels.
  WAS DAS KOSTET: weil der Spitzensatz bei 28 % feststeht, trifft die
  Anhebung die Spitze nur mit einem festen Betrag. Die Zusatzlast liegt
  zwischen 0,97 % des Einkommens oben und 2,63 % in der Mitte, steigt
  also nicht mit dem Einkommen. Keine der 335 geprüften Kombinationen
  vermeidet das — bei fixiertem Spitzensatz ist es unvermeidbar.
  Die Nettoposition einschliesslich Dividende bleibt progressiv.
  NICHT ANGERECHNET: die Einbeziehung von Beamtinnen, Beamten und
  Selbständigen. Sie ist als Gleichbehandlung begründet, nicht als
  Gegenfinanzierung — siehe Position 10 im Belegstand.
""",
'en': """5 | BUDGET RECONCILIATION
  Checks R1 to R6 corrected six items of the model, all downwards:
  inheritance 35.9 to 21.0 (allowance 200,000 instead of none); carbon
  70.0 to 33.0 (the statutory price corridor instead of 100 to 150 EUR);
  land levy 20.0 to 0.0 (revenue-neutral, see section 2); companies
  157.6 to 152.0; wealth 32.7 to 30.0. Together −80.2 bn EUR. The
  first-year balance therefore falls from +67.3 to −12.9 bn EUR.
  The path carries that nonetheless: the fund starts with 100 bn EUR,
  and investment comes out of the fund under rule 1, not out of the
  annual balance. What was tested is therefore not the annual balance
  but the twenty-year path. Without a counter-measure it has no gap
  year in the first two scenarios and five in the stress scenario.
  COUNTER-MEASURE: the middle steps of both taxes rise by 3 points —
  income tax 16/21/26 to 19/24/27 %, VAT 17/22 to 20/25 %. That yields
  38.9 bn EUR against a need of 36.1. After it no scenario has a gap
  year, and the cautious one reaches 99.5 % of the investment target.
  WHAT IT COSTS: because the top rate is fixed at 28 %, the increase
  hits the top only with a fixed amount. The additional burden runs
  from 0.97 % of income at the top to 2.63 % in the middle, so it does
  not rise with income. None of the 335 combinations tested avoids
  this — with a fixed top rate it is unavoidable. The net position
  including the dividend remains progressive.
  NOT COUNTED: including civil servants and the self-employed. It is
  justified as equal treatment, not as financing — see position 10 in
  the evidence table.
"""}

for code in ('de', 'en'):
    p = pathlib.Path(f'lang/{code}.json')
    d = json.loads(p.read_text())
    t = d['src_text']
    for alt, neu in PAR[code]:
        assert t.count(alt) == 1, f'{code}: "{alt}" {t.count(alt)}x'
        t = t.replace(alt, neu)
    zus, anker = BODEN[code]
    assert t.count(anker) == 1, f'{code}: Anker "{anker}" {t.count(anker)}x'
    t = t.replace(anker, zus + anker)
    # Abschnitte 6 und 5 hochzählen, in dieser Reihenfolge
    for a, b in ((r'^6 \| ', '7 | '), (r'^5 \| ', '6 | ')):
        t2 = re.sub(a, b, t, flags=re.M)
        assert t2 != t, f'{code}: {a} nicht gefunden'
        t = t2
    # neuen Abschnitt 5 vor dem (jetzt) 6. einsetzen
    m = re.search(r'^6 \| ', t, re.M)
    t = t[:m.start()] + NEU[code] + '\n' + t[m.start():]
    d['src_text'] = t
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
    secs = re.findall(r'^(\d) \| (.+)$', t, re.M)
    print(f'lang/{code}.json  {len(t)} Zeichen')
    for n, ti in secs: print(f'    {n} | {ti}')
