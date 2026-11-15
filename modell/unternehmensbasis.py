#!/usr/bin/env python3
"""Unternehmensbasis nach Rechtsform und Stellhebel für Option C (Logbuch v4.88, Korrektur 89). Interne Prüfrechnung.

1 Heutige Basis der Kapitalgesellschaften 2025 aus der Kasse: KSt / 15 % (vorsichtig), Gewerbesteuer-Anteil der Kapitalgesellschaften
  (Messbetragsanteil 2018) / (3,5 % × Hebesatz) (hoch), mittel = Mittel beider.
2 Gegenstücke: Modellbasis (4,42 % BIP / 33 %), VGR-Unternehmensgewinn und Betriebsüberschuss der Kapitalgesellschaften 2024.
3 Hebel H1–H5 je Fall; Ergebnis: belegbare Unternehmensposition in % BIP, Rest-Lücke, Wirkung der Einmalbesteuerung auf die Kapitalerträge.
Ausgabe: daten/aggregate/unternehmensbasis.json (liest einnahmen_belege.py).
"""
import json
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "unternehmensbasis.toml").read_text(encoding="utf-8"))


def main():
    s, K, G, S, V, H = P["satz"], P["kasse_2025"], P["gewst_2018"], P["kst_2017"], P["vgr_2024"], P["hebel"]
    bip = K["bip_mrd"]
    pct = lambda mrd: mrd / bip * 100
    mb = {k: G[f"messbetrag_{k}"] for k in ("kapg", "persg", "einzel", "uebrige")}
    anteil = {k: v / sum(mb.values()) for k, v in mb.items()}
    gew_satz = K["messzahl"] * K["hebesatz"]
    kapg_kst = K["kst"] / K["kst_satz"]
    kapg_gew = K["gewst"] * anteil["kapg"] / gew_satz
    kapg = [kapg_kst, (kapg_kst + kapg_gew) / 2, kapg_gew]
    persg = K["gewst"] * anteil["persg"] / gew_satz
    einzel = K["gewst"] * anteil["einzel"] / gew_satz
    modell_basis = P["modell_unternehmen_pct_bip"] / s / 100 * bip
    vgr = dict(unternehmensgewinn_kapg_pct_bip=round((V["b4n_s11"] + V["b4n_s12"]) / V["bip_mio"] * 100, 2),
               betriebsueberschuss_kapg_pct_bip=round((V["b2n_s11"] + V["b2n_s12"]) / V["bip_mio"] * 100, 2))
    verlust_quote = S["verlustabzug_genutzt"] / S["zve"]
    div_anteil = K["nve"] / (K["nve"] + K["abgeltung"])
    faelle = {}
    for i, fall in enumerate(P["faelle"]):
        h1 = H["r6_mrd_28"][i] / 0.28 + H["plattformen_pct_bip"][i] / 100 * bip / s
        h2 = H["verlagerung_steuer_mrd"] / 0.30 * H["verlagerung_anrechnung"][i]
        h3 = kapg[i] * verlust_quote * H["verlust_anteil"][i]
        basis = kapg[i] + h1 + h2 + h3
        position = pct(basis) * s
        h5 = -P["modell_kapitalertraege_pct_bip"] * div_anteil * H["dividende_wirksam"][i]
        faelle[fall] = dict(
            basis_mrd=dict(kapitalgesellschaften_heute=round(kapg[i]), h1_kundenort_plattformen=round(h1), h2_gewinnverlagerung=round(h2),
                           h3_verlustverrechnung=round(h3), zusammen=round(basis)),
            unternehmen_pct_bip=round(position, 2), luecke_zum_modell_pct_bip=round(position - P["modell_unternehmen_pct_bip"], 2),
            h4_personengesellschaften_umbuchung_pct_bip=round(pct(persg) * s, 2),
            h5_einmalbesteuerung_kapitalertraege_pct_bip=round(h5, 2))
    E = dict(version=P["version"], status="interne Prüfrechnung zu Option C; nicht veröffentlichen bis zur Entscheidung E1–E5",
             basis_2025_mrd=dict(kapitalgesellschaften_kst=round(kapg_kst), kapitalgesellschaften_gewst=round(kapg_gew),
                                 personengesellschaften_gewst=round(persg), einzelunternehmen_gewst=round(einzel), modell=round(modell_basis)),
             basis_2025_pct_bip=dict(kapitalgesellschaften_mittel=round(pct(kapg[1]), 2), personengesellschaften=round(pct(persg), 2),
                                     modell=round(pct(modell_basis), 2)),
             messbetrag_anteile_2018={k: round(v, 3) for k, v in anteil.items()}, vgr_2024=vgr,
             kst_2017=dict(verlustabzug_quote_zve=round(verlust_quote, 3), verlustvortrag_bestand_mrd=round(S["verlustvortrag_bestand"] / 1000),
                           beteiligungsertraege_8b_frei_mrd=round(S["beteiligungsertraege_8b_frei"] / 1000)),
             dividendenanteil_kapitalertragsteuern=round(div_anteil, 3), faelle=faelle)
    (AGG / "unternehmensbasis.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Basis 2025 Mrd. €:", E["basis_2025_mrd"], "| % BIP:", E["basis_2025_pct_bip"], "| VGR:", vgr)
    for f, d in faelle.items():
        print(f"{f:>10}: {d['basis_mrd']} → {d['unternehmen_pct_bip']:.2f} % BIP (Lücke {d['luecke_zum_modell_pct_bip']:+.2f}); "
              f"H4 {d['h4_personengesellschaften_umbuchung_pct_bip']:+.2f}; H5 {d['h5_einmalbesteuerung_kapitalertraege_pct_bip']:+.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
