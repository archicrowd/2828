#!/usr/bin/env python3
"""Rentnerausgleich und Lebensarbeitszeit (Logbuch v4.10). Prüfrechnung, Deutschland.

Ausgangslage im Modell (haushalte33.rentner, altlasten, sozialschutz):
  - Bestandsrenten werden voll weitergezahlt, gekürzt um die entfallenden KV-/PV-Beiträge (12,35 %). Die Dividende ist darin enthalten
    (Altlastenfonds zahlt nur den Anspruch über der Dividende, Z) – Rentner erhalten keine Dividende zusätzlich.
  - Die ganze Rente ist steuerpflichtig (heute Besteuerungsanteil 83 %), dazu höhere Mehrwertsteuer und Altlastenzuschlag 13,7 %.
  - Mindestrente gilt nur für Ansprüche nach dem Stichtag 2028; ein Boden für kleine Bestandsrenten ist nicht geregelt.
  - Anwartschaften der Erwerbstätigen: pro rata der Erwerbsjahre vor dem Stichtag (Kohortenschema, Rentenalter 65 in sozialschutz.toml).
Gerechnet werden:
  A  Netto je Monat heute und neu für Renten 900–2.200 € unter Ausgleichsvarianten (geringere Kürzung, Besteuerungsanteil 83 %,
     Pauschale, Befreiung vom Zuschlag) und ihre jährlichen Kosten (grob, Rentnerzahl × Mittelwert);
  B  kleine Bestandsrenten: Lücke zum Grundbedarf ohne Boden, mit Boden (volle Anrechnung) und heutige Grundsicherung im Vergleich;
  C  Lebensarbeitszeit: Kopplung des Rentenbeginns an die fernere Lebenserwartung (1:1 wie Dänemark, 2/3 wie Niederlande) – Entlastung
     des Altlastenfonds (Z) und der Mindestrente, in % BIP und als Dividende je Erwachsenem.
Ausgabe: daten/aggregate/rentnerausgleich.json
"""
import contextlib, csv, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "rentnerausgleich.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("rb", W / "modell" / "regel_boden.py")
RB = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(RB)
H = RB.SL.H33
H.setze_jahr(2028)
NZ = json.loads((AGG / "netz33.json").read_text(encoding="utf-8"))
NB = {r["jahr"]: r for r in NZ["beschluss"]["reihe"]}
TOPF = RB.topf(RB.S)
GB = RB.SL.HL.LS["staaten"]["DE"]["grundbedarf_jahr_eur"]


def heute(r_monat):
    return H.rentner(r_monat, P["zuschlag_pct"], 2028)[0]          # Jahresbetrag


def neu(r_monat, kuerzung=None, steueranteil=1.0, pauschale=0.0, zuschlag=None, boden=False):
    k = P["kuerzung"] if kuerzung is None else kuerzung
    zu = P["zuschlag_pct"] if zuschlag is None else zuschlag
    r = 12 * r_monat * (1 - k)
    st = H.est(r * steueranteil)
    y = r - st + 12 * pauschale
    eff = H.eff_jahr(2028)
    konsum = H.kq(y) * y
    n = y - konsum * ((1 + eff / 100) / (1 + H.EFF_ALT / 100) - 1) - zu / 100 * (st + konsum * eff / (100 + eff))
    if boden:
        n = max(n, GB)
    return n


def varianten():
    v = {"Beschluss (Kürzung 12,35 %, voll steuerpflichtig, Zuschlag)": {}}
    for r in P["renten_monat"]:
        v["Beschluss (Kürzung 12,35 %, voll steuerpflichtig, Zuschlag)"][r] = neu(r)
    for k in P["varianten_kuerzung"][1:]:
        v[f"Kürzung {k * 100:.1f} %".replace(".", ",")] = {r: neu(r, kuerzung=k) for r in P["renten_monat"]}
    v["Besteuerungsanteil 83 % wie heute"] = {r: neu(r, steueranteil=0.83) for r in P["renten_monat"]}
    v["Befreiung vom Altlastenzuschlag"] = {r: neu(r, zuschlag=0.0) for r in P["renten_monat"]}
    for p in P["pauschale_monat"]:
        v[f"Pauschale {p} € steuerfrei"] = {r: neu(r, pauschale=p) for r in P["renten_monat"]}
    v["Kürzung 7,5 % + Besteuerungsanteil 83 %"] = {r: neu(r, kuerzung=0.075, steueranteil=0.83) for r in P["renten_monat"]}
    out = {}
    for name, w in v.items():
        diff = {str(r): round((w[r] - heute(r)) / 12) for r in P["renten_monat"]}
        mittel = sum((w[r] - neu(r)) for r in P["renten_monat"]) / len(P["renten_monat"])   # Mehrkosten je Rentner/Jahr gegen Beschluss
        mrd = mittel * P["rentner_mio"] * 1e6 / 1e9
        out[name] = dict(differenz_monat_je_rente=diff, mehrkosten_mrd=round(mrd, 1), mehrkosten_pct_bip=round(100 * mrd / P["bip_mrd_2028"], 2))
    return out


def kleine_renten():
    out = {}
    for r in (600, 900, 1200):
        n = neu(r)
        out[str(r)] = dict(neu_ohne_boden=round(n / 12), neu_mit_boden=round(max(n, GB) / 12), grundbedarf=round(GB / 12),
                           heute_ohne_grundsicherung=round(heute(r) / 12), heute_mit_grundsicherung=round(max(heute(r) / 12, P["bedarf_heute_monat"])))
    return out


def z_pfad():
    z = {}
    with open(AGG / "z_pfad.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["land"] == "DE":
                z[int(row["jahr"])] = float(row["z_pct_bip"])
    return z


def lebensarbeitszeit():
    z = z_pfad()
    mr = lambda j: NB[j]["positionen"]["Grundrente (ab 67)"] if j in NB else NB[2060]["positionen"]["Grundrente (ab 67)"]
    eur_pkt = lambda j: NB[min(j, 2060)]["dividende_erw_eur2026"] / NB[min(j, 2060)]["dividende_pct_bip"] * TOPF
    out = {}
    for name, a in P["kopplungen"].items():
        reihe = {}
        for j in (2035, 2040, 2045, 2050, 2060, 2070):
            d = a * P["le65_zuwachs_jahr"] * max(0, j - P["start_kopplung"])       # Anhebung des Rentenbeginns in Jahren
            anteil = min(d / P["bezugsdauer_jahre"], 1.0)                          # weniger Rentnerjahrgänge (Gleichverteilung)
            spar = (z.get(j, 0.0) + mr(j)) * anteil
            reihe[str(j)] = dict(rentenbeginn_plus_jahre=round(d, 2), entlastung_pct_bip=round(spar, 2),
                                 dividende_plus_eur_monat=round(spar * eur_pkt(j), 1))
        out[name] = reihe
    return out


def main():
    E = dict(version=P["version"], status="Prüfrechnung, grob", varianten=varianten(), kleine_bestandsrenten=kleine_renten(),
             lebensarbeitszeit=lebensarbeitszeit(),
             grundsicherung_heute=dict(empfaenger_ab_altersgrenze=P["grundsicherung_alter_empfaenger"], ausgaben_mrd_alter_und_em=P["grundsicherung_ausgaben_mrd"]),
             hinweis="DE 2028, Kaufkraft 2026, Monatsbeträge. Mehrkosten = Mittel über die vier Beispielrenten × 18 Mio. Rentner (grob, ohne "
                     "Rentenverteilung). Lebensarbeitszeit: Entlastung von Altlastenfonds (Z, z_pfad.csv) und Mindestrente (netz33) durch späteren "
                     "Rentenbeginn; ohne zusätzliche Steuern aus längerer Arbeit (vorsichtig).")
    (AGG / "rentnerausgleich.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in E["varianten"].items():
        print(f"{k:<50}", v["differenz_monat_je_rente"], "| Mehrkosten", v["mehrkosten_mrd"], "Mrd. €,", v["mehrkosten_pct_bip"], "% BIP")
    print("kleine Bestandsrenten", E["kleine_bestandsrenten"])
    for k, v in E["lebensarbeitszeit"].items():
        print("Kopplung", k, v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
