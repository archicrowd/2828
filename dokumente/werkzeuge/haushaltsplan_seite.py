#!/usr/bin/env python3
"""Seite „Haushaltsplan Deutschland“ aus daten/aggregate/haushaltsplan_de.json (Logbuch v4.94). Darstellung, keine Rechnung.

Aufruf: python3 dokumente/werkzeuge/haushaltsplan_seite.py <ausgabe.html>
Die Seite enthält die interne Spalte „belegt“ (Prüfbefund B-1); sie gehört nicht auf die öffentliche Webseite (Beschluss 15.11.2026).
"""
import html
import json
import sys
from pathlib import Path

W = Path(__file__).resolve().parents[2]
D = json.loads((W / "daten" / "aggregate" / "haushaltsplan_de.json").read_text(encoding="utf-8"))


def f(x, n=2):
    if x is None:
        return "–"
    s = f"{x:,.{n}f}".replace(",", " ").replace(".", ",").replace(" ", ".")
    return s


def tabelle(zeilen, titel_heute):
    out, gruppe, sh, sn = [], None, 0.0, 0.0
    for z in zeilen:
        if z["gruppe"] != gruppe:
            gruppe = z["gruppe"]
            out.append(f'<tr class="grp"><th colspan="7" scope="colgroup">{html.escape(gruppe)}</th></tr>')
        sh += z["heute_pct_bip"] or 0
        sn += z["nachher_pct_bip"] or 0
        neu = f'<span class="neu">{html.escape(z["nachher_position"])}</span>' if z.get("nachher_position") else ""
        bel = z.get("belegt_pct_bip")
        belc = f'<td class="num bel">{f(bel)}</td>' if bel is not None else '<td class="num bel leer">–</td>'
        out.append(
            "<tr>"
            f'<th scope="row">{html.escape(z["position"])}{neu}</th>'
            f'<td class="num">{f(z["heute_mrd_2024"], 1)}</td><td class="num">{f(z["heute_pct_bip"])}</td>'
            f'<td class="num stark">{f(z["nachher_pct_bip"])}</td><td class="num">{f(z["nachher_mrd_2028"], 1)}</td>{belc}'
            f'<td class="txt">{html.escape(z["einfluss"])}</td></tr>')
    out.append(f'<tr class="summe"><th scope="row">Summe</th><td></td><td class="num">{f(sh)}</td><td class="num stark">{f(sn)}</td>'
               f'<td class="num">{f(sn * 4914.9 / 100, 1)}</td><td></td><td></td></tr>')
    kopf = ('<thead><tr><th scope="col">Position heute (nachher)</th><th scope="col" class="num">Heute<br>Mrd. € 2024</th>'
            '<th scope="col" class="num">Heute<br>% BIP</th><th scope="col" class="num">Drittel 2028<br>% BIP</th>'
            '<th scope="col" class="num">Drittel 2028<br>Mrd. €</th><th scope="col" class="num">belegt<br>(intern)</th>'
            '<th scope="col">Einfluss der neuen Regeln</th></tr></thead>')
    return f'<div class="tw"><table>{kopf}<tbody>{"".join(out)}</tbody></table></div>'


def fonds_tabelle():
    S, F = D["summen"], D["fondskonto"]
    z = [("Heute 2024", "Finanzierungssaldo Gesamtstaat (Aufkommen − Ausgaben)", S["finanzierungssaldo_heute_pct"], "gedeckt durch neue Kredite (Finanzierung, keine Einnahme)"),
         ("Nachher 2028", "Saldo Landeshaushalt (Aufkommen − Ausgaben)", S["saldo_nachher_pct"], "ausgeglichen; keine neuen Kredite des Landes")]
    z += [("Fonds 2028", "Einnahme: " + x["position"], x["pct_bip"], x["art"]) for x in F["einnahmen"]]
    z += [("Fonds 2028", "Ausgabe: " + x["position"], -x["pct_bip"], x["art"]) for x in F["ausgaben"]]
    z += [("Fonds 2028", "Finanzierung: " + x["position"], x["pct_bip"], x["art"]) for x in F["finanzierung"]]
    rows = "".join(f'<tr><td>{html.escape(a)}</td><th scope="row">{html.escape(b)}</th><td class="num stark">{f(c)}</td><td class="txt">{html.escape(d)}</td></tr>' for a, b, c, d in z)
    return ('<div class="tw"><table class="schmal"><thead><tr><th scope="col">Konto</th><th scope="col">Position</th><th scope="col" class="num">% BIP</th>'
            f'<th scope="col">Art</th></tr></thead><tbody>{rows}</tbody></table></div>'
            '<p class="hinweis">Konsolidiert (ohne den Beitrag, der nur vom Landeshaushalt in den Fonds fließt): Ausgaben 2028 '
            f'{f(S["ausgaben_konsolidiert_nachher_pct"])} % BIP, davon Landeshaushalt {f(S["ausgaben_nachher_pct"] - F["einnahmen"][0]["pct_bip"])} und Fonds {f(S["fonds_ausgaben_pct"])}.</p>')


def pruef_tabelle():
    rows = "".join(f'<tr><th scope="row">{html.escape(a)}</th><td>{html.escape(b)}</td><td>{html.escape(c)}</td><td class="txt">{html.escape(d)}</td></tr>' for a, b, c, d in D["pruefung"])
    return ('<div class="tw"><table class="schmal"><thead><tr><th scope="col">Position</th><th scope="col">Art</th><th scope="col">Konto</th>'
            f'<th scope="col">Befund</th></tr></thead><tbody>{rows}</tbody></table></div>')


E, A = D["einnahmen"], D["ausgaben"]
g = lambda L, s: next(x for x in L if x["position"].startswith(s))
sozial = sum(x["heute_pct_bip"] for x in E if x["gruppe"] == "Sozialbeiträge")
vorher = dict(
    quellen=[["Einkommensteuern", g(E, "Lohn")["heute_pct_bip"]], ["Gewinnsteuern", g(E, "Körperschaft")["heute_pct_bip"]],
             ["Mehrwertsteuer", g(E, "Mehrwert")["heute_pct_bip"]], ["Verbrauch- und übrige Steuern", g(E, "Verbrauch")["heute_pct_bip"]],
             ["Emissionshandel", g(E, "Emission")["heute_pct_bip"]], ["Grund- und Erbschaftsteuer", g(E, "Grundsteuer")["heute_pct_bip"] + g(E, "Erbschaft")["heute_pct_bip"]],
             ["Sozialbeiträge", round(sozial, 2)], ["Gebühren, Erträge, Transfers", g(E, "Verkäufe")["heute_pct_bip"]], ["Finanzierung: neue Kredite", -D["summen"]["finanzierungssaldo_heute_pct"]]],
    mitte=["Gesamtstaat 2024"],
    ziele=[["Renten, Pensionen, Hinterbliebene", g(A, "Alter")["heute_pct_bip"]], ["Gesundheit", g(A, "Gesundheit")["heute_pct_bip"]],
           ["Familie, Wohnen, Grundsicherung", g(A, "Familie")["heute_pct_bip"]], ["Krankheit, Pflege, Invalidität", g(A, "Krankheit")["heute_pct_bip"]],
           ["Arbeitslosigkeit", g(A, "Arbeitslos")["heute_pct_bip"]], ["Bildung und Forschung", g(A, "Schulen")["heute_pct_bip"] + g(A, "Hochschulen")["heute_pct_bip"]],
           ["Wirtschaft und Verkehr", g(A, "Wirtschaft")["heute_pct_bip"]], ["Verwaltung, Außen", g(A, "Allgemeine")["heute_pct_bip"]],
           ["Sicherheit und Verteidigung", g(A, "Verteidigung")["heute_pct_bip"] + g(A, "Öffentliche")["heute_pct_bip"]],
           ["Zinsen", g(A, "Zinsen")["heute_pct_bip"]],
           ["Umwelt, Wohnen, Kultur", g(A, "Umwelt")["heute_pct_bip"] + g(A, "Wohnen")["heute_pct_bip"] + g(A, "Freizeit")["heute_pct_bip"]]])
np_ = lambda s: next(x["nachher_pct_bip"] for x in E + A if (x.get("nachher_position") or x["position"]).startswith(s))
nachher = dict(
    steuern=[["Einkommen", np_("Einkommen")], ["Konsum (Label)", np_("Konsum")], ["Unternehmen und Plattformen", np_("Unternehmen")],
             ["Übrige Steuern", np_("Übrige")], ["CO₂-Preis", np_("CO₂")], ["Kapitalerträge", np_("Kapital")], ["Erbschaften", np_("Erbschaften")],
             ["Große Vermögen", np_("Große")], ["Grundstücksabgabe", np_("Grundstück")], ["Subventionsabbau", np_("Subvention")],
             ["Progression", np_("Progression")]],
    zuschlag=[["Altlastenzuschlag", np_("Altlastenzuschlag")]],
    ziele_steuern=[["Dividende", np_("Dividende")], ["Netz: Gesundheit", np_("Gesundheit")],
                   ["Netz: Pflege, Invalidität, Arbeit, Härtefall", round(g(A, "Krankheit")["nachher_pct_bip"] + g(A, "Arbeitslos")["nachher_pct_bip"] + g(A, "Familie")["nachher_pct_bip"], 2)],
                   ["Gemeinden: Schulen", g(A, "Schulen")["nachher_pct_bip"]],
                   ["Gemeinden: Verwaltung, Verkehr, Kultur u. a.", 6.65],
                   ["Dach: Wirtschaftsraum", 2.10], ["Dach: Forschung, Hochschulen", g(A, "Hochschulen")["nachher_pct_bip"]],
                   ["Dach: Verteidigung", g(A, "Verteidigung")["nachher_pct_bip"]], ["Dach: Außen, Standards, Polizei, Umwelt", 1.18],
                   ["Beitrag an den Gemeinschaftsfonds", np_("Beitrag an den Fonds")]],
    fonds_ein=[[x["position"], x["pct_bip"]] for x in D["fondskonto"]["einnahmen"]] + [[x["position"], x["pct_bip"]] for x in D["fondskonto"]["finanzierung"]],
    fonds_aus=[[x["position"], x["pct_bip"]] for x in D["fondskonto"]["ausgaben"]])
st = round(sum(v for _, v in nachher["steuern"] + nachher["zuschlag"]), 2)
nachher["saldo"] = round(st - sum(v for _, v in nachher["ziele_steuern"]), 2)
pf = D["dividendenpfad"]
de = D["dividende_eur"]
bel60 = D["dividende_pct_belegt_mittel"]["2060"]
daten = dict(vorher=vorher, nachher=nachher, pfad=pf, eur=de, belegt60=bel60)

seite = f"""<title>Haushaltsplan Deutschland</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;650;750&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: Haushaltsplan als Einzelplan – Kopf, zwei Flussbilder (heute / Drittel), Pfad der Dividende, dann die Titel als Tabelle */
:root {{
  --bg: #f6f7f8; --paper: #ffffff; --ink: #1d2733; --muted: #5d6b79; --rule: #d6dce2;
  --ein: #1f6f78; --fonds: #6a4c93; --kredit: #8a8f96; --aus: #b5651d; --div: #2e7d32; --warn: #a83232;
  --f-head: "Archivo", "Helvetica Neue", Arial, sans-serif; --f-body: "Source Sans 3", "Segoe UI", Arial, sans-serif; --f-num: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #12171d; --paper: #1a2129; --ink: #e5eaef; --muted: #9aa8b5; --rule: #2e3944;
  --ein: #4fb3bd; --fonds: #a98bd6; --kredit: #8d949c; --aus: #e0954f; --div: #6cc070; --warn: #e37b7b; color-scheme: dark }} }}
:root[data-theme="dark"] {{
  --bg: #12171d; --paper: #1a2129; --ink: #e5eaef; --muted: #9aa8b5; --rule: #2e3944;
  --ein: #4fb3bd; --fonds: #a98bd6; --kredit: #8d949c; --aus: #e0954f; --div: #6cc070; --warn: #e37b7b; color-scheme: dark }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--f-body); font-size: 16px; line-height: 1.5; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding-block: 28px 64px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 36px; }}
header {{ display: grid; gap: 8px; }}
.eyebrow {{ font-family: var(--f-num); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }}
h1 {{ font-family: var(--f-head); font-weight: 750; font-size: clamp(28px, 4vw, 40px); line-height: 1.1; margin: 0; text-wrap: balance; }}
h2 {{ font-family: var(--f-head); font-weight: 650; font-size: 22px; margin: 0; text-wrap: balance; }}
p {{ margin: 0; max-width: 70ch; }}
.lede {{ color: var(--muted); font-size: 17px; }}
section {{ display: grid; gap: 14px; min-width: 0; }}
.kennz {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.kz {{ background: var(--paper); border: 1px solid var(--rule); border-radius: 6px; padding: 12px 14px; display: grid; gap: 2px; min-width: 150px; flex: 1 1 160px; }}
.kz b {{ font-family: var(--f-num); font-weight: 500; font-size: 22px; font-variant-numeric: tabular-nums; }}
.kz span {{ font-size: 13px; color: var(--muted); }}
.sankeys {{ display: grid; grid-template-columns: 1fr; gap: 24px; }}
.sk {{ background: var(--paper); border: 1px solid var(--rule); border-radius: 6px; padding: 14px; display: grid; gap: 8px; min-width: 0; }}
.sk h3 {{ font-family: var(--f-head); font-weight: 650; font-size: 16px; margin: 0; }}
.sk .sv {{ overflow-x: auto; }}
.sk svg {{ display: block; }}
.sk text {{ fill: var(--ink); font-family: var(--f-body); font-size: 12px; }}
.sk text.w {{ fill: var(--muted); font-family: var(--f-num); font-size: 11px; }}
.legende {{ display: flex; flex-wrap: wrap; gap: 14px; font-size: 13px; color: var(--muted); }}
.legende i {{ display: inline-block; width: 12px; height: 12px; border-radius: 2px; margin-right: 6px; vertical-align: -1px; }}
.tw {{ overflow-x: auto; background: var(--paper); border: 1px solid var(--rule); border-radius: 6px; }}
table {{ border-collapse: collapse; width: 100%; min-width: 980px; font-size: 14px; }}
table.schmal {{ min-width: 720px; }}
th, td {{ padding: 7px 10px; border-bottom: 1px solid var(--rule); vertical-align: top; text-align: left; }}
thead th {{ font-family: var(--f-head); font-weight: 650; font-size: 13px; background: var(--paper); position: sticky; top: 0; }}
tbody th {{ font-weight: 600; max-width: 330px; }}
.num {{ text-align: right; font-family: var(--f-num); font-variant-numeric: tabular-nums; white-space: nowrap; }}
.stark {{ font-weight: 500; color: var(--ein); }}
.bel {{ color: var(--warn); }} .leer {{ color: var(--muted); }}
.txt {{ color: var(--muted); font-size: 13px; max-width: 420px; }}
.neu {{ display: block; font-weight: 400; font-size: 12px; color: var(--ein); font-family: var(--f-num); }}
tr.grp th {{ background: var(--bg); font-family: var(--f-num); font-weight: 500; font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }}
tr.summe th, tr.summe td {{ border-top: 2px solid var(--ink); font-weight: 600; }}
.hinweis {{ font-size: 13px; color: var(--muted); display: grid; gap: 6px; max-width: 90ch; }}
.pfad svg text {{ fill: var(--ink); font-family: var(--f-body); font-size: 12px; }}
.pfad svg text.w {{ font-family: var(--f-num); font-size: 11px; }}
.pfad {{ background: var(--paper); border: 1px solid var(--rule); border-radius: 6px; padding: 14px; overflow-x: auto; }}
.marke {{ font-family: var(--f-num); font-size: 11px; border: 1px solid var(--warn); color: var(--warn); border-radius: 3px; padding: 1px 6px; }}
a {{ color: var(--ein); }}
a:focus-visible {{ outline: 2px solid var(--ein); outline-offset: 2px; }}
@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>
<div class="wrap">
<header>
  <div class="eyebrow">Initiative 28:28 · Modellstand {html.escape(D["version"])} · Prüfrechnung, Spalte „belegt“ intern</div>
  <h1>Haushaltsplan Deutschland: heute und im Goldenen Drittel</h1>
  <p class="lede">Gesamtstaat mit Bund, Ländern, Gemeinden und Sozialversicherung. Heute: Ist 2024 (Eurostat). Nachher: geltende Rechnung 2028.
  Alle Anteile in % des BIP, Euro nominal im jeweiligen Jahr.</p>
</header>
<div class="kennz">
  <div class="kz"><b>{f(D["summen"]["aufkommen_heute_pct"],1)} / {f(D["summen"]["ausgaben_heute_pct"],1)} %</b><span>Heute 2024: Aufkommen / Ausgaben; Lücke {f(-D["summen"]["finanzierungssaldo_heute_pct"],1)} über Kredite</span></div>
  <div class="kz"><b>{f(D["summen"]["aufkommen_nachher_pct"],1)} / {f(D["summen"]["ausgaben_nachher_pct"],1)} %</b><span>Landeshaushalt 2028: Aufkommen / Ausgaben (mit Beitrag an den Fonds); Saldo +{f(D["summen"]["saldo_nachher_pct"])}</span></div>
  <div class="kz"><b>{f(D["summen"]["fonds_ausgaben_pct"],1)} %</b><span>Gemeinschaftsfonds, Anteil DE: Altrenten und Zinsen; davon {f(D["summen"]["fonds_kredite_pct"],1)} über Fondskredite</span></div>
  <div class="kz"><b>{de["geltend"]["2028"]} €</b><span>Dividende je Erwachsenem und Monat 2028 (Kaufkraft 2026); belegt {de["belegt_mittel"]["2028"]} €</span></div>
</div>
<section>
  <h2>Wie das Geld fließt</h2>
  <p>Alle Bilder im selben Maßstab: Die Breite eines Bandes ist sein Anteil am BIP. Links steht das Aufkommen, grau die Finanzierung über Kredite;
  Kredite sind keine Einnahme. Nachher gibt es zwei Konten: den Landeshaushalt und den Gemeinschaftsfonds, in den Deutschland seinen Beitrag zahlt.
  Die private Pflichtvorsorge (4,1 % BIP, eigenes Konto) ist nicht enthalten.</p>
  <div class="sankeys">
    <div class="sk"><h3>Heute, 2024: Gesamtstaat mit Sozialversicherung</h3><div class="sv" id="sk-vorher"></div></div>
    <div class="sk"><h3>Goldenes Drittel 2028: Landeshaushalt Deutschland</h3><div class="sv" id="sk-nachher"></div></div>
    <div class="sk"><h3>Goldenes Drittel 2028: Gemeinschaftsfonds, Anteil Deutschland</h3><div class="sv" id="sk-fonds"></div></div>
  </div>
  <div class="legende"><span><i style="background:var(--ein)"></i>Steuern</span><span><i style="background:var(--aus)"></i>Sozialbeiträge</span>
  <span><i style="background:var(--fonds)"></i>Fonds (Altlasten)</span><span><i style="background:var(--kredit)"></i>Gebühren; Kredite (Finanzierung)</span><span><i style="background:var(--div)"></i>Dividende</span></div>
</section>
<section>
  <h2>Wohin die Dividende bis 2060 geht</h2>
  <p>Die Dividende ist der Rest, nachdem Gemeinden, Dach und Netz bezahlt sind. In der geltenden Rechnung sinkt sie von {f(pf["dividende_2028"])} auf {f(pf["dividende_2060"])} % BIP.
  Die Gründe: Verteidigung steigt, die Lenkungsabgaben schrumpfen mit den Emissionen und dem Verbrauch, und das Netz wächst mit dem Alter der Bevölkerung.
  Die Progression gleicht einen Teil aus. Mit den belegten Einnahmen (intern) fehlt noch mehr; die Dividende würde vor 2060 negativ.</p>
  <div class="pfad" id="pfad"></div>
</section>
<section>
  <h2>Einnahmen nach Steuer- und Abgabenart</h2>
  {tabelle(E, "heute")}
</section>
<section>
  <h2>Ausgaben nach Aufgaben</h2>
  {tabelle(A, "heute")}
</section>
<section>
  <h2>Finanzierung und Gemeinschaftsfonds</h2>
  {fonds_tabelle()}
</section>
<section>
  <h2>Prüfung der Positionen</h2>
  {pruef_tabelle()}
</section>
<div class="hinweis">
  <p><b>Quellen.</b> Heute: Eurostat, <a href="{D["quellen"]["steuern"]}">gov_10a_taxag</a>, <a href="{D["quellen"]["ausgaben"]}">gov_10a_exp</a> (COFOG),
  <a href="{D["quellen"]["haupt"]}">gov_10a_main</a>, Deutschland 2024, vorläufig, BIP 4.386,9 Mrd. €. Nachher: Rechnung der Initiative 28:28
  (`haushaltsplan_de.json` aus systemvarianten, netz33, projektion33, fonds_geltend), BIP 2028 4.914,9 Mrd. €.</p>
  <p><b>Zuordnung.</b> Die Zuordnung heutiger Steuern und Aufgaben zu den neuen Positionen ist eigene Arbeit (Annahme). Die deutschen Steuernamen zu den
  Eurostat-Kategorien sind eigene Kenntnis. Gebühren und Entgelte sind im Modell mit den Ausgaben verrechnet (netto). Die Zinsen 2028 sind mit der Quote 2024
  angesetzt; die Altrenten über der Dividende sind die Altlast Deutschlands (10,19 % BIP) abzüglich dieser Zinsen.</p>
  <p><b>Belegt (intern).</b> Prüfbefund B-1: Werte nach amtlichen Daten, mittlerer Fall, mit allen Rückwirkungen durch die Kette. Seit v4.95 ohne
  Zölle (Einnahme der EU) und ohne Grundsteuer in „Übrige“ (sie geht in der Grundstücksabgabe auf).</p>
</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3-sankey@0.12.3/dist/d3-sankey.min.js"></script>
<script>
const D = {json.dumps(daten, ensure_ascii=False)};
const fmt = v => v.toFixed(2).replace('.', ',');
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const PX = 9.2; // Pixel je Punkt BIP, beide Bilder gleich
function zeichne(id, nodes, links, farbe) {{
  const el = document.getElementById(id); el.innerHTML = '';
  const total = d3.sum(links.filter(l => l.stufe === 0), l => l.value);
  const npad = 6, maxN = Math.max(...[0,1,2].map(s => nodes.filter(n => n.stufe === s).length));
  const H = Math.ceil(total * PX + npad * (maxN - 1)) + 20, Wd = 1100;
  const sk = d3.sankey().nodeId(d => d.name).nodeWidth(12).nodePadding(npad).nodeAlign(d3.sankeyJustify)
    .extent([[200, 10], [Wd - 300, H - 10]]);
  const g = sk({{nodes: nodes.map(d => ({{...d}})), links: links.map(d => ({{...d}}))}});
  const svg = d3.select(el).append('svg').attr('viewBox', `0 0 ${{Wd}} ${{H}}`).attr('width', Wd).attr('height', H)
    .attr('role', 'img').attr('aria-label', 'Flussbild der Einnahmen zu den Ausgaben');
  svg.append('g').selectAll('path').data(g.links).join('path').attr('d', d3.sankeyLinkHorizontal())
    .attr('fill', 'none').attr('stroke', d => css(farbe(d))).attr('stroke-opacity', .38).attr('stroke-width', d => Math.max(1, d.width))
    .append('title').text(d => `${{d.source.name}} → ${{d.target.name}}: ${{fmt(d.value)}} % BIP`);
  const n = svg.append('g').selectAll('g').data(g.nodes).join('g');
  n.append('rect').attr('x', d => d.x0).attr('y', d => d.y0).attr('width', d => d.x1 - d.x0).attr('height', d => Math.max(1, d.y1 - d.y0))
    .attr('fill', d => css(d.farbe || '--ink'));
  n.append('text').attr('x', d => d.stufe === 0 ? d.x0 - 8 : d.x1 + 8).attr('y', d => (d.y0 + d.y1) / 2).attr('dy', '0.35em')
    .attr('text-anchor', d => d.stufe === 0 ? 'end' : 'start').text(d => d.name);
  n.append('text').attr('class', 'w').attr('x', d => d.stufe === 0 ? d.x0 - 8 : d.x1 + 8).attr('y', d => (d.y0 + d.y1) / 2 + 14)
    .attr('text-anchor', d => d.stufe === 0 ? 'end' : 'start').text(d => (d.y1 - d.y0) > 18 ? fmt(d.value) + ' %' : '');
}}
function vorher() {{
  const V = D.vorher, mid = V.mitte[0];
  const fq = n => n === 'Sozialbeiträge' ? '--aus' : (n.startsWith('Finanzierung') || n.startsWith('Gebühren')) ? '--kredit' : '--ein';
  const nodes = [...V.quellen.map(([n]) => ({{name: n, stufe: 0, farbe: fq(n)}})), {{name: mid, stufe: 1, farbe: '--ink'}},
                 ...V.ziele.map(([n]) => ({{name: n, stufe: 2, farbe: '--muted'}}))];
  const links = [...V.quellen.map(([n, v]) => ({{source: n, target: mid, value: v, stufe: 0, f: fq(n)}})),
                 ...V.ziele.map(([n, v]) => ({{source: mid, target: n, value: v, stufe: 1, f: '--muted'}}))];
  zeichne('sk-vorher', nodes, links, l => l.f);
}}
function nachher() {{
  const N = D.nachher, H = 'Landeshaushalt';
  const fz = n => n === 'Dividende' ? '--div' : n.startsWith('Beitrag') ? '--fonds' : '--muted';
  const zs = [...N.ziele_steuern]; if (N.saldo > 0) zs.push(['Saldo', N.saldo]);
  const q = [...N.steuern.map(([n, v]) => [n, v, '--ein']), ...N.zuschlag.map(([n, v]) => [n, v, '--fonds'])];
  const nodes = [...q.map(([n, , c]) => ({{name: n, stufe: 0, farbe: c}})), {{name: H, stufe: 1, farbe: '--ein'}}, ...zs.map(([n]) => ({{name: n, stufe: 2, farbe: fz(n)}}))];
  const links = [...q.map(([n, v, c]) => ({{source: n, target: H, value: v, stufe: 0, f: c}})), ...zs.map(([n, v]) => ({{source: H, target: n, value: v, stufe: 1, f: fz(n)}}))];
  zeichne('sk-nachher', nodes, links, l => l.f);
  const F = 'Gemeinschaftsfonds';
  const fq = n => n.startsWith('Kredite') ? '--kredit' : '--fonds';
  const n2 = [...N.fonds_ein.map(([n]) => ({{name: n, stufe: 0, farbe: fq(n)}})), {{name: F, stufe: 1, farbe: '--fonds'}}, ...N.fonds_aus.map(([n]) => ({{name: n, stufe: 2, farbe: '--fonds'}}))];
  const l2 = [...N.fonds_ein.map(([n, v]) => ({{source: n, target: F, value: v, stufe: 0, f: fq(n)}})), ...N.fonds_aus.map(([n, v]) => ({{source: F, target: n, value: v, stufe: 1, f: '--fonds'}}))];
  zeichne('sk-fonds', n2, l2, l => l.f);
}}
function pfad() {{
  const p = D.pfad, el = document.getElementById('pfad'); el.innerHTML = '';
  const schritte = [['Dividende 2028', p.dividende_2028, 'start'], ['Verteidigung bis 2,5 %', p.verteidigung], ['CO₂-Preis sinkt mit den Emissionen', p.darin_co2],
    ['Verbrauchsteuern sinken', p.darin_verbrauchsteuern], ['Label: weniger schädlicher Konsum', p.darin_label], ['Netz: Alterung', p.netz_alterung],
    ['Progression', p.progression], ['Dividende 2060', p.dividende_2060, 'ende'], ['belegt (intern): Lücke der Einnahmen', +(D.belegt60 - p.dividende_2060).toFixed(2)], ['Dividende 2060 belegt', D.belegt60, 'ende']];
  const Wd = 1100, H = 320, x0 = 40, bw = 82, gap = 22, y = v => 236 - v * 26;
  const svg = d3.select(el).append('svg').attr('viewBox', `0 0 ${{Wd}} ${{H}}`).attr('width', Wd).attr('height', H).attr('role', 'img')
    .attr('aria-label', 'Zerlegung des Dividendenpfads 2028 bis 2060 in Prozent des BIP');
  svg.append('line').attr('x1', 20).attr('x2', Wd - 10).attr('y1', y(0)).attr('y2', y(0)).attr('stroke', css('--rule'));
  [2, 4, 6, 8].forEach(t => {{ svg.append('line').attr('x1', 20).attr('x2', Wd - 10).attr('y1', y(t)).attr('y2', y(t)).attr('stroke', css('--rule')).attr('stroke-dasharray', '2 4');
    svg.append('text').attr('class', 'w').attr('x', 4).attr('y', y(t) + 4).text(t); }});
  let lauf = 0;
  schritte.forEach(([name, v, art], i) => {{
    const x = x0 + i * (bw + gap); let a, b, farbe;
    if (art === 'start' || art === 'ende') {{ a = 0; b = v; lauf = v; farbe = css('--div'); }}
    else {{ a = lauf; b = lauf + v; lauf = b; farbe = v < 0 ? css(name.startsWith('belegt') ? '--warn' : '--aus') : css('--ein'); }}
    svg.append('rect').attr('x', x).attr('width', bw).attr('y', y(Math.max(a, b))).attr('height', Math.max(1, Math.abs(y(a) - y(b)))).attr('fill', farbe);
    svg.append('text').attr('class', 'w').attr('x', x + bw / 2).attr('y', y(Math.max(a, b)) - 6).attr('text-anchor', 'middle').text((v > 0 && !art ? '+' : '') + fmt(v));
    const fo = svg.append('foreignObject').attr('x', x - 6).attr('y', 272).attr('width', bw + 12).attr('height', 44);
    fo.append('xhtml:div').style('font-size', '11px').style('line-height', '1.2').style('text-align', 'center').style('color', css('--muted')).text(name);
  }});
}}
function alles() {{ try {{ vorher(); nachher(); pfad(); }} catch (e) {{ console.error(e); }} }}
alles();
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', alles);
new MutationObserver(alles).observe(document.documentElement, {{attributes: true, attributeFilter: ['data-theme']}});
</script>
"""
ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("haushaltsplan-de.html")
ziel.write_text(seite, encoding="utf-8")
print("geschrieben:", ziel)
