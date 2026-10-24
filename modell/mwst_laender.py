#!/usr/bin/env python3
"""Mehrwertsteuer nach Einkommen je Staat aus der Konsumstruktur der Haushaltsbudgeterhebung (Logbuch v4.54, R5). Prüfrechnung.

Wie modell/mwst_verteilung.py für Deutschland (EVS), hier aus Eurostat hbs_str_t223 (‰ der Ausgaben je Einkommensfünftel und COICOP):
  sichtbare Mehrbelastung s_q = Σ_g a_gq ((1 + r_g,neu)/(1 + r_g,heute) − 1), sichtbar gezahlte Steuer v_q = Σ_g a_gq (1+r_neu)/(1+r_heute) · r_neu/(1+r_neu)
  mit den Sätzen heute des Staates (toml) und neu nach 33R (mwst_verteilung.saetze). Rest bis zur bisherigen Durchschnittsrechnung des Staates
  ((1+eff_neu)/(1+eff_alt(c)) − 1 auf den ganzen Konsum) gleichmäßig je Euro Konsum (Annahme wie DE) → Faktoren φ_q.
Ausgabe: daten/aggregate/mwst_laender.json; Funktion faktoren(c, netto_aequivalent) für heute_laender.mwst_phi.
"""
import importlib.util, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "mwst_laender.toml").read_text(encoding="utf-8"))
_CACHE = {}


def _mv():
    spec = importlib.util.spec_from_file_location("mwst_verteilung", W / "modell" / "mwst_verteilung.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def rechne():
    MV = _mv()
    _, neu = MV.saetze()
    HLT = tomllib.loads((W / "modell" / "heute_laender.toml").read_text(encoding="utf-8"))
    BK = tomllib.loads((W / "modell" / "boden_kosten.toml").read_text(encoding="utf-8"))
    eff = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))["reihe"][0]["label_effektiv"]
    erg = {}
    for c, hbs in P["hbs"].items():
        r, e = HLT["mwst"][c]
        eff_alt = r * (1 - HLT["anteil_ermaessigt"]) + e * HLT["anteil_ermaessigt"]
        m_bisher, b_bisher = (1 + eff / 100) / (1 + eff_alt / 100) - 1, eff / (100 + eff)
        dz = BK["dezile"][c]
        lage = [dz[d - 1] * (P["q5_faktor"] if i == 4 else 1.0) for i, d in enumerate(P["fuenftel_dezil"])]
        zeilen = []
        for q in range(5):
            summe = sum(v[q] for v in hbs.values())
            s = v_neu = v_heute = pfl = 0.0
            for code, werte in hbs.items():
                z = P["zuordnung"][code]
                a = werte[q] / summe
                rh, rn = z["heute"][c] / 100, neu[z["gruppe"]] / 100
                s += a * ((1 + rn) / (1 + rh) - 1)
                v_neu += a * (1 + rn) / (1 + rh) * rn / (1 + rn)
                v_heute += a * rh / (1 + rh)
                pfl += a if rh > 0 else 0.0
            zeilen.append(dict(fuenftel=q + 1, aequivalent_jahr=round(lage[q]), steuerpflichtig=round(pfl, 3), sichtbar_mehr_pct=round(100 * s, 3),
                               sichtbar_bezahlt_neu_pct=round(100 * v_neu, 3), sichtbar_bezahlt_heute_pct=round(100 * v_heute, 3)))
        s_m = sum(z["sichtbar_mehr_pct"] for z in zeilen) / 500
        v_m = sum(z["sichtbar_bezahlt_neu_pct"] for z in zeilen) / 500
        for z in zeilen:
            z["phi"] = [round((z["sichtbar_mehr_pct"] / 100 + m_bisher - s_m) / m_bisher, 4), round((z["sichtbar_bezahlt_neu_pct"] / 100 + b_bisher - v_m) / b_bisher, 4)]
        vh_m = sum(z["sichtbar_bezahlt_heute_pct"] for z in zeilen) / 5
        erg[c] = dict(eff_alt=round(eff_alt, 2), bisher=dict(mehr_pct=round(100 * m_bisher, 3), bezahlt_pct=round(100 * b_bisher, 3)),
                      sichtbar_mittel=dict(mehr_pct=round(100 * s_m, 3), bezahlt_neu_pct=round(100 * v_m, 3), bezahlt_heute_pct=round(vh_m, 3)),
                      fuenftel=zeilen)
    return dict(version=P["version"], status="Prüfrechnung", quelle=P["quelle"], eff_neu=eff, staaten=erg,
                hinweis="φ = (Mehrbelastung, gezahlte Steuer) je Fünftel relativ zur bisherigen Durchschnittsrechnung; Lage der Fünftel auf dem "
                        "äquivalenzgewichteten verfügbaren Einkommen (Annahme Mitte); Rest gleichmäßig je Euro Konsum (Annahme wie DE). "
                        "Staaten ohne abgerufene Struktur rechnen weiter mit φ = 1.")


def faktoren(c, aequivalent_jahr):
    if "j" not in _CACHE:
        f = AGG / "mwst_laender.json"
        _CACHE["j"] = json.loads(f.read_text(encoding="utf-8")) if f.exists() else None
    J = _CACHE["j"]
    if J is None or c not in J["staaten"]:
        return 1.0, 1.0
    kl = J["staaten"][c]["fuenftel"]
    x = aequivalent_jahr
    if x <= kl[0]["aequivalent_jahr"]:
        return tuple(kl[0]["phi"])
    for a, b in zip(kl, kl[1:]):
        if x <= b["aequivalent_jahr"]:
            t = (x - a["aequivalent_jahr"]) / (b["aequivalent_jahr"] - a["aequivalent_jahr"])
            return tuple(pa + t * (pb - pa) for pa, pb in zip(a["phi"], b["phi"]))
    return tuple(kl[-1]["phi"])


def main():
    E = rechne()
    (AGG / "mwst_laender.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in E["staaten"].items():
        print(c, "eff_alt", x["eff_alt"], "bisher", x["bisher"], "sichtbar", x["sichtbar_mittel"])
        for z in x["fuenftel"]:
            print("  Q", z["fuenftel"], z["aequivalent_jahr"], "pflichtig", z["steuerpflichtig"], "mehr", z["sichtbar_mehr_pct"],
                  "heute", z["sichtbar_bezahlt_heute_pct"], "φ", z["phi"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
