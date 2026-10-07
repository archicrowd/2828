#!/usr/bin/env python3
"""Gesamtrechnung des Rahmenmodells (Stand B), Fassung des Gesamtkonzepts vom 6. Oktober 2026 (v3.12).

Eine Rechnung für alle Zahlen des Gesamtkonzepts. Die Formeln sind die der Originalskripte in
modell/rahmen/ (basis.py, final.py, pfad.py, tilgung.py, aufschlag.py, zahlen.py). Geändert sind nur
Eingänge und Regeln, und zwar aus Prüfung oder Entscheidung (Logbuch Band III, v3.11 und v3.12):

  * Einwohner 2024: Eurostat demo_gind AVG, daten/aggregate/laender_2024.csv (Korrektur 49)
  * effektiver Zins 2024: Zinsausgaben D41PAY / Schuldenstand, daten/aggregate/zinsausgaben_2024.csv
    (Korrektur 50; vorher 1,53 % aus 146 Mrd EUR)
  * Auslaufen des Altbestands ab 2024 (Entscheidung B6)
  * Quote = strenge Mindestquote, auf 0,1 Punkte aufgerundet (Korrektur 51, Regel)
  * Obergrenze von A aus Zentralfall und Einzelrisiken, auf volle Prozent aufgerundet (Entscheidung B9)
  * Sensitivität: Zentralfall 3,0 % nominal = 0,98 % real (Entscheidung B2)
  * Dividende je Land nach Preisniveau (Entscheidung B17, v3.20): der Dividendentopf des Klubs wird nach
    Einwohnern x Preisniveau verteilt; Deutschland erhält das Klubmittel x PLI_DE / PLI_Klub
  * Quotenkriterium (v3.20): die Dividende deckt in jedem Land und jedem Jahr das halbe Existenzminimum
    (halber Grundfreibetrag Deutschland in Preisen 2028, mit dem Preisniveau übertragen), auch ohne reales
    Wachstum; vorher 479 EUR je Kopf in Deutschland nach örtlichem BIP (Lesart von final.py)

Selbstprüfung: Mit den Eingängen der Fassung vom 4. Oktober (Zins 1,53, Auslauf 2028, Quote 30,6,
Einwohner aus basis.py) muss der Pfad final.pfad() aus dem Original exakt treffen. Sonst Abbruch.

Aufruf:  python3 modell/gesamtrechnung.py
Ausgabe: daten/aggregate/gesamtrechnung.json (alle Zahlen des Konzepts, ungerundet),
         daten/aggregate/gesamtrechnung_pfad.csv, daten/aggregate/gesamtrechnung_obergrenze.csv,
         daten/aggregate/deckung_quote.csv (B12)
"""
import contextlib
import csv
import io
import json
import math
import sys
import tomllib
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
AGG = WURZEL / "daten" / "aggregate"
RAHMEN = WURZEL / "modell" / "rahmen"
LAENDER = ("FR", "BE", "ES", "AT", "SI", "DE", "EE", "NL", "DK", "IE")
NAMEN = {"FR": "Frankreich", "BE": "Belgien", "ES": "Spanien", "AT": "Österreich", "SI": "Slowenien",
         "DE": "Deutschland", "EE": "Estland", "NL": "Niederlande", "DK": "Dänemark", "IE": "Irland"}


def originale():
    alt = list(sys.path)
    sys.path.insert(0, str(RAHMEN))
    for n in ("basis", "final", "pfad", "tilgung"):
        sys.modules.pop(n, None)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import basis
            import final
            import pfad as opfad
    finally:
        sys.path[:] = alt
    return basis, final, opfad


basis, final, opfad = originale()
T = tomllib.loads((WURZEL / "modell" / "gesamtrechnung.toml").read_text(encoding="utf-8"))
PAR = {p["name"]: p["wert"] for p in T["parameter"]}
for p in T["parameter"]:
    for feld in ("name", "wert", "einheit", "bezugsjahr", "preisbasis", "quelle", "status"):
        if feld not in p:
            sys.exit(f"FEHLER: Feld {feld} fehlt bei {p.get('name')}")

# ---------------------------------------------------------------- Eingänge
GDP, SCHULD, RENDITE = basis.GDP, basis.SCHULD, basis.RENDITE          # Eurostat 2024, Mio EUR / %
F2428 = basis.F2428
with open(AGG / "laender_2024.csv", encoding="utf-8") as f:
    POP = {r["land"]: float(r["einwohner_mio_2024"]) * 1e6 for r in csv.DictReader(f)}
with open(AGG / "preisniveau_2024.csv", encoding="utf-8") as f:
    PLI = {r["land"]: float(r["preisniveau_eu27_100"]) for r in csv.DictReader(f)}
with open(AGG / "zinsausgaben_2024.csv", encoding="utf-8") as f:
    ZINS = {r["land"]: float(r["zinsausgaben_mio_eur_2024_nominal"]) for r in csv.DictReader(f)}

A_POSTEN, B_POSTEN = opfad.A_POSTEN, opfad.B_POSTEN
A_SUM, B_AUFG, V_ZIEL = opfad.A_SUM, opfad.B_AUFG, opfad.V_ZIEL
A_OHNE_V = opfad.A_OHNE_V
BODEN, KIND_ANT, SCHULE = opfad.BODEN, opfad.KIND_ANT, opfad.SCHULE
V_START, V_JAHR = float(PAR["verteidigung_start"]), int(PAR["verteidigung_zieljahr"])
G_NOM, PREIS = float(PAR["wachstum_nominal"]) / 100, float(PAR["preissteigerung"]) / 100
VERSPRECHEN = float(PAR["versprechen_de_monat"])
I_ZIEL = float(PAR["garantiezins_klub"])
REST = float(PAR["restlaufzeit_schulden"])
D28 = float(PAR["schuldenquote_klub_2028"])
VORLAUF = 2028 - int(PAR["auslauf_beginn_jahr"])

BIP24_KLUB = sum(GDP.values()) / 1000
BIP28_KLUB = BIP24_KLUB * F2428
BIP28_DE = GDP["DE"] / 1000 * F2428
POP_KLUB = sum(POP.values())
KOPF_KLUB = BIP28_KLUB * 1e9 / POP_KLUB
KOPF_DE = BIP28_DE * 1e9 / POP["DE"]

# Länderdividende und Quotenkriterium (v3.20)
K_MINDER = float(PAR["anteil_minderjaehrige"]) / 100
PLI_KLUB = sum(POP[c] * PLI[c] for c in POP) / POP_KLUB          # einwohnergewichtet
R_DE = PLI["DE"] / PLI_KLUB                                         # Deutschland gegen Klubmittel
ANKER_DE = (float(PAR["existenzminimum_de_jahr"]) * (1 + PREIS) ** (2028 - 2026) / 12 / 2)  # je Erw., Preise 2028
SCHWELLE_KLUB = ANKER_DE / R_DE * (1 - K_MINDER / 2)                # je Einwohner des Klubs und Monat
D_ABS24 = sum(GDP[k] * SCHULD[k] / 100 for k in GDP)                   # Mio EUR
D_START_BER = D_ABS24 / sum(GDP.values()) * 100                         # 78,45 %
I_ALT = sum(ZINS.values()) / D_ABS24 * 100                              # effektiver Zins 2024
I_MARKT = sum(GDP[k] * SCHULD[k] / 100 * RENDITE[k] for k in GDP) / D_ABS24


# ---------------------------------------------------------------- Zeitpfad
def pfad(quote, *, i_alt=None, vorlauf=None, d0=None, v_ziel=V_ZIEL, g_nom=G_NOM, preis=PREIS,
         i_ziel=None, rest=None, tilg=0.0, jahre=33, kopf_de=None, kopf_klub=None):
    i_alt = I_ALT if i_alt is None else i_alt
    vorlauf = VORLAUF if vorlauf is None else vorlauf
    d = D28 if d0 is None else d0
    i_ziel = I_ZIEL if i_ziel is None else i_ziel
    rest = REST if rest is None else rest
    kopf_de = KOPF_DE if kopf_de is None else kopf_de
    kopf_klub = KOPF_KLUB if kopf_klub is None else kopf_klub
    g_real = (1 + g_nom) / (1 + preis) - 1
    out = []
    for j in range(2028, 2028 + jahre):
        t = j - 2028
        v = v_ziel if j >= V_JAHR else V_START + (v_ziel - V_START) * t / (V_JAHR - 2028)
        s = i_alt + (i_ziel - i_alt) * min((t + vorlauf) / rest, 1.0)
        zd = d * s / 100
        tl = tilg if d > tilg else max(d, 0.0)
        a = A_OHNE_V + v + zd
        div = quote - a - B_AUFG - tl
        out.append(dict(jahr=j, v=v, d=d, s=s, zd=zd, a=a, div=div,
                        de_fix=div / 100 * kopf_de / 12,
                        de_real=div / 100 * kopf_de * (1 + g_real) ** t / 12,
                        kl_real=div / 100 * kopf_klub * (1 + g_real) ** t / 12,
                        de_land=div / 100 * kopf_klub * R_DE * (1 + g_real) ** t / 12))
        d = (d - tl) / (1 + g_nom)
    return out


def mindestquote(feld="de_fix", schwelle=None, **kw):
    schwelle = VERSPRECHEN if schwelle is None else schwelle
    lo, hi = 20.0, 45.0
    for _ in range(90):
        m = (lo + hi) / 2
        if min(r[feld] for r in pfad(m, **kw)) < schwelle:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


# ---------------------------------------------------------------- Selbstprüfung
def selbstpruefung():
    ref = final.pfad()
    neu = pfad(30.60, i_alt=1.53, vorlauf=0, d0=basis.D_START,
               kopf_de=basis.KOPF_DE, kopf_klub=basis.KOPF_KLUB)
    for a, b in zip(ref, neu):
        for k in ("v", "d", "zd", "a", "div", "de_fix", "de_real", "kl_real"):
            if abs(a[k] - b[k]) > 1e-9:
                sys.exit(f"SELBSTPRÜFUNG FEHLGESCHLAGEN: {a['jahr']} {k} {a[k]} gegen {b[k]}")
    return len(ref)


def aufrunden(x, schritt):
    return math.ceil(round(x / schritt, 9)) * schritt


def main() -> int:
    n_geprueft = selbstpruefung()
    W: dict = {"fassung": T["modell"]["fassung"], "version": T["modell"]["version"]}

    # Basis
    W.update(bip24_klub_mrd=BIP24_KLUB, faktor=F2428, bip28_klub_mrd=BIP28_KLUB, bip28_de_mrd=BIP28_DE,
             pop_klub_mio=POP_KLUB / 1e6, kopf_klub=KOPF_KLUB, kopf_de=KOPF_DE,
             de_ueber_klub_pct=(KOPF_DE / KOPF_KLUB - 1) * 100,
             de_anteil_bip_pct=GDP["DE"] / sum(GDP.values()) * 100,
             schuld24_mrd=D_ABS24 / 1000, schuldenquote_ber=D_START_BER, schuldenquote_2028=D28,
             zinsausgaben24_mrd=sum(ZINS.values()) / 1000,
             zinsausgaben24_pct_bip=sum(ZINS.values()) / sum(GDP.values()) * 100,
             zins_eff_2024=I_ALT, zins_markt_2024=I_MARKT, garantiezins=I_ZIEL, restlaufzeit=REST,
             auslauf_beginn=2028 - VORLAUF, irland_faktor=(GDP["IE"] * 1e6 / POP["IE"]) / (
                 BIP24_KLUB * 1e9 / POP_KLUB))

    # Quote
    # Strenge Lesart (v3.12, Korrektur 51): real kein Wachstum heißt nominal = Preissteigerung, auch für
    # den Schuldenabbau. final.py hielt nur den Kopfbetrag fest und ließ die Schuld mit 3 % nominal schrumpfen.
    # Seit v3.20: Kriterium halbes Existenzminimum am Wohnort (Klubtopf gegen Bedarf), streng
    mq_streng = mindestquote("kl_real", schwelle=SCHWELLE_KLUB, g_nom=PREIS)
    mq_original_lesart = mindestquote("de_fix")
    mq_zentral = mindestquote("kl_real", schwelle=SCHWELLE_KLUB)
    W.update(mq_479_v2_streng=mindestquote("de_real", g_nom=PREIS),
             mq_479_v3a_streng=mindestquote("kl_real", schwelle=VERSPRECHEN / R_DE, g_nom=PREIS),
             mq_514_v3a_streng=mindestquote("kl_real", schwelle=SCHWELLE_KLUB * (1 + PREIS) ** -2, g_nom=PREIS),
             anker_de=ANKER_DE, schwelle_klub=SCHWELLE_KLUB, schwelle_de_kopf=ANKER_DE * (1 - K_MINDER / 2),
             pli_klub=PLI_KLUB, r_de=R_DE)
    q = round(aufrunden(mq_streng, float(PAR["quote_rundung"])), 2)
    W.update(mindestquote_streng=mq_streng, mindestquote_original_lesart=mq_original_lesart,
             mindestquote_zentral=mq_zentral, quote=q, boden=BODEN,
             einzug=q - BODEN)
    # zum Vergleich: alte Fassung, nur Zins neu bzw. nur Auslauf neu
    W["mq_alt_fassung"] = mindestquote("de_fix", i_alt=1.53, vorlauf=0, kopf_de=basis.KOPF_DE)
    W["mq_alt_fassung_streng"] = mindestquote("de_real", g_nom=PREIS, i_alt=1.53, vorlauf=0, kopf_de=basis.KOPF_DE)
    W["mq_nur_zins"] = mindestquote("de_real", g_nom=PREIS, vorlauf=0)
    W["mq_nur_auslauf"] = mindestquote("de_real", g_nom=PREIS, i_alt=1.53)
    
    P = pfad(q)
    by = {r["jahr"]: r for r in P}
    p0 = P[0]
    mx = max(P, key=lambda r: r["a"])
    tief = min(P, key=lambda r: r["de_land"])
    tief_fix = min(P, key=lambda r: r["de_fix"])
    W.update(a_2028=p0["a"], zd_2028=p0["zd"], zins_2028=p0["s"], zd_2028_mrd=p0["zd"] / 100 * BIP28_KLUB,
             div_2028=p0["div"], b_verfuegt_2028=q - p0["a"],
             a_hoechst=mx["a"], a_hoechst_jahr=mx["jahr"], div_2060=P[32]["div"],
             div_aenderung_pct=(P[32]["div"] / p0["div"] - 1) * 100,
             de_tief=tief["de_land"], de_tief_jahr=tief["jahr"],
             de_tief_fix=tief_fix["de_fix"], de_tief_fix_jahr=tief_fix["jahr"],
             de_tief_ueber_versprechen_pct=(tief["de_land"] / (ANKER_DE * (1 - K_MINDER / 2)) - 1) * 100,
             de_rueckgang_pct=(tief["de_land"] / p0["de_land"] - 1) * 100,
             de_anstieg_2060_pct=(P[32]["de_land"] / p0["de_land"] - 1) * 100,
             kl_tief=min(r["kl_real"] for r in P),
             kl_tief_jahr=min(P, key=lambda r: r["kl_real"])["jahr"],
             g_real=(1 + G_NOM) / (1 + PREIS) - 1)
    W["tabelle_pfad"] = [dict(jahr=j, v=by[j]["v"], d=by[j]["d"], zd=by[j]["zd"], a=by[j]["a"],
                              div=by[j]["div"], klub=by[j]["kl_real"], de=by[j]["de_land"])
                         for j in (2028, 2030, 2035, 2040, 2050, 2060)]
    for j in (2028, 2035, 2060):
        W[f"de_{j}"] = by[j]["de_land"]
        W[f"klub_{j}"] = by[j]["kl_real"]

    # Struktur 2028 in EUR je Kopf
    kopf = lambda pct: pct / 100 * KOPF_KLUB
    W["tabelle_einzug"] = [
        ("Gesamtaufkommen", q, kopf(q)), ("   davon zieht A ein", q - BODEN, kopf(q - BODEN)),
        ("   davon erhebt B selbst (Bodenabgabe)", BODEN, kopf(BODEN)),
        ("A behält 2028", p0["a"], kopf(p0["a"])), ("B verfügt 2028", q - p0["a"], kopf(q - p0["a"])),
        ("   B Fachaufgaben", B_AUFG, kopf(B_AUFG)), ("   B Dividende", p0["div"], kopf(p0["div"]))]
    W["tabelle_a"] = [(n, v, v / 100 * BIP28_KLUB) for n, v in A_POSTEN] + [("Summe", A_SUM, A_SUM / 100 * BIP28_KLUB)]
    W["tabelle_b"] = [(n, v, v / 100 * BIP28_KLUB) for n, v in B_POSTEN] + [("Summe", B_AUFG, B_AUFG / 100 * BIP28_KLUB)]
    W["boden_kopf"] = kopf(BODEN)
    W["boden_anteil_fach_pct"] = BODEN / B_AUFG * 100

    # Formel
    je_einw = (B_AUFG - SCHULE) / 100 * KOPF_KLUB
    je_kind = SCHULE / 100 * KOPF_KLUB / KIND_ANT
    W.update(formel_einw=je_einw, formel_kind=je_kind, kind_ant=KIND_ANT * 100,
             fach_12=je_einw + je_kind * 0.12, fach_schnitt=je_einw + je_kind * KIND_ANT,
             fach_20=je_einw + je_kind * 0.20)

    # Verwaltung
    verw = dict(B_POSTEN)["Kommunalverwaltung"]
    W.update(verw_anteil_pct=verw / B_AUFG * 100, verw_ersparnis_pkt=verw - B_AUFG * 0.058,
             verw_ersparnis_eur=(verw - B_AUFG * 0.058) / 100 * KOPF_KLUB / 12)

    # Obergrenze (B9)
    faelle = [("Zentralfall", {}),
              (f"Zielzins ohne Garantie ({I_MARKT:.2f} %)".replace(".", ","), dict(i_ziel=I_MARKT)),
              ("nominales Wachstum 1,5 %", dict(g_nom=0.015)),
              (f"Schuldenquote 2028 bei {D28 + 3.5:.1f} %".replace(".", ","), dict(d0=D28 + 3.5)),
              ("alle drei Finanzierungsrisiken zugleich", dict(i_ziel=I_MARKT, g_nom=0.015, d0=D28 + 3.5)),
              ("Verteidigung 3,5 % (Haager Zusage)", dict(v_ziel=3.5)),
              ("Verteidigung 2,0 % (COFOG-vergleichbar)", dict(v_ziel=2.0))]
    og = []
    for name, kw in faelle:
        Q = pfad(q, **kw)
        m = max(Q, key=lambda r: r["a"])
        og.append(dict(fall=name, jahr=m["jahr"], a=m["a"], pct_einzug=m["a"] / (q - BODEN) * 100))
    massgeblich = [o["pct_einzug"] for o in og[:4]]
    obergrenze = aufrunden(max(massgeblich), float(PAR["obergrenze_regel_rundung"]))
    for o in og:
        o["abstand"] = obergrenze - o["pct_einzug"]
    W.update(obergrenze=obergrenze, obergrenze_berechnet=og[0]["pct_einzug"], tabelle_obergrenze=og,
             obergrenze_anteil_schuld=obergrenze / 100 * (q - BODEN) / D28 * 100,
             a_anteil_schuld=p0["a"] / D28 * 100)

    # Sensitivität (B2): Zeilen reales Wachstum, nominal gekoppelt; Zentralfall 3,0 % nominal
    sens = []
    for g, name in ((0.0, "0,0 %"), (0.005, "0,5 %"), (None, "0,98 % (3,0 % nominal) — Zentralfall"),
                    (0.015, "1,5 %"), (0.020, "2,0 %")):
        gn = G_NOM if g is None else (1 + g) * (1 + PREIS) - 1
        S = pfad(q, g_nom=gn)
        sens.append(dict(fall=name, e2035=S[7]["de_land"], e2060=S[32]["de_land"],
                         gegen=(S[32]["de_land"] / S[0]["de_land"] - 1) * 100))
    W["tabelle_sens"] = sens

    # Gegenprobe: Quote 27,91 (nationales Modell)
    Q = pfad(27.91)
    unter = [r["jahr"] for r in Q if r["kl_real"] < SCHWELLE_KLUB]
    W.update(q2791_jahre=len(unter), q2791_bis=unter[-1] if unter else None)

    # Tilgung
    O, M = pfad(q, jahre=43), pfad(q, tilg=0.50, jahre=43)
    kum, be = 0.0, None
    for a, b in zip(O, M):
        kum += b["de_land"] - a["de_land"]
        if be is None and kum >= 0 and a["jahr"] > 2029:
            be = a["jahr"]
    W.update(tilg_verzicht=O[0]["de_land"] - M[0]["de_land"], tilg_break_even=be)
    W["punkt_bip_eur_de"] = 1.0 / 100 * KOPF_KLUB * R_DE / 12

    # Aufschlag (Bemessung am BIP, aufschlag.py; Satz des Startjahrs 2028)
    s28 = p0["s"]
    # Finanzierungssatz aus der berechneten, ungerundeten Schuldenquote: so summiert sich der Aufschlag
    # exakt auf null (das Original setzte 78,4 und kam auf 0,0955 Mrd, v3.8)
    satz = D_START_BER * s28 / 100
    a_kopf = p0["a"] / 100 * KOPF_KLUB
    auf = []
    summe = 0.0
    for k in LAENDER:
        bip28 = GDP[k] / 1000 * F2428
        kp = bip28 * 1e9 / POP[k]
        aus = SCHULD[k] / 100 * bip28 * s28 / 100 * 1e9 / POP[k]
        ein = satz / 100 * kp
        auf.append(dict(land=NAMEN[k], schuld=SCHULD[k], aus=aus, ein=ein, auf=aus - ein))
        summe += (aus - ein) * POP[k] / 1e9
    auf.sort(key=lambda r: -r["auf"])
    W.update(tabelle_aufschlag=auf, aufschlag_summe_mrd=summe,
             aufschlag_max_anteil_a=max(abs(r["auf"]) for r in auf) / a_kopf * 100,
             aufschlag_max_pos_anteil_a=auf[0]["auf"] / a_kopf * 100, aufschlag_max_pos_land=auf[0]["land"],
             klub_punkt_bip_eur=1.0 / 100 * KOPF_KLUB / 12,
             aufschlag_satz=satz)

    # Last
    LH, GS = float(PAR["last_heute"]), float(PAR["gesundheit_ausserhalb"])
    W.update(last_heute=LH, steuern_heute=float(PAR["steuern_heute"]), sb_heute=float(PAR["sozialbeitraege_heute"]),
             gesundheit=GS, last_entwurf=q + GS, entlastung=LH - (q + GS),
             entlastung_mrd=(LH - (q + GS)) / 100 * BIP28_KLUB)

    # B12: Deckungsrahmen aus dem nationalen Modell (Stand A), deutsche Basis
    # Quelle: modell/kern/modell-2828-ergebnisse.txt, Abschnitt B, Stufe 50 %, Modellbasis 4.200 Mrd
    basis_kern = 4200.0
    # Einkommen seit v3.22: Stufen beim 1- bis 4-fachen Grundbedarf (v3.21: bis 5-fach) (modell/tarif_grundbedarf.py, gleiche
    # Aufkommensfunktion des nationalen Modells); vorher 313,3 Mrd mit Stufen 12.348/25.000/40.000/55.000/70.000
    TG = json.loads((AGG / "tarif_grundbedarf.json").read_text(encoding="utf-8"))
    kern = [("01 Einkommen (Stufen 1- bis 4-facher Grundbedarf, 0/9/16/21/28 %, Dividende steuerpflichtig)",
             TG["einkommen_modell_mrd_neu"]),
            ("02 Kapital 28 %", 48.8), ("06 Konsum (Label, effektiv 20,0 %)", 375.9),
            ("05 Konzerne und Plattformen 28 %", 157.6), ("03 Erbschaft 28 %", 35.9),
            ("04c Vermögen, Mindeststeuer (anrechenbar)", 20.7), ("07 Klima, CO₂ 100 €/t netto", 55.0),
            ("Sonstige Steuern (Energie, Tabak u. a.)", 165.0)]
    bausteine = [("Vermögensteuer 1 % ab 2 Mio (nicht anrechenbar)", 12.0),
                 ("Abbau klimaschädlicher Subventionen", 20.0), ("CO₂-Pfad 100 → 150 €/t", 15.0)]
    zeilen = [(n, m / basis_kern * 100, "Kernsystem") for n, m in kern]
    zeilen += [(n, m / basis_kern * 100, "Baustein") for n, m in bausteine]
    kernsumme = sum(m for _, m in kern) / basis_kern * 100
    mit_bausteinen = kernsumme + sum(m for _, m in bausteine) / basis_kern * 100
    zeilen.append(("04a Bodenwertabgabe (Ebene B, Satz bis 1 %)", BODEN, "Stand B"))
    gedeckt = mit_bausteinen + BODEN
    W.update(tabelle_deckung=zeilen, deckung_kern=kernsumme, deckung_mit_bausteinen=mit_bausteinen,
             deckung_gesamt=gedeckt, deckung_luecke=q - gedeckt,
             deckung_luecke_mrd_klub=(q - gedeckt) / 100 * BIP28_KLUB)

    W["selbstpruefung_jahre"] = n_geprueft
    # Dividende je Erwachsenem und je Kind (Kinder zur Hälfte): Schnitt je Einwohner / (1 - k/2)
    k = float(PAR["anteil_minderjaehrige"]) / 100
    W["anteil_minderjaehrige"] = k * 100
    for j in (2028, 2035, 2060):
        W[f"erw_{j}"] = W[f"klub_{j}"] / (1 - k / 2)
        W[f"kind_{j}"] = W[f"erw_{j}"] / 2
        W[f"erw_de_{j}"] = W[f"erw_{j}"] * R_DE
        W[f"kind_de_{j}"] = W[f"erw_de_{j}"] / 2
    # Länderdividende (B17, v3.20): je Erwachsenem und Monat, Preise 2028; Boden = halbes Existenzminimum
    ST = pfad(q, g_nom=PREIS)
    st_min = min(r["kl_real"] for r in ST) / (1 - k / 2)
    W["tabelle_laender_div"] = [dict(
        land=c, name=NAMEN[c], pli=PLI[c], boden=ANKER_DE * PLI[c] / PLI["DE"],
        e2028=W["erw_2028"] * PLI[c] / PLI_KLUB, e2035=W["erw_2035"] * PLI[c] / PLI_KLUB,
        e2060=W["erw_2060"] * PLI[c] / PLI_KLUB, streng_min=st_min * PLI[c] / PLI_KLUB)
        for c in sorted(LAENDER, key=lambda c: -PLI[c])]
    W["streng_min_erw_klub"] = st_min
    W["streng_min_jahr"] = min(ST, key=lambda r: r["kl_real"])["jahr"]
    W["deckung_boden_2028_pct"] = p0["kl_real"] / SCHWELLE_KLUB * 100
    # Reihen für die Webseite: Dividende je Erwachsenem (Klub, Preise 2028) je Wachstumsfall; Anteile am Aufkommen
    W["reihe_jahre"] = [r["jahr"] for r in P]
    W["reihe_erw"] = {}
    for name, g in (("0,0", 0.0), ("0,5", 0.005), ("1,0", None), ("1,5", 0.015), ("2,0", 0.020)):
        gn = G_NOM if g is None else (1 + g) * (1 + PREIS) - 1
        W["reihe_erw"][name] = [r["de_land"] / (1 - k / 2) for r in pfad(q, g_nom=gn)]
    W["reihe_a"] = [r["a"] for r in P]
    W["reihe_d"] = [r["d"] for r in P]
    W["reihe_div"] = [r["div"] for r in P]
    W["b_fach"] = B_AUFG
    W["tarif_stufen_de_2028"] = TG["stufen_de_2028"]
    W["tarif_aenderung_pct_bip"] = TG["aenderung_pct_bip"]
    # Externe Kennzahlen der Ausgangslage (nur durchgereicht, Quelle im toml)
    for k in ("abgabenkeil_de_2024", "abgabenkeil_oecd_2024", "abgeltungsteuer_de", "anteil_mit_mehr_de"):
        W[k] = float(PAR[k])

    # Ausgaben
    (AGG / "gesamtrechnung.json").write_text(json.dumps(W, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(AGG / "gesamtrechnung_pfad.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["jahr", "verteidigung_pct_bip", "schuldenquote_pct_bip", "zinssatz_pct", "zinsdienst_pct_bip",
                    "a_gesamt_pct_bip", "dividende_anteil_pct_bip", "klub_eur_monat_real2028",
                    "de_eur_monat_real2028", "de_eur_monat_kopfbetrag_fest_3pct_nominal"])
        for r in P:
            w.writerow([r["jahr"]] + [f"{r[k]:.4f}" for k in ("v", "d", "s", "zd", "a", "div")]
                       + [f"{r[k]:.2f}" for k in ("kl_real", "de_real", "de_fix")])
    with open(AGG / "gesamtrechnung_obergrenze.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["fall", "jahr_hoechstbedarf", "a_pct_bip", "pct_des_einzugs", "abstand_zur_obergrenze"])
        for o in og:
            w.writerow([o["fall"], o["jahr"], f"{o['a']:.3f}", f"{o['pct_einzug']:.2f}", f"{o['abstand']:.2f}"])
    with open(AGG / "deckung_quote.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["position", "pct_bip_deutsche_basis", "art"])
        for n, v, a in zeilen:
            w.writerow([n, f"{v:.3f}", a])
        w.writerow(["Summe gedeckt", f"{gedeckt:.3f}", ""])
        w.writerow([f"Quote {q:.1f}".replace(".", ","), f"{q:.3f}", ""])
        w.writerow(["Lücke", f"{q - gedeckt:.3f}", "offen"])

    print(f"Selbstprüfung gegen final.pfad(): {n_geprueft} Jahre exakt")
    print(f"Kriterium: halbes Existenzminimum DE {ANKER_DE:.2f} EUR/Erw. (Preise 2028), PLI Klub {PLI_KLUB:.2f}, "
          f"R_DE {R_DE:.4f}, Schwelle {SCHWELLE_KLUB:.2f} EUR je Klub-Einwohner; Vergleich 479-DE alt "
          f"{W['mq_479_v2_streng']:.3f}, 479-DE V3a {W['mq_479_v3a_streng']:.3f}, 514,50 V3a {W['mq_514_v3a_streng']:.3f}")
    print(f"Einwohner {POP_KLUB/1e6:.3f} Mio, Zins 2024 {I_ALT:.3f} % ({sum(ZINS.values())/1000:.1f} Mrd), "
          f"Marktrendite {I_MARKT:.2f} %, Auslauf ab {2028 - VORLAUF}")
    print(f"Original-Lesart (Kopfbetrag fest, Schuld 3 % nominal): {mq_original_lesart:.3f}")
    print(f"Mindestquote streng {mq_streng:.3f} (alt {W['mq_alt_fassung']:.3f}, nur Zins {W['mq_nur_zins']:.3f}, "
          f"nur Auslauf {W['mq_nur_auslauf']:.3f}), zentral {mq_zentral:.3f} -> Quote {q:.1f} %")
    print(f"2028: Zinsdienst {p0['zd']:.3f} % ({p0['s']:.3f} %), A {p0['a']:.3f}, Dividende {p0['div']:.3f} % "
          f"= Klub {p0['kl_real']:.1f} / DE {p0['de_land']:.1f} EUR je Kopf (nach örtlichem BIP {p0['de_real']:.1f})")
    print(f"Höchstbedarf A {mx['a']:.3f} % ({mx['jahr']}) = {og[0]['pct_einzug']:.2f} % des Einzugs -> Obergrenze {obergrenze:.0f} %")
    for o in og:
        print(f"   {o['fall']:<45}{o['jahr']:>6}{o['a']:>8.2f}{o['pct_einzug']:>8.2f}{o['abstand']:>7.2f}")
    print(f"Tiefpunkt DE {tief['de_land']:.1f} ({tief['jahr']}), streng Klub je Erw. {W['streng_min_erw_klub']:.1f} ({W['streng_min_jahr']}); 2060 DE {P[32]['de_land']:.1f}, "
          f"Klub 2035 {by[2035]['kl_real']:.1f}, 2060 {by[2060]['kl_real']:.1f}")
    print(f"Deckung (B12): Kern {kernsumme:.2f} + Bausteine -> {mit_bausteinen:.2f} + Boden -> {gedeckt:.2f}; "
          f"Lücke {q-gedeckt:.2f} Punkte = {W['deckung_luecke_mrd_klub']:.0f} Mrd EUR Klub 2028")
    print(f"Aufschlag Summe {summe:.4f} Mrd; Entlastung {W['entlastung']:.2f} Punkte = {W['entlastung_mrd']:.0f} Mrd")
    return 0


if __name__ == "__main__":
    sys.exit(main())
