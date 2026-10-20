#!/usr/bin/env python3
"""Zerlegung des Unterschieds „neu gegen heute" für Beispielhaushalte eines Landes (Logbuch v4.2). Prüfrechnung.

Frage der Initiative (18.10.2026): Liegt das schwache Ergebnis Frankreichs an Schulden und Rentenzusagen (Altlastenzuschlag) oder an den heutigen
Familien- und Erwerbstätigenleistungen? Zerlegt wird je Haushalt der Monatsunterschied in:
  Altlastenzuschlag des eigenen Fonds, Pflichtvorsorge (eigenes Konto, als Abzug gerechnet), Dividende unter deutschem Niveau (kaufkraftbereinigt),
  heutige Leistungen, die entfallen (prime d'activité, allocations familiales; IT: assegno unico, trattamento integrativo, somma esente),
  Vorteil des quotient familial (FR), Rest (Tarif, Beiträge, Weitergabe, Mehrwertsteuer).
Dazu: Zuschlag nach Neustartverfahren (neustart33.json: Schnitt 33 %, Altrenten −10 %) und Anteil der Beschäftigten mit mehr Geld.
Ausgabe: daten/aggregate/zerlegung_laender.json
"""
import contextlib, copy, importlib.util, io, json
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
spec = importlib.util.spec_from_file_location("hl", W / "modell" / "heute_laender.py")
HL = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(HL)
spec2 = importlib.util.spec_from_file_location("lsx", W / "modell" / "laenderseiten.py")
LSM = importlib.util.module_from_spec(spec2)
with contextlib.redirect_stdout(io.StringIO()):
    spec2.loader.exec_module(LSM)
NS = json.loads((AGG / "neustart33.json").read_text(encoding="utf-8"))
MR = json.loads((AGG / "moeglichkeitsraum33.json").read_text(encoding="utf-8"))
FAELLE = {"FR": [(20000, 1, 0), (20000, 1, 1), (30000, 2, 2), (45000, 1, 0), (45000, 2, 2)],
          "IT": [(20000, 1, 0), (24000, 2, 2), (36000, 1, 0)]}


def monat(x):
    return round(x / 12)


def zerlege(c, b, e, k, j=2028):
    heute = HL.MODELLE[c][0]
    ls = HL.LS["staaten"][c]
    d = {}
    h = heute(b, e, k)["netto"]
    n = HL.neu(c, b, e, k, j)["netto"]
    d["gesamt"] = monat(n - h)
    zu = ls["fonds"]["zuschlag_pct"]
    ls["fonds"]["zuschlag_pct"] = 0.0
    n0 = HL.neu(c, b, e, k, j)["netto"]
    ls["fonds"]["zuschlag_pct"] = zu
    d["altlastenzuschlag"] = monat(n - n0)
    v = HL.P["vorsorge"]
    HL.P["vorsorge"] = 0.0
    n1 = HL.neu(c, b, e, k, j)["netto"]
    HL.P["vorsorge"] = v
    d["pflichtvorsorge"] = monat(n - n1)
    # Dividende auf deutsches Niveau, kaufkraftbereinigt (Grundbedarf-Verhältnis = Preisniveau)
    alt = list(ls["dividende_erw_eur"])
    pl = ls["grundbedarf_jahr_eur"] / HL.LS["staaten"]["DE"]["grundbedarf_jahr_eur"]
    ls["dividende_erw_eur"] = [x * pl for x in HL.LS["staaten"]["DE"]["dividende_erw_eur"]]
    n2 = HL.neu(c, b, e, k, j)["netto"]
    ls["dividende_erw_eur"] = alt
    d["dividende_unter_de_niveau"] = monat(n - n2)
    # heutige Leistungen, die entfallen
    if c == "FR":
        F = HL.F
        pa, af = copy.deepcopy(F["pa"]), copy.deepcopy(F["af"])
        F["pa"]["mf"] = -1e9
        d["prime_activite"] = -monat(h - heute(b, e, k)["netto"])
        F["pa"] = pa
        F["af"].update(zwei=0.0, drei=0.0, weitere=0.0)
        d["allocations_familiales"] = -monat(h - heute(b, e, k)["netto"])
        F["af"] = af
        qp, qi = F["qf_plafond"], F["qf_parent_isole"]
        F["qf_plafond"], F["qf_parent_isole"] = 0.0, 0.0
        d["quotient_familial"] = -monat(h - heute(b, e, k)["netto"])
        F["qf_plafond"], F["qf_parent_isole"] = qp, qi
    if c == "IT":
        I = HL.I
        au = copy.deepcopy(I["assegno_unico"])
        I["assegno_unico"].update(max=0.0, min=0.0)
        d["assegno_unico"] = -monat(h - heute(b, e, k)["netto"])
        I["assegno_unico"] = au
    d["rest"] = d["gesamt"] - sum(v for kk, v in d.items() if kk != "gesamt")
    return d


def anteil(c, zu=None, vorsorge=None):
    ls = HL.LS["staaten"][c]
    alt_zu, alt_v = ls["fonds"]["zuschlag_pct"], HL.P["vorsorge"]
    if zu is not None:
        ls["fonds"]["zuschlag_pct"] = zu
    if vorsorge is not None:
        HL.P["vorsorge"] = vorsorge
    aw = HL.P["oecd"]["durchschnittslohn"][c]
    vert = [(w, b * aw / HL.P["oecd"]["durchschnittslohn"]["DE"]) for w, b in HL.VERT_DE]
    tot = sum(w for w, _ in vert)
    out = {}
    for name, e, k in (("alleinstehend", 1, 0), ("alleinerziehend, 1 Kind", 1, 1), ("Paar, ein Einkommen, 2 Kinder", 2, 2)):
        out[name] = round(sum(w for w, b in vert if HL.neu(c, b, e, k, 2028)["netto"] > HL.MODELLE[c][0](b, e, k)["netto"]) / tot * 100)
    ls["fonds"]["zuschlag_pct"], HL.P["vorsorge"] = alt_zu, alt_v
    return out


def zuschlag_bei_zins(c, i):
    """Zuschlag des eigenen Fonds bei anderem Zins (Marktzins Frankreich 10 Jahre am 16.10.2026: 4,79 %, Sekundärquelle ideal-investisseur.fr)."""
    alt = LSM.MR.P["zins"]
    LSM.MR.P["zins"] = i
    z = LSM.fonds(c, HL.LS["staaten"][c]["fonds_eigen"]["start_2028"])["zuschlag_pct"]   # eigener Fonds (Vergleich)
    LSM.MR.P["zins"] = alt
    return z


def main():
    erg = {}
    for c, faelle in FAELLE.items():
        z = {f"{b}|{e}|{k}": zerlege(c, b, e, k) for b, e, k in faelle}
        ns = next(v for v in NS["staaten"][c]["varianten"] if v["schnitt"] == 0.33 and v["altrenten_kuerzung"] == 0.1)
        # Neustart: Zuschlag des eigenen Fonds um die relative Senkung aus neustart33 vermindert
        basis = next(v for v in NS["staaten"][c]["varianten"] if v["schnitt"] == 0.0 and v["altrenten_kuerzung"] == 0.0)["zuschlag_pct"]
        zu_ns = round(HL.LS["staaten"][c]["fonds"]["zuschlag_pct"] * ns["zuschlag_pct"] / basis, 1)
        erg[c] = dict(zerlegung_monat=z, zuschlag=HL.LS["staaten"][c]["fonds"]["zuschlag_pct"], zuschlag_neustart=zu_ns,
                      anteil_basis=anteil(c), anteil_neustart=anteil(c, zu=zu_ns), anteil_ohne_zuschlag=anteil(c, zu=0.0),
                      anteil_vorsorge_als_vermoegen=anteil(c, vorsorge=0.0), anteil_neustart_und_vorsorge=anteil(c, zu=zu_ns, vorsorge=0.0),
                      dividende_2028=HL.LS["staaten"][c]["dividende_erw_eur"][0],
                      dividende_de_kaufkraftgleich=round(HL.LS["staaten"]["DE"]["dividende_erw_eur"][0] * HL.LS["staaten"][c]["grundbedarf_jahr_eur"]
                                                          / HL.LS["staaten"]["DE"]["grundbedarf_jahr_eur"]),
                      zuschlag_nach_zins={str(i): zuschlag_bei_zins(c, i) for i in (2.5, 3.5, 4.5)},
                      netz_pct_bip_2028=MR["laender"][c]["z2028"]["netz"], abgabenquote_heute=MR["laender"][c]["abgabenquote_heute"])
    E = dict(version="v4.2", status="Prüfrechnung", staaten=erg,
             hinweis="Monatsbeträge, Euro 2026; positive Werte = Vorteil im neuen System. Einzeleffekte gegen den Gesamtfall, Rest = Wechselwirkungen und übrige Regeln.")
    (AGG / "zerlegung_laender.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, x in erg.items():
        print(c, "Zuschlag", x["zuschlag"], "→ Neustart", x["zuschlag_neustart"], "| Dividende", x["dividende_2028"], "DE-gleich", x["dividende_de_kaufkraftgleich"])
        for f, z in x["zerlegung_monat"].items():
            print("  ", f, z)
        for k in ("anteil_basis", "anteil_neustart", "anteil_ohne_zuschlag", "anteil_vorsorge_als_vermoegen", "anteil_neustart_und_vorsorge"):
            print("  ", k, x[k])
        print("   Netz 2028", x["netz_pct_bip_2028"], "| Zuschlag nach Zins", x["zuschlag_nach_zins"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
