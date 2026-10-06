#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
28:28 — GESAMTMODELL (Mikro, Makro, Haushaltspfad, Homepage-Daten)
Digitaldividende (DD) = 50 % des steuerlichen Existenzminimums (2026: 12.348 EUR/Jahr -> 515 EUR/Monat),
Kinder-DD = Haelfte (257,50 EUR). Aufstieg per Regel auf 55 % und 60 %.
Einheitssatz 28 % (ESt-Spitze, Kapital, Unternehmen/Plattformen, Erbschaft, MwSt-Topstufe).

Rechtsstand "heute": 2026 (§ 32a EStG 2026, SV-Rechengroessen 2026, Soli-Freigrenze 2026, Kindergeld 259 EUR).
Makro: Kalibrierung Projektmodell (Basis 880 / BIP 4.200 Modell-Mrd.). DD-Betraege werden in Euro 2026
gegen diese niedrigere Modellbasis gerechnet -> konservativ (Kostenanteil eher ueberzeichnet).
"""
import math, json, csv

# =====================================================================
# 0  PARAMETER
# =====================================================================
EXMIN_2026 = 12348                          # steuerliches Existenzminimum = Grundfreibetrag 2026
DD_EUR = {50: 515.0, 55: 566.0, 60: 617.0}  # EUR/Monat, gerundet (50/55/60 % von 12.348/12)
KIND_ANTEIL = 0.5
L = 28
TARIF_GRENZEN = [EXMIN_2026, 25000, 40000, 55000, 70000, float('inf')]
TARIF_SAETZE  = [0.00, 0.09, 0.16, 0.21, 0.26, 0.28]          # 0-9-16-21-26-28
MWST_STUFEN   = [5, 11, 17, 22, 28]                            # Label A+ ... D
MWST_GEWICHTE = [.10, .10, .20, .30, .30]                      # ANNAHME Konsumanteile
SV_AN = {50: 0.14, 55: 0.14, 60: 0.09}                         # AN-Anteil = Haelfte von 28 % bzw. 18 %
ERB_FREIBETRAG_KIND = 400000
KINDER_MIO, ERW_MIO = 14, 70

# ---- Recht 2026 (heute) ----
BBG_KV, BBG_RV = 69750, 101400
AN_KV_PV = 0.073 + 0.0145 + 0.018           # KV 7,3 + halber durchschn. Zusatzbeitrag 1,45 + PV 1,8
AN_KINDERLOS = 0.006
AN_RV_AV = 0.093 + 0.013
KINDERGELD = 259
WK_PAUSCH, SA_PAUSCH = 1230, 36
SOLI_FG = 20350

# =====================================================================
# 1  STEUER- UND ABGABENFUNKTIONEN
# =====================================================================
def est_2026(zve):
    zve = math.floor(max(0, zve))
    if zve <= 12348: return 0.0
    if zve <= 17799: y = (zve-12348)/1e4; return math.floor((914.51*y+1400)*y)
    if zve <= 69878: z = (zve-17799)/1e4; return math.floor((173.10*z+2397)*z+1034.87)
    if zve <= 277825: return math.floor(0.42*zve-11135.63)
    return math.floor(0.45*zve-19470.38)

def soli_2026(est, split=False):
    fg = SOLI_FG*(2 if split else 1)
    if est <= fg: return 0.0
    return min(0.055*est, 0.119*(est-fg))

def sv_heute(b, kinderlos=True):
    kvpv = (AN_KV_PV + (AN_KINDERLOS if kinderlos else 0))*min(b, BBG_KV)
    return kvpv + AN_RV_AV*min(b, BBG_RV)

def netto_heute(b, kinder=0, partner=False):
    sv = sv_heute(b, kinderlos=(kinder == 0))
    zve = max(0, b - sv - WK_PAUSCH*(b > 0) - SA_PAUSCH*(2 if partner else 1))
    est = 2*est_2026(zve/2) if partner else est_2026(zve)
    soli = soli_2026(est, partner)
    return dict(netto=b - sv - est - soli + kinder*KINDERGELD*12, est=est+soli, sv=sv)

def est_2828(x, saetze=TARIF_SAETZE, grenzen=TARIF_GRENZEN):
    s, prev = 0.0, 0.0
    for g, r in zip(grenzen, saetze):
        if x > prev: s += (min(x, g)-prev)*r
        prev = g
        if x <= g: break
    return s

def netto_2828(b, kinder=0, partner=False, anteil=50):
    dd = DD_EUR[anteil]*12
    sv = SV_AN[anteil]*b                          # keine Bemessungsgrenzen
    est = est_2828(b + dd)                        # DD steuerpflichtig, Individualbesteuerung
    kind = kinder*DD_EUR[anteil]*KIND_ANTEIL*12   # Kinder-DD steuerfrei (Annahme)
    p = 0.0
    if partner: p = dd - est_2828(dd)             # Partner: eigene DD, eigene Veranlagung
    return dict(netto=b - sv - est + dd + kind + p, est=est, sv=sv, dd=dd + kind + p)

def r_eff_mwst(stufen=MWST_STUFEN):
    return sum(w*s for w, s in zip(MWST_GEWICHTE, stufen))/100
R_EFF_HEUTE = 0.165                               # Projektannahme effektiver Satz heute

def konsumquote(n): return .95 if n < 25000 else .85 if n < 50000 else .75 if n < 80000 else .60
def mwst_mehrbelastung(netto):
    r = r_eff_mwst()
    return netto*konsumquote(netto)*(r/(1+r) - R_EFF_HEUTE/(1+R_EFF_HEUTE))

# =====================================================================
# 2  MAKRO: AUFKOMMEN UND AUSGABEN JE STUFE (Modell-Mrd.)
# =====================================================================
VERT = [(6,8000),(11,20000),(12,36000),(7,52000),(5,69000),(3,105000),(1,300000)]
S25, G25 = [0,.08,.14,.19,.23,.25], [12000,25000,40000,55000,70000,float('inf')]
def _grenz(b, r, g):
    for gg, x in zip(g, r):
        if b <= gg: return x
    return r[-1]
# Kalibrierung wie Projekt: 25er-Tarif + DD 6.000 = 284 Mrd.
K_EST = 284/sum(mio*est_2828(b+6000, S25, G25)/1000 for mio, b in VERT)

SZ = {
 'Optimistisch': dict(g_e=.030,g_a=.026,dd_idx=.02,verh=50,eti=.25,semi=.8,eps=.7,leak=.85,drag=.0003,schock={},schock_a={},hc=1.0),
 'Robust':       dict(g_e=.030,g_a=.030,dd_idx=.02,verh=20,eti=.35,semi=1.0,eps=.8,leak=.80,drag=.0004,schock={},schock_a={},hc=1.0),
 'Stress':       dict(g_e=.020,g_a=.020,dd_idx=.02,verh=0, eti=.50,semi=1.5,eps=1.0,leak=.70,drag=.0006,
                      schock={5:.94,6:.96,7:.98}, schock_a={5:20,6:20}, hc=0.7),
}

def est_aufkommen(anteil, eti):
    dd = DD_EUR[anteil]*12; tot = 0.0
    for mio, b in VERT:
        m0, m1 = _grenz(b+dd, S25, G25), _grenz(b+dd, TARIF_SAETZE, TARIF_GRENZEN)
        b1 = b*((1-m1)/(1-m0))**eti
        tot += mio*est_2828(b1+dd)/1000
    return K_EST*tot            # 25 Mio. Erwachsene ohne Markteinkommen: DD < Existenzminimum -> 0

def mwst_aufkommen(leak):
    r0 = 0.18; brutto = 350/(r0/(1+r0)); r1 = r_eff_mwst()
    return 350 + (brutto*r1/(1+r1) - 350)*leak

def einnahmen(anteil, sc, detail=False):
    t = L/100
    d = {
     'Einkommensteuer (inkl. steuerpfl. DD)': est_aufkommen(anteil, sc['eti']),
     'Kapitalerträge 28 %':                   45*(t/.25)*((1-t)/.75)**sc['eps'],
     'Mehrwertsteuer (Label 5–28 %)':         mwst_aufkommen(sc['leak']),
     'Unternehmen & Plattformen 28 %':        145*(t/.25)*math.exp(-sc['semi']*(L-25)/100),
     'Erbschaft 28 %':                        33*(t/.25)*math.exp(-(L-25)/100),
     'Vermögen-Mindeststeuer (anrechenbar)':  22*(1-0.02*(L-25)),
     'CO₂-Abgabe 100 €/t (netto)':            55,
     'Sonstige Steuern':                      165,
    }
    return (sum(d.values()), d) if detail else sum(d.values())

BAUSTEINE = {   # Zusatzeinnahmen (statisch, Modell-Mrd.), Annahmen gestuetzt auf DIW/UBA/Destatis
 'Vermögensteuer 1 % ab 2 Mio. (nicht anrechenbar)': 12,
 'Bodenwertabgabe statt Grundsteuer':               20,
 'Abbau klimaschädlicher Subventionen':             20,
 'CO₂-Pfad 100 → 150 €/t (voll ab Jahr 5)':          15,
}
def bausteine(t):
    return sum(BAUSTEINE.values()) - 15 + min(15, 3*(t+1))

AUSG = {  # Basisausgaben nach Transferersatz/RV/Verwaltung, SV-Zuschuss, Haertefall
 50: dict(basis=596, zusch=60, haerte=40),   # inkl. Bestandsgarantie (~5 Mrd.) fuer heutige Grundsicherungsbezieher
 55: dict(basis=596, zusch=60, haerte=40),
 60: dict(basis=576, zusch=90, haerte=42),
}
def dd_kosten(a): return (ERW_MIO*DD_EUR[a]*12 + KINDER_MIO*DD_EUR[a]*KIND_ANTEIL*12)/1000
def ausgaben(a): return sum(AUSG[a].values()) + dd_kosten(a)

# =====================================================================
# 3  HAUSHALTSPFAD 2028-2047 MIT REGELN
# =====================================================================
BIP0, START = 4200, 2028
INV, PUFFER, STARTPUFFER = 0.01, 0.02, 100.0
STUFEN = [50, 55, 60]

def simuliere(sc, mit_bausteinen=True, jahre=20):
    g_e = sc['g_e'] - sc['drag']*(L-25); g_a = sc['g_a'] - 0.5*sc['drag']*(L-25)
    E = {a: einnahmen(a, sc) for a in STUFEN}
    F, i, idx, idx_voll, letzter_schritt, rows = STARTPUFFER, 0, 1.0, 1.0, -99, []
    for t in range(jahre):
        bip = BIP0*(1+g_e)**t
        if t > 0: idx_voll *= 1+sc['dd_idx']
        def saldo(a, ix):
            e = (E[a] + (bausteine(t)*sc['hc'] if mit_bausteinen else 0))*(1+g_e)**t*sc['schock'].get(t,1.0) \
                + (sc['verh'] if t >= 2 else 0)
            x = AUSG[a]; aus = (x['basis']+x['zusch']+x['haerte'])*(1+g_a)**t + dd_kosten(a)*ix + sc['schock_a'].get(t,0)
            return e - aus
        # Regel 3: jaehrliche Anpassung an das Existenzminimum, solange der Puffer nicht angegriffen ist;
        #          ausgesetzte Anpassungen werden nur aus Ueberschuessen nachgeholt
        if t > 0 and F >= PUFFER*bip:
            idx *= 1+sc['dd_idx']
            if idx < idx_voll - 1e-9:
                kosten = dd_kosten(STUFEN[i])*(idx_voll-idx)
                if saldo(STUFEN[i], idx_voll) >= INV*bip and F - PUFFER*bip - INV*bip >= 2*kosten: idx = idx_voll
        # Regel 2: Aufstieg 50->55->60 %, fruehestens Jahr 3, Abstand >= 2 Jahre
        rest = max(F - PUFFER*bip, 0)
        if i < 2 and t >= 2 and t - letzter_schritt >= 2 and F >= PUFFER*bip \
           and saldo(STUFEN[i+1], idx) + rest/10 >= INV*bip:
            i += 1; letzter_schritt = t
        S = saldo(STUFEN[i], idx); F += S
        luecke = F < 0
        inv = min(max(F - PUFFER*bip, 0), INV*bip); F -= inv
        rows.append(dict(jahr=START+t, t=t+1, anteil=STUFEN[i], dd=DD_EUR[STUFEN[i]]*idx, dd_2026=DD_EUR[STUFEN[i]]*idx/idx_voll, dd_real=idx/idx_voll,
                         saldo=S, inv=inv, ziel=INV*bip, fonds=F, luecke=luecke, bip=bip))
    return rows

def kennzahlen(rows):
    return dict(saldo1=rows[0]['saldo'], min_saldo=min(r['saldo'] for r in rows),
                luecken=sum(r['luecke'] for r in rows), min_fonds=min(r['fonds'] for r in rows),
                j55=next((r['jahr'] for r in rows if r['anteil']>=55), None),
                j60=next((r['jahr'] for r in rows if r['anteil']>=60), None),
                invquote=sum(r['inv'] for r in rows)/sum(r['ziel'] for r in rows),
                inv_kum=sum(r['inv'] for r in rows), fonds_ende=rows[-1]['fonds'],
                dd_real_min=min(r['dd_real'] for r in rows)*1.0)

# =====================================================================
# 4  AUSGABE
# =====================================================================
if __name__ == '__main__':
    out = {}
    P = lambda s: print(s)
    P("="*100); P("A | TARIF, LABEL, DIVIDENDE"); P("="*100)
    P(f"ESt-Tarif 28:28: " + " | ".join(f"bis {g:,.0f}: {r*100:.0f} %" if g != float('inf') else f"darüber: {r*100:.0f} %" for g, r in zip(TARIF_GRENZEN, TARIF_SAETZE)))
    P(f"MwSt-Label: {MWST_STUFEN}  -> effektiv {r_eff_mwst()*100:.1f} % (heute Projektannahme {R_EFF_HEUTE*100:.1f} %)")
    for a in STUFEN:
        P(f"DD {a} %: Erwachsene {DD_EUR[a]:.2f} EUR/M, Kinder {DD_EUR[a]*KIND_ANTEIL:.2f} EUR/M, Kosten brutto {dd_kosten(a):.1f} Mrd., SV gesamt {SV_AN[a]*200:.0f} %")
    P(f"Hinweis: Kinder-DD 257,50 EUR liegt 1,50 EUR unter dem Kindergeld 2026 (259 EUR).")

    P("\n"+"="*100); P("B | STATISCHER HAUSHALT JE STUFE (Modell-Mrd., Szenario Robust)"); P("="*100)
    tabB = {}
    for a in STUFEN:
        e, d = einnahmen(a, SZ['Robust'], True)
        tabB[a] = dict(einnahmen=d, einnahmen_summe=e, bausteine=sum(BAUSTEINE.values()),
                       ausgaben=dict(AUSG[a], dd=dd_kosten(a)), ausgaben_summe=ausgaben(a),
                       saldo_ohne=e-ausgaben(a), saldo_mit=e+sum(BAUSTEINE.values())-ausgaben(a))
    keys = list(tabB[50]['einnahmen'].keys())
    P(f"{'':<42}{'50 %':>10}{'55 %':>10}{'60 %':>10}")
    for k in keys: P(f"{k:<42}" + "".join(f"{tabB[a]['einnahmen'][k]:>10.1f}" for a in STUFEN))
    P(f"{'= Einnahmen Kernsystem':<42}" + "".join(f"{tabB[a]['einnahmen_summe']:>10.1f}" for a in STUFEN))
    for k, v in BAUSTEINE.items(): P(f"{'+ '+k:<42}" + f"{v:>10.1f}"*3)
    P(f"{'Ausgaben: Basis':<42}" + "".join(f"{AUSG[a]['basis']:>10.1f}" for a in STUFEN))
    P(f"{'Ausgaben: SV-Zuschuss':<42}" + "".join(f"{AUSG[a]['zusch']:>10.1f}" for a in STUFEN))
    P(f"{'Ausgaben: Härtefall + Gesundheit':<42}" + "".join(f"{AUSG[a]['haerte']:>10.1f}" for a in STUFEN))
    P(f"{'Ausgaben: Digitaldividende':<42}" + "".join(f"{dd_kosten(a):>10.1f}" for a in STUFEN))
    P(f"{'= Ausgaben':<42}" + "".join(f"{ausgaben(a):>10.1f}" for a in STUFEN))
    P(f"{'SALDO ohne Bausteine':<42}" + "".join(f"{tabB[a]['saldo_ohne']:>+10.1f}" for a in STUFEN))
    P(f"{'SALDO mit Bausteinen':<42}" + "".join(f"{tabB[a]['saldo_mit']:>+10.1f}" for a in STUFEN))
    P(f"{'  in % BIP':<42}" + "".join(f"{tabB[a]['saldo_mit']/BIP0*100:>+10.2f}" for a in STUFEN))
    P(f"Zielsaldo Investitionen: +{INV*BIP0:.0f}")
    out['statisch'] = tabB

    P("\n"+"="*100); P("C | HAUSHALTSPFAD 2028-2047 (Startpuffer 100, Puffer 2 % BIP, Investitionen 1 % BIP)"); P("="*100)
    out['pfade'] = {}
    for name, sc in SZ.items():
        for mb in (True, False):
            rows = simuliere(sc, mb); k = kennzahlen(rows)
            lab = f"{name} {'mit' if mb else 'ohne'} Bausteine"
            out['pfade'][lab] = dict(rows=rows, kennzahlen=k)
            P(f"\n{lab}: Saldo J1 {k['saldo1']:+.0f} | min. Saldo {k['min_saldo']:+.0f} | Lückenjahre {k['luecken']} | min. Fonds {k['min_fonds']:.0f}"
              f" | 55 % ab {k['j55']} | 60 % ab {k['j60']} | Inv-Quote {k['invquote']*100:.0f} % | Inv kum. {k['inv_kum']:.0f}"
              f" | Fonds 2047 {k['fonds_ende']:.0f} | DD real min. {k['dd_real_min']*100:.0f} % des Sollwerts")
            if mb:
                P("  Jahr  " + " ".join(f"{r['jahr']:>5}" for r in rows))
                P("  Stufe " + " ".join(f"{r['anteil']:>5}" for r in rows))
                P("  DD €  " + " ".join(f"{r['dd']:>5.0f}" for r in rows))
                P("  DD'26 " + " ".join(f"{r['dd_2026']:>5.0f}" for r in rows))
                P("  Saldo " + " ".join(f"{r['saldo']:>+5.0f}" for r in rows))
                P("  Inv   " + " ".join(f"{r['inv']:>5.0f}" for r in rows))
                P("  Fonds " + " ".join(f"{r['fonds']:>5.0f}" for r in rows))

    P("\n"+"="*100); P("D | MIKROEBENE (EUR/Jahr, Recht 2026 vs. 28:28)"); P("="*100)
    profile = [
      ("Mia, Studentin (22), ohne Einkommen", 0, 0, False),
      ("Tom, Berufseinsteiger", 28000, 0, False),
      ("Sarah, Fachkraft", 42000, 0, False),
      ("Durchschnittsverdiener (51.944 €)", 51944, 0, False),
      ("Klaus, Facharbeiter", 55000, 0, False),
      ("Jonas, Ingenieur", 80000, 0, False),
      ("Dr. Weber, Führungskraft", 150000, 0, False),
      ("Familie Müller, Alleinverdiener, 2 Kinder", 63000, 2, True),
      ("Anna, alleinerziehend, 1 Kind", 28000, 1, False),
    ]
    mikro = []
    P(f"{'Profil':<44}{'heute':>9}{'50 %':>9}{'55 %':>9}{'60 %':>9}{'Δ 50 %':>9}{'MwSt':>8}{'Δ netto':>9}{'in %':>7}")
    for n, b, k, p in profile:
        h = netto_heute(b, k, p)['netto']
        v = {a: netto_2828(b, k, p, a)['netto'] for a in STUFEN}
        mw = mwst_mehrbelastung(v[50])
        d = v[50]-h; dn = d-mw
        mikro.append(dict(profil=n, brutto=b, kinder=k, partner=p, heute=h, s50=v[50], s55=v[55], s60=v[60], mwst=mw, delta=d, delta_nach_mwst=dn))
        pct = f"{dn/h*100:+.0f}" if h > 0 else "n.v."
        P(f"{n:<44}{h:>9.0f}{v[50]:>9.0f}{v[55]:>9.0f}{v[60]:>9.0f}{d:>+9.0f}{-mw:>8.0f}{dn:>+9.0f}{pct:>7}")
    # Rentnerin
    rente = 880*12
    h_inge = 1060*12
    kv_r_heute_satz = 0.073+0.0145+0.036+0.006
    inge = {a: rente - rente*(0.1235*(SV_AN[a]/0.2115)) + DD_EUR[a]*12 - est_2828(rente + DD_EUR[a]*12) for a in STUFEN}
    P(f"{'Inge, Rentnerin (880 €/M, heute mit GruSi)':<44}{h_inge:>9.0f}{inge[50]:>9.0f}{inge[55]:>9.0f}{inge[60]:>9.0f}{inge[50]-h_inge:>+9.0f}")
    mikro.append(dict(profil='Inge, Rentnerin (880 €/M)', brutto=rente, heute=h_inge, s50=inge[50], s55=inge[55], s60=inge[60]))
    out['mikro'] = mikro

    # Belastung Durchschnittsverdiener
    b = 51944
    hh = netto_heute(b)
    bel_h = (hh['est']+hh['sv'])/b*100
    bel = {a: (netto_2828(b,0,False,a)['est']+netto_2828(b,0,False,a)['sv'])/b*100 for a in STUFEN}
    beln = {a: (netto_2828(b,0,False,a)['est']+netto_2828(b,0,False,a)['sv']-DD_EUR[a]*12)/b*100 for a in STUFEN}
    P(f"\nDurchschnittsverdiener 51.944 €: Abgabenlast heute {bel_h:.1f} % | 28:28 {bel[50]:.1f} / {bel[55]:.1f} / {bel[60]:.1f} %"
      f" | nach Dividende {beln[50]:.1f} / {beln[55]:.1f} / {beln[60]:.1f} %")
    # Grenzbelastung
    def grenz_heute(b): return (netto_heute(b+100)['netto']-netto_heute(b)['netto'])
    def grenz_neu(b):   return (netto_2828(b+100)['netto']-netto_2828(b)['netto'])
    P(f"Grenzbelastung (Abgaben je zusätzliche 100 €) bei 51.944 €: heute {100-grenz_heute(b):.0f} % | 28:28 {100-grenz_neu(b):.0f} %")
    out['durchschnitt'] = dict(brutto=b, belastung_heute=bel_h, belastung=bel, belastung_nach_dd=beln,
                               grenz_heute=100-grenz_heute(b), grenz_neu=100-grenz_neu(b))

    # Gini (grobe Modellschaetzung, Individuen 18+)
    def gini(pairs):
        pairs = sorted(pairs, key=lambda x: x[1]); N = sum(w for w, _ in pairs); Y = sum(w*y for w, y in pairs)
        cum, area = 0.0, 0.0
        for w, y in pairs:
            area += w*(cum + w*y/2); cum += w*y
        return 1 - 2*area/(N*Y)
    TRANSFER_HEUTE = 3000   # ANNAHME: durchschnittliche Transfers je Erwachsenem ohne Markteinkommen
    g_h = gini([(m_, netto_heute(b_)['netto']) for m_, b_ in VERT] + [(25, TRANSFER_HEUTE)])
    g_n = {a: gini([(m_, netto_2828(b_,0,False,a)['netto']) for m_, b_ in VERT] + [(25, DD_EUR[a]*12)]) for a in STUFEN}
    P(f"Gini-Modellwert (verfügbar, Erwachsene, grob): heute {g_h:.3f} | 28:28 {g_n[50]:.3f} / {g_n[55]:.3f} / {g_n[60]:.3f}"
      f" | relative Änderung {(g_n[50]/g_h-1)*100:+.0f} % / {(g_n[60]/g_h-1)*100:+.0f} %")
    for tr in (2000, 5000):
        gh = gini([(m_, netto_heute(b_)['netto']) for m_, b_ in VERT] + [(25, tr)])
        gn = gini([(m_, netto_2828(b_,0,False,50)['netto']) for m_, b_ in VERT] + [(25, DD_EUR[50]*12)])
        P(f"  Sensitivität Transfers heute {tr} EUR: relative Änderung {(gn/gh-1)*100:+.0f} %")
    out['gini'] = dict(heute=g_h, neu=g_n)

    # Rechner-Tabelle
    with open('rechner-2828-tabelle.csv','w',newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['brutto','kinder','partner','heute_netto','heute_est_soli','heute_sv',
                    'neu50_netto','neu50_est','neu50_sv','neu55_netto','neu60_netto','plus50','plus60'])
        for b in range(0, 200001, 5000):
            for k in (0,1,2,3):
                for p in (False, True):
                    h = netto_heute(b,k,p); n50 = netto_2828(b,k,p,50)
                    w.writerow([b,k,int(p),round(h['netto']),round(h['est']),round(h['sv']),
                                round(n50['netto']),round(n50['est']),round(n50['sv']),
                                round(netto_2828(b,k,p,55)['netto']),round(netto_2828(b,k,p,60)['netto']),
                                round(n50['netto']-h['netto']),round(netto_2828(b,k,p,60)['netto']-h['netto'])])
    with open('modell-2828-daten.json','w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=float)
    P("\nDateien: rechner-2828-tabelle.csv, modell-2828-daten.json")

    # ================= ANTEIL MIT MEHR IM GELDBEUTEL (grobe Gruppenabschaetzung) =================
    P("\n"+"="*100); P("F | ANTEIL DER BEVÖLKERUNG MIT MEHR VERFÜGBAREM EINKOMMEN (Schätzung, Mio. Personen)"); P("="*100)
    BEV = 84.0
    risiko = {   # Personen, die OHNE Bestandsgarantie schlechter stuenden (Annahmen, siehe Datenblatt)
     'Bürgergeld-Haushalte ohne Erwerbseinkommen (von 5,5 Mio.)': 3.5,
     'Erwerbsminderungs-Grundsicherung ohne weiteres Einkommen':   0.36,
     'BAföG mit hohem Förderbetrag':                               0.3,
     'Sehr große Vermögen (Netto-Verlierer)':                      0.4,
    }
    for k_, v_ in risiko.items(): P(f"  {k_:<62} {v_:>5.2f}")
    ohne_g = BEV - sum(risiko.values()); mit_g = BEV - risiko['Sehr große Vermögen (Netto-Verlierer)']
    P(f"  Anteil mit mehr Geld: ohne Bestandsgarantie {ohne_g/BEV*100:.0f} % | mit Bestandsgarantie {mit_g/BEV*100:.0f} %")
    out['anteil_gewinner'] = dict(ohne_garantie=ohne_g/BEV, mit_garantie=mit_g/BEV, risikogruppen=risiko)

    # ================= HOMEPAGE: ZEITREIHEN (2010-2035) =================
    P("\n"+"="*100); P("E | HOMEPAGE-ZEITREIHEN (hist/ohne = bestehende Homepage-Werte; mit = Robust-Pfad 28:28)"); P("="*100)
    rob = {r['jahr']: r for r in out['pfade']['Robust mit Bausteine']['rows']}
    J = list(range(2026, 2036))
    OHNE = dict(schulden=[64,65,65,66,66,67,67,68,68,69],
                gini=[.313,.313,.314,.314,.315,.315,.316,.316,.317,.317],
                co2=[608,596,584,572,560,549,538,527,516,505],
                last=[36.7,36.8,36.9,37.0,37.1,37.2,37.3,37.4,37.5,37.6])
    MIT_CO2_ALT = [608,596,578,552,524,496,470,446,424,404]
    gfak = {50: g_n[50]/g_h, 55: g_n[55]/g_h, 60: g_n[60]/g_h}
    lfak = {a: bel[a]/bel_h for a in STUFEN}
    mit = dict(schulden=[], gini=[], co2=MIT_CO2_ALT, last=[])
    for k, j in enumerate(J):
        if j < START:
            mit['schulden'].append(OHNE['schulden'][k]); mit['gini'].append(OHNE['gini'][k]); mit['last'].append(OHNE['last'][k])
        else:
            r = rob[j]
            mit['schulden'].append(round(OHNE['schulden'][k] - r['fonds']/r['bip']*100, 1))
            mit['gini'].append(round(OHNE['gini'][k]*gfak[r['anteil']], 3))
            mit['last'].append(round(OHNE['last'][k]*lfak[r['anteil']], 1))
    for key in mit: P(f"  {key:<9} ohne {OHNE[key]}\n  {'':<9} mit  {mit[key]}")
    out['zeitreihen'] = dict(jahre=J, ohne=OHNE, mit=mit)
    with open('modell-2828-daten.json','w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=float)
