#!/usr/bin/env python3
"""Mehrwertsteuer nach Einkommen: Faktoren für die Haushaltsrechnungen (Logbuch v4.29). Prüfrechnung, Deutschland.

Bisher: Mehrbelastung = Konsum × ((1 + 18,84 %) / (1 + 15,97 %) − 1) und gezahlte Steuer = Konsum × 18,84 / 118,84, für alle Einkommen gleich.
Beide Sätze gelten aber für den steuerpflichtigen Konsum (systemvarianten.label_effektiv, nachfrage.toml); Miete, Gesundheit, Bildung und
Versicherungen sind steuerfrei, und die Güterstruktur hängt vom Einkommen ab (EVS 2023).

Rechnung je Einkommensklasse c (EVS 2023): sichtbare Mehrbelastung s_c = Σ_g K_gc ((1+r_g,neu)/(1+r_g,heute) − 1) / K_c und sichtbare gezahlte
Steuer v_c = Σ_g K_gc (1+r_neu)/(1+r_heute) · r_neu/(1+r_neu) / K_c. Sätze heute aus nachfrage.toml, neu nach der steuernden Zuordnung auf die
Sätze und Sonderstufen von 33R (systemvarianten.toml).
Varianten: „mit_vorsteuer“ (geltend): Rest bis zur bisherigen Durchschnittsbelastung (Vorsteuer in steuerfreien Bereichen, Wohnungsbau u. a.)
gleichmäßig je Euro Konsum (Annahme) → Faktor φ_c = (s_c + Rest) / bisher; „sichtbar“: φ_c = s_c / bisher; „einheitlich“: φ = 1.
Ausgabe: daten/aggregate/mwst_verteilung.json; Funktion faktoren(netto_jahr) für die Haushaltsmodule (DE).
"""
import json
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "mwst_verteilung.toml").read_text(encoding="utf-8"))
_CACHE = {}


def saetze():
    NF = tomllib.loads((W / "modell" / "nachfrage.toml").read_text(encoding="utf-8"))
    SVT = tomllib.loads((W / "modell" / "systemvarianten.toml").read_text(encoding="utf-8"))
    v = next(x for x in SVT["system"] if x["id"] == "33R")
    stufe = {5: 0, 11: 1, 17: 2, 22: 3, 28: 4}
    heute, neu = {}, {}
    for g in NF["gruppe"]:
        heute[g["id"]] = g["heute"]
        alt = NF["label_steuernd"].get(g["id"], g["label"])
        if g["label"] == 0:
            neu[g["id"]] = 0.0
        else:
            neu[g["id"]] = v["label_saetze"][stufe[alt]] if alt in stufe else alt * v["label_saetze"][4] / 28
        if g["id"] in v.get("label_sonder", {}):
            neu[g["id"]] = v["label_sonder"][g["id"]]
    return heute, neu


def rechne():
    heute, neu = saetze()
    eff = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))["reihe"][0]["label_effektiv"]
    eff_alt = tomllib.loads((W / "modell" / "haushalte33.toml").read_text(encoding="utf-8"))["mwst_heute_effektiv"]
    m_bisher = (1 + eff / 100) / (1 + eff_alt / 100) - 1
    b_bisher = eff / (100 + eff)
    zeilen = []
    for i, k in enumerate(P["konsum"]):
        s = v = vh = pfl = 0.0
        summe = 0.0
        for evs, teile in P["aufteilung"].items():
            for g, a in teile.items():
                x = P["gueter"][evs][i] * a
                rh, rn = heute[g] / 100, neu[g] / 100
                s += x * ((1 + rn) / (1 + rh) - 1)
                v += x * (1 + rn) / (1 + rh) * rn / (1 + rn)
                vh += x * rh / (1 + rh)
                pfl += x if heute[g] > 0 else 0.0
                summe += x
        zeilen.append(dict(klasse=P["klassen"][i], netto_monat=P["netto_monat"][i], konsum=k, summe_gueter=round(summe), steuerpflichtig=round(pfl / summe, 3),
                           sichtbar_mehr_pct=round(s / summe * 100, 3), sichtbar_bezahlt_neu_pct=round(v / summe * 100, 3),
                           sichtbar_bezahlt_heute_pct=round(vh / summe * 100, 3), konsumquote_evs=round(k / P["netto_monat"][i], 3)))
    # Durchschnitt über die Klassen, gewichtet mit dem Konsum (Klassenbesetzung nicht veröffentlicht: Annahme gleiche Besetzung je Klasse)
    km = sum(z["konsum"] for z in zeilen)
    s_m = sum(z["sichtbar_mehr_pct"] * z["konsum"] for z in zeilen) / km / 100
    v_m = sum(z["sichtbar_bezahlt_neu_pct"] * z["konsum"] for z in zeilen) / km / 100
    rest_m, rest_b = m_bisher - s_m, b_bisher - v_m
    for z in zeilen:
        s, v = z["sichtbar_mehr_pct"] / 100, z["sichtbar_bezahlt_neu_pct"] / 100
        z["phi"] = {"mit_vorsteuer": [round((s + rest_m) / m_bisher, 4), round((v + rest_b) / b_bisher, 4)],
                    "sichtbar": [round(s / m_bisher, 4), round(v / b_bisher, 4)], "einheitlich": [1.0, 1.0]}
    return dict(version=P["version"], status="Prüfrechnung", variante=P["variante"], eff_neu=eff, eff_heute=eff_alt,
                bisher=dict(mehr_pct_konsum=round(m_bisher * 100, 3), bezahlt_pct_konsum=round(b_bisher * 100, 3)),
                sichtbar_mittel=dict(mehr_pct_konsum=round(s_m * 100, 3), bezahlt_pct_konsum=round(v_m * 100, 3)),
                rest_gleichmaessig=dict(mehr_pct_konsum=round(rest_m * 100, 3), bezahlt_pct_konsum=round(rest_b * 100, 3)),
                saetze_heute=heute, saetze_neu=neu, klassen=zeilen,
                hinweis="EVS 2023 (Destatis, amtlich), Klassenmitten und Aufteilung der EVS-Gruppen Annahmen; sichtbar = Steuer auf den Gütern selbst; "
                        "Rest = bisheriger Durchschnitt minus sichtbar (Vorsteuer steuerfreier Bereiche u. a.), gleichmäßig je Euro Konsum (Annahme).")


def faktoren(netto_jahr, variante=None):
    """(φ Mehrbelastung, φ gezahlte Steuer) für ein Haushaltsnetto im Jahr; zwischen den Klassenmitten linear, außen konstant."""
    if "j" not in _CACHE:
        f = AGG / "mwst_verteilung.json"
        _CACHE["j"] = json.loads(f.read_text(encoding="utf-8")) if f.exists() else None
    J = _CACHE["j"]
    var = variante or P["variante"]
    if J is None or var == "einheitlich":
        return 1.0, 1.0
    x = netto_jahr / 12
    kl = J["klassen"]
    if x <= kl[0]["netto_monat"]:
        return tuple(kl[0]["phi"][var])
    for a, b in zip(kl, kl[1:]):
        if x <= b["netto_monat"]:
            t = (x - a["netto_monat"]) / (b["netto_monat"] - a["netto_monat"])
            return tuple(pa + t * (pb - pa) for pa, pb in zip(a["phi"][var], b["phi"][var]))
    return tuple(kl[-1]["phi"][var])


def main():
    E = rechne()
    (AGG / "mwst_verteilung.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("bisher", E["bisher"], "| sichtbar Mittel", E["sichtbar_mittel"], "| Rest", E["rest_gleichmaessig"])
    for z in E["klassen"]:
        print(z["klasse"], "steuerpfl.", z["steuerpflichtig"], "Konsumquote EVS", z["konsumquote_evs"], "φ", z["phi"]["mit_vorsteuer"], "sichtbar", z["phi"]["sichtbar"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
