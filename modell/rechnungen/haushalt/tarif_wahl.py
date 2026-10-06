# -*- coding: utf-8 -*-
"""
R10b — Die Tarifentscheidung

ZIELGRÖSSE 36,1 Mrd EUR aus R9. Nicht der Jahressaldo von +42 Mrd, der nach
R8 nie die Regel des Modells war, sondern der Betrag, bei dem der 20-Jahres-
Pfad in allen drei Szenarien ohne Lückenjahr bleibt und im Robust-Szenario
99 % des Investitionsziels erreicht.

WARUM EIN GLEICHMÄSSIGER AUFSCHLAG UND NICHT DAS OPTIMUM
  Eine Rastersuche über alle Stufen findet Kombinationen, die das Ziel um
  Zehntel genauer treffen, aber schiefe Tarife erzeugen: Stufen, die fast
  zusammenfallen (25 % und 26 % nebeneinander), oder eine einzelne
  Mehrwertsteuerstufe, die um fünf Punkte springt. Für ein Modell, dessen
  Anspruch Erklärbarkeit ist, ist ein gleichmässiger Aufschlag auf die
  bewegten Stufen die bessere Wahl. Der Preis ist ein etwas höherer
  Mehrertrag als nötig; er geht in den Fonds.

FESTGEHALTEN WIRD
  0 % bis 12.348 EUR · Eingangsstufe 9 % · MwSt-Grundstufe 5 % ·
  MwSt-Stufe A 11 % · Spitzensatz 28 %
  Begründung für die Eingangsstufen: R10 hat gezeigt, dass jede Anhebung
  inframarginaler Stufen bei fixiertem Spitzensatz regressiv wirkt. Die
  Wirkung ist unvermeidbar, aber sie lässt sich nach unten begrenzen.
"""
import itertools, json
exec(open('tarif.py').read().split("print('=' * 100)")[0])
ZIEL_PLUS = 36.1

print('=' * 100)
print('R10b — DIE TARIFENTSCHEIDUNG: GLEICHMÄSSIGER AUFSCHLAG AUF DIE MITTLEREN STUFEN')
print('=' * 100)
print(f'\n[1] DAS RASTER. x auf ESt 16/21/26, y auf MwSt 17/22. Mehrertrag in Mrd EUR.')
print(f'    Fett wäre, was {de(ZIEL_PLUS,1)} erreicht.\n')
print(f'{"":>8}' + ''.join(f'{"MwSt +"+str(y):>12}' for y in range(5)))
tab = {}
for x in range(5):
    s = [0, .09, (16+x)/100, (21+x)/100, min(26+x, 27)/100, .28]
    row = f'{"ESt +"+str(x):>8}'
    for y in range(5):
        st = [5, 11, 17+y, min(22+y, 26), 28]
        plus = (est_aufkommen(s)-EST0) + (mwst_aufkommen(st)-MWST0)
        tab[(x, y)] = (plus, s, st)
        mark = '*' if plus >= ZIEL_PLUS else ' '
        row += f'{pm(plus,1)+mark:>12}'
    print(row)

tref = [(abs(v[0]-ZIEL_PLUS), x+y, k) for k, v in tab.items()
        for x, y in [k] if v[0] >= ZIEL_PLUS]
tref.sort(key=lambda t: (t[1], t[0]))
print(f'\n[2] DIE SPARSAMSTEN TREFFER')
print(f'{"Aufschlag":>14}{"ESt-Stufen":>24}{"MwSt-Stufen":>16}{"Mehrertrag":>12}'
      f'{"Last unten":>12}{"Höchstlast":>12}')
for _, summe, k in tref[:5]:
    plus, s, st = tab[k]
    ml = [m[0] for m in mehrlast(s, st)]
    print(f'{"ESt +"+str(k[0])+" MwSt +"+str(k[1]):>14}'
          f'{"/".join(str(round(v*100)) for v in s):>24}{"/".join(map(str, st)):>16}'
          f'{pm(plus,1):>12}{de(ml[0],2)+" %":>12}{de(max(ml),2)+" %":>12}')

# Gewählt wird die symmetrische Variante: jede bewegte Stufe steigt gleich
# stark. Begründung steht im Kopf des Skripts und in [3]. Die beiden Flanken
# stehen in [2] und sind durch Ändern dieser Zeile einsetzbar.
K = (3, 3)
PLUS, S, ST = tab[K]
ML = [m[0] for m in mehrlast(S, ST)]
print(f'''
[3] GEWÄHLT: ESt +{K[0]} · MwSt +{K[1]} — die symmetrische Variante

    Drei Kombinationen liefern praktisch dasselbe Aufkommen und unterscheiden
    sich nur darin, WO die Last liegt. Das ist eine Wertentscheidung:
      ESt +4 / MwSt +2  Last unten 0,83 %, aber ein Sprung von 9 auf 20 %
                        bei 25.000 EUR — 11 Punkte auf einen Schlag.
      ESt +3 / MwSt +3  Last unten 1,25 %, grösster Sprung 10 Punkte.
      ESt +2 / MwSt +4  glattester Tarif (Sprung 9 wie bisher), aber die
                        Last unten steigt auf 1,67 %, weil die Mehrwert-
                        steuer das regressive Instrument ist.
    Gesetzt wird die Mitte. Wer die Regressivität stärker gewichtet als die
    Tarifglättung, nimmt ESt +4 / MwSt +2.

      Einkommensteuer  bisher  {" / ".join(str(round(v*100))+" %" for v in EST_IST)}
                       neu     {" / ".join(str(round(v*100))+" %" for v in S)}
      Mehrwertsteuer   bisher  {" / ".join(str(v)+" %" for v in MWST_IST)}
                       neu     {" / ".join(str(v)+" %" for v in ST)}

      Mehrertrag {pm(PLUS,1)} Mrd EUR gegen einen Bedarf von {de(ZIEL_PLUS,1)}.
      Effektiver Mehrwertsteuersatz {de(r_eff(MWST_IST)*100,1)} % -> {de(r_eff(ST)*100,1)} %.''')
print(f'\n[4] VERTEILUNGSWIRKUNG, gegen den Tarif 2025')
print(f'{"Markteinkommen":>16}{"ESt heute":>11}{"ESt alt":>10}{"ESt neu":>10}'
      f'{"MwSt mehr":>11}{"Zusatzlast":>12}{"netto mit DD":>14}{"in % Markt":>12}')
for (mio, b), (ml, d_est, d_mw, ein) in zip(VERT, mehrlast(S, ST)):
    e25, e_neu = est(b, S25, G25), est(ein, S)
    n = DD - (e_neu - e25) - d_mw
    print(f'{de(b,0):>16}{de(e25,0):>11}{de(est(ein,EST_IST),0):>10}{de(e_neu,0):>10}'
          f'{de(d_mw,0):>11}{de(ml,2)+" %":>12}{pm(n,0):>14}{pm(n/b*100,1)+" %":>12}')
json.dump(dict(est=S, mwst=ST, plus=PLUS, ml=ML, auf=list(K)),
          open('tarif_neu.json', 'w'))
print(f'''
    Zusatzlast {de(min(ML),2)} % bis {de(max(ML),2)} % des Einkommens einschliesslich Dividende.
    Nicht progressiv — nach R10 bei fixiertem Spitzensatz unvermeidbar —,
    aber auf keine Gruppe gekippt. Netto bleibt die Reform klar progressiv:
    unten +{de(DD-(est(VERT[0][1]+DD,S)-est(VERT[0][1],S25,G25))-mehrlast(S,ST)[0][2],0)} EUR, ab rund 105.000 EUR Markteinkommen ein Minus.''')
