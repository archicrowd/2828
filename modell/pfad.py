#!/usr/bin/env python3
"""Zeitpfad 2028 bis 2060 des Klubs (Rekonstruktion, Logbuch Band III v3.6).

ACHTUNG: Dies ist eine Rekonstruktion, nicht das Original. Das Original (pfad.py,
dyn.py) liegt nicht vor. Das Skript setzt eine Modellstruktur an, die aus den
Parametern und Fragmenten des Original-Skripts im Chat abgeleitet wurde, und
prüft sie gegen die Zeitpfad-Tabelle des Gesamtkonzepts
(daten/aggregate/referenz_gesamtkonzept.csv). Dass sie die Tabelle trifft, zeigt
Übereinstimmung, nicht, dass das Original so gerechnet hat.

Struktur (alle Anteile in % des BIP, Klub, Preise 2028)
  Schuldenquote   d(t)  = d0 / (1 + g)^t             nominaler Schuldenstand konstant,
                                                     g = nominales BIP-Wachstum
  Zinssatz        s(t)  = alt + (ziel - alt) * min(1, t / Restlaufzeit)
                                                     lineares Auslaufen des Altbestands
  Zinsdienst      z(t)  = d(t) * s(t) / 100
  Verteidigung    v(t)  = v0 + (v1 - v0) * min(1, t / (Zieljahr - 2028))
  A gesamt        a(t)  = a_rest + v(t) + z(t)
  Dividendenanteil      = Steuerquote - a(t) - b
  Dividende je Kopf     = Anteil * BIP/Kopf(2028) * (1 + r)^t / 12
                          r = (1 + g) / (1 + Preissteigerung) - 1, Bevölkerung konstant
  Mindestquote          = max_t [ a(t) + b + 12 * Dmin / (BIP/Kopf(t)) * 100 ],
                          Dmin = Versprechen Deutschland / (DE-Faktor)

Aufruf:  python3 modell/pfad.py
Ausgabe: daten/aggregate/pfad.csv, pfad_abgleich.csv, pfad_sensitivitaet.csv
Rückgabe: 0 wenn alle Abgleichswerte innerhalb der Toleranz liegen, 2 sonst.
"""
import copy
import csv
import sys
import tomllib
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
PARAMETER = WURZEL / "modell" / "parameter.toml"
AGG = WURZEL / "daten" / "aggregate"
REFERENZ = AGG / "referenz_gesamtkonzept.csv"

START, ENDE = 2028, 2060
STUETZ = (2028, 2030, 2035, 2040, 2050, 2060)

# Toleranzen = Rundung der Referenzwerte (+-0,005 bzw. +-0,5) plus Rundung der
# Eingaben (Schuldenquote 78,4 +-0,05; Einwohner 255,1). Sie wurden festgelegt,
# nachdem ein Prototyp lief: kein unabhängiger Test der Toleranzwahl.
TOL_PUNKTE = 0.01   # Prozentpunkte des BIP
TOL_EURO = 1.5      # EUR je Kopf und Monat


def lade() -> dict:
    daten = tomllib.loads(PARAMETER.read_text(encoding="utf-8"))
    return {p["name"]: p for p in daten["parameter"]}


def wert(P: dict, name: str) -> float:
    if name not in P:
        sys.exit(f"FEHLER: Parameter '{name}' fehlt in {PARAMETER.name}")
    return float(P[name]["wert"])


def rechne(P: dict, *, real_exakt: float | None = None, zins_vorlauf: float = 0.0) -> dict:
    """Rechnet den Pfad. real_exakt: reales Wachstum je Kopf in Prozent statt
    aus nominal/Preissteigerung abgeleitet. zins_vorlauf: Jahre, die das Auslaufen
    des Altbestands vor 2028 begonnen hat (0 = Zentralfall)."""
    g = wert(P, "wachstum_nominal") / 100
    pi = wert(P, "preissteigerung") / 100
    r = real_exakt / 100 if real_exakt is not None else (1 + g) / (1 + pi) - 1
    d0 = wert(P, "schuldenquote_klub_2028")
    alt = wert(P, "zins_effektiv_altbestand")
    ziel = wert(P, "garantiezins_klub")
    rest = wert(P, "restlaufzeit_schulden")
    v0 = wert(P, "verteidigung_basis_cofog_2024")
    v1 = wert(P, "verteidigung_ziel_nato_2035")
    vjahr = int(P["verteidigung_ziel_nato_2035"]["bezugsjahr"])
    a_rest = wert(P, "a_ohne_verteidigung_zins_bip_2028")
    b = wert(P, "b_fachaufgaben_bip_2028")
    q = wert(P, "steuerquote_klub")
    bip = wert(P, "klub_bip_2028") * 1e9
    pop = wert(P, "klub_einwohner_2024") * 1e6
    bipk = bip / pop
    dmin_klub = (wert(P, "dividende_de_versprechen_monat")
                 * wert(P, "dividende_klub_monat_2028") / wert(P, "dividende_de_monat_2028"))

    zeilen = {}
    for jahr in range(START, ENDE + 1):
        t = jahr - START
        d = d0 / (1 + g) ** t
        s = alt + (ziel - alt) * min(1.0, (t + zins_vorlauf) / rest)
        z = d * s / 100
        v = v0 + (v1 - v0) * min(1.0, t / (vjahr - START))
        a = a_rest + v + z
        anteil = q - a - b
        zeilen[jahr] = {
            "schuldenquote": d, "zinssatz": s, "zinsdienst": z, "verteidigung": v,
            "a_gesamt": a, "b": b, "dividende_anteil": anteil,
            "dividende_klub_monat": anteil / 100 * bipk * (1 + r) ** t / 12,
            "_bedarf": a + b + 12 * dmin_klub / (bipk * (1 + r) ** t) * 100,
        }
    mindestquote = max(z["_bedarf"] for z in zeilen.values())
    return {"zeilen": zeilen, "mindestquote": mindestquote, "r": r, "bipk": bipk}


def mindestquote(P: dict, r_prozent: float) -> float:
    """Mindestquote bei gegebenem realem Wachstum je Kopf (Prozent)."""
    return rechne(P, real_exakt=r_prozent)["mindestquote"]


def lies_referenz() -> list[dict]:
    with REFERENZ.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def schreibe(pfad: Path, kopf: list[str], zeilen: list[list]) -> None:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    with pfad.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(kopf)
        w.writerows(zeilen)


def main() -> int:
    P = lade()
    zentral = rechne(P)
    z = zentral["zeilen"]

    schreibe(AGG / "pfad.csv",
             ["jahr", "schuldenquote_pct_bip", "zinssatz_pct", "zinsdienst_pct_bip",
              "verteidigung_pct_bip", "a_gesamt_pct_bip", "b_pct_bip",
              "dividende_anteil_pct_bip", "dividende_klub_monat_eur_real2028"],
             [[j, round(v["schuldenquote"], 4), round(v["zinssatz"], 4),
               round(v["zinsdienst"], 4), round(v["verteidigung"], 4),
               round(v["a_gesamt"], 4), round(v["b"], 4),
               round(v["dividende_anteil"], 4), round(v["dividende_klub_monat"], 2)]
              for j, v in z.items()])

    # Abgleich gegen die Referenz
    abgleich, abweichungen = [], 0
    for ref in lies_referenz():
        gr = ref["groesse"]
        soll = float(ref["wert"])
        if gr.startswith("mindestquote"):
            r_prozent = float(gr.rsplit("_", 1)[1])
            # "1" in der Referenz bedeutet das Szenario "1,0 %" des Gesamtkonzepts
            ist = mindestquote(P, r_prozent) if r_prozent == 0 else zentral["mindestquote"]
            jahr, tol = "", TOL_PUNKTE
        else:
            jahr = int(ref["jahr"])
            schluessel = {"zinsdienst": "zinsdienst", "a_gesamt": "a_gesamt",
                          "dividende_anteil": "dividende_anteil",
                          "dividende_klub_monat": "dividende_klub_monat"}[gr]
            ist = z[jahr][schluessel]
            tol = TOL_EURO if gr == "dividende_klub_monat" else TOL_PUNKTE
        diff = ist - soll
        ok = abs(diff) <= tol
        abweichungen += not ok
        abgleich.append([gr, jahr, round(ist, 4), soll, round(diff, 4), tol, "ja" if ok else "NEIN"])
    schreibe(AGG / "pfad_abgleich.csv",
             ["groesse", "jahr", "rekonstruktion", "referenz", "differenz", "toleranz", "innerhalb"],
             abgleich)

    # Sensitivitäten (keine Alternative zum Zentralfall, sondern Prüfung der Annahmen)
    varianten = [
        ("zentral", zentral),
        ("reales_wachstum_exakt_1_0_prozent", rechne(P, real_exakt=1.0)),
        ("zinsauslaufen_ab_2024_statt_2028", rechne(P, zins_vorlauf=4.0)),
    ]
    # Annahmen ohne Datengrundlage: Restlaufzeit (nicht erhoben) und Zielzins
    for name, wert_neu in (("restlaufzeit_schulden", 5.0), ("restlaufzeit_schulden", 10.0),
                           ("garantiezins_klub", 2.3), ("garantiezins_klub", 2.78)):
        Q = copy.deepcopy(P)
        Q[name]["wert"] = wert_neu
        varianten.append((f"{name}_{wert_neu}", rechne(Q)))
    sens = []
    for name, res in varianten:
        for j in STUETZ:
            sens.append([name, j, round(res["zeilen"][j]["zinsdienst"], 4),
                         round(res["zeilen"][j]["dividende_anteil"], 4),
                         round(res["zeilen"][j]["dividende_klub_monat"], 2),
                         round(res["mindestquote"], 3)])
    schreibe(AGG / "pfad_sensitivitaet.csv",
             ["variante", "jahr", "zinsdienst_pct_bip", "dividende_anteil_pct_bip",
              "dividende_klub_monat_eur_real2028", "mindestquote_pct_bip"], sens)

    # Ausgabe
    n = len(abgleich)
    print(f"Abgleich: {n - abweichungen} von {n} Werten innerhalb der Toleranz "
          f"(Punkte {TOL_PUNKTE}, Euro {TOL_EURO}).")
    for zeile in abgleich:
        if zeile[-1] != "ja":
            print("  ABWEICHUNG:", zeile)
    print(f"Reales Wachstum je Kopf, abgeleitet: {zentral['r'] * 100:.4f} % "
          f"(Parameter wachstum_real_je_kopf: {wert(P, 'wachstum_real_je_kopf')} %)")
    print(f"Mindestquote (Zentralfall): {zentral['mindestquote']:.3f} %, "
          f"bei 0 % Wachstum: {mindestquote(P, 0.0):.3f} %")
    print(f"Schuldenquote 2060: {z[2060]['schuldenquote']:.2f} % "
          f"(Parameter: {wert(P, 'schuldenquote_klub_2060')} %)")
    return 2 if abweichungen else 0


if __name__ == "__main__":
    sys.exit(main())
