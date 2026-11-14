#!/usr/bin/env python3
"""Wirtschaftliche Dynamik des Goldenen Drittels: fünf Kanäle als Thesen mit Werten (Logbuch v4.83). Prüfrechnung, keine Prognose.

Kanäle (Parameter und Quellen in wirtschaftsdynamik.toml):
  N1 Nachfrage aus mehr verfügbarem Einkommen (vorübergehend), A1 Beschäftigung, B1 Entbürokratisierung, M1 Markt ohne Grenzen,
  I1 Investitionen (Gegenrichtung), Z1 Zuversicht.
Je Kanal drei Fälle (vorsichtig, mittel, hoch); die Fälle werden kanalweise addiert (gleiche Richtung aller Unsicherheiten: Spanne eher zu weit).
Wirkung auf die Dividende wie dynamik33.py: Steuern als Anteile am BIP, Dividende in Euro wächst mit dem BIP-Faktor, dazu Progression.
Vergleich: Mehr der Haushalte 2028 (Mikrosimulation) gegen die Neuaufnahme des Fonds 2028 (gesamtlast33.json).
Nicht enthalten: Preise, Zinsen, Löhne als Rückwirkung; Verteilung; Wechselwirkungen zwischen den Kanälen; Tilgungsphase des Fonds als Nachfrageentzug.
Ausgabe: daten/aggregate/wirtschaftsdynamik.json
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
PAR = {p["name"]: p["wert"] for p in tomllib.loads((W / "modell" / "parameter.toml").read_text(encoding="utf-8"))["parameter"]}
MK = json.loads((AGG / "mikro_de.json").read_text(encoding="utf-8"))["basis"]["ergebnis"]["0.8"]["gesamt"]
AW = json.loads((AGG / "ausweichen33.json").read_text(encoding="utf-8"))
GL = json.loads((AGG / "gesamtlast33.json").read_text(encoding="utf-8"))
_s = importlib.util.spec_from_file_location("dyn", W / "modell" / "dynamik33.py")
DY = importlib.util.module_from_spec(_s)
with contextlib.redirect_stdout(io.StringIO()):
    _s.loader.exec_module(DY)
JAHRE = [2028, 2030, 2033, 2035, 2040, 2045, 2050, 2060]


def aufbau(j, bis):
    return max(0.0, min(1.0, (j - P["start"]) / (bis - P["start"])))


def nachfrage_anteil(j):
    n = P["nachfrage"]
    if j <= n["voll_bis"]:
        return 1.0
    return max(0.0, 1 - (j - n["voll_bis"]) / (n["null_ab"] - n["voll_bis"]))


def main():
    # Impuls N1: Mehr der Haushalte 2028 in % des BIP
    erw_mio = PAR["de_einwohner_2024"] * (1 - P["nachfrage"]["minderjaehrige_anteil"])
    eur_bip = AW["eur_je_bip_punkt"]["j2028"]                                  # Euro je Erwachsenem und Monat je BIP-Punkt (Kaufkraft 2026)
    mehr_mrd = MK["mittel_mehr_monat_eur"] * MK["haushalte_mio"] * 12 / 1000
    impuls = MK["mittel_mehr_monat_eur"] * MK["haushalte_mio"] / erw_mio / eur_bip
    fonds_neu = GL["c_ohne_fonds_2028"]["altlasten_im_jahr"] - GL["reihe"][0]["fonds"]
    b = P["buerokratie"]
    bk_pct = b["ifo_mrd"] / b["bip_2024_mrd"] * 100
    faelle = {}
    for i, fall in enumerate(P["faelle"]):
        A, M, I, Z = P["beschaeftigung"], P["markt"], P["investition"], P["zuversicht"]
        dauer = dict(A1=(A["arbeitsvolumen_pct"][i] + A["einkommenseffekt_dividende_pct"]) * A["lohnanteil_bip"],
                     B1=bk_pct * b["anteil_abgebaut"][i], M1=M["iwf_bip_je_10pct"] * M["abbau_hemmnisse_pct"][i] / 10,
                     I1=I["bip_pct"][i], Z1=Z["bip_pct"][i])
        bis = dict(A1=A["aufbau_bis"], B1=b["aufbau_bis"], M1=M["aufbau_bis"], I1=I["aufbau_bis"], Z1=Z["aufbau_bis"])
        reihe = {}
        for j in JAHRE:
            k = {c: v * aufbau(j, bis[c]) for c, v in dauer.items()}
            k["N1"] = impuls * P["nachfrage"]["multiplikator"][i] * nachfrage_anteil(j)
            summe = sum(k.values())
            fy = 1 + summe / 100
            jj = min(DY.NZ, key=lambda x: abs(x - j))                             # Netz-Beschluss liegt für 2028/2035/2045/2060 vor
            n, fr = DY.NZ[jj], DY.R[jj]["wachstum_je_kopf_faktor"]
            prog = DY.E0 * (DY.PJM.progression((fr * fy) ** (1 - DY.LA)) - DY.PJM.progression(fr ** (1 - DY.LA)))
            div_pct = n["dividende_pct_bip"] + prog
            eur = n["dividende_erw_eur2026"] / n["dividende_pct_bip"] * div_pct * fy
            reihe[str(j)] = dict(kanaele_bip_pct={c: round(v, 2) for c, v in k.items()}, bip_pct=round(summe, 2),
                                 dividende_erw_eur2026=round(eur), dividende_grundpfad_eur2026=n["dividende_erw_eur2026"],
                                 dividende_mehr_eur=round(eur - n["dividende_erw_eur2026"]), grundpfad_jahr=jj)
        faelle[fall] = dict(dauerhaft_voll_bip_pct={c: round(v, 2) for c, v in dauer.items()}, reihe=reihe)
    E = dict(version=P["version"], status="Prüfrechnung, Thesen mit Werten; nicht in der geltenden Rechnung",
             nachfrage=dict(mehr_haushalte_mrd_jahr_eur2026=round(mehr_mrd, 1), impuls_pct_bip=round(impuls, 2),
                            fonds_neuaufnahme_2028_pct_bip=round(fonds_neu, 2), erwachsene_mio=round(erw_mio, 1),
                            hinweis="Mehr der Haushalte 2028 (Mittel 442 € je Haushalt und Monat, 41,1 Mio. Haushalte, 80 % Weitergabe) in % des BIP über "
                                    "Euro je BIP-Punkt der Dividende; in der Größenordnung der Neuaufnahme des Fonds: Der Nachfrageschub ist zu einem großen "
                                    "Teil über die Streckung der Altlasten finanziert und kehrt sich in der Tilgungsphase um (nicht gerechnet)."),
             buerokratie_ifo_pct_bip_2024=round(bk_pct, 2), belege={k: P[k]["beleg"] for k in ("nachfrage", "beschaeftigung", "buerokratie", "markt", "investition", "zuversicht")},
             faelle=faelle,
             hinweis="Niveau des BIP gegen den Grundpfad in %; Dividende je Erwachsenem und Monat, Kaufkraft 2026, Grundpfad Netz-Beschluss (nächstliegendes "
                     "Jahr). Fälle kanalweise addiert. Keine Rückwirkung auf Preise, Zinsen und Löhne.")
    (AGG / "wirtschaftsdynamik.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Impuls N1: {mehr_mrd:.0f} Mrd. €/Jahr = {impuls:.2f} % BIP (Fonds nimmt 2028 {fonds_neu:.2f} % BIP neu auf); Bürokratie ifo {bk_pct:.2f} % BIP")
    for f, d in faelle.items():
        print(f"{f:>10}: dauerhaft {d['dauerhaft_voll_bip_pct']}")
        print("            " + " | ".join(f"{j}: BIP {x['bip_pct']:+.1f} %, Div {x['dividende_mehr_eur']:+d} €" for j, x in d["reihe"].items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
