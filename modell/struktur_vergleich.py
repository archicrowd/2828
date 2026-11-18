#!/usr/bin/env python3
"""Strukturvergleich heute gegen Goldenes Drittel (Logbuch v4.99). Prüfrechnung, ändert die geltende Rechnung nicht.

Einnahmen nach Quelle: Arbeit, Kapital (einschließlich Vermietung, Boden, Erbschaft), Konsum; Ausgaben nach Zweck: Gemeinwesen, Unterstützung
(Gesundheit, laufende Geldleistungen, Alter, Dividende), Verwaltung, dazu Altlasten (Altrenten, Zinsen).
Spalten: EU-27 heute (Durchschnittsland, Kommission/Eurostat), Deutschland 2024 (Eurostat, eigene Zuordnung), Modellland Stand C 2028/2040/2050.
Das Modellland rechnet die Ausgaben als Schnitt der zehn Staaten (gesamtrechnung), die Einnahmen auf deutscher Basis (systemvarianten 33R).
Ausgabe: daten/aggregate/struktur_vergleich.json
"""
import json
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "struktur_vergleich.toml").read_text(encoding="utf-8"))
HP = tomllib.loads((W / "modell" / "haushaltsplan_de.toml").read_text(encoding="utf-8"))["eurostat_2024"]
SV = json.loads((AGG / "systemvarianten.json").read_text(encoding="utf-8"))
V = next(x for x in SV["varianten"] if x["id"] == "33R")
PJ = {r["jahr"]: r for r in json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))["reihe"]}
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
GL = json.loads((AGG / "gesamtlast33.json").read_text(encoding="utf-8"))
r2 = lambda x: round(x, 2)


def anteile(d):
    s = sum(d.values())
    return {k: round(v / s * 100, 1) for k, v in d.items()}


def einnahmen():
    Z = P["zuordnung"]
    # EU-27 heute
    E = P["eu27_einnahmen_2024"]
    eu = {k: E["steuerquote"] * E["anteil_" + k] / 100 for k in ("arbeit", "kapital", "konsum")}
    # Deutschland 2024 (Mrd. €)
    m = {k: v / 1000 for k, v in HP.items()}
    est_ohne_kap = m["D51A_C1"] - Z["kapitalertragsteuern_de_mrd"]
    kap_in_est = sum(Z["einkommen_kapital_pct_bip_neu"].values()) / V["deckung_positionen"]["Einkommen"]   # gleiche Aufteilung wie neu
    sb = m["D611"] + m["D613CE"] + m["D613CN"] + m["D613CS"] + m["D613V"] + m["D612"]
    nz = sum(Z["nicht_zugeordnet_mrd_2024"].values())
    de_mrd = dict(arbeit=est_ohne_kap * (1 - kap_in_est) + sb,
                  kapital=m["D51B_C2"] + Z["kapitalertragsteuern_de_mrd"] + est_ohne_kap * kap_in_est + m["D29A"] + Z["grunderwerb_mrd_2024"] + m["D91"],
                  konsum=m["D211"] + m["D2122C"] + m["D214A"] + m["D214G"] + m["D214_rest"] + m["D29F"] + Z["kfz_haushalte_mrd_2024"],
                  nicht_zugeordnet=nz)
    de = {k: v / Z["bip_2024_mrd"] * 100 for k, v in de_mrd.items()}
    # Modellland 2028 (Steuern, % BIP)
    p = V["deckung_positionen"]
    ek = Z["einkommen_kapital_pct_bip_neu"]
    gw = Z["grunderwerb_mrd_2024"] / Z["bip_2024_mrd"] * 100
    nz_neu = (Z["nicht_zugeordnet_mrd_2024"]["D29_rest"] + Z["nicht_zugeordnet_mrd_2024"]["D59_sonstige"]) / Z["bip_2024_mrd"] * 100
    neu = dict(arbeit=p["Einkommen"] - sum(ek.values()),
               kapital=p["Kapitalerträge"] + p["Unternehmen und Plattformen"] + p["Erbschaften"] + p["Große Vermögen"] + p["Grundstücksabgabe"] + sum(ek.values()) + gw,
               konsum=p["Konsum (Label)"] + p["CO₂-Preis"] + p["Übrige Steuern"] - gw - nz_neu,
               nicht_zugeordnet=nz_neu)
    subv = p["Subventionsabbau"]
    fonds = GL["fonds"]["beitrag_pct_bip"]
    zu = fonds / sum(neu.values())                         # Altlastenzuschlag auf alle Steuern, anteilig
    neu_f = {k: v * (1 + zu) for k, v in neu.items()}
    vorsorge = GL["pflichtvorsorge_route"]
    neu_b = dict(neu_f, arbeit=neu_f["arbeit"] + vorsorge)
    # Zeitpfad der Steuern im Modellland (Lenkung sinkt, Progression steigt)
    pfad = {}
    for j in (2028, 2040, 2050, 2060):
        r = PJ[j]
        d_konsum = (r["konsum"] - PJ[2028]["konsum"]) + (r["co2"] - PJ[2028]["co2"]) - r["verbrauchsteuern_minus"]
        pfad[str(j)] = dict(arbeit=r2(neu["arbeit"] + r["progression"]), kapital=r2(neu["kapital"]), konsum=r2(neu["konsum"] + d_konsum),
                            nicht_zugeordnet=r2(nz_neu), subventionsabbau=subv, lenkung=r["lenkung_pct_bip"],
                            summe=r2(sum(neu.values()) + subv + r["progression"] + d_konsum))
    return dict(
        eu27_2024=dict(pct_bip={k: r2(v) for k, v in eu.items()}, anteil_pct=anteile(eu), summe=E["steuerquote"]),
        de_2024=dict(mrd=dict({k: round(v, 1) for k, v in de_mrd.items()}), pct_bip={k: r2(v) for k, v in de.items()}, anteil_pct=anteile(de), summe=r2(sum(de.values()))),
        neu_2028_steuern=dict(pct_bip={k: r2(v) for k, v in neu.items()}, subventionsabbau=subv, anteil_pct=anteile(neu), summe=r2(sum(neu.values()) + subv)),
        neu_2028_mit_fonds=dict(pct_bip={k: r2(v) for k, v in neu_f.items()}, subventionsabbau=subv, zuschlag_pct=round(zu * 100, 1), summe=r2(sum(neu_f.values()) + subv)),
        neu_2028_mit_pflichtvorsorge=dict(pct_bip={k: r2(v) for k, v in neu_b.items()}, subventionsabbau=subv, anteil_pct=anteile(neu_b), summe=r2(sum(neu_b.values()) + subv)),
        neu_pfad_steuern=pfad, hilf=dict(kapitalanteil_einkommensteuer=round(kap_in_est, 3), grunderwerb_pct_bip=r2(gw), nicht_zugeordnet_neu_pct_bip=r2(nz_neu)))


def ausgaben():
    # EU-27 2023
    e = P["eu27_ausgaben_2023"]
    zins_eu = e["gesamt"] * e["zinsen_anteil_ausgaben"] / 100
    eu = dict(gemeinwesen=e["GF02"] + e["GF03"] + e["GF04"] + e["GF05"] + e["GF06"] + e["GF08"] + e["GF09"],
              verwaltung=e["GF01"] - zins_eu,
              gesundheit=e["GF07"], alter=e["GF1002"], geldleistungen_uebrige=e["GF10"] - e["GF1002"], dividende=0.0, zinsen=zins_eu)
    # Deutschland 2024
    m = {k: v / 1000 for k, v in HP.items()}
    b = P["zuordnung"]["bip_2024_mrd"]
    de_mrd = dict(gemeinwesen=m["GF02"] + m["GF03"] + m["GF04"] + m["GF05"] + m["GF06"] + m["GF08"] + m["GF09"],
                  verwaltung=m["GF01"] - m["GF0107"], gesundheit=m["GF07"], alter=m["GF1002"], geldleistungen_uebrige=m["GF10"] - m["GF1002"],
                  dividende=0.0, zinsen=m["GF0107"])
    de = {k: v / b * 100 for k, v in de_mrd.items()}
    # Modellland: Dach A (mit Verteidigungspfad), Gemeinden B, Netz, Dividende, Altlasten
    A = dict((n, v) for n, v, _ in G["tabelle_a"] if n != "Summe")
    B = dict((n, v) for n, v, _ in G["tabelle_b"] if n != "Summe")
    verw_namen = ("Kommunalverwaltung", "Außenbeziehungen", "Bildungs-, Markt- und Produktstandards", "Grundlagenforschung")
    seil, hf, gs = SV["seil"], SV["annahmen"]["haertefall_pct_bip"], SV["gesundheit"]
    pu = V["punkte"]
    neu = {}
    for j, key in ((2028, "2028"), (2040, "2040"), (2050, "2050")):
        r = PJ[j]
        vert = r["dach_ohne_zins"] - (sum(A.values()) - A["Verteidigung und digitale Souveränität"])   # Verteidigung im Jahr j
        gem = sum(v for n, v in {**A, **B}.items() if n not in verw_namen and not n.startswith("Verteidigung")) + vert
        verw = sum(v for n, v in {**A, **B}.items() if n in verw_namen)
        z = pu[key]["z"]
        zins = pu[key]["altlastenbeitrag"] - z
        neu[key] = dict(gemeinwesen=gem, verwaltung=verw, gesundheit=gs + r["gesundheit_plus"], alter=z, geldleistungen_uebrige=seil + hf,
                        dividende=r["dividende_pct_bip"], zinsen=zins)
    def form(d):
        unt = d["gesundheit"] + d["alter"] + d["geldleistungen_uebrige"] + d["dividende"]
        drei = dict(gemeinwesen=d["gemeinwesen"], unterstuetzung=unt, verwaltung=d["verwaltung"])
        return dict(einzeln={k: r2(v) for k, v in d.items()}, drei={k: r2(v) for k, v in drei.items()},
                    drei_ohne_altlasten=dict(gemeinwesen=r2(d["gemeinwesen"]), unterstuetzung=r2(unt - d["alter"]), verwaltung=r2(d["verwaltung"])),
                    anteil_drei_pct=anteile(drei), summe=r2(sum(d.values())))
    # Abdeckung je COFOG-Bereich: DE heute gegen Modellland 2028/2040 (Ausgaben der zehn), Kennzeichnung
    A_ = lambda n: A[n]; B_ = lambda n: B[n]
    vert28 = neu["2028"]["gemeinwesen"] - (sum(v for n, v in {**A, **B}.items() if n not in verw_namen and not n.startswith("Verteidigung")))
    abd = [
        ("Verteidigung (GF02)", m["GF02"] / b * 100, vert28, "Pfad 1,40 → 2,50 % bis 2035 (Entscheidung)"),
        ("Öffentliche Ordnung, Justiz (GF03)", m["GF03"] / b * 100, A_("Übergeordnete Polizei") + B_("Ordnung, Feuerwehr, Rettung"), "Gerichte und Strafvollzug nicht eigens abgebildet (offen)"),
        ("Wirtschaft und Verkehr (GF04)", m["GF04"] / b * 100, A_("Wirtschaftsraum, Agrar, Energie, Netze") + B_("Nahverkehr, Ortsstraßen"), "Kürzung 1,65 Punkte beschlossen (P8); Fernverkehrswege nicht eigens genannt (offen)"),
        ("Umwelt (GF05)", m["GF05"] / b * 100, A_("Umwelt, grenzüberschreitend") + B_("Wasser, Abwasser, Abfall"), "abgebildet"),
        ("Wohnen, Gemeinwesen (GF06)", m["GF06"] / b * 100, B_("Wohnen, Gemeinwesen"), "abgebildet"),
        ("Kultur, Sport (GF08)", m["GF08"] / b * 100, B_("Kultur, Sport, Gemeinschaft"), "abgebildet"),
        ("Bildung (GF09)", m["GF09"] / b * 100, B_("Schulen") + A_("Hochschulen"), "abgebildet (Kitas: Teil der Schulen oder der Familie, zu prüfen)"),
        ("Allgemeine Verwaltung ohne Zinsen (GF01)", (m["GF01"] - m["GF0107"]) / b * 100, sum(v for n, v in {**A, **B}.items() if n in verw_namen),
         "Ebene der Staaten (Parlamente, Ministerien, Steuer- und Finanzverwaltung, Statistik) und Beiträge an die EU nicht eigens abgebildet (offen)"),
        ("Gesundheit (GF07)", m["GF07"] / b * 100, gs, "Netz, Schnitt der zehn; steigt mit der Alterung"),
        ("Alter (GF1002)", m["GF1002"] / b * 100, neu["2028"]["alter"], "Altrenten Z im Fonds, laufen bis 2092 aus; neue Renten aus Pflichtvorsorge (eigenes Konto) und Dividende"),
        ("übrige Geldleistungen (GF10 ohne Alter)", (m["GF10"] - m["GF1002"]) / b * 100, seil + hf + neu["2028"]["dividende"], "Seil, Härtefall und Dividende ersetzen Familie, Grundsicherung, Wohngeld, Lohnersatz"),
        ("Zinsen (GF0107)", m["GF0107"] / b * 100, neu["2028"]["zinsen"], "Fonds (Altlasten)"),
    ]
    abdeckung = [dict(bereich=n, de_2024=r2(h), modell_2028=r2(x), differenz=r2(x - h), bemerkung=t) for n, h, x, t in abd]
    return dict(eu27_2023=form(eu), de_2024=dict(form(de), mrd={k: round(v, 1) for k, v in de_mrd.items()}),
                **{f"neu_{k}": form(v) for k, v in neu.items()}, abdeckung=abdeckung)


def main():
    ein, aus = einnahmen(), ausgaben()
    a28 = aus["neu_2028"]["summe"]
    steuern = ein["neu_2028_steuern"]["summe"]
    fonds = GL["fonds"]["beitrag_pct_bip"]
    finanz = dict(ausgaben_2028=a28, steuern_2028=steuern, fondsbeitrag=fonds, luecke_2028_fondskredit=r2(a28 - steuern - fonds),
                  fonds_neuaufnahme_2028_gesamtlast33=GL["c_ohne_fonds_2028_dynamisch"]["fonds_neuaufnahme"],
                  fonds_schuldenquote_spitze=GL["fonds"]["schuldenquote_spitze"], spitzenjahr=GL["fonds"]["spitzenjahr"], zieljahr=GL["fonds"]["zieljahr"])
    r28, r60 = PJ[2028], PJ[2060]
    zerl = dict(dividende_2028=r28["dividende_pct_bip"], dividende_2060=r60["dividende_pct_bip"],
                verteidigung=r2(-(r60["dach_ohne_zins"] - r28["dach_ohne_zins"])),
                lenkung_erosion=r2(-(r60["erosion"] - r28["erosion"])),
                gesundheit_pflege=r2(-(r60["gesundheit_plus"] - r28["gesundheit_plus"])),
                progression=r2(r60["progression"] - r28["progression"]))
    zerl["summe"] = r2(zerl["verteidigung"] + zerl["lenkung_erosion"] + zerl["gesundheit_pflege"] + zerl["progression"])
    E = dict(version=P["version"], status="Prüfrechnung (Auftrag 18.11.2026); geltende Rechnung unverändert", einnahmen=ein, ausgaben=aus,
             finanzierung_2028=finanz, dividende_zerlegung_2028_2060=zerl,
             hinweis="% des jeweiligen BIP. EU-27: Einnahmen 2024, Ausgaben 2023 (verschiedene Jahre). Modellland: Ausgaben der zehn Staaten, Einnahmen auf "
                     "deutscher Basis. Zuordnung der Einkommensteuer zu Arbeit und Kapital und der übrigen Steuern sind Annahmen (struktur_vergleich.toml).")
    (AGG / "struktur_vergleich.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for k in ("eu27_2024", "de_2024", "neu_2028_steuern", "neu_2028_mit_fonds", "neu_2028_mit_pflichtvorsorge"):
        print("EIN", k, ein[k]["pct_bip"], ein[k].get("anteil_pct"), ein[k]["summe"])
    print("EIN pfad", ein["neu_pfad_steuern"])
    for k in ("eu27_2023", "de_2024", "neu_2028", "neu_2040", "neu_2050"):
        print("AUS", k, aus[k]["einzeln"], aus[k]["drei"], aus[k]["anteil_drei_pct"], aus[k]["summe"])
    for x in aus["abdeckung"]:
        print("ABD", x["bereich"], x["de_2024"], x["modell_2028"], x["differenz"])
    print(finanz)
    print(zerl)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
