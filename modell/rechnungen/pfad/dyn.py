# -*- coding: utf-8 -*-
"""Dynamischer Pfad 2028-2060. Alle Groessen in % des Klub-BIP, sofern nicht anders vermerkt.
Grundlagen: Eurostat 2024 (gepruefte Einzelabrufe), Haager Gipfelerklaerung 25.6.2025,
Fruehjahrsprojektion der Bundesregierung 22.4.2026."""

G_NOM   = 0.030     # nominales BIP-Wachstum p.a., vorsichtige Fortschreibung
A_OHNE_V= 6.44      # Ebene A ohne Verteidigung
B_AUFG  = 10.35     # Ebene B, Fachaufgaben
V_START, V_ZIEL, V_JAHR = 1.40, 3.50, 2035   # Verteidigung: heute -> Haager Zusage
D_START = 78.4      # Schuldenstand % BIP, Klub 2024
I_ALT   = 1.53      # effektiver Zins des Altbestands
REST    = 7.5       # mittlere Restlaufzeit in Jahren
BIP28_KLUB = 12157*1.1702/1000   # Bio EUR, Klub 2028 auf derselben Basis wie Deutschland
POP = 255.06e6

def verteidigung(j):
    if j >= V_JAHR: return V_ZIEL
    return V_START + (V_ZIEL-V_START)*(j-2028)/(V_JAHR-2028)

def zins_eff(j, ziel):
    """Altbestand laeuft linear ueber REST Jahre aus und wird zum Zielsatz erneuert."""
    a = min((j-2028)/REST, 1.0)
    return I_ALT + (ziel-I_ALT)*a

def lauf(quote, zinsziel, tilgung=0.0, jahre=33):
    d = D_START; bip = BIP28_KLUB; out=[]
    for j in range(2028, 2028+jahre):
        i = zins_eff(j, zinsziel)
        zinslast = d*i/100
        v = verteidigung(j)
        fest = A_OHNE_V + v + B_AUFG + zinslast + tilgung
        div = quote - fest
        out.append(dict(jahr=j, bip=bip, schuld=d, zins=i, zinslast=zinslast, vert=v,
                        fest=fest, div=div, div_kopf=div/100*bip*1e12/POP/12))
        # Haushalt ausgeglichen: Schuldenstand in Euro konstant, ausser es wird getilgt
        d = (d - tilgung)/(1+G_NOM)
        bip *= 1+G_NOM
    return out
