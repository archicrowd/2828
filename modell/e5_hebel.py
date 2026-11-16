#!/usr/bin/env python3
"""Hebel zu E5 (Logbuch v4.96): Label (+1/+2 Punkte, Stufenwanderung), Grundbedarf knapper, Erbschaftsfreibetrag 2 × Grundbedarf, Satz 33⅓ %.

Statisch 2028 in % BIP, auf die belegten Werte (einnahmen_belege, mittlerer Fall) bezogen, wo eine Position belegt ist.
Ausgabe: daten/aggregate/e5_hebel.json (liest e5_varianten.py für die Variante A+).
"""
import contextlib
import importlib.util
import io
import json
import math
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "e5_hebel.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("sv", W / "modell" / "systemvarianten.py")
SV = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(SV)
EB = json.loads((AGG / "einnahmen_belege.json").read_text(encoding="utf-8"))["faelle"]["mittel"]["positionen"]


def einkommen(saetze, g):
    eti, inf = SV.KERN.SZ["Robust"]["eti"], float("inf")

    def auf(s, gg):
        SV.KERN.TARIF_SAETZE[:] = [x / 100 for x in s]
        SV.KERN.TARIF_GRENZEN[:] = [gg * x for x in (1, 1.5, 2, 3)] + [inf]
        return SV.KERN.est_aufkommen(50, eti)
    return SV.zeile("01") * auf(saetze, g) / auf([0, 9, 16, 21, 28], 12348.0)


def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def anteil_ueber(F, mu, s, mittel):
    """E[(X − F)+] / E[X] für lognormal(mu, s)."""
    d1 = (mu + s * s - math.log(F)) / s
    return phi(d1) - F / mittel * phi(d1 - s)


def main():
    sy = [x for x in SV.P["system"] if x["id"] == "33R"][0]
    pos, eff0 = SV.deckung(sy)
    # Label
    L = {f"plus_{p:g}": round(SV.konsum(eff0 + p) - SV.konsum(eff0), 3) for p in P["label"]["plus_punkte"]}
    # Grundbedarf
    G = P["grundbedarf"]
    ein0 = einkommen(sy["einkommen_saetze"], G["basis_jahr"])
    gb = {}
    for v in G["varianten"]:
        k = (G["gesundheitspflege_monat"] + G["bildung_monat"] + (G["verkehr_monat"] if v == "mit_verkehr" else 0)) * 12
        neu = G["basis_jahr"] - k
        gb[v] = dict(grundbedarf_eur_2026=neu, kuerzung_pct=round(k / G["basis_jahr"] * 100, 1),
                     einkommen_pct_bip=round(einkommen(sy["einkommen_saetze"], neu), 3), mehr_pct_bip=round(einkommen(sy["einkommen_saetze"], neu) - ein0, 3))
    # Erbschaft
    E = P["erbschaft"]
    s = math.sqrt(2 * math.log(E["mittel_2015"] / E["median_2015"]))
    mu = math.log(E["median_2015"] * E["preisfaktor_2015_2028"])
    mittel = E["mittel_2015"] * E["preisfaktor_2015_2028"]
    p99 = math.exp(math.log(E["median_2015"]) + 2.3263 * s)
    g28 = G["basis_jahr"] * (1 + E["preissteigerung"]) ** 2
    F_neu = E["freibetrag_vielfaches_grundbedarf"] * g28
    r_alt, r_neu = anteil_ueber(E["freibetrag_heute_modell"], mu, s, mittel), anteil_ueber(F_neu, mu, s, mittel)
    erb_bel = EB["erbschaft"]["belegt_pct_bip"]
    erb = dict(freibetrag_neu_eur_2028=round(F_neu), sigma=round(s, 3), p99_anpassung_2015=round(p99), p99_soep_2015=E["p99_2015"],
               anteil_ueber_freibetrag_alt=round(r_alt, 3), anteil_ueber_freibetrag_neu=round(r_neu, 3), faktor=round(r_neu / r_alt, 3),
               belegt_alt_pct_bip=erb_bel, belegt_neu_pct_bip=round(erb_bel * r_neu / r_alt, 3), mehr_pct_bip=round(erb_bel * (r_neu / r_alt - 1), 3))
    # Satz 33⅓ %
    S = P["satz"]["neu"]
    f = S / 33
    ein_neu = einkommen([0, 11, 19, 25, S], G["basis_jahr"])
    sonder = {k: (S if v == 33 else v) for k, v in sy["label_sonder"].items()}
    eff_neu = SV.label_effektiv(sy["label_saetze"], sonder)
    satz = dict(einkommen=round(ein_neu - ein0, 3), kapitalertraege=round(pos["Kapitalerträge"] * (f - 1), 3),
                unternehmen_belegt=round(EB["unternehmen"]["belegt_pct_bip"] * (f - 1), 3),
                erbschaft_belegt=round(erb["belegt_neu_pct_bip"] * (f - 1), 3), label_sonderstufe=round(SV.konsum(eff_neu) - SV.konsum(eff0), 3))
    satz["zusammen"] = round(sum(satz.values()), 3)
    paket = dict(label=L["plus_2"], grundbedarf=gb["gesundheit_bildung"]["mehr_pct_bip"], erbschaft=erb["mehr_pct_bip"], satz=satz["zusammen"])
    paket["zusammen"] = round(sum(paket.values()), 3)
    Eo = dict(version=P["version"], status="interne Prüfrechnung zu E5 (Vorgaben der Initiative 16.11.2026)", label_effektiv_2028=round(eff0, 2),
              label=L, label_halten=P["label"]["halten"], grundbedarf=gb, erbschaft=erb, satz_33_drittel=satz,
              paket_2028_pct_bip=paket,
              paket_hinweis="Label +2, Grundbedarf ohne Gesundheitspflege und Bildung, Erbschaftsfreibetrag 2 × Grundbedarf, Satz 33⅓ %; dazu Stufenwanderung im Pfad (e5_varianten)")
    (AGG / "e5_hebel.json").write_text(json.dumps(Eo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(Eo, ensure_ascii=False, indent=1)[:2500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
