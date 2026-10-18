#!/usr/bin/env python3
"""Haushaltswirkung des Drittel-Systems (33F) gegen das heutige System (Logbuch v3.47). Prüfrechnung.

Heute: Nettoeinkommen nach Lohnsteuer, Soli, Sozialbeiträgen der Beschäftigten und Kindergeld (Kernmodell, Recht 2026); für 2035 mit den
Beitragssätzen der IGES-Projektion (Parameterfile).
33F: Bruttolohn zuzüglich weitergegebener Arbeitgeberbeiträge, Einkommensteuer 0/11/19/25/33 % auf Brutto + Dividende der Erwachsenen,
keine Sozialbeiträge, keine Prämien, Dividende des Jahres (Kinder die Hälfte, steuerfrei; 2035 aus dem Zeitpfad modell/projektion33.py),
Mehrbelastung durch den höheren effektiven Mehrwertsteuersatz auf den Konsum (Konsumquote des Kernmodells), optional ein Altlastenzuschlag
des Staates auf Einkommen- und Mehrwertsteuer, optional eigene Altersvorsorge in Höhe des heutigen Rentenbeitrags.
Grenzbelastung: Anteil eines zusätzlichen Euro Arbeitskosten, der nicht beim Haushalt ankommt (eigene Vorsorge zählt nicht als Belastung).
Nicht enthalten: Bürgergeld/Wohngeld (Fälle ohne Einkommen nicht gerechnet), Verhaltensänderungen.
Ausgabe: daten/aggregate/haushalte33.json
"""
import contextlib, importlib.util, io, itertools, json, sys, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "haushalte33.toml").read_text(encoding="utf-8"))
_AL = W / "daten" / "aggregate" / "altlasten.json"
if _AL.exists():   # v4.11: Altlastenzuschlag aus dem Fonds (Beschluss), nicht mehr von Hand
    P["zuschlag_pct"] = [0.0, json.loads(_AL.read_text(encoding="utf-8"))["beschluss"]["zuschlag_auf_alle_steuern_pct"]]
spec = importlib.util.spec_from_file_location("kern", W / "modell" / "kern" / "modell-2828.py")
K = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(K)
SV = json.loads((AGG / "systemvarianten.json").read_text(encoding="utf-8"))
PJ = json.loads((AGG / "projektion33.json").read_text(encoding="utf-8"))
v = next(x for x in SV["varianten"] if x["id"] == P["system"])
G26 = 12348.0
STUFEN = [G26 * x for x in (1, 1.5, 2, 3)]
SAETZE = v["einkommen_saetze"]
EFF_ALT = P["mwst_heute_effektiv"]
BASIS = (K.AN_KV_PV, K.AN_RV_AV)
JAHR = {r["jahr"]: r for r in PJ["reihe"]}
# v3.51: Dividende nach dem Beschluss zum starken Netz (netz33.json), falls vorhanden
_NZ = AGG / "netz33.json"
if _NZ.exists():
    for _r in json.loads(_NZ.read_text(encoding="utf-8"))["beschluss"]["reihe"]:
        if _r["jahr"] in JAHR:
            JAHR[_r["jahr"]] = dict(JAHR[_r["jahr"]], dividende_erw_eur2026=_r["dividende_erw_eur2026"])


def setze_jahr(j):
    """Beitragssätze heute im Jahr j (2028: Recht 2026; 2035: IGES-Projektion)."""
    plus = P["plus_2035"] if j >= 2035 else dict(rv_av=0.0, kv_pv=0.0)
    K.AN_KV_PV = BASIS[0] + plus["kv_pv"] / 200
    K.AN_RV_AV = BASIS[1] + plus["rv_av"] / 200


def div_jahr(j):
    return JAHR[j]["dividende_erw_eur2026"] * 12


def eff_jahr(j):
    return JAHR[j]["label_effektiv"]


def kq(n):
    """Konsumquote des Kernmodells (Stufen .95/.85/.75/.60), zwischen den Stufenmitten linear geglättet, damit die Grenzbelastung keine
    Sprünge an den Stufengrenzen zeigt (Abweichung vom Kernmodell höchstens eine halbe Stufe)."""
    pkt = [(12500, .95), (37500, .85), (65000, .75), (100000, .60)]
    if n <= pkt[0][0]:
        return pkt[0][1]
    for (a, x), (b, y) in zip(pkt, pkt[1:]):
        if n <= b:
            return x + (y - x) * (n - a) / (b - a)
    return pkt[-1][1]


def ag(b):
    return K.AN_KV_PV * min(b, K.BBG_KV) + K.AN_RV_AV * min(b, K.BBG_RV)


def est(x):
    s, u = 0.0, 0.0
    for g, p in zip(STUFEN + [float("inf")], SAETZE):
        if x > u:
            s += (min(x, g) - u) * p / 100
        u = g
    return s


def neu(b, kinder, partner, wg, zu, vs, j):
    DIV, EFF = div_jahr(j), eff_jahr(j)
    brutto = b + wg * ag(b)
    st = est(brutto + DIV) + (est(DIV) if partner else 0.0)
    div = DIV * (2 if partner else 1) + kinder * DIV / 2
    netto = brutto - st + div
    konsum = kq(netto) * netto
    mwst_mehr = konsum * ((1 + EFF / 100) / (1 + EFF_ALT / 100) - 1)
    mwst_bezahlt = konsum * EFF / (100 + EFF)
    return netto - mwst_mehr - zu / 100 * (st + mwst_bezahlt) - (vs * K.AN_RV_AV / BASIS[1] * min(b, K.BBG_RV) if vs > 0.15 else vs * b)


def heute(b, kinder, partner):
    return K.netto_heute(b, kinder, partner)["netto"]


def rentner(r_monat, zu, j):
    r = 12 * r_monat
    kvpv = P["rentner_kv_pv"] * r
    zve = max(0.0, P["besteuerungsanteil"] * r - kvpv - 102 - K.SA_PAUSCH)
    h = r - kvpv - K.est_2026(zve) - K.soli_2026(K.est_2026(zve))
    EFF = eff_jahr(j)
    r = r * (1 - P.get("rente_kuerzung", 0.0))         # v3.48: Rente um die eingesparten Beiträge gekürzt
    st = est(r)                                        # Dividende + Altrente zusammen r, ganz steuerpflichtig
    konsum = kq(r - st) * (r - st)
    n = r - st - konsum * ((1 + EFF / 100) / (1 + EFF_ALT / 100) - 1) - zu / 100 * (st + konsum * EFF / (100 + EFF))
    # v4.11 B1: Grundauskommen auch für Bestandsrenten (volle Anrechnung); heute zum Vergleich Grundsicherung im Alter (Regelbedarf + KdU)
    g = P.get("grundauskommen_rentner")
    if g:
        h, n = max(h, 12 * g["heute_monat"]), max(n, 12 * g["neu_monat"])
    return round(h), round(n)


def main():
    faelle = [("alleinstehend", 0, False), ("alleinerziehend, 1 Kind", 1, False), ("Paar, ein Einkommen, 2 Kinder", 2, True)]
    kombi = list(itertools.product(P["jahre"], P["weitergabe_ag"], P["zuschlag_pct"], P["vorsorge_satz"]))
    erg, anteil = [], {}
    for j, wg, zu, vs in kombi:
        setze_jahr(j)
        for name, ki, pa in faelle:
            zeilen = []
            for b in P["bruttoeinkommen"]:
                h, n = heute(b, ki, pa), neu(b, ki, pa, wg, zu, vs, j)
                db, dak = 1000, 1000 + ag(b + 1000) - ag(b)
                gh = 1 - (heute(b + db, ki, pa) - h) / dak
                gn = 1 - (neu(b + db, ki, pa, wg, zu, 0, j) - neu(b, ki, pa, wg, zu, 0, j)) / dak
                zeilen.append(dict(brutto=b, netto_heute=round(h), netto_33=round(n), differenz=round(n - h),
                                   differenz_monat=round((n - h) / 12), grenzbelastung_heute=round(gh * 100, 1),
                                   grenzbelastung_33=round(gn * 100, 1)))
            erg.append(dict(jahr=j, haushalt=name, weitergabe_ag=wg, zuschlag_pct=zu, vorsorge_satz=vs, zeilen=zeilen))
        tot = sum(w for w, _ in K.VERT)
        plus = sum(w for w, b in K.VERT if neu(b, 0, False, wg, zu, vs, j) > heute(b, 0, False))
        anteil[f"{j}|weitergabe {wg}|zuschlag {zu}|vorsorge {vs}"] = round(plus / tot * 100)
    # Raster für den Rechner der Webseite (Entwurf): Brutto 10.000 bis 150.000 € in 1.000-€-Schritten, Euro im Monat
    raster = dict(brutto=list(range(10000, 150001, 1000)), heute={}, neu={}, grenz_heute=[], grenz_neu={})
    for j in P["jahre"]:
        setze_jahr(j)
        for name, ki, pa in faelle:
            raster["heute"][f"{j}|{name}"] = [round(heute(b, ki, pa) / 12) for b in raster["brutto"]]
            for wg, zu, vs in itertools.product(P["weitergabe_ag"], P["zuschlag_pct"], P["vorsorge_satz"]):
                raster["neu"][f"{j}|{name}|{wg}|{zu}|{vs}"] = [round(neu(b, ki, pa, wg, zu, vs, j) / 12) for b in raster["brutto"]]
    setze_jahr(2028)
    gb = list(range(10000, 150001, 2500))
    raster["grenz_brutto"] = gb
    raster["grenz_heute"] = [round(100 * (1 - (heute(b + 500, 0, False) - heute(b, 0, False)) / (500 + ag(b + 500) - ag(b))), 1) for b in gb]
    for wg in P["weitergabe_ag"]:
        raster["grenz_neu"][str(wg)] = [round(100 * (1 - (neu(b + 500, 0, False, wg, 0, 0, 2028) - neu(b, 0, False, wg, 0, 0, 2028))
                                                / (500 + ag(b + 500) - ag(b))), 1) for b in gb]
    # v3.56: Rechner der Webseite (Zeitstrahl 2028–2060, 1–3 Erwachsene, 0–3 Kinder). „Heute" hängt nur vom Beitragsregime ab (bis 2034
    # Recht 2026, ab 2035 IGES-Sätze, danach gleich gehalten: Annahme); das Neue rechnet die Seite mit denselben Formeln wie neu() nach,
    # mit Dividende und effektivem Labelsatz des Jahres. Dritter Erwachsener ohne Einkommen: heute wie Paar, neu eigene Dividende (Annahme).
    rr = dict(brutto=raster["brutto"], heute={}, beitrag={}, jahre=[], div=[], eff=[], bbg_kv=K.BBG_KV, bbg_rv=K.BBG_RV,
              stufen=STUFEN, saetze=SAETZE, eff_alt=EFF_ALT, weitergabe=min(P["weitergabe_ag"]), zuschlag=max(P["zuschlag_pct"]),
              vorsorge=min(P["vorsorge_satz"]), kq=[[12500, .95], [37500, .85], [65000, .75], [100000, .60]])
    for reg in (2028, 2035):
        setze_jahr(reg)
        rr["beitrag"][str(reg)] = [K.AN_KV_PV, K.AN_RV_AV]
        for e in (1, 2, 3):
            for ki in range(4):
                rr["heute"][f"{reg}|{e}|{ki}"] = [round(heute(b, ki, e > 1)) for b in raster["brutto"]]
    for j in sorted(JAHR):
        rr["jahre"].append(j); rr["div"].append(JAHR[j]["dividende_erw_eur2026"]); rr["eff"].append(JAHR[j]["label_effektiv"])
    # Selbstprüfung: die Formel der Seite muss neu() für den Einpersonenhaushalt treffen
    setze_jahr(2028)
    assert abs(neu(42000, 0, False, rr["weitergabe"], rr["zuschlag"], rr["vorsorge"], 2028) - neu(42000, 0, False, 0.8, max(P["zuschlag_pct"]), 0.10, 2028)) < 1e-6
    raster["rechner"] = rr
    # v3.58: Anteil der Beschäftigten mit mehr verfügbarem Einkommen je Haushaltstyp (Lohnverteilung K.VERT, 7 Stützstellen, grob; geltende
    # Regeln: Weitergabe 80 %, Zuschlag 13,7 %, Pflichtvorsorge 10 %). Für die Aussage „9 von 10 Beschäftigten" auf der Webseite.
    tot = sum(w for w, _ in K.VERT)
    for j in P["jahre"]:
        setze_jahr(j)
        for name, ki, pa in faelle:
            anteil[f"beschluss|{j}|{name}"] = round(sum(w for w, b in K.VERT if neu(b, ki, pa, 0.8, max(P["zuschlag_pct"]), 0.10, j)
                                                        > heute(b, ki, pa)) / tot * 100, 1)
    (AGG / "haushalte33_raster.json").write_text(json.dumps(raster, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    setze_jahr(2028)
    rente = [dict(rente_monat=r, zuschlag_pct=zu, netto_heute_monat=round(a / 12), netto_33_monat=round(b / 12), differenz_monat=round((b - a) / 12))
             for r in P["renten_monat"] for zu in P["zuschlag_pct"] for a, b in [rentner(r, zu, 2028)]]
    E = dict(rentner=rente, rentner_hinweis="Rente um die eingesparten Kranken- und Pflegebeiträge gekürzt (Beschluss v3.48), sonst voll weitergezahlt; Besteuerungsanteil 83 % (Annahme)", version=P["version"], system=P["system"], preisbasis="Euro 2026; heute: Recht 2026 (2035: Beitragssätze IGES)",
             dividende_erw_jahr={str(j): div_jahr(j) for j in P["jahre"]}, faelle=erg, anteil_erwachsene_mit_mehr=anteil,
             verteilung="Kernmodell VERT (7 Gruppen Alleinstehender, Annahmen des nationalen Modells)",
             hinweis="grob: Fälle ohne Erwerbseinkommen nicht gerechnet (Härtefall sichert den Grundbedarf); keine Verhaltensänderung")
    (AGG / "haushalte33.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    for e in erg:
        if e["haushalt"] == "alleinstehend":
            print(f"{e['jahr']} | {e['haushalt']} | Weitergabe {e['weitergabe_ag']} | Zuschlag {e['zuschlag_pct']} | Vorsorge {e['vorsorge_satz']}: "
                  + " ".join(f"{z['brutto']//1000}k:{z['differenz_monat']:+}" for z in e["zeilen"]))
    print("Anteil Erwachsene mit mehr Geld:", anteil)
    print("Rentner:", [(x["rente_monat"], x["zuschlag_pct"], x["differenz_monat"]) for x in rente])
    return 0


if __name__ == "__main__":
    sys.exit(main())
