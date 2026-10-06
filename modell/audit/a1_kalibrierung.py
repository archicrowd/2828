# -*- coding: utf-8 -*-
"""
A1 — Stimmt der Ausgangspunkt? Modell gegen amtliche Zahlen

WARUM DAS BISHER NIE GEPRÜFT WURDE
  Alle Prüfungen R1 bis R16 haben EINZELNE Positionen gegen Primärdaten
  gerechnet. Nie geprüft wurde, ob der GESAMTRAHMEN des Modells — das BIP,
  die Kalibrierung der Einkommensteuer, die Summe aller Einnahmen — zur
  amtlichen Wirklichkeit passt. Das ist die Grundlage für alles andere.

AMTLICHE ZAHLEN (Recherche 3.10.2026)
  Steuereinnahmen insgesamt 2025: 989,8 Mrd EUR (Destatis)
  Steueraufkommen ohne reine Gemeindesteuern 2025: 901,9 Mrd (BMF-Monatsbericht)
  BIP nominal: 2023 4.219,3 · 2024 4.329,0 · 2025 4.469,9 Mrd
    (Statistische Ämter des Bundes und der Länder, VGRdL, Stand Februar 2026)
  Steuerschätzung Oktober 2025 für 2028: 1.079,8 Mrd
  Sozialversicherungsbeiträge 2024: rund 707,7 Mrd (Summe der Einzelzweige
    aus BAS, BMG und BA — keine amtliche Aggregatzahl)
"""
def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=1): return ('+' if v >= 0 else '') + de(v, nk)

BIP = {2023: 4219.3, 2024: 4329.0, 2025: 4469.9}
STEUER_2025, STEUER_2028_SCHAETZ = 989.8, 1079.8
AMTLICH = {   # Mrd EUR, 2025, BMF-Monatsbericht Dezember 2025 / Destatis
 'Lohnsteuer': 262.7, 'veranlagte Einkommensteuer': 78.4,
 'nicht veranlagte Steuern vom Ertrag': 31.1, 'Abgeltungsteuer': 24.8,
 'Körperschaftsteuer': 39.2, 'Steuern vom Umsatz': 310.2,
 'Gewerbesteuer (2024)': 75.3, 'Grundsteuer A+B (2024)': 16.0,
 'Grunderwerbsteuer': 15.1, 'Erbschaft/Schenkung': 15.4,
 'Energiesteuer': 37.6, 'Tabaksteuer': 17.6, 'Versicherungsteuer': 19.6,
 'Stromsteuer': 5.9, 'Kraftfahrzeugsteuer': 9.6, 'Luftverkehrsteuer': 2.1,
 'Solidaritätszuschlag': 12.9, 'Alkoholsteuer': 2.1,
 'Rennwett-/Lotteriesteuer': 2.5, 'Biersteuer': 0.5, 'Zölle': 5.9,
 'Gewerbesteuerumlagen': 6.6, 'übrige Bundes-/Ländersteuern': 2.4,
}
print('=' * 94)
print('A1 — STIMMT DER AUSGANGSPUNKT DES MODELLS?')
print('=' * 94)

print(f'''
[1] DAS BIP — HIER LIEGT DER ERSTE FEHLER
    Das Modell setzt BIP0 = 4.200 Mrd für das Startjahr 2028.
    Amtlich 2025: {de(BIP[2025])} Mrd. Nominales Wachstum 2025: +3,3 %.''')
for g in (0.025, 0.030, 0.035):
    b28 = BIP[2025] * (1 + g) ** 3
    print(f'      bei {de(g*100,1)} % nominal bis 2028: {de(b28)} Mrd  '
          f'-> Modell ist {de((4200/b28-1)*100,1)} % zu niedrig')
b28 = BIP[2025] * 1.03 ** 3
print(f'''
    FOLGE: das Investitionsziel von 1 % des BIP sind nicht 42, sondern
    {de(b28*0.01)} Mrd EUR. Der Puffer von 2 % sind {de(b28*0.02)} statt 84 Mrd.
    Der gesamte Haushaltsabgleich lief gegen ein zu kleines Ziel.''')

print(f'''
[2] DIE EINKOMMENSTEUER-KALIBRIERUNG — DER ZWEITE FEHLER
    Das Modell kalibriert K_EST so, dass der Tarif 2025 plus Dividende
    von 6.000 EUR genau 284 Mrd ergibt.
    Amtlich 2025: Lohnsteuer {de(AMTLICH["Lohnsteuer"])} + veranlagte Einkommensteuer '''
      f'''{de(AMTLICH["veranlagte Einkommensteuer"])}
    = {de(AMTLICH["Lohnsteuer"]+AMTLICH["veranlagte Einkommensteuer"])} Mrd. Ohne Soli, ohne Kapitalertragsteuern.
    Das Modell liegt damit {de((284/(AMTLICH["Lohnsteuer"]+AMTLICH["veranlagte Einkommensteuer"])-1)*100,1)} % zu niedrig.''')

print(f'''
[3] DER BEFUND, DER BEIDE ERKLÄRT
    BIP zu niedrig um {de((1-4200/b28)*100,1)} %, Einkommensteuer zu niedrig um '''
      f'''{de((1-284/341.1)*100,1)} %.
    Beide Abweichungen gehen in dieselbe Richtung und sind etwa gleich gross.
    Das Modell ist also nicht falsch gerechnet, sondern auf ein FRÜHERES
    NIVEAU kalibriert — grob 2021/2022 — und als Startjahr 2028 etikettiert.
    Intern konsistent, aber die Euro-Beträge sind keine 2028er Werte.

    WO ES WIRKLICH WEHTUT: die Ausgabenseite ist NICHT mitskaliert. Die
    Digitaldividende von 515 EUR ist 50 % des Existenzminimums 2026, also
    ein aktueller Wert. Einnahmen auf 2021er Niveau, Ausgaben auf 2026er
    Niveau — der Saldo ist dadurch systematisch zu schlecht.''')
ERW, KIND, DD = 70, 14, 515.0
dd_kosten = (ERW * DD * 12 + KIND * DD * 0.5 * 12) / 1000
print(f'''
    Grössenordnung: die Dividende kostet {de(dd_kosten)} Mrd. Würde man die
    Einnahmen auf dasselbe Niveau heben wie die Ausgaben — also um die
    {de((341.1/284-1)*100,1)} % der Einkommensteuer-Abweichung —, wären es bei
    1.159 Mrd Einnahmen rund {de(1159*(341.1/284-1))} Mrd mehr.
    Mein Saldo von −12,9 Mrd ist damit zu pessimistisch, und zwar deutlich.''')

print(f'''
[4] DIE BLACKBOX "SONSTIGE STEUERN 165" — AUFGELÖST
    Was bleibt amtlich übrig, wenn die benannten Positionen abgezogen sind?''')
benannt = ('Lohnsteuer', 'veranlagte Einkommensteuer', 'nicht veranlagte Steuern vom Ertrag',
           'Abgeltungsteuer', 'Körperschaftsteuer', 'Steuern vom Umsatz',
           'Gewerbesteuer (2024)', 'Grundsteuer A+B (2024)', 'Erbschaft/Schenkung')
rest = {k: v for k, v in AMTLICH.items() if k not in benannt}
print()
for k, v in sorted(rest.items(), key=lambda x: -x[1]):
    print(f'      {k:<38}{de(v):>7}')
print(f'      {"-"*45}')
print(f'      {"zusammen":<38}{de(sum(rest.values())):>7}')
print(f'''
    Amtlich bleiben {de(sum(rest.values()))} Mrd. Das Modell bucht 165 — also
    {de(165-sum(rest.values()))} Mrd zu viel. Dafür gibt es zwei mögliche Erklärungen,
    und beide sind Probleme:
      a) die Grundsteuer von {de(AMTLICH["Grundsteuer A+B (2024)"])} Mrd steckt darin. Dann ist Position 04a
         doppelt gezählt, denn sie ist aufkommensneutral zur Grundsteuer.
      b) es ist dieselbe Niveau-Abweichung wie oben, nur mit umgekehrtem
         Vorzeichen. Dann ist der Posten einfach nicht hergeleitet.
    In beiden Fällen gilt: 165 Mrd ist der grösste unbelegte Einzelposten
    des Modells, grösser als Erbschaft, Vermögen und CO2 zusammen.''')
