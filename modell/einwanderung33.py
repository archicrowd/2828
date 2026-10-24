#!/usr/bin/env python3
"""Einwanderung im Drittel-System (Logbuch v3.48). Prüfrechnung, keine Prognose.

Frage: Was bedeuten Einwanderungsziele, wenn die Staaten kontrollierte Einwanderung ermöglichen, um die Alterung auszugleichen?
Modell (Parameter in einwanderung33.toml): zusätzliche Nettoeinwanderung m (% der Bevölkerung 2028 je Jahr) im Erwerbsalter, Erwerbstätigkeit steigt
mit den Jahren seit Ankunft, Produktivität relativ zum Durchschnitt. Wirtschaftsleistung wächst mit der Zahl der Erwerbstätigen (Kapital passt sich an).
Wirkungen:
  1. Altenquotient (65+ je Person 20–64).
  2. Wirtschaftsleistung und Wirtschaftsleistung je Einwohner gegen den Grundpfad.
  3. Dividende je Erwachsenem (Euro): Anteil am BIP aus projektion33.json, Gesundheit und Pflege neu gewichtet (Eingewanderte jung, geringere Kosten),
     in Euro mit der Wirtschaftsleistung je Einwohner.
  4. Altlasten: Altrenten (Z) und Schulden sind feste Beträge aus dem alten System; mit größerer Wirtschaft sinkt ihr Anteil. Beitrag des gemeinsamen
     Fonds (Beschluss, Tilgung bis 2098) neu gelöst. Eingewanderte erwerben im neuen System keine Ansprüche über der Dividende.
Ausgabe: daten/aggregate/einwanderung33.json
"""
import contextlib, importlib.util, io, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "einwanderung33.toml").read_text(encoding="utf-8"))
PJ = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))
AL = json.loads((AGG / "altlasten.json").read_text(encoding="utf-8"))
# v4.41 (R9): Dividende nach dem Netz-Beschluss (netz33.json, geltend) statt projektion33 (Vorstufe); Fonds der 30 (fonds_geltend.json)
NZ = {r["jahr"]: r for r in json.loads((AGG / "netz33.json").read_text(encoding="utf-8"))["beschluss"]["reihe"]}
FG = json.loads((AGG / "fonds_geltend.json").read_text(encoding="utf-8"))
V30 = FG["grundlage"]["verhaeltnis_beitrag_30_zu_10"]
spec = importlib.util.spec_from_file_location("al", W / "modell" / "altlasten.py")
ALM = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(ALM)


def lin(pkte, j):
    if j <= pkte[0][0]:
        return pkte[0][1]
    for (a, x), (b, y) in zip(pkte, pkte[1:]):
        if j <= b:
            return x + (y - x) * (j - a) / (b - a)
    return pkte[-1][1]


def szenario(m, erwerb=None, prod=None):
    """Jahrespfad 2028–2098: Zuwachs Bevölkerung, Erwerbstätige, BIP (Faktoren gegen Grundpfad)."""
    out = {}
    for j in range(2028, 2099):
        erw_neu = kinder = besch = 0.0
        for ank in range(2028, j + 1):
            alter = P["alter_bei_ankunft"] + (j - ank)
            if alter >= 65:
                continue                                   # nach 2063 erste Zugänge im Rentenalter: dann wie Einheimische (Dividende), hier vereinfacht ausgeblendet
            erw_neu += m
            kinder += m * P["mitkommende_kinder"] if j - ank < 18 else 0.0
            besch += m * lin(erwerb or P["erwerb"], j - ank)
        wa = lin(P["erwerbsalter_anteil"], j) * 100
        oadr = lin(P["altenquotient"], j)
        alte = oadr * wa
        dy = besch * (prod or P["produktivitaet"]) / (wa * P["erwerb_einheimische"])
        dp = (erw_neu + kinder) / 100
        out[j] = dict(oadr_basis=oadr, oadr=alte / (wa + erw_neu), dy=dy, dp=dp)
    return out


def fonds(dy):
    """Beitrag des Altlastenfonds (Beschluss) mit größerer Wirtschaft: Z und Schuld als feste Beträge, Anteil am BIP sinkt."""
    B = AL["beschluss"]
    k = ALM.G["anteil_minderjaehrige"] / 100
    sv = next(x for x in ALM.SV["varianten"] if x["id"] == B["system"])
    z = [x * B["z_anteil"] for x in ALM.SZ.z_klub(sv["dividende_pct_bip_2028"] / (1 - k / 2))]
    zs = [z[t] / (1 + dy.get(2028 + t, dy[max(dy)])) for t in range(len(z))]
    i, g = B["zins"] / 100, ALM.G_NOM
    d0 = ALM.G["schuldenquote_2028"]

    def pf(c):
        d, o = d0, []
        for t in range(B["zieljahr"] - 2028):
            j = 2029 + t
            wachs = (1 + dy.get(j, dy[max(dy)])) / (1 + dy.get(j - 1, dy[max(dy)]))
            d = d * (1 + i) / ((1 + g) * wachs) + (zs[t] if t < len(zs) else 0) - c
            o.append(d)
        return o
    lo, hi = -5.0, 20.0
    for _ in range(80):
        c = (lo + hi) / 2
        lo, hi = (c, hi) if pf(c)[-1] > 0 else (lo, c)
    p = pf(hi)
    return round(hi, 2), round(max(p), 1), 2029 + p.index(max(p))


def main():
    R = {r["jahr"]: r for r in PJ["reihe"]}
    gs0 = P["gesundheit_pct_bip_2028"]
    erg = []
    for m, art in [(m_, a_) for m_ in P["zusatz_pct"] for a_ in ("kontrolliert", "schwierig")]:
        s = szenario(m) if art == "kontrolliert" else szenario(m, P["schwer_erwerb"], P["schwer_produktivitaet"])
        reihe = {}
        for j in (2035, 2045, 2060):
            x, r = s[j], R[j]
            # Gesundheit und Pflege: Bestand (gs0 + Anstieg) bezogen auf das größere BIP, dazu Eingewanderte mit relativen Kosten
            n = NZ[j]                                         # v4.41: Netz-Beschluss
            gs = n["positionen"]["Gesundheit (Grundversorgung)"] + n["positionen"]["Pflege (Teilkasko)"]
            gs_neu = (gs + gs0 * P["gesundheit_relativ"] * x["dp"]) / (1 + x["dy"])
            # Kopfbeträge (Dividende, Gemeinden) wachsen mit der Bevölkerung; vereinfachend: Dividende in % BIP gleich, plus Gesundheitsentlastung
            div_pct = n["dividende_pct_bip"] + (gs - gs_neu)
            kopf = (1 + x["dy"]) / (1 + x["dp"])            # BIP je Einwohner gegen Grundpfad
            eur = n["dividende_erw_eur2026"] / n["dividende_pct_bip"] * div_pct * kopf if n["dividende_pct_bip"] > 0 else 0
            reihe[str(j)] = dict(altenquotient_basis=round(x["oadr_basis"], 3), altenquotient=round(x["oadr"], 3),
                                 bevoelkerung_plus_pct=round(x["dp"] * 100, 1), bip_plus_pct=round(x["dy"] * 100, 1),
                                 bip_je_kopf_pct=round((kopf - 1) * 100, 1), gesundheit_pflege_pct_bip=round(gs_neu, 2),
                                 gesundheit_pflege_basis=round(gs, 2), dividende_erw_eur2026=round(eur),
                                 dividende_basis_eur2026=n["dividende_erw_eur2026"])
        c, spitze, sj = fonds({j: v["dy"] for j, v in s.items()})
        # v4.41: auf den Fonds der 30 übertragen (Verhältnis wie fonds_klub.py; Spitze mit Spitze 30 / Spitze zehn skaliert, Annahme)
        c30 = c * V30
        erg.append(dict(zusatz_pct=m, integration=art, zusatz_mio_je_jahr_klub=round(m / 100 * 255.06, 2), reihe=reihe,
                        fonds_beitrag_pct_bip=round(c30, 2), fonds_zuschlag_pct=round(c30 / FG["beitrag_pct_bip"] * FG["zuschlag_auf_alle_steuern_pct"], 1),
                        fonds_spitze=round(spitze * FG["schuldenquote_spitze"] / AL["beschluss"]["schuldenquote_spitze"], 1), fonds_spitzenjahr=sj,
                        fonds_beitrag_zehn_pct_bip=c))
    B = AL["beschluss"]
    E = dict(version=P["version"], status="Prüfrechnung", annahmen={k: P[k] for k in P if k != "version"}, szenarien=erg,
             grundpfad_fonds=dict(beitrag_pct_bip=FG["beitrag_pct_bip"], zuschlag_pct=FG["zuschlag_auf_alle_steuern_pct"], spitze=FG["schuldenquote_spitze"],
                                  spitzenjahr=FG["spitzenjahr"], zehn=dict(beitrag_pct_bip=B["beitrag_pct_bip"], spitze=B["schuldenquote_spitze"])),
             hinweis="v4.41: Grundpfad Dividende netz33.json (Netz-Beschluss), Fonds der 30 (Beschluss der zehn mit Wirtschaftszuwachs gelöst, Verhältnis 30/10); "
                     "Einwanderung zusätzlich zu den amtlichen Annahmen")
    (AGG / "einwanderung33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Grundpfad Fonds:", E["grundpfad_fonds"])
    for e in erg:
        print(f"[{e['integration']}] +{e['zusatz_pct']} % je Jahr ({e['zusatz_mio_je_jahr_klub']} Mio): Fonds {e['fonds_beitrag_pct_bip']} % BIP, Spitze {e['fonds_spitze']} ({e['fonds_spitzenjahr']})")
        for j, x in e["reihe"].items():
            print("   ", j, x)
    return 0


if __name__ == "__main__":
    sys.exit(main())
