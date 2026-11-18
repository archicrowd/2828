#!/usr/bin/env python3
"""Szenario 38: vorgeschlagene neue Regeln mit einheitlichem Satz 38 % (Logbuch v4.101). Prüfrechnung, ändert die geltende Rechnung nicht.

Regeln (szenario38.toml): Satz 38 % (Label fest), Regel L (Lenkungsabgaben an den Fonds, Dividende erhält die barwertgleiche Konstante),
Puffer 0,5 % BIP, Glättung (Dividende real +1 % je Jahr, Rücklage), Altersausgleich R4 (neu geeicht bei 38 %), CO₂ nach K2.
Rechenweg:
  1. Rentner (rentner_eichung): Altersausgleich so geeicht, dass das Mittel wieder −109 € beträgt; Kosten = Ausgleich + Mehr an Aufstockung.
  2. Makro (quote_optimum.pfad): Dividendenpfad 2028–2060 mit Zusatzausgaben (R4, CO₂, Mehrkosten Grundauskommen); Glättung → Startwert D0.
  3. Haushalte 2028 (mikro_de, regel_boden): Tarif × 38/33⅓, Dividende D0, Zuschlag nach Szenario; Rückwirkung der Dividende auf das Netz
     (Aufstockung bis zum Grundbedarf) über netz33 je Jahr; Mikrosimulation nur zur Verteilung.
Ausgabe: daten/aggregate/szenario38.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path
import numpy as np

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "szenario38.toml").read_text(encoding="utf-8"))


def lade(name, datei):
    spec = importlib.util.spec_from_file_location(name, W / "modell" / datei)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


QO = lade("qo", "quote_optimum.py")
RE = lade("re", "rentner_eichung.py")
MD = lade("md", "mikro_de.py")
S0 = QO.S0
G = P["glaettung_wachstum"]
BIP = P["bip_2028_kaufkraft_2026_mrd"]


# ------------------------------------------------------------------ Makro
netz_korrektur, fixpunkt = QO.netz_korrektur, QO.fixpunkt


def makro(extra):
    sy = QO.system(P["satz"], not P["label_fest"])
    r = QO.pfad(sy, P["regel"], P["puffer_pct_bip"], extra, mit_reihe=True)
    reihe = r.pop("reihe")

    def lauf(d0):
        rl, ok, out = 0.0, True, []
        for x in reihe:
            d = d0 * (1 + G) ** (x["jahr"] - 2028)
            frei = x["div"] + netz_korrektur(x["jahr"], d)
            rl += frei - d / x["eur_je_punkt"]
            ok &= rl >= -1e-9
            out.append(dict(jahr=x["jahr"], dividende_eur=round(d), dividende_pct_bip=round(d / x["eur_je_punkt"], 2), rest_mit_netz_pct_bip=round(frei, 2),
                            ruecklage_pct_bip=round(rl, 2), steuern_pct_bip=round(x["steuern"], 2),
                            ohne_glaettung_eur=round(fixpunkt(x["div"], x["eur_je_punkt"], x["jahr"]))))
        return ok, out
    lo, hi = 0.0, 1000.0
    for _ in range(40):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if lauf(m)[0] else (lo, m)
    return lo, r, lauf(lo)[1]


def zuschlag_faktor(r_s):
    g = QO.pfad(QO.system(S0, False), "0", QO.V["punkte"]["2028"]["saldo"])
    return r_s["zuschlag_pct"] / g["zuschlag_pct"], g


# ------------------------------------------------------------------ Szenario in die Haushaltsmodelle setzen
BASIS = dict(tc=list(MD.TARIF_C), div=MD.DIV, zu=MD.ZU, mr_zu=MD.MR.ZU, sl_zu=MD.SL.P["zuschlag_de"],
             d28=MD.HL.LS["staaten"]["DE"]["dividende_erw_eur"][0], mr_tc=list(MD.MR.TARIF_C), sl_tc=list(MD.SL.TARIF_C))


def setze(d0=None, f=1.0, k=1.0):
    tc = [x * k for x in BASIS["tc"]]
    MD.TARIF_C = tc
    MD.MR.TARIF_C = [x * k for x in BASIS["mr_tc"]]
    MD.SL.TARIF_C = [x * k for x in BASIS["sl_tc"]]
    d = BASIS["d28"] if d0 is None else d0
    MD.DIV = BASIS["div"] * d / BASIS["d28"]
    MD.HL.LS["staaten"]["DE"]["dividende_erw_eur"][0] = d
    MD.ZU, MD.MR.ZU, MD.SL.P["zuschlag_de"] = BASIS["zu"] * f, BASIS["mr_zu"] * f, BASIS["sl_zu"] * f


POP = {}


def mikro():
    if not POP:
        hh, rr, st, sb = MD.ziehe(MD.P["seeds"][0], MD.P["partner"]["basis_korrelation"])
        w, wr, _ = MD.eiche(hh, rr, st, sb)
        POP.update(hh=hh, rr=rr, w=w, wr=wr)
    wg = MD.P["szenarien"]["basis_weitergabe"]
    a = MD.auswerten(MD.rechne(POP["hh"], POP["rr"], POP["w"], POP["wr"], [wg]), wg)
    kurz = lambda x: dict(mit_mehr_pct=x["anteil_mehr_haushalte_pct"], mittel_eur=x["mittel_mehr_monat_eur"])
    return dict(gesamt=kurz(a["gesamt"]), erwerbsfaehige=kurz(a["erwerbsfaehige_haushalte"]),
                status={n: kurz(v) for n, v in a["status"].items()}, haushaltstyp={n: kurz(v) for n, v in a["haushaltstyp"].items()},
                dezile=[dict(dezil=x["dezil"], mit_mehr_pct=x["anteil_mehr_haushalte_pct"], mittel_eur=x["mittel_mehr_monat_eur"]) for x in a["dezile"]],
                armut=a["armut"], grundauskommen_mrd=a["kosten_mrd"]["grundauskommen_neu"])


def beispiele():
    RB, SL = MD.RB, MD.SL
    out = {}
    for b in (20000, 30000, 42000, 60000, 90000, 150000):
        out[str(b)] = {n: round((RB.neu("DE", b, e, kk) - SL.heute("DE", b, e, kk)) / 12) for n, e, kk in SL.HAUSHALTE}
    out["anteil_mit_mehr_pct"] = RB.anteile("DE")
    return out


# ------------------------------------------------------------------ Rentner
def rentner(k, f):
    R, gw = RE.M.ziehe(np.random.default_rng(RE.PK["seed"]), RE.PK["stichprobe"], 18.0, 6.3)
    pre = [(RE.M.brutto_aus_netto(r["netto_2024"] * 1.06 / r["n"], RE.A), max(r["netto_2024"] * 1.06, RE.M.bedarf_heute(r["n"])), r["n"], r["eps"]) for r in R]
    hs = np.array([h for _, h, _, _ in pre])
    grp = np.searchsorted(np.quantile(hs, [.2, .4, .6, .8]), hs)
    kk = dict(RE.NEU, zu=RE.NEU["zu"] * f, saetze=[x * k for x in RE.NEU["saetze"]])

    def lauf(kx, aus):
        x = [RE.netto(g, n, e, RE.BS, aus, kx) for g, h, n, e in pre]
        d = np.array([(y - h) / 12 for (y, _, _), (_, h, _, _) in zip(x, pre)])
        bo = float(sum(wi * a for wi, (_, a, _) in zip(gw, x))) / 1e9
        au = float(sum(wi * 12 * aus * n for wi, (_, _, n, _) in zip(gw, pre))) / 1e9
        return dict(mit_mehr_pct=round(float(gw[d > 0].sum() / gw.sum() * 100), 1), mittel_eur=round(float(np.average(d, weights=gw))),
                    fuenftel_eur=[round(float(np.average(d[grp == i], weights=gw[grp == i]))) for i in range(5)], boden_mrd=bo, ausgleich_mrd=au)
    geltend = lauf(RE.NEU, 0.0)
    ohne = lauf(kk, 0.0)
    lo, hi = 0.0, 400.0
    for _ in range(40):
        m = (lo + hi) / 2
        (lo, hi) = (m, hi) if lauf(kk, m)["mittel_eur"] < P["rentner_ziel_mittel"] else (lo, m)
    mit = lauf(kk, (lo + hi) / 2)
    kosten = mit["ausgleich_mrd"] + mit["boden_mrd"] - geltend["boden_mrd"]
    rund = lambda d: {k_: (round(v, 1) if isinstance(v, float) else v) for k_, v in d.items()}
    return dict(geltend=rund(geltend), satz38_ohne_ausgleich=rund(ohne), satz38_mit_r4=rund(mit), ausgleich_person_monat=round((lo + hi) / 2),
                kosten_mrd=round(kosten, 1), kosten_pct_bip=round(kosten / BIP * 100, 2))


def main():
    k = P["satz"] / S0
    # geltend (Bezug)
    setze()
    m_geltend, b_geltend = mikro(), beispiele()
    # Zuschlag des Szenarios (aus einem ersten Makrolauf)
    _, r0, _ = makro(P["co2_k2_pct_bip"])
    f, g_ref = zuschlag_faktor(r0)
    rt = rentner(k, f)
    extra = P["co2_k2_pct_bip"] + rt["kosten_pct_bip"]
    d0, r, pfad = makro(extra)                 # Rückwirkung der Dividende auf das Netz über netz33 (geltender Rechenweg)
    setze(d0, f, k)
    m = mikro()
    d_ga = (m["grundauskommen_mrd"] - m_geltend["grundauskommen_mrd"]) / BIP * 100   # nur zur Information (Mikrosimulation, alle Haushalte)
    verlauf = []
    b = beispiele()
    # Gegenprobe: geltende Regeln über denselben Weg (Rest mit Netz-Rückwirkung, ohne Glättung) gegen netz33.json (245 € 2028)
    gp = QO.pfad(QO.system(S0, False), "0", QO.V["punkte"]["2028"]["saldo"], 0.0, mit_reihe=True)["reihe"]
    gegenprobe = {str(x["jahr"]): round(fixpunkt(x["div"], x["eur_je_punkt"], x["jahr"])) for x in gp if x["jahr"] in (2028, 2035, 2050, 2060)}
    setze()                                                     # zurücksetzen
    d0_st, r_st, pfad_st = makro(extra + P["staatsebene_pct_bip"])
    QO.PJ.sy.clear(); QO.PJ.sy.update(QO.BASIS33); QO.PJ._PROG.clear()
    sel = lambda pf: {str(x["jahr"]): x for x in pf if x["jahr"] in (2028, 2030, 2035, 2040, 2045, 2050, 2055, 2060)}
    E = dict(version=P["version"], status="Prüfrechnung (Auftrag 18.11.2026); geltende Rechnung unverändert", regeln=dict(
        satz=P["satz"], label="fest 7/13/19/27 + Sonderstufe ein Drittel", regel=P["regel"], puffer_pct_bip=P["puffer_pct_bip"], glaettung=G,
        co2="K2", rentner="R4 neu geeicht"),
        makro=dict(steuern_2028=r["steuern_2028"], steuern_2060=r["steuern_2060"], fondsbeitrag=QO.FONDS, zuschlag_pct=r["zuschlag_pct"],
                   effektiver_spitzensatz=r["effektiver_spitzensatz"], lenkung_konstante=r["lenkung_konstante"],
                   last_steuern_fonds_2028=r["last_steuern_und_fonds_2028"], pflichtvorsorge=QO.GL["pflichtvorsorge_route"],
                   last_mit_pflichtvorsorge_2028=round(r["last_steuern_und_fonds_2028"] + QO.GL["pflichtvorsorge_route"], 2),
                   geltend=dict(steuern_2028=g_ref["steuern_2028"], zuschlag_pct=g_ref["zuschlag_pct"], effektiver_spitzensatz=g_ref["effektiver_spitzensatz"],
                                dividende_eur=g_ref["dividende_eur2026"]),
                   zusatzausgaben_pct_bip=dict(co2_k2=P["co2_k2_pct_bip"], rentner_r4=rt["kosten_pct_bip"]),
                   info_mehrkosten_grundauskommen_mikro_pct_bip=round(d_ga, 2), gegenprobe_geltend_netz33_eur=gegenprobe),
        dividende=dict(d0_eur=round(d0), pfad=sel(pfad), ruecklage_hoechst_pct_bip=max(x["ruecklage_pct_bip"] for x in pfad),
                       ),
        mit_staatsebene=dict(d0_eur=round(d0_st), pfad=sel(pfad_st)),
        rentner=rt, haushalte_mikro=dict(geltend=m_geltend, szenario38=m), beispiele=dict(geltend=b_geltend, szenario38=b),
        hinweis="Euro je Monat, 2028, Kaufkraft 2026, Deutschland. Rentner aus rentner_eichung (BS35), übrige Haushalte aus mikro_de (eine Ziehung, "
                "Weitergabe 80 %); die Rentnerzeilen in mikro_de enthalten R4 nicht. Haushaltsrechnungen ohne CO₂-Kosten (B-4). Mehrkosten des "
                "Netzes (Aufstockung bis zum Grundbedarf) über netz33 je Jahr mit der gezahlten Dividende; Mikrosimulation nur zur Information.")
    (AGG / "szenario38.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(dict(makro=E["makro"], d0=E["dividende"]["d0_eur"], staat=E["mit_staatsebene"]["d0_eur"]), ensure_ascii=False))
    for j, x in E["dividende"]["pfad"].items():
        print(j, x)
    print("Rentner", {kk: v for kk, v in rt.items()})
    for n in ("geltend", "szenario38"):
        mm = E["haushalte_mikro"][n]
        print(n, mm["gesamt"], mm["erwerbsfaehige"], mm["grundauskommen_mrd"], [ (x["mit_mehr_pct"], x["mittel_eur"]) for x in mm["dezile"]])
        print("  status", {s: v for s, v in mm["status"].items()})
        print("  typ", mm["haushaltstyp"])
        print("  bsp", E["beispiele"][n])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
