# -*- coding: utf-8 -*-
"""
R1c — Stundung als allgemeine Option für Betriebe und Immobilien

ANLASS
  Wenn der Entwurf keine Ausnahmen will, Übergänge aber ermöglichen soll, tritt
  die Stundung an die Stelle der Verschonung. Die Frage ist dann nicht mehr OB,
  sondern ZU WELCHEN BEDINGUNGEN — und daran entscheidet sich, ob die Stundung
  eine Zahlungserleichterung ist oder eine Verschonung unter anderem Namen.

DIE ENTSCHEIDENDE GRÖSSE IST DER ZINS
  Eine zinslose Stundung ist ein Erlass in Höhe des Zinsvorteils. Dieses Skript
  beziffert ihn.

QUELLE
  Statistisches Bundesamt, Erbschaft- und Schenkungsteuerstatistik 2024,
  Statistischer Bericht 73611, Tabelle 73611-07.
"""
import pandas as pd, numpy as np

XLS = '/home/claude/erbschaft/erbst.xlsx'
MRD = 1e6

def lies(blatt, um):
    d = pd.read_excel(XLS, sheet_name=blatt)
    d.columns = [str(c).strip() for c in d.columns]
    d = d.rename(columns=um)
    for c in d.columns:
        if pd.api.types.is_string_dtype(d[c]) or d[c].dtype == object:
            d[c] = d[c].astype('string').str.strip()
    d['n'] = pd.to_numeric(d['Wert'], errors='coerce')
    return d

def de(v, nk=1):
    return '.' if pd.isna(v) else format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')

k = lies('csv-73611-07', {'Gegenstand_der_Nachweisung': 'pos',
                          'Steuerpflichtige_Erwerbe': 'art', 'Masseinheit': 'e',
                          'Steuerpflichtiger_Erwerb_groesser_Null_groesser_gleich_Null': 'abgr'})
k = k[k.abgr == 'Steuerpflichtiger Erwerb größer/gleich Null']
hol = lambda p: k[(k.pos == p) & (k.art == 'Erwerbe insgesamt') & (k.e == '1 000 EUR')].n.iloc[0]

GEGENST = hol('Anteiliger Wert der Nachlassgegenstände / Steuerwert des übertragenen Vermögens')
GRUND   = hol('Grundvermögen')
BETRIEB = hol('Betriebsvermögen (Wert > 0)')
LANDW   = hol('Land- und forstwirtschaftliches Vermögen')
UEBRIG  = hol('Übriges Vermögen')
BANK    = hol('Bankguthaben')
WERTP   = hol('Wertpapiere, Anteile, Genussscheine usw.')
STEU    = hol('Tatsächlich festgesetzte Steuer')

AUFK_POS03 = 16.54 * MRD      # aus R1, Entwurfsfassung mit 400.000 EUR Freibetrag

print('=' * 96)
print('R1c — STUNDUNG STATT VERSCHONUNG: WAS DAS KOSTET')
print('=' * 96)

# ----------------------------------------------- [1] Wie viel ist überhaupt illiquide
ILLIQ = GRUND + BETRIEB + LANDW
LIQUID = BANK + WERTP
print(f'\n[1] WIE VIEL DES GEERBTEN VERMÖGENS IST NICHT ZU GELD ZU MACHEN?')
print(f'    Nachlassgegenstände insgesamt            {de(GEGENST/MRD,1):>8} Mrd EUR')
print(f'      Grundvermögen                          {de(GRUND/MRD,1):>8}  ({de(GRUND/GEGENST*100,0)} %)')
print(f'      Betriebsvermögen                       {de(BETRIEB/MRD,1):>8}  ({de(BETRIEB/GEGENST*100,0)} %)')
print(f'      Land- und Forstwirtschaft              {de(LANDW/MRD,1):>8}  ({de(LANDW/GEGENST*100,0)} %)')
print(f'    = stundungsfähig im Sinne des Vorschlags {de(ILLIQ/MRD,1):>8} Mrd  '
      f'({de(ILLIQ/GEGENST*100,0)} %)')
print(f'      Bankguthaben                           {de(BANK/MRD,1):>8}')
print(f'      Wertpapiere und Anteile                {de(WERTP/MRD,1):>8}')
print(f'    = sofort zahlungsfähig                   {de(LIQUID/MRD,1):>8} Mrd  '
      f'({de(LIQUID/GEGENST*100,0)} %)')
ANTEIL = ILLIQ / GEGENST
print(f'\n    Fiele die Steuer anteilig auf die Vermögensarten, wären von den')
print(f'    {de(AUFK_POS03/MRD,1)} Mrd EUR aus Position 03 rund {de(AUFK_POS03*ANTEIL/MRD,1)} Mrd stundungsfähig.')
print(f'    Das ist eine Obergrenze: nicht jeder Erbe mit Grundbesitz braucht Stundung,')
print(f'    und wer daneben Bankguthaben erbt, kann daraus zahlen.')

# ----------------------------------------------- [2] Der Zins entscheidet alles
print(f'\n[2] WAS EINE ZINSLOSE STUNDUNG WERT IST — BARWERT JE 100 EUR STEUER')
print(f'    Abzinsung mit dem Satz, zu dem sich der Staat refinanziert.')
print(f'{"Laufzeit":>10}{"Abzinsung":>12}{"Einmalzahlung":>16}{"gleiche Raten":>16}{"Erlassanteil":>15}')
zeilen = []
for r in [0.02, 0.03, 0.04]:
    print(f'    --- Refinanzierungssatz {de(r*100,0)} % ---')
    for n in [5, 10, 20, 30]:
        bullet = 100 / (1 + r) ** n
        af = sum(1 / (1 + r) ** t for t in range(1, n + 1))     # Rentenbarwertfaktor
        raten = 100 / n * af
        zeilen.append(dict(zins=r, jahre=n, barwert_einmal=bullet, barwert_raten=raten))
        print(f'{n:>10} J{de(r*100,0)+" %":>12}{de(bullet,1):>16}{de(raten,1):>16}'
              f'{de(100-raten,1)+" %":>15}')
z = pd.DataFrame(zeilen)
b10 = z[(z.zins == 0.03) & (z.jahre == 10)].iloc[0]
b20 = z[(z.zins == 0.03) & (z.jahre == 20)].iloc[0]
print(f'\n    Gelesen: eine zinslose Stundung über 20 Jahre in gleichen Raten bei 3 %')
print(f'    Refinanzierung ist ein Erlass von {de(100-b20.barwert_raten,0)} % der Steuer.')
print(f'    Über 10 Jahre sind es {de(100-b10.barwert_raten,0)} %.')
stund = AUFK_POS03 * ANTEIL
print(f'    Auf {de(stund/MRD,1)} Mrd EUR gestundete Steuer bezogen: '
      f'{de(stund*(100-b10.barwert_raten)/100/MRD,1)} Mrd (10 J) bis '
      f'{de(stund*(100-b20.barwert_raten)/100/MRD,1)} Mrd (20 J) im Jahr.')
print(f'    Zum Vergleich: die Betriebsvermögensverschonung kostet heute 3,9 bis 5,1 Mrd.')
print(f'    Eine zinslose Stundung über 20 Jahre wäre also keine Abschaffung der')
print(f'    Verschonung, sondern ihre Umbenennung.')

# ----------------------------------------------- [3] Übergang
print(f'\n[3] DER ÜBERGANG — EINMALIGE LÜCKE, KEIN DAUERVERLUST')
print(f'    Wird die Steuer verzinst gestundet, ist das Aufkommen im eingeschwungenen')
print(f'    Zustand unverändert: was neu gestundet wird, fliesst aus Altfällen zurück.')
print(f'    Bis dahin fehlt Geld.')
print(f'{"Ratenlaufzeit":>14}{"Lücke kumuliert":>18}{"im Schnitt je Jahr":>21}{"voll ab Jahr":>14}')
for n in [5, 7, 10, 15, 20]:
    luecke = stund * (n - 1) / 2
    print(f'{n:>12} J{de(luecke/MRD,1)+" Mrd":>18}{de(luecke/n/MRD,1)+" Mrd":>21}{n:>14}')
print(f'\n    Das ist der Punkt, an dem die Stundung den Entwurf wirklich berührt:')
print(f'    28:28 soll vom ersten Jahr an ausgeglichen sein. Eine Lücke von mehreren')
print(f'    Milliarden über ein Jahrzehnt muss im Haushalt stehen, nicht in einer Fussnote.')

# ----------------------------------------------- [4] Zwei Bauarten
print(f'\n[4] ZWEI BAUARTEN, DIE SICH GRUNDSÄTZLICH UNTERSCHEIDEN')
print(f'''
    A  EINKOMMENSABHÄNGIG (das BAföG-Muster)
       Gezahlt wird, was die Erbin aus laufendem Einkommen tragen kann.
       + trifft die Zahlungsfähigkeit genau
       + bekanntes, akzeptiertes Verfahren
       - Erbschaftsteuer knüpft an Vermögen an, BAföG an Erwerbsfähigkeit.
         Wer 2 Mio EUR Grundbesitz erbt und wenig verdient, zahlte wenig —
         obwohl das Vermögen beleihbar oder verkäuflich ist. Das ist keine
         Härtefallregel mehr, sondern eine Lücke.
       - Erlass nach Frist, wie beim BAföG, wäre ein verdeckter Freibetrag
         für genau die Gruppe mit dem grössten Vermögen.

    B  OBJEKTGEBUNDEN (Sicherung am geerbten Gegenstand)
       Die Steuer wird als Last auf dem Objekt eingetragen, verzinst, und
       fällig bei Verkauf, Weitergabe oder nach einer Höchstfrist.
       + kein Verkaufszwang, keine Lücke, kein Erlass
       + die Steuer folgt dem Vermögen, nicht dem Einkommen — passend zur
         Erbschaftsteuer
       + Vorbild: aufgeschobene Grundsteuer für Ältere in mehreren Ländern
       - Eintragung und Verwaltung kosten Aufwand
       - bei Betrieben ist die Sicherung schwieriger als bei Grundstücken

    EINE KOMBINATION LÄGE NAHE
       Laufende Raten nach Leistungsfähigkeit — Ihr Gedanke —, der jeweils
       offene Rest als verzinste Last auf dem Objekt, fällig spätestens bei
       Verkauf oder im nächsten Erbfall. Dann trifft die Zahlung die
       Möglichkeiten der Begünstigten, ohne dass am Ende etwas erlassen wird.
       Die Stundung bliebe eine Stundung.''')

pd.DataFrame(zeilen).to_csv('/home/claude/erbschaft/r1c-stundung-barwerte.csv', index=False)
print('\n-> r1c-stundung-barwerte.csv')
