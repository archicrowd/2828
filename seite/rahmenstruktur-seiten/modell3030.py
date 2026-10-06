#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
30:30 – konsolidiertes Haushaltsmodell (Gebietskoerperschaften + Sozialversicherung)
Interpolation 25 -> 30, Verhaltenselastizitaeten, drei Szenarien, 20-Jahres-Pfad.
Alle Betraege Mrd. EUR, Preisbasis 2025. Delta-Rechnung gegenueber geltendem Recht.

KALIBRIERUNG (amtlich, 2025)
  BMF Monatsbericht 01/2026: LSt 262,7 (nach Kindergeld), vESt 78,4, nvSvE 31,1,
      AbgSt 24,8, KSt 39,2, USt 310,2, Soli 12,9, ErbSt 15,4
  BA Familienkasse 01/2026: Kindergeld 55,3, Kinderzuschlag 3,3
  Destatis 2025: Staatsdefizit 119,1 (2,7 % BIP); DRV-Renten 417,9; ALG I 28,2; Wohngeld 5,0
  Bundesbank 03/2026: Schuldenstand 2.838 = 63,5 % BIP  -> BIP ~ 4.469
  DRV 12/2025: RV-Beitraege 2025 ~321; 21,5 Mio. Rentner (DRV 2024)
  Destatis 2024: Gewerbesteuer 75,3 (2025 hier 76 angenommen)
EIGENE SCHAETZUNGEN sind als ANNAHME markiert.
"""
import numpy as np, json, math

BIP = 4469.0
ESt_ALT = 262.7 + 55.3 + 78.4 + 9.0      # brutto inkl. Kindergeld-Verrechnung + Soli-Anteil ESt (ANNAHME 9)
KAP_ALT = 24.8 + 31.1                    # AbgSt + nicht veranlagte St. v. Ertrag
U_ALT   = 39.2 + 76.0 + 2.1              # KSt + GewSt + Soli-KSt (ANNAHME 2,1)
UST_ALT = 310.2
ERB_ALT = 15.4
SV_ALT  = 776.0                          # ANNAHME: Beitragssaetze x Bemessung (RV 321 amtlich)
SV_SATZ_ALT = 41.9                       # 18,6 RV + 14,6 KV + 2,5 Zusatz + 3,6 PV + 2,6 AV
N_ERW, N_KIND = 69.4, 14.2               # Mio. (Bevoelkerung ~83,6 Mio.; ANNAHME Aufteilung)
N_RENTE = 21.5 + 1.4                     # DRV-Rentner + Versorgungsempfaenger (ANNAHME 1,4)

# ------------------------------------------------------------------ Tarife
GRENZEN = [12000, 25000, 40000, 55000, 70000]
SAETZE25 = [0.00, 0.08, 0.14, 0.19, 0.23, 0.25]          # finaler 25:25-PLUS-Tarif (Projekt)
def tarif(X):
    return [r * X / 25 for r in SAETZE25]                 # proportionale Interpolation

def est_neu(y, X):
    s = tarif(X); t = np.zeros_like(y, dtype=float); lo = 0.0
    for g, r in zip(GRENZEN + [1e12], s):
        t += np.clip(y - lo, 0, g - lo) * r
        lo = g
    return t

def grenz_neu(y, X):
    s = tarif(X)
    idx = np.searchsorted(np.array(GRENZEN, dtype=float), y, side="left")
    return np.array(s)[idx]

def est_alt(z):                          # §32a EStG 2025 (vektorisiert)
    z = np.asarray(z, dtype=float)
    y = (z - 12096) / 1e4; q = (z - 17443) / 1e4
    return np.select([z <= 12096, z <= 17443, z <= 68480, z <= 277825],
                     [0.0, (932.3 * y + 1400) * y, (176.64 * q + 2397) * q + 1015.13, 0.42 * z - 10911.92],
                     0.45 * z - 19246.67)

def soli(t):
    return np.where(t <= 19950, 0.0, np.minimum(0.055 * t, 0.119 * (t - 19950)))

def gesamt_alt(z):
    t = est_alt(z); return t + soli(t)

def grenz_alt(z):
    return (gesamt_alt(z + 100) - gesamt_alt(z)) / 100

# ------------------------------------------------------------------ Verteilung (ANNAHME, parametrisch)
rng = np.random.default_rng(2525)
def verteilung():
    # Erwerbstaetige 42 Mio. (Lognormal + Pareto-Rand), Renten 20,9 Mio., Sonstige 6,5 Mio.
    n = 60_000
    w = rng.lognormal(mean=np.log(40000), sigma=0.72, size=n)
    tail = rng.random(n) < 0.04
    w[tail] = 110000 * (1 - rng.random(tail.sum())) ** (-1 / 1.9)
    w *= (2000 + 280 + 60) * 1e9 / (w.mean() * 42e6)          # Loehne + Gewinne + V+V
    r = rng.lognormal(mean=np.log(21000), sigma=0.55, size=n)
    r *= 553e9 / (r.mean() * 20.9e6)                           # GRV + Pensionen + bAV
    o = rng.lognormal(mean=np.log(2500), sigma=0.9, size=n)
    return w, r, o
W, R, O = verteilung()
GEW = {"w": 42.0 / len(W), "r": 20.9 / len(R), "o": 6.5 / len(O)}   # Mio. Personen je Draw

vest_alt = gesamt_alt
def modell_alt():
    zw = np.maximum(0, W * (1 - 0.18) - 1230)                  # SV-AN-Anteil + WK (vereinfacht)
    zr = np.maximum(0, R * 0.80 * (1 - 0.11) - 102)            # Besteuerungsanteil, KV/PV
    return (vest_alt(zw).sum() * GEW["w"] + vest_alt(zr).sum() * GEW["r"]) / 1000
K_SPLIT = ESt_ALT / modell_alt()                               # Kalibrierfaktor (Splitting etc.)

# ------------------------------------------------------------------ Szenarien
SZ = {
 "konservativ": dict(eti=0.10, lam=1.5, sigma=0.05, plat=0.5, arbeit=-0.015, buero=-10,
                     inz=0.50, comp=0.94, wegfall=90,  erb=0.80, co2=24),
 "basis":       dict(eti=0.15, lam=1.0, sigma=0.10, plat=1.0, arbeit=-0.005, buero=-20,
                     inz=0.67, comp=0.96, wegfall=101, erb=0.90, co2=30),
 "optimistisch":dict(eti=0.25, lam=0.7, sigma=0.20, plat=1.3, arbeit=+0.005, buero=-30,
                     inz=0.80, comp=0.97, wegfall=125, erb=1.00, co2=36),
}

# ------------------------------------------------------------------ Kernrechnung (Vollausbau, statisch+Verhalten)
def rechne(X, s, dd=(600, 300), a=0.5, p=SZ["basis"], X_est=None, X_ust=None, detail=False, kind_min=255.0):
    Xe = X if X_est is None else X_est
    Xu = X if X_ust is None else X_ust
    dA, dK = dd
    if dA > 0: dK = max(dK, kind_min)          # Kinder-DD nie unter heutigem Kindergeld
    # Arbeitgeber-Entlastung -> Lohninzidenz (Anteil p['inz'] in Bruttoloehne)
    ag_alt, ag_neu = SV_SATZ_ALT / 2, s / 2
    lohn_hub = p["inz"] * (ag_alt - ag_neu) / (100 + ag_neu)
    # Einkommensteuer (individuell, breite Basis, DD steuerpflichtig)
    m_old = grenz_alt(np.maximum(0, W * 0.82)) + 0.20 * (W < 96600)
    base = W * (1 + lohn_hub) * (1 + p["arbeit"])
    m_new = grenz_neu(base, Xe) + s / 200
    fak = ((1 - m_new) / np.maximum(0.05, 1 - m_old)) ** p["eti"]
    yw = base * fak + dA * 12
    anr = a * 0.85 * dA * 12                                  # Rentensockel-Anrechnung
    yr = R - np.minimum(R, anr) + dA * 12
    yo = O + dA * 12
    vn = lambda y: est_neu(y, Xe)
    est = (vn(yw).sum() * GEW["w"] + vn(yr).sum() * GEW["r"] + vn(yo).sum() * GEW["o"]) / 1000 * p["comp"]
    d_est = est - ESt_ALT
    # Umsatzsteuer: 5 Nachhaltigkeitsstufen, skaliert
    anteile, st25 = [0.04, 0.10, 0.20, 0.55, 0.11], [5, 10, 15, 20, 25]
    w_neu = sum(q * r * Xu / 25 for q, r in zip(anteile, st25)) / 100
    w_alt = 0.83 * 0.19 + 0.17 * 0.07
    B0 = UST_ALT / w_alt
    ust = w_neu * B0 * (1 - p["lam"] * (w_neu - w_alt)) * 1.02
    d_ust = ust - UST_ALT
    # Kapital
    kap = KAP_ALT * (X / 26.375) * 1.15 * ((1 - X / 100) / (1 - 0.26375)) ** 0.5
    d_kap = kap - KAP_ALT
    # Unternehmen + Plattformen (Nutzungsort)
    unt = U_ALT * (X / 30.0) * (1 + p["sigma"]) * (1 + 0.005 * (30 - X)) - 8.0
    plat = p["plat"] * (X / 100 * 38 * 0.85 - 1.0)
    unt += (ag_alt - ag_neu) / 100 * 1500 * (1 - p["inz"]) * X / 100   # nicht ueberwaelzter AG-Anteil
    d_unt = unt + plat - U_ALT
    # Erbschaft, Vermoegen-Mindeststeuer, CO2
    d_erb = 150 * X / 100 * 0.9 * (1 - 0.02 * (X - 25)) * p["erb"] - ERB_ALT
    d_verm = 10 - 0.6 * (X - 25)
    d_co2 = p["co2"]
    # Sozialversicherung
    # BBG-Aufhebung: nur KV/PV-Anteil dauerhaft (+6 %); RV-Anteil erzeugt spaetere Rentenansprueche
    sv = SV_ALT * (s / SV_SATZ_ALT) * 1.06 * (1 + lohn_hub * 0.8)
    # ~10 % der Beitraege zahlt der Staat selbst (AG oeff. Dienst, BA/Bund fuer Leistungsbezieher, KEZ)
    d_sv = (sv - SV_ALT) * 0.90
    E = dict(ESt=d_est, USt=d_ust, Kapital=d_kap, Unternehmen=d_unt, Erbschaft=d_erb,
             Vermoegen=d_verm, CO2=d_co2, SV=d_sv)
    # Ausgaben
    dd_kost = (N_ERW * dA + N_KIND * dK) * 12 / 1000
    rsockel = -a * 0.85 * dA * 12 * N_RENTE / 1000
    # Kindergeld + KiZ (58,6) entfallen vollstaendig, sobald DD gezahlt wird; Rest skaliert mit DD-Hoehe
    wegf = -((58.6 if dA > 0 else 0.0) + (p["wegfall"] - 58.6) * (min(dA, 563) / 563) ** 0.5)
    A = dict(DD=dd_kost, Rentensockel=rsockel, Wegfall=wegf, Haerte=40.0, Buerokratie=p["buero"])
    saldo = sum(E.values()) - sum(A.values())
    if detail:
        return saldo, E, A, dict(w_neu=w_neu, lohn_hub=lohn_hub, plat=plat)
    return saldo

# ------------------------------------------------------------------ Zusatzfunktionen
def dd_max(X, s, a, p, puffer=0.0, kind_ant=0.5):
    """hoechste Erwachsenen-DD (EUR/M, 2025-Preise), die bei X, s, a ohne Luecke finanzierbar ist"""
    lo, hi = 0.0, 900.0
    if rechne(X, s, (0, 0), a, p) < puffer * BIP: return None
    for _ in range(22):
        mid = (lo + hi) / 2
        if rechne(X, s, (mid, mid * kind_ant), a, p) >= puffer * BIP: lo = mid
        else: hi = mid
    return lo

def pfad(X, s_ziel, a, p, dd_cap=600, jahre=20, g_nom=0.03, infl=0.02, i=0.028,
         puffer=0.003, stufe=25, dd_index="preise", s_start=None):
    """Haushaltsformel (exakt je Jahr): DD steigt in 25-EUR-Stufen (real), nur wenn der Saldo danach
       >= Puffer bleibt; sie sinkt nie nominal. Nicht-DD-Positionen wachsen mit dem nominalen BIP,
       die DD mit den Preisen (bzw. Loehnen). Einnahmenreform Jahr 1 zu 50 %, ab Jahr 2 voll.
       SV-Satz sinkt linear von s_start auf s_ziel ueber 5 Jahre."""
    s0 = SV_SATZ_ALT if s_start is None else s_start
    d, schuld, res = 0.0, 0.0, []
    for t in range(jahre):
        G = (1 + g_nom) ** t
        P = (1 + infl) ** t if dd_index == "preise" else G
        f = 0.5 if t == 0 else 1.0
        s = s0 + (s_ziel - s0) * min(1.0, (t + 1) / 5)
        def S(dd_real, s_):
            b0 = rechne(X, s_, (0, 0), a, p)
            q = dd_real * P / G
            return G * (f * b0 + (rechne(X, s_, (q, q / 2), a, p, kind_min=255.0 * P / G) - b0))
        # vorausschauend: Stufe nur, wenn sie auch beim Ziel-SV-Satz (volle Einnahmenreform) gedeckt ist
        while d + stufe <= dd_cap and S(d + stufe, s_ziel) / (f if f < 1 else 1) >= puffer * BIP * G \
                and S(d + stufe, s) >= puffer * BIP * G:
            d += stufe
        saldo = S(d, s)
        schuld = schuld * (1 + i) - saldo
        res.append(dict(jahr=2028 + t, dd=d, sv=s, saldo=saldo, saldo_bip=saldo / (BIP * G) * 100,
                        schuld_bip=schuld / (BIP * G) * 100))
    return res

def mikro(X, s, dd, a, w_neu, lohn_hub):
    """Jaehrliches real verfuegbares Einkommen, heute vs. neu (Single, Kinder via Kindergeld/Kinder-DD)"""
    w_alt = 0.83 * 0.19 + 0.17 * 0.07
    preis = (1 + w_neu) / (1 + w_alt)                     # Preisniveau-Effekt der USt (volle Ueberwaelzung)
    dA, dK = dd
    dK = max(dK, 255.0)
    def heute(b, k=0, rente=False, split=False):
        if rente:
            z = max(0, b * 0.80 * 0.89 - 102); return b * 0.89 - float(gesamt_alt(np.array(z)))
        sv = 0.2095 * min(b, 66150) + 0.0 * b
        sv = 0.1155 * min(b, 66150) + 0.106 * min(b, 96600)
        z = max(0, b - sv - 1230 - 1900 * (b > 0))
        if split: t = 2 * float(gesamt_alt(np.array(z / 2)))
        else: t = float(gesamt_alt(np.array(z)))
        return b - sv - t + k * 255 * 12
    def neu(b, k=0, rente=False, erw=1):
        if rente:
            y = b - min(b, a * 0.85 * dA * 12) + dA * 12
            return (y - float(est_neu(np.array(y), X)) - b * 0.11 * s / SV_SATZ_ALT) / preis
        bb = b * (1 + lohn_hub)
        y = bb + dA * 12
        netto = y - bb * s / 200 - float(est_neu(np.array(y), X)) + k * dK * 12
        if erw == 2: netto += dA * 12                     # nicht erwerbstaetige/r Partner/in (steuerfrei unter GFB)
        return netto / preis
    prof = [("Rentnerin, 1.100 EUR/Monat", 13200, 0, True, False, 1),
            ("Geringverdiener, 20.000 EUR", 20000, 0, False, False, 1),
            ("Fachkraft, 42.000 EUR", 42000, 0, False, False, 1),
            ("Facharbeiter, 55.000 EUR", 55000, 0, False, False, 1),
            ("Familie, 63.000 EUR, 2 Kinder, Alleinverdiener", 63000, 2, False, True, 2),
            ("Fuehrungskraft, 150.000 EUR", 150000, 0, False, False, 1)]
    out = []
    for name, b, k, r, sp, e in prof:
        h = heute(b, k, r, sp) if not sp else heute(b, k, r, True)
        n = neu(b, k, r, e)
        out.append(dict(profil=name, heute=h, neu=n, delta=n - h, pct=(n - h) / h * 100))
    return out

if __name__ == "__main__":
    B, K, O_ = SZ["basis"], SZ["konservativ"], SZ["optimistisch"]
    out = {"kalib": K_SPLIT}
    print(f"Kalibrierfaktor Altrecht: {K_SPLIT:.3f}")

    print("\n[1] PRUEFUNG BISHERIGER STAND 25:25 PLUS (Basis)")
    out["pruefung"] = []
    for lbl, s, dd, a in [("Stufe 2: SV 28 %, DD 500/250", 28, (500, 250), 1.0),
                          ("Stufe 3: SV 18 %, DD 600/300", 18, (600, 300), 1.0)]:
        sd, E, A, _ = rechne(25, s, dd, a, B, detail=True)
        out["pruefung"].append(dict(lbl=lbl, saldo=sd, E=E, A=A))
        print(f"  {lbl:<34} {sd:+7.0f} ({sd/BIP*100:+.1f} % BIP)")

    print("\n[2] INTERPOLATION X:X, Zielbild (SV 18 %, DD 600/300, Rentensockel 100 %)")
    out["gitter"] = {}
    for X in range(25, 31):
        row = {k: rechne(X, 18, (600, 300), 1.0, SZ[k]) for k in SZ}
        out["gitter"][X] = row
        print(f"  {X}:{X}  " + "  ".join(f"{k[:5]} {v:+7.0f}" for k, v in row.items()))
    # benoetigter Einheitssatz fuer Zielbild (Extrapolation)
    for X in range(30, 61):
        if rechne(X, 18, (600, 300), 1.0, B) >= 0: break
    out["x_noetig"] = X
    print(f"  -> Zielbild waere erst bei einem Einheitssatz von ca. {X} % ausgeglichen (Basis, Extrapolation)")

    sd, E, A, info = rechne(30, 18, (600, 300), 1.0, B, detail=True)
    out["detail_ziel"] = dict(saldo=sd, E=E, A=A, info=info)

    print("\n[3] FRONT: max. finanzierbare DD (Erw., Kinder = 1/2) je SV-Satz, 30:30, Rentensockel 100 %")
    out["front"] = {}
    for s in [18, 22, 26, 30, 34, 38, 41.9]:
        r = {k: dd_max(30, s, 1.0, SZ[k], puffer=0.0) for k in SZ}
        r["basis_puffer"] = dd_max(30, s, 1.0, B, puffer=0.003)
        out["front"][s] = r
        print(f"  SV {s:>4}%: " + "  ".join(f"{k[:5]} {('%4.0f' % v) if v is not None else '  – '}" for k, v in r.items()))

    print("\n[4] FRONT je Einheitssatz (SV 38 %, Rentensockel 100 %)")
    out["front_x"] = {}
    for X in range(25, 31):
        out["front_x"][X] = {k: dd_max(X, 38, 1.0, SZ[k]) for k in SZ}
        print(f"  {X}:{X}  " + "  ".join(f"{k[:5]} {('%4.0f' % v) if v else '  – '}" for k, v in out['front_x'][X].items()))

    print("\n[5] EMPFOHLENE KONFIGURATION: 30:30, SV 38 %, Rentensockel 100 %, DD per Formel")
    out["pfade_sv"] = {}
    for s_ in (34, 41.9):
        out["pfade_sv"][s_] = {k: [r["dd"] for r in pfad(30, s_, 1.0, SZ[k])] for k in SZ}
    for k in SZ:
        pf = pfad(30, 38, 1.0, SZ[k])
        out.setdefault("pfad", {})[k] = pf
        print(f"  {k:<12} DD J1 {pf[0]['dd']:>4.0f} J5 {pf[4]['dd']:>4.0f} J10 {pf[9]['dd']:>4.0f} J20 {pf[19]['dd']:>4.0f}"
              f" | Saldo J1 {pf[0]['saldo_bip']:+.2f} J20 {pf[19]['saldo_bip']:+.2f} % | reformbed. Schuld J20 {pf[19]['schuld_bip']:+.1f} % BIP")
    pfl = pfad(30, 38, 1.0, B, dd_index="loehne")
    out["pfad_lohnindex"] = pfl
    print(f"  basis (DD lohnindexiert): DD J20 {pfl[19]['dd']:.0f}, Saldo J20 {pfl[19]['saldo_bip']:+.2f} %")

    # Detail der Endkonfiguration bei DD aus Basis-Pfad J20
    d_end = 350.0
    sd, E, A, info = rechne(30, 38, (d_end, d_end / 2), 1.0, B, detail=True)
    out["detail_empf"] = dict(saldo=sd, E=E, A=A, info=info, dd=d_end)
    print(f"  Detail bei DD {d_end:.0f}/{d_end/2:.0f} (Preise 2025): Saldo {sd:+.1f}")
    for k, v in {**E, **{('A_' + a_): b for a_, b in A.items()}}.items(): print(f"    {k:<16}{v:+8.1f}")

    print("\n[6] MISCHVARIANTEN (SV 38 %, Rentensockel 100 %): max. DD ohne Luecke (konservativ | basis)")
    out["misch"] = {}
    for lbl, X, xe, xu in [("25:25", 25, 25, 25), ("28:28", 28, 28, 28), ("30:30", 30, 30, 30),
                           ("ESt 28 | USt, Kapital, Unternehmen 30", 30, 28, 30),
                           ("ESt 30 | USt 28 | Kapital, Unternehmen 30", 30, 30, 28)]:
        def f(p):
            lo, hi = 0.0, 900.0
            if rechne(X, 38, (0, 0), 1.0, p, X_est=xe, X_ust=xu) < 0: return None
            for _ in range(22):
                mid = (lo + hi) / 2
                if rechne(X, 38, (mid, mid / 2), 1.0, p, X_est=xe, X_ust=xu) >= 0: lo = mid
                else: hi = mid
            return lo
        out["misch"][lbl] = dict(kons=f(K), basis=f(B))
        print(f"  {lbl:<42} {out['misch'][lbl]['kons'] or 0:5.0f} | {out['misch'][lbl]['basis'] or 0:5.0f}")

    out["mikro"] = {}
    for lbl, dd in (("kons", (225, 112.5)), ("basis", (400, 200))):
        print(f"\n[7] MIKRO {lbl}: 30:30, SV 38 %, DD {dd[0]:.0f}/{dd[1]:.0f}, Rentensockel 100 % (real, inkl. USt-Preiseffekt)")
        sd, E, A, info = rechne(30, 38, dd, 1.0, B, detail=True)
        mk = mikro(30, 38, dd, 1.0, info["w_neu"], info["lohn_hub"])
        out["mikro"][lbl] = mk
        for r in mk: print(f"  {r['profil']:<48}{r['heute']:>9,.0f}{r['neu']:>9,.0f}{r['delta']:>+9,.0f} ({r['pct']:+.0f} %)")

    json.dump(out, open("/home/claude/ergebnisse.json", "w"), default=float, indent=1)
