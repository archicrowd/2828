#!/usr/bin/env python3
"""Ländervergleich nach den Kriterien der Webseite (Logbuch v3.28).

Rechnet je Land die Größen, die die Webseite kommuniziert:
  Dividende je Erwachsenem und je Kind 2028; Tarifstufen am Grundbedarf (höchstens 28 %); Musterhaushalte mit der
  Rechenregel des Rechners der Seite (Funktion steuer in seite/werkzeuge/vorlage.html: Stufentarif auf das Brutto, kein
  Splitting, Sozialabgaben 0, Dividende Erwachsene voll und Kinder halb); Gemeindebudget je Einwohner und je Kind;
  heutige Last (Abgabenkeil, Kapitalertragsteuer, Spitzensatz, Sozialbeiträge, soweit belegt); Staatsschulden.
Beträge: Euro 2028, nominal. Keine neue Annahme des Konzepts; alle Größen stammen aus den Ergebnissen der Gesamtrechnung,
der Ländervarianten, des Tarifs am Grundbedarf und der Länderrechnung nach Standard.

Eingänge: modell/laender/vergleich.toml, daten/aggregate/{gesamtrechnung,laendervarianten,tarif_grundbedarf}.json,
          preisniveau_2024.csv, laender_2024.csv, schulden_2010_2025.csv, laender/<cc>.json
Ausgabe:  daten/aggregate/laendervergleich.json, daten/aggregate/laendervergleich.csv
"""
import csv, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell/laender/vergleich.toml").read_text(encoding="utf-8"))
GR = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
TG = json.loads((AGG / "tarif_grundbedarf.json").read_text(encoding="utf-8"))
LV = {z["land"]: z for z in json.loads((AGG / "laendervarianten.json").read_text(encoding="utf-8"))["zeilen"]}
G28, SAETZE = float(TG["grundbedarf_2028"]), [float(s) for s in TG["saetze"]]
G_NOM = float({p["name"]: p["wert"] for p in tomllib.loads((W / "modell/gesamtrechnung.toml").read_text(encoding="utf-8"))["parameter"]}["wachstum_nominal"])


def lies_csv(name, schluessel="land"):
    with open(AGG / name, encoding="utf-8") as f:
        return {r[schluessel]: r for r in csv.DictReader(f)}


PLI = {k: float(v["preisniveau_eu27_100"]) for k, v in lies_csv("preisniveau_2024.csv").items()}
STAMM = lies_csv("laender_2024.csv")
SCHULD = lies_csv("schulden_2010_2025.csv")
PLI_DE = PLI["DE"]
KEIL = lies_csv("abgabenkeil_2024.csv")                     # OECD Taxing Wages 2025 (seit v3.30)
ANR = json.loads((AGG / "anreize.json").read_text(encoding="utf-8"))["laender"]


def steuer(x, stufen):
    """Wie der Rechner der Seite: Grenzen (obere Grenze je Satz), Sätze 0 / 9 / 16 / 21 / 28 %."""
    grenzen = list(stufen) + [float("inf")]
    s, u = 0.0, 0.0
    for g, p in zip(grenzen, SAETZE):
        if x > u:
            s += (min(x, g) - u) * p / 100
        u = g
    return s


def standard(cc):
    p = AGG / "laender" / f"{cc.lower()}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def land(cc):
    luecken, st = [], standard(cc)
    # Preisniveau
    if cc in PLI:
        pli, pli_q = PLI[cc], "preisniveau_2024.csv (Eurostat prc_ppp_ind, A01)"
    elif st and "preisniveau_2024" in st["wohnort"]:
        pli, pli_q = st["wohnort"]["preisniveau_2024"], f"laender/{cc.lower()}.json (Standard 2.6)"
    else:
        return None
    f = pli / PLI_DE
    stufen = [round(G28 * f * k) for k in TG["vielfache"]]
    if cc in TG["stufen_laender_2028"] and TG["stufen_laender_2028"][cc] != stufen:
        sys.exit(f"{cc}: Tarifstufen weichen von tarif_grundbedarf.json ab")
    boden = float(GR["anker_de"]) * f
    if cc in LV:
        if abs(LV[cc]["div_v3b"] - boden) > 0.01:
            sys.exit(f"{cc}: Dividendenboden weicht von laendervarianten.json ab")
        # seit v3.38 (Entscheidung E2): V2, gleicher Anteil am eigenen BIP je Kopf (gesamtrechnung.json, tabelle_laender_div)
        v2 = next((r for r in GR["tabelle_laender_div"] if r["land"] == cc), None)
        if v2 and "v2_e2028" in v2:
            div, div_art = v2["v2_e2028"], "ausgezahlt (V2, gleicher Anteil am eigenen BIP je Kopf)"
        else:
            div, div_art = LV[cc]["div_v3a"], "ausgezahlt (V3a, Klubtopf nach Einwohnern x Preisniveau)"
    else:
        div, div_art = boden, "Boden (V3b, halbes Existenzminimum am Wohnort); V2 nur für die zehn Staaten der Gesamtrechnung"
        luecken.append("Dividende: nur Boden (V3b), keine ausgezahlte Dividende V2 (BIP je Kopf nicht in der Gesamtrechnung)")
    # Einwohner
    if cc in STAMM:
        einw, einw_q = float(STAMM[cc]["einwohner_mio_2024"]), "laender_2024.csv (Eurostat demo_gind, AVG 2024)"
    else:
        s = P.get("stamm", {}).get(cc, {})
        einw, einw_q = s.get("einwohner_mio"), s.get("einwohner_quelle")
    # Musterhaushalte
    muster = {}
    for m in P["muster"]:
        brutto = m["brutto_eur"] if "brutto_eur" in m else G28 * f * m["brutto_vielfaches_grundbedarf"]
        st_ = steuer(brutto, stufen)
        div_jahr = 12 * (m["erwachsene"] * div + m["kinder"] * div / 2)
        muster[m["id"]] = dict(brutto=round(brutto), einkommensteuer=round(st_), durchschnittssatz_pct=round(st_ / brutto * 100, 2),
                              sozialabgaben=0, dividende_jahr=round(div_jahr), dividende_minus_steuer=round(div_jahr - st_))
    # Gemeinde
    if cc in LV:
        gem = dict(je_einwohner_land=round(LV[cc]["gemeinde_je_einwohner_land"]), je_kind_land=round(LV[cc]["gemeinde_je_kind_land"]),
                   budget_je_kopf_land=round(LV[cc]["gemeinde_budget_je_kopf_land"]),
                   je_einwohner_klubformel=round(float(GR["formel_einw"])), je_kind_klubformel=round(float(GR["formel_kind"])),
                   hinweis="Land: Pro-Kopf-Variante des Länderbeitrags (Logbuch v3.17); Klubformel: wie auf der Webseite gezeigt")
    else:
        gem = None
        luecken.append("Gemeindebudget: nicht gerechnet (Land nicht in laendervarianten.json)")
    # Staatsschulden
    if cc in SCHULD:
        d25, s25 = float(SCHULD[cc]["2025"]), float(SCHULD[cc]["defizit_2025"])
    elif st:
        d25, s25 = st["ausgang"]["schuld_2025_pct_bip"], st["ausgang"]["saldo_2025_pct_bip"]
    else:
        d25 = s25 = None
    schuld = None
    if d25 is not None:
        d = d25
        for _ in range(3):
            d = d / (1 + G_NOM / 100) - s25
        schuld = dict(schuld_2025=d25, saldo_2025=s25, status_quo_2028=round(d, 2),
                      regierung_2028=(st["pfade"]["C_regierungsschuldenquote"].get("werte", {}).get("2028") if st else None),
                      regierungsdefizit_2028=(st["pfade"]["B_regierungsdefizit"]["werte"]["2028"] if st else None))
        if not st:
            luecken.append("Schulden: nur Status quo, Land noch nicht nach dem Standard gerechnet")
        elif schuld["regierung_2028"] is None:
            luecken.append("Schulden: keine Regierungsschuldenquote 2028 (Pfad C entfällt)")
    heute = dict(P.get("heute", {}).get(cc, {}))
    if cc in KEIL:
        heute["abgabenkeil_pct"] = float(KEIL[cc]["abgabenkeil_pct"])
        heute["abgabenkeil_quelle"] = "OECD Taxing Wages 2025, Tab. 1.2 (abgabenkeil_2024.csv)"
    if cc in ANR:
        heute["keil_2828_pct"] = ANR[cc]["keil_2828_pct"]
        heute["keil_2828_hinweis"] = ("Alleinstehende beim Durchschnittslohn, Arbeitskosten 2028 gleich, Einkommensteuer nach 28:28; "
                                      "ohne Konsumsteuern (wie OECD), daher überzeichnet der Vergleich die Entlastung (modell/anreize.py)")
    for k, lbl in (("abgabenkeil_pct", "Abgabenkeil"), ("kapital_pct", "Kapitalertragsteuer"),
                   ("spitzensatz_pct", "Spitzensatz Einkommensteuer"), ("sozialbeitraege_pct_bip", "Sozialbeiträge")):
        if k not in heute:
            luecken.append(f"heute: {lbl} nicht belegt")
    return dict(land=cc, name=P["namen"][cc], einwohner_mio=einw, einwohner_quelle=einw_q,
                preisniveau_2024=pli, preisniveau_quelle=pli_q, faktor_gegen_de=round(f, 4),
                dividende_erwachsener_monat=round(div, 2), dividende_kind_monat=round(div / 2, 2), dividende_art=div_art,
                dividende_boden_monat=round(boden, 2), tarifstufen=stufen, tarifsaetze_pct=SAETZE,
                muster=muster, gemeinde=gem, schulden=schuld, heute=heute, luecken=luecken)


def main():
    erg = [x for x in (land(cc) for cc in P["laender"]) if x]
    # Gegenprobe: Deutschland wie auf der Webseite (Dividende 2028 je Erwachsenem)
    de = next(x for x in erg if x["land"] == "DE")
    if abs(de["dividende_erwachsener_monat"] - float(GR["erw_de_2028"])) > 0.01:
        sys.exit("DE: Dividende weicht von gesamtrechnung.json (erw_de_2028) ab")
    E = dict(einheit="Euro 2028, nominal; Dividende je Monat; Steuer, Brutto und Dividende im Jahr",
             grundbedarf_de_2028=round(G28, 2), muster=P["muster"], oecd=P.get("heute", {}).get("OECD"), laender=erg,
             hinweis="Kaufkraftgleiche Musterhaushalte haben in jedem Land denselben Durchschnittssatz; Unterschiede entstehen "
                     "beim gleichen Eurobetrag (single_40000) und bei der Dividende (V3a gegen Boden).")
    (AGG / "laendervergleich.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    spalten = ["land", "name", "einwohner_mio", "preisniveau_2024", "dividende_erwachsener_monat", "dividende_kind_monat",
               "dividende_boden_monat", "stufe1", "stufe4"]
    for m in P["muster"]:
        spalten += [f"{m['id']}_steuer", f"{m['id']}_satz_pct", f"{m['id']}_dividende_minus_steuer"]
    spalten += ["gemeinde_je_einwohner_land", "gemeinde_je_kind_land", "schuld_2025", "schuld_2028_status_quo",
                "schuld_2028_regierung", "abgabenkeil_pct", "keil_2828_pct", "kapital_pct", "spitzensatz_pct", "sozialbeitraege_pct_bip", "luecken"]
    with open(AGG / "laendervergleich.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(spalten)
        for x in erg:
            row = [x["land"], x["name"], x["einwohner_mio"], x["preisniveau_2024"], x["dividende_erwachsener_monat"],
                   x["dividende_kind_monat"], x["dividende_boden_monat"], x["tarifstufen"][0], x["tarifstufen"][3]]
            for m in P["muster"]:
                mm = x["muster"][m["id"]]
                row += [mm["einkommensteuer"], mm["durchschnittssatz_pct"], mm["dividende_minus_steuer"]]
            g, s, h = x["gemeinde"] or {}, x["schulden"] or {}, x["heute"]
            row += [g.get("je_einwohner_land", ""), g.get("je_kind_land", ""), s.get("schuld_2025", ""), s.get("status_quo_2028", ""),
                    s.get("regierung_2028") or "", h.get("abgabenkeil_pct", ""), h.get("keil_2828_pct", ""), h.get("kapital_pct", ""),
                    h.get("spitzensatz_pct", ""), h.get("sozialbeitraege_pct_bip", ""), len(x["luecken"])]
            w.writerow(row)
    print(f"{'Land':<4}{'PLI':>7}{'Div Erw':>9}{'Stufe1':>8}{'40k Satz':>9}{'40k D-S':>9}{'Fam D-S':>9}{'Gem/Einw':>9}{'Schuld28 SQ':>12}{'Reg':>7}")
    for x in erg:
        m40, fam = x["muster"]["single_40000"], x["muster"]["familie_3gb"]
        s = x["schulden"] or {}
        print(f"{x['land']:<4}{x['preisniveau_2024']:>7.1f}{x['dividende_erwachsener_monat']:>9.2f}{x['tarifstufen'][0]:>8}"
              f"{m40['durchschnittssatz_pct']:>8.2f}%{m40['dividende_minus_steuer']:>9}{fam['dividende_minus_steuer']:>9}"
              f"{(x['gemeinde'] or {}).get('je_einwohner_land', ''):>9}{s.get('status_quo_2028', ''):>12}{str(s.get('regierung_2028') or ''):>7}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
