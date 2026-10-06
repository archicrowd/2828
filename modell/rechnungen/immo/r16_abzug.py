# -*- coding: utf-8 -*-
"""
R16 — Ist der Abzug der Grundsteuer vom Verkaufsgewinn richtig?

ANLASS
  Ich hatte in R12 geschrieben, ohne Anrechnung werde "zweimal besteuert":
  die laufende Abgabe erfasse den Zuwachs, während er entsteht, der
  Verkaufsgewinn danach noch einmal. Daraus hatte ich den vollen Abzug
  abgeleitet und ihn in die Kachel geschrieben — ohne ihn zu rechnen.
  Beides wird hier geprüft: die Begründung und die Größenordnung.

DIE PRÜFUNG DER BEGRÜNDUNG
  Die laufende Grundsteuer besteuert den WERT, also einen Bestand. Der
  Veräußerungsgewinn besteuert den ZUWACHS, also eine Veränderung. Das
  sind verschiedene Bemessungsgrundlagen, nicht dieselbe zweimal.
  Die Entsprechung ist eine Aktie: wer Dividende versteuert und beim
  Verkauf den Kursgewinn, wird nicht doppelt besteuert. Die Grundsteuer
  entspricht der Dividende, der Verkaufsgewinn dem Kursgewinn.
  Meine Doppelbesteuerungsbehauptung war damit falsch.
"""
import json, numpy as np

def de(v, nk=0):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=0): return ('+' if v >= 0 else '') + de(v, nk)

HPI = {int(k): v for k, v in json.load(open('hpi.json')).items()}
J0, J1 = min(HPI), max(HPI)
BODEN_ANT = {'Land': 0.20, 'Mittelstadt': 0.35, 'Großstadt': 0.55, 'München': 0.70}
REGIO_DYN = {'Land': 0.75, 'Mittelstadt': 1.00, 'Großstadt': 1.35, 'München': 1.60}
SATZ, EINMAL = 0.28, 300_000
# 04a aufkommensneutral: 15,5 Mrd auf 3.529 Mrd Bodenwert (R5b) = 0,44 %;
# die Spanne dort war 0,22 bis 0,44. Zentral gerechnet mit 0,35 %.
GRST = 0.0035
DISKONT = 0.03

def hpi(j): return HPI[min(max(j, J0), J1)]
def wert(preis, kauf, jahr, reg):
    i1 = hpi(J1) * 1.032 if jahr > J1 else hpi(jahr)
    return preis * (1 + (i1 / hpi(kauf) - 1) * REGIO_DYN[reg])

FAELLE = [
 ('Reihenhaus Landkreis Sachsen',     2005, 'Land',        110_000, 'aus'),
 ('Einfamilienhaus Kleinstadt NRW',   2000, 'Mittelstadt', 185_000, 'aus'),
 ('Altbauwohnung München',            2000, 'München',     180_000, 'aus'),
 ('Einfamilienhaus Münchner Umland',  2010, 'München',     420_000, 'aus'),
 ('Vermietetes Haus Hamburg',         2012, 'Großstadt',   890_000, 'verm'),
 ('Neubau Brandenburg, Kauf im Hoch', 2022, 'Land',        395_000, 'aus'),
]
print('=' * 100)
print('R16 — DER ABZUG DER GRUNDSTEUER VOM VERKAUFSGEWINN')
print('=' * 100)

print(f'''
[1] DIE GRÖSSENORDNUNG — was ich hätte einpreisen müssen
    Grundsteuer {de(GRST*100,2)} % des Bodenwerts im Jahr, Bodenwert jährlich
    fortgeschrieben mit der amtlichen Preisreihe.
''')
print(f'{"Fall":<34}{"Jahre":>6}{"Gewinn":>12}{"GrSt kumuliert":>16}'
      f'{"in % Gewinn":>13}{"Steuer ohne":>13}{"mit Abzug":>11}')
tab = []
for name, kj, reg, preis, art in FAELLE:
    g = wert(preis, kj, 2026, reg) - preis
    kum = sum(wert(preis, kj, j, reg) * BODEN_ANT[reg] * GRST
              for j in range(kj, 2026))
    def steuer(gew):
        if art == 'verm': return max(gew, 0) * SATZ
        if gew <= EINMAL: return 0.0
        return (gew - EINMAL) * SATZ
    s0, s1 = steuer(g), steuer(g - kum)
    tab.append((name, kj, g, kum, s0, s1, art))
    print(f'{name[:33]:<34}{2026-kj:>6}{pm(g):>12}{de(kum):>16}'
          f'{de(kum/abs(g)*100,1)+" %":>13}{de(s0):>13}{de(s1):>11}')
print(f'''
    Der Abzug kostet in diesen Fällen {de(sum(t[4]-t[5] for t in tab))} EUR von {de(sum(t[4] for t in tab))} EUR,
    also {de(sum(t[4]-t[5] for t in tab)/sum(t[4] for t in tab)*100,1)} %. Nicht dramatisch — aber meine Fallzahlen waren
    um diesen Betrag zu hoch.''')

print(f'''
[2] KORREKTUR AN MIR SELBST: DIE KAPITALISIERUNG IST KEINE ZWEITE LAST
    Ich war versucht, so zu argumentieren: die Abgabe drückt den Bodenpreis,
    also hat sie den Zuwachs schon abgeschöpft. Das ist falsch. Der
    Preisrückgang IST der Barwert der künftigen Abgaben — wer hält und zahlt,
    trägt die Zahlungen; wer sofort verkauft, trägt den Preisverlust. Niemand
    trägt beides. Die Kapitalisierung ist der Übertragungsweg der Last, nicht
    eine zusätzliche Last.

    Der Befund, der daraus wirklich folgt, betrifft nicht den Abzug, sondern
    das MODELL: eine laufende Bodenabgabe senkt das Preisniveau dauerhaft und
    damit alle künftigen Gewinne. 04a und 04b sind nicht addierbar.
    Bei {de(GRST*100,2)} % Abgabe und {de(DISKONT*100,0)} % Diskontsatz liegt der Bodenwert dauerhaft
    rund {de(GRST/DISKONT*100,1)} % niedriger. Bei einem Bodenanteil von durchschnittlich 40 %
    am Objektwert sind das {de(GRST/DISKONT*0.40*100,1)} % weniger Verkaufspreis — und damit
    grob {de(GRST/DISKONT*0.40*100,1)} % weniger Gewinnvolumen für 04b.
    Auf die +4,3 Mrd aus R15 angewandt: rund {de(4.3*GRST/DISKONT*0.40,1)} Mrd weniger,
    also etwa {de(4.3*(1-GRST/DISKONT*0.40),1)} Mrd. Das gehört in den Haushaltsabgleich.
''')

print(f'''
[3] DER ENTSCHEIDENDE PUNKT, DEN ICH ÜBERSEHEN HATTE
    Bei VERMIETETEN Objekten ist die Grundsteuer bereits Werbungskosten
    und wird von den Mieteinnahmen abgezogen — heute wie künftig. Ein
    zweiter Abzug beim Verkauf wäre eine doppelte Entlastung, nicht eine
    Vermeidung doppelter Belastung.

    Bei SELBSTGENUTZTEN Objekten gibt es keine Einnahme, von der etwas
    abzuziehen wäre. Dafür gibt es aber auch keinen versteuerten Ertrag:
    Deutschland besteuert den Nutzungswert des Eigenheims nicht — anders
    als Dänemark mit der ejendomsværdiskat und die Niederlande. Die
    Grundsteuer ist hier faktisch der einzige Zugriff auf einen sonst
    unbesteuerten Konsum. Ein Abzug würde eine Konsumsteuer in
    Anlagekosten umdeuten.

[4] DER VOLLZUGSEINWAND, der allein schon reicht
    Ein voller Abzug verlangt, dass jeder Eigentümer die Grundsteuer-
    bescheide über die gesamte Haltedauer aufbewahrt — in den Fällen oben
    bis zu {max(2026-t[1] for t in tab)} Jahre. Dafür ein Effekt von {de(sum(t[4]-t[5] for t in tab)/sum(t[4] for t in tab)*100,1)} % auf die Steuer.
    Das ist ein schlechtes Verhältnis, und es widerspricht dem Anspruch,
    dass die Regel erklärbar bleibt.

[5] ERGEBNIS: KEIN ABZUG, UND DIE KACHEL MUSS GEÄNDERT WERDEN
    Drei unabhängige Gründe, jeder für sich tragend:
      - verschiedene Bemessungsgrundlagen, keine Doppelbesteuerung
      - bei Vermietung schon als Werbungskosten abgezogen
      - bei Eigennutzung Zugriff auf unbesteuerten Nutzungswert
    Dazu der Vollzugseinwand. Der Satz "die laufend gezahlte Grundsteuer
    wird abgezogen" fällt aus der Kachel.

    WAS DAGEGEN SPRICHT, fair benannt: in einem Markt mit fallenden Preisen
    ist die Grundsteuer reine Kosten ohne Gegenwert. Der Brandenburger Fall
    zahlt {de([t for t in tab if t[1]==2022][0][3])} EUR Grundsteuer auf einen Verlust von
    {de(abs([t for t in tab if t[1]==2022][0][2]))} EUR. Das fängt die Verlustverrechnung aber auf,
    nicht der Abzug — und zwar besser, weil sie am Verlust selbst ansetzt.''')
