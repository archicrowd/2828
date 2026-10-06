# -*- coding: utf-8 -*-
"""
SCHLUSSABGLEICH — alle Belege der letzten Tage gegen das Haushaltsmodell

WAS HIER PASSIERT
  Das Gesamtmodell (modell-2828.py) wurde kalibriert, bevor die
  Einzelrechnungen vorlagen. Jetzt werden seine Posten gegen die Belege
  gestellt, Abweichungen beziffert und der Saldo neu gebildet.

QUELLEN DER KORREKTUREN
  Erbschaft    R1, Statistisches Bundesamt, Erbschaft- und Schenkungsteuer-
               statistik 2024, Bericht 73611
  Boden        R5b, Destatis WISTA 6/2015; Grundsteueraufkommen Destatis 2025
  CO2          R4, Drittes BEHG-Änderungsgesetz §§ 10, 44; DEHSt-Kennzahlen 2025
  Subventionen R4b, Umweltbundesamt 2021, Datenjahr 2018
  Vermögen     R5a, DIW Politikberatung kompakt 211 (2026)
  Konzerne     R6, OECD CbCR Tabelle I, 2016-2023
  Sozialvers.  IW Köln 2025; DIW 2025

EINE REGEL FÜR DEN GANZEN ABGLEICH
  Wo ein Beleg eine Spanne liefert, wird der MITTLERE Wert gesetzt und die
  Spanne mitgeführt. Wo gar nichts vorliegt, bleibt der Modellwert stehen
  und ist unten als solcher gekennzeichnet.
"""
import math, sys

sys.path.insert(0, '/mnt/user-data/outputs/horizon25-broschure')

def de(v, nk=1):
    s = format(abs(v), f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
    return ('−' if v < 0 else '') + s

def pm(v, nk=1):
    s = format(abs(v), f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
    return ('+' if v >= 0 else '−') + s

BIP = 4200.0     # Modellbasis, Mrd EUR

# ---------------------------------------------------------------- Modellstand
MODELL = {
 'Einkommensteuer (inkl. steuerpfl. DD)': 313.3,
 'Kapitalerträge 28 %':                    48.8,
 'Mehrwertsteuer (Label 5–28 %)':         375.9,
 'Unternehmen und Plattformen 28 %':      157.6,
 'Erbschaft 28 %':                         35.9,
 'Vermögen-Mindeststeuer (anrechenbar)':   20.7,
 'CO₂-Abgabe 100 €/t (netto)':             55.0,
 'Sonstige Steuern':                      165.0,
}
BAUSTEINE = {
 'Vermögensteuer 1 % ab 2 Mio.':          12.0,
 'Bodenwertabgabe statt Grundsteuer':     20.0,
 'Abbau klimaschädlicher Subventionen':   20.0,
 'CO₂-Pfad 100 → 150 €/t':                15.0,
}
AUSGABEN = {'Basis': 596.0, 'SV-Zuschuss': 60.0, 'Härtefall und Gesundheit': 40.0,
            'Digitaldividende': 475.9}

print('=' * 100)
print('SCHLUSSABGLEICH — BELEGE GEGEN MODELL, STUFE 515 EUR, SZENARIO ROBUST')
print('=' * 100)

e0 = sum(MODELL.values()); b0 = sum(BAUSTEINE.values()); a0 = sum(AUSGABEN.values())
print(f'\n[0] AUSGANGSLAGE')
print(f'    Einnahmen Kernsystem {de(e0,1)} + Bausteine {de(b0,1)} = {de(e0+b0,1)} Mrd')
print(f'    Ausgaben {de(a0,1)} Mrd  ->  Saldo {pm(e0+b0-a0,1)} Mrd '
      f'({pm((e0+b0-a0)/BIP*100,2)} % BIP)')
print(f'    Zielsaldo für Investitionen: +42 Mrd (1 % BIP)')

# ------------------------------------------------------------- Korrekturen
# (Posten, alt, neu, Begründung, Spanne unten/oben)
KORR = [
 ('Erbschaft 28 %', 35.9, 21.0,
  'R1: amtliche Statistik, 200.000 EUR Freibetrag je Erwerb, keine Verschonungen. '
  'Das Modell hatte 400.000 EUR und einen höheren Ansatz.', 20.3, 22.3),
 ('Bodenwertabgabe statt Grundsteuer', 20.0, 0.0,
  'R5b: Position 04 ist ein UMBAU der Grundsteuer bei gleichem Aufkommen, keine '
  'zusätzliche Abgabe. Die Grundsteuer steckt bereits in den sonstigen Steuern. '
  'Der Posten war eine Doppelzählung.', 0.0, 0.0),
 ('CO₂ gesamt (Abgabe + Pfad)', 70.0, 33.0,
  'R4: § 44 Abs. 2 BEHG, Menge 2026 252,4 Mio t. Bei 100 EUR/t 25,2 Mrd im nationalen '
  'Handel, dazu geschätzt 8 Mrd deutsche Versteigerungserlöse aus dem EU-ETS 1. '
  'Der Modellwert von 70 war nicht belegbar.', 28.0, 40.0),
 ('Vermögen gesamt (Mindest- und Vermögensteuer)', 32.7, 30.0,
  'R5a: DIW-Verteilung, Pareto-Zwischenrechnung auf 2 Mio EUR Freibetrag, '
  '1 % Satz, nach Verwaltungskosten und mittlerer Verhaltensreaktion.', 17.0, 42.0),
 ('Unternehmen und Plattformen 28 %', 157.6, 152.0,
  'R6: Position 05 bringt im Konzernsegment netto +4,7 bis +10,0 Mrd gegenüber heute, '
  'nicht +12,6. Der Satz von 28 % ist für Deutschland eine Senkung; nur die Zerlegung '
  'nach dem Kundenort trägt den Zuwachs.', 149.0, 155.0),
]
print(f'\n[1] KORREKTUREN AUS DEN BELEGEN')
print(f'{"Posten":<46}{"Modell":>9}{"belegt":>9}{"Änderung":>11}{"Spanne":>16}')
delta = 0.0
for name, alt, neu, grund, lo, hi in KORR:
    delta += neu - alt
    print(f'{name:<46}{de(alt,1):>9}{de(neu,1):>9}{pm(neu-alt,1):>11}'
          f'{de(lo,1)+" bis "+de(hi,1):>16}')
print(f'{"Summe der Korrekturen":<46}{"":>9}{"":>9}{pm(delta,1):>11}')
print()
for name, alt, neu, grund, lo, hi in KORR:
    print(f'  {name}')
    for z in [grund[i:i+88] for i in range(0, len(grund), 88)]:
        print(f'      {z}')

# ------------------------------------------- Unverändert, weil unbelegt
print(f'\n[2] UNVERÄNDERT STEHEN GEBLIEBEN, WEIL KEIN BELEG VORLIEGT')
print('''    Abbau klimaschädlicher Subventionen, 20,0 Mrd. Das Umweltbundesamt weist für
    2018 statisch 47 Mrd als aufkommenswirksam aus; davon ist der Spitzenausgleich
    entfallen, und der statische Wert einer Steuervergünstigung ist nicht ihr
    Abbauertrag. 20 Mrd sind rund 44 % des statischen Werts — ein vertretbarer
    Abschlag, aber eine Setzung.
    Sonstige Steuern, 165,0 Mrd, und die Ausgabenblöcke: nicht Gegenstand dieser
    Prüfung.''')

saldo_alt = e0 + b0 - a0
saldo_neu = saldo_alt + delta
print(f'\n[3] NEUER SALDO')
print(f'    bisher {pm(saldo_alt,1)} Mrd  ->  nach Korrektur {pm(saldo_neu,1)} Mrd '
      f'({pm(saldo_neu/BIP*100,2)} % BIP)')
print(f'    Lücke zum Zielsaldo von +42 Mrd: {de(42-saldo_neu,1)} Mrd')
LUECKE = 42 - saldo_neu
