#!/usr/bin/env python3
"""Gemeinsamer Altlastenfonds: zehn, zwölf und 30 Staaten; geltender Fonds der 30 (Logbuch v4.19, v4.20). Prüfrechnung.

v4.19: Bei gleichem Zins, gleichem Wachstum und gleichem Zieljahr ist die Rekursion d(t+1) = d(t)(1+i)/(1+g) + Z(t) − c linear. Der
gemeinsame Beitrag eines Klubs ist das BIP-gewichtete Mittel der eigenen Beiträge (Abgrenzung moeglichkeitsraum33: Schuld 2024, Altrenten
nach Tabelle 29). Diese Abgrenzung weicht vom Beschluss der zehn (altlasten.py, Rentnerpaket, Startschuld 2028) ab; übertragen wird deshalb
das Verhältnis Klub / zehn (Annahme: Die Abweichung der Abgrenzung wirkt für alle Klubs gleich).
v4.20 (Beschluss 21.10.2026): Der gemeinsame Fonds umfasst alle 30 Staaten. Geltende Werte = Beschluss der zehn × Verhältnis 30 / zehn;
Schuldenpfad: Pfad der 30 in der Abgrenzung des Möglichkeitsraums, Niveau skaliert mit Spitze Beschluss / Spitze der zehn (Annahme).
Ausgaben: daten/aggregate/fonds_klub.json, daten/aggregate/fonds_geltend.json (von Haushalts-, Länder- und Seitenrechnungen gelesen)
"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
MRJ = json.loads((AGG / "moeglichkeitsraum33.json").read_text(encoding="utf-8"))["laender"]
BJ = json.loads((AGG / "altlasten.json").read_text(encoding="utf-8"))["beschluss"]
BU = BJ.get("ungerundet", dict(beitrag_pct_bip=BJ["beitrag_pct_bip"], zuschlag_auf_alle_steuern_pct=BJ["zuschlag_auf_alle_steuern_pct"]))   # v4.26, Korrektur 70
spec = importlib.util.spec_from_file_location("mr", W / "modell" / "moeglichkeitsraum33.py")
MR = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(MR)
ZEHN = ["DE", "FR", "ES", "NL", "IE", "BE", "AT", "DK", "SI", "EE"]
KLUBS = {"zehn (Beschluss)": ZEHN, "zehn + Italien": ZEHN + ["IT"], "zehn + Polen": ZEHN + ["PL"],
         "zwölf (zehn + Italien + Polen)": ZEHN + ["IT", "PL"], "alle 30": list(MRJ)}
JAHRE = range(2029, 2099)


def pfad_land(c):
    """Eigener Fonds wie moeglichkeitsraum33.altlasten, mit Pfad."""
    a = MR.land(c, "2028")
    rente = MR.D["gf1002"][c] + MR.D["gf1003"][c]
    pv = sum(rente * MR.SZ.z_anteil_vor_stichtag(j) / 1.01 ** (j - 2028) for j in range(2028, 2101))
    rente = rente * min(1.0, MR.D["s13pu_2021"][c] / pv)
    z = [x["z_pct_bip"] for x in MR.SZ.z_pfad(c, rente, MR.D["anteil65"][c], a["div_erw_pct_kopf"], lambda j: 1.0)]
    i, g, c0 = MR.P["zins"] / 100, MR.P["wachstum_nominal"] / 100, MRJ[c]["altlasten"]["beitrag_pct_bip"]
    d, out = MR.D["schuld"][c], []
    for t in range(len(JAHRE)):
        d = d * (1 + i) / (1 + g) + (z[t] if t < len(z) else 0) - c0
        out.append(d)
    return out


def klub(laender, pfade=None):
    bip = {c: MRJ[c]["bip_kopf_eur_2024"] * MRJ[c]["einwohner_mio"] for c in laender}
    s = sum(bip.values())
    beitrag = sum(bip[c] * MRJ[c]["altlasten"]["beitrag_pct_bip"] for c in laender) / s
    deckung = sum(bip[c] * MRJ[c]["altlasten"]["beitrag_pct_bip"] / MRJ[c]["altlasten"]["zuschlag_pct"] * 100 for c in laender) / s
    pf = [sum(bip[c] * pfade[c][t] for c in laender) / s for t in range(len(JAHRE))] if pfade else None
    return beitrag, beitrag / deckung * 100, pf


def main():
    pfade = {c: pfad_land(c) for c in MRJ}
    b10, z10, p10 = klub(ZEHN, pfade)
    erg = []
    for name, l in KLUBS.items():
        b, z, _ = klub(l)
        erg.append(dict(klub=name, staaten=len(l), beitrag_mr_pct_bip=round(b, 2), zuschlag_mr_pct=round(z, 1),
                        beitrag_skaliert_pct_bip=round(BU["beitrag_pct_bip"] * b / b10, 2), zuschlag_skaliert_pct=round(BU["zuschlag_auf_alle_steuern_pct"] * z / z10, 1)))
    E = dict(version="v4.20", status="Prüfrechnung", zins=MR.P["zins"], beschluss_zehn=dict(beitrag_pct_bip=BJ["beitrag_pct_bip"], zuschlag_pct=BJ["zuschlag_auf_alle_steuern_pct"]),
             klubs=erg, hinweis="BIP 2024 (bip_kopf × Einwohner, moeglichkeitsraum33). Skaliert = Beschluss × Verhältnis zur Zehnergruppe in der Abgrenzung "
                                 "des Möglichkeitsraums (Annahme). Tilgung bis 2098 wie im Beschluss.")
    (AGG / "fonds_klub.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    # v4.20: geltender gemeinsamer Fonds der 30 Staaten
    b30, z30, p30 = klub(list(MRJ), pfade)
    f_niveau = BJ["schuldenquote_spitze"] / max(p10)
    pf = [x * f_niveau for x in p30]
    sp = max(pf)
    G = dict(version="v4.26", status="geltend (Beschluss 21.10.2026: 30 Staaten, Zins = Mittel 2006–2025)", staaten=len(MRJ), zins=MR.P["zins"],
             beitrag_pct_bip=round(BU["beitrag_pct_bip"] * b30 / b10, 2), zuschlag_auf_alle_steuern_pct=round(BU["zuschlag_auf_alle_steuern_pct"] * z30 / z10, 1),
             schuldenquote_spitze=round(sp, 1), spitzenjahr=JAHRE[pf.index(sp)], zieljahr=BJ["zieljahr"],
             schuldenquote={str(j): round(pf[j - 2029], 1) for j in (2030, 2040, 2050, 2060, 2070, 2080, 2090, 2098)},
             grundlage=dict(beschluss_zehn=dict(beitrag_pct_bip=BJ["beitrag_pct_bip"], zuschlag_pct=BJ["zuschlag_auf_alle_steuern_pct"],
                                                spitze=BJ["schuldenquote_spitze"], spitzenjahr=BJ["spitzenjahr"]),
                            verhaeltnis_beitrag_30_zu_10=round(b30 / b10, 4), verhaeltnis_zuschlag_30_zu_10=round(z30 / z10, 4)),
             hinweis="Beschluss der zehn (altlasten.py, Rentnerpaket) × Verhältnis 30/10 aus dem Möglichkeitsraum; Schuldenpfad der 30, Niveau skaliert "
                     "(Annahme). Gleicher Satz für alle Staaten; die Verrechnung je Staat (30 Jahre) ist nur für die zehn gerechnet.")
    (AGG / "fonds_geltend.json").write_text(json.dumps(G, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in erg:
        print(r)
    print("geltend 30:", {k: G[k] for k in ("beitrag_pct_bip", "zuschlag_auf_alle_steuern_pct", "schuldenquote_spitze", "spitzenjahr", "zins")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
