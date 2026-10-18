#!/usr/bin/env python3
"""Haushalte heute gegen Goldenes Drittel je Referenzland der Sprachversionen (FR, IT, ES, PL; Logbuch v4.2). Prüfrechnung, vereinfacht.

Heute: vereinfachtes Steuer- und Abgabenmodell nach Recht 2026 (Parameter und Quellen: heute_laender.toml) für Beschäftigte mit einem Einkommen:
  Frankreich  cotisations salariales, CSG/CRDS, impôt sur le revenu mit quotient familial (Plafond), décote, prime d'activité, allocations familiales
  Italien     contributi INPS, IRPEF mit detrazioni lavoro e coniuge, cuneo fiscale (somma esente, ulteriore detrazione), trattamento integrativo,
              addizionali, assegno unico
  Spanien     cotizaciones a la Seguridad Social, IRPF mit reducción por rendimientos del trabajo, mínimos, tributación conjunta
  Polen       składki ZUS, składka zdrowotna, PIT mit kwota wolna, wspólne rozliczenie, ulga na dzieci, 800+
Nicht enthalten: Wohnbeihilfen, Mindestsicherung (RSA, ADI, IMV, zasiłek), regionale Sonderregeln, Verhaltensänderungen. Weitere Erwachsene ohne Einkommen.
Neu: wie modell/haushalte33.py neu(), mit den Größen des Landes (laenderseiten.json: Grundbedarf, Dividende, Zuschlag des eigenen Fonds).
Prüfung: Einkommensteuer und Sozialbeiträge bei 100 % des Durchschnittslohns (Alleinstehend) gegen OECD Taxing Wages 2025 (Daten 2024).
Ausgabe: daten/aggregate/heute_laender.json (Raster für die Webseite, Prüftabelle, Anteile mit mehr Geld)
"""
import json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "heute_laender.toml").read_text(encoding="utf-8"))
LS = json.loads((AGG / "laenderseiten.json").read_text(encoding="utf-8"))
PJ = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))
HH = json.loads((AGG / "haushalte33.json").read_text(encoding="utf-8"))
JAHRE = LS["jahre"]
EFF_NEU = {r["jahr"]: r["label_effektiv"] for r in PJ["reihe"]}
VERT_DE = [(6, 8000), (11, 20000), (12, 36000), (7, 52000), (5, 69000), (3, 105000), (1, 300000)]   # Kernmodell DE (Mio. Personen, Brutto)


def stufen(x, grenzen, saetze):
    s, u = 0.0, 0.0
    for g, p in zip(list(grenzen) + [float("inf")], saetze):
        if x > u:
            s += (min(x, g) - u) * p / 100
        u = g
    return s


# ---------------- Frankreich
F = P["fr"]


def fr_ag(b):
    a, smic, pss = F["ag_satz"], F["smic"], F["pss"]
    r = b / smic if smic else 9
    s = (a["maladie_red"] if r <= F["ag_schwellen_smic"]["maladie_red"] else a["maladie"]) + (a["af_red"] if r <= F["ag_schwellen_smic"]["af_red"] else a["af"])
    s += a["vieillesse_deplaf"] + a["at"] + a["csa"] + a["formation"] + a["apprentissage"] + a["mobilite"] + a["peec"]
    x = b * s / 100 + min(b, 4 * pss) * a["chomage_ags"] / 100 + min(b, pss) * (a["vieillesse_plaf"] + a["fnal"] + a["agirc_t1"]) / 100
    x += max(0.0, min(b, 8 * pss) - pss) * a["agirc_t2"] / 100
    g = F["rgdu"]
    if 0 < b < g["bis_smic"] * smic:
        c = g["tmin"] + g["tdelta"] * (0.5 * (g["bis_smic"] * smic / max(b, smic) - 1)) ** g["p"]
        x -= c * b
    return max(0.0, x)   # die Reduktion kann die Beiträge nicht übersteigen


def fr_ir_brut(r, parts):
    return stufen(r / parts, F["ir_grenzen"], F["ir_saetze"]) * parts


def fr_heute(b, e, k):
    pss = F["pss"]
    sv = b * F["an_vieillesse_deplaf"] / 100 + min(b, pss) * (F["an_vieillesse_plaf"] + F["an_agirc_t1"]) / 100 \
        + max(0.0, min(b, 8 * pss) - pss) * F["an_agirc_t2"] / 100
    csg = 0.9825 * b * F["csg_crds"] / 100
    net = b - sv - csg
    imposable = b - sv - 0.9825 * b * F["csg_deduct"] / 100
    ab = min(max(imposable * F["abattement"][0], F["abattement"][1]), F["abattement"][2])
    r = max(0.0, imposable - ab)
    couple = e >= 2
    base = 2.0 if couple else 1.0
    parts = base + 0.5 * min(k, 2) + 1.0 * max(k - 2, 0) + (0.5 if (not couple and k > 0) else 0.0)
    ir_base, ir_parts = fr_ir_brut(r, base), fr_ir_brut(r, parts)
    demi = round((parts - base) * 2)
    cap = F["qf_plafond"] * demi if couple or k == 0 else F["qf_parent_isole"] + F["qf_plafond"] * max(demi - 2, 0)
    ir = max(ir_parts, ir_base - cap)
    s, m = F["decote"]["couple"] if couple else F["decote"]["seul"]
    if ir < s:
        ir = max(0.0, ir - max(0.0, m - F["decote"]["taux"] * ir))
    # allocations familiales (ab dem 2. Kind), monatlich
    af = 0.0
    if k >= 2:
        af = F["af"]["zwei"] if k == 2 else F["af"]["drei"] + F["af"]["weitere"] * (k - 3)
        af *= 1.0 if r <= F["af"]["grenze1"] else 0.5 if r <= F["af"]["grenze2"] else 0.25
    # prime d'activité, monatlich
    pa = F["pa"]
    pers = e + k
    mf = pa["mf"] * (1 + 0.5 * min(pers - 1, 1) + 0.3 * min(max(pers - 2, 0), 2) + 0.4 * max(pers - 4, 0))
    rm, smic_m = net / 12, F["smic"] / 12
    bon = pa["bonif_max"] * min(1.0, max(0.0, (b / 12 - pa["bonif_ab_smic"] * smic_m) / ((pa["bonif_voll_smic"] - pa["bonif_ab_smic"]) * smic_m)))
    prime = mf + pa["taux"] * rm + bon - (rm + af)
    prime = prime if prime >= pa["seuil"] else 0.0
    return dict(netto=net - ir + 12 * (af + prime), est=ir, sv=sv + csg, steuer_oecd=ir + csg, sv_oecd=sv)


# ---------------- Italien
I = P["it"]


def it_ag(b):
    return b * I["ag_satz"] / 100


def it_detr_lavoro(r):
    if r <= 15000:
        d = 1955.0
    elif r <= 28000:
        d = 1910 + 1190 * (28000 - r) / 13000
    elif r <= 50000:
        d = 1910 * (50000 - r) / 22000
    else:
        d = 0.0
    return d + (65 if 25000 < r <= 35000 else 0)


def it_heute(b, e, k):
    ssc = b * I["inps_an"] / 100 + max(0.0, b - I["inps_an_zusatz"][0]) * I["inps_an_zusatz"][1] / 100
    r = b - ssc
    lorda = stufen(r, I["irpef_grenzen"], I["irpef_saetze"])
    det = it_detr_lavoro(r)
    if e >= 2:
        det += 800 - 110 * r / 15000 if r <= 15000 else 690 if r <= 40000 else max(0.0, 690 * (80000 - r) / 40000)
    a, b1, c1, amt = I["cuneo_detrazione"]
    det += amt if a < r <= b1 else amt * (c1 - r) / (c1 - b1) if b1 < r <= c1 else 0.0
    irpef = max(0.0, lorda - det)
    add = r * I["addizionali"] / 100
    esente = next((b * p / 100 for g, p in I["cuneo_esente"] if b <= g), 0.0)
    lo, hi, ti = I["trattamento_integrativo"]
    tratt = ti if lo < r <= hi else 0.0
    au = 0.0
    if k > 0:
        isee = (r - irpef - add) / I["scala_isee"][min(e + k - 1, len(I["scala_isee"]) - 1)]
        q = I["assegno_unico"]
        mon = q["max"] if isee <= q["isee_max"] else q["min"] if isee >= q["isee_min"] else \
            q["max"] - (q["max"] - q["min"]) * (isee - q["isee_max"]) / (q["isee_min"] - q["isee_max"])
        au = 12 * mon * k
    return dict(netto=b - ssc - irpef - add + esente + tratt + au, est=irpef + add, sv=ssc, steuer_oecd=irpef + add - esente - tratt, sv_oecd=ssc)


# ---------------- Spanien
S = P["es"]


def es_ag(b):
    return min(b, S["base_max"]) * S["ss_ag"] / 100 + max(0.0, b - S["base_max"]) * S["solidaridad"] * 5 / 6 / 100


def es_reduccion(rn):
    g1, v1, g2, v2, g3 = S["reduccion"]
    if rn <= g1:
        return v1
    if rn <= g2:
        return v1 - 1.75 * (rn - g1)
    if rn <= g3:
        return v2 - 1.5 * (rn - g2)
    return 0.0


def es_heute(b, e, k):
    ss = min(b, S["base_max"]) * S["ss_an"] / 100 + max(0.0, b - S["base_max"]) * S["solidaridad"] / 6 / 100
    rn = max(0.0, b - ss - S["gastos"])
    base = max(0.0, rn - es_reduccion(rn))
    minimo = S["minimo_personal"] + sum(S["minimo_hijos"][min(i, 3)] for i in range(k))

    def cuota(bl, mn):
        return max(0.0, stufen(bl, S["irpf_grenzen"], S["irpf_saetze"]) - stufen(min(mn, bl), S["irpf_grenzen"], S["irpf_saetze"]))
    ind = cuota(base, S["minimo_personal"] + (sum(S["minimo_hijos"][min(i, 3)] for i in range(k)) / (2 if e >= 2 else 1)))
    red = S["conjunta"]["biparental"] if e >= 2 else S["conjunta"]["monoparental"] if k > 0 else 0.0
    conj = cuota(max(0.0, base - red), minimo) if red else ind
    irpf = min(ind, conj)
    return dict(netto=b - ss - irpf, est=irpf, sv=ss, steuer_oecd=irpf, sv_oecd=ss)


# ---------------- Polen
L = P["pl"]


def pl_ag(b):
    return min(b, L["limit_30"]) * L["zus_ag_limit"] / 100 + b * L["zus_ag_rest"] / 100


def pl_pit(d):
    return max(0.0, stufen(d, [L["pit_grenze"]], L["pit_saetze"]) - L["kwota_zmniejszajaca"])


def pl_heute(b, e, k):
    zus = min(b, L["limit_30"]) * L["zus_an_limit"] / 100 + b * L["zus_an_chorobowe"] / 100
    zdr = (b - zus) * L["zdrowotna"] / 100
    d = max(0.0, b - zus - L["koszty"])
    pit = 2 * pl_pit(d / 2) if e >= 2 else pl_pit(d) if k == 0 else 2 * pl_pit(d / 2)   # wspólne rozliczenie / samotny rodzic
    ulga = 0.0
    if k == 1:
        lim = L["ulga_jedno_dziecko_limit"]["para" if e >= 2 else "samotny"]
        ulga = L["ulga_dzieci"][0] if d <= lim else 0.0
    elif k > 1:
        ulga = sum(L["ulga_dzieci"][min(i, 3)] for i in range(k))
    pit_netto = pit - ulga
    pit_netto = max(pit_netto, -(zus + zdr))            # Erstattung bis zur Höhe der gezahlten Beiträge
    return dict(netto=b - zus - zdr - pit_netto + k * L["swiadczenie_800"], est=pit_netto, sv=zus + zdr, steuer_oecd=pit, sv_oecd=zus + zdr)


MODELLE = {"FR": (fr_heute, fr_ag), "IT": (it_heute, it_ag), "ES": (es_heute, es_ag), "PL": (pl_heute, pl_ag)}


def faktor(c):
    return P["waehrung"].get(c, 1.0)


def eff_alt(c):
    r, e = P["mwst"][c]
    return r * (1 - P["anteil_ermaessigt"]) + e * P["anteil_ermaessigt"]


def kq(n, c):
    """Konsumquote wie haushalte33.kq, Stützstellen mit Grundbedarf (Preisniveau) und Währung skaliert."""
    s = LS["staaten"][c]["grundbedarf_jahr_eur"] / LS["staaten"]["DE"]["grundbedarf_jahr_eur"] * faktor(c)
    pkt = [(12500 * s, .95), (37500 * s, .85), (65000 * s, .75), (100000 * s, .60)]
    if n <= pkt[0][0]:
        return pkt[0][1]
    for (a, x), (bb, y) in zip(pkt, pkt[1:]):
        if n <= bb:
            return x + (y - x) * (n - a) / (bb - a)
    return pkt[-1][1]


def neu(c, b, e, k, j):
    st_c = LS["staaten"][c]
    fx = faktor(c)
    DIV = st_c["dividende_erw_eur"][JAHRE.index(j)] * 12 * fx
    EFF = EFF_NEU[j]
    grenzen = [g * fx for g in st_c["tarif_stufen"]]
    saetze = [0.0, 11.0, 19.0, 25.0, 33.0]
    est = lambda x: stufen(x, grenzen, saetze)
    brutto = b + P["weitergabe"] * MODELLE[c][1](b)
    st = est(brutto + DIV) + (e - 1) * est(DIV)
    div = DIV * e + k * DIV / 2
    netto = brutto - st + div
    konsum = kq(netto, c) * netto
    mm = konsum * ((1 + EFF / 100) / (1 + eff_alt(c) / 100) - 1)
    mb = konsum * EFF / (100 + EFF)
    zu = st_c["fonds"]["zuschlag_pct"]
    return dict(netto=netto - mm - zu / 100 * (st + mb) - P["vorsorge"] * b, div=div)


def brutto_raster(c):
    fx = faktor(c)
    schritt = 1000 * (4 if c == "PL" else 1)
    start = 10000 * (4 if c == "PL" else 1)
    return [start + schritt * i for i in range(141)], schritt


def main():
    erg = {}
    for c, (heute, ag) in MODELLE.items():
        aw = P["oecd"]["durchschnittslohn"][c]
        h = heute(aw, 1, 0)
        lk = aw + ag(aw)
        pruef = dict(durchschnittslohn=aw, modell_est_pct_lk=round(100 * h["steuer_oecd"] / lk, 1), oecd_est_pct_lk=P["oecd"]["einkommensteuer"][c],
                     modell_sv_an_pct_lk=round(100 * h["sv_oecd"] / lk, 1), oecd_sv_an_pct_lk=P["oecd"]["sv_an"][c],
                     modell_sv_ag_pct_lk=round(100 * ag(aw) / lk, 1), oecd_sv_ag_pct_lk=P["oecd"]["sv_ag"][c],
                     modell_keil_pct=round(100 * (lk - h["netto"]) / lk, 1), oecd_keil_pct=P["oecd"]["keil"][c],
                     hinweis="Modell Recht 2026, OECD Daten 2024; OECD zählt CSG/CRDS (FR) zur Einkommensteuer")
        # Anteile mit mehr Geld: deutsche Lohnverteilung, skaliert mit dem Durchschnittslohn (Annahme)
        s = aw / P["oecd"]["durchschnittslohn"]["DE"]
        vert = [(w, b * s) for w, b in VERT_DE]
        tot = sum(w for w, _ in vert)
        anteile = {}
        for j in (2028, 2035):
            for name, e, k in (("alleinstehend", 1, 0), ("alleinerziehend, 1 Kind", 1, 1), ("Paar, ein Einkommen, 2 Kinder", 2, 2)):
                anteile[f"{j}|{name}"] = round(sum(w for w, b in vert if neu(c, b, e, k, j)["netto"] > heute(b, e, k)["netto"]) / tot * 100, 1)
        bsp = round(P["median_zu_durchschnitt"] * aw / (1000 * (4 if c == "PL" else 1))) * 1000 * (4 if c == "PL" else 1)
        if c == "PL":
            bsp = round(P["median_zu_durchschnitt"] * aw / 1000) * 1000
        beispiel = dict(brutto=bsp, plus_monat=round((neu(c, bsp, 1, 0, 2028)["netto"] - heute(bsp, 1, 0)["netto"]) / 12))
        awr = round(aw / 1000) * 1000
        beispiel_aw = dict(brutto=awr, plus_monat=round((neu(c, awr, 1, 0, 2028)["netto"] - heute(awr, 1, 0)["netto"]) / 12))
        br, schritt = brutto_raster(c)
        ras = dict(brutto=br, heute={}, ag=[round(ag(b), 1) for b in br])
        for e in (1, 2, 3):
            for k in range(4):
                ras["heute"][f"{e}|{k}"] = [round(heute(b, e, k)["netto"]) for b in br]
        ras.update(jahre=JAHRE, div=[round(d * faktor(c), 2) for d in LS["staaten"][c]["dividende_erw_eur"]], eff=[EFF_NEU[j] for j in JAHRE],
                   stufen=[g * faktor(c) for g in LS["staaten"][c]["tarif_stufen"]], saetze=[0.0, 11.0, 19.0, 25.0, 33.0], eff_alt=round(eff_alt(c), 2),
                   weitergabe=P["weitergabe"], zuschlag=LS["staaten"][c]["fonds"]["zuschlag_pct"], vorsorge=P["vorsorge"],
                   kq=[[x * LS["staaten"][c]["grundbedarf_jahr_eur"] / LS["staaten"]["DE"]["grundbedarf_jahr_eur"] * faktor(c), y]
                       for x, y in ((12500, .95), (37500, .85), (65000, .75), (100000, .60))], schritt=schritt, waehrung="PLN" if c == "PL" else "EUR")
        # Selbstprüfung: Rasterformel = neu()
        erg[c] = dict(pruefung_oecd=pruef, anteile_mit_mehr=anteile, anteil_min=min(anteile.values()), anteil_max=max(anteile.values()), beispiel=beispiel, beispiel_aw=beispiel_aw, raster=ras,
                      faelle={str(b): {f"{e}|{k}": round((neu(c, b, e, k, 2028)["netto"] - heute(b, e, k)["netto"]) / 12)
                                       for e, k in ((1, 0), (1, 1), (2, 2))} for b in [br[10], br[20], br[35], br[60], br[90], br[140]]})
    E = dict(version=P["version"], status="Prüfrechnung, vereinfacht", staaten=erg,
             hinweis="Heute nach Recht 2026 (vereinfacht, Quellen in heute_laender.toml); neu wie haushalte33.neu mit Landesgrößen. Beträge in Landeswährung je Jahr (Raster) bzw. Monat.")
    (AGG / "heute_laender.json").write_text(json.dumps(E, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    for c, x in erg.items():
        p = x["pruefung_oecd"]
        print(f"{c}: Keil {p['modell_keil_pct']} (OECD {p['oecd_keil_pct']}) | ESt {p['modell_est_pct_lk']} ({p['oecd_est_pct_lk']}) | SV-AN {p['modell_sv_an_pct_lk']} "
              f"({p['oecd_sv_an_pct_lk']}) | SV-AG {p['modell_sv_ag_pct_lk']} ({p['oecd_sv_ag_pct_lk']}) | mehr: {x['anteil_min']} % | Beispiel {x['beispiel']}")
        print("   Fälle (Monat):", x["faelle"])
        print("   Anteile:", x["anteile_mit_mehr"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
