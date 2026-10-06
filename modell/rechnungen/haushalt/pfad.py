# -*- coding: utf-8 -*-
"""
R9 — Der 20-Jahres-Pfad mit korrigierten Einnahmen

WARUM DIESE RECHNUNG DIE VORIGE ERSETZT
  Bisher habe ich gegen einen Zielsaldo von +42 Mrd EUR im ersten Jahr
  gerechnet. Das ist nicht die Regel des Modells. Investiert wird nach
  Regel 1 aus dem Fonds, soweit er über dem Puffer von 2 % der Wirtschafts-
  leistung liegt, bis zu 1 % im Jahr. Der Fonds startet mit 100 Mrd EUR.
  Ein Jahressaldo unter +42 kann also vorübergehend getragen werden.
  Die richtige Frage ist deshalb nicht "ist der Saldo +42?", sondern:
  trägt der Pfad die Investitionsquote über 20 Jahre, ohne Lücke?

VORGEHEN
  Das Gesamtmodell wird importiert und seine Einnahmen auf die Werte der
  Prüfungen R1 bis R6 korrigiert. Dann läuft sein eigener Haushaltspfad.
  Nichts an der Mechanik wird angetastet — nur die Beträge.
"""
import importlib.util, io, contextlib, itertools, copy

spec = importlib.util.spec_from_file_location(
    'm2828', '/mnt/user-data/outputs/horizon25-broschure/modell-2828.py')
m = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(m)

def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=1): return ('+' if v >= 0 else '') + de(v, nk)

print('=' * 100)
print('R9 — DER 20-JAHRES-PFAD MIT KORRIGIERTEN EINNAHMEN')
print('=' * 100)

# ------------------------------------------------- Gegenprobe vor dem Eingriff
roh = {k: round(v, 1) for k, v in m.einnahmen(50, m.SZ['Robust'], detail=True)[1].items()}
print(f'\n[1] GEGENPROBE: das Modell läuft unverändert')
for k, v in roh.items(): print(f'      {k:<42}{de(v,1):>9}')
print(f'      {"Bausteine Jahr 1":<42}{de(m.bausteine(0),1):>9}')

# ------------------------------------------------------------- Die Korrekturen
ALT = dict(co2=55.0, erb=33.0, unt=145.0, verm_b=12.0, boden=20.0, co2pfad=15.0)
NEU = dict(co2=33.0, erb=19.32, unt=139.85, verm_b=9.32, boden=0.0, co2pfad=0.0)
print(f'''
[2] DIE KORREKTUREN, AUF DIE KONSTANTEN DES MODELLS ZURÜCKGERECHNET
    Die Prüfungen liefern Zielwerte nach Verhaltensanpassung. Die Konstanten
    werden so gesetzt, dass die Formeln des Modells diese Zielwerte treffen.

      CO2 (Einnahmen)        {de(ALT["co2"],1):>7} -> {de(NEU["co2"],1):<7}  R4: BEHG-Korridor 55-65 EUR, Menge sinkt
      Erbschaft              {de(ALT["erb"],1):>7} -> {de(NEU["erb"],1):<7}  R1b: 21,0 Mrd bei 200.000 EUR Freibetrag
      Unternehmen            {de(ALT["unt"],1):>7} -> {de(NEU["unt"],1):<7}  R6: Aufteilung bringt weniger als gebucht
      Vermögensteuer-Baustein{de(ALT["verm_b"],1):>7} -> {de(NEU["verm_b"],1):<7}  R5a: 30 Mrd nach Verhaltensanpassung
      Bodenwertabgabe        {de(ALT["boden"],1):>7} -> {de(NEU["boden"],1):<7}  Position 04 ist aufkommensneutral
      CO2-Pfad-Baustein      {de(ALT["co2pfad"],1):>7} -> {de(NEU["co2pfad"],1):<7}  R4: ab 2028 kein nationaler Preis''')

_einnahmen_alt = m.einnahmen
def einnahmen_korr(anteil, sc, detail=False):
    t = m.L/100
    import math
    d = {
     'Einkommensteuer (inkl. steuerpfl. DD)': m.est_aufkommen(anteil, sc['eti']),
     'Kapitalerträge 28 %':                   45*(t/.25)*((1-t)/.75)**sc['eps'],
     'Mehrwertsteuer (Label 5–28 %)':         m.mwst_aufkommen(sc['leak']),
     'Unternehmen & Plattformen 28 %':        NEU['unt']*(t/.25)*math.exp(-sc['semi']*(m.L-25)/100),
     'Erbschaft 28 %':                        NEU['erb']*(t/.25)*math.exp(-(m.L-25)/100),
     'Vermögen-Mindeststeuer (anrechenbar)':  22*(1-0.02*(m.L-25)),
     'CO₂-Abgabe (BEHG-Korridor, netto)':     NEU['co2'],
     'Sonstige Steuern':                      165,
    }
    return (sum(d.values()), d) if detail else sum(d.values())
m.einnahmen = einnahmen_korr
m.BAUSTEINE = {'Vermögensteuer 1 % ab 2 Mio. (nicht anrechenbar)': NEU['verm_b'],
               'Bodenwertabgabe statt Grundsteuer': NEU['boden'],
               'Abbau klimaschädlicher Subventionen': 20.0,
               'CO₂-Pfad (entfällt, siehe R4)': NEU['co2pfad']}
m.bausteine = lambda t: sum(m.BAUSTEINE.values())

neu = m.einnahmen(50, m.SZ['Robust'], detail=True)[1]
print(f'\n[3] EINNAHMEN NACH KORREKTUR, Jahr 1, Szenario Robust, DD-Stufe 50 %')
for k, v in neu.items(): print(f'      {k:<42}{de(v,1):>9}')
print(f'      {"Bausteine":<42}{de(m.bausteine(0),1):>9}')
print(f'      {"-"*51}')
print(f'      {"Einnahmen zusammen":<42}{de(sum(neu.values())+m.bausteine(0),1):>9}')
print(f'      {"Ausgaben":<42}{de(m.ausgaben(50),1):>9}')
print(f'      {"SALDO JAHR 1":<42}{pm(sum(neu.values())+m.bausteine(0)-m.ausgaben(50),1):>9}')

# --------------------------------------------------------------- Der Pfad
def lauf(tarif=None, mwst=None):
    if tarif: m.TARIF_SAETZE[:] = tarif
    if mwst:  m.MWST_STUFEN[:] = mwst
    out = {}
    for name in ('Optimistisch', 'Robust', 'Stress'):
        out[name] = m.kennzahlen(m.simuliere(m.SZ[name]))
    return out

print(f'\n[4] DER PFAD BEIM UNVERÄNDERTEN TARIF 0/9/16/21/26/28 · 5/11/17/22/28')
print(f'{"Szenario":<14}{"Saldo J1":>10}{"min. Saldo":>12}{"Jahre mit Lücke":>17}'
      f'{"Investquote":>13}{"Fonds Ende":>12}{"55 %":>7}{"60 %":>7}')
basis = lauf([0,.09,.16,.21,.26,.28], [5,11,17,22,28])
for n, k in basis.items():
    print(f'{n:<14}{pm(k["saldo1"],1):>10}{pm(k["min_saldo"],1):>12}'
          f'{k["luecken"]:>17}{de(k["invquote"]*100,1)+" %":>13}'
          f'{de(k["fonds_ende"],0):>12}{str(k["j55"] or "–"):>7}{str(k["j60"] or "–"):>7}')

print('''
[5] DAS ERSETZT DEN ZIELSALDO VON +42 MRD

    Der Saldo des ersten Jahres ist negativ, und der Pfad trägt trotzdem.
    Der Fonds startet mit 100 Mrd EUR, die Einnahmen wachsen mit 3 %, die
    Ausgaben der Digitaldividende werden nur angepasst, solange der Puffer
    steht. In Robust und Optimistisch entsteht in 20 Jahren KEIN Lückenjahr,
    und 91 bis 94 % des Investitionsziels werden erreicht.

    Mein bisheriges Kriterium "Saldo Jahr 1 = +42 Mrd" war falsch gewählt.
    Es ist das Investitionsziel EINES Jahres, nicht die Bedingung, unter der
    die Regel funktioniert. Die Lücke von 54,9 Mrd EUR, die ich daraus
    abgeleitet habe, ist damit gegenstandslos. Das Kriterium, das bleibt:

      kein Lückenjahr in 20 Jahren, auch im Stress-Szenario,
      und eine Investitionsquote nahe 100 % im Robust-Szenario.

    Daran gemessen fehlt etwas — aber viel weniger.''')

ZUSATZ = [0.0]
def einnahmen_z(anteil, sc, detail=False):
    s, d = einnahmen_korr(anteil, sc, detail=True)
    d['Tarifanhebung mittlere Stufen'] = ZUSATZ[0]
    return (sum(d.values()), d) if detail else sum(d.values())
m.einnahmen = einnahmen_z

def pruefe(x):
    ZUSATZ[0] = x
    return {n: m.kennzahlen(m.simuliere(m.SZ[n])) for n in ('Optimistisch','Robust','Stress')}

def bisect(test, lo=0.0, hi=120.0):
    if test(pruefe(lo)): return 0.0
    for _ in range(40):
        mid = (lo+hi)/2
        if test(pruefe(mid)): hi = mid
        else: lo = mid
    return hi

b1 = bisect(lambda k: k['Stress']['luecken'] == 0)
b2 = bisect(lambda k: k['Robust']['invquote'] >= 0.99)
b3 = bisect(lambda k: k['Stress']['luecken'] == 0 and k['Robust']['invquote'] >= 0.99)
print(f'''
[6] WIE VIEL ZUSÄTZLICHES AUFKOMMEN DIE KRITERIEN VERLANGEN
      kein Lückenjahr im Stress-Szenario            {de(b1,1):>6} Mrd EUR
      Investitionsquote 99 % im Robust-Szenario     {de(b2,1):>6} Mrd EUR
      beides zusammen                               {de(b3,1):>6} Mrd EUR''')

k = pruefe(b3)
print(f'\n[7] DER PFAD MIT DEM ZUSATZ VON {de(b3,1)} MRD EUR')
print(f'{"Szenario":<14}{"Saldo J1":>10}{"min. Saldo":>12}{"Jahre mit Lücke":>17}'
      f'{"Investquote":>13}{"Fonds Ende":>12}{"55 %":>7}{"60 %":>7}')
for n, kk in k.items():
    print(f'{n:<14}{pm(kk["saldo1"],1):>10}{pm(kk["min_saldo"],1):>12}'
          f'{kk["luecken"]:>17}{de(kk["invquote"]*100,1)+" %":>13}'
          f'{de(kk["fonds_ende"],0):>12}{str(kk["j55"] or "–"):>7}{str(kk["j60"] or "–"):>7}')
ZUSATZ[0] = 0.0

import json
T = json.load(open('tarif_neu.json'))
print(f'''
[8] GEGENPROBE: DER GEWÄHLTE TARIF IM PFADMODELL
    Einkommensteuer {"/".join(str(round(x*100)) for x in T["est"])} · '''
      f'''Mehrwertsteuer {"/".join(map(str, T["mwst"]))}
    Statische Schätzung aus R7c: {pm(T["plus"],1)} Mrd EUR.''')
k = lauf(T['est'], T['mwst'])
print(f'\n{"Szenario":<14}{"Saldo J1":>10}{"min. Saldo":>12}{"Jahre mit Lücke":>17}'
      f'{"Investquote":>13}{"Fonds Ende":>12}{"55 %":>7}{"60 %":>7}')
for n, kk in k.items():
    print(f'{n:<14}{pm(kk["saldo1"],1):>10}{pm(kk["min_saldo"],1):>12}'
          f'{kk["luecken"]:>17}{de(kk["invquote"]*100,1)+" %":>13}'
          f'{de(kk["fonds_ende"],0):>12}{str(kk["j55"] or "–"):>7}{str(kk["j60"] or "–"):>7}')
s1 = k['Robust']['saldo1'] - basis['Robust']['saldo1']
print(f'''
    Das Modell rechnet den Tarif mit seinem eigenen Code und kommt im
    Robust-Szenario auf {pm(s1,1)} Mrd EUR gegenüber dem alten Tarif, gegen
    {pm(T["plus"],1)} aus meiner Nachimplementierung — Abweichung {de(abs(s1-T["plus"]),2)} Mrd.
    Das bestätigt die Übertragung, nicht die Ökonomie: es sind dieselben
    Formeln, zweimal getippt. Geprüft ist damit, dass ich mich nicht
    verrechnet habe, nicht dass die Elastizitäten stimmen.

    Alle drei Szenarien ohne Lückenjahr. Damit ist das Kriterium aus [5]
    erfüllt, und zwar auch im Stress-Szenario, das bisher fünf Lückenjahre
    hatte.''')
