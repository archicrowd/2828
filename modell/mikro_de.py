#!/usr/bin/env python3
"""Synthetische Mikrosimulation Deutschland, Stufe 1 (Logbuch v4.22). Prüfrechnung.

Ziel: Anteil mit mehr verfügbarem Einkommen (Stand C, 2028, Kaufkraft 2026) nicht nur für drei Beispielhaushalte, sondern für eine
auf veröffentlichte Verteilungen geeichte Gesamtbevölkerung: Vollzeit, Teilzeit, Minijob, Bürgergeld, Familien, Rentner.
Keine Mikrodaten: Die Datensätze werden gezogen (fester Startwert) und mit Raking (Deville/Särndal, exponentiell) auf Eckwerte geeicht.

Aufbau
  1. Haushalte erwerbsfähigen Alters (allein, alleinerziehend, Paar ohne / mit minderjährigen Kindern, ggf. ein volljähriges Kind),
     Erwerbsstatus je Erwachsenem (Vollzeit, Teilzeit, Minijob, ohne Erwerb), Löhne aus den amtlichen Verteilungen (mikro_de.toml).
     Partnerlöhne über eine Gauß-Copula mit Rangkorrelation rho.
  2. Rentnerhaushalte (allein, Paar), Renten lognormal auf Mittel und Anteil unter 1.000 € geeicht.
  3. Eichung auf: Haushalte je Typ, Bedarfsgemeinschaften ohne Erwerb, Vollzeit-, Teilzeit-, Minijob-Personen, Kinder unter 18 und volljährig.
  4. Validierung an NICHT geeichten Aggregaten 2025: Bruttolohnsumme (D11), Lohnsteuer + Kindergeld (kassenmäßig), Soli.
  5. heute (Recht 2026, sozial_laender / Kernmodell, Paare mit Splitting beider Einkommen, Midijob-Übergangsbereich genähert)
     gegen neu (regel_boden: 33R, Dividende, Grundauskommen mit Halbanrechnung, Pflichtvorsorge; Rentner: rentnerausgleich).
  Szenarien: Weitergabe 0 / 50 / 80 / 100 %, Partnerkorrelation 0 / 0,3 / 0,5, Haushaltsanteile ±15 %, fünf Ziehungen.

Gegenprobe: Für Haushalte mit einem Einkommen über dem Midijob-Bereich muss die Rechnung regel_boden.neu und sozial_laender.heute treffen.
Ausgabe: daten/aggregate/mikro_de.json
"""
import contextlib
import importlib.util
import io
import json
import math
import tomllib
from pathlib import Path

import numpy as np
from scipy.stats import norm

W = Path(__file__).resolve().parent.parent
AGG = W / "daten" / "aggregate"
P = tomllib.loads((W / "modell" / "mikro_de.toml").read_text(encoding="utf-8"))


def lade(name, pfad):
    spec = importlib.util.spec_from_file_location(name, W / pfad)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


RB = lade("rb", "modell/regel_boden.py")
RA = lade("ra", "modell/rentnerausgleich.py")
SL, HL = RB.SL, RB.SL.HL
H33, K = SL.H33, SL.H33.K
DE = HL.LS["staaten"]["DE"]
J = 2028
DIV = DE["dividende_erw_eur"][SL.JAHRE.index(J)] * 12 * RB.topf(RB.S)
EFF = HL.EFF_NEU[J]
ZU = SL.P["zuschlag_de"]
GB = DE["grundbedarf_jahr_eur"]
MINI = P["minijob"]["grenze_monat_2026"] * 12
MIDI_OBEN = 2000 * 12                      # Übergangsbereich 2026 bis 2.000 €/Monat (Annahme: AN-Beitrag linear von 0 auf voll)


def est_neu(x):
    return HL.stufen(x, DE["tarif_stufen"], [0.0, 11.0, 19.0, 25.0, 33.0])


# ------------------------------------------------------------------ heute (Recht 2026)
def sv_an(b, art, kinderlos, midijob=True):
    if art == "mini" or b <= 0:
        return 0.0
    v = K.sv_heute(b, kinderlos)
    if midijob and b < MIDI_OBEN:
        v *= max(0.0, (b - MINI) / (MIDI_OBEN - MINI))
    return v


def heute(hh, midijob=True):
    """hh: dict(erw=[(lohn, art)], kind=minderjährige, vkind=(lohn, art) oder None, paar=bool)."""
    kinderlos = hh["kind"] == 0 and hh["vkind"] is None
    sv = [sv_an(b, a, kinderlos, midijob) for b, a in hh["erw"]]
    zve = [max(0.0, b - s - K.WK_PAUSCH * (b > 0)) if a != "mini" else 0.0 for (b, a), s in zip(hh["erw"], sv)]
    if hh["paar"]:
        z = max(0.0, sum(zve) - 2 * K.SA_PAUSCH)
        est = 2 * K.est_2026(z / 2)
        st = est + K.soli_2026(est, True)
    else:
        z = max(0.0, zve[0] - K.SA_PAUSCH)
        est = K.est_2026(z)
        st = est + K.soli_2026(est)
    brutto = sum(b for b, _ in hh["erw"])
    netto = brutto - sum(sv) - st
    n_kg = hh["kind"]
    if hh["vkind"]:
        b, a = hh["vkind"]
        s = sv_an(b, a, False, midijob)
        e2 = K.est_2026(max(0.0, b - s - K.WK_PAUSCH * (b > 0) - K.SA_PAUSCH)) if a != "mini" else 0.0
        netto += b - s - e2
        brutto += b
        st += e2
        n_kg += 1
    netto += n_kg * K.KINDERGELD * 12
    e = len(hh["erw"]) + (1 if hh["vkind"] else 0)
    bg = SL.de_buergergeld(brutto, min(e, 3), hh["kind"], netto)
    return netto + bg, dict(lohnsteuer=est, soli=st - est, sv=sum(sv), kindergeld=n_kg * K.KINDERGELD * 12, buergergeld=bg)


# ------------------------------------------------------------------ neu (Stand C, regel_boden)
def neu(hh, w):
    loehne = [b for b, _ in hh["erw"]] + ([hh["vkind"][0]] if hh["vkind"] else [])
    e, k = len(loehne), hh["kind"]
    brutto = [b + w * H33.ag(b) for b in loehne]
    st = sum(est_neu(x + DIV) for x in brutto)
    netto = sum(brutto) - st + DIV * e + k * DIV * RB.S
    konsum = HL.kq(netto, "DE") * netto
    netto = netto - konsum * ((1 + EFF / 100) / (1 + HL.eff_alt("DE") / 100) - 1) - ZU / 100 * (st + konsum * EFF / (100 + EFF))
    dv = DIV * (e + RB.S * k)
    auf = max(0.0, RB.boden("DE", e, k) - dv - RB.P["anrechnung"] * max(0.0, netto - dv))
    return netto + auf - HL.P["vorsorge"] * sum(loehne), auf


def rentner_heute_neu(r_monate):
    """Je Person (Paare: zwei Renten, Boden je Person – Annahme). Rückgabe: heute, neu, Aufstockung neu, Grundsicherung heute, Fälle heute."""
    h = sum(RA.heute(r) for r in r_monate)
    gs = [RA.heute(r) - RA.heute_ohne_gs(r) for r in r_monate]
    n = sum(RA.neu(r) for r in r_monate)
    g = RA.H.P["grundauskommen_rentner"]
    RA.H.P["grundauskommen_rentner"] = None
    try:
        ohne = sum(RA.neu(r) for r in r_monate)
    finally:
        RA.H.P["grundauskommen_rentner"] = g
    return h, n, n - ohne, sum(gs), sum(x > 0 for x in gs)


def gegenprobe():
    """Einverdienerhaushalte über dem Midijob-Bereich: identisch mit regel_boden.neu / sozial_laender.heute."""
    alt = HL.P["weitergabe"]
    abw = 0.0
    for b in (30000, 42000, 60000, 90000):
        for e, k in ((1, 0), (1, 1), (2, 2)):
            hh = dict(erw=[(b, "vz")] + ([(0.0, "ohne")] if e == 2 else []), kind=k, vkind=None, paar=e == 2)
            abw = max(abw, abs(heute(hh, midijob=False)[0] - SL.heute("DE", b, e, k)), abs(neu(hh, alt)[0] - RB.neu("DE", b, e, k)))
    assert abw < 1.0, f"Gegenprobe verfehlt: {abw:.2f} €"
    return round(abw, 3)


# ------------------------------------------------------------------ Verteilungen
def _vz_stuetz():
    v = P["vollzeit"]
    pk = sorted((int(p) / 100, x) for p, x in v["perzentile"].items())
    return v, [(0.0, v["untergrenze"])] + [x for x in pk if x[0] <= 0.9], pk[-2][1], pk[-1][1]


def _vz_ohne_spitze(u):
    """Bis P90 linear zwischen den Dezilen, P90–P99 Pareto-Interpolation (log-linear in 1 − u)."""
    v, xs, p90, p99 = _vz_stuetz()
    a90 = math.log(10) / math.log(p99 / p90)
    out = np.interp(u, [a for a, _ in xs], [b for _, b in xs])
    m = (u > 0.9) & (u <= 0.99)
    out[m] = p90 * ((1 - u[m]) / 0.1) ** (-1 / a90)
    return out


def vz_quantil(u):
    v, _, _, p99 = _vz_stuetz()
    out = _vz_ohne_spitze(u)
    oben = u > 0.99                     # Pareto-Spitze über P99, Alpha so, dass das Mittel getroffen wird (Abschneidung bei obergrenze)
    out[oben] = np.minimum(p99 * ((1 - u[oben]) / 0.01) ** (-1 / vz_alpha()), v["obergrenze"])
    return out


_ALPHA = {}


def vz_alpha():
    if "a" not in _ALPHA:
        v, _, _, p99 = _vz_stuetz()
        g = (np.arange(198000) + 0.5) / 200000                     # Mittelpunkte 0 … 0,99
        unten = _vz_ohne_spitze(g).mean() * 0.99
        t = (np.arange(20000) + 0.5) / 20000
        lo, hi = 1.05, 8.0
        for _ in range(60):
            a = (lo + hi) / 2
            spitze = np.minimum(p99 * t ** (-1 / a), v["obergrenze"]).mean() * 0.01
            lo, hi = (a, hi) if unten + spitze > v["mittel"] else (lo, a)
        _ALPHA["a"] = (lo + hi) / 2
        assert 1.1 < _ALPHA["a"] < 7.9, "Pareto-Spitze nicht lösbar"
    return _ALPHA["a"]


def tz_quantil(u):
    t = P["teilzeit"]
    m = t["monat_april_2025"] * 12 * (1 + t["sonderzahlung"]) / P["lohn_2024_2025"]       # auf 2024 zurückgerechnet
    s = t["streuung_log"]
    x = np.exp(math.log(m) - s * s / 2 + s * norm.ppf(np.clip(u, 1e-6, 1 - 1e-6)))
    return np.maximum(x, t["untergrenze_monat"] * 12 / P["lohn_2024_2025"])


def mini_quantil(u):
    a, b = P["minijob"]["verdienst_monat"]
    return (a + (b - a) * u) * 12 / P["lohn_2024_2025"]


def rente_parameter():
    r = P["rentner"]
    z = norm.ppf(r["anteil_unter_1000"])
    m = math.log(r["zahlbetrag_mittel_2024"])
    s = -z + math.sqrt(z * z + 2 * (m - math.log(1000)))          # s²/2 − z·s − (m − ln 1000) = 0
    return m - s * s / 2, s


# ------------------------------------------------------------------ Population
TYPEN = ("allein", "alleinerziehend", "paar_ohne", "paar_mit")
# Ausgangswahrscheinlichkeiten Erwerbsstatus (vz, tz, mini, ohne) für Haushalte mit Erwerb – Annahme, wird geeicht
STATUS_P = {"allein": [(0.68, 0.20, 0.07, 0.05)], "alleinerziehend": [(0.40, 0.48, 0.08, 0.04)],
            "paar_ohne": [(0.80, 0.12, 0.04, 0.04), (0.55, 0.25, 0.07, 0.13)], "paar_mit": [(0.86, 0.08, 0.03, 0.03), (0.28, 0.45, 0.10, 0.17)]}
VKIND_P = (0.35, 0.10, 0.20, 0.35)          # volljähriges Kind: Ausbildung/Vollzeit, Teilzeit, Minijob, ohne (Annahme)
AZUBI = 13000                               # Ausbildungsvergütung 2024 (Annahme)
ARTEN = ("vz", "tz", "mini", "ohne")


def ziehe(seed, rho, struktur=1.0):
    rng = np.random.default_rng(seed)
    H = P["haushalte"]
    n = P["haushalte_stichprobe"]
    soll_typ = {"allein": H["allein_mio"] * struktur, "alleinerziehend": H["alleinerziehend_mio"],
                "paar_ohne": H["paar_ohne_minderj_mio"] - (struktur - 1) * H["allein_mio"] / 2,
                "paar_mit": H["paar_mit_minderj_mio"] - (struktur - 1) * H["allein_mio"] / 2}
    tot = sum(soll_typ.values())
    typ = rng.choice(len(TYPEN), size=n, p=[soll_typ[t] / tot for t in TYPEN])
    kz = np.array([1, 2, 3, 4])
    kinder = np.where(np.isin(typ, [1, 3]), rng.choice(kz, size=n, p=H["kinderzahl_anteile"]), 0)
    # Bürgergeld ohne Erwerb: Wahrscheinlichkeit je Typ aus der Zahl der Bedarfsgemeinschaften
    B = P["buergergeld"]
    gr = {"allein": 1, "alleinerziehend": 1 + 1.70, "paar_ohne": 2, "paar_mit": 2 + 1.70}
    a = dict(B["anteile"])
    a["paar_ohne"] += 1 - sum(a.values())
    bg_hh = B["personen_mio"] / sum(a[t] * gr[t] for t in TYPEN)
    soll_bg = {t: bg_hh * a[t] * B["anteil_ohne_erwerb"] for t in TYPEN}
    p_bg = np.array([soll_bg[TYPEN[t]] / soll_typ[TYPEN[t]] for t in typ])
    bg = rng.random(n) < p_bg
    # volljähriges Kind
    vk_mio = H["kinder_volljaehrig_mio"]
    q = H["anteil_volljaehrige_kinder_bei_paaren"]
    p_vk = np.select([typ == 1, np.isin(typ, [2, 3])], [(1 - q) * vk_mio / soll_typ["alleinerziehend"],
                     q * vk_mio / (soll_typ["paar_ohne"] + soll_typ["paar_mit"])], 0.0)
    vkind = rng.random(n) < p_vk
    # Status und Löhne
    z1 = rng.standard_normal(n)
    z2 = rho * z1 + math.sqrt(1 - rho * rho) * rng.standard_normal(n)
    u = [norm.cdf(z1), norm.cdf(z2)]
    haushalte = []
    for i in range(n):
        t = TYPEN[typ[i]]
        erw = []
        for p_idx, probs in enumerate(STATUS_P[t]):
            art = "ohne" if bg[i] else ARTEN[rng.choice(4, p=probs)]
            if not bg[i] and p_idx == 0 and art == "ohne":
                art = "tz"                                                   # Haushalt mit Erwerb: Hauptperson erwerbstätig
            ui = np.array([u[p_idx][i]])
            lohn = {"vz": vz_quantil, "tz": tz_quantil, "mini": mini_quantil}.get(art)
            erw.append((float(lohn(ui)[0]) if lohn else 0.0, art))
        vk = None
        if vkind[i]:
            art = ARTEN[rng.choice(4, p=VKIND_P)]
            lohn = {"vz": AZUBI, "tz": float(tz_quantil(rng.random(1))[0]) * 0.6, "mini": float(mini_quantil(rng.random(1))[0]), "ohne": 0.0}[art]
            vk = (lohn, art)
        haushalte.append(dict(typ=t, erw=erw, kind=int(kinder[i]), vkind=vk, paar=t.startswith("paar"), bg=bool(bg[i])))
    # Rentner
    R = P["rentner"]
    mu, s = rente_parameter()
    nr = P["rentner_stichprobe"]
    allein_r = rng.random(nr) < R["allein_lebend_mio"] / (R["allein_lebend_mio"] + (R["personen_mio"] - R["allein_lebend_mio"]) / 2)
    zr1 = rng.standard_normal(nr)
    zr2 = 0.3 * zr1 + math.sqrt(1 - 0.09) * rng.standard_normal(nr)
    brutto = lambda z: np.exp(mu + s * z) / (1 - RA.H.P["rentner_kv_pv"])          # Zahlbetrag → Brutto
    rentner = [dict(typ="rentner_allein" if allein_r[i] else "rentner_paar",
                    renten=[float(brutto(zr1[i]))] + ([] if allein_r[i] else [float(brutto(zr2[i]))])) for i in range(nr)]
    return haushalte, rentner, soll_typ, soll_bg


def eiche(haushalte, rentner, soll_typ, soll_bg):
    """Exponentielles Raking: w = d · exp(X λ), Newton-Verfahren. Rentner getrennt (nur Personen und Alleinlebende)."""
    Bz = P["beschaeftigte"]
    H = P["haushalte"]
    mini_unter65 = Bz["minijob_ausschliesslich_mio"] * (1 - P["minijob"]["anteil_65plus"])
    spalten = [f"typ_{t}" for t in TYPEN] + ["bg", "vz", "tz", "mini", "kind", "vkind"]
    soll = np.array([soll_typ[t] for t in TYPEN] + [sum(soll_bg.values()), Bz["vollzeit_mio"], Bz["teilzeit_mio"], mini_unter65,
                     H["kinder_minderj_mio"], H["kinder_volljaehrig_mio"]]) * 1e6
    X = np.zeros((len(haushalte), len(spalten)))
    for i, h in enumerate(haushalte):
        X[i, TYPEN.index(h["typ"])] = 1
        X[i, 4] = h["bg"]
        arten = [a for _, a in h["erw"]] + ([h["vkind"][1]] if h["vkind"] else [])
        X[i, 5], X[i, 6], X[i, 7] = arten.count("vz"), arten.count("tz"), arten.count("mini")
        X[i, 8], X[i, 9] = h["kind"], h["vkind"] is not None
    d = np.full(len(haushalte), sum(soll_typ.values()) * 1e6 / len(haushalte))
    lam = np.zeros(len(spalten))
    for _ in range(100):
        w = d * np.exp(X @ lam)
        r = soll - X.T @ w
        if np.max(np.abs(r) / soll) < 1e-9:
            break
        lam += np.linalg.solve((X * w[:, None]).T @ X, r)
    w = d * np.exp(X @ lam)
    # Rentner: Haushaltsgewichte so, dass Personen und Alleinlebende getroffen werden
    R = P["rentner"]
    na = sum(r["typ"] == "rentner_allein" for r in rentner)
    npa = len(rentner) - na
    wr = np.array([R["allein_lebend_mio"] * 1e6 / na if r["typ"] == "rentner_allein" else (R["personen_mio"] - R["allein_lebend_mio"]) * 1e6 / 2 / npa
                   for r in rentner])
    spanne = dict(gewicht_min_max=[round(float((w / d).min()), 3), round(float((w / d).max()), 3)], restfehler_max=float(np.max(np.abs(soll - X.T @ w) / soll)))
    return w, wr, spanne


# ------------------------------------------------------------------ Validierung 2025
def validierung(haushalte, w):
    V = P["validierung"]
    f = P["lohn_2024_2025"]
    lohnsumme, lst, soli, kg, n_bg_pos, n_aufstocker = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    for h, wi in zip(haushalte, w):
        hh = skaliere(h, f)
        _, d = heute(hh)
        lohnsumme += wi * sum(b for b, _ in hh["erw"]) + wi * (hh["vkind"][0] if hh["vkind"] else 0)
        lst += wi * d["lohnsteuer"]
        soli += wi * d["soli"]
        kg += wi * d["kindergeld"]
        if d["buergergeld"] > 0:
            n_bg_pos += wi
            if not h["bg"]:
                n_aufstocker += wi
    # Ergänzungen außerhalb der Population (Annahmen): Minijobs im Nebenjob, Beamte
    neben = 3.52e6 * float(np.mean(mini_quantil(np.linspace(0, 1, 101)))) * f
    beamte = V["beamte_mio"] * 1e6 * V["beamte_brutto"]
    lst_beamte = V["beamte_mio"] * 1e6 * K.est_2026(0.85 * V["beamte_brutto"] - K.WK_PAUSCH)
    mrd = lambda x: round(x / 1e9, 1)
    lst_modell = lst + lst_beamte
    soll_lst = V["lohnsteuer_kasse_mrd"] + V["kindergeld_mrd"]
    return dict(
        bruttolohnsumme=dict(modell_mrd=mrd(lohnsumme + neben + beamte), davon_population=mrd(lohnsumme), nebenjob_minijobs=mrd(neben),
                             beamte_annahme=mrd(beamte), amtlich_d11_mrd=V["bruttoloehne_d11_mrd"],
                             abweichung_pct=round(((lohnsumme + neben + beamte) / 1e9 / V["bruttoloehne_d11_mrd"] - 1) * 100, 1)),
        lohnsteuer=dict(modell_mrd=mrd(lst_modell), davon_beamte_annahme=mrd(lst_beamte), amtlich_lohnsteuer_plus_kindergeld_mrd=round(soll_lst, 1),
                        abweichung_pct=round((lst_modell / 1e9 / soll_lst - 1) * 100, 1),
                        nicht_abgebildet="Lohnsteuer auf Beamtenpensionen und Betriebsrenten, Steuerklasse VI (Nebenjobs), Selbständigenhaushalte mit "
                                         "Beschäftigten, Erstattungen aus der Veranlagung; Tarif 2026 statt 2025 (Grundfreibetrag 12.348 statt 12.096 €)"),
        soli=dict(modell_mrd=mrd(soli), amtlich_mrd=V["soli_mrd"], hinweis="amtlich einschließlich Soli auf Körperschaft- und Kapitalertragsteuer"),
        kindergeld=dict(modell_mrd=mrd(kg), amtlich_mrd=V["kindergeld_mrd"], hinweis="Konsistenzprüfung (Kinderzahl geeicht), Satz 2026 259 €; "
                        "amtlich mit Kindern im Ausland und Nachzahlungen"),
        buergergeld=dict(anspruch_haushalte_mio=round(n_bg_pos / 1e6, 2), davon_mit_erwerb_mio=round(n_aufstocker / 1e6, 2),
                         hinweis="Anspruch bei voller Inanspruchnahme (Bürgergeld als Näherung auch für Wohngeld und Kinderzuschlag); "
                                 "amtlich 2025 rund 3,1 Mio. Bedarfsgemeinschaften (abgeleitet aus 5,6 Mio. Personen, Annahme)"))


def skaliere(h, f):
    return dict(h, erw=[(b * f, a) for b, a in h["erw"]], vkind=(h["vkind"][0] * f, h["vkind"][1]) if h["vkind"] else None)


# ------------------------------------------------------------------ Auswertung
def personen(h):
    return len(h["erw"]) + h["kind"] + (1 if h["vkind"] else 0)


def aequiv(h, y):
    return y / (1 + 0.5 * (len(h["erw"]) + (1 if h["vkind"] else 0) - 1) + 0.3 * h["kind"])


def gruppe_status(h):
    if h["bg"]:
        return "ohne Erwerb (Bürgergeld)"
    a = h["erw"][0][1]
    return {"vz": "Hauptperson Vollzeit", "tz": "Hauptperson Teilzeit", "mini": "Hauptperson Minijob", "ohne": "Hauptperson ohne Erwerb"}[a]


def rechne(haushalte, rentner, w, wr, weitergaben):
    f = P["lohn_2024_2026"]
    zeilen = []
    for h, wi in zip(haushalte, w):
        hh = skaliere(h, f)
        y0, d0 = heute(hh)
        res = {}
        for wg in weitergaben:
            y1, auf = neu(hh, wg)
            res[wg] = (y1, auf)
        zeilen.append(dict(w=wi, p=personen(h), typ=h["typ"], status=gruppe_status(h), tz=any(a == "tz" for _, a in h["erw"]),
                           kinder=h["kind"] > 0, heute=y0, aeq=aequiv(h, y0), neu=res, bg_heute=d0["buergergeld"]))
    for r, wi in zip(rentner, wr):
        rm = [x * f for x in r["renten"]]
        y0, y1, auf, gs, ngs = rentner_heute_neu(rm)
        n = len(rm)
        zeilen.append(dict(w=wi, p=n, typ=r["typ"], status="Rentner", tz=False, kinder=False, heute=y0, aeq=y0 / (1 + 0.5 * (n - 1)),
                           neu={wg: (y1, auf) for wg in weitergaben}, bg_heute=0.0, gs_heute=gs, gs_faelle=ngs))
    return zeilen


def auswerten(zeilen, wg):
    w = np.array([z["w"] for z in zeilen])
    wp = w * np.array([z["p"] for z in zeilen])
    d = np.array([(z["neu"][wg][0] - z["heute"]) / 12 for z in zeilen])
    mehr = d > 0
    aeq = np.array([z["aeq"] for z in zeilen])

    def anteil(mask):
        return dict(anteil_mehr_haushalte_pct=round(float(w[mask & mehr].sum() / w[mask].sum() * 100), 1),
                    anteil_mehr_personen_pct=round(float(wp[mask & mehr].sum() / wp[mask].sum() * 100), 1),
                    mittel_mehr_monat_eur=round(float((w[mask] * d[mask]).sum() / w[mask].sum())),
                    median_mehr_monat_eur=round(float(gew_median(d[mask], w[mask]))),
                    haushalte_mio=round(float(w[mask].sum() / 1e6), 2))
    alle = np.ones(len(zeilen), bool)
    out = dict(gesamt=anteil(alle))
    out["haushaltstyp"] = {t: anteil(np.array([z["typ"] == t for z in zeilen])) for t in TYPEN + ("rentner_allein", "rentner_paar")}
    out["status"] = {s: anteil(np.array([z["status"] == s for z in zeilen])) for s in sorted({z["status"] for z in zeilen})}
    out["erwerbsfaehige_haushalte"] = anteil(np.array([z["status"] != "Rentner" for z in zeilen]))
    out["mit_teilzeit"] = anteil(np.array([z["tz"] for z in zeilen]))
    out["mit_kindern"] = anteil(np.array([z["kinder"] for z in zeilen]))
    # Dezile des heutigen Äquivalenzeinkommens, Personen gewichtet
    o = np.argsort(aeq)
    cum = np.cumsum(wp[o]) / wp.sum()
    dez = np.empty(len(zeilen), int)
    dez[o] = np.minimum((cum * 10).astype(int), 9)
    out["dezile"] = [dict(dezil=i + 1, obergrenze_aequiv_monat_eur=round(float(aeq[dez == i].max() / 12)), **anteil(dez == i)) for i in range(10)]
    auf = np.array([z["neu"][wg][1] for z in zeilen])
    bg = np.array([z["bg_heute"] for z in zeilen])
    ren = np.array([z["status"] == "Rentner" for z in zeilen])
    ohne = np.array([z["status"].startswith("ohne Erwerb") for z in zeilen])
    out["kosten_mrd"] = dict(grundauskommen_neu=round(float((w * auf).sum() / 1e9), 1),
                             davon_ohne_erwerb=round(float((w * auf)[ohne].sum() / 1e9), 1),
                             davon_erwerbstaetige_haushalte=round(float((w * auf)[~ohne & ~ren].sum() / 1e9), 1),
                             davon_rentner=round(float((w * auf)[ren].sum() / 1e9), 1),
                             buergergeld_naeherung_heute=round(float((w * bg).sum() / 1e9), 1),
                             grundsicherung_alter_heute=round(float(sum(z["w"] * z.get("gs_heute", 0.0) for z in zeilen) / 1e9), 1),
                             grundsicherung_alter_faelle_heute_mio=round(float(sum(z["w"] * z.get("gs_faelle", 0) for z in zeilen) / 1e6), 2),
                             amtlich_grundsicherung_alter=dict(empfaenger_mio=0.764, ausgaben_mrd_mit_erwerbsminderung=11.8,
                                                               quelle="rentnerausgleich.toml (Destatis/BMAS über Münster Aktuell, Sekundärquelle)"),
                             hinweis="Jahresbeträge 2028 in Kaufkraft 2026; Grundauskommen = Aufstockung über Dividende und eigenes Einkommen; "
                                     "heute: Bürgergeld-Näherung bei voller Inanspruchnahme (einschließlich Wohngeld und Kinderzuschlag genähert), ohne Grundsicherung im Alter")
    return out


def gew_median(x, w):
    o = np.argsort(x)
    c = np.cumsum(w[o])
    return x[o][np.searchsorted(c, c[-1] / 2)]


def main():
    abw = gegenprobe()
    S = P["szenarien"]
    rho0, wg0 = P["partner"]["basis_korrelation"], S["basis_weitergabe"]
    E = dict(version=P["version"], status="Prüfrechnung (synthetische Population, Stufe 1)", jahr=J, kaufkraft=2026, gegenprobe_max_abweichung_eur=abw,
             vollzeit_pareto_alpha=round(vz_alpha(), 3), rente_lognormal=dict(zip(("mu", "sigma"), [round(x, 4) for x in rente_parameter()])))
    basis, ziehungen = None, []
    for seed in P["seeds"]:
        hh, rr, st, sb = ziehe(seed, rho0)
        w, wr, sp = eiche(hh, rr, st, sb)
        z = rechne(hh, rr, w, wr, S["weitergabe"])
        erg = {str(wg): auswerten(z, wg) for wg in S["weitergabe"]}
        ziehungen.append(erg)
        if basis is None:
            basis = dict(eichung=sp, validierung_2025=validierung(hh, w), ergebnis=erg)
    E["basis"] = basis

    def spanne(pfad):
        werte = []
        for erg in ziehungen:
            x = erg
            for k in pfad:
                x = x[k]
            werte.append(x)
        return [min(werte), max(werte)]
    E["ziehungen"] = {str(wg): dict(gesamt_haushalte=spanne([str(wg), "gesamt", "anteil_mehr_haushalte_pct"]),
                                    vollzeit=spanne([str(wg), "status", "Hauptperson Vollzeit", "anteil_mehr_haushalte_pct"]),
                                    teilzeit=spanne([str(wg), "status", "Hauptperson Teilzeit", "anteil_mehr_haushalte_pct"]),
                                    rentner=spanne([str(wg), "status", "Rentner", "anteil_mehr_haushalte_pct"]),
                                    grundauskommen_mrd=spanne([str(wg), "kosten_mrd", "grundauskommen_neu"])) for wg in S["weitergabe"]}
    # Partnerkorrelation und Haushaltsanteile (Ziehung 1, Basis-Weitergabe)
    E["partnerkorrelation"] = {}
    for rho in P["partner"]["korrelation"]:
        hh, rr, st, sb = ziehe(P["seeds"][0], rho)
        w, wr, _ = eiche(hh, rr, st, sb)
        a = auswerten(rechne(hh, rr, w, wr, [wg0]), wg0)
        E["partnerkorrelation"][str(rho)] = dict(gesamt=a["gesamt"], paar_ohne=a["haushaltstyp"]["paar_ohne"], paar_mit=a["haushaltstyp"]["paar_mit"])
    E["struktur"] = {}
    for name, fak in S["struktur"].items():
        hh, rr, st, sb = ziehe(P["seeds"][0], rho0, fak)
        w, wr, _ = eiche(hh, rr, st, sb)
        a = auswerten(rechne(hh, rr, w, wr, [wg0]), wg0)
        E["struktur"][name] = dict(faktor_allein=fak, gesamt=a["gesamt"], kosten_mrd=a["kosten_mrd"])
    E["hinweis"] = ("Synthetische Population aus veröffentlichten Eckwerten; Spanne der Ziehungen misst nur das Rauschen der Ziehung, nicht die "
                    "Unsicherheit der Annahmen (Haushaltszahlen, Teilzeitstreuung, Partnerstatus, Rentenverteilung). Nicht abgebildet: Selbständige "
                    "und Beamte (Haushalte herausgenommen), Hinterbliebenen- und Betriebsrenten, Vermögenseinkommen, Rentner mit Minijob, "
                    "Nicht-Inanspruchnahme von Bürgergeld. Validierung nur an Aggregaten, auf die nicht geeicht wurde.")
    (AGG / "mikro_de.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
    b = basis["ergebnis"]
    print("Gegenprobe", abw, "€ | Eichung", basis["eichung"])
    print("Validierung 2025:", json.dumps(basis["validierung_2025"], ensure_ascii=False))
    for wg in S["weitergabe"]:
        g = b[str(wg)]
        print(f"Weitergabe {wg:.0%}: gesamt {g['gesamt']['anteil_mehr_haushalte_pct']} % HH | "
              + " | ".join(f"{k} {v['anteil_mehr_haushalte_pct']} %" for k, v in g["status"].items()) + f" | Kosten {g['kosten_mrd']}")
    print("Ziehungen", E["ziehungen"])
    print("Partner", {k: v["gesamt"]["anteil_mehr_haushalte_pct"] for k, v in E["partnerkorrelation"].items()},
          "Struktur", {k: v["gesamt"]["anteil_mehr_haushalte_pct"] for k, v in E["struktur"].items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
