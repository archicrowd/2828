#!/usr/bin/env python3
"""Das Drittel-System (33R, starkes Netz als Grundversorgung) für jeden Staat des Möglichkeitsraums (Logbuch v3.52). Prüfrechnung.

Je Staat: Netz aus Landesdaten (Gesundheit GF07 −5 %, Pflege, Invalidität nach GF1001 relativ zu Deutschland, Arbeitslosigkeit nach Quote, Mindestrente nach
Anteil 65+, Waisen, Härtefall), Grundbedarf nach Preisniveau, Transformationsdividende als Rest; Altlasten: Staatsschuld 2024 + Altrenten über der Dividende
(um eingesparte Beiträge gekürzt), eigener Fonds bis 2098. Zwei Zeitpunkte: 2028 und Dauerzustand (nach Auslauf der Altrenten, Trends wie 2060).
Ausgabe: daten/aggregate/moeglichkeitsraum33.json
"""
import contextlib, csv, importlib.util, io, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "moeglichkeitsraum33.toml").read_text(encoding="utf-8"))
D = json.loads((AGG / "moeglichkeitsraum_2024.json").read_text(encoding="utf-8"))
NZ = json.loads((AGG / "netz33.json").read_text(encoding="utf-8"))
PJ = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))
SV = json.loads((AGG / "systemvarianten.json").read_text(encoding="utf-8"))
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
NT = tomllib.loads((W / "modell" / "netz33.toml").read_text(encoding="utf-8"))
EW = {r["land"]: r for r in csv.DictReader(open(AGG / "moeglichkeitsraum.csv", encoding="utf-8"))}
spec = importlib.util.spec_from_file_location("sz", W / "modell" / "sozialschutz.py")
SZ = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(SZ)
SZ.KUERZUNG = 0.1235
V = next(x for x in SV["varianten"] if x["id"] == PJ["system"])
R = {r["jahr"]: r for r in PJ["reihe"]}
K = G["anteil_minderjaehrige"] / 100
LAENDER = list(D["gf07"].keys())
kopf = {c: D["bip_mio_eur"][c] / float(EW[c]["einwohner_mio"]) for c in LAENDER}            # € je Einwohner 2024
pli = {c: kopf[c] / D["pps_index"][c] for c in LAENDER}                                       # Preisniveau (relativ)
saldo = V["punkte"]["2028"]["saldo"]


def rahmen(z):
    if z == "2028":
        return dict(deck=V["deckung"], dach=R[2028]["dach_ohne_zins"], gem=V["quote_kern"] - R[2028]["dach_ohne_zins"] - R[2028]["dividende_ohne_trends_pct_bip"],
                    gp=0.0, alter=False, f=1.0)
    r = R[2060]
    return dict(deck=r["deckung"] + r["progression"], dach=r["dach_ohne_zins"], gem=V["quote_kern"] - r["dach_ohne_zins"] - r["dividende_ohne_trends_pct_bip"],
                gp=r["gesundheit_plus"], alter=True, f=r["wachstum_je_kopf_faktor"])


POS = V["deckung_positionen"]


def deckung_land(c, deck_de):
    """v3.53: Aufkommen nach eigener Steuerbasis: Einkommen nach Arbeitnehmerentgelt, Kapital und Unternehmen nach Betriebsüberschuss, Konsum nach
    privatem Konsum (je relativ zu Deutschland); übrige Positionen wie auf deutscher Basis. Skaliert auf das Jahr (deck_de/Deckung 2028)."""
    if P.get("aufkommen") == "gleich":
        return deck_de
    rel = lambda k: D[k][c] / D[k]["DE"]
    eigen = (POS["Einkommen"] * rel("d1") + (POS["Kapitalerträge"] + POS["Unternehmen und Plattformen"]) * rel("b2a3g")
             + POS["Konsum (Label)"] * rel("p31_s14") + sum(v for k, v in POS.items() if k not in ("Einkommen", "Kapitalerträge", "Unternehmen und Plattformen", "Konsum (Label)")))
    return eigen * deck_de / V["deckung"]


def land(c, z):
    ra = rahmen(z)
    ra = dict(ra, deck=deckung_land(c, ra["deck"]))
    kp = kopf[c] * P["bip_2024_zu_kaufkraft_2026_2028"] * ra["f"]                             # € je Kopf (Rechengröße)
    gb = NT["grundbedarf_eur_2026"] * pli[c] / pli["DE"] * ra["f"] ** 0.3                        # Grundbedarf nach Preisniveau
    gs = P["schweiz_gesundheit_pct_bip"] if c == "CH" else D["gf07"][c]
    div_pct = 5.0
    for _ in range(50):
        div_eur = div_pct / 100 * kp / 12 / (1 - K / 2) * 12                                   # je Erwachsenem im Jahr
        luecke = max(gb - div_eur, 0) / kp * 100
        netz = {"Gesundheit": (gs + ra["gp"] / 3) * (1 - NT["gesundheit_kuerzung_basis"]), "Pflege": P["pflege_basis"] + ra["gp"] * 2 / 3,
                "Mindestrente": (D["anteil65"][c] / 100 * NT["anteil_67_an_65plus"] * P["faktor_mindestrente"] * luecke) if ra["alter"] else 0.0,
                "Invalidität": NT["invaliditaet_anteil_bev"] * D["gf1001"][c] / D["gf1001"]["DE"] * luecke,
                "Arbeitslosigkeit": D["arbeitslos"][c] / 100 * P["erwerbsquote_bev"] * luecke,
                "Waisen": NT["waisen_pct_bip"], "Härtefall": NT["haertefall_pct_bip"]}
        neu = ra["deck"] - saldo - ra["dach"] - ra["gem"] - sum(netz.values())
        if abs(neu - div_pct) < 1e-6:
            break
        div_pct = neu
    div_mon = div_pct / 100 * kp / 12 / (1 - K / 2)
    return dict(deckung_pct_bip=round(ra["deck"], 2), netz_pct_bip=round(sum(netz.values()), 2), netz={k: round(v, 2) for k, v in netz.items()}, dividende_pct_bip=round(div_pct, 2),
                dividende_erw_eur=round(div_mon), dividende_erw_kaufkraft_de=round(div_mon * pli["DE"] / pli[c]),
                grundbedarf_monat_eur=round(gb / 12), div_erw_pct_kopf=div_pct / (1 - K / 2))


def altlasten(c, div_erw, deck):
    rente = D["gf1002"][c] + D["gf1003"][c]
    # v3.53: Skalierung auf Tabelle 29 (ungedeckte staatliche Ansprüche 2021) wie sozialschutz.z_laender, wo der Barwert der Ausgaben größer ist
    pv = sum(rente * SZ.z_anteil_vor_stichtag(j) / 1.01 ** (j - 2028) for j in range(2028, 2101))
    rente = rente * min(1.0, D["s13pu_2021"][c] / pv)
    z = [x["z_pct_bip"] for x in SZ.z_pfad(c, rente, D["anteil65"][c], div_erw, lambda j: 1.0)]
    d0, i, g = D["schuld"][c], P["zins"] / 100, P["wachstum_nominal"] / 100

    def pf(cc):
        d, o = d0, []
        for t in range(2098 - 2028):
            d = d * (1 + i) / (1 + g) + (z[t] if t < len(z) else 0) - cc
            o.append(d)
        return o
    lo, hi = -5.0, 30.0
    for _ in range(80):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if pf(m)[-1] > 0 else (lo, m)
    p = pf(hi)
    return dict(z_2028=round(z[0], 2), beitrag_pct_bip=round(hi, 2), zuschlag_pct=round(hi / deck * 100, 1), spitze=round(max(p)))


def main():
    erg = {}
    for c in LAENDER:
        a, b = land(c, "2028"), land(c, "dauer")
        al = altlasten(c, a["div_erw_pct_kopf"], a["deckung_pct_bip"])
        erg[c] = dict(name=EW[c]["name"], einwohner_mio=float(EW[c]["einwohner_mio"]), bip_kopf_eur_2024=round(kopf[c]),
                      preisniveau_de_100=round(pli[c] / pli["DE"] * 100), abgabenquote_heute=D["abgabenquote"][c],
                      z2028={k: v for k, v in a.items() if k != "div_erw_pct_kopf"}, dauer={k: v for k, v in b.items() if k != "div_erw_pct_kopf"},
                      altlasten=al, gesamtlast_2028=round(a["deckung_pct_bip"] + al["beitrag_pct_bip"], 1))
    ew = {c: erg[c]["einwohner_mio"] for c in erg}
    bip = {c: D["bip_mio_eur"][c] for c in erg}
    sw, sb = sum(ew.values()), sum(bip.values())
    raum = dict(staaten=len(erg), einwohner_mio=round(sw, 1), bip_mrd_eur_2024=round(sb / 1000),
                dividende_erw_kaufkraft_de_2028=round(sum(ew[c] * erg[c]["z2028"]["dividende_erw_kaufkraft_de"] for c in erg) / sw),
                dividende_erw_kaufkraft_de_dauer=round(sum(ew[c] * erg[c]["dauer"]["dividende_erw_kaufkraft_de"] for c in erg) / sw),
                netz_pct_bip_2028=round(sum(bip[c] * erg[c]["z2028"]["netz_pct_bip"] for c in erg) / sb, 2),
                altlasten_beitrag_pct_bip=round(sum(bip[c] * erg[c]["altlasten"]["beitrag_pct_bip"] for c in erg) / sb, 2),
                abgabenquote_heute=round(sum(bip[c] * erg[c]["abgabenquote_heute"] for c in erg) / sb, 1))
    raum["deckung_pct_bip_2028"] = round(sum(bip[c] * erg[c]["z2028"]["deckung_pct_bip"] for c in erg) / sb, 2)
    raum["zuschlag_pct"] = round(raum["altlasten_beitrag_pct_bip"] / raum["deckung_pct_bip_2028"] * 100, 1)
    E = dict(version=P["version"], status="Prüfrechnung", system=PJ["system"], laender=erg, raum=raum, quellen=D["quellen"], hinweise=D["hinweise"],
             annahmen={k: v for k, v in P.items() if k != "version"},
             hinweis="Aufkommen je Staat nach eigener Steuerbasis (Lohn-, Gewinn-, Konsumanteil relativ zu Deutschland; übrige Positionen wie DE). Dividende in Euro des Landes und in deutscher Kaufkraft. "
                     "Altrenten ohne Altersprofil des Ageing Report, auf Tabelle 29 skaliert (Nordische Staaten: GF1002 enthält Pflegedienste -> Z überzeichnet)")
    (AGG / "moeglichkeitsraum33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{'Staat':<16}{'Einw':>6}{'Quote heute':>12}{'Deck':>6}{'Netz28':>8}{'Div28 €':>9}{'KK DE':>7}{'Div∞ KK':>9}{'Schuld':>8}{'Z28':>6}{'Fonds':>7}{'Zuschl':>8}{'Last28':>8}")
    for c, e in sorted(erg.items(), key=lambda x: -x[1]["einwohner_mio"]):
        print(f"{e['name'][:15]:<16}{e['einwohner_mio']:>6.1f}{e['abgabenquote_heute']:>12}{e['z2028']['deckung_pct_bip']:>6}{e['z2028']['netz_pct_bip']:>8}{e['z2028']['dividende_erw_eur']:>9}"
              f"{e['z2028']['dividende_erw_kaufkraft_de']:>7}{e['dauer']['dividende_erw_kaufkraft_de']:>9}{D['schuld'][c]:>8}{e['altlasten']['z_2028']:>6}"
              f"{e['altlasten']['beitrag_pct_bip']:>7}{e['altlasten']['zuschlag_pct']:>8}{e['gesamtlast_2028']:>8}")
    print("Raum:", raum)
    return 0


if __name__ == "__main__":
    sys.exit(main())
