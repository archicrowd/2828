#!/usr/bin/env python3
"""Validierung der Steuer- und Abgabenmodelle „heute“ je Staat gegen OECD Taxing Wages 2026 (Daten 2025); Logbuch v4.51. Prüfrechnung.

Geprüft wird, ob die Modelle, mit denen die Länderseiten und Haushaltsrechnungen „heute“ rechnen (DE: Kernmodell über haushalte33;
FR, IT, ES, PL: heute_laender), den amtlichen Steuer- und Abgabenkeil treffen:
  Keil = (Arbeitskosten − verfügbares Einkommen einschließlich Geldleistungen) / Arbeitskosten
für (a) Alleinstehende bei 100 % des Durchschnittslohns, mit Zerlegung in Einkommensteuer, Beiträge der Beschäftigten und der Arbeitgeber;
(b) Paar mit einem Einkommen (100 %) und zwei Kindern. Die Modelle rechnen Recht 2026, die OECD-Werte gelten für 2025: Rechtsänderungen
zum 1.1.2026 erscheinen als Abweichung und sind zu erklären, nicht zu eichen.
Dazu (ohne neue Rechnung) die Rekonstruktion des Gini heute gegen Eurostat aus gini.json.
Ausgabe: daten/aggregate/validierung_laender.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "validierung_laender.toml").read_text(encoding="utf-8"))
O = P["oecd"]


def lade(name):
    spec = importlib.util.spec_from_file_location(name, W / "modell" / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


H = lade("haushalte33")
HL = lade("heute_laender")


def de_heute(b, e, k):
    r = H.K.netto_heute(b, k, e >= 2)
    return dict(netto=r["netto"], steuer_oecd=r["est"], sv_oecd=r["sv"])


MODELLE = {"DE": (de_heute, H.ag_roh)}
MODELLE.update(HL.MODELLE)


def keil(c, b, e, k):
    heute, ag = MODELLE[c]
    h = heute(b, e, k)
    lk = b + ag(b)
    return h, lk, 100 * (lk - h["netto"]) / lk


def anteile(c):
    """Anteile mit mehr Geld 2028 wie heute_laender.main (deutsche Lohnverteilung auf den Durchschnittslohn skaliert)."""
    heute = MODELLE[c][0]
    sk = HL.P["oecd"]["durchschnittslohn"][c] / HL.P["oecd"]["durchschnittslohn"]["DE"]
    vert = [(w, b * sk) for w, b in HL.VERT_DE]
    tot = sum(w for w, _ in vert)
    return {n: round(sum(w for w, b in vert if HL.neu(c, b, e, k, 2028)["netto"] > heute(b, e, k)["netto"]) / tot * 100, 1)
            for n, e, k in (("alleinstehend", 1, 0), ("alleinerziehend, 1 Kind", 1, 1), ("Paar, ein Einkommen, 2 Kinder", 2, 2))}


def main():
    tol = P["toleranz_pp"]
    erg = {}
    for c in ("DE", "FR", "IT", "ES", "PL"):
        aw = O["durchschnittslohn_2025"][c]
        h, lk, k1 = keil(c, aw, 1, 0)
        ag = MODELLE[c][1](aw)
        allein = dict(modell_keil=round(k1, 1), oecd_keil=O["keil_allein_100"][c], abw_pp=round(k1 - O["keil_allein_100"][c], 1),
                      modell_est=round(100 * h["steuer_oecd"] / lk, 1), oecd_est=O["est_allein_100"][c],
                      modell_sv_an=round(100 * h["sv_oecd"] / lk, 1), oecd_sv_an=O["sv_an_allein_100"][c],
                      modell_sv_ag=round(100 * ag / lk, 1), oecd_sv_ag=O["sv_ag_allein_100"][c])
        _, _, k2 = keil(c, aw, 2, 2)
        paar = dict(modell_keil=round(k2, 1), oecd_keil=O["keil_paar_ein_einkommen_2k"][c], abw_pp=round(k2 - O["keil_paar_ein_einkommen_2k"][c], 1))
        for x in (allein, paar):
            x["bestanden"] = abs(x["abw_pp"]) <= tol
        erg[c] = dict(durchschnittslohn_2025=aw, allein_100=allein, paar_ein_einkommen_2k=paar)
    # Varianten zu den Abweichungen (v4.51)
    var = {}
    # FR: prime d'activité gegen das Ministerium (Beispiele nach der Reform 1.4.2026, Paar mit einem Einkommen und zwei Kindern, Alleinstehend,
    # Alleinerziehend mit zwei Kindern) und gegen OECD; Variante forfait logement für alle (Obergrenze der Wirkung)
    def prime(f, e, k):
        b = f * HL.F["smic"]
        r = HL.fr_heute(b, e, k)
        af = (HL.F["af"]["zwei"] * 12 if k >= 2 else 0.0)
        return round((r["netto"] - (b - r["sv"]) + r["est"] - af) / 12)
    M = P["fr_ministerium"]
    pa = {}
    for fl in (0.0, 1.0):
        HL.F["pa"]["forfait_anteil"] = fl
        pa[str(fl)] = {n: [[f, prime(f, *M[n]["haushalt"]), v] for f, v in M[n]["werte"]] for n in M}
        pa[str(fl)]["keil_paar_2k_aw"] = round(keil("FR", O["durchschnittslohn_2025"]["FR"], 2, 2)[2], 1)
        pa[str(fl)]["anteile_mit_mehr"] = anteile("FR")
    HL.F["pa"]["forfait_anteil"] = 0.0
    var["FR_prime_activite"] = dict(spalten="Vielfaches des SMIC, Modell, Ministerium (€/Monat)", ohne_forfait=pa["0.0"], mit_forfait=pa["1.0"])
    # PL: Abgrenzung der Arbeitgeberbeiträge wie OECD (ohne Unfall, Arbeitsfonds, Garantiefonds = zus_ag_rest)
    rest = HL.L["zus_ag_rest"]
    alt = HL.MODELLE["PL"]
    HL.L["zus_ag_rest"] = 0.0
    aw = O["durchschnittslohn_2025"]["PL"]
    var["PL_ag_wie_oecd"] = dict(keil_allein=round(keil("PL", aw, 1, 0)[2], 1), keil_paar_2k=round(keil("PL", aw, 2, 2)[2], 1),
                                 anteile_mit_mehr_ohne_rest_in_weitergabe=anteile("PL"))
    HL.L["zus_ag_rest"] = rest
    var["PL_ag_wie_oecd"]["anteile_mit_mehr_geltend"] = anteile("PL")
    G = json.loads((W / "daten" / "aggregate" / "gini.json").read_text(encoding="utf-8"))
    gini = {c: dict(amtlich_2025=v["gini_amtlich_2025"], rekonstruktion=v["gini_rekonstruktion_heute"],
                    abw=round(v["gini_rekonstruktion_heute"] - v["gini_amtlich_2025"], 1)) for c, v in G["staaten"].items()}
    n_ok = sum(x[t]["bestanden"] for x in erg.values() for t in ("allein_100", "paar_ein_einkommen_2k"))
    E = dict(version=P["version"], status="Prüfrechnung", quelle=O["quelle"], toleranz_pp=tol, keil=erg, varianten=var, gini_heute=gini,
             bestanden=f"{n_ok} von {2 * len(erg)} Haushaltstypen innerhalb ±{tol} Pp",
             offen="Paar mit zwei Einkommen (Tab. 1.5) nicht geprüft: Ländermodelle kennen je Haushalt ein Erwerbseinkommen",
             hinweis="Modelle Recht 2026, OECD Daten 2025. Keil in % der Arbeitskosten, einschließlich Geldleistungen (Kindergeld, allocations "
                     "familiales, prime d'activité, assegno unico, 800+). DE heute ohne Günstigerprüfung Kinderfreibetrag (Kernmodell).")
    (W / "daten" / "aggregate" / "validierung_laender.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in erg.items():
        a, p = x["allein_100"], x["paar_ein_einkommen_2k"]
        print(f"{c}: allein Keil {a['modell_keil']} (OECD {a['oecd_keil']}, {a['abw_pp']:+}) ESt {a['modell_est']}/{a['oecd_est']} "
              f"SV-AN {a['modell_sv_an']}/{a['oecd_sv_an']} SV-AG {a['modell_sv_ag']}/{a['oecd_sv_ag']} | Paar 2K {p['modell_keil']} "
              f"(OECD {p['oecd_keil']}, {p['abw_pp']:+})")
    print(E["bestanden"])
    print(json.dumps(var, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
