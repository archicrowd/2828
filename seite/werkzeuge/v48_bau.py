"""Bausteine der Webseite v4.8 (Logbuch v4.8): Regelwerte aus dem Modell, Gini-Grafik, Tabelle „Mehr Sicherheit und mehr Freiheit“,
Rechner mit Kinderanteil 0,8, Boden (Halbanrechnung) und heutigen Bedarfsleistungen. Wird von drittel_bau.py geladen.
"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
AGG = WURZEL / "daten" / "aggregate"
spec = importlib.util.spec_from_file_location("rb", WURZEL / "modell" / "regel_boden.py")
RB = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(RB)
SL = RB.SL
RBJ = json.loads((AGG / "regel_boden.json").read_text(encoding="utf-8"))
GINI = json.loads((AGG / "gini.json").read_text(encoding="utf-8"))
TOPF = RB.topf(RB.S)
S_KIND = RB.S
KW = RB.P["skala"]["kind"]
ANR = RB.P["anrechnung"]
LAENDER = ("DE", "FR", "IT", "ES", "PL")


def anteil(c):
    """Anteil der Beschäftigten mit mehr (Regel Boden, heute mit Bedarfsleistungen): min und max über die Haushaltstypen."""
    a = RBJ["staaten"][c]["anteil"].values()
    return min(a), max(a)


def plus_monat(c, brutto):
    return (RB.neu(c, brutto, 1, 0) - SL.heute(c, brutto, 1, 0)) / 12


def heute_mit_bedarf(c, brutto, heute, e, k):
    z = SL.ZUSATZ.get(c)
    return [round(h + (z(b, e, k, h) if z else 0.0), 1) for b, h in zip(brutto, heute)]


def rechner_felder(c, f=1.0):
    """Zusatzfelder für den Rechner: Kinderanteil, Topf, Boden (Jahresbetrag in Landeswährung × f), Kindergewicht, Anrechnung."""
    gb = SL.HL.LS["staaten"][c]["grundbedarf_jahr_eur"] * SL.HL.faktor(c) * f
    return dict(s=S_KIND, topf=round(TOPF, 5), gb=round(gb, 2), kw=KW, anr=ANR)


def gini_svg(name, ref, l1, l2, l3, lref, unit):
    """Waagrechte Balken: heute (amtlich 2025), 2028 und 2060 (Modell, Mitte) je Land; DK und SE zum Vergleich."""
    zeilen = []
    for c in LAENDER:
        x = GINI["staaten"][c]
        r = {z["jahr"]: z["mitte"] for z in x["reihe"]}
        zeilen.append((c, [(x["gini_amtlich_2025"], "#9AA9B6"), (r[2028], "#1D7A4F"), (r[2060], "#8FB8A0")]))
    for c, v in GINI["vergleich_amtlich_2025"].items():
        zeilen.append((c, [(v, "#C9D3DB")]))
    x0, x1, vmax = 170, 860, 35.0
    sx = lambda v: x0 + (x1 - x0) * v / vmax
    y, teile = 30, []
    for g in range(0, 36, 5):
        teile.append(f'<line x1="{sx(g):.1f}" y1="18" x2="{sx(g):.1f}" y2="@@H@@" stroke="#E3E8EC"/>'
                     f'<text x="{sx(g):.1f}" y="12" text-anchor="middle" font-family="IBM Plex Mono,monospace" font-size="10" fill="#5A7186">{g}</text>')
    for c, balken in zeilen:
        fett = ' font-weight="700"' if c == ref else ""
        zusatz = f" · {lref}" if len(balken) == 1 else ""
        h = 12 * len(balken) + 4 * (len(balken) - 1)
        teile.append(f'<text x="{x0 - 10}" y="{y + h / 2 + 4:.1f}" text-anchor="end" font-family="Inter,sans-serif" font-size="13" fill="#0F3B5C"{fett}>{name[c]}</text>')
        if zusatz:
            teile.append(f'<text x="{x0 - 10}" y="{y + h / 2 + 17:.1f}" text-anchor="end" font-family="IBM Plex Mono,monospace" font-size="9" fill="#5A7186">{lref}</text>')
        for v, farbe in balken:
            teile.append(f'<rect x="{x0}" y="{y}" width="{sx(v) - x0:.1f}" height="12" fill="{farbe}"/>'
                         f'<text x="{sx(v) + 6:.1f}" y="{y + 10}" font-family="IBM Plex Mono,monospace" font-size="10" fill="#0F3B5C">{str(v).replace(".", "@@DEZ@@")}</text>')
            y += 16
        y += 14 + (8 if zusatz else 0)
    hoehe = y + 6
    leg = "".join(f'<span><b style="background:{f};display:inline-block;width:12px;height:12px;margin-right:6px;vertical-align:-1px"></b>{t}</span>'
                  for t, f in ((l1, "#9AA9B6"), (l2, "#1D7A4F"), (l3, "#8FB8A0")))
    svg = (f'<div class="giniwrap"><svg viewBox="0 0 900 {hoehe}" role="img" aria-label="{unit}" style="width:100%;height:auto">'
           + "".join(teile).replace("@@H@@", str(hoehe - 4)) + "</svg></div>")
    return svg, f'<div class="legend" style="display:flex;gap:18px;flex-wrap:wrap">{leg}</div>'


def bess_tab(sp, c, T, eur, pct):
    lb = RBJ["staaten"][c]["lohnabstand"]["alleinstehend"]
    bel = lb["belastung_zusatzeuro_bei_halbem_mindestlohn"]
    g = GINI["staaten"][c]
    g28 = next(z["mitte"] for z in g["reihe"] if z["jahr"] == 2028)
    zahl = lambda v: str(v).replace(".", "," if sp != "en" else ".")
    besser = [lb["0.5"]["neu"] >= lb["0.5"]["heute"], bel["neu"] <= bel["heute"], g28 <= g["gini_amtlich_2025"], True]
    reihen = [(T["bess_r1"], eur(lb["0.5"]["heute"]), eur(lb["0.5"]["neu"])),
              (T["bess_r2"], pct(100 - bel["heute"]), pct(100 - bel["neu"])),
              (T["bess_r3"], zahl(g["gini_amtlich_2025"]), zahl(g28)),
              (T["bess_r4"], T["bess_r4a"], T["bess_r4b"])]
    kopf = f'<div class="bk"><span>{T["bess_k0"]}</span><span>{T["bess_k1"]}</span><span>{T["bess_k2"]}</span></div>'
    zeilen = "".join(f'<div class="br"><span>{a}</span><span>{b}</span><span class="neu">{"" if ok else "@@X"}{n}</span></div>' for (a, b, n), ok in zip(reihen, besser)).replace('class="neu">@@X', 'class="schlechter">')
    return f'<div class="bess">{kopf}{zeilen}</div>'


CSS = ("details.mehr>summary{cursor:pointer;font-family:'IBM Plex Mono',monospace;font-size:13px;color:#1D7A4F;margin:18px 0}"
       ".bess{margin:18px 0 8px}.bess .bk,.bess .br{display:grid;grid-template-columns:46% 1fr 1fr;gap:12px;border-bottom:1px solid #D6DEE5;padding:10px 4px}"
       ".bess .bk span{font-family:'IBM Plex Mono',monospace;font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:#5A7186}"
       ".bess span+span{text-align:right}.bess .br span{font-size:15px;color:#0F3B5C}.bess .br span+span{font-family:'IBM Plex Mono',monospace;font-size:14px;color:#33475B}"
       ".bess .br span.neu{color:#1D7A4F;font-weight:600}.bess .br span.schlechter{color:#A33A2B;font-weight:600}"
       "@media(max-width:640px){.bess .bk,.bess .br{grid-template-columns:1fr 1fr;gap:4px 12px}.bess .bk span:first-child,.bess .br span:first-child{grid-column:1/-1}}"
       ".giniwrap{overflow-x:auto}.giniwrap svg{min-width:620px}")
