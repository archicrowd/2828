# -*- coding: utf-8 -*-
"""
R10 — Die mittleren Tarifstufen: wie hoch müssen sie, und wen trifft das?

AUFGABE
  Der Haushaltsabgleich lässt eine Lücke von 54,9 Mrd EUR zum Investitions-
  ziel von 1 % der Wirtschaftsleistung. Geschlossen werden soll sie über die
  mittleren Stufen von Einkommen- und Mehrwertsteuer. Oben bleibt 28 %,
  unten bleibt 0 % — der eine Satz ist die Identität des Konzepts.

NEBENBEDINGUNG, DIE DEN AUSSCHLAG GIBT
  Nicht jede Kombination, die rechnerisch passt, ist vertretbar. Gesucht wird
  die Kombination, deren ZUSATZLAST mit dem Einkommen steigt — die also die
  Progression nicht umkehrt. Eine Anhebung der zweiten Stufe (ab 12.348 EUR)
  trifft die niedrigsten steuerpflichtigen Einkommen; eine Anhebung der
  Mehrwertsteuer trifft sie über die Konsumquote noch stärker. Beides wird
  unten gerechnet, nicht behauptet.

GRENZEN DIESER RECHNUNG
  Die Einkommensverteilung VERT des Modells hat sieben Gruppen — das ist grob
  und sagt nichts über die Streuung innerhalb einer Gruppe. Die Konsumquoten
  sind eine Setzung nach dem Muster der Einkommens- und Verbrauchsstichprobe
  und stehen unten offen. Das Ergebnis ist eine Grössenordnung der Verteilungs-
  wirkung, kein Mikrosimulationsergebnis.
"""
import itertools

def de(v, nk=1):
    return format(v, f',.{nk}f').replace(',', 'X').replace('.', ',').replace('X', '.')
def pm(v, nk=1):
    return ('+' if v >= 0 else '') + de(v, nk)

VERT = [(6,8000),(11,20000),(12,36000),(7,52000),(5,69000),(3,105000),(1,300000)]
S25, G25 = [0,.08,.14,.19,.23,.25], [12000,25000,40000,55000,70000,float('inf')]
GRENZEN = [12348, 25000, 40000, 55000, 70000, float('inf')]
EST_IST, MWST_IST = [0,.09,.16,.21,.26,.28], [5,11,17,22,28]
DD_M, ETI, LEAK = 515.0, 0.35, 0.80
DD = DD_M * 12
MWST_GEW = [.10,.10,.20,.30,.30]
BRUTTO = 350/(0.18/1.18)
ZIEL, SALDO0 = 42.0, -12.9

# Konsumquote: Anteil des verfügbaren Einkommens, der verbraucht wird.
# Setzung nach dem Muster der EVS — unten hoch, oben fallend. Bestreitbar.
KONSUM = [1.00, 0.95, 0.88, 0.82, 0.76, 0.68, 0.50]

def est(x, s, g=GRENZEN):
    tot, pr = 0.0, 0.0
    for i, gg in enumerate(g):
        if x > pr: tot += (min(x, gg) - pr) * s[i]
        pr = gg
        if x <= gg: break
    return tot
def grenz(b, s, g):
    for gg, x in zip(g, s):
        if b <= gg: return x
    return s[-1]
K_EST = 284 / sum(m*est(b+6000, S25, G25)/1000 for m, b in VERT)

def est_aufkommen(s):
    tot = 0.0
    for m, b in VERT:
        b1 = b*((1-grenz(b+DD, s, GRENZEN))/(1-grenz(b+DD, S25, G25)))**ETI
        tot += m*est(b1+DD, s)/1000
    return K_EST*tot
def r_eff(st): return sum(a*g for a, g in zip(st, MWST_GEW))/100
def mwst_aufkommen(st):
    r = r_eff(st)
    return 350 + (BRUTTO*r/(1+r) - 350)*LEAK

EST0, MWST0 = est_aufkommen(EST_IST), mwst_aufkommen(MWST_IST)

def mehrlast(s, st):
    """Zusatzlast je Verteilungsgruppe in Prozent des Bruttoeinkommens inkl. DD."""
    dr = r_eff(st) - r_eff(MWST_IST)
    out = []
    for (m, b), kq in zip(VERT, KONSUM):
        ein = b + DD
        d_est = est(ein, s) - est(ein, EST_IST)
        d_mwst = ein * kq * dr / (1 + r_eff(MWST_IST))
        out.append(((d_est + d_mwst)/ein*100, d_est, d_mwst, ein))
    return out

print('=' * 100)
print('R10 — DIE MITTLEREN TARIFSTUFEN')
print('=' * 100)
print(f'\n    Gegenprobe: Einkommensteuer {de(EST0,1)} (Modell 313,3) · '
      f'Mehrwertsteuer {de(MWST0,1)} (Modell 375,9) Mrd EUR.')
print(f'    Ausgangssaldo nach Korrektur {pm(SALDO0,1)}, Ziel {pm(ZIEL,0)}, '
      f'Lücke {de(ZIEL-SALDO0,1)} Mrd EUR.')

# ---------------------------------------------------------------- Rastersuche
kand = []
for de2, de3, de4, de5 in itertools.product(range(4), repeat=4):
    s = [0, .09+de2/100, .16+de3/100, .21+de4/100, .26+de5/100, .28]
    if not all(s[i] <= s[i+1] for i in range(5)): continue
    for dm2, dm3, dm4 in itertools.product(range(5), repeat=3):
        st = [5, 11+dm2, 17+dm3, 22+dm4, 28]
        if not all(st[i] <= st[i+1] for i in range(4)): continue
        plus = (est_aufkommen(s)-EST0) + (mwst_aufkommen(st)-MWST0)
        if plus < ZIEL - SALDO0: continue
        ml = [x[0] for x in mehrlast(s, st)]
        progressiv = all(ml[i] <= ml[i+1] + 1e-9 for i in range(len(ml)-1))
        # Kosten: Anhebung tiefer Stufen wiegt schwerer
        kosten = de2*4 + de3*3 + de4*2 + de5*1 + dm2*4 + dm3*3 + dm4*2
        kand.append((progressiv, kosten, plus, s, st, ml))

prog = sorted([k for k in kand if k[0]], key=lambda k: (k[1], k[2]))
alle = sorted(kand, key=lambda k: (k[1], k[2]))
print(f'\n[1] RASTERSUCHE')
print(f'    {len(kand)} Kombinationen erreichen das Ziel. Davon tragen {len(prog)} die')
print(f'    Zusatzlast progressiv, also mit dem Einkommen steigend.')

print(f'\n[2] DIE SPARSAMSTEN KOMBINATIONEN MIT PROGRESSIVER ZUSATZLAST')
print(f'{"ESt-Stufen":>24}{"MwSt":>18}{"Mehrertrag":>13}{"Saldo":>9}'
      f'{"Last unten":>12}{"Last oben":>11}')
for p, k, plus, s, st, ml in prog[:8]:
    print(f'{"/".join(str(round(x*100)) for x in s):>24}'
          f'{"/".join(map(str, st)):>18}{pm(plus,1):>13}{pm(SALDO0+plus,1):>9}'
          f'{de(ml[0],2)+" %":>12}{de(ml[-1],2)+" %":>11}')

print(f'\n[3] ZUM VERGLEICH: SPARSAMSTE OHNE DIE PROGRESSIONSBEDINGUNG')
print(f'{"ESt-Stufen":>24}{"MwSt":>18}{"Mehrertrag":>13}{"Saldo":>9}'
      f'{"Last unten":>12}{"Last oben":>11}')
for p, k, plus, s, st, ml in alle[:4]:
    mark = '' if p else '  <- kehrt die Progression um'
    print(f'{"/".join(str(round(x*100)) for x in s):>24}'
          f'{"/".join(map(str, st)):>18}{pm(plus,1):>13}{pm(SALDO0+plus,1):>9}'
          f'{de(ml[0],2)+" %":>12}{de(ml[-1],2)+" %":>11}{mark}')

print('''
[4] WARUM NULL — UND WARUM DAS KEIN SUCHFEHLER IST

    Die oberste Gruppe liegt mit 300.000 EUR weit über der letzten Stufen-
    grenze von 70.000 EUR. Sie zahlt den Spitzensatz, und der bleibt bei
    28 %. Eine Anhebung der Stufen DARUNTER trifft sie nur mit einem festen
    Betrag: die zweite Stufe um 3 Punkte anzuheben kostet jeden oberhalb von
    25.000 EUR dieselben 12.652 x 3 % = 380 EUR. Für ein Einkommen von
    26.180 EUR sind das 1,45 %, für 306.180 EUR sind es 0,12 %.

    Das ist keine Eigenheit dieses Rasters, sondern eine Eigenschaft des
    Entwurfs: WENN DER SPITZENSATZ FESTSTEHT, KANN ZUSÄTZLICHES AUFKOMMEN
    AUS DER EINKOMMENSTEUER NUR AUS DER MITTE KOMMEN — und das ist relativ
    zur Spitze zwangsläufig regressiv. Die Mehrwertsteuer verstärkt es über
    die fallende Konsumquote.

    Die Anweisung, die mittleren Stufen anzuheben, ist also ausführbar, aber
    nicht ohne diesen Preis. Er wird hier beziffert, nicht weggelassen.''')

# ------------------------------------------- schwächeres Kriterium und Netto
schwach = [k for k in kand if k[5][0] <= k[5][-1] + 1e-9]
print(f'\n[5] SCHWÄCHERES KRITERIUM: UNTEN NICHT MEHR ALS OBEN')
print(f'    Auch das erfüllen {len(schwach)} von {len(kand)} Kombinationen.')

print('''
[6] DIE NETTOPOSITION — WAS DIE REFORM ALS GANZES TUT

    Die Zusatzlast allein ist das falsche Mass. Gegen sie steht die
    Digitaldividende, ein fester Betrag für alle. Entscheidend ist, was
    unter dem Strich bleibt. Gerechnet gegen den Tarif 2025.''')
best = alle[0]
_, _, plus_b, s_b, st_b, ml_b = best
print(f'\n    Zugrunde gelegt: ESt {"/".join(str(round(x*100)) for x in s_b)} · '
      f'MwSt {"/".join(map(str, st_b))} · DD {de(DD_M,0)} EUR im Monat')
print(f'\n{"Markteinkommen":>16}{"DD":>10}{"ESt 2025":>11}{"ESt 28:28":>11}'
      f'{"MwSt mehr":>11}{"netto":>11}{"in % Markt":>12}')
for (m, b), kq, (ml, d_est, d_mw, ein) in zip(VERT, KONSUM, mehrlast(s_b, st_b)):
    e25 = est(b, S25, G25)
    e28 = est(ein, s_b)
    netto = DD - (e28 - e25) - d_mw
    print(f'{de(b,0):>16}{de(DD,0):>10}{de(e25,0):>11}{de(e28,0):>11}'
          f'{de(d_mw,0):>11}{pm(netto,0):>11}{pm(netto/b*100,1)+" %":>12}')
print(f'''
    Die Nettoposition ist stark progressiv: unten ein Vielfaches des
    Markteinkommens, oben ein Minus. Dass der FINANZIERUNGSZUSCHLAG
    regressiv wirkt, ändert daran nichts — es heisst nur, dass er die
    Progression der Reform abschwächt und nicht verstärkt.

[7] DIE ALTERNATIVE, DIE DIE MITTE NICHT BERÜHRT

    Von der Lücke von {de(ZIEL-SALDO0,1)} Mrd EUR gehen 20 Mrd auf eine einzige
    Korrektur zurück: die Bodenwertabgabe. Das Modell hatte "Bodenwertabgabe
    statt Grundsteuer" mit +20 Mrd gebucht, Position 04 beschreibt aber einen
    Umbau bei gleichem Aufkommen — dann sind es null. R5b zeigt, woher die
    20 Mrd kommen könnten: der Bodenwert lag 2014 bei 3.529 Mrd EUR, und ein
    Satz von 0,22 bis 0,44 % trägt die heutigen 15,5 Mrd Grundsteuer. Ein
    Satz von 1 % ergäbe rund 35 Mrd, also +20 gegenüber heute.

    Das ist keine Spitzfindigkeit, sondern eine Weggabelung:
      a) Position 04 bleibt aufkommensneutral. Dann fehlen 20 Mrd, und sie
         müssen aus der Mitte kommen — mit der oben gezeigten Wirkung.
      b) Position 04 wird als Bodenwertabgabe ÜBER dem heutigen Niveau
         formuliert. Dann schrumpft die Lücke auf {de(ZIEL-SALDO0-20,1)} Mrd, und die
         Stufen müssen deutlich weniger steigen. Der Träger ist der Boden,
         der nicht ausweichen kann, und nach R5b liegen 87 % des Bodenwerts
         auf 17 % der Fläche — die Last wäre konzentriert, nicht breit.

    Weg b) ist die sachlich bessere Antwort auf die Lücke. Er verlangt aber
    eine Änderung an Position 04 und damit eine MAJOR-Version.''')

# Variante b) durchrechnen
print(f'\n[8] WEG b) GERECHNET: LÜCKE {de(ZIEL-SALDO0-20,1)} MRD STATT {de(ZIEL-SALDO0,1)}')
kand_b = []
for d2, d3, d4, d5 in itertools.product(range(4), repeat=4):
    s = [0, .09+d2/100, .16+d3/100, .21+d4/100, .26+d5/100, .28]
    if not all(s[i] <= s[i+1] for i in range(5)): continue
    for m2, m3, m4 in itertools.product(range(5), repeat=3):
        st = [5, 11+m2, 17+m3, 22+m4, 28]
        if not all(st[i] <= st[i+1] for i in range(4)): continue
        plus = (est_aufkommen(s)-EST0) + (mwst_aufkommen(st)-MWST0)
        if plus < ZIEL - SALDO0 - 20: continue
        ml = [x[0] for x in mehrlast(s, st)]
        kand_b.append((d2*4+d3*3+d4*2+d5*1+m2*4+m3*3+m4*2, plus, s, st, ml))
kand_b.sort(key=lambda k: (k[0], k[1]))
print(f'{"ESt-Stufen":>24}{"MwSt":>18}{"Mehrertrag":>13}{"Saldo":>9}'
      f'{"Last unten":>12}{"Last oben":>11}')
for k, plus, s, st, ml in kand_b[:5]:
    print(f'{"/".join(str(round(x*100)) for x in s):>24}'
          f'{"/".join(map(str, st)):>18}{pm(plus,1):>13}{pm(SALDO0+20+plus,1):>9}'
          f'{de(ml[0],2)+" %":>12}{de(ml[-1],2)+" %":>11}')
print(f'''
    Die sparsamste Kombination hebt die Einkommensteuer um einen Punkt in
    einer Stufe und die Mehrwertsteuer in zwei Stufen — statt vier bzw. drei
    Anhebungen in Weg a). Die Zusatzlast unten halbiert sich.''')
