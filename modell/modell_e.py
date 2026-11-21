#!/usr/bin/env python3
"""Modell E näher betrachtet (Logbuch v4.104). Prüfrechnung, ändert die geltende Rechnung nicht.

1. Dividendenpaket: Gesamtwert = Baranteil + Wert des steuerfinanzierten Netzes je Einwohner (X). Baranteil Erwachsene = D × topf, Kinder
   = 0,8 × D × topf (regel_boden). Mindestens 100 € bar je Erwachsenem und Kind.
2. Eigene Dynamik von E (Kanäle wie dynamik_geltend; Arbeit ein Drittel, Investition wie 38 %, Bürokratie 40 %, KI-Trend, Fachkräfte mit Netto E,
   Nachfrage aus mikro_de mit Baranteil E abzüglich nicht enthaltener Lasten), Fonds bis 2125 mit der Dividende von E.
3. Stabilität: Dividende als fester Anteil am Grundbedarf mit Rücklage; Fortschrittsregel; Stresstests (Zins, KI, Rezession, Boden, Ausweichen).
Ausgabe: daten/aggregate/modell_e.json
"""
import contextlib, importlib.util, io, json, math, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "modell_e.toml").read_text(encoding="utf-8"))


def lade(name, datei):
    spec = importlib.util.spec_from_file_location(name, W / "modell" / datei)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


ST = lade("st_e", "stellschrauben.py")
DS, QO, DGM, NZ = ST.DS, ST.QO, ST.DGM, ST.NZ
S38, MD = DS.S38, DS.MD
JAHRE = list(range(2028, 2061))
I = DGM.I
S = MD.RB.S
TOPF = MD.RB.topf(S)
r2 = lambda x: round(x, 2)
SCHRAUBEN = ST.schrauben()


def boden_mit_r(tau, r):
    alt = ST.P["boden"]["r"]
    ST.P["boden"]["r"] = r
    try:
        return ST.boden(tau)
    finally:
        ST.P["boden"]["r"] = alt


def ki_ln(pp):
    out, l = {}, 0.0
    for j in range(2028, 2099):
        if j > 2028:
            l += math.log(1 + ((pp if j <= 2040 else pp / 2) if j <= 2060 else 0.0) / 100)
        out[j] = l
    return out


@__import__("functools").lru_cache(maxsize=None)
def kapital_faktor(ks):
    """v4.106: Mehraufkommen bei einheitlichem Satz ks auf Kapitalerträge, Unternehmen, Erbschaft im Verhältnis zu 38 %."""
    with contextlib.redirect_stdout(io.StringIO()):
        return ST.kapital(ks)[0] / ST.kapital(P["kapital_satz"])[0]


def dynamik_e(d_bar, ki_pp, mehr_hh, ks=None):
    D = P["dynamik"]
    ks = P["kapital_satz"] if ks is None else ks
    # Eingaben
    e97 = ST.E97
    av = e97["arbeitsvolumen_pct"] + DGM.P["beschaeftigung"]["einkommenseffekt_dividende_pct"] * (d_bar / D["einkommenseffekt_bezug_eur"] - 1)
    inv = DS.P["investition_mittel"] * ((ks - DS.P["satz_heute_kapital"]) + (ks - DS.P["satz_heute_gewinne"])) / (
        (ST.QO.S0 - DS.P["satz_heute_kapital"]) + (ST.QO.S0 - DS.P["satz_heute_gewinne"]))
    S38.setze(d_bar)
    dln = math.log(MD.RB.neu("DE", DS.P["brutto_fachkraft"], 1, 0) / MD.SL.heute("DE", DS.P["brutto_fachkraft"], 1, 0))
    S38.setze()
    L = D["lasten_haushalte"]
    sw = {n: SCHRAUBEN[n]["wirkung"][2028] for n in P["stellschrauben"]}
    last = L["boden"] * sw["Boden 2.0 %"] + L["kapital"] * sw["Kapital 38 %"] * kapital_faktor(ks) + L["subventionen"] * sw["Subventionen mittel"] + L["co2"] * ST.P["co2"]["k3_minus_k2_2028"]
    impuls = DS.P["impuls_bezug_pct_bip"] * mehr_hh / DS.P["mehr_bezug_eur"] - last
    alt_b = DGM.P["buerokratie"]["anteil_abgebaut"][I]
    DGM.P["buerokratie"]["anteil_abgebaut"][I] = D["buerokratie_anteil"]
    reihe, _ = DS.dynamik(impuls, dln, av, inv)
    DGM.P["buerokratie"]["anteil_abgebaut"][I] = alt_b
    k = ki_ln(ki_pp)
    for j, r in reihe.items():
        f = math.exp(k.get(j, k[max(k)]))
        r["dy"] = (1 + r["dy"]) * f - 1
        r["kopf"] = r["kopf"] * f
        r["kanaele"]["KI"] = (f - 1) * 100
    return reihe, dict(impuls_pct_bip=r2(impuls), arbeitsvolumen_pct=r2(av), investition_pct_bip=r2(inv), dln_netto_fachkraefte=round(dln, 3),
                       lasten_nicht_in_mikro_pct_bip=r2(last))


def basis(reihe):
    DS.setze_dynamik(reihe)
    r = QO.pfad(QO.system(QO.S0, False), P["regel"], P["puffer_pct_bip"], 0.0, mit_reihe=True)
    return {x["jahr"]: x for x in r["reihe"]}, r


def ziel_eur(j, a):
    return a * ST.GB26 / 12 * NZ.R[j]["wachstum_je_kopf_faktor"] ** NZ.LA


def extra_e(stress):
    ex = {j: 0.0 for j in JAHRE}
    for n in P["stellschrauben"]:
        w = SCHRAUBEN[n]["wirkung"]
        for j in JAHRE:
            v = w[j]
            if n == "Boden 2.0 %" and "boden_r" in stress:
                v = boden_mit_r(0.020, stress["boden_r"])
            if n == "Boden 2.0 %" and "boden_einschleifen_bis" in stress:     # v4.105: linear von heute bis 2 % im Zieljahr
                v *= min(1.0, (j - 2027) / (stress["boden_einschleifen_bis"] - 2027))
            if n == "Kapital 38 %" and "kapital_satz" in stress:           # v4.106: einheitlicher Satz auf alle Einkommensarten außer Arbeit
                v *= kapital_faktor(stress["kapital_satz"])
            if n == "Kapital 38 %" and "kapital_ausweichen" in stress:
                v *= stress["kapital_ausweichen"]
            ex[j] += v
    kv = P["dynamik"]["kapital_verschiebung_pp"] if stress.get("ki_pp", P["dynamik"]["ki_pp"]) > 0 else 0.0
    for j in JAHRE:                                    # Verschiebung zu Kapital (Teil des KI-Trends, Aufkommen)
        ex[j] += kv * (j - 2028) / 32 * (ST.P["ki"]["belastung_kapital"] - ST.P["ki"]["belastung_arbeit"])
    if "schock_jahr" in stress:
        sj = stress["schock_jahr"]
        ex[sj] -= stress["schock_netz"]
    for j in JAHRE:                                    # v4.105: zusätzliche Ausgaben je Jahr (Altersausgleich, Stundung)
        ex[j] -= stress.get("ausgaben", {}).get(j, 0.0)
    return ex


def schock_ln(stress):
    out = {j: 0.0 for j in JAHRE}
    if "schock_jahr" in stress:
        sj, s = stress["schock_jahr"], stress["schock_bip"]
        for j in JAHRE:
            if sj <= j <= sj + 3:
                out[j] = math.log(1 + s * (1 - (j - sj) / 3))
    return out


def fonds(div28, dy, zins=None):
    B = DGM.AL["beschluss"]
    alt = B["zins"]
    if zins is not None:
        B["zins"] = zins
    try:
        c, sp = ST.fonds_c(div28, dy, P["fonds_zieljahr"])
    finally:
        B["zins"] = alt
    return c, sp


def rechne(stress=None, mit_regel=True):
    stress = stress or {}
    ki = stress.get("ki_pp", P["dynamik"]["ki_pp"])
    # Fixpunkt: Baranteil ↔ Nachfrageimpuls ↔ Dynamik
    d_bar, mehr = 330.0, 214.0
    for _ in range(5):
        reihe, ein = dynamik_e(d_bar, ki, mehr, stress.get("kapital_satz"))
        B, rb = basis(reihe)
        dy = {j: r["dy"] for j, r in reihe.items()}
        ex = extra_e(stress)
        sch = schock_ln(stress)

        def bil(a):
            d28 = ziel_eur(2028, a) / B[2028]["eur_je_punkt"]
            c, sp = fonds(d28, dy, stress.get("zins"))
            ent = QO.FONDS * (1 - c / ST.C_G)
            out = {}
            for j in JAHRE:
                x = B[j]
                bed = ziel_eur(j, a) * math.exp(-(1 - NZ.LA) * sch[j]) / x["eur_je_punkt"]
                frei = x["div"] + QO.netz_korrektur(j, ziel_eur(j, a)) + ent + ex[j]
                out[j] = frei - bed
            return out, ent, sp, c

        lo, hi = 0.0, 1.0
        for _ in range(22):
            m = (lo + hi) / 2
            b, *_ = bil(m)
            rl, ok = 0.0, True
            for j in JAHRE:
                rl += b[j]
                ok &= rl >= -1e-9
            lo, hi = (m, hi) if ok else (lo, m)
        a0 = stress.get("anteil_fest", lo)               # v4.105: fester Anteil (Beschluss 30 %) statt des größten tragbaren
        d_neu = ziel_eur(2028, a0) * TOPF
        S38.setze(ziel_eur(2028, a0))
        mehr_alt, mehr = mehr, S38.mikro()["gesamt"]["mittel_eur"]
        S38.setze()
        if abs(d_neu - d_bar) < 2 and abs(mehr - mehr_alt) < 5:   # Korrektur 98: auch der Impuls muss zum Baranteil passen
            d_bar = d_neu
            break
        d_bar = d_neu
    b, ent, sp, c = bil(a0)
    # Fortschrittsregel
    F = P["fortschritt"]
    a, rl, ueber, pfad = a0, 0.0, 0, []
    bil_cache = {}
    for j in JAHRE:
        ak = round(a, 3)
        if ak not in bil_cache:
            bil_cache[ak] = bil(ak)[0]
        rl += bil_cache[ak][j]
        ueber = ueber + 1 if rl > F["ziel_ruecklage_pct_bip"] else 0
        if mit_regel and ueber >= F["jahre_ueber"] and a < F["hoechst"]:     # solange die Rücklage über dem Ziel liegt: jedes Jahr +1 Punkt
            a = min(F["hoechst"], a + F["schritt"])
        pfad.append(dict(jahr=j, anteil_pct=round(a * 100, 1), ruecklage_pct_bip=r2(rl)))
    # Paket: Bar + Netz je Einwohner
    paket = {}
    for j in (2028, 2035, 2045, 2060):
        a_j = next(p["anteil_pct"] for p in pfad if p["jahr"] == j) / 100
        d = ziel_eur(j, a_j)
        alt = NZ.R[j]
        NZ.R[j] = dict(alt, dividende_erw_eur2026=d)
        pos, _ = NZ.netz(j, QO.K_B, False, QO.GR_B)
        NZ.R[j] = alt
        netz = sum(pos.values()) - P["gesundheit_digital"] * pos["Gesundheit (Grundversorgung)"]
        x_eur = netz / 100 * NZ.KOPF26 * NZ.R[j]["wachstum_je_kopf_faktor"] / 12
        bar_e, bar_k = d * TOPF, d * S * TOPF
        paket[str(j)] = dict(anteil_grundbedarf_pct=round(a_j * 100, 1), bar_erwachsen=round(bar_e), bar_kind=round(bar_k), netz_x_je_einwohner=round(x_eur),
                             gesamt_erwachsen=round(bar_e + x_eur), gesamt_kind=round(bar_k + x_eur), netz_pct_bip=r2(netz),
                             halber_grundbedarf=round(ziel_eur(j, 0.5)), mindest_bar_erfuellt=min(bar_e, bar_k) >= P["bar_mindest_eur"])
    dyn = {str(j): dict(bip_pct=r2(reihe[j]["dy"] * 100), je_kopf_pct=r2((reihe[j]["kopf"] - 1) * 100),
                        kanaele={k: r2(v) for k, v in reihe[j]["kanaele"].items()}) for j in (2028, 2030, 2035, 2045, 2060)}
    rmin = min(p["ruecklage_pct_bip"] for p in pfad)
    DS.zuruecksetzen()
    return dict(eingaben=ein, dynamik=dyn, anteil_stabil_pct=round(a0 * 100, 1), anteil_tragbar_pct=round(lo * 100, 1), paket=paket, fortschritt=[p for p in pfad if p["jahr"] in (2028, 2030, 2035, 2040, 2045, 2050, 2055, 2060)],
                ruecklage_min_pct_bip=rmin, ruecklage_max_pct_bip=max(p["ruecklage_pct_bip"] for p in pfad),
                fonds=dict(beitrag_eigen_pct_bip=r2(QO.FONDS * c / ST.C_G), an_dividende_pct_bip=r2(ent), schuld_spitze_pct_bip=round(sp)),
                steuern_2028=rb["steuern_2028"])


def main():
    basis_e = rechne()
    st = P["stress"]
    stress = {
        "Fondszins 3,0 %": dict(zins=st["zins"][0]),
        "Fondszins 3,5 %": dict(zins=st["zins"][1]),
        "ohne KI-Trend": dict(ki_pp=0.0),
        f"Rezession {st['schock_jahr']} (BIP −4 %)": dict(schock_jahr=st["schock_jahr"], schock_bip=st["schock_bip"], schock_netz=st["schock_netz"]),
        "Bodenrendite 2 %": dict(boden_r=st["boden_r"]),
        "Kapital: halbes Mehraufkommen": dict(kapital_ausweichen=st["kapital_ausweichen"]),
        "alles zusammen (Zins 3,0, ohne KI, Boden 2 %, Ausweichen)": dict(zins=st["zins"][0], ki_pp=0.0, boden_r=st["boden_r"], kapital_ausweichen=st["kapital_ausweichen"]),
    }
    sres = {}
    for n, s in stress.items():
        r = rechne(s)
        sres[n] = dict(anteil_stabil_pct=r["anteil_stabil_pct"], bar_2028=r["paket"]["2028"]["bar_erwachsen"], bar_kind_2028=r["paket"]["2028"]["bar_kind"],
                       anteil_2060_mit_regel_pct=r["paket"]["2060"]["anteil_grundbedarf_pct"], bar_2060=r["paket"]["2060"]["bar_erwachsen"],
                       fonds_spitze_pct_bip=r["fonds"]["schuld_spitze_pct_bip"], mindest_bar_erfuellt=all(p["mindest_bar_erfuellt"] for p in r["paket"].values()),
                       bip_2045_pct=r["dynamik"]["2045"]["bip_pct"])
    # Vergleich: geltend als Paket
    g = json.loads((AGG / "netz33.json").read_text(encoding="utf-8"))["beschluss"]["reihe"]
    geltend = {str(x["jahr"]): dict(bar_erwachsen=round(x["dividende_erw_eur2026"] * TOPF), bar_kind=round(x["dividende_erw_eur2026"] * S * TOPF),
                                    netz_x_je_einwohner=x["netz_eur_kopf_monat"], gesamt_erwachsen=round(x["dividende_erw_eur2026"] * TOPF + x["netz_eur_kopf_monat"]))
               for x in g if x["jahr"] in (2028, 2035, 2045, 2060)}
    E = dict(version=P["version"], status="Prüfrechnung (Auftrag 21.11.2026); geltende Rechnung unverändert", modell_e=basis_e, stress=sres, geltend_als_paket=geltend,
             kinderanteil=S, topf=round(TOPF, 3),
             hinweis="Euro je Monat, Kaufkraft 2026, Deutschland. Gesamtwert = Baranteil + Netz je Einwohner (Durchschnitt; Versicherungswert, keine Auszahlung). "
                     "Bar Erwachsene = Dividende × topf (Kinderanteil 0,8). Stellschrauben und Kanäle überwiegend Annahmen (stellschrauben.toml, modell_e.toml).")
    (AGG / "modell_e.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("E", {k: v for k, v in basis_e.items() if k not in ("dynamik",)})
    print("Dynamik", {j: (v["bip_pct"], v["kanaele"]) for j, v in basis_e["dynamik"].items()})
    for n, x in sres.items():
        print(n, x)
    print("geltend", geltend)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
