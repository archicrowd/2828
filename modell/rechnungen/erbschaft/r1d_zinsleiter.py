# -*- coding: utf-8 -*-
"""
R1d — Die Zinsleiter der Stundung in Position 03

ENTWURFSENTSCHEIDUNG
  Die Verschonung entfällt, an ihre Stelle tritt eine Stundung für Betriebe
  UND Immobilien. Der Zins beginnt niedrig und steigt über zehn Jahre auf den
  marktüblichen Kreditzins.

DIE KONSTRUKTION
  Untergrenze: der Satz, zu dem sich der Staat selbst refinanziert. Dort
  verliert er nichts — die Stundung ist dann kein Zuschuss, sondern ein
  korrekt bepreister Kredit.
  Obergrenze: der marktübliche Zins für ein grundpfandrechtlich gesichertes
  Darlehen, also Refinanzierung plus Marge.
  Dazwischen linear über zehn Jahre.

      Zins im Jahr t  =  Basiszins + (t-1)/9 * Marge     für t = 1..10
                      =  Basiszins + Marge               ab t = 11

  Der Verzicht beschränkt sich damit auf die MARGE, und auch die nur
  anfangs. Das ist sachlich begründbar: die Forderung ist dinglich
  gesichert, das Ausfallrisiko des Staates also gering. Eine Bank verlangt
  die Marge für ein Risiko, das hier nicht besteht.

KEIN ERLASS
  Es gibt keine Verjährung und keinen Erlass nach Frist. Der offene Rest
  bleibt als Last auf dem Gegenstand und wird fällig bei Verkauf,
  Weitergabe oder im nächsten Erbfall.

QUELLE DER MENGENGERÜSTE
  Statistisches Bundesamt, Erbschaft- und Schenkungsteuerstatistik 2024,
  Statistischer Bericht 73611.
"""
import pandas as pd, numpy as np

MRD = 1e6
STUNDBAR = 10.0 * MRD      # Mrd EUR aus R1c: stundungsfähiger Teil von Position 03

def de(v, nk=1):
    return '.' if pd.isna(v) else format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')

def leiter(basis, marge, jahre_rampe=10):
    """Zinssatz je Jahr t (1-basiert)."""
    return lambda t: basis + min(max(t - 1, 0), jahre_rampe - 1) / (jahre_rampe - 1) * marge

print('=' * 94)
print('R1d — ZINSLEITER DER STUNDUNG')
print('=' * 94)

SZEN = [('vorsichtig', 0.025, 0.020), ('mittel', 0.030, 0.020), ('hoch', 0.035, 0.025)]

print('\n[1] DIE LEITER')
print(f'{"Jahr":>6}' + ''.join(f'{n[:10]:>14}' for n, _, _ in SZEN))
for t in list(range(1, 11)) + [11, 15]:
    print(f'{t:>6}' + ''.join(f'{de(leiter(b, m)(t)*100,2)+" %":>14}' for _, b, m in SZEN))
print('    Basiszins = Refinanzierung des Staates, Marge = Aufschlag einer Bank')
print('    für ein gesichertes Darlehen. Ab Jahr 10 gilt der volle Marktzins.')

# ------------------------------------------------- [2] Was der Staat verzichtet
print('\n[2] WAS DER STAAT VERZICHTET — je 100 EUR gestundeter Steuer')
print('    Verglichen mit: (a) sofortiger Zahlung, (b) Marktzins ab dem ersten Jahr.')
print(f'{"Szenario":>12}{"Tilgung":>10}{"Barwert gg. sofort":>21}{"Barwert gg. Marktzins":>23}')
zeilen = []
for name, basis, marge in SZEN:
    z = leiter(basis, marge)
    for N in [5, 10, 15, 20]:
        rest = 100.0
        bw_leiter = bw_markt = 0.0
        rest_m = 100.0
        for t in range(1, N + 1):
            tilg = 100.0 / N
            zins_l = rest * z(t)
            zins_m = rest_m * (basis + marge)
            bw_leiter += (tilg + zins_l) / (1 + basis) ** t
            bw_markt += (tilg + zins_m) / (1 + basis) ** t
            rest -= tilg
            rest_m -= tilg
        zeilen.append(dict(szenario=name, basis=basis, marge=marge, jahre=N,
                           bw_leiter=bw_leiter, bw_markt=bw_markt))
        print(f'{name:>12}{N:>8} J{de(bw_leiter,1):>21}{de(bw_markt,1):>23}')
z = pd.DataFrame(zeilen)
m10 = z[(z.szenario == 'mittel') & (z.jahre == 10)].iloc[0]
m20 = z[(z.szenario == 'mittel') & (z.jahre == 20)].iloc[0]
print(f'''
    Gelesen, mittleres Szenario (Basis 3,0 %, Marge 2,0 %):
      Über 10 Jahre bekommt der Staat {de(m10.bw_leiter,1)} statt 100 — er gewinnt sogar
      {de(m10.bw_leiter-100,1)}, weil der Zins ab der Mitte über seiner Refinanzierung liegt.
      Über 20 Jahre: {de(m20.bw_leiter,1)}.
      Der Verzicht gegenüber vollem Marktzins ab Jahr 1 beträgt
      {de(m10.bw_markt-m10.bw_leiter,1)} (10 J) bzw. {de(m20.bw_markt-m20.bw_leiter,1)} (20 J) je 100 EUR.''')
verz10 = (m10.bw_markt - m10.bw_leiter) / 100 * STUNDBAR
print(f'      Auf {de(STUNDBAR/MRD,1)} Mrd EUR stundungsfähiger Steuer: '
      f'{de(verz10/MRD,2)} Mrd EUR im Jahr —')
print(f'      gegen 3,9 bis 5,1 Mrd, die die heutige Verschonung kostet.')
print('''
    ENTSCHEIDEND: der Staat verliert gegenüber sofortiger Zahlung NICHTS.
    Die Stundung ist damit keine Verschonung unter anderem Namen, sondern
    das, was sie heisst. Der Unterschied zur zinslosen Variante aus R1c
    (dort 15 bis 26 % Erlass) ist die ganze Pointe dieser Entscheidung.''')

# ------------------------------------------------- [3] Was der Erbe zahlt
print('\n[3] WAS EINE ERBIN TATSÄCHLICH ZAHLT')
print('    Freibetrag 400.000 EUR, Satz 28 %, Tilgung in zehn gleichen Raten,')
print('    Zins auf den Restbetrag nach der Leiter (Basis 3,0 %, Marge 2,0 %).')
z30 = leiter(0.030, 0.020)
print(f'{"Erbe":>12}{"Steuer":>11}{"Jahr 1":>12}{"Jahr 5":>12}{"Jahr 10":>12}'
      f'{"gesamt":>12}{"je Monat Ø":>13}')
beispiele = []
for erbe in [500_000, 600_000, 800_000, 1_200_000, 2_000_000]:
    steuer = max(0, erbe - 400_000) * 0.28
    rest, summe, raten = steuer, 0.0, []
    for t in range(1, 11):
        tilg = steuer / 10
        zahl = tilg + rest * z30(t)
        raten.append(zahl)
        summe += zahl
        rest -= tilg
    beispiele.append(dict(erbe=erbe, steuer=steuer, j1=raten[0], j5=raten[4],
                          j10=raten[9], summe=summe, monat=summe / 120))
    print(f'{de(erbe/1000,0)+" Tsd":>12}{de(steuer/1000,1)+" T":>11}'
          f'{de(raten[0],0):>12}{de(raten[4],0):>12}{de(raten[9],0):>12}'
          f'{de(summe,0):>12}{de(summe/120,0):>13}')
print(f'\n    Die Zahlen sind Euro im Jahr, letzte Spalte Euro im Monat über zehn Jahre.')
print(f'    Ein geerbtes Haus von 500.000 EUR kostet rund '
      f'{de(beispiele[0]["monat"],0)} EUR im Monat — das ist')
print(f'    tragbar, ohne zu verkaufen, und es ist kein Geschenk.')

# ------------------------------------------------- [4] Übergangslücke neu
print('\n[4] DIE ÜBERGANGSLÜCKE BLEIBT — SIE IST NUR GESTRECKT, NICHT VERLOREN')
for N in [5, 10, 15]:
    luecke = STUNDBAR * (N - 1) / 2
    print(f'    Tilgung über {N:>2} Jahre: kumuliert {de(luecke/MRD,1)} Mrd EUR, '
          f'im Schnitt {de(luecke/N/MRD,1)} Mrd je Jahr, voll ab Jahr {N}.')
print('    Verzinst fliesst alles zurück. Im Haushalt der ersten Jahre fehlt es')
print('    trotzdem und gehört dort ausgewiesen.')

print('''
[5] WAS NOCH ZU PRÜFEN IST
    - § 234 AO setzt für Stundungszinsen einen festen Satz. Nach meinem
      Kenntnisstand 0,5 % je Monat, also 6 % im Jahr; das Bundesverfassungs-
      gericht hat 2021 für die Nachzahlungszinsen nach § 233a AO einen festen
      Satz von 6 % als realitätsfern verworfen, worauf der Gesetzgeber auf
      1,8 % im Jahr gesenkt hat. Eine an einen Referenzzins gebundene Leiter
      ist deshalb vermutlich robuster als jeder feste Satz — das ist aber zu
      prüfen, ich kann von hier aus keine Rechtsquelle aufrufen.
    - Welcher Referenzzins: Basiszinssatz nach § 247 BGB, EZB-Hauptrefinan-
      zierungssatz oder die Umlaufrendite des Bundes. Die Wahl verändert die
      Leiter um Zehntelpunkte, nicht die Konstruktion.
    - Sicherung bei Betriebsvermögen ist schwieriger als bei Grundstücken.
      Für Grundstücke genügt die Eintragung, für Betriebe braucht es eine
      eigene Regelung.''')

pd.DataFrame(zeilen).to_csv('/home/claude/erbschaft/r1d-zinsleiter.csv', index=False)
pd.DataFrame(beispiele).to_csv('/home/claude/erbschaft/r1d-beispiele.csv', index=False)
print('\n-> r1d-zinsleiter.csv, r1d-beispiele.csv')
