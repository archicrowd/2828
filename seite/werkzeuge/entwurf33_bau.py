#!/usr/bin/env python3
"""Entwurf der überarbeiteten Webseite (Drittel-System, seit v3.48 System 33R), nur Deutsch, zur Prüfung durch die Initiative (Logbuch v3.47/v3.48).

Die veröffentlichte Seite (seite/stand-b, Bau: seite_bau.py) bleibt unverändert. Dieser Entwurf übernimmt Stylesheet und Gestaltung
(stylesheet(), ZUSATZ_CSS aus seite_bau.py) und füllt alle Zahlen aus den Ergebnissen der Prüfrechnungen:
  daten/aggregate/systemvarianten.json (System 33F), haushalte33.json + haushalte33_raster.json (modell/haushalte33.py),
  projektion33.json (modell/projektion33.py), altlasten.json (modell/altlasten.py), gesamtrechnung.json (Ausgangslage).
Quellen der Aussagen, die nicht aus der Rechnung stammen: seite/entwurf/QUELLEN-33.md.
Aufruf: python3 seite/werkzeuge/entwurf33_bau.py  ->  seite/entwurf/konzept33/de.html
"""
import importlib.util
import json
import re
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
AGG = WURZEL / "daten" / "aggregate"
ZIEL = WURZEL / "seite" / "entwurf" / "konzept33"
spec = importlib.util.spec_from_file_location("seite_bau", Path(__file__).resolve().parent / "seite_bau.py")
SB = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SB)


def lade(n):
    return json.loads((AGG / n).read_text(encoding="utf-8"))


SV, H, RA, PJ, AL, J, DY = (lade(n) for n in ("systemvarianten.json", "haushalte33.json", "haushalte33_raster.json", "projektion33.json",
                                               "altlasten.json", "gesamtrechnung.json", "dynamik33.json"))
V = next(x for x in SV["varianten"] if x["id"] == PJ["system"])
ZU = max(f["zuschlag_pct"] for f in H["faelle"])                 # Beispielzuschlag (Altlastenfonds, Beschluss)
F26 = 1.0404                                   # Preise 2028 -> Kaufkraft 2026 (2 % je Jahr, Annahme der Gesamtrechnung)
G26 = 12348
REIHE = {r["jahr"]: r for r in PJ["reihe"]}


def zahl(x, nk=0):
    return SB.zahl(x, nk, "de")


def eur(x, nk=0):
    return SB.eur(x, "de", nk)


def pct(x, nk=0):
    return SB.pct(x, "de", nk)


def fall(jahr, haushalt, wg=0.8, zu=0.0, vs=0.186):
    return next(f for f in H["faelle"] if f["jahr"] == jahr and f["haushalt"] == haushalt and f["weitergabe_ag"] == wg
                and f["zuschlag_pct"] == zu and f["vorsorge_satz"] == vs)


def zeile(f, b):
    return next(z for z in f["zeilen"] if z["brutto"] == b)


def altfall(z=None):
    return AL["beschluss"]


def werte():
    d28, d35, d60 = REIHE[2028], REIHE[2035], REIHE[2060]
    m42 = zeile(fall(2028, "alleinstehend"), 42000)
    m42z = zeile(fall(2028, "alleinstehend", zu=ZU), 42000)
    m42k = zeile(fall(2028, "alleinstehend", wg=1.0), 42000)
    plus42_35 = zeile(fall(2035, "alleinstehend"), 42000)["differenz_monat"]
    plus150 = zeile(fall(2028, "alleinstehend"), 150000)["differenz_monat"]
    m42o = zeile(fall(2028, "alleinstehend", vs=0.0), 42000)
    gr = zeile(fall(2028, "alleinstehend", vs=0.0), 55000)
    rent = {(r["rente_monat"], r["zuschlag_pct"]): r for r in H["rentner"]}
    a1 = altfall(1.0)
    fh = [x for x in PJ["buergerfonds"] if x["anteil"] == 0.5]
    an = H["anteil_erwachsene_mit_mehr"]
    def dyn(b, ki, kv, j="2060"):
        return next(x for x in DY["szenarien"] if x["beschaeftigung_pct"] == b and x["ki_pp"] == ki
                    and x["kapital_verschiebung_pp"] == kv)["reihe"][j]["dividende_erw_eur2026"]
    d45 = REIHE[2045]
    return dict(
        netz28=eur(d28["netz_eur_kopf_monat"]), netz60=eur(d60["netz_eur_kopf_monat"]),
        paket28=eur(d28["netz_eur_kopf_monat"] + d28["dividende_erw_eur2026"]), paket60=eur(d60["netz_eur_kopf_monat"] + d60["dividende_erw_eur2026"]),
        prog60=zahl(d60["progression"], 1), div45=eur(d45["dividende_erw_eur2026"]),
        dyn_ki_lo=eur(dyn(0.0, 0.07, 0.0)), dyn_ki_hi=eur(dyn(0.0, 0.6, 0.0)), dyn_b=eur(dyn(4.6, 0.0, 0.0)),
        dyn_mittel=eur(dyn(4.6, 0.3, 3.0)), dyn_max=eur(dyn(4.6, 0.6, 3.0)),
        heute_kap=zahl(abs(next(x for x in DY["szenarien"] if x["kapital_verschiebung_pp"] == 3.0)["heute_aufkommen_aenderung_2060_pct_bip"]), 2),
        div28=eur(d28["dividende_erw_eur2026"]), kind28=eur(d28["dividende_erw_eur2026"] / 2),
        div35=eur(d35["dividende_erw_eur2026"]), div60=eur(d60["dividende_erw_eur2026"]),
        div60_ohne=eur(d60["dividende_ohne_trends_eur2026"]),
        lenk28=pct(d28["lenkung_pct_bip"], 1), lenk60=pct(d60["lenkung_pct_bip"], 1),
        lenkanteil=pct(d28["lenkung_pct_bip"] / d28["dividende_pct_bip"] * 100),
        ges_plus=zahl(d60["gesundheit_plus"], 1),
        label_eff=pct(V["label_effektiv"], 1), deckung=pct(V["deckung"], 1),
        plus42=eur(m42["differenz_monat"]), plus42z=eur(m42z["differenz_monat"]), plus42k=eur(m42k["differenz_monat"]),
        plus42o=eur(m42o["differenz_monat"]),
        gh55=pct(gr["grenzbelastung_heute"]), gn55=pct(gr["grenzbelastung_33"]),
        r1200=eur(rent[(1200, 0.0)]["differenz_monat"]), r1200z=eur(rent[(1200, ZU)]["differenz_monat"]), r900=eur(rent[(900, 0.0)]["differenz_monat"]), r2200=eur(rent[(2200, 0.0)]["differenz_monat"]),
        anteil_voll=pct(an[f"2028|weitergabe 0.8|zuschlag {ZU}|vorsorge 0.186"]), zu=pct(ZU, 1), zu_v=str(ZU),
        st1=eur(G26), st15=eur(G26 * 1.5), st2=eur(G26 * 2), st3=eur(G26 * 3),
        a_c=zahl(a1["beitrag_pct_bip"], 2).replace(",00", ""), a_zu=pct(a1["zuschlag_auf_alle_steuern_pct"], 1), a_sp=pct(a1["schuldenquote_spitze"]),
        a_spj=str(a1["spitzenjahr"]), keil=pct(J["abgabenkeil_de_2024"], 1), keil_oecd=pct(J["abgabenkeil_oecd_2024"], 1),
        abgeltung=pct(J["abgeltungsteuer_de"], 1), og=pct(J["obergrenze"]), gesundheit=pct(SV["gesundheit"], 2), seil=pct(SV["seil"], 2),
        version="v3.49 (Entwurf)", plus42_35=eur(plus42_35), plus150=eur(plus150), f28=eur(fh[0]["dividende_erw_eur2026"]["2028"]), f60a=eur(fh[0]["dividende_erw_eur2026"]["2060"]),
        f60b=eur(fh[1]["dividende_erw_eur2026"]["2060"]), fv=pct(fh[0]["fondsvermoegen_2060_pct_bip"]),
    )


# ------------------------------------------------------------------ Grafiken (statisch, SVG)
def linie(xs, ys, x0, x1, lo, hi, W=900, H=340, L=64, R=24, T=18, B=40):
    def px(x):
        return L + (x - x0) / (x1 - x0) * (W - L - R)

    def py(y):
        return T + (1 - (y - lo) / (hi - lo)) * (H - T - B)
    return " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in zip(xs, ys)), px, py


def achsen(px, py, xt, yt, fmt, W=900, H=340, L=64, R=24, T=18, B=40):
    s = []
    for y in yt:
        s.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{py(y):.1f}" y2="{py(y):.1f}"/>'
                 f'<text class="axis" x="{L - 8}" y="{py(y) + 4:.1f}" text-anchor="end">{fmt(y)}</text>')
    for x in xt:
        s.append(f'<text class="axis" x="{px(x):.1f}" y="{H - 14}" text-anchor="middle">{zahl(x) if x > 3000 else x}</text>')
    return "".join(s)


def grafik_grenz():
    xs = RA["grenz_brutto"]
    p_h, px, py = linie(xs, RA["grenz_heute"], 10000, 150000, 0, 70)
    p_n, _, _ = linie(xs, RA["grenz_neu"]["0.8"], 10000, 150000, 0, 70)
    p_k, _, _ = linie(xs, RA["grenz_neu"]["1.0"], 10000, 150000, 0, 70)
    ax = achsen(px, py, [10000, 40000, 70000, 100000, 130000], [0, 20, 40, 60], lambda y: f"{y} %")
    return (f'<svg id="chart" class="g33" viewBox="0 0 900 340" role="img" aria-label="Grenzbelastung heute und neu">{ax}'
            f'<polyline class="ohne" points="{p_h}"/><polyline class="prog" points="{p_k}"/><polyline class="mit" points="{p_n}"/></svg>')


def grafik_zeit():
    xs = [r["jahr"] for r in PJ["reihe"]]
    ohne = [r["dividende_ohne_trends_eur2026"] for r in PJ["reihe"]]
    mit = [r["dividende_erw_eur2026"] for r in PJ["reihe"]]
    lenk = [r["dividende_erw_eur2026"] * r["lenkung_pct_bip"] / r["dividende_pct_bip"] if r["dividende_pct_bip"] > 0 else 0 for r in PJ["reihe"]]
    p_o, px, py = linie(xs, ohne, 2028, 2060, 0, 320)
    p_m, _, _ = linie(xs, mit, 2028, 2060, 0, 320)
    p_l, _, _ = linie(xs, [min(a, b) for a, b in zip(lenk, mit)], 2028, 2060, 0, 320)
    flaeche = p_l + f" {px(2060):.1f},{py(0):.1f} {px(2028):.1f},{py(0):.1f}"
    ax = achsen(px, py, [2028, 2035, 2040, 2045, 2050, 2055, 2060], [0, 100, 200, 300], lambda y: f"{y} €")
    return (f'<svg id="chart2" viewBox="0 0 900 340" role="img" aria-label="Dividende 2028 bis 2060">{ax}'
            f'<polygon points="{flaeche}" fill="#1D7A4F" opacity=".14"/>'
            f'<polyline class="prog" points="{p_o}"/><polyline class="mit" points="{p_m}"/></svg>')


CSS33 = """
.g33 .grid,#chart2 .grid{stroke:var(--line-soft)}
.g33 .axis,#chart2 .axis{font-family:var(--mono);font-size:12px;fill:var(--dim)}
.g33 .ohne{stroke:var(--warn);fill:none;stroke-width:2.5;stroke-linecap:round}
.g33 .mit{stroke:var(--accent);fill:none;stroke-width:3.5;stroke-linecap:round}
.g33 .prog{stroke:var(--accent);fill:none;stroke-width:2;stroke-dasharray:6 6}
.legend .l-ohne i{border-color:var(--warn)}
.pruef{border:2px dashed var(--warn);background:#fff;border-radius:3px;padding:20px 24px;margin:28px auto 0;max-width:980px}
.pruef h3{font-family:var(--disp);font-size:18px;margin-bottom:8px;color:var(--warn)}
.pruef li{margin:6px 0 6px 18px;font-size:15px;line-height:1.5}
.seg.klein button{font-size:12px;padding:6px 10px}
.vergl{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}
.vergl .c{display:block;border:1px solid var(--line);border-radius:3px;padding:12px;background:#fff}
.vergl .k{display:block;font-family:var(--mono);font-size:11.5px;color:var(--dim);text-transform:uppercase;letter-spacing:.06em}
.vergl .v{display:block;font-family:var(--mono);font-size:26px;font-weight:500;margin-top:4px}
.vergl .v.new{color:var(--accent)}
.trend{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:18px 0 22px}
.grenzen li{margin:8px 0 8px 18px;line-height:1.55;font-size:15.5px}
"""

# ------------------------------------------------------------------ Texte (Deutsch, Du-Form)
SEITE = r"""<!DOCTYPE html><html lang="de"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ein Drittel höchstens – Entwurf</title>
<meta name="description" content="Höchstens ein Drittel auf jeden Euro, keine Sozialbeiträge, Gesundheit und Absicherung ohne Prämie. Ein Bauplan, den jeder Staat übernehmen kann.">
<meta name="robots" content="noindex, nofollow">
<style>@@CSS@@</style></head><body>
<div style="background:#B03A2E;color:#fff;font-family:monospace;padding:8px 16px;text-align:center">ENTWURF ZUR PRÜFUNG – nicht veröffentlichen · Stand {version}</div>
<nav class="titleblock" id="top" aria-label="Seitennavigation"><div class="wrap">
  <a class="tb-left" href="#top">33 : 33</a>
  <div class="tb-right"><a href="#konzept">Bauplan</a><a class="opt" href="#paket">Paket</a><a href="#rechner">Rechner</a><a class="opt" href="#zeitpfad">Bis 2060</a>
  <a class="opt" href="#altlasten">Altlasten</a><a href="#vorbilder">Vorbilder</a><a class="opt" href="#offen">Mitmachen</a></div>
</div></nav>

<header class="hero"><div class="wrap">
  <svg class="hero-mark" viewBox="0 0 560 300" role="img" aria-label="33:33">
    <text x="60" y="168" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="196" fill="#0F3B5C" textLength="440" lengthAdjust="spacing">TAX</text>
    <text x="60" y="286" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="116" fill="#0F3B5C" letter-spacing="-2" textLength="440" lengthAdjust="spacing">33:33</text>
  </svg>
  <h1>Ein Drittel. Höchstens.</h1>
  <p class="claim2">Mehr Netto. Versorgt ohne Prämie. Ein Netz, das trägt.</p>
  <p class="sub">Auf jeden Euro – aus Arbeit, Kapital, Gewinn oder Erbe – höchstens ein Drittel Steuer. Keine Sozialbeiträge, keine Prämien:
  Gesundheit, Arbeitslosigkeit, Invalidität und Hinterbliebene sind für alle abgesichert. Ein Bauplan aus bewährten Vorbildern, den jeder Staat übernehmen kann.</p>
  <div class="cta-row"><a class="btn primary" href="#rechner">Selbst nachrechnen</a><a class="btn ghost" href="#konzept">Bauplan ansehen</a></div>
  <p class="opensrc">Alle Rechenmodelle sind <a href="#offen">offen prüfbar</a>.</p>
  <div class="stamps">
    <div class="stamp"><div class="val">33 %</div><div class="lbl">das Goldene Drittel: höchstens, auf jedes Einkommen</div></div>
    <div class="stamp"><div class="val">0 €</div><div class="lbl">Prämie für das Goldene Netz</div></div>
    <div class="stamp"><div class="val">+{plus42}*</div><div class="lbl">mehr im Monat bei 42.000 € brutto – nach eigener Vorsorge</div></div>
  </div>
  <p class="fineprint" style="text-align:center;margin:16px auto 0">* Schätzung des Projekts: alleinstehend, 2028, Kaufkraft 2026; mindestens 80 % der gesparten Arbeitgeberbeiträge gehen in den Lohn (Pflicht);
  vom Mehr ist schon abgezogen, was heute in die Rentenversicherung fließt, als eigene Vorsorge. Ohne Altlastenzuschlag des Staates; mit Zuschlag +{plus42z}.</p>

  <div class="pruef"><h3>Zur Prüfung durch die Initiative (erscheint nicht auf der Seite)</h3><ol>
    <li><b>Name:</b> Der Bauplan heißt im Entwurf „33:33“. Absender bleibt die Initiative 28:28. Alternative: „TAX 28:28 – Drittel-Fassung“.</li>
    <li><b>Namen (Vorschlag, im Entwurf verwendet):</b> „Das Goldene Drittel“ (Steuerregel), „Das Goldene Netz“ (Absicherung ohne Prämie), „Transformationsdividende“
      (Geldzuweisung), „Zukunftsschatz“ (Bürgerfonds, falls beschlossen). Nicht markenrechtlich geprüft. „TrafoDi“ nicht verwendet (siehe Bewertung im Bericht).</li>
    <li><b>Korrektur 61:</b> Die Rechnung v3.47/v3.48 hielt den Anteil der Einkommensteuer fest, obwohl die Stufen am Grundbedarf hängen und dieser langsamer wächst als die
      Einkommen. Mit dieser Wirkung (+{prog60} Punkte 2060) sinkt die Dividende von {div28} (2028) auf {div35} (2035) und {div45} (2045) und bleibt dann bei {div60} (2060) – statt 83 €.
      Lenkung (Erosion), Gesundheit/Pflege und Verteidigungspfad drücken weiter. Bürgerfonds (Hälfte der Lenkungseinnahmen): 2028 {f28}, 2060 {f60a} bis {f60b}.</li>
    <li><b>Automatisierung und Beschäftigung</b> (neu gerechnet, Szenarien): KI {dyn_ki_lo} bis {dyn_ki_hi}, mehr Arbeit {dyn_b}, zusammen mit Verschiebung zum Kapital
      {dyn_mittel} bis {dyn_max} Dividende 2060. Wachstum wirkt vor allem auf die Löhne, nicht auf die Dividende: Sie ist nur ein kleiner Anteil des BIP.</li>
    <li><b>Umgesetzt (Beschluss v3.48):</b> Pflicht, mindestens 80 % der gesparten Arbeitgeberbeiträge in den Lohn zu geben; Renten um die eingesparten Kranken- und
      Pflegebeiträge gekürzt (Annahme 12,35 % wie in Deutschland); Mehrwertsteuer 22 und 28 % zu 25 % zusammengefasst (effektiv {label_eff} statt 17,6 %, Dividende 2028 {div28}).</li>
    <li><b>Rentner verlieren leicht:</b> Mit der Kürzung und der höheren Mehrwertsteuer liegt eine Rente von 1.200 € bei {r1200} im Monat (900 €: {r900}; 2.200 €: {r2200}),
      mit Altlastenzuschlag {r1200z}. Der Text auf der Seite sagt das offen. Prüfen: Ausgleich über einen höheren Grundfreibetrag für Renten oder Kürzung nur um den Krankenanteil.</li>
    <li><b>Verteilung:</b> In Euro gewinnen hohe Einkommen am meisten (150.000 €: {plus150} im Monat), weil der Spitzensatz sinkt und die Beitragsgrenzen wegfallen;
      in Prozent des Nettos liegen die Gewinne näher beieinander. Familien mit einem Einkommen gewinnen weniger, weil die Kinderdividende ({kind28}) unter dem Kindergeld (259 €) liegt.</li>
    <li><b>Altlasten</b> sind Sache der Staaten (Beschluss); der Entwurf bietet den gemeinsamen Fonds als Werkzeug an und nennt ein Rechenbeispiel.</li>
  </ol></div>
</div></header>

<section id="problem"><div class="wrap">
  <p class="kicker alt">Das heutige System:</p>
  <h2>Arbeit trägt die Last. Und sie wird schwerer.</h2>
  <p class="lede">Das heutige System ist Schicht um Schicht gewachsen. Es belastet Arbeit stärker als alles andere – und die Beiträge steigen mit jedem Jahrgang, der in Rente geht.</p>
  <div class="befund-grid">
    <div class="befund"><div class="num">{keil}</div><h3>Abgaben auf einen Durchschnittslohn</h3><p>Deutschland, zweithöchster Wert der OECD. Im OECD-Schnitt sind es {keil_oecd}.</p></div>
    <div class="befund"><div class="num">48,6 %</div><h3>Sozialbeiträge im Jahr 2035</h3><p>So eine Projektion für die Krankenkasse DAK (heute rund 42 %). Rente und Gesundheit treiben den Anstieg.</p></div>
    <div class="befund"><div class="num">{abgeltung}</div><h3>auf Zinsen und Kursgewinne</h3><p>Ein Euro aus Kapital trägt deutlich weniger als ein Euro aus Arbeit.</p></div>
    <div class="befund"><div class="num">0 €</div><h3>Sozialbeiträge auf Maschinen</h3><p>Wer Arbeit durch Automaten ersetzt, spart Abgaben. Die Finanzierung des Sozialstaats hängt an der Arbeit, die weniger wird.</p></div>
  </div>
  <p class="fineprint">Quellen: OECD, Taxing Wages 2025 (Alleinstehende, Durchschnittslohn, 2024); IGES-Institut für DAK-Gesundheit 2024 (Basisszenario, eine Studie;
  berichtet vom Deutschen Ärzteblatt, 25.6.2024); § 32d EStG mit Solidaritätszuschlag.</p>
</div></section>

<section id="konzept"><div class="wrap">
  <p class="kicker neu">Der Bauplan:</p>
  <h2>Wenige Regeln. Eine Grenze: das Goldene Drittel.</h2>
  <p class="lede">Jeder Euro wird gleich behandelt, egal woher er kommt. Was heute über Beiträge, Prämien und Sonderregeln läuft, kommt aus einer Kasse:
  den Steuern. Das macht das System einfach – und gerecht zwischen Arbeit und Kapital.</p>
  <div class="mass-grid">
    <div class="mass"><div class="pos">Einkommen</div><h3>Fünf Stufen, harte Grenze</h3>
      <div class="taxlbl" role="img" aria-label="Stufentarif">
        <div><b class="t1">0 %</b><em>bis {st1} (Grundbedarf)</em></div><div><b class="t2">11 %</b><em>bis {st15}</em></div>
        <div><b class="t3">19 %</b><em>bis {st2}</em></div><div><b class="t4">25 %</b><em>bis {st3}</em></div><div><b class="t5">33 %</b><em>darüber – Obergrenze</em></div></div>
      <p>Besteuert wird das Brutto ohne Abzüge. Der Grundbedarf bleibt frei. Die Stufen hängen am Grundbedarf und wachsen mit ihm.</p></div>
    <div class="mass"><div class="pos">Arbeit</div><h3>Keine Sozialbeiträge</h3><span class="regel">0 % auf den Lohn</span>
      <p>Was Betriebe heute als Beitrag abführen, kann in den Lohn gehen. Dänemark finanziert seinen Sozialstaat fast ganz aus Steuern.</p></div>
    <div class="mass"><div class="pos">Absicherung</div><h3>Das Goldene Netz: versorgt ohne Prämie</h3><span class="regel">Gesundheit · Arbeitslosigkeit · Invalidität · Hinterbliebene</span>
      <p>Jeder ist versorgt, ohne Beitrag, ohne Antrag auf Mitgliedschaft, ohne Sonderfälle. Bezahlt aus den Steuern ({gesundheit} und {seil} der Wirtschaftsleistung).</p></div>
    <div class="mass"><div class="pos">Kapital</div><h3>Kapital wie Arbeit</h3><span class="regel">höchstens 33 % auf alle Erträge</span>
      <p>Auch Veräußerungsgewinne zählen. Lohn in Kapitalertrag umzuwandeln lohnt sich nicht mehr.</p></div>
    <div class="mass"><div class="pos">Erbschaft</div><h3>Geerbtes ist Einkommen</h3><span class="regel">33 % über 100.000 € je Erwerb</span>
      <p>Keine Verschonungsausnahmen. Wer Betrieb oder Haus erbt, kann stunden – niemand muss verkaufen.</p></div>
    <div class="mass"><div class="pos">Konzerne und Plattformen</div><h3>Besteuert, wo die Kunden sind</h3><span class="regel">33 % am Ort der Nutzung</span>
      <p>Gewinne lassen sich verschieben, Kundschaft nicht. Das gilt ausdrücklich für digitale Plattformen.</p></div>
    <div class="mass"><div class="pos">Konsum</div><h3>Die Mehrwertsteuer wird zum Label</h3>
      <div class="vatlbl" role="img" aria-label="Label">
        <div><b class="v1">A+ · 5&nbsp;%</b><em>Grundbedarf, Reparatur</em></div><div><b class="v2">A · 11&nbsp;%</b><em>nachhaltige Güter</em></div>
        <div><b class="v3">B · 17&nbsp;%</b><em>Standardgüter</em></div><div><b class="v4">C · 25&nbsp;%</b><em>ressourcenintensiv, Luxus</em></div><div><b class="v5" style="background:#5b1a14">S · 33&nbsp;%</b><em>Schädliches (Sonderstufe)</em></div></div>
      <p>Man sieht auf einen Blick, was ein Produkt kostet und warum. Die Sonderstufe gilt nur für Tabak, Alkohol, Kraftstoffe und Fahrzeuge mit Verbrennungsmotor: 33 % sind die Ausnahme für Schädliches, nicht die Regel. Im Mittel {label_eff}.</p></div>
    <div class="mass"><div class="pos">Boden · Gemeinde</div><h3>Die Gemeinde besteuert den Boden</h3><span class="regel">0,1–1 % auf den Bodenwert</span>
      <p>Nur der Grundstückswert zählt, nicht das Haus. Wer baut oder saniert, zahlt dafür nicht mehr.</p></div>
    <div class="mass"><div class="pos">Vermögen</div><h3>Große Vermögen tragen mit</h3><span class="regel">1,5 % ab 2 Mio. €</span>
      <p>Darunter bleibt Vermögen unberührt. Darüber greift eine Mindeststeuer, anrechenbar auf die Einkommensteuer.</p></div>
    <div class="mass"><div class="pos">Klima</div><h3>CO₂-Preis, an alle zurück</h3><span class="regel">europäischer Preispfad · Rückgabe über die Dividende</span>
      <p>Wer wenig verbraucht, gewinnt. Die Schweiz gibt ihre CO₂-Abgabe seit Jahren gleichmäßig an alle zurück.</p></div>
    <div class="mass"><div class="pos">Dividende</div><h3>Transformationsdividende: jeden Monat, für alle</h3><span class="regel">2028: {div28} je Erwachsenem · {kind28} je Kind</span>
      <p>Ohne Antrag. Sie gibt vor allem zurück, was Schädliches zahlt – und wird kleiner, wenn das Schädliche verschwindet. Das ist gewollt.</p></div>
    <div class="mass"><div class="pos">Schutz</div><h3>Niemand fällt unter den Grundbedarf</h3><span class="regel">Grundbedarf {st1} im Jahr gesichert</span>
      <p>Wer kein Einkommen hat, wird auf den Grundbedarf aufgestockt; Wohnkosten, Pflege und besondere Lagen trägt ein Härtefallfonds.</p></div>
  </div>
  <p class="fineprint">Beträge in Kaufkraft 2026. Die Sätze und Grenzen sind ein Bauplan: Jeder Staat setzt den Grundbedarf nach seinen Preisen.</p>
</div></section>

<section id="paket"><div class="wrap">
  <h2>Was Du vom System bekommst</h2>
  <p class="lede">Zwei Teile, ein Paket: Das Goldene Netz sichert Dich ab, die Transformationsdividende kommt jeden Monat aufs Konto. Und Du zahlst höchstens das Goldene Drittel.</p>
  <div class="effects">
    <div><h3>Das Goldene Drittel</h3><p>Höchstens ein Drittel auf jeden Euro – aus Arbeit, Kapital, Gewinn oder Erbe. Keine Beiträge, keine Prämien.</p></div>
    <div><h3>Das Goldene Netz · {netz28}</h3><p>Gesundheit und Pflege, Arbeitslosigkeit, Invalidität, Hinterbliebene, Grundbedarf: für jeden, ohne Prämie. Wert je Einwohner im Monat
      (Durchschnitt, 2028); bis 2060 wächst er auf {netz60}.</p></div>
    <div><h3>Die Transformationsdividende · {div28}</h3><p>Jeden Monat für jeden Erwachsenen, Kinder die Hälfte. Sie gibt zurück, was Klimaschutz und Lenkung einbringen,
      und wird kleiner, wenn das Schädliche verschwindet.</p></div>
  </div>
  <p class="fineprint">Kaufkraft 2026, Deutschland. Der Wert des Netzes ist der Durchschnitt der öffentlichen Ausgaben je Einwohner, kein Anspruch in Euro.</p>
</div></section>

<section id="rechner"><div class="wrap">
  <h2>Rechne selbst nach: heute gegen neu</h2>
  <p class="lede">Was bleibt Dir im Monat – heute und im neuen System? Gerechnet mit dem deutschen Recht 2026, in Kaufkraft 2026.</p>
  <div class="calc">
    <div>
      <label class="lbl" for="brutto">Bruttolohn im Jahr</label><div class="bigval" id="bruttoval"></div>
      <input type="range" id="brutto" min="10000" max="150000" step="1000" value="42000">
      <label class="lbl">Haushalt</label>
      <div class="seg klein" id="hh"><button type="button" aria-pressed="true" data-v="alleinstehend">allein</button><button type="button" aria-pressed="false" data-v="alleinerziehend, 1 Kind">allein + 1 Kind</button><button type="button" aria-pressed="false" data-v="Paar, ein Einkommen, 2 Kinder">Paar, 1 Einkommen, 2 Kinder</button></div>
      <label class="lbl">Jahr</label>
      <div class="seg klein" id="rj"><button type="button" aria-pressed="true" data-v="2028">2028</button><button type="button" aria-pressed="false" data-v="2035">2035</button></div>
      <label class="lbl">Gesparte Arbeitgeberbeiträge</label>
      <div class="seg klein" id="wg"><button type="button" aria-pressed="true" data-v="0.8">80 % in den Lohn (Pflicht)</button><button type="button" aria-pressed="false" data-v="1.0">alles in den Lohn</button></div>
      <label class="lbl">Eigene Altersvorsorge</label>
      <div class="seg klein" id="vs"><button type="button" aria-pressed="true" data-v="0.186">so viel wie heute</button><button type="button" aria-pressed="false" data-v="0.0">keine</button></div>
      <label class="lbl">Altlastenzuschlag Deines Staates</label>
      <div class="seg klein" id="zu"><button type="button" aria-pressed="true" data-v="0.0">keiner</button><button type="button" aria-pressed="false" data-v="{zu_v}">Beispiel {zu}</button></div>
    </div>
    <div>
      <p class="vergl"><span class="c"><span class="k">heute netto im Monat</span><span class="v" id="r-h"></span></span><span class="c"><span class="k">neu netto im Monat</span><span class="v new" id="r-n"></span></span></p>
      <div class="plus-box"><div class="plus" id="r-d"></div><div class="sub" id="r-dsub"></div></div>
      <p class="fineprint" style="margin-top:12px">Heute: nach Lohnsteuer, Soli, Sozialbeiträgen, mit Kindergeld; 2035 mit den Beitragssätzen der IGES-Projektion.
      Neu: Einkommensteuer auf Lohn und Dividende, Dividende für alle im Haushalt (Kinder die Hälfte), höhere Mehrwertsteuer im Mittel ({label_eff} statt 16,0 %).
      „So viel wie heute“: der heutige Rentenbeitrag (18,6 %) geht als Sparen in Dein eigenes Vermögen und ist abgezogen. Bürgergeld und Wohngeld sind nicht gerechnet.</p>
    </div>
  </div>
  <div class="effects">
    <div><h3>Rente heute 1.200 € brutto</h3><p>Die Rente sinkt um die Kranken- und Pflegebeiträge, die nicht mehr anfallen; die Versorgung bleibt ohne Prämie.
      Mit der höheren Mehrwertsteuer bleiben {r1200} im Monat (mit Altlastenzuschlag {r1200z}) – ein kleines Minus.</p></div>
    <div><h3>Wer arbeitet, hat mehr</h3><p>Mit der Pflicht zur Weitergabe haben alle gerechneten Einkommensgruppen mehr – auch nach eigener Vorsorge und Altlastenzuschlag ({anteil_voll}).</p></div>
    <div><h3>Mehr, das bleibt</h3><p>Das Mehr kommt nicht aus einer Zahlung, die man streichen kann, sondern aus dem Wegfall der Beiträge. 2035 ist die Dividende kleiner,
      die Beiträge heute wären höher – das Mehr bleibt fast gleich ({plus42_35} bei 42.000 €).</p></div>
  </div>
</div></section>

<section id="anreiz"><div class="wrap">
  <h2>Mehr Arbeit lohnt sich wieder</h2>
  <p class="lede">Von jedem zusätzlichen Euro, den ein Betrieb für Arbeit ausgibt, bleiben heute bei mittleren Löhnen oft weniger als die Hälfte. Neu höchstens ein Drittel weg,
  plus der Mehrwertsteuer beim Ausgeben. Bei 55.000 € brutto: heute {gh55}, neu {gn55}.</p>
  <div class="chart-card">
    <div class="unit">Grenzbelastung: Anteil eines zusätzlichen Euro Arbeitskosten, der nicht im Haushalt ankommt (alleinstehend, 2028)</div>
    @@GRENZ@@
    <div class="legend"><span class="l-ohne"><i></i>heute</span><span class="l-mit"><i></i>neu, 80 % der Beiträge gehen in den Lohn</span><span class="l-prog"><i></i>neu, alles geht in den Lohn</span></div>
  </div>
  <p class="fineprint">Eigene Vorsorge zählt nicht als Belastung: Sie bleibt Dein Eigentum. Wie stark Menschen auf niedrigere Grenzbelastung reagieren, ist in der Forschung umstritten;
  der Grundpfad nimmt keine Mehrarbeit an; Szenarien mit Mehrarbeit stehen im Abschnitt „Bis 2060“.</p>
</div></section>

<section id="zeitpfad"><div class="wrap">
  <h2>Bis 2060: ehrlich gerechnet</h2>
  <p class="lede">Ein Steuersystem muss auch dann tragen, wenn sich die Welt ändert. Drei Entwicklungen sind gut belegt – wir haben sie eingerechnet.</p>
  <div class="trend">
    <div class="land"><div class="n">Verkehr</div><h3>Verbrenner werden Einzelfälle</h3><span class="k">@@TREND_VERKEHR_K@@</span><p>@@TREND_VERKEHR_P@@</p></div>
    <div class="land"><div class="n">Alter</div><h3>Gesundheit und Pflege kosten mehr</h3><span class="k">+{ges_plus} Punkte der Wirtschaftsleistung bis 2060</span><p>@@TREND_ALTER_P@@</p></div>
    <div class="land"><div class="n">Heute</div><h3>Die Beiträge steigen weiter</h3><span class="k">48,6 % im Jahr 2035</span><p>Im heutigen System tragen die Beschäftigten die Alterung über höhere Beiträge.
      Im neuen System trägt sie jeder Euro, nicht nur der Lohn. Der Abstand zugunsten des neuen Systems wächst.</p></div>
  </div>
  <div class="chart-card">
    <div class="unit">Dividende je Erwachsenem und Monat, Kaufkraft 2026</div>
    @@ZEIT@@
    <div class="legend"><span class="l-mit"><i></i>mit den Trends</span><span class="l-prog"><i></i>ohne Trends (alle Anteile fest)</span><span><i style="background:#1D7A4F;opacity:.25;border:none;height:10px"></i>davon aus Lenkungseinnahmen</span></div>
    <p class="fineprint" style="margin-top:12px">Die Dividende gibt vor allem zurück, was Schädliches zahlt ({lenk28} der Wirtschaftsleistung 2028). Wenn Verbrenner und Emissionen verschwinden,
    sinkt dieser Teil – 2060 sind es noch {lenk60}. Dazu kommen die steigenden Kosten für Gesundheit und Pflege. Dagegen wirkt das Wachstum: Wer mehr verdient, rückt
    in höhere Stufen (+{prog60} Punkte der Wirtschaftsleistung 2060). So sinkt die Dividende von {div28} (2028) auf {div35} (2035) und hält sich ab 2045 bei rund {div60}.</p>
  </div>
  <div class="box"><h3>Was das bedeutet</h3>
    <p>Die Transformationsdividende gibt zurück, was der Wandel einbringt – sie wird kleiner, wenn der Schaden kleiner wird. Das Goldene Netz wächst dagegen mit:
    Gesundheit und Pflege für alle, ohne Prämie. Zusammen ist das Paket 2060 mehr wert als 2028 ({paket28} → {paket60} im Monat). Jeder Staat kann einen Teil der
    Lenkungseinnahmen in einen Zukunftsschatz legen, wie Norwegen seine Öleinnahmen: Dann bleibt ein Teil der Dividende auf Dauer.</p></div>
  <div class="trend" style="margin-top:22px">
    <div class="land"><div class="n">Automatisierung</div><h3>Maschinen tragen mit</h3><span class="k">2060: {dyn_ki_lo} bis {dyn_ki_hi} Dividende</span>
      <p>Heute hängt der Sozialstaat am Lohn: Ersetzen Maschinen Arbeit, fehlen Beiträge (−{heute_kap} Punkte, wenn 3 Punkte Einkommen von Arbeit zu Kapital wandern).
      Im neuen System trägt jeder Euro gleich – Gewinne aus Automatisierung zahlen ihr Drittel. Wie stark KI die Produktivität hebt, ist offen: Die Schätzungen reichen
      von 0,07 bis 0,9 Prozentpunkten im Jahr.</p></div>
    <div class="land"><div class="n">Arbeit</div><h3>Billigere Arbeit, mehr Arbeit</h3><span class="k">2060: {dyn_b} Dividende</span>
      <p>Ohne Beiträge sinken die Arbeitskosten, und von jedem zusätzlichen Euro bleibt mehr. Vorsichtig gerechnet steigt das Arbeitsvolumen um 3 bis 5 %.
      Der größte Teil davon kommt als Lohn an, nicht als Dividende.</p></div>
    <div class="land"><div class="n">Zusammen</div><h3>Alles zusammen</h3><span class="k">2060: {dyn_mittel} bis {dyn_max} Dividende</span>
      <p>Mehr Arbeit, KI im mittleren bis hohen Bereich und eine Verschiebung zum Kapital: Die Transformationsdividende bleibt 2060 nahe am heutigen Wert in Kaufkraft.</p></div>
  </div>
</div></section>

<section id="altlasten"><div class="wrap">
  <h2>Altlasten: Jeder Staat findet seinen Weg</h2>
  <p class="lede">Staatsschulden und Rentenzusagen stammen aus dem alten System. Sie sind nicht Teil des Bauplans. Jeder Staat regelt sie selbst –
  eigene, kreative Lösungen sind ausdrücklich erwünscht. Der Bauplan bietet Werkzeuge an.</p>
  <div class="effects">
    <div><h3>Ein gemeinsamer Fonds</h3><p>Staaten können ihre Altlasten in einen gemeinsamen Fonds geben: ein Zins für alle, ein gleichbleibender Beitrag, bis spätestens 2098 getilgt.
      Rechenbeispiel für die zehn gerechneten Staaten mit allen Altrenten (um die eingesparten Beiträge gekürzt): {a_c} % der Wirtschaftsleistung im Jahr, als Zuschlag von {a_zu} auf alle Steuern;
      die Schuld des Fonds steigt bis {a_spj} auf {a_sp} und sinkt dann auf null.</p></div>
    <div><h3>Gute Jahre tilgen</h3><p>Was in einem Jahr über dem Durchschnitt der letzten fünf Jahre hereinkommt, tilgt die Altlast. Schlechte Jahre bleiben ohne Zusatzlast.</p></div>
    <div><h3>Eigene Wege</h3><p>Rücklagen auflösen, Übergänge nach Jahrgängen, eigene Fonds wie in Norwegen, Pflichtvorsorge wie in Australien: Jeder Staat wählt, was zu seiner Lage passt.
      Der Zuschlag steht offen auf jedem Steuerbescheid – und er endet.</p></div>
  </div>
  <p class="fineprint">Zinssatz des Fonds 2,5 %, Wachstum nominal 3 % (Annahmen der Gesamtrechnung). Liegt der Zins beim Wachstum, steigt der Beitrag. Altrenten als Schätzung aus Eurostat (Tabelle 29).</p>
</div></section>

<section id="ebenen"><div class="wrap">
  <h2>Starke Gemeinden, starke Bürger, ein schlankes Dach</h2>
  <p class="lede">Statt fünf Ebenen gibt es zwei. Die Gemeinde erhält den größten Teil des Geldes und entscheidet selbst über ihre Finanzen und über die Weitergabe an andere Verwaltungen.
  Ein gemeinsames europäisches Dach übernimmt, was nur gemeinsam geht.</p>
  <div class="effects">
    <div><h3>Dir wird zugetraut,</h3><p>mit Deinem Geld umzugehen: mehr Netto, eine einfache Steuer, eigene Vorsorge, die Dir gehört.</p></div>
    <div><h3>Der Gemeinde wird zugetraut,</h3><p>ihre Angelegenheiten zu führen: feste Beträge je Einwohner und je Kind, nach derselben Regel in jedem Land.</p></div>
    <div><h3>Dem Dach wird zugetraut,</h3><p>was nur gemeinsam geht: Verteidigung, digitale Souveränität, Binnenmarkt. Mit Obergrenze: Es behält höchstens {og} dessen, was es einzieht.</p></div>
  </div>
</div></section>

<section id="vorbilder"><div class="wrap">
  <h2>Das Beste aus vielen Vorbildern</h2>
  <p class="lede">Nichts an diesem Bauplan ist ein Experiment ins Blaue. Jeder Baustein läuft heute schon irgendwo. Neu ist, dass sie zusammenpassen – und dass jeder Staat sie übernehmen kann.</p>
  <div class="reg-grid" style="grid-template-columns:repeat(auto-fit,minmax(290px,1fr))">
    <div class="land"><div class="n">Dänemark</div><h3>Sozialstaat aus Steuern</h3><span class="k">Sozialbeiträge 0,7 % der Wirtschaftsleistung</span><p>Gemeinden tragen Schulen, Pflege und Soziales. Beiträge spielen kaum eine Rolle.</p></div>
    <div class="land"><div class="n">Estland</div><h3>Einfach und digital</h3><span class="k">ein Einkommensteuersatz · Bodensteuer seit 1993</span><p>Die Steuererklärung ist in Minuten online erledigt. Die Grundsteuer bemisst sich allein am Bodenwert.</p></div>
    <div class="land"><div class="n">Neuseeland</div><h3>Eine Mehrwertsteuer ohne Ausnahmen</h3><span class="k">ein Satz, breite Basis</span><p>Wenige Ausnahmen machen die Steuer einfach und ergiebig. Das Label übernimmt die Einfachheit und ergänzt die Lenkung.</p></div>
    <div class="land"><div class="n">Schweiz</div><h3>CO₂-Abgabe an alle zurück</h3><span class="k">gleicher Betrag für jeden</span><p>Die Einnahmen gehen gleichmäßig an alle Einwohner zurück. Gemeinden setzen ihre Steuern selbst.</p></div>
    <div class="land"><div class="n">Alaska · Norwegen</div><h3>Eine Dividende, ein Fonds</h3><span class="k">Dividende seit 1982 · Ausgaberegel 3 %</span><p>Alaska zahlt jedem Einwohner einen Anteil am gemeinsamen Fonds. Norwegen legt vergängliche Einnahmen an und verbraucht nur den Ertrag.</p></div>
    <div class="land"><div class="n">Australien</div><h3>Vorsorge, die einem gehört</h3><span class="k">Pflichtsparen 12 % auf eigenem Konto</span><p>Ein Beispiel, wie ein Staat Eigenverantwortung mit Sicherheit verbindet. Ob und wie: Sache jedes Staates.</p></div>
  </div>
</div></section>

<section id="grenzen"><div class="wrap">
  <h2>Was wir noch nicht wissen</h2>
  <p class="lede">Ein Entwurf, dessen Annahmen offen liegen, lässt sich prüfen. Diese Punkte entscheiden mit über das Ergebnis:</p>
  <ul class="grenzen">
    <li><b>Weitergabe der Arbeitgeberbeiträge:</b> Mindestens 80 % der gesparten Beiträge müssen in den Lohn gehen. Wie sich die Pflicht durchsetzen lässt (Tarifverträge, Übergangsregel, Kontrolle), ist auszuarbeiten. Vorgeschrieben sind mindestens 80 %; bei voller Weitergabe wäre das Mehr größer ({plus42k} statt {plus42} bei 42.000 €).</li>
    <li><b>Deckung:</b> Das Aufkommen ist auf deutscher Basis gerechnet und auf die zehn Staaten übertragen; Ausweichreaktionen sind nicht eingerechnet.</li>
    <li><b>Trends:</b> Die Pfade für Verkehr, CO₂ und Gesundheit sind aus Quellen gesetzt, keine eigene Prognose.</li>
    <li><b>Grundbedarf:</b> Der Härtefallfonds ist mit 0,65 % der Wirtschaftsleistung angesetzt (Annahme); mit kleinerer Dividende wird er größer.</li>
    <li><b>Altlasten:</b> Die Zahlen zum Fonds sind ein Beispiel. Jeder Staat entscheidet selbst.</li>
  </ul>
</div></section>

<section id="offen"><div class="wrap">
  <h2>Offen entwickelt – mach mit</h2>
  <p class="lede">Der Bauplan wird unabhängig von Parteien und Interessengruppen entwickelt. Jede Zahl stammt aus amtlichen Statistiken oder ist als Annahme gekennzeichnet; jede Rechnung lässt sich nachvollziehen.</p>
</div></section>

<footer><div class="wrap">
  <div><h4>Methodik</h4><p>Prüfrechnungen modell/systemvarianten.py (System 33F), modell/haushalte33.py, modell/projektion33.py, modell/altlasten.py auf Grundlage der offenen Gesamtrechnung (Eurostat, OECD, Kernmodell mit dem Recht 2026).</p>
    <p class="verstamp">Modellstand <b>{version}</b></p></div>
  <div><h4>Kontakt</h4><p>Initiative 28 : 28<br><a href="#top">Nach oben</a></p></div>
  <div><h4>Impressum und Datenschutz</h4><p>@@IMPRESSUM@@</p></div>
</div></footer>

<script>
const R=@@RASTER@@;
const $=id=>document.getElementById(id);
const zahl=x=>Math.round(Math.abs(x)).toString().replace(/\B(?=(\d{3})+(?!\d))/g,'.');
const eur=x=>(x<0?'−':'')+zahl(x)+' €';
function seg(id,cb){const el=$(id);el.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
  el.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));cb();});}
const val=id=>$(id).querySelector('[aria-pressed=true]').dataset.v;
function rechner(){const br=+$('brutto').value,i=R.brutto.indexOf(br),j=val('rj'),h=val('hh');
  const heute=R.heute[j+'|'+h][i],neu=R.neu[[j,h,val('wg'),val('zu'),val('vs')].join('|')][i],d=neu-heute;
  $('bruttoval').textContent=eur(br);$('r-h').textContent=eur(heute);$('r-n').textContent=eur(neu);
  const p=$('r-d');p.textContent=(d>=0?'+':'−')+zahl(d)+' € im Monat';p.classList.toggle('neg',d<0);
  $('r-dsub').textContent=(d>=0?'mehr':'weniger')+' als heute, '+eur(d*12)+' im Jahr';}
$('brutto').addEventListener('input',rechner);['hh','rj','wg','vs','zu'].forEach(x=>seg(x,rechner));rechner();
</script>
</body></html>"""


def main():
    w = werte()
    trend = lade_trends()
    tx = SEITE
    for k, v in w.items():
        tx = tx.replace("{" + k + "}", v)
    ersetz = {"CSS": SB.stylesheet() + SB.ZUSATZ_CSS + CSS33, "GRENZ": grafik_grenz(), "ZEIT": grafik_zeit(),
              "RASTER": json.dumps({k: RA[k] for k in ("brutto", "heute", "neu")}, separators=(",", ":")),
              "IMPRESSUM": json.loads((Path(__file__).resolve().parent / "sprachen" / "de.json").read_text(encoding="utf-8"))["fuss_imp_p"],
              **trend}
    html = re.sub(r"@@([A-Z_]+)@@", lambda m: ersetz[m.group(1)], tx)
    offen = re.findall(r"\{[a-z_0-9]+\}", re.sub(r"<script>.*?</script>", "", html, flags=re.S))
    if offen:
        raise SystemExit(f"nicht ersetzt: {sorted(set(offen))}")
    ZIEL.mkdir(parents=True, exist_ok=True)
    (ZIEL / "de.html").write_text(html, encoding="utf-8")
    print(f"geschrieben: {(ZIEL / 'de.html').relative_to(WURZEL)} ({len(html)} Zeichen)")


def lade_trends():
    """Texte der Trendkarten; Zahlen und Quellen aus projektion33.json (Feld 'quellen'), sonst vorläufiger Text."""
    q = PJ.get("texte", {})
    return {"TREND_VERKEHR_K": q.get("verkehr_k", "EU: ab 2035 kaum noch neue Verbrenner"),
            "TREND_VERKEHR_P": q.get("verkehr_p", "Neuwagen werden elektrisch; der Bestand folgt mit einigen Jahren Abstand. Kraftstoffe und Verbrennerfahrzeuge "
                                                  "zahlen im Label 33 % – diese Einnahmen sinken mit dem Erfolg."),
            "TREND_ALTER_P": q.get("alter_p", "Mehr ältere Menschen brauchen mehr Versorgung. Wir rechnen mit dem Referenzszenario der EU-Kommission (Ageing Report 2024).")}


if __name__ == "__main__":
    main()
