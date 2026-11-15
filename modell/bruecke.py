#!/usr/bin/env python3
"""Brücke für Partner (Logbuch v4.91): Partner unter der Rechtsstaatsschwelle tragen einen Teil b ihrer Altlast zum gemeinsamen Satz.

Gemeinsamer Satz = BIP-gewichtetes Mittel der eigenen Sätze über alle Anteile im gemeinsamen Topf (Teilnehmer mit a = 50 %, Partner mit b).
Jeder Staat zahlt Anteil × gemeinsamer Satz + (1 − Anteil) × eigener Satz. Summenkontrolle: Das BIP-gewichtete Mittel aller Beiträge
ist gleich dem Mittel der eigenen Sätze (der Topf verteilt nur um). Grundlage: fonds_5050.py (eigene Sätze, skaliert mit dem Beschluss).
Ausgabe: daten/aggregate/bruecke.json
"""
import json
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "bruecke.toml").read_text(encoding="utf-8"))
F5 = json.loads((AGG / "fonds_5050.json").read_text(encoding="utf-8"))
MR = json.loads((AGG / "moeglichkeitsraum33.json").read_text(encoding="utf-8"))


def bip_von(c):
    l = MR["laender"][c] if "laender" in MR else MR[c]
    return l["bip_kopf_eur_2024"] * l["einwohner_mio"]


def rechne(b, form):
    a = F5["anteil_gemeinsam"]
    L = F5["laender"]
    eigen = {c: L[c]["eigen"]["beitrag_pct_bip"] for c in L}
    bip = {c: bip_von(c) for c in L}
    anteil = {c: a for c in F5["teilnehmer"]}
    # gemeinsamer Satz ohne Brücke (nur Teilnehmer)
    g0 = sum(bip[c] * eigen[c] for c in F5["teilnehmer"]) / sum(bip[c] for c in F5["teilnehmer"])
    for c in F5["partner"]:
        if form == "alle" or eigen[c] > g0:
            anteil[c] = b
    for _ in range(50):   # "wahl": Auswahl hängt am gemeinsamen Satz; Fixpunkt
        g = sum(anteil[c] * bip[c] * eigen[c] for c in anteil) / sum(anteil[c] * bip[c] for c in anteil)
        if form == "wahl":
            neu = {c: a for c in F5["teilnehmer"]} | {c: b for c in F5["partner"] if eigen[c] > g}
            if neu == anteil:
                break
            anteil = neu
        else:
            break
    zahl = {c: anteil.get(c, 0) * g + (1 - anteil.get(c, 0)) * eigen[c] for c in L}
    mittel = sum(bip[c] * zahl[c] for c in L) / sum(bip.values())
    mittel_eigen = sum(bip[c] * eigen[c] for c in L) / sum(bip.values())
    if abs(mittel - mittel_eigen) > 1e-9:
        raise SystemExit("Summenkontrolle Brücke verletzt")
    ohne = {c: (a * g0 + (1 - a) * eigen[c]) if c in F5["teilnehmer"] else eigen[c] for c in L}
    umverteilt = sum(bip[c] * (ohne[c] - zahl[c]) for c in F5["partner"]) / 100   # Mio. € (BIP in Mio. €) je Jahr, Entlastung der Partner
    teil_bip = sum(bip[c] for c in F5["teilnehmer"])
    return dict(gemeinsamer_satz_pct_bip=round(g, 3), gemeinsamer_satz_ohne_bruecke_pct_bip=round(g0, 3),
                partner={c: dict(eigen=round(eigen[c], 2), mit_bruecke=round(zahl[c], 2), aenderung=round(zahl[c] - eigen[c], 2),
                                 in_bruecke=c in anteil) for c in F5["partner"]},
                teilnehmer_aenderung_pct_bip=round((sum(bip[c] * (zahl[c] - ohne[c]) for c in F5["teilnehmer"])) / teil_bip, 3),
                entlastung_partner_mrd_eur_2024=round(umverteilt / 1000, 2),
                beispiel_teilnehmer={c: round(zahl[c] - ohne[c], 3) for c in ("DE", "FR", "IT", "PL")})


def main():
    E = dict(version=P["version"], status="Entwicklungsmodus: Prüfrechnung, kein Beschluss", partner=F5["partner"],
             einheit="Beitrag zum Fonds in % des eigenen BIP je Jahr, dauerhaft; Entlastung in Mrd. € je Jahr, BIP 2024 nominal",
             varianten={f"{int(b * 100)}_{f}": rechne(b, f) for b in P["anteile"] for f in P["formen"]})
    (AGG / "bruecke.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in E["varianten"].items():
        print(k, "gem.", v["gemeinsamer_satz_pct_bip"], "(ohne", v["gemeinsamer_satz_ohne_bruecke_pct_bip"], ") Teiln.", v["teilnehmer_aenderung_pct_bip"],
              "Entl.", v["entlastung_partner_mrd_eur_2024"], "Mrd |", " ".join(f"{c} {p['eigen']}→{p['mit_bruecke']}" for c, p in v["partner"].items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
