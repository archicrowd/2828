#!/usr/bin/env python3
"""Erwartete Dynamik in der geltenden Rechnung (Logbuch v4.85). Beschluss der Initiative vom 14.11.2026: mittlerer Fall aller Kanäle mit Nachfrage.

Läuft nach altlasten.py und vor projektion33.py. Liefert je Jahr 2028–2098:
  dy   Niveau des BIP gegen den statischen Pfad (Anteil),
  dp   Bevölkerung gegen den statischen Pfad (Fachkräfte und Kinder, Anteil),
  kopf BIP je Einwohner gegen den statischen Pfad (Faktor) – projektion33.py multipliziert damit das Wachstum je Kopf; Dividende in Euro,
       Progression, Grundbedarf und Netz je Kopf folgen daraus,
und das Verhältnis des Fondsbeitrags mit Dynamik zu ohne (Lösung wie einwanderung33.fonds: Altlasten feste Beträge, Anteil am BIP sinkt);
fonds_klub.py multipliziert Beitrag und Zuschlag des Fonds der 30 damit.
Kanäle, Werte und Quellen: wirtschaftsdynamik.toml; Prüfrechnung und Spannen: wirtschaftsdynamik.py (auf dem statischen Pfad).
Ausgabe: daten/aggregate/dynamik_geltend.json
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
P = tomllib.loads((W / "modell" / "wirtschaftsdynamik.toml").read_text(encoding="utf-8"))
EP = tomllib.loads((W / "modell" / "einwanderung33.toml").read_text(encoding="utf-8"))
PAR = {p["name"]: p["wert"] for p in tomllib.loads((W / "modell" / "parameter.toml").read_text(encoding="utf-8"))["parameter"]}
AL = json.loads((AGG / "altlasten.json").read_text(encoding="utf-8"))
_s = importlib.util.spec_from_file_location("al", W / "modell" / "altlasten.py")
ALM = importlib.util.module_from_spec(_s)
with contextlib.redirect_stdout(io.StringIO()):
    _s.loader.exec_module(ALM)
G = P["geltend"]
I = G["fall"]
START = P["start"]


def lin(pkte, j):
    if j <= pkte[0][0]:
        return pkte[0][1]
    for (a, x), (b, y) in zip(pkte, pkte[1:]):
        if j <= b:
            return x + (y - x) * (j - a) / (b - a)
    return pkte[-1][1]


def aufbau(j, bis):
    return max(0.0, min(1.0, (j - START) / (bis - START)))


def nachfrage_anteil(j):
    n = P["nachfrage"]
    if j <= n["voll_bis"]:
        return 1.0
    return max(0.0, 1 - (j - n["voll_bis"]) / (n["null_ab"] - n["voll_bis"]))


def kanaele(j):
    A, B, M, In, Z = P["beschaeftigung"], P["buerokratie"], P["markt"], P["investition"], P["zuversicht"]
    k = dict(A1=(A["arbeitsvolumen_pct"][I] + A["einkommenseffekt_dividende_pct"]) * A["lohnanteil_bip"] * aufbau(j, A["aufbau_bis"]),
             B1=B["ifo_mrd"] / B["bip_2024_mrd"] * 100 * B["anteil_abgebaut"][I] * aufbau(j, B["aufbau_bis"]),
             M1=M["iwf_bip_je_10pct"] * M["abbau_hemmnisse_pct"][I] / 10 * aufbau(j, M["aufbau_bis"]),
             I1=In["bip_pct"][I] * aufbau(j, In["aufbau_bis"]), Z1=Z["bip_pct"][I] * aufbau(j, Z["aufbau_bis"]))
    k["N1"] = G["impuls_pct_bip"] * P["nachfrage"]["multiplikator"][I] * nachfrage_anteil(j) if G["mit_nachfrage"] else 0.0
    return k


def fachkraefte(j):
    """Wie wirtschaftsdynamik.fachkraefte, mit festem Netto-Anreiz (Eingangswert)."""
    F = P["fachkraefte"]
    s = F["elastizitaet"][I] * G["dln_netto_fachkraefte"] * F["bestand_mio_de"] / PAR["de_einwohner_2024"] * 100
    da = besch = kinder = 0.0
    for ank in range(START, min(j, START - 1 + F["aufbau_jahre"]) + 1):
        m = s / F["aufbau_jahre"]
        if F["alter_bei_ankunft"] + (j - ank) >= 65:
            continue
        da += m
        besch += m * F["erwerb"]
        kinder += m * F["mitkommende_kinder"] if j - ank < 18 else 0.0
    wa = lin(EP["erwerbsalter_anteil"], j) * 100
    return besch * F["produktivitaet"] / (wa * EP["erwerb_einheimische"]), (da + kinder) / 100


def fonds(dy):
    """Beitrag des Altlastenfonds (Beschluss der zehn) mit größerer Wirtschaft (gleiche Lösung wie einwanderung33.fonds)."""
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
    return hi, max(p), 2029 + p.index(max(p))


def main():
    reihe = {}
    for j in range(START, 2099):
        k = kanaele(j)
        fdy, fdp = fachkraefte(j)
        k["F1"] = fdy * 100
        dy = sum(k.values()) / 100
        reihe[j] = dict(dy=dy, dp=fdp, kopf=(1 + dy) / (1 + fdp), kanaele={c: round(v, 3) for c, v in k.items()})
    c1, sp1, sj1 = fonds({j: r["dy"] for j, r in reihe.items()})
    c0, sp0, sj0 = fonds({j: 0.0 for j in reihe})
    E = dict(version="v4.85", status="geltend (Beschluss der Initiative 14.11.2026: mittlerer Fall, alle Kanäle mit Nachfrage; Visum nicht enthalten)",
             fall=P["faelle"][I], mit_nachfrage=G["mit_nachfrage"], mit_visum=G["mit_visum"],
             reihe={str(j): dict(dy=round(r["dy"], 5), dp=round(r["dp"], 6), kopf=round(r["kopf"], 5), kanaele_bip_pct=r["kanaele"]) for j, r in reihe.items()},
             fonds=dict(verhaeltnis_beitrag=round(c1 / c0, 5), verhaeltnis_spitze=round(sp1 / sp0, 5), beitrag_zehn_mit=round(c1, 3),
                        beitrag_zehn_ohne=round(c0, 3), spitzenjahr_mit=sj1, spitzenjahr_ohne=sj0),
             hinweis="Faktoren gegen den statischen Pfad; Eingangswerte Impuls und Netto-Anreiz aus der statischen Rechnung v4.84 (fest). Dieselbe Dynamik "
                     "für alle 30 Staaten (Annahme). Keine Rückwirkung auf Preise, Zinsen und Löhne.")
    (AGG / "dynamik_geltend.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Dynamik geltend ({E['fall']}, Nachfrage {G['mit_nachfrage']}): "
          + " ".join(f"{j}: BIP {reihe[j]['dy']*100:+.2f} %, je Kopf {(reihe[j]['kopf']-1)*100:+.2f} %" for j in (2028, 2030, 2035, 2045, 2060))
          + f" | Fonds × {c1 / c0:.4f}, Spitze × {sp1 / sp0:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
