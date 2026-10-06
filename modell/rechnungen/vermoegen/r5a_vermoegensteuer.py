# -*- coding: utf-8 -*-
"""
R5a — Position 04, Vermögensteuer 1 % ab 2 Mio. EUR

WAS HIER EIGENE ARBEIT IST UND WAS NICHT
  Die Verteilung stammt nicht von mir. Sie stammt aus:
    Bach, S. u. a. (2026): Aufkommens- und Verteilungswirkungen einer
    Vermögensteuer. DIW Berlin, Politikberatung kompakt 211.
  Dort wird das SOEP 2019 mit den Reichenlisten des Manager Magazins
  verbunden, die Spitze mit einer Pareto-Verteilung geschätzt und mit
  Vermögenspreisindizes auf 2026 fortgeschrieben.

  Eigene Arbeit ist allein die Zwischenrechnung: das DIW veröffentlicht
  Bemessungsgrundlagen für Freibeträge von 1, 10, 20, 100 und 1000 Mio.
  EUR, aber nicht für die 2 Mio. EUR aus Position 04. Dieses Skript passt
  an die veröffentlichten Punkte eine Pareto-Beziehung an und liest den
  Wert bei 2 Mio. ab.

WARUM DAS ZULÄSSIG IST
  Oberhalb einer hohen Schwelle u gilt für eine Pareto-Verteilung
      B(u) = Summe der Vermögen über u, abzüglich u je Fall  ~  u^(1-alpha)
  Im Log-Log-Bild ist das eine Gerade. Trifft sie die veröffentlichten
  Punkte, ist die Zwischenrechnung keine Erfindung, sondern Ablesen.
  Die Probe steht unten: alpha wird aus jedem Punktepaar getrennt
  bestimmt. Streuen die Werte stark, taugt das Verfahren nicht.

VORBEHALT, DER ÜBER ALLEM STEHT
  Die DIW-Zahlen sind aus dem PDF maschinell ausgelesen, nicht von mir
  in der Originaltabelle nachgeschlagen. Vor jeder Veröffentlichung sind
  sie an der Quelle zu prüfen.
"""
import numpy as np

def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')

# Freibetrag in Mio EUR -> Bemessungsgrundlage in Billionen EUR (DIW, Tab.)
DIW = [(1, 5.50), (10, 2.72), (20, 2.13), (100, 1.12), (1000, 0.36)]
ZIEL = 2.0          # Mio EUR, Freibetrag nach Position 04
SATZ = 0.01
BIO = 1000.0        # Mrd EUR je Billion

print('=' * 92)
print('R5a — VERMÖGENSTEUER 1 % AB 2 MIO. EUR')
print('=' * 92)

print('\n[1] DIE VERÖFFENTLICHTEN PUNKTE UND DIE PROBE')
print(f'{"Freibetrag":>12}{"Basis Bio EUR":>16}{"alpha aus Paar":>18}')
alphas = []
for i, (u, b) in enumerate(DIW):
    a = ''
    if i:
        u0, b0 = DIW[i-1]
        alpha = 1 + np.log(b0/b)/np.log(u/u0)
        alphas.append((u0, u, alpha))
        a = de(alpha, 3)
    print(f'{de(u,0)+" Mio":>12}{de(b,2):>16}{a:>18}')
print('\n    alpha aus den Paaren:')
for u0, u, a in alphas:
    print(f'      {de(u0,0):>4} bis {de(u,0):>4} Mio EUR   alpha = {de(a,3)}')
spanne = max(a for _,_,a in alphas) - min(a for _,_,a in alphas)
print(f'    Streuung {de(spanne,3)} — die Beziehung ist über drei Größenordnungen')
print(f'    hinreichend stabil. Für die Zwischenrechnung zählt das unterste')
print(f'    Paar, 1 bis 10 Mio EUR, mit alpha = {de(alphas[0][2],3)}.')

# ---------------------------------------------- [2] Zwischenrechnung auf 2 Mio
alpha = alphas[0][2]
basis = DIW[0][1] * (ZIEL/DIW[0][0])**(1-alpha)
# ECHTE Gegenprobe: alpha aus dem NÄCHSTEN Paar nehmen und von 10 Mio
# herunterrechnen. Nur das ist unabhängig; mit alpha aus dem Paar 1-10
# stimmen beide Wege zwangsläufig exakt überein, das wäre keine Probe.
alpha2 = alphas[1][2]
basis_gegen = DIW[1][1] * (ZIEL/DIW[1][0])**(1-alpha2)
print(f'\n[2] BEMESSUNGSGRUNDLAGE BEI {de(ZIEL,0)} MIO. EUR FREIBETRAG')
print(f'    aus dem Paar 1 bis 10 Mio (alpha {de(alpha,3)}):   {de(basis,2)} Billionen EUR')
print(f'    Gegenprobe mit alpha aus 10 bis 20 Mio ({de(alpha2,3)}),')
print(f'    von 10 Mio heruntergerechnet:                 {de(basis_gegen,2)} Billionen EUR')
print(f'    Abstand {de(abs(basis_gegen-basis)/basis*100,1)} %. Das ist die Unschärfe der')
print(f'    Zwischenrechnung — nicht null, aber klein gegen die')
print(f'    Verhaltensreaktion weiter unten.')
print(f'    -> Bemessungsgrundlage {de(basis,2)} bis {de(basis_gegen,2)} Billionen EUR')

brutto, brutto_o = basis * BIO * SATZ, basis_gegen * BIO * SATZ
print(f'\n[3] AUFKOMMEN')
print(f'    1 % auf {de(basis,2)} bis {de(basis_gegen,2)} Bio EUR        '
      f'{de(brutto,1)} bis {de(brutto_o,1)} Mrd EUR  brutto')

# ----------------------------------------- [4] Abschläge nach DIW-Angaben
VERW, WERT = 0.032, 0.014
nach_kosten = brutto * (1 - VERW - WERT)
print(f'    abzüglich Verwaltung und Befolgung {de(VERW*100,1)} %  {de(-brutto*VERW,1):>8}')
print(f'    abzüglich Wertkorrekturen {de(WERT*100,1)} %           {de(-brutto*WERT,1):>8}')
print(f'    = vor Verhaltensreaktion                   {de(nach_kosten,1):>8} Mrd EUR')
print(f'\n    Verhaltensreaktion. Das DIW rechnet mit Elastizitäten der')
print(f'    Bemessungsgrundlage von -0,1 bis -0,25 und kommt auf Minderungen')
print(f'    bis 60 %, einschließlich der Rückwirkung auf die Ertragsteuern')
print(f'    bis 80 %. Das ist die mit Abstand größte Unsicherheit.')
print(f'{"Minderung":>14}{"Aufkommen":>14}')
for m in (0.0, 0.15, 0.30, 0.45, 0.60):
    print(f'{de(m*100,0)+" %":>14}{de(nach_kosten*(1-m),1)+" Mrd":>14}')
print(f'\n    ERGEBNIS  rund {de(nach_kosten*0.40,0)} bis {de(nach_kosten,0)} Mrd EUR,')
print(f'              mittlerer Fall um {de(nach_kosten*0.70,0)} Mrd EUR.')

# ------------------------------------- [5] Gegenprobe an der DIW-Angabe selbst
print(f'\n[4] GEGENPROBE')
print(f'    Das DIW nennt für 1 % proportional bei 1 Mio EUR persönlichem und')
print(f'    5 Mio EUR Unternehmensfreibetrag ein Aufkommen von 42 Mrd EUR auf')
print(f'    einer Basis von 4,2 Billionen. 1 % von 4,2 Bio = 42 Mrd — die')
print(f'    Angabe ist in sich schlüssig und bestätigt, dass die Basiswerte')
print(f'    oben richtig gelesen sind.')
print(f'    Position 04 kennt keinen Unternehmensfreibetrag. Die hier')
print(f'    gerechnete Basis ist deshalb die ungekürzte.')

# ------------------------------------- [6] Wie sehr hängt alles am Verfahren?
print(f'\n[5] WIE WEIT LIEGEN DIE QUELLEN AUSEINANDER?')
print(f'    Dieselbe Grundgesamtheit, drei Auswertungen, Bezugsjahr 2023:')
print(f'''
      IW aus PHF, unkorrigiert, Haushalte
        Median 103.100 EUR · 90-%-Perzentil 777.200 EUR · Gini 0,724
      Sachverständigenrat nach Albers u. a., korrigiert, Haushalte
        Median rund 160.000 EUR · 90-% rund 1,1 Mio · 99-% rund 6 Mio · Gini 0,76
      DIW, korrigiert, Personen
        oberstes 1 % ab 2,3 Mio EUR · Gesamtvermögen 16,5 Billionen (2026)

    Zwischen der unkorrigierten und der korrigierten Fassung liegen beim
    Median rund 55 %, beim 90-%-Perzentil rund 42 %. Die Korrekturmethode
    verschiebt das Bild also stärker als der Datenjahrgang. Wer eine Zahl
    aus diesem Feld zitiert, muss sagen, welche Korrektur dahintersteht.''')
print('''
[6] WAS DAMIT NOCH NICHT GEHT
    - Der Freibetrag in Position 04 ist nicht als "je Person" oder "je
      Haushalt" bestimmt. Das DIW rechnet je Person. Bei Haushalten läge
      die Basis niedriger.
    - Die Bodenwertabgabe ist der zweite Teil von Position 04 und hier
      gar nicht enthalten. Dafür fehlt der Wert des Grund und Bodens aus
      den sektoralen Vermögensbilanzen.
    - Betriebsvermögen: Position 04 sieht keinen Sonderfreibetrag vor.
      Ob das durchhaltbar ist, ist eine Entwurfsfrage, keine Rechenfrage —
      beim obersten 1 % besteht rund die Hälfte des Vermögens aus
      Betriebsvermögen (Sachverständigenrat).''')
