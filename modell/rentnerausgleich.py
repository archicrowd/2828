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
P["zuschlag_pct"] = round(json.loads((AGG / "fonds_geltend.json").read_text(encoding="utf-8"))["zuschlag_haushalte"]["laender"]["DE"]["2028"], 1)   # v4.38 (E11): DE 2028   # v4.11; v4.20 Fonds der 30
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
    zu = P["zuschlag_pct"] if zuschlag is None else zuschlag
    r = H.kuerze(12 * r_monat, kuerzung)                 # v4.26: ohne Angabe Regel E (haushalte33.rente_regel), sonst flacher Vergleichssatz
    st = H.est(r * steueranteil)
    y = r - st + 12 * pauschale
    eff = H.eff_jahr(2028)
    konsum = H.kq(y) * y
    fm, fb = H.MV.faktoren(y)                                                            # v4.29
    n = y - fm * konsum * ((1 + eff / 100) / (1 + H.EFF_ALT / 100) - 1) - zu / 100 * (st + fb * konsum * eff / (100 + eff))
    g = H.P.get("grundauskommen_rentner")
    if boden or g:                                   # v4.11 B1: Grundauskommen auch für Bestandsrenten (volle Anrechnung)
        n = max(n, 12 * g["neu_monat"] if g else GB)
    return n


def varianten():
    v = {"Beschluss v4.26 (Regel E: 15 % über dem Grundbedarf, Boden 1.083 €)": {r: neu(r) for r in P["renten_monat"]}}
    for k in P["varianten_kuerzung"]:
        v[f"Kürzung {k * 100:.1f} %".replace(".", ",")] = {r: neu(r, kuerzung=k) for r in P["renten_monat"]}
    v["Besteuerungsanteil 83 % wie heute"] = {r: neu(r, steueranteil=0.83) for r in P["renten_monat"]}
    v["Befreiung vom Altlastenzuschlag"] = {r: neu(r, zuschlag=0.0) for r in P["renten_monat"]}
    for p in P["pauschale_monat"]:
        v[f"Pauschale {p} € steuerfrei"] = {r: neu(r, pauschale=p) for r in P["renten_monat"]}
    out = {}
    for name, w in v.items():
        diff = {str(r): round((w[r] - heute(r)) / 12) for r in P["renten_monat"]}
        mittel = sum((w[r] - neu(r)) for r in P["renten_monat"]) / len(P["renten_monat"])   # Mehrkosten je Rentner/Jahr gegen Beschluss
        mrd = mittel * P["rentner_mio"] * 1e6 / 1e9
        out[name] = dict(differenz_monat_je_rente=diff, mehrkosten_mrd=round(mrd, 1), mehrkosten_pct_bip=round(100 * mrd / P["bip_mrd_2028"], 2))
    return out


def heute_ohne_gs(r_monat):
    g = H.P.pop("grundauskommen_rentner", None)
    try:
        return H.rentner(r_monat, P["zuschlag_pct"], 2028)[0]
    finally:
        if g:
            H.P["grundauskommen_rentner"] = g


def kleine_renten():
    out = {}
    for r in (600, 900, 1200):
        g = H.P.pop("grundauskommen_rentner", None)
        n0 = neu(r)
        if g:
            H.P["grundauskommen_rentner"] = g
        out[str(r)] = dict(neu_ohne_grundauskommen=round(n0 / 12), neu_mit_grundauskommen=round(neu(r) / 12), grundbedarf=round(GB / 12),
                           heute_ohne_grundsicherung=round(heute_ohne_gs(r) / 12), heute_mit_grundsicherung=round(heute(r) / 12))
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


def zerlegung():
    """v4.11: Beitrag des gemeinsamen Altlastenfonds (% BIP) je Schritt des Rentnerpakets (A Kürzung 7,5 %, T1 anteilig, B1, L1)."""
    spec_a = importlib.util.spec_from_file_location("al", W / "modell" / "altlasten.py")
    AL = importlib.util.module_from_spec(spec_a)
    with contextlib.redirect_stdout(io.StringIO()):
        spec_a.loader.exec_module(AL)
    SZ, B = AL.SZ, AL.P["beschluss"]
    k = AL.G["anteil_minderjaehrige"] / 100
    vb = next(x for x in AL.SV["varianten"] if x["id"] == B["system"])
    r0 = dict(SZ.P.get("rentner", {}))

    def beitrag(kuerzung, anteilig, b1, kopplung):
        SZ.KUERZUNG = kuerzung
        SZ.P["rentner"] = dict(r0, anteilige_verrechnung=anteilig, grundauskommen_bestand_pct_bip=b1, kopplung=kopplung)
        zb = [x * B["z_anteil"] for x in SZ.z_klub(vb["dividende_pct_bip_2028"] / (1 - k / 2), SZ.gewicht())]
        return AL.loese_c(zb, B["zins"] / 100, AL.G["schuldenquote_2028"], B["zieljahr"], B["zielquote"])
    schritte = [("vorher (v4.10: Kürzung 12,35 %, volle Verrechnung, ohne B1, ohne Kopplung)", (0.1235, False, 0.0, 0.0)),
                ("+ A: Kürzung 7,5 %", (0.075, False, 0.0, 0.0)),
                ("+ T1: anteilige Verrechnung", (0.075, True, 0.0, 0.0)),
                ("+ B1: Grundauskommen im Bestand", (0.075, True, P["b1_v411"], 0.0)),
                ("+ L1: Rentenbeginn ⅔ gekoppelt (= Beschluss v4.11)", (0.075, True, P["b1_v411"], r0.get("kopplung", 0.0))),
                ("+ E: 15 % über dem Grundbedarf, Boden 1.083 € (= Beschluss v4.26)", (AL.P["kuerzung"], True,
                                                                                       r0.get("grundauskommen_bestand_pct_bip", 0.0), r0.get("kopplung", 0.0))),
                ("+ R6: Kürzungssatz je Staat (= v4.37)", (SZ.kuerzung_aus(AL.P), True, r0.get("grundauskommen_bestand_pct_bip", 0.0), r0.get("kopplung", 0.0)))]
    out, vor = [], None
    for name, a in schritte:
        c = beitrag(*a)
        out.append(dict(schritt=name, beitrag_pct_bip=round(c, 2), aenderung=round(c - vor, 2) if vor is not None else None))
        vor = c
    # v4.37 (R6): Preis von T1 unter den geltenden Regeln (E, je Staat, B1, L1): ohne anteilige Verrechnung
    ohne = beitrag(SZ.kuerzung_aus(AL.P), False, r0.get("grundauskommen_bestand_pct_bip", 0.0), r0.get("kopplung", 0.0))
    out.append(dict(schritt="Prüfung T1 (v4.37): geltend ohne anteilige Verrechnung", beitrag_pct_bip=round(ohne, 2), aenderung=round(ohne - vor, 2)))
    SZ.P["rentner"] = r0
    return out


def main():
    E = dict(version=P["version"], status="Prüfrechnung, grob", varianten=varianten(), kleine_bestandsrenten=kleine_renten(),
             lebensarbeitszeit=lebensarbeitszeit(), fonds_zerlegung=zerlegung(),
             grundsicherung_heute=dict(empfaenger_ab_altersgrenze=P["grundsicherung_alter_empfaenger"], ausgaben_mrd_alter_und_em=P["grundsicherung_ausgaben_mrd"]),
             hinweis="DE 2028, Kaufkraft 2026, Monatsbeträge. Mehrkosten = Mittel über die vier Beispielrenten × 18 Mio. Rentner (grob, ohne "
                     "Rentenverteilung). Lebensarbeitszeit: Entlastung von Altlastenfonds (Z, z_pfad.csv) und Mindestrente (netz33) durch späteren "
                     "Rentenbeginn; ohne zusätzliche Steuern aus längerer Arbeit (vorsichtig).")
    (AGG / "rentnerausgleich.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in E["varianten"].items():
        print(f"{k:<50}", v["differenz_monat_je_rente"], "| Mehrkosten", v["mehrkosten_mrd"], "Mrd. €,", v["mehrkosten_pct_bip"], "% BIP")
    print("kleine Bestandsrenten", E["kleine_bestandsrenten"])
    for z in E["fonds_zerlegung"]:
        print("Fonds", z)
    for k, v in E["lebensarbeitszeit"].items():
        print("Kopplung", k, v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
