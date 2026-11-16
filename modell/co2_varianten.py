#!/usr/bin/env python3
"""CO₂-Position prüfen und Varianten einer strengeren Bepreisung (Logbuch v4.98). Prüfrechnung, ändert die Deckung nicht.

Befund: deckung_belegt setzt alle bepreisten Mengen (528 Mt 2028) × 100 €/t an. Im EU-ETS 1 erhält Deutschland Erlöse nur für die
versteigerten Mengen (2025 rund 26 %); frei zugeteilte Zertifikate bringen keine Einnahme. Varianten K0–K5 (co2_varianten.toml): Aufkommen 2028
in % BIP, Unterschied zur geltenden Position, Wirkung auf die Dividende je Erwachsenem (Euro je BIP-Punkt) und grobe Last der Rentnerhaushalte.
Ausgabe: daten/aggregate/co2_varianten.json
"""
import json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
P = tomllib.loads((W / "modell" / "co2_varianten.toml").read_text(encoding="utf-8"))


def main():
    m, e, a = P["mengen_2025"], P["erloese_2025"], P["annahmen"]
    f = (1 - P["rueckgang_je_jahr"]) ** 3
    ets1 = (m["ets1_anlagen"] + m["ets1_luftverkehr"] + m["ets1_seeverkehr"]) * f
    nehs = m["nehs"] * f
    bezahlt_2025 = e["ets1_mrd"] * 1000 / e["ets1_preis"] / (m["ets1_anlagen"] + m["ets1_luftverkehr"] + m["ets1_seeverkehr"])
    bip, p0 = P["bip_2028_mrd"], P["preis_2028"]
    pct = lambda mt, preis: mt * preis / 1000 / bip * 100
    heute = (e["ets1_mrd"] + e["nehs_mrd"]) / P["bip_2025_mrd"] * 100   # Erlöse 2025 in % BIP 2025
    erg = []
    for v in P["variante"]:
        preis = v.get("preis", p0)
        mf = (preis / p0) ** a["elastizitaet"]          # Mengenreaktion auf den höheren Preis
        if v["id"] == "K0":
            mt = ets1 + nehs
        elif v["id"] == "K1":
            mt = nehs + ets1 * a["ets1_bezahlt_2028"]
        else:
            mt = nehs + ets1 * (a["ets1_bezahlt_2028"] + (1 - a["ets1_bezahlt_2028"]) * a["abgabe_erfasst"])
            if v["id"] == "K5":
                mt += a["landwirtschaft_mt"] * f
        auf = pct(mt * mf, preis)
        d = auf - P["geltend_pct_bip"]
        erg.append(dict(id=v["id"], name=v["name"], preis_eur_t=preis, menge_bezahlt_mt=round(mt * mf), aufkommen_pct_bip=round(auf, 2),
                        aufkommen_mrd=round(auf * bip / 100, 1), gegen_geltend_pct_bip=round(d, 2),
                        dividende_erw_monat_eur=round(d * P["eur_je_bip_punkt_2028"]),
                        mehrlast_gegen_2025_pct_bip=round(auf - heute, 2),
                        rentner_mittel_monat_eur=round((auf - heute) / 0.1 * a["rentner_eur_je_0_1_pct"])))
    E = dict(version=P["version"], status="Prüfrechnung (2028); Deckung unverändert bis zur Entscheidung",
             mengen_2028_mt=dict(ets1=round(ets1), nehs_ets2=round(nehs)), ets1_bezahlt_2025_anteil=round(bezahlt_2025, 3), varianten=erg,
             erloese_2025_pct_bip=round(heute, 2),
             hinweis="Die Haushaltsrechnungen (haushalte33, mikro_de, Rentner) enthalten keine CO₂-Kosten, weder heute noch neu; die Mehrlast gegenüber "
                     "den Erlösen 2025 fehlt dort. Rentnerlast als grobe Ableitung aus der Labelwirkung (gleiche Inzidenz, Annahme; Heizung und Kraftstoff "
                     "wiegen bei Rentnern eher schwerer). Preise nominal 2028 (Annahme). Recht: nationale Abgabe neben dem EU-ETS und Preis über der "
                     "ETS2-Preisbremse sind rechtlich zu prüfen (P1).")
    (W / "daten" / "aggregate" / "co2_varianten.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(E["mengen_2028_mt"], "ETS1 bezahlt 2025:", E["ets1_bezahlt_2025_anteil"])
    for x in erg:
        print(x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
