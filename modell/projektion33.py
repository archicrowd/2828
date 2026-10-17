#!/usr/bin/env python3
"""Zeitpfad des Drittel-Systems 33F, 2028–2060, mit belegten Trends (Logbuch v3.47). Prüfrechnung, keine Prognose.

Was sich bewegt (Pfade in projektion33.toml):
  1. Sonderstufe Mehrwertsteuer: Verbrenneranteil der Fahrzeugausgaben und Kraftstoffausgaben sinken (Flottenwechsel); weggefallene
     Kraftstoffausgaben gehen teils als Fahrstrom (22 %), teils in den übrigen Konsum. Alkohol und Tabak sinken langsam.
  2. CO₂-Preis: Aufkommen sinkt mit den Emissionen. Energiesteuer auf Kraftstoffe sowie Tabak- und Alkoholsteuer folgen den Indizes.
  3. Gesundheit und Pflege: steigen mit der Alterung (Ageing Report 2024).
Was gleich bleibt: Sätze, Dach und Gemeinden in % des BIP, Seil, Härtefall, übrige Positionen der Deckung, Saldo +0,12.
Die Dividende ist der Rest (% des BIP); in Euro wächst sie mit der Wirtschaftsleistung je Einwohner. Prüfung gegen das Mindestniveau.
Altlasten (Staatsschulden, Altrenten) liegen außerhalb und sind Sache der Staaten (Beschluss der Initiative, Stand v3.47).
Ausgabe: daten/aggregate/projektion33.json
"""
import contextlib, importlib.util, io, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "projektion33.toml").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("sv", W / "modell" / "systemvarianten.py")
SVM = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(SVM)
SV = json.loads((AGG / "systemvarianten.json").read_text(encoding="utf-8"))
v = next(x for x in SV["varianten"] if x["id"] == P["system"])
sy = next(x for x in SVM.P["system"] if x["id"] == P["system"])


TEXTE = dict(
    verkehr_k="Neuwagen 2025: 17,4 % elektrisch, 2026 schon über 21 %",
    verkehr_p="Ab 2035 sollen neue Pkw kein CO₂ mehr ausstoßen (EU-Recht; eine Lockerung auf 90 % ist vorgeschlagen). Der Bestand folgt mit "
              "Abstand: Die Emissionen des Verkehrs sinken laut Projektion bis 2040 auf ein Drittel. Kraftstoffe und Verbrenner zahlen im Label 33 % – "
              "diese Einnahmen sinken mit dem Erfolg.",
    alter_p="Mehr ältere Menschen brauchen mehr Versorgung, vor allem in der Pflege. Wir rechnen mit dem Referenzszenario der EU-Kommission "
            "(Ageing Report 2024).")


def lin(name, j):
    s = P["pfad"][name]["stuetz"]
    if j <= s[0][0]:
        return s[0][1]
    for (a, x), (b, y) in zip(s, s[1:]):
        if a <= j <= b:
            return x + (y - x) * (j - a) / (b - a)
    return s[-1][1]


def label(j, ohne_sonder=False):
    """Effektiver Satz (wie systemvarianten.label_effektiv) mit Gewichten und Sätzen des Jahres j."""
    stufe = {5: 0, 11: 1, 17: 2, 22: 3, 28: 4}
    st = SVM.NFT["label_steuernd"]
    saetze, sonder = sy["label_saetze"], dict(sy["label_sonder"])
    pfl = [g for g in SVM.NFT["gruppe"] if g["label"] > 0]
    w = {g["id"]: (g["q1"] + g["q5"]) / 2 for g in pfl}
    satz = {}
    for g in pfl:
        alt = st.get(g["id"], g["label"])
        satz[g["id"]] = saetze[stufe[alt]] if alt in stufe else alt * saetze[4] / 28
        if g["id"] in sonder:
            satz[g["id"]] = sonder[g["id"]]
    vb = lin("verbrenner_fahrzeuge", j)
    satz["fahrzeuge"] = saetze[4] if ohne_sonder else 33 * vb + saetze[4] * (1 - vb)          # Mischsatz wie in 33F (0,8 → 32 %)
    w0 = dict(w)
    w["kraftstoffe"] = w0["kraftstoffe"] * lin("kraftstoffe", j)
    w["alkohol_tabak"] = w0["alkohol_tabak"] * lin("alkohol_tabak", j)
    frei = (w0["kraftstoffe"] - w["kraftstoffe"]) + (w0["alkohol_tabak"] - w["alkohol_tabak"])
    strom = (w0["kraftstoffe"] - w["kraftstoffe"]) * P["fahrstrom_anteil"]
    w["haushaltsenergie"] += strom
    rest = frei - strom                               # anteilig auf alle übrigen Gruppen
    andere = [k for k in w if k not in ("kraftstoffe", "alkohol_tabak")]
    s_andere = sum(w[k] for k in andere)
    for k in andere:
        w[k] += rest * w[k] / s_andere
    return sum(w[k] * satz[k] for k in w) / sum(w.values())


def konsum_ohne_sonder(j):
    """Konsumaufkommen des Jahres j, wenn die Sonderstufe nicht gälte (Kraftstoffe und Fahrzeuge 28 %, Alkohol und Tabak 28 %)."""
    alt = dict(sy["label_sonder"])
    sy["label_sonder"] = {"alkohol_tabak": 28, "kraftstoffe": 28, "fahrzeuge": 28}
    try:
        e = label(j, ohne_sonder=True)
    finally:
        sy["label_sonder"] = alt
    return KONSUM_EICH * SVM.konsum(e)


def main():
    global KONSUM_EICH
    pos, eff0 = SVM.deckung(sy)
    deck0 = sum(pos.values())
    eff_check = label(2028)
    KONSUM_EICH = SVM.konsum(eff0) / SVM.konsum(eff_check)
    k = SVM.G["anteil_minderjaehrige"] / 100
    div0 = v["dividende_pct_bip_2028"]
    bedarf_ohne_div = v["punkte"]["2028"]["steuerbedarf"] - div0
    saldo = v["punkte"]["2028"]["saldo"]
    f = P["preis_2026_zu_2028"]
    eur0 = v["dividende_de_erw_2028"] / f
    mind = v["mindestniveau_de_erw_monat"] / f
    # Grundpfad der Gesamtrechnung mit der Quote von 33F (Dach mit Verteidigungspfad, Zinsen außerhalb, Wachstum je Kopf der Gesamtrechnung)
    basis = {r["jahr"]: r for r in SVM.GR.pfad(v["quote_kern"], i_alt=0.0, i_ziel=0.0)}
    f_erw = SVM.GR.F_DE / (1 - k / 2) / f                          # Klub je Einwohner (Preise 2028) -> DE je Erwachsenem (Euro 2026)
    reihe = []
    for j in range(P["jahre"][0], P["jahre"][1] + 1):
        eff = label(j)
        konsum = SVM.konsum(eff) * KONSUM_EICH                           # auf den Ausgangswert geeicht
        co2 = pos["CO₂-Preis"] * lin("co2_index", j)
        verbr = (P["energiesteuer_kraftstoffe_pct_bip"] * (1 - lin("kraftstoffe", j))
                 + P["tabak_alkohol_steuer_pct_bip"] * (1 - lin("alkohol_tabak", j)))   # Rückgang gegen 2028
        deck = deck0 - pos["Konsum (Label)"] - pos["CO₂-Preis"] + konsum + co2 - verbr
        gp = lin("gesundheit_pflege_plus", j)
        erosion = deck0 - deck
        b = basis[j]
        div = b["div"] - erosion - gp
        eur_basis = b["kl_real"] * f_erw
        eur = eur_basis * div / b["div"]
        mind_pct = mind / eur_basis * b["div"]                         # Mindestniveau in % des BIP im Jahr j
        lenk = co2 + konsum - konsum_ohne_sonder(j) + P["energiesteuer_kraftstoffe_pct_bip"] * lin("kraftstoffe", j) \
            + P["tabak_alkohol_steuer_pct_bip"] * lin("alkohol_tabak", j)
        reihe.append(dict(jahr=j, lenkung_pct_bip=round(lenk, 2), luecke_mindestniveau_pct_bip=round(max(0.0, mind_pct - div), 2), label_effektiv=round(eff, 2), konsum=round(konsum, 2), co2=round(co2, 2), verbrauchsteuern_minus=round(verbr, 2), deckung=round(deck, 2),
                          gesundheit_plus=round(gp, 2), dach_ohne_zins=round(b['a'], 2), dividende_ohne_trends_pct_bip=round(b['div'], 2),
                          dividende_ohne_trends_eur2026=round(eur_basis), erosion=round(erosion, 2), dividende_pct_bip=round(div, 2), dividende_erw_eur2026=round(eur),
                          mindestniveau_eur2026=round(mind), ueber_mindestniveau=eur >= mind))
    # Variante Bürgerfonds: ein Teil der Lenkungseinnahmen wird angelegt, 3 % des Vermögens fließen in die Dividende
    fonds = []
    for phi in P["fonds_anteil"]:
        for rr in P["fonds_rendite"]:
            F, werte = 0.0, {}
            for r in reihe:
                L = r["lenkung_pct_bip"]
                dn = r["dividende_pct_bip"] - phi * L + P["fonds_entnahme"] * F
                werte[str(r["jahr"])] = round(r["dividende_ohne_trends_eur2026"] / r["dividende_ohne_trends_pct_bip"] * dn)
                F = F * (1 + rr) / (1 + P["fonds_wachstum"]) + phi * L - P["fonds_entnahme"] * F
            fonds.append(dict(anteil=phi, rendite=rr, dividende_erw_eur2026={j: werte[j] for j in ("2028", "2035", "2045", "2060")},
                              fondsvermoegen_2060_pct_bip=round(F, 1)))
    E = dict(version=P["version"], system=P["system"], preisbasis="Euro 2026; Dividende je Erwachsenem und Monat, Deutschland",
             ausgang=dict(deckung=round(deck0, 2), label_effektiv=round(eff0, 2), dividende_pct_bip=div0, dividende_erw_eur2026=round(eur0)),
             reihe=reihe, buergerfonds=fonds, texte=TEXTE, annahmen={k_: P["pfad"][k_]["stuetz"] for k_ in P["pfad"]},
             wachstum_real_kopf=round(SVM.GR.G_REAL * 100, 2) if hasattr(SVM.GR, 'G_REAL') else None, fahrstrom_anteil=P["fahrstrom_anteil"],
             hinweis="Prüfrechnung: Pfade aus Quellen gesetzt (siehe Logbuch v3.47), keine Rückwirkung auf Wachstum und Arbeitsangebot")
    (AGG / "projektion33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Ausgang: Deckung {deck0:.2f}, Label {eff0:.2f} (Prüfung {eff_check:.2f}), Dividende {div0} % = {eur0:.0f} € (2026), Mindest {mind:.0f} €")
    for x in fonds:
        print("Bürgerfonds", x)
    for r in reihe:
        if r["jahr"] in (2028, 2030, 2035, 2040, 2045, 2050, 2060):
            print(r["jahr"], "Lenkung", r["lenkung_pct_bip"], "Erosion", r["erosion"], "Gesundheit+", r["gesundheit_plus"], "Div %", r["dividende_ohne_trends_pct_bip"],
                  "->", r["dividende_pct_bip"], "| € ohne Trends", r["dividende_ohne_trends_eur2026"], "mit", r["dividende_erw_eur2026"],
                  "| Lücke zum Mindestniveau", r["luecke_mindestniveau_pct_bip"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
