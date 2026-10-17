#!/usr/bin/env python3
"""Das starke Netz als Grundversorgung: Kosten 2028–2060 und Finanzierung im Drittel-System 33R (Logbuch v3.50). Prüfrechnung.

Bisher (v3.46–v3.49) trugen die Steuern Gesundheit (GF07 7,75 % BIP), das „Seil“ (Lohnersatz bei Arbeitslosigkeit, Teile von Invalidität,
Hinterbliebenen, Familie: 2,72 %) und den Härtefall (0,65 %). Nicht finanziert waren: eine Absicherung im Alter über der Dividende für Menschen ohne
Altansprüche, die Pflege außerhalb von GF07 und die Invalidität über dem Seil-Anteil. Hier wird das Netz als Grundversorgung neu gebaut
(Parameter netz33.toml): Gesundheit ohne Extras, Pflege als Teilkasko, Grundrente, Grundbedarf bei Invalidität und Arbeitslosigkeit, Waisen, Härtefall.
Die Dividende ist der Rest: Mehr- oder Minderkosten gegen den bisher finanzierten Teil (11,12 % BIP + Anstieg Gesundheit/Pflege) gehen in die Dividende.
Ausgabe: daten/aggregate/netz33.json
"""
import contextlib, importlib.util, io, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "netz33.toml").read_text(encoding="utf-8"))
PJ = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))
SV = json.loads((AGG / "systemvarianten.json").read_text(encoding="utf-8"))
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("sz", W / "modell" / "sozialschutz.py")
SZ = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(SZ)
R = {r["jahr"]: r for r in PJ["reihe"]}
KOPF26 = G["kopf_de"] / 1.0404                     # BIP je Einwohner DE, Kaufkraft 2026 (Bezugsgröße für Euro-Beträge)
LA = 0.3                                          # Lohnbindung des Grundbedarfs (projektion33.toml, stufen_lohnanteil)


def lin(p, j):
    (a, x), (b, y) = p[0], p[-1]
    return x + (y - x) * min(max((j - a) / (b - a), 0), 1)


def netz(j, kuerzung, dauer=False, gr="volksrente"):
    r = R[j]
    f = r["wachstum_je_kopf_faktor"]
    kopf = KOPF26 * f                               # BIP je Kopf im Jahr j, Kaufkraft 2026
    gb = P["grundbedarf_eur_2026"] * f ** LA        # Grundbedarf folgt zu 30 % den Löhnen
    div = r["dividende_erw_eur2026"] * 12
    luecke = max(gb - div, 0) / kopf * 100          # Aufstockung je Person in % des BIP je Kopf
    if gr == "zwei_drittel":
        gr_luecke = max(gb * 2 / 3 - div, 0) / kopf * 100
    else:
        gr_luecke = luecke * P["grundrente_varianten"][gr]
    gp = r["gesundheit_plus"]
    pos = {
        "Gesundheit (Grundversorgung)": (SV["gesundheit"] + gp / 3) * (1 - kuerzung),   # Anteil Gesundheit am Anstieg: 0,4 von 1,2 (AR 2024, EU 2022–2070)
        "Pflege (Teilkasko)": P["pflege_pct_bip"] * (1 - P["pflege_in_gf07"]) + gp * 2 / 3,
        "Grundrente (ab 67)": lin(P["anteil_65plus"], j) * P["anteil_67_an_65plus"] * (1 - (0.0 if dauer else SZ.z_anteil_vor_stichtag(j))) * gr_luecke,
        "Invalidität (Grundbedarf)": P["invaliditaet_anteil_bev"] * luecke,
        "Arbeitslosigkeit (Grundbedarf)": P["arbeitslose_anteil_bev"] * luecke,
        "Waisen": P["waisen_pct_bip"],
        "Härtefall": P["haertefall_pct_bip"],
    }
    return pos, gb


def main():
    bisher0 = SV["gesundheit"] + SV["seil"] + P["haertefall_pct_bip"]
    erg = []
    faelle = [(k, "volksrente") for k in P["gesundheit_kuerzung"]] + [(P["gesundheit_kuerzung_basis"], g) for g in ("zwei_drittel", "mindestrente")]
    for k, gr in faelle:
        reihe = {}
        for j, dauer in ((2028, False), (2035, False), (2045, False), (2060, False), (2060, True)):
            r = R[j]
            bisher = bisher0 + r["gesundheit_plus"]
            # Dividende neu: Rest ändert sich um (bisher − neu); Grundrente/Aufstockung hängen an der Dividende -> zwei Schritte genügen
            div_pct = r["dividende_pct_bip"]
            pos, gb = netz(j, k, dauer, gr)
            for _ in range(20):
                summe = sum(pos.values())
                neu_div_pct = r["dividende_pct_bip"] + (bisher - summe)
                eur = r["dividende_erw_eur2026"] / r["dividende_pct_bip"] * neu_div_pct
                R2 = dict(r, dividende_erw_eur2026=eur)
                alt = R[j]
                R[j] = R2
                pos, gb = netz(j, k, dauer, gr)
                R[j] = alt
            reihe["dauer" if dauer else str(j)] = dict(positionen={n: round(v, 2) for n, v in pos.items()}, netz_pct_bip=round(sum(pos.values()), 2),
                                 bisher_finanziert_pct_bip=round(bisher, 2), dividende_pct_bip=round(neu_div_pct, 2),
                                 dividende_erw_eur2026=round(eur), dividende_bisher_eur2026=r["dividende_erw_eur2026"],
                                 grundbedarf_monat_eur2026=round(gb / 12),
                                 netz_eur_kopf_monat=round(sum(pos.values()) / 100 * KOPF26 * r["wachstum_je_kopf_faktor"] / 12))
        erg.append(dict(gesundheit_kuerzung=k, grundrente=gr, reihe=reihe))
    E = dict(version=P["version"], status="Prüfrechnung", system="33R", bisher_finanziert_2028=round(bisher0, 2), varianten=erg,
             hinweis="Mengen (Rentner, Invalidität, Arbeitslose) und Kürzung des Leistungskatalogs sind Annahmen; Euro je Erwachsenem, Kaufkraft 2026, Deutschland")
    (AGG / "netz33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for v in erg:
        print("Kürzung Gesundheit", v["gesundheit_kuerzung"], "Grundrente", v["grundrente"])
        for j, x in v["reihe"].items():
            print(f"  {j}: Netz {x['netz_pct_bip']} (bisher {x['bisher_finanziert_pct_bip']}) Dividende {x['dividende_pct_bip']} % = {x['dividende_erw_eur2026']} € "
                  f"(bisher {x['dividende_bisher_eur2026']}), Grundbedarf {x['grundbedarf_monat_eur2026']} €, Netz {x['netz_eur_kopf_monat']} €/Kopf | {x['positionen']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
