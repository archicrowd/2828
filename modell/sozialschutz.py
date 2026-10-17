#!/usr/bin/env python3
"""Sozialschutz im Konzept (Logbuch v3.42): Was liegt heute außerhalb des Rahmens, und was kostet der Übergang?

Zusammenführung der Vorschläge vom 16.10.2026 („Generationenbaustein“: Gemeinsames, Eigenes E, Zugesagtes Z; „Hütte · eigene Route ·
Seil“). VORBEREITUNG: bewegt keine Zahl der Gesamtrechnung. Ergebnis: daten/aggregate/sozialschutz.json und z_pfad.csv.

Teil 1  Zerlegung: Sozialschutz heute (COFOG GF10 je Untergruppe, Eurostat 2024) gegen die Dividende des Konzepts. Je Untergruppe
        Anteile Hütte / Route / Seil (Setzung, sozialschutz.toml). Hütte-Bedarf gegen Dividende; Route und Seil als Pflichtzahlungen
        außerhalb der Steuern.
Teil 2  Zugesagtes (Z, Rechenauftrag R-Z1, vereinfacht): Rentenausgaben (GF1002 + GF1003) über der Dividende der Rentner, nur der
        Teil, der vor dem Stichtag erworben wurde. Kohortenschema: Rentnerjahrgänge gleich verteilt über die Bezugsdauer; ein Jahrgang
        hat den Anteil seiner Erwerbsjahre vor dem Stichtag erworben. Ausgabenniveau je Rentner wie 2024 (in % des BIP, also mit dem BIP
        je Kopf fortgeschrieben); Zahl der Rentner nach dem Ageing Report der Kommission, wo vorhanden, sonst konstant. SCHÄTZUNG.
Teil 3  Wirkung auf die Abgabenquote je Finanzierungsvariante (Z aus Steuern / teils Schuld; Gesundheit Hütte-Anteil 0–90 %;
        Härtefall-Spanne) und auf die Gesamtlast-Aussage.
"""
import csv
import json
import sys
import tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "sozialschutz.toml").read_text(encoding="utf-8"))
G = json.loads((AGG / "gesamtrechnung.json").read_text(encoding="utf-8"))
D = json.loads((AGG / "sozialschutz_2024.json").read_text(encoding="utf-8"))
GDP = {r["land"]: float(r["bip_mio_eur_2024_nominal"]) for r in csv.DictReader(open(AGG / "laender_2024.csv", encoding="utf-8"))}
LAENDER = ["BE", "DK", "DE", "EE", "IE", "FR", "NL", "AT", "SI", "ES"]
CODES = [f"GF100{i}" for i in range(1, 10)]


def gewicht():
    """BIP-Gewichte der zehn Staaten aus der Gesamtrechnung (Anteile am Klub-BIP 2024)."""
    if GDP:
        s = sum(GDP[c] for c in LAENDER)
        return {c: GDP[c] / s for c in LAENDER}
    raise SystemExit("BIP je Land fehlt in laender_2024.csv")


def wert(c, code):
    return float(D["cofog"][c][code]["wert"])


def zerlegung(w):
    z = P["zuordnung"]
    erg = {}
    for c in LAENDER + ["KLUB"]:
        h = r = s = 0.0
        zeilen = {}
        for code in CODES:
            v = sum(w[l] * wert(l, code) for l in LAENDER) if c == "KLUB" else wert(c, code)
            a = z[code]
            zeilen[code] = v
            h += v * a[0] / 100
            r += v * a[1] / 100
            s += v * a[2] / 100
        gf10 = sum(zeilen.values())
        erg[c] = dict(gf10=round(gf10, 2), huette=round(h, 2), route=round(r, 2), seil=round(s, 2), untergruppen=zeilen)
    return erg


def z_anteil_vor_stichtag(jahr):
    """Anteil der Rentenausgaben im Jahr `jahr`, der auf Erwerbsjahre vor dem Stichtag entfällt (Kohortenschema)."""
    st, eb, ra, bd = (P["stichtag"][k] for k in ("jahr", "erwerbsbeginn_alter", "rentenalter", "bezugsdauer_jahre"))
    karriere = ra - eb
    anteile = []
    for k in range(bd):                       # Rentnerjahrgang, seit k Jahren in Rente
        eintritt = jahr - k                    # Jahr des Renteneintritts
        beginn = eintritt - karriere
        anteile.append(min(max((st - beginn) / karriere, 0.0), 1.0))
    return sum(anteile) / bd


# v3.48 (Beschluss): Renten werden um die eingesparten Sozialbeiträge der Rentner gekürzt (Anteil der Bruttorente). 0 = keine Kürzung
# (Standard dieses Skripts); altlasten.py setzt den Wert aus seinem Parameterfile.
KUERZUNG = 0.0


def z_pfad(c, rente_pct, anteil65, div_erw_pct_kopf, faktor_rentner):
    """Z in % des BIP je Jahr. rente_pct: GF1002+GF1003 2024; div_erw_pct_kopf: Dividende je Erwachsenem in % des BIP je Kopf (Jahr)."""
    je_rentner = rente_pct / anteil65 * 100      # Rentenausgabe je Rentner in % des BIP je Kopf (Annahme: Rentner = 65+)
    out = []
    for j in range(2028, 2101):
        f = z_anteil_vor_stichtag(j)
        zahl = anteil65 * faktor_rentner(j)      # Rentner in % der Bevölkerung
        anspruch = je_rentner * f * (1 - KUERZUNG)   # erworbener Anspruch je Rentner, ggf. um eingesparte Beiträge gekürzt
        ueber = max(anspruch - div_erw_pct_kopf, 0.0)   # Z = erworbener Anspruch über der Dividende (die jeder Rentner erhält)
        out.append(dict(land=c, jahr=j, anteil_vor_stichtag=round(f, 4), z_pct_bip=round(zahl / 100 * ueber, 3)))
    return out


def faktor_rentner(c):
    ar = D.get("ageing_report", {})

    def fak(j):
        r = ar.get(c, {})
        pts = sorted((int(y), float(v)) for y, v in r.get("pct_bip", {}).items()) if r else []
        if not pts:
            return 1.0
        base = pts[0][1]
        prev = pts[0]
        for y, v in pts:
            if j <= y:
                y0, v0 = prev
                vv = v0 + (v - v0) * (j - y0) / (y - y0) if y > y0 else v
                return vv / base
            prev = (y, v)
        return prev[1] / base
    return fak


def z_laender(div_erw):
    """Z je Land (Pfad 2028–2100) bei einer Dividende je Erwachsenem von div_erw (% des BIP je Kopf). Auch für Varianten (v3.43)."""
    pfade, roh, skal = {}, {}, {}
    for c in LAENDER:
        rente = wert(c, "GF1002") + wert(c, "GF1003")
        a65 = float(D["anteil_65plus"][c]["wert"])
        fak = faktor_rentner(c)
        # Variante „nach erworbenen Ansprüchen“: Skalierung auf die Tabelle 29 (nasa_10_pens1, S13PU, 2021), wo diese kleiner ist als
        # der Barwert der vor dem Stichtag erworbenen Rentenausgaben (Diskont 1 % real über dem Wachstum, Annahme). Wirkt vor allem für
        # Dänemark (Volksrente steuerfinanziert, keine Anwartschaft im Sinne der Tabelle 29).
        pv = sum(rente * z_anteil_vor_stichtag(j) / 1.01 ** (j - 2028) for j in range(2028, 2101))
        adl = (D.get("pension_entitlements", {}).get(c) or {}).get("S13PU_unfunded_pc_bip")
        skal[c] = min(1.0, float(adl) / pv) if adl else 1.0
        pfade[c] = z_pfad(c, rente * skal[c], a65, div_erw, fak)
        roh[c] = z_pfad(c, rente, a65, div_erw, fak)
    return pfade, roh, skal


def z_klub(div_erw, w=None):
    w = w or gewicht()
    pfade, _, _ = z_laender(div_erw)
    return [round(sum(w[c] * pfade[c][j - 2028]["z_pct_bip"] for c in LAENDER), 3) for j in range(2028, 2101)]


def main():
    w = gewicht()
    zl = zerlegung(w)
    k = G["anteil_minderjaehrige"] / 100
    div = G["div_2028"]                                  # Dividende in % des BIP (Klubschnitt 2028)
    div_erw = div / (1 - k / 2)                          # je Erwachsenem in % des BIP je Kopf
    pfade, roh, skal = z_laender(div_erw)
    # Klub: BIP-gewichtet
    jahre = range(2028, 2101)
    klub = [dict(jahr=j, z_pct_bip=round(sum(w[c] * pfade[c][j - 2028]["z_pct_bip"] for c in LAENDER), 3),
                 z_ohne_skalierung=round(sum(w[c] * roh[c][j - 2028]["z_pct_bip"] for c in LAENDER), 3)) for j in jahre]
    with open(AGG / "z_pfad.csv", "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["land", "jahr", "anteil_vor_stichtag", "z_pct_bip"])
        for c in LAENDER:
            for r in pfade[c]:
                wr.writerow([c, r["jahr"], r["anteil_vor_stichtag"], r["z_pct_bip"]])
        for r in klub:
            wr.writerow(["KLUB", r["jahr"], "", r["z_pct_bip"]])
    # Teil 3: Wirkung auf die Quote
    gs = G["gesundheit"]
    hf = P["haertefall"]["spanne_pct_bip"]
    z28 = klub[0]["z_pct_bip"]
    zmax = max(klub, key=lambda r: r["z_pct_bip"])
    ende = next((r["jahr"] for r in klub if r["jahr"] > zmax["jahr"] and r["z_pct_bip"] < 0.1), None)
    kum = sum(r["z_pct_bip"] for r in klub)
    var = []
    for ga in P["gesundheit"]["huette_anteil_varianten"]:
        for sa in P["z_finanzierung"]["schuldanteil_varianten"]:
            zusatz = gs * ga / 100 + z28 * (1 - sa) + sum(hf) / 2
            var.append(dict(gesundheit_huette_pct=ga, z_schuldanteil=sa, zusatz_quote_2028=round(zusatz, 2),
                            quote_2028=round(G["quote"] + zusatz, 2), luecke_2028=round(G["deckung_luecke"] + zusatz, 2)))
    kl = zl["KLUB"]
    # Dauerzustand nach dem Auslauf von Z: Dividende + Route + Seil + Härtefall gegen den Sozialschutz heute (GF10)
    dauer = round(div + kl["route"] + kl["seil"] + sum(hf) / 2, 2)
    # Schuldvariante: Z vollständig über neue Schuld (zusätzlich zum ausgeglichenen Haushalt der Gesamtrechnung), nominal 3 %,
    # Zins wie der Garantiezins der Gesamtrechnung; Schuldenquote aus der Gesamtrechnung (Pfad ohne Z) plus Zusatzschuld
    g, i = G["wachstum_nominal"] / 100 if "wachstum_nominal" in G else 0.03, G["garantiezins"] / 100
    zus, zmax_s, jmax = 0.0, 0.0, 2028
    for r in klub:
        zus = zus * (1 + i) / (1 + g) + r["z_pct_bip"]
        if zus > zmax_s:
            zmax_s, jmax = zus, r["jahr"]
    E = dict(version=P["version"], status="Vorbereitung, keine Zahl der Gesamtrechnung bewegt",
             zerlegung=zl, dividende_pct_bip=round(div, 2),
             huette_gegen_dividende=round(kl["huette"] - div, 2),
             ausserhalb_quote=dict(route=kl["route"], seil=kl["seil"], gesundheit_heute=gs),
             z=dict(z_2028=z28, z_max=zmax, unter_0_1_ab=ende, kumuliert_pct_bip_jahre=round(kum, 1),
                    z_2028_ohne_skalierung=klub[0]["z_ohne_skalierung"], skalierung_tabelle29={c: round(v, 2) for c, v in skal.items()},
                    je_land_2028={c: pfade[c][0]["z_pct_bip"] for c in LAENDER},
                    je_land_2050={c: pfade[c][22]["z_pct_bip"] for c in LAENDER},
                    pfad_klub={r["jahr"]: r["z_pct_bip"] for r in klub if r["jahr"] % 5 == 0}),
             varianten=var,
             dauerzustand=dict(sozialschutz_heute_gf10=kl["gf10"], konzept_nach_auslauf_z=dauer,
                               hinweis="Dividende + Route + Seil + Härtefall (Mitte), nach dem Auslauf von Z"),
             schuldvariante=dict(zusatzschuld_max_pct_bip=round(zmax_s, 1), jahr=jmax,
                                 hinweis="Z vollständig über neue Schuld, Zins = Garantiezins, nominales Wachstum 3 %"),
             z_gegen_sozialbeitraege_heute=round(z28 / G["sb_heute"] * 100, 1),
             gesamtlast=dict(heute=G["last_heute"], entwurf_bisher=G["last_entwurf"],
                             entwurf_mit_pflichtzahlungen_2028=round(G["last_entwurf"] + kl["route"] + kl["seil"] + z28 + sum(hf) / 2, 2)))
    (AGG / "sozialschutz.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Klub GF10 {kl['gf10']} % BIP: Hütte {kl['huette']}, Route {kl['route']}, Seil {kl['seil']}; Dividende {div:.2f}")
    print(f"Z 2028 {z28} % BIP, Höchstwert {zmax['z_pct_bip']} ({zmax['jahr']}), unter 0,1 ab {ende}; kumuliert {kum:.0f} Prozentpunkt-Jahre")
    print(f"Gesamtlast: heute {G['last_heute']}, Entwurf bisher {G['last_entwurf']}, mit Pflichtzahlungen 2028 {E['gesamtlast']['entwurf_mit_pflichtzahlungen_2028']}")
    for v in var:
        print(v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
