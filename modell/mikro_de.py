#!/usr/bin/env python3
"""Synthetische Mikrosimulation Deutschland, Stufe 1 (Logbuch v4.22). Prüfrechnung.

Ziel: Anteil mit mehr verfügbarem Einkommen (Stand C, 2028, Kaufkraft 2026) nicht nur für drei Beispielhaushalte, sondern für eine
auf veröffentlichte Verteilungen geeichte Gesamtbevölkerung: Vollzeit, Teilzeit, Minijob, Bürgergeld, Familien, Rentner.
Keine Mikrodaten: Die Datensätze werden gezogen (fester Startwert) und mit Raking (Deville/Särndal, exponentiell) auf Eckwerte geeicht.

Aufbau
  1. Haushalte erwerbsfähigen Alters (allein, alleinerziehend, Paar ohne / mit minderjährigen Kindern, ggf. ein volljähriges Kind),
     Erwerbsstatus je Erwachsenem (Vollzeit, Teilzeit, Minijob, ohne Erwerb), Löhne aus den amtlichen Verteilungen (mikro_de.toml).
     Partnerlöhne über eine Gauß-Copula mit Rangkorrelation rho.
  2. Rentnerhaushalte (allein, Paar): seit v4.23 Haushaltseinkommen aus EU-SILC mit Einkommensarten nach ASID (modell/mikro_rentner_de.py);
     v4.22 zog Renten je Rente (Grundsicherung im Alter weit überschätzt, Validierung nicht bestanden).
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
MR = lade("mr", "modell/mikro_rentner_de.py")      # v4.23
MB = lade("mb", "modell/mikro_bs_de.py")           # v4.28: Beamte und Selbständige
ZULAGE = MB.P["beamte"]["zulage"]["basis"]
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
    if art in ("mini", "beamt") or b <= 0:                 # Beamte: private KV je Haushalt (heute())
        return 0.0
    if art == "selbst":                                    # v4.28: freiwillige KV/PV der Selbständigen
        S = MB.P["selbst"]
        return S["kv_satz"] * min(max(b, S["kv_mindest_jahr"]), K.BBG_KV)
    v = K.sv_heute(b, kinderlos)
    if midijob and b < MIDI_OBEN:
        v *= max(0.0, (b - MINI) / (MIDI_OBEN - MINI))
    return v


def heute(hh, midijob=True):
    """hh: dict(erw=[(lohn, art)], kind=minderjährige, vkind=(lohn, art) oder None, paar=bool)."""
    kinderlos = hh["kind"] == 0 and hh["vkind"] is None
    sv = [sv_an(b, a, kinderlos, midijob) for b, a in hh["erw"]]
    zve = [max(0.0, b - s - K.WK_PAUSCH * (b > 0 and a != "selbst")) if a != "mini" else 0.0 for (b, a), s in zip(hh["erw"], sv)]
    if any(a == "beamt" for _, a in hh["erw"]):            # v4.28: private KV zur Beihilfe für den Haushalt, zu 80 % abziehbar
        ohne = sum(1 for b, a in hh["erw"][1:] if a in ("ohne", "mini"))
        pk = MB.pkv(ohne, hh["kind"])
        i = next(j for j, (_, a) in enumerate(hh["erw"]) if a == "beamt")
        sv[i] = pk
        zve[i] = max(0.0, zve[i] - MB.P["beamte"]["pkv_abziehbar"] * pk)
    kap, miete = hh.get("kap", 0.0), hh.get("miete", 0.0)          # v4.29 R3: Kapital- und Mieteinkünfte
    zve[0] += miete                                                 # Vermietung nach Tarif (Paare: Splitting über die Summe)
    if hh["paar"]:
        z = max(0.0, sum(zve) - 2 * K.SA_PAUSCH)
        est = 2 * K.est_2026(z / 2)
        st = est + K.soli_2026(est, True)
    else:
        z = max(0.0, zve[0] - K.SA_PAUSCH)
        est = K.est_2026(z)
        st = est + K.soli_2026(est)
    brutto = sum(b for b, _ in hh["erw"])
    abgeltung = max(0.0, kap - KP["sparerpauschbetrag"] * len(hh["erw"])) * KP["abgeltung_satz"]
    netto = brutto - sum(sv) - st + kap + miete - abgeltung
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
    return netto + bg, dict(lohnsteuer=est, soli=st - est, sv=sum(sv), kindergeld=n_kg * K.KINDERGELD * 12, buergergeld=bg, abgeltung=abgeltung)


# ------------------------------------------------------------------ neu (Stand C, regel_boden)
def brutto_neu(b, art, w, zulage):
    """v4.28: Weitergabe nur für Arbeitnehmer; Beamte erhalten die Versicherungszulage (Vorschlag), Selbständige den Gewinn."""
    if art == "beamt":
        return b + MB.zulage(b, zulage)
    if art in ("selbst", "ohne"):
        return b
    return b + w * H33.ag(b)


def neu(hh, w, zulage=None):
    zulage = ZULAGE if zulage is None else zulage
    arten = hh["erw"] + ([hh["vkind"]] if hh["vkind"] else [])
    loehne = [b for b, _ in arten]
    e, k = len(loehne), hh["kind"]
    brutto = [brutto_neu(b, a, w, zulage) for b, a in arten]
    extra = hh.get("kap", 0.0) + hh.get("miete", 0.0)               # v4.29 R3: Kapital und Miete nach 33R, je Hälfte bei Paaren (Annahme)
    for i in range(len(hh["erw"])):
        brutto[i] += extra / len(hh["erw"])
    st = sum(est_neu(x + DIV) for x in brutto)
    netto = sum(brutto) - st + DIV * e + k * DIV * RB.S
    konsum = HL.kq(netto, "DE") * netto
    fm, fb = HL.mwst_phi("DE", netto)                                                   # v4.29
    netto = netto - fm * konsum * ((1 + EFF / 100) / (1 + HL.eff_alt("DE") / 100) - 1) - ZU / 100 * (st + fb * konsum * EFF / (100 + EFF))
    dv = DIV * (e + RB.S * k)
    auf = max(0.0, RB.boden("DE", e, k) - dv - RB.P["anrechnung"] * max(0.0, netto - dv))
    return netto + auf - HL.P["vorsorge"] * sum(loehne), auf


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


# ------------------------------------------------------------------ Population
TYPEN = ("allein", "alleinerziehend", "paar_ohne", "paar_mit")
# Ausgangswahrscheinlichkeiten Erwerbsstatus (vz, tz, mini, ohne) für Haushalte mit Erwerb – Annahme, wird geeicht
STATUS_P = {"allein": [(0.68, 0.20, 0.07, 0.05)], "alleinerziehend": [(0.40, 0.48, 0.08, 0.04)],
            "paar_ohne": [(0.80, 0.12, 0.04, 0.04), (0.55, 0.25, 0.07, 0.13)], "paar_mit": [(0.86, 0.08, 0.03, 0.03), (0.28, 0.45, 0.10, 0.17)]}
VKIND_P = (0.35, 0.10, 0.20, 0.35)          # volljähriges Kind: Ausbildung/Vollzeit, Teilzeit, Minijob, ohne (Annahme)
AZUBI = 13000                               # Ausbildungsvergütung 2024 (Annahme)
ARTEN = ("vz", "tz", "mini", "ohne")


def gewinn_aus_netto(netto):
    """Gewinn (2024) zu einem persönlichen Nettoeinkommen nach Recht 2026 (allein veranlagt, Annahme)."""
    lo, hi = 0.0, max(20000.0, 4 * netto)
    for _ in range(60):
        m = (lo + hi) / 2
        kv = sv_an(m, "selbst", True)
        est = K.est_2026(max(0.0, m - kv - K.SA_PAUSCH))
        lo, hi = (m, hi) if m - kv - est - K.soli_2026(est) < netto else (lo, m)
    return (lo + hi) / 2


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
    # v4.28: Beamte und Selbständige als Hauptperson (eigene Gewichte, nicht geeicht)
    bs, wbs = MB.ziehe(rng, MB.P["stichprobe"], {"vz": vz_quantil, "tz": tz_quantil, "mini": mini_quantil}, H["kinderzahl_anteile"], P["lohn_2024_2025"])
    for h, x in zip(bs, wbs):
        h["w"] = float(x)
        if h["erw"][0][1] == "selbst_netto":
            h["erw"][0] = (gewinn_aus_netto(h["erw"][0][0]), "selbst")
    haushalte += bs
    kapital_zuweisen(haushalte, rng)                                # v4.29 R3
    # Rentner (v4.23: Haushaltseinkommen, mikro_rentner_de)
    R = P["rentner"]
    rentner, wr = MR.ziehe(rng, P["rentner_stichprobe"], R["personen_mio"], R["allein_lebend_mio"])
    for r, x in zip(rentner, wr):
        r["w"] = float(x)
    return haushalte, rentner, soll_typ, soll_bg


def eiche(haushalte, rentner, soll_typ, soll_bg):
    """Exponentielles Raking: w = d · exp(X λ), Newton-Verfahren. Rentner getrennt (nur Personen und Alleinlebende)."""
    Bz = P["beschaeftigte"]
    H = P["haushalte"]
    mini_unter65 = Bz["minijob_ausschliesslich_mio"] * (1 - P["minijob"]["anteil_65plus"])
    spalten = [f"typ_{t}" for t in TYPEN] + ["bg", "vz", "tz", "mini", "kind", "vkind", "beamt", "selbst"]
    soll = np.array([soll_typ[t] for t in TYPEN] + [sum(soll_bg.values()), Bz["vollzeit_mio"], Bz["teilzeit_mio"], mini_unter65,
                     H["kinder_minderj_mio"], H["kinder_volljaehrig_mio"], MB.P["beamte"]["anzahl_mio"], MB.P["selbst"]["anzahl_mio"]]) * 1e6
    # v4.28: Beamte und Selbständige gemeinsam geeicht (Haushaltstypen, Kinder und Partnerbeschäftigung gelten für alle Haushalte)
    X = np.zeros((len(haushalte), len(spalten)))
    for i, h in enumerate(haushalte):
        X[i, TYPEN.index(h["typ"])] = 1
        X[i, 4] = h["bg"]
        arten = [a for _, a in h["erw"]] + ([h["vkind"][1]] if h["vkind"] else [])
        X[i, 5], X[i, 6], X[i, 7] = arten.count("vz"), arten.count("tz"), arten.count("mini")
        X[i, 8], X[i, 9] = h["kind"], h["vkind"] is not None
        X[i, 10], X[i, 11] = h.get("bs") == "beamt", h.get("bs") == "selbst"
    n_bs = sum(1 for h in haushalte if h.get("bs"))
    w_bs = sum(h["w"] for h in haushalte if h.get("bs"))
    d = np.array([h["w"] if h.get("bs") else (sum(soll_typ.values()) * 1e6 - w_bs) / (len(haushalte) - n_bs) for h in haushalte])
    lam = np.zeros(len(spalten))
    for _ in range(100):
        w = d * np.exp(X @ lam)
        r = soll - X.T @ w
        if np.max(np.abs(r) / soll) < 1e-9:
            break
        lam += np.linalg.solve((X * w[:, None]).T @ X, r)
    w = d * np.exp(X @ lam)
    wr = np.array([r["w"] for r in rentner])                 # Rentner: Personen und Alleinlebende (mikro_rentner_de.ziehe)
    spanne = dict(gewicht_min_max=[round(float((w / d).min()), 3), round(float((w / d).max()), 3)],
                  restfehler_max=float(np.max(np.abs(soll - X.T @ w) / soll)))
    return w, wr, spanne


# ------------------------------------------------------------------ Validierung 2025
def validierung(haushalte, w):
    V = P["validierung"]
    f = P["lohn_2024_2025"]
    lohnsumme, lst, soli, kg, n_bg_pos, n_aufstocker = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    for h, wi in zip(haushalte, w):
        hh = skaliere(h, f)
        _, d = heute(hh)
        lohnsumme += wi * sum(b for b, a in hh["erw"] if a != "selbst") + wi * (hh["vkind"][0] if hh["vkind"] else 0)   # v4.28: Gewinne nicht in D11
        if h.get("bs") != "selbst":                                  # Selbständige: veranlagte Einkommensteuer, nicht Lohnsteuer
            lst += wi * d["lohnsteuer"]
        soli += wi * d["soli"]
        kg += wi * d["kindergeld"]
        if d["buergergeld"] > 0:
            n_bg_pos += wi
            if not h["bg"]:
                n_aufstocker += wi
    # Ergänzung außerhalb der Population (Annahme): Minijobs im Nebenjob; Beamte seit v4.28 in der Population
    neben = 3.52e6 * float(np.mean(mini_quantil(np.linspace(0, 1, 101)))) * f
    beamte = lst_beamte = 0.0
    mrd = lambda x: round(x / 1e9, 1)
    lst_modell = lst + lst_beamte
    soll_lst = V["lohnsteuer_kasse_mrd"] + V["kindergeld_mrd"]
    return dict(
        bruttolohnsumme=dict(modell_mrd=mrd(lohnsumme + neben + beamte), davon_population=mrd(lohnsumme), nebenjob_minijobs=mrd(neben),
                             amtlich_d11_mrd=V["bruttoloehne_d11_mrd"],
                             abweichung_pct=round(((lohnsumme + neben + beamte) / 1e9 / V["bruttoloehne_d11_mrd"] - 1) * 100, 1)),
        lohnsteuer=dict(modell_mrd=mrd(lst_modell), amtlich_lohnsteuer_plus_kindergeld_mrd=round(soll_lst, 1),
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
    return dict(h, erw=[(b * f, a) for b, a in h["erw"]], vkind=(h["vkind"][0] * f, h["vkind"][1]) if h["vkind"] else None,
                kap=h.get("kap", 0.0) * f * KAP_SKAL[0], miete=h.get("miete", 0.0) * f)


KP = P["kapital"]
KAP_SKAL = [1.0]                                                    # Empfindlichkeit Untererfassung (main setzt Varianten)


def lognorm_parameter(median, mittel):
    return math.log(median), math.sqrt(2 * math.log(mittel / median))


def kapital_zuweisen(haushalte, rng):
    """v4.29 R3: Kapital- und Mieteinkünfte (Jahr, 2024) nach Rang des Erwerbseinkommens; Besitz und Höhe steigen mit dem Rang (Annahmen)."""
    n = len(haushalte)
    lohn = np.array([sum(b for b, _ in h["erw"]) for h in haushalte])
    rang = (np.argsort(np.argsort(lohn + rng.random(n) * 1e-6)) + 0.5) / n
    z = norm.ppf(rang)
    gesamt = sum(P["haushalte"][k] for k in ("allein_mio", "alleinerziehend_mio", "paar_ohne_minderj_mio", "paar_mit_minderj_mio"))
    for art, hh_mio, med, mit in (("kap", KP["kap_haushalte_mio"], KP["kap_median_monat"], KP["kap_mittel_monat"]),
                                   ("miete", KP["miete_haushalte_mio"], KP["miete_median_monat"], KP["miete_mittel_monat"])):
        grund = hh_mio * KP["anteil_erwerbsfaehig"] / gesamt
        p_besitz = np.clip(grund * (0.4 + KP["besitz_steigung"] * rang), 0, 0.95)
        mu, sig = lognorm_parameter(med, mit)
        r = KP["rang_korrelation"]
        betrag = 12 * np.exp(mu + sig * (r * z + math.sqrt(1 - r * r) * rng.standard_normal(n)))
        hat = rng.random(n) < p_besitz
        for h, x, j in zip(haushalte, betrag, hat):
            h[art] = float(x) if j else 0.0


# ------------------------------------------------------------------ Auswertung
def personen(h):
    return len(h["erw"]) + h["kind"] + (1 if h["vkind"] else 0)


def aequiv(h, y):
    return y / (1 + 0.5 * (len(h["erw"]) + (1 if h["vkind"] else 0) - 1) + 0.3 * h["kind"])


def gruppe_status(h):
    if h.get("bs"):
        return {"beamt": "Hauptperson Beamte", "selbst": "Hauptperson selbständig"}[h["bs"]]
    if h["bg"]:
        return "ohne Erwerb (Bürgergeld)"
    a = h["erw"][0][1]
    return {"vz": "Hauptperson Vollzeit", "tz": "Hauptperson Teilzeit", "mini": "Hauptperson Minijob", "ohne": "Hauptperson ohne Erwerb"}[a]


def rechne(haushalte, rentner, w, wr, weitergaben, rentner_variante="asid", inanspruchnahme="voll", zulage=None):
    f = P["lohn_2024_2026"]
    zeilen = []
    for h, wi in zip(haushalte, w):
        hh = skaliere(h, f)
        y0, d0 = heute(hh)
        res = {}
        for wg in weitergaben:
            y1, auf = neu(hh, wg, zulage)
            res[wg] = (y1, auf)
        zeilen.append(dict(w=wi, p=personen(h), typ=h["typ"], status=gruppe_status(h), tz=any(a == "tz" for _, a in h["erw"]),
                           kinder=h["kind"] > 0, heute=y0, aeq=aequiv(h, y0), neu=res, bg_heute=d0["buergergeld"]))
    for r, wi in zip(rentner, wr):
        res = {}
        for wg in weitergaben:
            y0, y1, auf, gs, _ = MR.rechne(r, f, wg, rentner_variante, inanspruchnahme)
            res[wg] = (y1, auf)
        n = r["n"]
        zeilen.append(dict(w=wi, p=n, typ=r["typ"], status="Rentner", tz=False, kinder=False, heute=y0, aeq=y0 / (1 + 0.5 * (n - 1)),
                           neu=res, bg_heute=0.0, gs_heute=gs, gs_faelle=n * (gs > 0)))
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
    E = dict(version=P["version"], status="Prüfrechnung (synthetische Population; Rentner Stufe 2; Beamte und Selbständige v4.28)", jahr=J, kaufkraft=2026, gegenprobe_max_abweichung_eur=abw,
             vollzeit_pareto_alpha=round(vz_alpha(), 3))
    basis, ziehungen = None, []
    for seed in P["seeds"]:
        hh, rr, st, sb = ziehe(seed, rho0)
        w, wr, sp = eiche(hh, rr, st, sb)
        z = rechne(hh, rr, w, wr, S["weitergabe"])
        erg = {str(wg): auswerten(z, wg) for wg in S["weitergabe"]}
        ziehungen.append(erg)
        if basis is None:
            basis = dict(eichung=sp, validierung_2025=validierung(hh, w), pruefung_rentner=MR.pruefwerte(rr, wr, P["rente_2023_2024"]), ergebnis=erg)
            # v4.28: Versicherungszulage der Beamten (Ziehung 1, Basis-Weitergabe)
            E["beamte_zulage"] = dict(basis=ZULAGE, beihilfe_je_beamter=round(MB.beihilfe_je_beamter()),
                                      selbst_netto_lognormal=dict(zip(("mu", "sigma", "kum_anteile"), MB.selbst_lognormal())), varianten={})
            for var in MB.P["beamte"]["zulage"]["varianten"]:
                a = auswerten(rechne(hh, rr, w, wr, [wg0], zulage=var), wg0)
                E["beamte_zulage"]["varianten"][var] = dict(beamte=a["status"]["Hauptperson Beamte"], gesamt=a["gesamt"])
            # v4.29 R3: Kapitaleinkünfte, Summen und Untererfassung (Ziehung 1, Basis-Weitergabe)
            f26 = P["lohn_2024_2026"]
            E["kapital"] = dict(summe_kapital_mrd_2024=round(float(sum(wi * h.get("kap", 0.0) for h, wi in zip(hh, w)) / 1e9), 1),
                                summe_miete_mrd_2024=round(float(sum(wi * h.get("miete", 0.0) for h, wi in zip(hh, w)) / 1e9), 1),
                                abgeltung_heute_mrd=round(float(sum(wi * heute(skaliere(h, 1.0))[1]["abgeltung"] for h, wi in zip(hh, w))) / 1e9, 1),
                                vergleich="EU-SILC (Umfrage) erfasst rund 25 Mrd. € Kapitaleinkünfte aller Haushalte; Abgeltungsteuer 2025 24,8 Mrd. € "
                                          "(alle Steuerpflichtigen) entspricht rund 94 Mrd. € Erträgen über den Freibeträgen", skalierung={})
            for sk in KP["skalierung_varianten"]:
                KAP_SKAL[0] = sk
                a = auswerten(rechne(hh, rr, w, wr, [wg0]), wg0)
                E["kapital"]["skalierung"][str(sk)] = dict(gesamt=a["gesamt"], dezil_10=a["dezile"][9], dezil_9=a["dezile"][8])
            KAP_SKAL[0] = 1.0
            # v4.23: Varianten der Rentnerhaushalte (Ziehung 1, Basis-Weitergabe)
            E["rentner_varianten"] = {}
            for var, inan in (("asid", "voll"), ("asid", "beobachtet"), ("nur_grv", "voll")):
                a = auswerten(rechne(hh, rr, w, wr, [wg0], var, inan), wg0)
                E["rentner_varianten"][f"{var}/{inan}"] = dict(rentner=a["status"]["Rentner"], rentner_allein=a["haushaltstyp"]["rentner_allein"],
                                                              rentner_paar=a["haushaltstyp"]["rentner_paar"], gesamt=a["gesamt"],
                                                              dezil_1=a["dezile"][0], kosten_mrd=a["kosten_mrd"])
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
                    "Unsicherheit der Annahmen (Haushaltszahlen, Teilzeitstreuung, Partnerstatus, Zusammensetzung der Alterseinkommen). Nicht abgebildet: "
                    "Vermögenseinkommen der Erwerbstätigen, Rentner unter 65, Partner der Beamten und Selbständigen nicht in der Eichung (Doppelzählung möglich), "
                    "Nicht-Inanspruchnahme von Bürgergeld (Rentner: Variante beobachtet). Validierung nur an Aggregaten, auf die nicht geeicht wurde.")
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
