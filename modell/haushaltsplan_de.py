#!/usr/bin/env python3
"""Haushaltsplan Deutschland vorher (Gesamtstaat 2024, Eurostat) – nachher (Stand C 2028, geltend) mit internem Beleg (Logbuch v4.94).

Einnahmen nach Steuer- und Abgabenart, Ausgaben nach Aufgaben; je Zeile % BIP und Mrd. € (vorher nominal 2024, nachher nominal 2028).
Dazu: Zerlegung des Dividendenpfads 2028 → 2060 (warum die Dividende sinkt) und Flüsse für die Grafik.
Ausgabe: daten/aggregate/haushaltsplan_de.json
"""
import json
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "haushaltsplan_de.toml").read_text(encoding="utf-8"))
SV = json.loads((AGG / "systemvarianten.json").read_text(encoding="utf-8"))
NZ = json.loads((AGG / "netz33.json").read_text(encoding="utf-8"))["beschluss"]["reihe"]
PJ = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))["reihe"]
FG = json.loads((AGG / "fonds_geltend.json").read_text(encoding="utf-8"))
EB = json.loads((AGG / "einnahmen_belege.json").read_text(encoding="utf-8"))
E5 = json.loads((AGG / "e5_varianten.json").read_text(encoding="utf-8"))
DB = json.loads((AGG / "dach_beitrag.json").read_text(encoding="utf-8"))


def main():
    E24 = P["eurostat_2024"]
    b24 = P["bip_2024_mio"]
    b28 = P["bip_2028_mrd"]
    v = [x for x in SV["varianten"] if x["id"] == "33R"][0]
    dp = v["deckung_positionen"]
    n28 = {r["jahr"]: r for r in NZ}
    p28 = {r["jahr"]: r for r in PJ}
    pos = n28[2028]["positionen"]
    de = FG["verrechnung"]["laender"]["DE"]
    altlast = de["altlast_2028_pct_bip"]
    fonds_beitrag = de["reihe"]["2028"]["beitrag_pct_bip"]
    zins = round(E24["D41PAY"] / b24 * 100, 2)                 # Annahme: Zinsquote 2028 wie 2024
    altrenten = round(altlast - zins, 2)
    progression = round(n28[2028]["dividende_pct_bip"] - v["dividende_pct_bip_2028"] - (11.12 - n28[2028]["netz_pct_bip"]), 2)
    m = EB["faelle"]["mittel"]["positionen"]
    bel = {"Unternehmen und Plattformen": m["unternehmen"]["belegt_pct_bip"], "Übrige Steuern": m["uebrige"]["belegt_pct_bip"],
           "CO₂-Preis": round(dp["CO₂-Preis"] + m["co2_2028"]["luecke_pct_bip"], 2), "Erbschaften": m["erbschaft"]["belegt_pct_bip"]}
    pct = lambda mio: round(mio / b24 * 100, 2)
    mrd28 = lambda p: round(p * b28 / 100, 1)

    def z(gruppe, name, heute_mio, nachher, einfluss, belegt=None, nachher_name=None):
        return dict(gruppe=gruppe, position=name, heute_mrd_2024=round(heute_mio / 1000, 1) if heute_mio is not None else None,
                    heute_pct_bip=pct(heute_mio) if heute_mio is not None else None, nachher_position=nachher_name,
                    nachher_pct_bip=nachher, nachher_mrd_2028=mrd28(nachher) if nachher is not None else None,
                    belegt_pct_bip=belegt, einfluss=einfluss)
    ein = [
        z("Steuern", "Lohn- und Einkommensteuer, Soli (Haushalte), sonstige Einkommensteuern", E24["D51A_C1"] - 0 + E24["D51E"], dp["Einkommen"],
          "Ein Tarif 0/11/19/25/33 % auf alle Einkommen einschließlich Dividende und Gewinnen der Personengesellschaften; Grundbedarf frei; keine Abzüge; Soli entfällt",
          nachher_name="Einkommen"),
        z("Steuern", "darin heute: Kapitalertrag- und Abgeltungsteuer", None, dp["Kapitalerträge"],
          "Kapitalerträge einschließlich Kursgewinnen höchstens 33 % (heute 26,375 %); je Einkommensart ein Drittel", nachher_name="Kapitalerträge"),
        z("Steuern", "Körperschaft- und Gewerbesteuer (Kapitalgesellschaften)", E24["D51B_C2"], dp["Unternehmen und Plattformen"],
          "Unternehmen 33 % auf den Konzerngewinn, verteilt nach Kundenumsatz; Plattformen mit Untergrenze; Gewerbesteuer entfällt (Gemeinden über feste Anteile); Altverluste 5 Jahre, Verrechnung über 1 Mio. € höchstens 50 %",
          bel["Unternehmen und Plattformen"], "Unternehmen und Plattformen"),
        z("Steuern", "Mehrwertsteuer", E24["D211"], dp["Konsum (Label)"],
          "Label 5/11/17/25 % nach Wirkung auf Gesundheit und Umwelt, Sonderstufe 33 % (Alkohol, Tabak, Kraftstoffe, Fahrzeuge 31 %); effektiv 18,8 % (heute 19/7 %)",
          nachher_name="Konsum (Label)"),
        z("Steuern", "Verbrauchsteuern (Energie, Strom, Tabak, Alkohol, Kaffee), Versicherung-, Grunderwerb- und Verkehrsteuern, Kfz-Steuer, übrige",
          E24["D2122C"] + E24["D214A"] + E24["D214G"] + E24["D214B"] + E24["D214_rest"] + E24["D29_rest"] + E24["D59"], dp["Übrige Steuern"],
          "Weitgehend wie heute (Annahme der Gesamtrechnung); Lenkung über die Sonderstufe im Label. Der Modellwert 3,93 enthält den Emissionshandel (eigene Position CO₂-Preis) und die Grundsteuer (geht in der Grundstücksabgabe auf) ein zweites Mal (Prüfbefund B-1, Korrektur 92)",
          bel["Übrige Steuern"], "Übrige Steuern"),
        z("Steuern", "Emissionshandel (Abgaben auf Verschmutzung)", E24["D29F"], dp["CO₂-Preis"],
          "CO₂-Preis 100 €/t auf alle bepreisten Emissionen, Pfad bis 150 €/t; sinkt mit den Emissionen", bel["CO₂-Preis"], "CO₂-Preis"),
        z("Steuern", "Grundsteuer", E24["D29A"], dp["Grundstücksabgabe"], "Bodenwertabgabe bis 1 % des Bodenwerts (Gemeinden)", nachher_name="Grundstücksabgabe"),
        z("Steuern", "Erbschaft- und Schenkungsteuer", E24["D91"], dp["Erbschaften"],
          "33 % auf Erwerbe über 100.000 € je Erbe, ohne Verschonung von Betriebsvermögen (heute bis 50 %, viele Ausnahmen)", bel["Erbschaften"], "Erbschaften"),
        z("Steuern", "Vermögensteuer (seit 1997 nicht erhoben)", 0, dp["Große Vermögen"], "Mindeststeuer (anrechenbar) und 1 % ab 2 Mio. €", nachher_name="Große Vermögen"),
        z("Steuern", "Abbau klimaschädlicher Subventionen (heute Ausgabe oder Steuervergünstigung)", None, dp["Subventionsabbau"],
          "20 Mrd. € nach UBA-Liste, überwiegend Steuervergünstigungen (Mehraufkommen) und zum Teil Finanzhilfen (weniger Ausgaben); im Modell als Einnahme geführt. Prüfpunkt: Entfernungspauschale und Dienstwagen fallen schon mit „ohne Abzüge“ im Einkommen weg", nachher_name="Subventionsabbau"),
        z("Steuern", "Progression und Dynamik (2028)", None, progression, "Mehraufkommen aus dem Tarif bei wachsenden Einkommen und erwarteter Dynamik"),
        z("Sozialbeiträge", "Beiträge der Arbeitgeber", E24["D611"], 0.0, "entfallen: Arbeit wird um diesen Betrag billiger"),
        z("Sozialbeiträge", "Beiträge der Arbeitnehmer", E24["D613CE"], 0.0, "entfallen; Gesundheit und Netz aus Steuern"),
        z("Sozialbeiträge", "Beiträge Nichterwerbstätiger, Selbständiger, freiwillige", E24["D613CN"] + E24["D613CS"] + E24["D613V"], 0.0, "entfallen"),
        z("Sozialbeiträge", "unterstellte Beiträge (Beamtenversorgung)", E24["D612"], 0.0, "entfallen; laufende Pensionen als Altlast über den Fonds"),
        z("Abgabe für Altlasten", "– (neu)", None, fonds_beitrag,
          "Altlastenzuschlag auf alle Steuern (DE 2028 14,6 %), zweckgebunden: fließt vollständig als Beitrag an den Gemeinschaftsfonds (Ausgabe), bis 2098",
          nachher_name="Altlastenzuschlag"),
        z("Übrige Einnahmen", "Verkäufe, Gebühren, Vermögenserträge, Transfers", E24["TR"] - sum(E24[k] for k in ("D51A_C1", "D51E", "D51B_C2", "D211", "D2122C", "D214A", "D214G", "D214B", "D214_rest", "D29A", "D29F", "D29_rest", "D59", "D91", "D611", "D613CE", "D613CN", "D613CS", "D613V", "D612")),
          None, "im Modell nicht gerechnet: Ausgaben der Gemeinden und des Dachs sind netto nach Gebühren angesetzt (Annahme); heute brutto. Vergleich der Summen deshalb nur eingeschränkt"),
    ]
    A = DB["aufgaben"]
    a_ = {x["aufgabe"]: x["pct_bip_ziel"] for x in A}
    vert28 = [r for r in DB["reihe"] if r["jahr"] == 2028][0]["verteidigung"]
    from_b = {"Schulen": 3.7, "Kommunalverwaltung": 1.62, "Nahverkehr, Ortsstraßen": 1.48, "Kultur, Sport, Gemeinschaft": 1.22,
              "Ordnung, Feuerwehr, Rettung": 1.05, "Wohnen, Gemeinwesen": 0.71, "Wasser, Abwasser, Abfall": 0.57}
    aus = [
        z("Verwaltung", "Allgemeine Verwaltung, Außenbeziehungen (COFOG 01 ohne Zinsen und Grundlagenforschung)", E24["GF01"] - E24["GF0107"] - E24["GF0104"],
          round(from_b["Kommunalverwaltung"] + a_["Außenbeziehungen"] + a_["Bildungs-, Markt- und Produktstandards"], 2),
          "Kommunalverwaltung 1,62 + Außenbeziehungen 0,30 + Standards 0,30; einfaches System, Verwaltung der Sozialversicherung (heute rund 1,1 % BIP) entfällt"),
        z("Verwaltung", "Zinsen (Schuldendienst)", E24["GF0107"], 0.0, f"Ausgabe des Gemeinschaftsfonds, nicht des Landeshaushalts ({zins:.2f} % BIP, siehe Fondskonto)"),
        z("Sicherheit", "Verteidigung", E24["GF02"], vert28, "Pfad bis 2,5 % BIP 2035 (Verteidigung und digitale Souveränität, gemeinsam)"),
        z("Sicherheit", "Öffentliche Ordnung und Sicherheit", E24["GF03"], round(a_["Übergeordnete Polizei"] + from_b["Ordnung, Feuerwehr, Rettung"], 2),
          "übergeordnete Polizei 0,29 + Ordnung, Feuerwehr, Rettung 0,05 + 1,0 (Gemeinden); Gerichte und Vollzug in der Zuordnung nicht getrennt (Annahme)"),
        z("Wirtschaft", "Wirtschaft, Verkehr, Energie, Landwirtschaft", E24["GF04"], round(a_["Wirtschaftsraum, Agrar, Energie, Netze"] + from_b["Nahverkehr, Ortsstraßen"], 2),
          "Wirtschaftsraum, Agrar, Energie, Netze 2,10 + Nahverkehr und Ortsstraßen 1,48; klimaschädliche Subventionen abgebaut"),
        z("Umwelt", "Umweltschutz, Wasser, Abwasser, Abfall", E24["GF05"], round(a_["Umwelt, grenzüberschreitend"] + from_b["Wasser, Abwasser, Abfall"], 2),
          "grenzüberschreitend 0,29 + Gemeinden 0,57 (netto nach Gebühren)"),
        z("Gemeinwesen", "Wohnen und kommunale Einrichtungen", E24["GF06"], from_b["Wohnen, Gemeinwesen"], "Gemeinden"),
        z("Gesundheit", "Gesundheit", E24["GF07"], pos["Gesundheit (Grundversorgung)"], "Grundversorgung für alle aus Steuern; keine Krankenkassenbeiträge"),
        z("Kultur", "Freizeit, Sport, Kultur, Religion", E24["GF08"], from_b["Kultur, Sport, Gemeinschaft"], "Gemeinden"),
        z("Bildung", "Schulen (Vorschule bis Sekundarstufe)", E24["GF0901"] + E24["GF0902"], from_b["Schulen"], "Gemeinden, Schulen 3,70"),
        z("Bildung", "Hochschulen, Grundlagenforschung, übrige Bildung", E24["GF09"] - E24["GF0901"] - E24["GF0902"] + E24["GF0104"],
          round(a_["Hochschulen"] + a_["Grundlagenforschung"], 2), "Hochschulen 0,74 + Grundlagenforschung 0,77 (Dach)"),
        z("Soziale Sicherung", "Alter und Hinterbliebene (Renten, Pensionen)", E24["GF1002"] + E24["GF1003"], 0.0,
          f"Landeshaushalt: keine eigene Position. Alte Ansprüche bis zur Höhe der Dividende trägt die Dividende, darüber der Gemeinschaftsfonds ({altrenten:.2f} % BIP, siehe Fondskonto); neue Ansprüche: Dividende und Pflichtvorsorge (eigenes Konto, 4,1 % BIP, privat)"),
        z("Soziale Sicherung", "Krankheit und Invalidität (Krankengeld, Pflege, Erwerbsminderung)", E24["GF1001"], round(pos["Pflege (Teilkasko)"] + pos["Invalidität (Grundbedarf)"], 2),
          "Pflege (Teilkasko) 0,85 + Invalidität (Grundbedarf) 0,29"),
        z("Soziale Sicherung", "Arbeitslosigkeit", E24["GF1005"], pos["Arbeitslosigkeit (Grundbedarf)"], "Grundbedarf; die Dividende trägt mit"),
        z("Soziale Sicherung", "Familie und Kinder, Wohnen, Grundsicherung, übrige", E24["GF10"] - E24["GF1001"] - E24["GF1002"] - E24["GF1003"] - E24["GF1005"],
          round(pos["Waisen"] + pos["Härtefall"], 2), "Waisen 0,05 + Härtefall 0,65; Kindergeld, Wohngeld und Grundsicherung gehen in der Dividende auf"),
        z("Dividende", "– (neu)", None, n28[2028]["dividende_pct_bip"],
          f"Transformationsdividende für alle Erwachsenen, halb für Kinder; DE 2028 {n28[2028]['dividende_erw_eur2026']} € je Erwachsenem und Monat (Kaufkraft 2026)",
          belegt=E5["varianten"]["A_mittel"]["dividende_pct_bip"].get("2028", E5["varianten"]["A_mittel"]["dividende_pct_bip"].get(2028)), nachher_name="Dividende"),
    ]
    aus.append(z("Gemeinschaftsfonds", "– (neu)", None, fonds_beitrag, "Beitrag Deutschlands an den Gemeinschaftsfonds, finanziert aus dem Altlastenzuschlag",
                 nachher_name="Beitrag an den Fonds"))
    summe = lambda L, k: round(sum(x[k] or 0 for x in L), 2)
    fonds = dict(einnahmen=[dict(position="Beitrag Deutschlands", pct_bip=fonds_beitrag, art="Aufkommen (aus dem Altlastenzuschlag)")],
                 ausgaben=[dict(position="Altrenten über der Dividende", pct_bip=altrenten, art="Ausgabe"),
                           dict(position="Zinsen auf übernommene Altschulden", pct_bip=zins, art="Ausgabe (Annahme: Zinsquote 2024)")],
                 finanzierung=[dict(position="Fondskredite", pct_bip=round(altlast - fonds_beitrag, 2),
                                    art="Finanzierung, keine Einnahme; Tilgung aus späteren Beiträgen bis 2098")],
                 hinweis="Rechnung für den Anteil Deutschlands im Fonds der 30 (fonds_geltend, Verrechnung je Staat)")
    # Dividendenpfad 2028 → 2060 (geltend)
    d28, d60 = n28[2028], n28[2060]
    p0, p1 = p28[2028], p28[2060]
    zer = dict(dividende_2028=d28["dividende_pct_bip"], dividende_2060=d60["dividende_pct_bip"],
               verteidigung=round(-(p1["dach_ohne_zins"] - p0["dach_ohne_zins"]), 2),
               lenkung_und_verbrauch=round(-(p1["erosion"] - p0["erosion"]), 2),
               darin_co2=round(p1["co2"] - p0["co2"], 2), darin_verbrauchsteuern=round(-p1["verbrauchsteuern_minus"] + p0["verbrauchsteuern_minus"], 2),
               darin_label=round(p1["konsum"] - p0["konsum"], 2),
               netz_alterung=round(-(d60["netz_pct_bip"] - d28["netz_pct_bip"]), 2),
               progression=round(p1["progression"] - p0["progression"], 2))
    zer["rest"] = round(zer["dividende_2060"] - zer["dividende_2028"] - zer["verteidigung"] - zer["lenkung_und_verbrauch"] - zer["netz_alterung"] - zer["progression"], 2)
    E = dict(version=P["version"], status="Prüfrechnung; Spalte belegt intern", einheit="% BIP; Mrd. € nominal (vorher 2024, nachher 2028)",
             quellen=dict(steuern=P["url_steuern"], ausgaben=P["url_ausgaben"], haupt=P["url_haupt"]),
             einnahmen=ein, ausgaben=aus,
             fondskonto=fonds,
             pruefung=[
                 ("Einkommen", "Aufkommen (Steuer)", "Landeshaushalt", "Wert aus der Tarifrechnung, nicht amtlich belegt; enthält die Steuer auf die Dividende selbst, weil sie steuerpflichtig ist"),
                 ("Kapitalerträge", "Aufkommen (Steuer)", "Landeshaushalt", "heute in den Einkommensteuern der Haushalte enthalten; getrennt nicht gelesen"),
                 ("Unternehmen und Plattformen", "Aufkommen (Steuer)", "Landeshaushalt", "Modellwert 4,42 nicht belegt, belegt 2,37 (Prüfbefund B-1)"),
                 ("Konsum (Label)", "Aufkommen (Steuer)", "Landeshaushalt", "heute Mehrwertsteuer 6,81; Anstieg aus Sonderstufe und Labelstufen (Modell)"),
                 ("Übrige Steuern", "Aufkommen (Steuer)", "Landeshaushalt", "Modellwert 3,93 enthält Emissionshandel und Grundsteuer, die eigene Positionen haben (Korrektur 92); wie heute: 2,89"),
                 ("CO₂-Preis", "Aufkommen (Abgabe)", "Landeshaushalt", "heute Emissionshandel 0,42; 100 €/t auf alle bepreisten Emissionen; sinkt mit den Emissionen"),
                 ("Grundstücksabgabe", "Aufkommen (Abgabe)", "Landeshaushalt (Gemeinden)", "ersetzt die Grundsteuer (0,37); 0,82 ist der Gesamtbetrag"),
                 ("Erbschaften, Große Vermögen", "Aufkommen (Steuer)", "Landeshaushalt", "Erbschaft belegt 0,97 statt 1,16"),
                 ("Subventionsabbau", "überwiegend Aufkommen (Wegfall von Steuervergünstigungen), zum Teil weniger Ausgaben", "Landeshaushalt",
                  "Mischposition; mögliche Überschneidung mit „Einkommen ohne Abzüge“ (Entfernungspauschale, Dienstwagen) und mit dem Label; zu prüfen"),
                 ("Progression und Dynamik", "Aufkommen (Steuer)", "Landeshaushalt", "Mehraufkommen aus dem Tarif 2028"),
                 ("Altlastenzuschlag", "Aufkommen (zweckgebundene Abgabe)", "Landeshaushalt", "Durchlauf: geht vollständig als Beitrag an den Fonds; bis v4.94 ohne Gegenbuchung als Einnahme geführt (Korrektur 93)"),
                 ("Sozialbeiträge (heute)", "Aufkommen (Abgabe)", "Gesamtstaat (Sozialversicherung)", "entfallen nachher; unterstellte Beiträge der Beamtenversorgung stehen heute zugleich in Aufkommen und Ausgaben"),
                 ("Gebühren, Erträge, Transfers (heute)", "Aufkommen", "Gesamtstaat", "nachher nicht gerechnet, Ausgaben netto (Annahme); Summen deshalb nur eingeschränkt vergleichbar"),
                 ("Neue Kredite (heute)", "Finanzierung", "Gesamtstaat", "keine Einnahme; deckt den Finanzierungssaldo; bis v4.94 als Einnahme geführt (Korrektur 93)"),
                 ("Kredite des Fonds", "Finanzierung", "Gemeinschaftsfonds", "keine Einnahme des Landes; bis v4.94 in den Einnahmen des Landes (Korrektur 93)"),
                 ("Dach und Gemeinden", "Ausgabe", "Landeshaushalt", "Werte netto nach Gebühren (Annahme); Zuordnung zu COFOG eigene"),
                 ("Netz (Gesundheit, Pflege, Invalidität, Arbeitslosigkeit, Waisen, Härtefall)", "Ausgabe", "Landeshaushalt", "aus Steuern statt Beiträgen"),
                 ("Dividende", "Ausgabe (Transfer)", "Landeshaushalt", "Rest nach allen anderen Ausgaben; steuerpflichtig"),
                 ("Beitrag an den Gemeinschaftsfonds", "Ausgabe (Transfer)", "Landeshaushalt", "Gegenbuchung zum Altlastenzuschlag; neu seit v4.95"),
                 ("Altrenten über der Dividende", "Ausgabe", "Gemeinschaftsfonds", "bis v4.94 im Landeshaushalt geführt (Korrektur 93)"),
                 ("Zinsen (Schuldendienst)", "Ausgabe", "heute Gesamtstaat, nachher Gemeinschaftsfonds", "nachher für übernommene Altschulden; Zinsquote 2024 angenommen; bis v4.94 im Landeshaushalt geführt (Korrektur 93)")],
             summen=dict(aufkommen_heute_pct=pct(E24["TR"]), ausgaben_heute_pct=pct(E24["TE"]), finanzierungssaldo_heute_pct=pct(E24["B9"]),
                         aufkommen_nachher_pct=summe(ein, "nachher_pct_bip"), ausgaben_nachher_pct=summe(aus, "nachher_pct_bip"),
                         saldo_nachher_pct=round(summe(ein, "nachher_pct_bip") - summe(aus, "nachher_pct_bip"), 2),
                         fonds_ausgaben_pct=altlast, fonds_kredite_pct=round(altlast - fonds_beitrag, 2),
                         ausgaben_konsolidiert_nachher_pct=round(summe(aus, "nachher_pct_bip") - fonds_beitrag + altlast, 2),
                         steuern_nachher_pct=round(sum(dp.values()) + progression, 2), altlast_de_2028=altlast),
             dividendenpfad=zer,
             dividende_eur=dict(geltend=E5["geltend"]["dividende_erw_eur2026"], belegt_mittel=E5["varianten"]["A_mittel"]["dividende_erw_eur2026"]),
             dividende_pct_belegt_mittel=E5["varianten"]["A_mittel"]["dividende_pct_bip"],
             pflichtvorsorge_pct_bip=4.1)
    (AGG / "haushaltsplan_de.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Summen:", E["summen"])
    print("Dividendenpfad:", zer)
    for x in ein + aus:
        print(f"{x['gruppe'][:12]:12} {x['position'][:60]:60} {x['heute_pct_bip']!s:>6} → {x['nachher_pct_bip']!s:>6} (belegt {x['belegt_pct_bip']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
