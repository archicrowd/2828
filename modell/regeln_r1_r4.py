#!/usr/bin/env python3
"""Beschlossene Regeln R1–R4 in der Modellrechnung (Logbuch v4.4). Prüfrechnung.

Beschluss der Initiative (18.10.2026): R1 Kinderanteil der Dividende – 0,8 prüfen (Vorschlag war 0,7); R2 Pflichtvorsorge erst auf den Lohn über dem
Grundbedarf; R3 Härtefall-Boden Grundbedarf × (1 + 0,5 je weitere/n Erwachsene/n + 0,45 je Kind); R4 Mindestlohn mindestens 50 % des
Durchschnittslohns. Geprüft wird:
  1. Dividende je Erwachsenem und Kind (Topf unverändert) für 0,5 / 0,7 / 0,8 je Land;
  2. Anteil der Beschäftigten mit mehr Geld und Beispielhaushalte (heute mit Bedarfsleistungen, sozial_laender.py);
  3. Vollzeit-Mindestlohnhaushalte mit R4;
  4. Rückwirkung von R2 auf die Mindestrente (weniger eigene Vorsorge bei Geringverdienern) und damit auf die Dividende im Dauerzustand (DE);
  5. Rückwirkung von R1 auf die netzpositionen, die an der Lücke Grundbedarf − Erwachsenendividende hängen (DE 2060);
  6. Größenordnung des Härtefall-Bodens gegen den Härtefallfonds (DE, Plausibilität).
Ausgabe: daten/aggregate/regeln_r1_r4.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
spec = importlib.util.spec_from_file_location("sl", W / "modell" / "sozial_laender.py")
SL = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(SL)
NT = tomllib.loads((W / "modell" / "netz33.toml").read_text(encoding="utf-8"))
NZ = json.loads((AGG / "netz33.json").read_text(encoding="utf-8"))
MR = json.loads((AGG / "moeglichkeitsraum33.json").read_text(encoding="utf-8"))
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
NB = {r["jahr"]: r for r in NZ["beschluss"]["reihe"]}
K = SL.K
PAKET = dict(boden=True, vorsorge_frei=True)
QUELLE_AUFSTOCKER = "BT-Drs. 21/6855 vom 02.07.2026, Tab. 4: 809.815 erwerbstätige Leistungsberechtigte im Jahresdurchschnitt 2025, Bruttoeinkommen im Mittel 834 € (amtlich)"


def topf(s):
    return (1 - K / 2) / (1 - K + s * K)


def mindest_faktor(L_monat, satz, frei):
    """wie netz33.mindest_faktor; frei = Lohnanteil ohne Pflichtvorsorge (R2: Grundbedarf)."""
    r, g = NT["realzins"], NT["lohnwachstum_real"]
    A = sum(((1 + r) / (1 + g)) ** k for k in range(NT["spar_jahre"])) / ((1 - (1 + r) ** -NT["bezugsdauer_jahre"]) / r)
    V = SL.HL.VERT_DE
    tot = sum(w * max(L_monat - NT["anrechnung_eigene_rente"] * satz * A * max(0.0, b - frei) / 12, 0) for w, b in V) / sum(w for w, _ in V)
    q = NT["anteil_lange_luecken"]
    return (1 - q) * tot / L_monat + q


def main():
    erg = dict(quelle_aufstocker=QUELLE_AUFSTOCKER, staaten={})
    # 1.–3. je Land
    for c in SL.LAENDER:
        fx = SL.HL.faktor(c)
        d28 = SL.HL.LS["staaten"][c]["dividende_erw_eur"][0] * fx
        x = dict(dividende_2028={str(s): dict(erwachsen=round(d28 * topf(s)), kind=round(d28 * topf(s) * s)) for s in (0.5, 0.7, 0.8)})
        x["anteil_s05_ohne_regeln"] = SL.anteile(c)
        for s in (0.7, 0.8):
            x[f"anteil_paket_s{s}"] = SL.anteile(c, s=s, **PAKET)
            x[f"faelle_paket_s{s}"] = SL.faelle(c, s=s, **PAKET)
        x["anteil_paket_s0.8_vorsorge_als_vermoegen"] = SL.ohne_vorsorge(lambda: SL.anteile(c, s=0.8, boden=True))
        ml = SL.mindestlohn(c)
        if "mindestlohn_jahr" in ml:
            jahr, f = ml["mindestlohn_jahr"], ml["faktor_regel_50"]
            ml["paket_s0.8"] = {n: dict(heute=round(SL.heute(c, jahr, e, k) / 12), neu=round(SL.neu(c, jahr, e, k, s=0.8, lohn_faktor=f, **PAKET) / 12))
                                for n, e, k in SL.HAUSHALTE}
        x["mindestlohn"] = ml
        erg["staaten"][c] = x
    # 4. R2 und Mindestrente (DE): Faktor bei der Lücke 2060 und im Dauerzustand
    gb = NT["grundbedarf_eur_2026"]
    L60 = max(gb * NB[2060]["netz_pct_bip"] * 0 + gb - NB[2060]["dividende_erw_eur2026"] * 12, 0) / 12
    f_basis, f_r2 = mindest_faktor(L60, 0.10, 0.0), mindest_faktor(L60, 0.10, gb)
    mr60 = NB[2060]["positionen"]["Grundrente (ab 67)"]
    mr_dauer = MR["laender"]["DE"]["dauer"]["netz"]["Mindestrente"]
    eur_je_pkt = NB[2060]["dividende_erw_eur2026"] / NB[2060]["dividende_pct_bip"]
    erg["r2_mindestrente_de"] = dict(faktor_basis=round(f_basis, 3), faktor_r2=round(f_r2, 3),
                                     mindestrente_2060_pct_bip=[mr60, round(mr60 * f_r2 / f_basis, 2)],
                                     mindestrente_dauer_pct_bip=[mr_dauer, round(mr_dauer * f_r2 / f_basis, 2)],
                                     dividende_2060_minus_eur=round((mr60 * f_r2 / f_basis - mr60) * eur_je_pkt, 1),
                                     dividende_dauer_minus_eur=round((mr_dauer * f_r2 / f_basis - mr_dauer) * eur_je_pkt, 1))
    # 5. R1: Lückenpositionen DE 2060 (Mindestrente, Invalidität, Arbeitslosigkeit) proportional zur Lücke
    pos = NB[2060]["positionen"]
    lp = pos["Grundrente (ab 67)"] + pos["Invalidität (Grundbedarf)"] + pos["Arbeitslosigkeit (Grundbedarf)"]
    div60 = NB[2060]["dividende_erw_eur2026"] * 12
    r1 = {}
    for s in (0.7, 0.8):
        d_neu = div60 * topf(s)
        mehr = lp * ((gb - d_neu) / (gb - div60) - 1)
        r1[str(s)] = dict(luecke_positionen_plus_pct_bip=round(mehr, 3), dividende_rueckwirkung_eur=round(-mehr * eur_je_pkt, 1))
    erg["r1_rueckwirkung_de_2060"] = r1
    # 6. Härtefall-Boden: Plausibilität DE (Budget 0,65 % BIP)
    bip_de_mrd = G["kopf_de"] * 83.5e6 / 1e9
    erg["r3_haertefall_de"] = dict(budget_mrd_eur=round(NT["haertefall_pct_bip"] / 100 * bip_de_mrd, 1), erwerbstaetige_leistungsberechtigte_2025=809815,
                                   kosten_bei_500_eur_monat_mrd=round(809815 * 500 * 12 / 1e9, 1), kosten_bei_1000_eur_monat_mrd=round(809815 * 1000 * 12 / 1e9, 1),
                                   hinweis="Obergrenze grob: heutige Aufstocker mit 500 bzw. 1.000 € Aufstockung je Monat; der Fonds deckt außerdem Wohnkosten über dem Grundbedarf und besondere Lagen")
    E = dict(version="v4.4", status="Prüfrechnung", **erg,
             hinweis="Monatsbeträge in Landeswährung (PL: Zł), 2028, Kaufkraft 2026. Anteile mit grober Lohnverteilung. R4 nur für Vollzeit-Mindestlohnhaushalte (Stundenlohn), nicht in den Anteilen.")
    (AGG / "regeln_r1_r4.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in erg["staaten"].items():
        print(c, "Dividende", x["dividende_2028"])
        print("   ohne Regeln", x["anteil_s05_ohne_regeln"], "| Paket 0,7", x["anteil_paket_s0.7"], "| Paket 0,8", x["anteil_paket_s0.8"],
              "| 0,8 Vorsorge als Vermögen", x["anteil_paket_s0.8_vorsorge_als_vermoegen"])
        print("   Fälle Paket 0,8:", x["faelle_paket_s0.8"])
        if "paket_s0.8" in x["mindestlohn"]:
            print("   Mindestlohn", x["mindestlohn"]["anteil_durchschnitt_2026"], "% → Faktor", x["mindestlohn"]["faktor_regel_50"], x["mindestlohn"]["paket_s0.8"])
    print("R2 Mindestrente DE:", erg["r2_mindestrente_de"])
    print("R1 Rückwirkung DE 2060:", erg["r1_rueckwirkung_de_2060"])
    print("R3 Härtefall DE:", erg["r3_haertefall_de"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
