# -*- coding: utf-8 -*-
"""
R4 — Position 07, CO2-Preis: was das geltende Recht hergibt

QUELLE
  Drittes Gesetz zur Änderung des Brennstoffemissionshandelsgesetzes
  (Drittes BEHG-Änderungsgesetz), Gesetzentwurf 2026.
  Darin:
    § 10 Abs. 2 Satz 4 BEHG neu: "Für die Jahre 2026 und 2027 wird ein
      Preiskorridor mit einem Mindestpreis von 55 Euro pro Emissions-
      zertifikat und einem Höchstpreis von 65 Euro pro Emissionszertifikat
      festgelegt."
    § 44 Abs. 2 BEHG neu: jährliche Emissionsmengen 2021 bis 2030.
    § 10 Abs. 3 Satz 2 Nr. 4 neu: ab 2028 Verkauf zu einem marktbasierten
      Preis, der dem Durchschnitt der EU-ETS-1-Versteigerungen entspricht.

WAS DAS FÜR POSITION 07 BEDEUTET
  Position 07 nennt 100 steigend auf 150 EUR je Tonne. Das geltende Recht
  sieht für 2026 und 2027 einen Korridor von 55 bis 65 EUR vor, und ab
  2028 KEINEN national gesetzten Preis mehr, sondern den europäischen.
  Die Rechnung unten zeigt beides nebeneinander.

ABGRENZUNG
  Das BEHG erfasst fossile Brennstoffemissionen ausserhalb des
  europäischen Emissionshandels — im Kern Wärme und Verkehr. Strom und
  Industrie liegen im EU-ETS 1 und sind hier NICHT enthalten. Die
  Mengen sind die gesetzlich festgelegten Emissionsmengen, also die
  Obergrenze; tatsächlich verkauft wird, was an Emissionen anfällt.
"""
import numpy as np

def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')

# § 44 Abs. 2 BEHG in der Fassung des Dritten Änderungsgesetzes, Tonnen CO2
MENGE = {2021: 301_037_178, 2022: 291_116_621, 2023: 280_149_525,
         2024: 275_998_949, 2025: 260_092_203, 2026: 252_366_567,
         2027: 234_418_353, 2028: 216_470_033, 2029: 198_521_712,
         2030: 180_573_392}
MRD = 1e9

print('=' * 94)
print('R4 — CO2-BEPREISUNG: GELTENDES RECHT GEGEN POSITION 07')
print('=' * 94)

print('\n[1] DIE GESETZLICHE MENGE')
print(f'{"Jahr":>6}{"Emissionsmenge Mio t":>24}{"gegen Vorjahr":>16}{"gegen 2021":>13}')
j0 = min(MENGE)
for j in sorted(MENGE):
    vj = MENGE.get(j-1)
    dv = f'{de((MENGE[j]/vj-1)*100,1)} %' if vj else '–'
    print(f'{j:>6}{de(MENGE[j]/1e6,1):>24}{dv:>16}'
          f'{de((MENGE[j]/MENGE[j0]-1)*100,1)+" %":>13}')
print(f'\n    Die Menge sinkt von {de(MENGE[2021]/1e6,1)} auf {de(MENGE[2030]/1e6,1)} Mio Tonnen,')
print(f'    also um {de((1-MENGE[2030]/MENGE[2021])*100,1)} % in neun Jahren. Das ist der Zweck der Sache —')
print(f'    und zugleich der Grund, warum das Aufkommen nicht mit dem Preis mitwächst.')

print('\n[2] AUFKOMMEN: RECHTSPFAD GEGEN ENTWURF')
print('    Preiskorridor 55 bis 65 EUR gilt nach dem Gesetz für 2026 und 2027.')
print(f'{"Jahr":>6}{"Menge Mio t":>14}{"bei 55 EUR":>13}{"bei 65 EUR":>13}'
      f'{"bei 100 EUR":>14}{"bei 150 EUR":>14}')
for j in range(2026, 2031):
    m = MENGE[j]
    print(f'{j:>6}{de(m/1e6,1):>14}' + ''.join(
        f'{de(m*p/MRD,1)+" Mrd":>13}' if p < 100 else f'{de(m*p/MRD,1)+" Mrd":>14}'
        for p in (55, 65, 100, 150)))

print('\n[3] WAS POSITION 07 GEGENÜBER DEM RECHTSPFAD BRINGT')
print(f'{"Jahr":>6}{"Rechtspfad 55-65":>20}{"Position 07 bei 100":>22}{"Mehraufkommen":>18}')
for j in (2026, 2027):
    m = MENGE[j]
    print(f'{j:>6}{de(m*55/MRD,1)+" bis "+de(m*65/MRD,1)+" Mrd":>20}'
          f'{de(m*100/MRD,1)+" Mrd":>22}'
          f'{"+"+de((m*100-m*65)/MRD,1)+" bis +"+de((m*100-m*55)/MRD,1):>18}')
print(f'\n    Bei 150 EUR und der Menge von 2026: {de(MENGE[2026]*150/MRD,1)} Mrd EUR,')
print(f'    gegenüber dem Rechtspfad also +{de((MENGE[2026]*150-MENGE[2026]*65)/MRD,1)} '
      f'bis +{de((MENGE[2026]*150-MENGE[2026]*55)/MRD,1)} Mrd EUR.')

print('\n[4] DIE SCHERE: PREIS STEIGT, MENGE FÄLLT')
print('    Bei einem auf 150 EUR festgehaltenen Preis:')
print(f'{"Jahr":>6}{"Menge Mio t":>14}{"Aufkommen":>14}{"gegen 2026":>13}')
basis = MENGE[2026] * 150
for j in range(2026, 2031):
    a = MENGE[j] * 150
    print(f'{j:>6}{de(MENGE[j]/1e6,1):>14}{de(a/MRD,1)+" Mrd":>14}'
          f'{de((a/basis-1)*100,1)+" %":>13}')
print(f'\n    Das Aufkommen fällt binnen vier Jahren um '
      f'{de((1-MENGE[2030]/MENGE[2026])*100,1)} %, obwohl der Preis')
print(f'    unverändert bleibt. Wer die Dividende aus dem CO2-Preis speist,')
print(f'    finanziert sie aus einer schrumpfenden Quelle. Das ist kein Fehler')
print(f'    des Entwurfs, aber es gehört in die Haushaltsrechnung.')

print('''
[5] DER HARTE BEFUND: AB 2028 GIBT ES KEINEN NATIONALEN PREIS MEHR

    § 10 Absatz 3 Satz 2 Nummer 4 BEHG in der neuen Fassung sieht für die
    Jahre ab 2028 den Verkauf zu einem "marktbasierten Preis" vor, der dem
    mengengewichteten Durchschnittspreis der Versteigerungen im
    europäischen Emissionshandel entspricht. Der nationale Brennstoff-
    emissionshandel läuft in den europäischen ETS 2 nach Kapitel IVa der
    Emissionshandelsrichtlinie über; dessen Start wurde durch die
    Verordnung (EU) 2026/667 vom 11. März 2026 um ein Jahr verschoben.

    Daraus folgt: Ein nationaler CO2-Preis von 100 oder 150 EUR ab 2028
    ist mit dem geltenden Recht nicht vereinbar. Der Preis wird dann am
    europäischen Markt gebildet. Deutschland könnte einen höheren Preis
    nur als ZUSÄTZLICHE nationale Abgabe oben drauf setzen — das wäre
    etwas anderes als ein CO2-Preis, rechtlich wie politisch.

    Position 07 muss das benennen. Drei Wege stehen offen:
      a) Den Preispfad als europäische Forderung formulieren, nicht als
         nationale Setzung. Passt zur Klub-Logik der Seite.
      b) Eine nationale Zusatzabgabe vorsehen und sie so nennen.
      c) Den Preispfad auf das absenken, was national gilt — 55 bis 65 EUR
         bis 2027, danach Marktpreis.

[6] WAS DIESE RECHNUNG NICHT ABDECKT
    - Nur der nationale Brennstoffemissionshandel: Wärme und Verkehr.
      Strom und Industrie liegen im EU-ETS 1 und fehlen hier ganz.
    - Die gesetzliche Emissionsmenge ist eine Obergrenze. Verkauft wird,
      was an Emissionen anfällt; liegt die Nachfrage darunter, fällt das
      Aufkommen entsprechend geringer aus.
    - Eine Reserve von 40 Millionen Zertifikaten kann die Menge in einem
      Jahr erhöhen (§ 10 Absatz 3 Satz 2 Nummer 2 neu).
    - Der Abbau klimaschädlicher Subventionen, der zweite Teil von
      Position 07, ist hier nicht enthalten.''')
