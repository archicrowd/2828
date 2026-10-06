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

# =====================================================================
# 4  BEAMTE UND SELBSTÄNDIGE IN DIE SOZIALVERSICHERUNG
# =====================================================================
print(f'\n[4] EINBEZIEHUNG VON BEAMTEN UND SELBSTÄNDIGEN')
print('''    Das Ziel ist Gleichbehandlung, nicht Gegenfinanzierung. Die Belege sind
    hier eindeutig und sprechen gegen die naheliegende Erwartung:

      IW Köln 2025: Werden die rund 1,9 Mio Beamten einbezogen und trägt der
        Staat den vollen Beitragssatz, entstehen knapp 20 Mrd EUR Mehrkosten
        im Jahr; bei paritätischer Finanzierung 10 Mrd. Kurzfristig fliessen
        mehr Beiträge, langfristig steigen auch die Ausgaben, weil die
        künftigen Beamtenrenten aus dem Umlagesystem zu zahlen wären. Die
        Altersstruktur der Beamten ist dabei ungünstiger als im Durchschnitt.
      DIW 2025: Die Pensionen kosten den Staat schon heute über 63 Mrd EUR
        im Jahr, rund 1,5 % der Wirtschaftsleistung. Durchschnittliche
        Pension 3.240 EUR gegen 1.599 EUR Durchschnittsrente. Deshalb der
        Vorschlag, nur NEU eingestellte Beschäftigte nicht mehr zu verbeamten
        — der "Einführungsgewinn" entsteht dann ohne sofortige Ansprüche.
      DIW 2025: rund 5 Mio Selbständige, viele solo und mit hohem Armutsrisiko
        im Alter. Versicherungspflicht wird als gerecht und angemessen
        bezeichnet, ohne Kostenschätzung.''')

SELB_MIO, SELB_EINK, SELB_SATZ = 3.5, 30000, 0.28
selb = SELB_MIO * SELB_EINK * SELB_SATZ / 1000
BEAMTE_NETTO = -10.0
print(f'''
    EIGENE SCHÄTZUNG, mit offengelegten Setzungen:
      Selbständige: von 5,0 Mio sind rund 1,5 Mio bereits pflichtversichert
        (Versorgungswerke, Künstlersozialkasse, Handwerker, Landwirte).
        Bleiben {de(SELB_MIO,1)} Mio. Durchschnittlich beitragspflichtiges Einkommen
        {de(SELB_EINK/1000,0)} Tsd EUR — bewusst niedrig, weil Solo-Selbständige
        überwiegen. Beitrag {de(SELB_SATZ*100,0)} %, von ihnen allein zu tragen.
        -> {de(selb,1)} Mrd EUR im Jahr.
      Beamte: der Staat zahlt als Arbeitgeber die Hälfte und schuldet die
        bestehende Versorgung weiter. Konsolidiert für die öffentliche Hand
        nach IW rund {de(BEAMTE_NETTO,0)} Mrd EUR.
      Zusammen {pm(selb + BEAMTE_NETTO,1)} Mrd EUR.

    DIESER BETRAG WIRD NICHT AUF DEN SALDO ANGERECHNET.
    Er ist ein Einführungsgewinn: die Beiträge fliessen sofort, die Ansprüche
    entstehen mit. Wer ihn als dauerhafte Gegenfinanzierung bucht, rechnet
    sich reich — denselben Fehler macht die Debatte regelmässig. Er steht
    deshalb als eigene Zeile, nicht in der Summe.''')

# =====================================================================
# ÜBERHOLT AB ABSCHNITT [5] — bitte pfad.py (R9) lesen
# =====================================================================
# Abschnitt [5] rechnet gegen einen Zielsaldo von +42 Mrd EUR im ersten
# Jahr und leitet daraus eine Lücke von 54,9 Mrd ab. Dieses Kriterium ist
# FALSCH gewählt: +42 Mrd ist das Investitionsziel eines Jahres (1 % des
# BIP), nicht die Bedingung, unter der die Haushaltsregel funktioniert.
# Investiert wird nach Regel 1 aus dem Fonds, der mit 100 Mrd startet.
# Der echte Bedarf, gegen den 20-Jahres-Pfad bisektiert, ist 36,1 Mrd.
# Siehe pfad.py und Korrektur 15 im Logbuch. Die Abschnitte [1] bis [4]
# dieser Datei bleiben gültig — die Korrekturen und der Saldo von
# −12,9 Mrd sind in pfad.py unabhängig nachgerechnet und bestätigt.
# =====================================================================

# =====================================================================
# 5  TARIFANPASSUNG: MITTLERE STUFEN
# =====================================================================
VERT = [(6,8000),(11,20000),(12,36000),(7,52000),(5,69000),(3,105000),(1,300000)]
S25, G25 = [0,.08,.14,.19,.23,.25], [12000,25000,40000,55000,70000,float('inf')]
GRENZEN = [12348, 25000, 40000, 55000, 70000, float('inf')]
DD, ETI, LEAK = 515.0*12, 0.35, 0.80

def est(x, saetze, grenzen=GRENZEN):
    s, pr = 0.0, 0.0
    for i, g in enumerate(grenzen):
        if x > pr: s += (min(x, g) - pr) * saetze[i]
        pr = g
        if x <= g: break
    return s

def grenzsatz(b, r, g):
    for gg, x in zip(g, r):
        if b <= gg: return x
    return r[-1]

K_EST = 284 / sum(mio * est(b + 6000, S25, G25) / 1000 for mio, b in VERT)

def est_aufkommen(saetze):
    tot = 0.0
    for mio, b in VERT:
        m0 = grenzsatz(b + DD, S25, G25)
        m1 = grenzsatz(b + DD, saetze, GRENZEN)
        b1 = b * ((1 - m1) / (1 - m0)) ** ETI
        tot += mio * est(b1 + DD, saetze) / 1000
    return K_EST * tot

MWST_GEW = [.10, .10, .20, .30, .30]
BRUTTO = 350 / (0.18 / 1.18)
def mwst_aufkommen(stufen):
    r1 = sum(s * g for s, g in zip(stufen, MWST_GEW)) / 100
    return 350 + (BRUTTO * r1 / (1 + r1) - 350) * LEAK

EST0, MWST0 = est_aufkommen([0, .09, .16, .21, .26, .28]), mwst_aufkommen([5, 11, 17, 22, 28])
print(f'\n[5] TARIFANPASSUNG — DIE MITTLEREN STUFEN')
print(f'    Gegenprobe der nachgebauten Funktionen gegen das Gesamtmodell:')
print(f'      Einkommensteuer {de(EST0,1)} (Modell 313,3) · '
      f'Mehrwertsteuer {de(MWST0,1)} (Modell 375,9)')
print(f'\n    Gesucht: {de(LUECKE,1)} Mrd. Oben bleibt 28 %, unten bleibt 0 %.')
print(f'    Bewegt werden nur die Stufen dazwischen.\n')
print(f'{"ESt-Stufen":>26}{"MwSt-Stufen":>22}{"ESt":>9}{"MwSt":>9}{"zusammen":>11}{"Saldo":>10}')
KANDIDATEN = [
 ([0,.09,.16,.21,.26,.28], [5,11,17,22,28]),
 ([0,.10,.17,.22,.27,.28], [5,12,18,23,28]),
 ([0,.10,.18,.23,.27,.28], [5,12,19,24,28]),
 ([0,.11,.18,.23,.27,.28], [5,13,19,24,28]),
 ([0,.11,.19,.24,.27,.28], [5,13,20,25,28]),
 ([0,.12,.19,.24,.27,.28], [5,13,20,25,28]),
]
for s, m in KANDIDATEN:
    e, mw = est_aufkommen(s), mwst_aufkommen(m)
    plus = (e - EST0) + (mw - MWST0)
    txt_s = '/'.join(str(round(x*100)) for x in s)
    txt_m = '/'.join(str(x) for x in m)
    print(f'{txt_s:>26}{txt_m:>22}{pm(e-EST0,1):>9}{pm(mw-MWST0,1):>9}'
          f'{pm(plus,1):>11}{pm(saldo_neu+plus,1):>10}')
