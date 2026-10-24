#!/usr/bin/env python3
"""Altlastenfonds mit maximaler Streckung (Logbuch v3.45). Prüfrechnung; die Gesamtrechnung bleibt unverändert.

Vorgabe der Initiative (17.10.2026): Der Altlastenbeitrag soll nicht einseitig und nicht länderbezogen auf die Löhne gehen; maximale Streckung,
Tilgung bei Einnahmenspitzen.

Modell: Ein gemeinsamer Altlastenfonds übernimmt die Staatsschulden 2028 (Schuldenquote der Gesamtrechnung) und zahlt die Altrenten über der
Dividende (Z, modell/sozialschutz.py, mit der Dividende der gewählten Systemvariante). Er erhält einen gleichbleibenden Beitrag c (% des BIP) aus
einer breiten Quelle (Zuschlag auf alle Steuern oder Abzug von der Dividende). Schuldenquote: d(t+1) = d(t)·(1+i)/(1+g) + Z(t) − c.
Gesucht: c, sodass die Schuldenquote im Zieljahr T den Zielwert erreicht. Varianten: T, Zielwert, Zins i, Z voll oder halb.
Tilgung bei Einnahmenspitzen: nicht modelliert (Regel, keine Prognose); jeder Punkt des BIP, der in einem Jahr t zusätzlich getilgt wird, senkt
die Schuldenquote im Jahr T um ((1+i)/(1+g))^(T−t) Punkte.
Ausgabe: daten/aggregate/altlasten.json
"""
import contextlib
import importlib.util
import io
import json
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "altlasten.toml").read_text(encoding="utf-8"))
_mz = round(sum(P["zins_reihe_ea"]) / len(P["zins_reihe_ea"]), 2)     # v4.20: Fondszins = Mittel 2006–2025 (Euroraum)
if abs(_mz - P["beschluss"]["zins"]) > 0.005:
    raise SystemExit(f"altlasten.toml: Fondszins {P['beschluss']['zins']} weicht vom Mittel der Reihe {_mz} ab")


def lade(name, pfad):
    spec = importlib.util.spec_from_file_location(name, pfad)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


SZ = lade("sz", W / "modell" / "sozialschutz.py")
SZ.KUERZUNG = SZ.kuerzung_aus(P)                       # v3.48: Renten um eingesparte Beiträge gekürzt; v4.37 je Staat
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
SV = json.loads((AGG / "systemvarianten.json").read_text(encoding="utf-8"))
G_NOM = G.get("wachstum_nominal", 3.0) / 100 if G.get("wachstum_nominal") else 0.03


def pfad(c, z, i, d0, jahre):
    d, out = d0, []
    for t in range(jahre):
        d = d * (1 + i) / (1 + G_NOM) + (z[t] if t < len(z) else 0.0) - c
        out.append(d)
    return out


def loese_c(z, i, d0, jahr_ende, ziel):
    n = jahr_ende - 2028
    lo, hi = -5.0, 20.0
    for _ in range(80):
        c = (lo + hi) / 2
        lo, hi = (c, hi) if pfad(c, z, i, d0, n)[-1] > ziel else (lo, c)
    return (lo + hi) / 2


def main():
    k = G["anteil_minderjaehrige"] / 100
    d0 = G["schuldenquote_2028"]
    erg = {}
    for sid in P["systeme"]:
        v = next(x for x in SV["varianten"] if x["id"] == sid)
        div_erw = v["dividende_pct_bip_2028"] / (1 - k / 2)
        zv = SZ.z_klub(div_erw)
        quote = v["punkte"]["2028"]["steuerbedarf"]
        faelle = []
        for zanteil in P["z_anteil"]:
            z = [x * zanteil for x in zv]
            for i in P["zins"]:
                for (ende, ziel) in P["ziele"]:
                    c = loese_c(z, i / 100, d0, ende, ziel)
                    pf = pfad(c, z, i / 100, d0, ende - 2028)
                    spitze = max(pf)
                    faelle.append(dict(z_anteil=zanteil, zins=i, zieljahr=ende, zielquote=ziel, beitrag_pct_bip=round(c, 2),
                                       zuschlag_auf_alle_steuern_pct=round(c / quote * 100, 1),
                                       je_einwohner_monat_eur=round(c / 100 * G["kopf_klub"] / 12),
                                       schuldenquote_spitze=round(spitze, 1), spitzenjahr=2029 + pf.index(spitze),
                                       schuldenquote_2050=round(pf[2050 - 2029], 1) if ende >= 2050 else None))
        deckel = []
        for zanteil in P["z_anteil"]:
            z = [x * zanteil for x in zv]
            for cap in P["deckel"]:
                lo, hi = -5.0, 20.0
                for _ in range(60):
                    c = (lo + hi) / 2
                    lo, hi = (c, hi) if max(pfad(c, z, P["zins"][0] / 100, d0, 72)) > cap else (lo, c)
                pf = pfad(hi, z, P["zins"][0] / 100, d0, 72)
                deckel.append(dict(z_anteil=zanteil, zins=P["zins"][0], deckel=cap, beitrag_pct_bip=round(hi, 2),
                                   zuschlag_auf_alle_steuern_pct=round(hi / quote * 100, 1),
                                   je_einwohner_monat_eur=round(hi / 100 * G["kopf_klub"] / 12), schuldenquote_2100=round(pf[-1], 1)))
        erg[sid] = dict(name=v["name"], steuerquote=quote, dividende_de_erw_2028=v["dividende_de_erw_2028"],
                        z_2028=round(zv[0], 2), faelle=faelle, deckel=deckel)
    # Verteilung zwischen den Staaten bei gemeinsamem Fonds (nicht länderbezogen): Altlast 2028 je Land gegen den Beitrag nach BIP-Anteil
    sid = P["systeme"][0]
    v = next(x for x in SV["varianten"] if x["id"] == sid)
    pfade, _, _ = SZ.z_laender(v["dividende_pct_bip_2028"] / (1 - k / 2))
    s28 = G["zins_2028"]
    aufschlag = {r["land"]: r for r in G["tabelle_aufschlag"]}
    namen = {r["land"]: r["name"] for r in G["tabelle_laender_div"]}
    schuld = {c: next(r["schuld"] for r in G["tabelle_aufschlag"] if r["land"] == namen[c]) for c in SZ.LAENDER}
    w = SZ.gewicht()
    alt = {c: pfade[c][0]["z_pct_bip"] + schuld[c] * s28 / 100 for c in SZ.LAENDER}
    schnitt = sum(w[c] * alt[c] for c in SZ.LAENDER)
    verteilung = {namen[c]: dict(altlast_2028_pct_bip=round(alt[c], 2), gegen_schnitt=round(alt[c] - schnitt, 2)) for c in SZ.LAENDER}
    # v3.46: Beschluss – gemeinsamer Fonds, Verrechnung je Staat, linear abschmelzend
    B = P["beschluss"]
    vb = next(x for x in SV["varianten"] if x["id"] == B["system"])
    pf_b, _, _ = SZ.z_laender(vb["dividende_pct_bip_2028"] / (1 - k / 2))
    zb = [x * B["z_anteil"] for x in SZ.z_klub(vb["dividende_pct_bip_2028"] / (1 - k / 2), w)]
    cb = loese_c(zb, B["zins"] / 100, d0, B["zieljahr"], B["zielquote"])
    pfb = pfad(cb, zb, B["zins"] / 100, d0, B["zieljahr"] - 2028)
    quote_b = vb["punkte"]["2028"]["steuerbedarf"]
    zins_c = {c: schuld[c] * s28 / 100 for c in SZ.LAENDER}
    zins_s = sum(w[c] * zins_c[c] for c in SZ.LAENDER)
    # Verrechnung je Staat (Beschluss): Jeder Staat trägt den gemeinsamen Beitrag c im Verhältnis seiner eigenen Altlast 2028 (Z-Anteil + Zinsen,
    # % des eigenen BIP) zum Durchschnitt; dieses Verhältnis schmilzt linear in `verrechnung_jahre` auf 1 ab (dann gleicher Satz für alle).
    # Summe über die Staaten (BIP-gewichtet) = c; kein Staat zahlt weniger als null.
    alt_b = {c: pf_b[c][0]["z_pct_bip"] * B["z_anteil"] + zins_c[c] for c in SZ.LAENDER}
    alt_s = sum(w[c] * alt_b[c] for c in SZ.LAENDER)
    laender_b = {}
    for c in SZ.LAENDER:
        reihe = {}
        for j in (2028, 2035, 2040, 2050, 2058):
            m = max(0.0, 1 - (j - 2028) / B["verrechnung_jahre"])
            beitrag = cb * (m * alt_b[c] / alt_s + (1 - m))
            reihe[str(j)] = dict(beitrag_pct_bip=round(beitrag, 2), zuschlag_pct=round(beitrag / quote_b * 100, 1))
        laender_b[namen[c]] = dict(altlast_2028_pct_bip=round(alt_b[c], 2), reihe=reihe)
    beschluss = dict(system=B["system"], z_anteil=B["z_anteil"], zins=B["zins"], zieljahr=B["zieljahr"], beitrag_pct_bip=round(cb, 2),
                     zuschlag_auf_alle_steuern_pct=round(cb / quote_b * 100, 1), je_einwohner_monat_eur=round(cb / 100 * G["kopf_klub"] / 12),
                     schuldenquote_spitze=round(max(pfb), 1), spitzenjahr=2029 + pfb.index(max(pfb)),
                     schuldenquote={str(j): round(pfb[j - 2029], 1) for j in (2030, 2040, 2050, 2060, 2070, 2080, 2090, 2098)},
                     verhandlungsmasse_z_2028_pct_bip=round(zb[0], 2), laender=laender_b,
                     ungerundet=dict(beitrag_pct_bip=cb, zuschlag_auf_alle_steuern_pct=cb / quote_b * 100),   # v4.26, Korrektur 70: für den Übertrag (fonds_klub)
                     altlast_schnitt_2028=round(alt_s, 2),
                     hinweis="Beitrag je Staat = gemeinsamer Beitrag × (Anteil nach eigener Altlast, linear in 30 Jahren abschmelzend auf gleichen Satz); "
                             "Zuschlag bezogen auf die Steuerquote der Variante (vereinfachend für alle Staaten gleich)")
    E = dict(version=P["version"], status="Prüfrechnung", kuerzung_renten=SZ.KUERZUNG, wachstum_nominal=G_NOM * 100, schuldenquote_2028=d0, systeme=erg, beschluss=beschluss,
             verteilung_gemeinsamer_fonds=dict(system=sid, schnitt_pct_bip=round(schnitt, 2), laender=verteilung,
                                               hinweis="Altlast 2028 = Z + Zinsen auf die eigene Schuld (Zins 2028 der Gesamtrechnung); "
                                                       "positiv: das Land bringt mehr Altlast mit, als es nach BIP-Anteil beiträgt"),
             tilgungsregel=P["tilgungsregel"])
    (AGG / "altlasten.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for s, e in erg.items():
        print(f"{e['name']}: Quote {e['steuerquote']}, Dividende DE {e['dividende_de_erw_2028']} €, Z 2028 {e['z_2028']}")
        for f in e["faelle"]:
            print(f"   Z {f['z_anteil']:.0%} Zins {f['zins']} % Ziel {f['zielquote']} % bis {f['zieljahr']}: Beitrag {f['beitrag_pct_bip']} % BIP "
                  f"= Zuschlag {f['zuschlag_auf_alle_steuern_pct']} % auf alle Steuern = {f['je_einwohner_monat_eur']} €/Einw./Monat; "
                  f"Spitze {f['schuldenquote_spitze']} % ({f['spitzenjahr']})")
    print("Beschluss:", {k_: v_ for k_, v_ in beschluss.items() if k_ != "laender"})
    for n, r in beschluss["laender"].items():
        print(f"   {n:<12} Altlast {r['altlast_2028_pct_bip']:>5}", {j: x["zuschlag_pct"] for j, x in r["reihe"].items()})
    print("Verteilung (gemeinsamer Fonds):", {n: x["gegen_schnitt"] for n, x in verteilung.items()}, "Schnitt", round(schnitt, 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
