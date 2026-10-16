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


def lade(name, pfad):
    spec = importlib.util.spec_from_file_location(name, pfad)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


SZ = lade("sz", W / "modell" / "sozialschutz.py")
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
    E = dict(version=P["version"], status="Prüfrechnung", wachstum_nominal=G_NOM * 100, schuldenquote_2028=d0, systeme=erg,
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
    print("Verteilung (gemeinsamer Fonds):", {n: x["gegen_schnitt"] for n, x in verteilung.items()}, "Schnitt", round(schnitt, 2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
