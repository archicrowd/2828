#!/usr/bin/env python3
"""Zahlen der Länderseiten (Fassung 4.x): Drittel-System je Referenzland der Sprachversionen (Logbuch v4.1). Prüfrechnung.

Je Staat (FR, IT, ES, PL; DE als Abgleich; EU30 = Durchschnitt der 30 Staaten des Möglichkeitsraums für die englische Fassung):
  - Transformationsdividende je Erwachsenem 2028–2060 (Euro des Landes, Kaufkraft 2026): deutscher Pfad (netz33, Beschluss) mal Verhältnis
    Land/Deutschland aus dem Modell des Möglichkeitsraums, jahrweise gerechnet (moeglichkeitsraum33.land mit den Trends des Jahres);
  - Geldfluss je 100 € Steuern (Dach, Gemeinde, Netz, Dividende), deutscher Pfad plus Differenz Land − Deutschland in Punkten des BIP;
  - Gemeindeformel je Einwohner und je Kind nach eigener Wirtschaftsleistung je Kopf (Regel des Bauplans);
  - Grundbedarf und Tarifstufen (1/1,5/2/3 × Grundbedarf);
  - eigener Altlastenfonds: Schuld 2028 (Fortschreibung, laender_daten.toml) + Altrenten, Tilgung bis 2098, Zuschlag auf alle Steuern, Pfad.
Mindestrente: Anlauf wie im deutschen Pfad (Anteil der Grundrente 2028–2060 an ihrem Dauerwert), Annahme.
Ausgabe: daten/aggregate/laenderseiten.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "laenderseiten.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("mr", W / "modell" / "moeglichkeitsraum33.py")
MR = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(MR)
NZ = json.loads((AGG / "netz33.json").read_text(encoding="utf-8"))
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
NB = {r["jahr"]: r for r in NZ["beschluss"]["reihe"]}
# v4.17 (Beschluss 20.10.2026, Prüfbericht B11): auf allen Seiten gilt der gemeinsame Fonds (Beschluss altlasten.json); der eigene Fonds
# je Staat bleibt als Vergleich („fonds_eigen“).
AL = json.loads((AGG / "altlasten.json").read_text(encoding="utf-8"))["beschluss"]   # Verrechnung je Staat (zehn)
FG = json.loads((AGG / "fonds_geltend.json").read_text(encoding="utf-8"))   # v4.20: geltender Fonds der 30
DNAME = {"DE": "Deutschland", "FR": "Frankreich", "ES": "Spanien", "IT": "Italien", "PL": "Polen"}
JAHRE = list(range(2028, 2061))
GR = "Grundrente (ab 67)"


def rahmen_j(j, mr_dauer):
    """Rahmen des Jahres j (wie moeglichkeitsraum33.rahmen, aber für jedes Jahr); Mindestrente mit Anlaufgewicht."""
    r = MR.R[j]
    w = min(1.0, NB[j]["positionen"][GR] / mr_dauer) if mr_dauer else 0.0
    return dict(deck=r["deckung"] + r["progression"], dach=r["dach_ohne_zins"],
                gem=MR.V["quote_kern"] - r["dach_ohne_zins"] - r["dividende_ohne_trends_pct_bip"],
                gp=r["gesundheit_plus"], alter=w, f=r["wachstum_je_kopf_faktor"])


def land_j(c, j, mr_dauer):
    """moeglichkeitsraum33.land für das Jahr j (Mindestrente mit Gewicht w statt 0/1)."""
    alt = MR.rahmen
    ra = rahmen_j(j, mr_dauer)
    w = ra["alter"]
    MR.rahmen = lambda z: dict(ra, alter=True)
    try:
        voll = MR.land(c, "x")
    finally:
        MR.rahmen = alt
    MR.rahmen = lambda z: dict(ra, alter=False)
    try:
        ohne = MR.land(c, "x")
    finally:
        MR.rahmen = alt
    # lineare Mischung zwischen ohne und mit voller Mindestrente
    mix = lambda a, b: a + (b - a) * w
    return dict(dividende_pct_bip=mix(ohne["dividende_pct_bip"], voll["dividende_pct_bip"]),
                dividende_erw_eur=mix(ohne["dividende_erw_eur"], voll["dividende_erw_eur"]),
                netz_pct_bip=mix(ohne["netz_pct_bip"], voll["netz_pct_bip"]), deckung_pct_bip=voll["deckung_pct_bip"],
                grundbedarf_monat_eur=voll["grundbedarf_monat_eur"])


def fonds(c, d0):
    """Eigener Altlastenfonds (wie moeglichkeitsraum33.altlasten), Startschuld d0 = Fortschreibung 2028; Pfad 2028–2098."""
    rente = MR.D["gf1002"][c] + MR.D["gf1003"][c]
    pv = sum(rente * MR.SZ.z_anteil_vor_stichtag(j) / 1.01 ** (j - 2028) for j in range(2028, 2101))
    rente = rente * min(1.0, MR.D["s13pu_2021"][c] / pv)
    a = MR.land(c, "2028")
    z = [x["z_pct_bip"] for x in MR.SZ.z_pfad(c, rente, MR.D["anteil65"][c], a["div_erw_pct_kopf"], lambda j: 1.0)]
    i, g = MR.P["zins"] / 100, MR.P["wachstum_nominal"] / 100

    def pf(cc):
        d, o = d0, []
        for t in range(2098 - 2028):
            d = d * (1 + i) / (1 + g) + (z[t] if t < len(z) else 0) - cc
            o.append(d)
        return o
    lo, hi = -5.0, 30.0
    for _ in range(80):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if pf(m)[-1] > 0 else (lo, m)
    p = pf(hi)
    return dict(beitrag_pct_bip=round(hi, 2), zuschlag_pct=round(hi / a["deckung_pct_bip"] * 100, 1), spitze=round(max(p)),
                spitzenjahr=2029 + p.index(max(p)), pfad={str(2029 + t): round(v, 1) for t, v in enumerate(p)}, z_2028=round(z[0], 2))


def main():
    mr_dauer_de = MR.land("DE", "dauer")["netz"]["Mindestrente"]
    laender = list(MR.LAENDER)
    roh = {c: {j: land_j(c, j, mr_dauer_de) for j in JAHRE} for c in laender}
    ew = {c: float(MR.EW[c]["einwohner_mio"]) for c in laender}
    bip = {c: MR.D["bip_mio_eur"][c] for c in laender}
    sw, sb = sum(ew.values()), sum(bip.values())
    # EU30: Dividende einwohnergewichtet (Euro), Anteile BIP-gewichtet
    roh["EU30"] = {j: dict(dividende_erw_eur=sum(ew[c] * roh[c][j]["dividende_erw_eur"] for c in laender) / sw,
                           **{k: sum(bip[c] * roh[c][j][k] for c in laender) / sb for k in ("dividende_pct_bip", "netz_pct_bip", "deckung_pct_bip")},
                           grundbedarf_monat_eur=sum(ew[c] * roh[c][j]["grundbedarf_monat_eur"] for c in laender) / sw) for j in JAHRE}
    kopf_klub = MR.kopf["DE"] / G["f_de"]                                       # Kopf des Klubs der zehn (Bezug der Gemeindeformel), 2024
    kopf = dict(MR.kopf, EU30=sb / sw)
    erg = {}
    for c in P["staaten"]:
        de, x = roh["DE"], roh[c]
        div = [round(NB[j]["dividende_erw_eur2026"] * x[j]["dividende_erw_eur"] / de[j]["dividende_erw_eur"], 1) for j in JAHRE]
        f = kopf[c] / kopf_klub
        e = dict(name=P["namen"][c], dividende_erw_eur=div, kind_2028=round(div[0] / 2, 1),
                 dividende_pct_bip=[round(NB[j]["dividende_pct_bip"] + x[j]["dividende_pct_bip"] - de[j]["dividende_pct_bip"], 3) for j in JAHRE],
                 netz_pct_bip=[round(NB[j]["netz_pct_bip"] + x[j]["netz_pct_bip"] - de[j]["netz_pct_bip"], 3) for j in JAHRE],
                 deckung_delta_pct_bip=[round(x[j]["deckung_pct_bip"] - de[j]["deckung_pct_bip"], 3) for j in JAHRE],
                 grundbedarf_jahr_eur=round(x[2028]["grundbedarf_monat_eur"] * 12),
                 gemeinde_einw=round(G["formel_einw"] * f), gemeinde_kind=round(G["formel_kind"] * f), f_kopf=round(f, 4))
        e["tarif_stufen"] = [round(e["grundbedarf_jahr_eur"] * m) for m in (1, 1.5, 2, 3)]
        if c != "EU30":
            d0 = P["schuld_2028"][c]
            e["fonds_eigen"] = fonds(c, d0)
            e["fonds_eigen"]["start_2028"] = d0
            vr = AL["laender"].get(DNAME.get(c, ""), {}).get("reihe", {}).get("2028")
            e["fonds"] = dict(abgrenzung="gemeinsamer Fonds der 30 Staaten (Beschluss 21.10.2026)", beitrag_pct_bip=FG["beitrag_pct_bip"],
                              zuschlag_pct=FG["zuschlag_auf_alle_steuern_pct"], spitze=FG["schuldenquote_spitze"], spitzenjahr=FG["spitzenjahr"],
                              zieljahr=FG["zieljahr"], zins=FG["zins"], verrechnung_2028_zehn=vr,
                              hinweis="gleicher Satz für alle (vereinfachend wie im Beschluss); Verrechnung je Staat nur für die zehn gerechnet")
        erg[c] = e
    erg["DE"]["abgleich"] = "DE-Pfad identisch mit netz33 (Verhältnis 1)"
    E = dict(version=P["version"], status="Prüfrechnung", jahre=JAHRE, staaten=erg,
             hinweis="Dividende: deutscher Beschlusspfad × Verhältnis Land/DE aus dem Möglichkeitsraum-Modell (jahrweise). Anteile: DE-Pfad + Differenz Land−DE. "
                     "Gemeindeformel nach BIP je Kopf 2024 relativ zum Klub der zehn. Fonds: gemeinsamer Fonds (Beschluss) geltend, eigener Fonds mit Startschuld 2028 aus laenderseiten.toml als Vergleich (fonds_eigen). Euro des Landes, Kaufkraft 2026.")
    (AGG / "laenderseiten.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{'Staat':<8}{'Div28':>7}{'Div35':>7}{'Div60':>7}{'Netz28':>8}{'Div%28':>8}{'Gem/Einw':>9}{'Kind':>7}{'GB/Jahr':>9}{'Zuschl':>8}{'Spitze':>8}")
    for c, e in erg.items():
        fz = e.get("fonds_eigen", {})
        print(f"{c:<8}{e['dividende_erw_eur'][0]:>7.0f}{e['dividende_erw_eur'][7]:>7.0f}{e['dividende_erw_eur'][-1]:>7.0f}{e['netz_pct_bip'][0]:>8.2f}"
              f"{e['dividende_pct_bip'][0]:>8.2f}{e['gemeinde_einw']:>9}{e['gemeinde_kind']:>7}{e['grundbedarf_jahr_eur']:>9}"
              f"{fz.get('zuschlag_pct', '–'):>8}{fz.get('spitze', '–'):>8}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
