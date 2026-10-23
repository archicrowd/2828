#!/usr/bin/env python3
"""Basis der Positionen „Große Vermögen“ und „Erbschaften“ (Deckung 33R) gegen Verteilungsdaten (Logbuch v4.32). Prüfrechnung.

Große Vermögen: Pareto-Verteilung über P90, geeicht (a) auf die Bundesbank-Befragung 2021 (P90, Anteil der oberen 10 %; Umfrage untererfasst die
Spitze) und (b) auf die DIW-Schätzung mit Millionärsstichprobe (Anteile der oberen 1 % und 10 %). Statisches Aufkommen = Satz × Vermögen über der
Schwelle, fortgeschrieben auf 2028, in % des deutschen BIP 2028. Vergleich: statische Position der Deckung (ausweichen33.json, Klub-% BIP).
Erbschaften: Basis über 100.000 € je Erwerb, die die Position der Deckung voraussetzt, gegen den steuerpflichtigen Erwerb 2025 (geltendes Recht,
höhere Freibeträge, Verschonungen). Wirkung auf die Dividende: Euro je BIP-Punkt aus ausweichen33.json.
Ausgabe: daten/aggregate/vermoegensbasis33.json
"""
import json
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "vermoegensbasis33.toml").read_text(encoding="utf-8"))
AW = json.loads((AGG / "ausweichen33.json").read_text(encoding="utf-8"))


def pareto_ueber(alpha, t90, n):
    """Haushalte über der Schwelle und Vermögen über der Schwelle (Summe) bei Pareto(alpha) über P90 = t90."""
    s = P["schwelle"]
    anteil = 0.1 * (t90 / s) ** alpha if s > t90 else 0.1
    return anteil * n, anteil * n * s / (alpha - 1)


def main():
    n = P["haushalte_mio_2021"] * 1e6
    f = P["fortschreibung_2021_2028"]
    erg = {}
    ph = P["phf"]
    m10 = ph["anteil_top10"] * ph["mittel"] / 0.1
    a_phf = m10 / (m10 - ph["p90"])                              # Pareto-Mittel = alpha/(alpha−1) × Schwelle
    hh, ueber = pareto_ueber(a_phf, ph["p90"], n)
    erg["phf_2021"] = dict(alpha=round(a_phf, 3), p90=ph["p90"], haushalte_ueber_schwelle_mio=round(hh / 1e6, 2), vermoegen_ueber_schwelle_bio=round(ueber / 1e12, 2))
    d = P["diw"]
    a_diw = 1 / (1 - __import__("math").log(d["anteil_top1"] / d["anteil_top10"]) / __import__("math").log(0.1))
    m10d = d["anteil_top10"] * d["mittel_vgr"] / 0.1
    t90d = m10d * (a_diw - 1) / a_diw
    hh, ueber = pareto_ueber(a_diw, t90d, n)
    erg["diw_spitze"] = dict(alpha=round(a_diw, 3), p90=round(t90d), haushalte_ueber_schwelle_mio=round(hh / 1e6, 2), vermoegen_ueber_schwelle_bio=round(ueber / 1e12, 2))
    for k, v in erg.items():
        auf = v["vermoegen_ueber_schwelle_bio"] * 1e12 * f * P["satz"] / 100
        v["statisch_mrd_2028"] = round(auf / 1e9, 1)
        v["statisch_pct_bip_de"] = round(auf / 1e9 / P["bip_de_2028_mrd"] * 100, 2)
    stat_modell = AW["positionen_pct_bip"]["grosse_vermoegen_statisch"]
    eur = AW["eur_je_bip_punkt"]["j2028"]
    ausw = 0.5
    for k, v in erg.items():
        v["position_nach_ausweichen_50_pct_bip"] = round(v["statisch_pct_bip_de"] * (1 - ausw), 2)
        v["dividende_2028_eur_gegen_deckung"] = round((v["statisch_pct_bip_de"] - stat_modell) * (1 - ausw) * eur)
    E_ = P["erbschaft"]
    erb_pos = AW["positionen_pct_bip"]["erbschaften"]
    basis_noetig = erb_pos / 100 * P["bip_de_2028_mrd"] / E_["satz_neu"]
    erb = dict(position_pct_bip=erb_pos, noetige_basis_ueber_100k_mrd_2028=round(basis_noetig), steuerpflichtiger_erwerb_2025_mrd=E_["steuerpflichtiger_erwerb_2025_mrd"],
               fortgeschrieben_2028_mrd=round(E_["steuerpflichtiger_erwerb_2025_mrd"] * 1.03 ** 3),
               hinweis="Der steuerpflichtige Erwerb 2025 gilt nach heutigem Recht (Freibeträge bis 500.000 €, Verschonung des Betriebsvermögens, "
                       "Erlass nach § 28a); die Basis über 100.000 € ohne Verschonung ist größer. Die nötige Basis liegt damit im Bereich der Daten, "
                       "eher vorsichtig. 2025 war ein Rekordjahr (+32,9 %), getrieben von Erwerben über 20 Mio. €: schwankend und ausweichanfällig.")
    E = dict(version=P["version"], status="Prüfrechnung", grosse_vermoegen=erg, deckung_statisch_pct_bip=stat_modell, eur_je_bip_punkt_2028=eur,
             erbschaften=erb,
             bewertung="Die statische Position der Deckung (1,94 % BIP) entspricht der Verteilung mit korrigierter Spitze (DIW); nach der Befragung "
                       "allein läge sie bei rund 40 % davon (0,79 % BIP). Bei 50 % Ausweichen kostet das die Dividende bis zu rund 30 € im Monat (2028).",
             hinweis="Haushalt statt Person als Einheit der Schwelle, Pareto über P90, Fortschreibung 3 % je Jahr: Annahmen. Anrechnung auf die "
                     "Einkommensteuer (Mindeststeuer) nicht abgezogen.")
    (AGG / "vermoegensbasis33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(erg, ensure_ascii=False))
    print("Deckung statisch", stat_modell, "| Erbschaft", erb)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
