#!/usr/bin/env python3
"""Bedarfsgeprüfte Leistungen heute, Härtefall-Boden neu, Kinderanteil der Dividende und Mindestlohn je Land (Logbuch v4.3). Prüfrechnung.

Auftrag der Initiative (18.10.2026): (1) die Lücke aus v4.2 schließen – heute bedarfsgeprüfte Leistungen, neu den Härtefallfonds zuordnen;
(2) die halbe Kinderdividende am Bedarf prüfen und Vorschläge machen (keine neuen Programme, sondern Parameter und Regeln, die sich selbst
justieren); (3) Wirkung eines Mindestlohns je Land.
Heute (zusätzlich zu heute_laender.py): DE Bürgergeld-Aufstockung (Näherung auch für Wohngeld und Kinderzuschlag), FR APL (grob), ES CAPI;
seit v4.35 auch ES IMV, IT Assegno di Inclusione (nur mit Minderjährigen) und PL zasiłek okresowy (50 % der Lücke, Annahme). Weiter nicht enthalten:
FR RSA (Annahme: von der prime d'activité im Arbeitsbereich weitgehend abgedeckt), PL dodatek mieszkaniowy, regionale Leistungen.
Neu: Kinderdividende s × Erwachsenendividende, finanziert aus demselben Topf (Erwachsenendividende × (1−K/2)/(1−K+sK)); Härtefall-Boden:
verfügbares Einkommen mindestens Grundbedarf × (1 + 0,5 × weitere Erwachsene + 0,45 × Kinder). Mindestlohn: Vollzeit-Mindestlohnhaushalte heute und neu,
dazu eine Regel „Mindestlohn mindestens 50 % des Durchschnittslohns" (Referenzwert der EU-Richtlinie 2022/2041).
Ausgabe: daten/aggregate/sozial_laender.json
"""
import contextlib, importlib.util, io, json, tomllib
from pathlib import Path

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "sozial_laender.toml").read_text(encoding="utf-8"))
P["zuschlag_de"] = round(json.loads((W / "daten" / "aggregate" / "fonds_geltend.json").read_text(encoding="utf-8"))["zuschlag_haushalte"]["laender"]["DE"]["2028"], 1)   # v4.38 (E11): DE 2028 nach Verrechnung   # v4.11; v4.20 geltender Fonds der 30


def lade_modul(name, pfad):
    spec = importlib.util.spec_from_file_location(name, W / pfad)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


HL = lade_modul("hl", "modell/heute_laender.py")
H33 = lade_modul("h33", "modell/haushalte33.py")
H33.setze_jahr(2028)
K = P["anteil_minderjaehrige"]
JAHRE = HL.JAHRE


# ---------------- heute: bedarfsgeprüfte Leistungen
def de_heute_basis(b, e, k):
    return dict(netto=H33.heute(b, k, e >= 2))


def de_buergergeld(b, e, k, netto):
    d = P["de"]
    g = b / 12
    f = d["freibetrag"]
    obere = f[4] if k > 0 else f[3]
    fb = min(g, f[0]) + 0.2 * max(0, min(g, f[1]) - f[0]) + 0.3 * max(0, min(g, f[2]) - f[1]) + 0.1 * max(0, min(g, obere) - f[2])
    bedarf = d["regelbedarf_erw"][min(e, 3) - 1] + k * d["regelbedarf_kind"] + d["kdu"][min(e + k, 7) - 1]
    einkommen = netto / 12 - fb            # Kindergeld ist im Netto enthalten und wird angerechnet
    return 12 * max(0.0, bedarf - einkommen)


def fr_apl(b, e, k, netto):
    d = P["fr"]
    pers = e + k
    skala = 1 + 0.5 * min(pers - 1, 1) + 0.3 * max(pers - 2, 0)
    r0 = d["rsa_niveau"] * skala
    apl = 12 * max(0.0, d["apl_max"][min(pers, 6) - 1] - d["apl_satz"] * max(0.0, netto / 12 - r0))
    if apl > 0 and d.get("forfait_bei_apl", False):
        # v4.51 (Korrektur 78): Wer APL erhält, dem rechnet die CAF den forfait logement als Ressource der prime d'activité an
        pa = HL.F["pa"]
        alt = pa.get("forfait_anteil", 0.0)
        pa["forfait_anteil"] = 1.0
        mit = HL.MODELLE["FR"][0](b, e, k)["netto"]
        pa["forfait_anteil"] = alt
        apl -= max(0.0, netto - mit)
    return apl


def es_capi(b, e, k, netto):
    d = P["es"]
    if k == 0:
        return 0.0
    renta = d["imv_renta"] * (1 + 0.3 * (e + k - 1))
    return 12 * d["capi_kind"] * k if netto <= 3 * renta else 0.0


def it_adi(b, e, k, netto):
    """v4.35: Assegno di Inclusione (Mindestsicherung Italien), nur mit Minderjährigen (Haushalte dieser Rechnung ohne Personen ab 60)."""
    d = P["it"]
    if k == 0:
        return 0.0
    au = netto - HL.MODELLE["IT"][0](b, e, 0)["netto"]                       # Assegno unico (nicht angerechnet)
    eigen = max(0.0, netto - au - min(b, d["adi_freibetrag_erwerb"]))
    isee = (netto - au) / HL.P["it"]["scala_isee"][min(e + k - 1, len(HL.P["it"]["scala_isee"]) - 1)]
    if isee > d["adi_isee_max"]:
        return 0.0
    skala = 1 + sum(d["adi_skala_kind"][min(i, 2)] for i in range(k))
    schwelle = d["adi_basis"] * skala
    if eigen >= schwelle:                                                  # Einkommen über der Schwelle: kein Anspruch, auch kein Mietzuschuss
        return 0.0
    return schwelle - eigen + d["adi_miete"]


def es_imv_capi(b, e, k, netto):
    """v4.35: Ingreso Mínimo Vital (Garantie minus Einkommen) und Kinderzuschlag CAPI."""
    d, m = P["es"], P["es_imv"]
    garantie = d["imv_renta"] * min(m["skala_max"], 1 + m["skala_weitere"] * (e + k - 1))
    return max(0.0, garantie - netto) + es_capi(b, e, k, netto)


def pl_zasilek(b, e, k, netto):
    """v4.35: Zasiłek okresowy (50 % der Lücke zum Einkommenskriterium), 800+ nicht angerechnet, Beträge in zł."""
    d = P["pl"]
    pers = e + k
    kriterium = 12 * (d["kryterium_samotna"] if pers == 1 else d["kryterium_rodzina"] * pers)
    einkommen = netto - k * HL.P["pl"]["swiadczenie_800"]
    return d["anteil"] * max(0.0, kriterium - einkommen)


ZUSATZ = {"DE": de_buergergeld, "FR": fr_apl, "ES": es_imv_capi, "IT": it_adi, "PL": pl_zasilek}   # v4.35: IT, PL, ES-IMV ergänzt


def heute(c, b, e, k, mit_bedarf=True):
    n = de_heute_basis(b, e, k)["netto"] if c == "DE" else HL.MODELLE[c][0](b, e, k)["netto"]
    z = ZUSATZ[c](b, e, k, n) if (mit_bedarf and c in ZUSATZ) else 0.0
    return n + z


def ag(c, b):
    return H33.ag(b) if c == "DE" else HL.ag_weitergabe(c, b)   # v4.36: einheitlicher Deckel (DE in haushalte33.ag)


# ---------------- neu: Kinderanteil, Boden
def neu(c, b, e, k, j=2028, s=0.5, boden=True, lohn_faktor=1.0, vorsorge_frei=False):
    st_c = HL.LS["staaten"][c]
    fx = HL.faktor(c)
    topf = (1 - K / 2) / (1 - K + s * K)
    DIV = st_c["dividende_erw_eur"][JAHRE.index(j)] * 12 * fx * topf
    EFF = HL.EFF_NEU[j]
    est = lambda x: HL.stufen(x, [g * fx for g in st_c["tarif_stufen"]], [0.0, 11.0, 19.0, 25.0, 33.0])
    lohn = b * lohn_faktor
    brutto = lohn + HL.P["weitergabe"] * ag(c, b)       # Weitergabe bemisst sich an den heutigen Arbeitgeberbeiträgen
    st = est(brutto + DIV) + (e - 1) * est(DIV)
    netto = brutto - st + DIV * e + k * DIV * s
    konsum = HL.kq(netto, c) * netto
    zu = (P["zuschlag_de"] if c == "DE" else st_c["fonds"]["zuschlag_pct"]) * HL.zu_faktor(c, j)   # v4.38 (E11)
    fm, fb = HL.mwst_phi(c, netto)                                                      # v4.29
    netto = netto - fm * konsum * ((1 + EFF / 100) / (1 + HL.eff_alt(c) / 100) - 1) - zu / 100 * (st + fb * konsum * EFF / (100 + EFF))
    gbj = st_c["grundbedarf_jahr_eur"] * fx
    netto -= HL.P["vorsorge"] * (max(0.0, lohn - gbj) if vorsorge_frei else lohn)   # Variante: Pflichtvorsorge erst über dem Grundbedarf
    if boden:
        gb = st_c["grundbedarf_jahr_eur"] * fx
        netto = max(netto, gb * (1 + P["boden"]["skala_erwachsen"] * (e - 1) + P["boden"]["skala_kind"] * k))
    return netto


# ---------------- Auswertung
LAENDER = ["DE", "FR", "IT", "ES", "PL"]
HAUSHALTE = (("alleinstehend", 1, 0), ("alleinerziehend, 1 Kind", 1, 1), ("Paar, ein Einkommen, 2 Kinder", 2, 2))


def verteilung(c):
    aw = HL.P["oecd"]["durchschnittslohn"][c]
    return [(w, b * aw / HL.P["oecd"]["durchschnittslohn"]["DE"]) for w, b in HL.VERT_DE]


def anteile(c, **kw):
    v = verteilung(c)
    tot = sum(w for w, _ in v)
    mb = kw.pop("mit_bedarf", True)
    return {n: round(sum(w for w, b in v if neu(c, b, e, k, **kw) > heute(c, b, e, k, mb)) / tot * 100) for n, e, k in HAUSHALTE}


def faelle(c, **kw):
    mb = kw.pop("mit_bedarf", True)
    aw = HL.P["oecd"]["durchschnittslohn"][c]
    out = {}
    for f in (0.33, 0.5, 0.66, 1.0):
        b = round(f * aw, -2)
        out[f"{f}"] = {n: round((neu(c, b, e, k, **kw) - heute(c, b, e, k, mb)) / 12) for n, e, k in HAUSHALTE}
    return out


def ohne_vorsorge(f):
    """Pflichtvorsorge als eigenes Vermögen statt als Abzug (sie bleibt Eigentum der Beschäftigten)."""
    alt = HL.P["vorsorge"]
    HL.P["vorsorge"] = 0.0
    try:
        return f()
    finally:
        HL.P["vorsorge"] = alt


def mindestlohn(c):
    if c not in P["mindestlohn"]["monat_2026"]:
        return dict(hinweis="kein gesetzlicher Mindestlohn")
    m = P["mindestlohn"]
    jahr = m["monat_2026"][c] * 12
    aw26 = HL.P["oecd"]["durchschnittslohn"][c] * m["lohnwachstum_2024_2026"][c]
    kaitz = jahr / aw26
    faktor = max(1.0, m["ziel_anteil_durchschnitt"] / kaitz)
    r = dict(mindestlohn_jahr=jahr, anteil_durchschnitt_2026=round(100 * kaitz, 1),
             kaitz_2024_durchschnitt=round(100 * m["monat_2024"][c] * 12 / HL.P["oecd"]["durchschnittslohn"][c], 1),
             faktor_regel_50=round(faktor, 3), ag_heute_pct=round(100 * ag(c, jahr) / jahr, 1))
    for n, e, k in HAUSHALTE:
        h = heute(c, jahr, e, k)
        r[n] = dict(heute_monat=round(h / 12), neu_monat=round(neu(c, jahr, e, k, s=0.7) / 12),
                    neu_regel50_monat=round(neu(c, jahr, e, k, s=0.7, lohn_faktor=faktor) / 12),
                    lohnkosten_regel50_pct=round(100 * (jahr * faktor - jahr - ag(c, jahr)) / (jahr + ag(c, jahr)), 1))
    return r


def kinder():
    d = P["bedarf_kind"]
    rb = d["regelbedarf"]
    mittel = (rb["kind_0_5"] * 6 + rb["kind_6_13"] * 8 + rb["kind_14_17"] * 4) / 18
    out = dict(existenzminimum_saechlich=round(d["existenzminimum_kind_saechlich"] / d["existenzminimum_erwachsen"], 2),
               existenzminimum_mit_bea=round(d["existenzminimum_kind_gesamt"] / d["existenzminimum_erwachsen"], 2),
               regelbedarf_mittel=round(mittel / rb["erwachsen"], 2), regelbedarf_je_alter=[round(rb[x] / rb["erwachsen"], 2) for x in ("kind_0_5", "kind_6_13", "kind_14_17")],
               oecd_skala_gegen_erwachsenenmittel=[round(0.3 / 0.75, 2), round(0.5 / 0.75, 2)],
               heute_kindergeld_de_gegen_dividende=round(d["kindergeld_de"] / HL.LS["staaten"]["DE"]["dividende_erw_eur"][0], 2))
    var = {}
    for s in P["kinder_anteile"]:
        topf = (1 - K / 2) / (1 - K + s * K)
        var[str(s)] = {c: dict(erwachsen=round(HL.LS["staaten"][c]["dividende_erw_eur"][0] * topf * HL.faktor(c)),
                               kind=round(HL.LS["staaten"][c]["dividende_erw_eur"][0] * topf * s * HL.faktor(c))) for c in LAENDER}
    out["varianten_2028"] = var
    return out


def main():
    erg = dict(kinderbedarf=kinder(), staaten={})
    for c in LAENDER:
        x = dict(
            anteil_v41=anteile(c, boden=False, mit_bedarf=False),
            anteil_mit_bedarf_ohne_boden=anteile(c, boden=False),
            anteil_mit_bedarf_und_boden=anteile(c),
            anteil_kind_0_7=anteile(c, s=0.7),
            anteil_kind_1_0=anteile(c, s=1.0),
            anteil_paket=anteile(c, s=0.7, vorsorge_frei=True),
            faelle_paket=faelle(c, s=0.7, vorsorge_frei=True),
            anteil_paket_vorsorge_als_vermoegen=ohne_vorsorge(lambda: anteile(c, s=0.7)),
            faelle_kind_0_5=faelle(c),
            faelle_kind_0_7=faelle(c, s=0.7),
            mindestlohn=mindestlohn(c))
        erg["staaten"][c] = x
    E = dict(version=P["version"], status="Prüfrechnung", **erg,
             hinweis="Monatsbeträge in Landeswährung (PL: Zł), 2028, Kaufkraft 2026. Anteile: Beschäftigte mit mehr verfügbarem Einkommen, deutsche Lohnverteilung skaliert (grob).")
    (AGG / "sozial_laender.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Kinderbedarf:", json.dumps({k: v for k, v in erg["kinderbedarf"].items() if k != "varianten_2028"}, ensure_ascii=False))
    for s, v in erg["kinderbedarf"]["varianten_2028"].items():
        print(f"  s={s}:", v)
    for c, x in erg["staaten"].items():
        print(c)
        for k in ("anteil_v41", "anteil_mit_bedarf_ohne_boden", "anteil_mit_bedarf_und_boden", "anteil_kind_0_7", "anteil_kind_1_0", "anteil_paket", "anteil_paket_vorsorge_als_vermoegen"):
            print(f"   {k:<32}", x[k])
        print("   Fälle s=0,5:", x["faelle_kind_0_5"])
        print("   Fälle s=0,7:", x["faelle_kind_0_7"])
        print("   Fälle Paket:", x["faelle_paket"])
        print("   Mindestlohn:", x["mindestlohn"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
