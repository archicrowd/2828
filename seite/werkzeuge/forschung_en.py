#!/usr/bin/env python3
"""English research site (main version, international), Logbuch v4.57. Called by forschung_bau.py; writes to docs/ root.

Content is international: five reference countries instead of the German example household, the common fund of 30 states, VAT factors
for Germany and France, marginal burden (Germany, so far the only country computed), reviews with English summaries, research kit with
numbered figures. All figures come from the result files (daten/aggregate/), via forschung_bau (shared data and helpers).
"""
import csv, html, importlib.util, json
from pathlib import Path

_spec = importlib.util.spec_from_file_location("forschung_bau_daten", Path(__file__).resolve().parent / "forschung_bau.py")
F = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(F)

J, VERSION, KONTAKT, SEITE = F.J, F.VERSION, F.KONTAKT, F.SEITE
DATUM = "1 November 2026"
KORR, STUFEN, GEPRUEFT, PAGES = F.KORREKTUREN, F.STUFEN, F.GEPRUEFT, F.PAGES
SINCE_REVIEW = [
 ("v4.46", "Responses to the third review: corrections 73–76 (presentation), interest × growth grid", "no adopted figure"),
 ("v4.47", "Marginal burden adjusted for counter-values (cross-check, Z17)", "no adopted figure"),
 ("v4.49–v4.50", "Design decisions E12–E15 (top-up, locked account, pension cut, dividend, label)", "no calculation"),
 ("v4.51", "Country models checked against OECD Taxing Wages 2026; corrections 77–79 (prime d'activité 59.85 %, housing lump sum)", "France: today's income at half the minimum wage 1,219 → 1,136 € per month"),
 ("v4.52", "Pass-through only from social-security contributions that disappear (decision E16); correction 80", "average wage, single: FR +390 → +286 €, ES +350 → +321 €, PL +1,474 → +1,404 zł"),
 ("v4.53", "Key figures checked automatically against result files; correction 81", "no calculation; outdated statements corrected"),
 ("v4.54", "VAT by income for France (Eurostat HBS 2020)", "FR average wage +286 → +276 €"),
 ("v4.57", "Household types by country (new output)", "no adopted figure; new values Z20–Z34"),
 ("v4.58", "Review coverage shown on the site; correction 83", "no calculation"),
 ("v4.59", "Archive on Zenodo, DOI on the site", "no calculation"),
 ("v4.60", "Working paper (draft) built from the result files", "no calculation"),
 ("v4.61", "Working paper: objectives and assessment against them", "no calculation"),
 ("v4.62", "Working paper: climate and the label as an economic incentive", "no calculation"),
]
assert len(SINCE_REVIEW) == len(F.SEIT_PRUEFUNG), "englische und deutsche Liste seit der Prüfung gleich lang halten"
LS = J("laenderseiten.json")["staaten"]
VH = F.VH["laender"]
G = J("gini.json")["staaten"]
LAENDER = ("DE", "FR", "IT", "ES", "PL")
NAME = {"DE": "Germany", "FR": "France", "IT": "Italy", "ES": "Spain", "PL": "Poland"}
TYP_EN = {"alleinstehend": "single", "alleinerziehend, 1 Kind": "single parent, 1 child", "Paar, ein Einkommen, 2 Kinder": "couple, one earner, 2 children"}
FG, FZ, GB, MV, ML, PN, MB, RE, VL = F.FG, F.FZ, F.GB, F.MV, F.ML, F.PN, F.MB, F.RE, F.VL
V = {c: VH[c]["verrechnung_2028"] for c in LAENDER}


def en(x, n=0):
    return ("−" if x < 0 else "") + f"{abs(x):,.{n}f}"


def pm(x, n=0):
    return ("+" if x > 0 else "") + en(x, n)


def cur(c, x, sign=True):
    t = pm(x) if sign else en(x)
    return f"{t} zł" if c == "PL" else f"{t} €"


def wert(x):
    if isinstance(x, str):
        return x
    if isinstance(x, int) or float(x).is_integer():
        return str(int(x)) if 1900 < x < 2200 else en(x)
    return en(x, len(repr(float(x)).split(".")[1]))


# ---------------- Figures to cite (Z01–Z19 as in German, Z20–Z34 by country)
FIGURES = [
 ("Z01", "Transformation dividend per adult (Germany)", round(F.DIV_ERW), "€ per month", "2028, purchasing power 2026", "netz33.json × regel_boden.json topf", "adopted"),
 ("Z02", "Transformation dividend per child (Germany)", round(F.DIV_ERW * 0.8), "€ per month", "as Z01, child share 0.8", "as Z01", "adopted"),
 ("Z03", "Gain, single, gross wage € 42,000 (Germany)", F.fall(2028, F.TYPEN[0], 0.8, F.ZU_DE, 0.1)["differenz_monat"], "€ per month", "2028; pass-through 80 %, surcharge 15.0 %, compulsory saving 10 %", "haushalte33.json faelle", "adopted"),
 ("Z04", "Gain, couple with one earner and 2 children, € 42,000 (Germany)", F.fall(2028, F.TYPEN[2], 0.8, F.ZU_DE, 0.1)["differenz_monat"], "€ per month", "as Z03", "haushalte33.json faelle", "adopted"),
 ("Z05", "Working-age households better off (Germany)", MB["erwerbsfaehige_haushalte"]["anteil_mehr_haushalte_pct"], "%", "2028; synthetic microsimulation, pass-through 80 %", "mikro_de.json basis/ergebnis/0.8", "check"),
 ("Z06", "All households better off (Germany)", MB["gesamt"]["anteil_mehr_haushalte_pct"], "%", "as Z05", "mikro_de.json basis/ergebnis/0.8/gesamt", "check"),
 ("Z07", "Pensioner households better off (pension rule E)", RE["anteil_mehr_pct"], "%", "2028, Germany", "rentner_kombi.json varianten/4", "adopted"),
 ("Z08", "Pensioner households, mean change (pension rule E)", RE["mittel_monat"], "€ per month", "2028, Germany", "rentner_kombi.json varianten/4", "adopted"),
 ("Z09", "Contribution to the common fund of 30 states", FG["beitrag_pct_bip"], "% of GDP", "annual until repaid", "fonds_geltend.json", "adopted"),
 ("Z10", "Legacy surcharge on all taxes (common rate)", FG["zuschlag_auf_alle_steuern_pct"], "%", "fund interest 2.45 %", "fonds_geltend.json", "adopted"),
 ("Z11", "Debt ratio of the fund, peak", FG["schuldenquote_spitze"], "% of GDP", f"in {FG['spitzenjahr']}", "fonds_geltend.json", "adopted"),
 ("Z12", "Fund fully repaid", FG["zieljahr"], "year", "", "fonds_geltend.json", "adopted"),
 ("Z13", "Old pension claims above the dividend (Z)", F.AL["beschluss"]["verhandlungsmasse_z_2028_pct_bip"], "% of GDP", "2028, average of states", "altlasten.json beschluss", "adopted"),
 ("Z14", "Total burden, taxes and fund (Germany)", F.ZR["a_steuern_und_fonds"], "% of GDP", "2028; today 40.76 % (Eurostat 2024)", "gesamtlast33.json reihe/0", "adopted"),
 ("Z15", "Total burden including compulsory saving (own account)", F.ZR["b_mit_pflichtvorsorge"], "% of GDP", "2028", "gesamtlast33.json reihe/0", "adopted"),
 ("Z16", "Cost of the strong net (Germany)", F.NZ["beschluss"]["reihe"][0]["netz_pct_bip"], "% of GDP", "2028", "netz33.json beschluss/reihe/0", "adopted"),
 ("Z17", "Marginal burden at € 60,000: today / new 2028 (Germany)", f"{en(GB['zeilen'][5]['heute_pct'], 1)} / {en(GB['zeilen'][5]['neu_2028_pct'], 1)}", "% per additional euro", "single; new without compulsory saving", "grenzbelastung33.json zeilen/5", "check"),
 ("Z18", "VAT label burden, factor lowest / highest income class (Germany)", f"{en(MV['klassen'][0]['phi']['mit_vorsteuer'][0], 2)} / {en(MV['klassen'][-1]['phi']['mit_vorsteuer'][0], 2)}", "relative to mean", "EVS 2023", "mwst_verteilung.json klassen", "adopted"),
 ("Z19", "One-off price level effect of the VAT label 2028", f"{en(PN['reihe'][0]['mwst_spanne_pct'][0], 1)} to {en(PN['reihe'][0]['mwst_spanne_pct'][1], 1)}", "%", "mechanical 2.47 %", "preisniveau33.json reihe/0", "check"),
]
for i, c in enumerate(LAENDER):
    FIGURES.append((f"Z{20 + i}", f"Gain, single employee at the average wage ({NAME[c]})", V[c]["mehr_monat"]["1"], "zł per month" if c == "PL" else "€ per month",
                    "2028; country's own legacy surcharge after netting", "verrechnung_haushalte.json laender/" + c, "adopted"))
for i, c in enumerate(LAENDER):
    FIGURES.append((f"Z{25 + i}", f"Legacy surcharge 2028 after netting ({NAME[c]})", LS[c]["fonds"]["zuschlag_pct"], "%", "converging to the common rate by 2058",
                    "laenderseiten.json staaten/" + c + "/fonds", "adopted"))
for i, c in enumerate(LAENDER):
    FIGURES.append((f"Z{30 + i}", f"Gini coefficient 2025 → 2028 ({NAME[c]})", f"{en(G[c]['gini_amtlich_2025'], 1)} → {en(G[c]['reihe'][0]['mitte'], 1)}", "index 0–100",
                    "official 2025 (Eurostat) plus model change", "gini.json staaten/" + c, "check"))

ZITAT = (f"Initiative 28:28 (2026): The Golden Third – research kit and figures to cite, model version {VERSION}, {DATUM}. "
         f"Zenodo. https://doi.org/{F.DOI_KONZEPT}. Licence: scripts MIT, texts and results CC BY 4.0.")

NAV = [("index.html", "Overview"), ("households.html", "Households"), ("fund.html", "Legacy fund"), ("vat.html", "VAT label"),
       ("marginal.html", "Marginal burden"), ("reviews.html", "Reviews"), ("kit.html", "Research kit"), ("index.html#contact", "Contact")]


def seite(datei, titel, inhalt, beschreibung):
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == datei else ""}>{t}</a>' for h, t in NAV) + \
          f'<a href="de/{DE_ZIEL.get(datei, "index.html")}" lang="de">Deutsch</a>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titel)} – The Golden Third (research)</title><meta name="description" content="{html.escape(beschreibung)}">
<link rel="stylesheet" href="style.css"></head><body>
<header><div class="marke"><a href="index.html">The Golden Third · Research and review</a></div><nav>{nav}</nav></header>
<main>{inhalt}</main>
<footer>Initiative 28:28 · model version {VERSION} · {DATUM} · texts and results CC BY 4.0, scripts MIT · figures taken from the model's
result files (<a href="data/">data/</a>) · contact <a href="mailto:{KONTAKT}">{KONTAKT}</a> · legal notice and privacy:
<a href="{SEITE}">archicrowd.de</a></footer>
</body></html>"""


DE_ZIEL = {"index.html": "index.html", "households.html": "faelle-42000.html", "fund.html": "fonds.html", "vat.html": "mwst.html",
           "marginal.html": "grenzbelastung.html", "reviews.html": "pruefungen.html", "kit.html": "kit.html"}


def tabelle(kopf, zeilen, rechts=(), hl=()):
    return F.tabelle(kopf, zeilen, rechts, hl)


def quelle(*dateien):
    return '<p class="meta">Data: ' + ", ".join(f'<a href="data/{d}"><code>{d}</code></a>' for d in dateien) + \
           f' · model version {VERSION} · citable figures: <a href="kit.html">research kit</a></p>'


def laender_tabelle():
    z = [[NAME[c], cur(c, V[c]["mehr_monat"]["0.5"]), "<b>" + cur(c, V[c]["mehr_monat"]["1"]) + "</b>", cur(c, V[c]["mehr_monat"]["2"]),
          f"{V[c]['anteil_mehr']['alleinstehend']} %", f"{en(G[c]['gini_amtlich_2025'], 1)} → {en(G[c]['reihe'][0]['mitte'], 1)}",
          f"{en(LS[c]['fonds']['zuschlag_pct'], 1)} %"] for c in LAENDER]
    return tabelle(["Country", "½ × av. wage", "1 × av. wage", "2 × av. wage", "Better off", "Gini 2025 → 28", "Surcharge 2028"], z, rechts=(1, 2, 3, 4, 5, 6))


AW_TEXT = "; ".join(f"{NAME[c]} {cur(c, V[c]['durchschnittslohn'], False)}" for c in LAENDER)


def p_index():
    eu = ("DE", "FR", "IT", "ES")
    lo, hi = min(V[c]["mehr_monat"]["1"] for c in eu), max(V[c]["mehr_monat"]["1"] for c in eu)
    karten = [
     ("households.html", "Households in five countries", f"+{en(lo)} to +{en(hi)} €",
      "per month for a single employee at the average wage (euro countries) – by country, household type and wage level, with all assumptions and cross-checks"),
     ("fund.html", "Common legacy fund", en(FG["zuschlag_auf_alle_steuern_pct"], 1) + " %", f"surcharge on all taxes across 30 states; repaid by {FG['zieljahr']}; sensitivity to interest and growth"),
     ("vat.html", "VAT label by income", en(MV["klassen"][0]["phi"]["mit_vorsteuer"][0], 2) + " – " + en(MV["klassen"][-1]["phi"]["mit_vorsteuer"][0], 2),
      "burden of the VAT label relative to the average, from household budget surveys (Germany, France)"),
     ("marginal.html", "Marginal burden", en(GB["zeilen"][5]["heute_pct"], 1) + " → " + en(GB["zeilen"][5]["neu_2028_pct"], 1) + " %",
      "per additional euro at € 60,000 (Germany), adjusted for what contributions buy")]
    k = "".join(f'<a class="karte" href="{h}"><b>{t}</b><span class="wert">{w}</span>{x}</a>' for h, t, w, x in karten)
    n_ok = VL["bestanden"].split(" ")[0]
    inhalt = f"""
<h1>The Golden Third – calculations, reviews and data</h1>
<p class="lede">A proposal for taxation and social protection shared by a group of states: no euro of income taxed at more than one third,
social contributions replaced by a strong safety net without premiums, a monthly transformation dividend for every adult, a funded
pension account of one's own, and a common fund for legacy debt and pension promises. These pages are written for research and review:
they show the core calculations with their assumptions, the reviews so far, and the figures in citable form.</p>
<p class="meta">Draft for discussion, not an adopted programme. Model version {VERSION}, {DATUM}. General website in six languages:
<a href="{SEITE}">archicrowd.de</a> · <a href="de/index.html">Deutsch</a></p>
<h2>Five reference countries, 2028</h2>
<p>Change in monthly disposable income for a single employee, compared with today's tax and benefit law (2026), in today's purchasing power.
Each country carries its own legacy surcharge after netting in the common fund.</p>
{laender_tabelle()}
<p class="meta">Average wage: OECD Taxing Wages, 2024 ({AW_TEXT}). Static model; employer contributions passed on into wages at 80 % (legal
obligation with fallback rule); compulsory saving of 10 % counted as an outflow. Better off: share of single full-time employees across the
wage distribution, scaled from Germany (assumption). Surcharge: legacy surcharge on all taxes after netting in the common fund (converging to
{en(FG['zuschlag_auf_alle_steuern_pct'], 1)} % by 2058). Gini: official value 2025 (Eurostat, EU-SILC) plus the change in the model. Poland in złoty.</p>
<h2>Four core topics</h2><div class="karten">{k}</div>
<h2>The building blocks</h2>
<div class="tab"><table><tbody>
<tr><td><b>Income tax</b></td><td>0 / 11 / 19 / 25 / 33 % in steps tied to each country's basic needs; capital income, profits and inheritance at most
33 %; company profits taxed where customers are, including digital platforms</td></tr>
<tr><td><b>Contributions</b></td><td>Social contributions abolished; employers must pass at least 80 % of the contributions that disappear into wages
(health, long-term care, pensions, unemployment, family)</td></tr>
<tr><td><b>Strong net</b></td><td>Health care, long-term care, minimum pension, basic needs in disability and unemployment, financed from taxes
(about {en(F.NZ['beschluss']['reihe'][0]['netz_pct_bip'], 1)} % of GDP in Germany); low earners are topped up on a pre-filled application, own earnings count by half</td></tr>
<tr><td><b>Dividend</b></td><td>Monthly payment to every adult, children 80 %, without application; financed from steering taxes and the gains of
digitalisation; it shrinks as emissions disappear – by design</td></tr>
<tr><td><b>Own route</b></td><td>Compulsory saving of 10 % of gross wages into a personal account, locked until retirement age, few investment options and a default fund</td></tr>
<tr><td><b>VAT label</b></td><td>5 / 11 / 17 / 25 %, special rate 33 % only for harmful goods; lower rates through certification by supervised bodies</td></tr>
<tr><td><b>Legacy</b></td><td>Public debt and unfunded pension promises in a common fund of the participating states: contribution {en(FG['beitrag_pct_bip'], 2)} % of GDP,
debt peak {en(FG['schuldenquote_spitze'], 1)} % of GDP in {FG['spitzenjahr']}, repaid by {FG['zieljahr']}; existing pensions above basic needs reduced by 15 %</td></tr>
</tbody></table></div>
<h2>Which states?</h2>
<p>The calculations cover a possibility space of 30 European states, with France, Italy, Spain and Poland as reference countries besides Germany.
Common rules only work where they are broadly accepted and reliably enforced. A selection by structural criteria – rule of law, democratic
legitimacy, data availability, acceptance – rather than by geography is under discussion; on the World Justice Project's Rule of Law Index 2025,
Australia, Canada, New Zealand, the United Kingdom and Japan score at the level of the strongest European states. These states are not
calculated in the model; the index is used here only as one possible criterion.</p>
<h2>How the figures are produced</h2>
<p>All values come from one open chain of calculations ({STUFEN} stages) based on official statistics (Eurostat, OECD, national statistical offices) and published
surveys. The country tax models are checked against the OECD's Taxing Wages 2026: {n_ok} of 10 household types lie within ±2 percentage points
of the OECD tax wedge; the deviations for France and Poland are explained. For Germany, a synthetic microsimulation checks the distribution
across all households. Every change and every error found is logged with a number ({KORR} corrections so far). The model is static: labour supply,
saving and migration do not respond; pass-through, avoidance and take-up enter as assumptions or bands. A qualitative review of behavioural
effects has been done; the quantitative stage is open.</p>
<div class="hinweis vorbehalt">The three reviews so far (October 2026) were <b>commissioned by the initiative</b> and cover the model up to
version {GEPRUEFT}. Changes up to {VERSION} have not yet been reviewed (<a href="reviews.html#since">list</a>). Independent review is explicitly
invited; the material is ready.</div>
<h2>Reviews and research kit</h2>
<p><a href="reviews.html">Reviews</a>: review reports and responses, with all findings and how they were handled.
<a href="kit.html">Research kit</a>: short summary (PDF), numbered figures to cite (CSV, JSON), result files and a citation.</p>
<h2 id="contact">Contact</h2>
<p>Questions, objections and offers to review: <a href="mailto:{KONTAKT}">{KONTAKT}</a>. Scripts, parameters and the full log of all versions are
available to reviewers on request. Archive with DOI: <a href="https://doi.org/{F.DOI_KONZEPT}">{F.DOI_KONZEPT}</a>; a working paper is in preparation.</p>"""
    return seite("index.html", "Overview", inhalt, "Calculations, reviews and citable figures for the Golden Third proposal.")


def p_households():
    tz = []
    for c in LAENDER:
        for t, te in TYP_EN.items():
            m = V[c]["mehr_monat_typen"][t]
            tz.append([NAME[c] if t == "alleinstehend" else "", te, cur(c, m["0.5"]), cur(c, m["1"]), cur(c, m["2"]), f"{V[c]['anteil_mehr'][t]} %"])
    kz = [[NAME[c], en(x["allein_100"]["modell_keil"], 1), en(x["allein_100"]["oecd_keil"], 1), pm(x["allein_100"]["abw_pp"], 1),
           en(x["paar_ein_einkommen_2k"]["modell_keil"], 1), en(x["paar_ein_einkommen_2k"]["oecd_keil"], 1), pm(x["paar_ein_einkommen_2k"]["abw_pp"], 1)]
          for c, x in VL["keil"].items()]
    g = [F.fall(2028, t, 0.8, F.ZU_DE, 0.1) for t in F.TYPEN]
    inhalt = f"""
<h1>Households in five countries</h1>
<p class="lede">How disposable income changes in 2028 for three household types at half, once and twice the average wage, compared with today's
tax and benefit law of each country. The same rules apply everywhere; the amounts follow each country's basic needs, price level and legacy.</p>
<h2>Change in monthly disposable income, 2028</h2>
{tabelle(["Country", "Household", "½ × av. wage", "1 × av. wage", "2 × av. wage", "Better off"], tz, rechts=(2, 3, 4, 5))}
<p class="meta">Purchasing power 2026; Poland in złoty. Today: income tax, employee contributions and cash benefits under 2026 law, including minimum
income schemes where modelled (Germany: Bürgergeld approximation incl. housing and child supplements; France: APL; Italy: Assegno di Inclusione;
Spain: IMV and CAPI; Poland: zasiłek okresowy). New: tax 0/11/19/25/33 %, dividend, pass-through of 80 % of the employer contributions that disappear
(capped at six times basic needs), VAT label, the country's own legacy surcharge, compulsory saving of 10 % (counted as outflow), basic income floor
with own earnings counted by half. Average wage: OECD Taxing Wages 2024 ({AW_TEXT}). Better off: share of employees of this type across the wage
distribution, scaled from Germany (assumption).</p>
<h2>What drives the differences</h2>
<ul>
<li><b>One-earner couples with higher wages</b> lose part of today's joint taxation (German splitting, French quotient familial): every adult is taxed
individually and receives an own dividend. Around twice the average wage the gain shrinks to about zero in Germany and France.</li>
<li><b>France at half the average wage</b>: today's in-work benefit (prime d'activité) and family allowances are replaced by the dividend and the
floor; for single people at half the average wage this is a loss of {en(-V['FR']['mehr_monat']['0.5'])} € per month. Employer contributions near the
minimum wage are already largely waived today (RGDU), so little is passed on.</li>
<li><b>Italy, Spain and Poland at low wages</b>: today's minimum income schemes reach fewer households; the floor and the dividend raise low incomes
more strongly.</li>
<li><b>Legacy surcharge</b>: France ({en(LS['FR']['fonds']['zuschlag_pct'], 1)} %) and Italy ({en(LS['IT']['fonds']['zuschlag_pct'], 1)} %) carry higher
surcharges than Germany ({en(LS['DE']['fonds']['zuschlag_pct'], 1)} %) and Poland ({en(LS['PL']['fonds']['zuschlag_pct'], 1)} %) until 2058.</li>
</ul>
<h2>Cross-checks</h2>
<h3>Country models against the OECD (Taxing Wages 2026, tax wedge in % of labour costs)</h3>
{tabelle(["Country", "Single: model", "OECD", "Diff. (pp)", "Couple, 2 ch.: model", "OECD", "Diff. (pp)"], kz, rechts=(1, 2, 3, 4, 5, 6))}
<p class="meta">Model: 2026 law; OECD: 2025. Poland: the OECD counts neither accident insurance nor the labour and guarantee funds on the employer
side, and the health contribution differently (open). France, couple: the model pays the prime d'activité at this wage level, consistent with the
ministry's examples for the 2026 reform; the OECD apparently does not (to be checked in the country chapter). In France the rate of the prime
d'activité (59.85 %) and the housing lump sum for APL recipients were corrected after this check (corrections 77 and 78).</p>
<h3>Germany: microsimulation and pensioners</h3>
<p>A synthetic microsimulation calibrated to official totals finds {en(MB['erwerbsfaehige_haushalte']['anteil_mehr_haushalte_pct'], 1)} % of working-age
households and {en(MB['gesamt']['anteil_mehr_haushalte_pct'], 1)} % of all households better off; households whose main earner has a mini-job
{en(MB['status']['Hauptperson Minijob']['anteil_mehr_haushalte_pct'], 1)} %, households without earnings (Bürgergeld)
{en(MB['status']['ohne Erwerb (Bürgergeld)']['anteil_mehr_haushalte_pct'], 1)} %. Pensioners: {en(RE['anteil_mehr_pct'], 1)} % better off, mean change
{en(RE['mittel_monat'])} € per month, top fifth {en(RE['fuenftel_monat'][4])} €. Validation 2025: gross wages {en(MI_V('bruttolohnsumme'), 1)} %, wage tax
{en(MI_V('lohnsteuer'), 1)} % against official figures.</p>
<h3>Germany: the € 42,000 example</h3>
<p>Single {pm(g[0]['differenz_monat'])} €, single parent {pm(g[1]['differenz_monat'])} €, couple with one earner and two children
{pm(g[2]['differenz_monat'])} € per month (gross wage € 42,000, about two thirds of the average wage). Sensitivity to pass-through, surcharge,
saving and fund interest: <a href="de/faelle-42000.html">German page</a>.</p>
<div class="hinweis vorbehalt">Country models are simplified (one earner per household; regional rules, housing benefits beyond those named and
behavioural responses not included). The share of employees better off uses the German wage distribution scaled to each country's average wage;
national wage distributions are an open task.</div>
{quelle("verrechnung_haushalte.json", "validierung_laender.json", "mikro_de.json", "rentner_kombi.json", "haushalte33.json")}"""
    return seite("households.html", "Households", inhalt, "Households in five countries: gains and losses, assumptions and cross-checks.")


def MI_V(k):
    return F.MI["basis"]["validierung_2025"][k]["abweichung_pct"]


def p_fund():
    vz = FG["verrechnung"]["laender"]
    z1 = [[NAME[c], en(vz[c]["reihe"]["2028"]["beitrag_pct_bip"], 2), en(vz[c]["reihe"]["2028"]["zuschlag_pct"], 1)] for c in LAENDER]
    z2 = [[v["fall"].replace("fest ", "fixed ").replace("Übergang", "transition"), en(v["beitrag_pct_bip"], 2), en(v["zuschlag_pct"], 1),
           f"{en(v['spitze_zehn'], 1)} ({v['spitzenjahr_zehn']})"] for v in FZ["varianten"]]
    z3 = [[en(r["zins"], 2) + " %", en(r["wachstum"], 1) + " %", en(r["beitrag_pct_bip"], 2), en(r["zuschlag_pct"], 1),
           en(r["beschlussbeitrag_fest"]["restschuld_2098_zehn"], 1)] for r in FZ["zins_wachstum"] if r["zins"] in (2.45, 3.5)]
    inhalt = f"""
<h1>The common legacy fund</h1>
<p class="lede">Public debt and pension promises from the old system remain each state's responsibility. The blueprint offers a common fund with a
common interest rate. It spreads the burden until repayment in {FG['zieljahr']} and is financed by a surcharge on all taxes.</p>
<h2>Adopted calculation</h2>
{tabelle(["Item", "Value"], [["Contribution", en(FG['beitrag_pct_bip'], 2) + " % of GDP"], ["Surcharge on all taxes", en(FG['zuschlag_auf_alle_steuern_pct'], 1) + " %"],
   ["Debt ratio of the fund, peak", f"{en(FG['schuldenquote_spitze'], 1)} % of GDP ({FG['spitzenjahr']})"], ["Repaid", str(FG["zieljahr"])],
   ["Interest", en(FG["zins"], 2) + " % (euro area average 2006–2025)"], ["Old pension claims above the dividend (Z), 2028", en(F.AL['beschluss']['verhandlungsmasse_z_2028_pct_bip'], 2) + " % of GDP"],
   ["Total burden, taxes and fund, Germany 2028", en(F.ZR['a_steuern_und_fonds'], 2) + " % of GDP (today 40.76 %)"]])}
<p class="meta">Fund of 30 states: decision of the ten states calculated in detail, scaled by the ratio 30/10 from the possibility space (assumption).
Pension rule E: promises above basic needs reduced by 15 %, own savings not reduced; pensioners' health and care contributions disappear.</p>
<h2>Netting by state, 2028</h2>
{tabelle(["State", "Contribution (% GDP)", "Surcharge (%)"], z1, rechts=(1, 2))}
<p class="meta">Each state carries the surcharge after netting its own legacy; converging to the common rate by 2058.</p>
<h2>Sensitivity: interest</h2>
{tabelle(["Interest", "Contribution (% GDP)", "Surcharge (%)", "Peak (% GDP, year; ten states)"], z2, rechts=(1, 2, 3))}
<p class="meta">Market rates October 2026: German federal bonds about 3.5 %, EU bonds about 4.0 % (secondary sources).</p>
<h2>Sensitivity: interest and nominal growth</h2>
{tabelle(["Interest", "Growth", "Contribution (% GDP)", "Surcharge (%)", "Remaining debt 2098 at fixed contribution (% GDP)"], z3, rechts=(2, 3, 4))}
<div class="hinweis vorbehalt">Sustainability depends on interest relative to growth. At 2.45 % interest and only 2.0 % nominal growth, a fixed
contribution would leave debt of {en(FZ['zins_wachstum'][0]['beschlussbeitrag_fest']['restschuld_2098_zehn'], 0)} % of GDP in 2098. Holding Z constant
in % of GDP across growth paths is a simplification.</div>
{quelle("fonds_geltend.json", "fondszins.json")}"""
    return seite("fund.html", "Legacy fund", inhalt, "Common fund for public debt and pension promises: calculation and sensitivity.")


def p_vat():
    z1 = [[k["klasse"].replace(">=", "≥ ") + " €", en(k["phi"]["mit_vorsteuer"][0], 2), en(k["phi"]["mit_vorsteuer"][1], 2), en(k["phi"]["sichtbar"][0], 2)] for k in MV["klassen"]]
    fr = ML["staaten"]["FR"]
    z2 = [[f"Q{q['fuenftel']}", en(q["aequivalent_jahr"]), en(100 * q["steuerpflichtig"], 1) + " %", en(q["phi"][0], 2), en(q["phi"][1], 2)] for q in fr["fuenftel"]]
    p0 = PN["reihe"][0]
    inhalt = f"""
<h1>VAT label by income</h1>
<p class="lede">VAT becomes a label: A+ 5 %, A 11 %, B 17 %, C 25 %, special rate 33 % only for harmful goods. How strongly a household feels the change
depends on how much it consumes and on what: rent, health, education and insurance are exempt.</p>
<h2>Germany (household budget survey EVS 2023)</h2>
{tabelle(["Household net income per month", "Factor: additional burden", "Factor: VAT paid", "visible tax only"], z1, rechts=(1, 2, 3))}
<p class="meta">Factor 1 = previous calculation (effective rate on all consumption). Visible additional burden on average {en(MV['sichtbar_mittel']['mehr_pct_konsum'], 2)} %
of consumption against {en(MV['bisher']['mehr_pct_konsum'], 2)} % before; the remainder (input tax in exempt sectors, housing construction) is spread
evenly per euro of consumption (assumption). Midpoints of open classes and the mapping of survey groups are assumptions.</p>
<h2>France (Eurostat Household Budget Survey 2020)</h2>
{tabelle(["Quintile", "Equivalised income (€ / year)", "Taxable share", "Factor: additional burden", "Factor: VAT paid"], z2, rechts=(1, 2, 3, 4))}
<p class="meta">Structure of consumption by income quintile (flagged as estimated by Eurostat). Position of the quintiles on equivalised income
(EU-SILC deciles) and rates per item are assumptions. Italy, Spain and Poland still use factor 1 (data request pending).</p>
<h2>Price level</h2>
<p>One-off price level effect in 2028: {en(p0['mechanisch_pct'], 2)} % mechanically, {en(p0['mwst_spanne_pct'][0], 1)} to {en(p0['mwst_spanne_pct'][1], 1)} %
with partial pass-through and taxable consumption only. VAT increases are passed on to prices three to four times more strongly than cuts
(Benzarti et al., JPE 2020); an asymmetric variant is open. Lower label rates are reached through certification, which may strengthen pass-through
of cuts (not yet evidenced).</p>
{quelle("mwst_verteilung.json", "mwst_laender.json", "preisniveau33.json")}"""
    return seite("vat.html", "VAT label", inhalt, "VAT label: burden factors by income for Germany and France.")


def p_marginal():
    z = [[en(r["brutto"]) + " €", en(r["heute_pct"], 1), " / ".join(en(r["heute_bereinigt_pct"][a], 1) for a in ("0.5", "1.0")),
          en(r["neu_2028_pct"], 1), en(r["neu_nach_tilgung_pct"], 1), en(r["neu_2028_mit_vorsorge_pct"], 1)] for r in GB["zeilen"]]
    inhalt = f"""
<h1>Marginal burden, adjusted for what contributions buy</h1>
<p class="lede">How much of an additional euro earned is kept? Comparing "new tax" with "today's tax" is misleading, because today health,
long-term care and pensions are financed by contributions and in the new system by taxes. The calculation therefore adjusts for counter-values.
So far computed for Germany.</p>
{tabelle(["Gross wage", "today", "today adjusted (equivalence 0.5 / 1)", "new 2028", "new after repayment", "new 2028 incl. compulsory saving"], z, rechts=(1, 2, 3, 4, 5))}
<p class="meta">Per cent per additional euro of gross wage, single, no children. Today: income tax, solidarity surcharge and employee contributions (2026
law); adjusted for the part of the pension contribution that creates an own entitlement (equivalence as a band, assumption). New: income tax, Germany's
surcharge ({en(GB['zuschlag_2028'], 1)} %, after repayment 0) and the additional VAT burden. Compulsory saving (10 %) goes to an own, inheritable account
and counts as saving; for comparison it is included in the last column.</p>
<div class="hinweis vorbehalt">Not included: the employer side, means-tested benefits and the top-up with earnings counted by half. In the lower
range the marginal burden is therefore not yet fully computed (open task V1).</div>
{quelle("grenzbelastung33.json")}"""
    return seite("marginal.html", "Marginal burden", inhalt, "Marginal burden today and new, adjusted for counter-values (Germany).")


REVIEWS = [
 ("First review, 19 October 2026",
  "Website and repository. The reviewer assessed the predecessor model (version B, 28 %) because our entry documents still named it as current – our "
  "error (correction 66). Main points: the pass-through of employer contributions is the weakest element; the level of the safety net was not "
  "quantified; a counter-proposal \"rule book instead of a roof\". Response: legal obligation to adjust employment contracts by the start date with "
  "a fallback rule; the net level is published; the variant was worked out.", 0),
 ("Second review, 20 October 2026",
  "The calculation core of the current model was re-implemented independently (household formulas, fund recursion, pass-through sensitivity) and "
  "confirmed. Findings B11–B16 concerned labelling and consistency: fund figures on the country pages, two dividend paths, communication of the "
  "pension cut, top-earner statements, total burden, size Z. A summarised report added an own microsimulation supporting \"9 out of 10 full-time "
  "employees better off\". Response: register of current figures (KENNZAHLEN), common fund on all pages, new calculations on price level, "
  "avoidance and the fallback rule.", 1),
 ("Third review, 24 October 2026",
  "Model version 4.42 along the six questions of our review folder. The calculation core was confirmed at rounding level; eight findings (B17–B24), "
  "all inconsistencies or gaps, none a calculation error – among them three different values for the same total burden, the undocumented base of "
  "the company tax position, and missing growth sensitivity of the fund. Response: corrections 73–76, interest × growth grid, definition table of "
  "revenue positions; the base of the company position remains open.", 2),
 ("For further reviews", "What should be reviewed, how to recalculate, assumptions and their sensitivity, review questions; plus the qualitative "
  "review of behavioural effects.", 3),
]


def p_reviews():
    teile = []
    for (titel, text, i) in REVIEWS:
        dok = F.PRUEF[i][2]
        li = "".join(f'<li><a href="downloads/{F.pdf_name(p)}">{DOK_EN.get(Path(p).stem, t)}</a> (PDF, German)</li>' for p, t in dok)
        teile.append(f"<h2>{titel}</h2><p>{text}</p><ul>{li}</ul>")
    inhalt = f"""
<h1>Reviews</h1>
<p class="lede">In October 2026 the website and the calculations were recalculated in three reviews. All findings are documented with their
assessment and implementation; errors found are logged as numbered corrections.</p>
<div class="hinweis vorbehalt">The reviews were commissioned by the initiative. They do not replace independent assessment. The documents
reflect the state of their version; later calculations may have changed figures in them. Current values: <a href="kit.html">research kit</a>.
The reports of the first and second review are held by the initiative and will be added with the reviewers' consent. Documents are in German;
English summaries above each list.</div>
{''.join(teile)}
<h2 id="since">Changed since the last review ({GEPRUEFT}), not yet reviewed</h2>
<p>The third review covered model version {GEPRUEFT}. Since then the following calculations and statements have changed (log, volume III);
a review of these changes is planned.</p>
{tabelle(["Version", "Change", "Figure moved"], [list(z) for z in SINCE_REVIEW])}"""
    return seite("reviews.html", "Reviews", inhalt, "Review reports and responses on the Golden Third model.")


DOK_EN = {"Stellungnahme-Pruefung-2026-10-20": "Response of the initiative (v4.12)", "Rueckmeldung-Pruefung-2026-10-20": "Reply to the reviewer (v4.13)",
          "Stellungnahme-Pruefung2-2026-10-20": "Response to the second review (v4.14)",
          "Stellungnahme-Pruefung3-2026-10-20": "Response to the summarised report (v4.17/v4.18)",
          "LIESMICH": "Reviewer's contribution: microsimulation \"9 out of 10 employees\"", "STELLUNGNAHME-2026-10-24": "Review report",
          "Stellungnahme-Pruefung4-2026-10-24": "Response of the initiative (v4.46)", "Pruefmappe-Extern-2026-10-24": "Review folder",
          "Verhaltenswirkungen-Voruntersuchung-2026-10-24": "Behavioural effects: qualitative review"}


def p_kit():
    z = [[x[0], x[1], f"<b>{wert(x[2])}</b>", x[3], x[4], x[6]] for x in FIGURES]
    inhalt = f"""
<h1>Research kit</h1>
<p class="lede">For research, press and review: a short summary, the core figures with origin and status, the result files and a citation.</p>
<h2>Downloads</h2>
<ul>
<li><a href="downloads/Research-Kit-Golden-Third.pdf">Short summary with figures to cite</a> (PDF) · <a href="downloads/Forschungs-Kit-Goldenes-Drittel.pdf">German version</a></li>
<li><a href="data/figures-to-cite.csv">Figures to cite</a> (CSV) · <a href="data/figures-to-cite.json">JSON</a></li>
<li><a href="data/">Result files</a> of the calculations shown (JSON; keys in German)</li>
</ul>
<h2>Figures to cite</h2>
{tabelle(["No.", "Item", "Value", "Unit", "Reference", "Status"], z, rechts=(2,))}
<p class="meta">"adopted": calculation under the decisions of the initiative; "check": cross-check or sensitivity. Please cite number and model version.
Euro amounts in purchasing power 2026 unless stated otherwise.</p>
<h2>Citation</h2>
<p>{html.escape(ZITAT)} {SEITE.replace("https://", "")}</p>
<p class="meta">DOI {F.DOI_KONZEPT} always resolves to the latest archived version. Archived versions: {", ".join(f"model version {v}: <a href=\"https://doi.org/{d}\">{d}</a>" for v, d in F.DOI_ARCHIV.items())}.
A working paper with its own DOI is in preparation.</p>"""
    return seite("kit.html", "Research kit", inhalt, "Figures to cite, result files and citation.")


def kit_html():
    zeilen = "".join(f"<tr><td>{x[0]}</td><td>{html.escape(x[1])}</td><td class=z><b>{wert(x[2])}</b></td><td>{x[3]}</td><td>{html.escape(x[4])}</td><td>{x[6]}</td></tr>"
                     for x in FIGURES)
    tz = "".join(f"<tr><td>{NAME[c]}</td><td class=z>{cur(c, V[c]['mehr_monat']['0.5'])}</td><td class=z>{cur(c, V[c]['mehr_monat']['1'])}</td>"
                 f"<td class=z>{cur(c, V[c]['mehr_monat']['2'])}</td><td class=z>{en(LS[c]['fonds']['zuschlag_pct'], 1)} %</td></tr>" for c in LAENDER)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><style>
body{{font:10.5pt/1.45 Georgia,serif;color:#1d2a33;margin:0}}h1{{font:700 20pt/1.2 Arial,sans-serif;color:#0f3b5c;margin:0 0 4pt}}
h2{{font:700 12.5pt/1.3 Arial,sans-serif;color:#0f3b5c;margin:14pt 0 4pt}}.meta{{font:8.5pt/1.4 Arial,sans-serif;color:#5a7186}}
table{{border-collapse:collapse;width:100%;font:8.5pt/1.35 Arial,sans-serif}}td,th{{border-bottom:.5pt solid #d8e1e8;padding:3pt 4pt;text-align:left;vertical-align:top}}
th{{color:#5a7186}}td.z{{text-align:right;white-space:nowrap}}ul{{margin:4pt 0}}
</style></head><body>
<h1>The Golden Third – research kit</h1>
<p class="meta">Initiative 28:28 · model version {VERSION} · {DATUM} · CC BY 4.0 · contact {KONTAKT}</p>
<h2>The proposal</h2>
<p>Taxation and social protection shared by a group of states: no euro of income taxed at more than one third (0/11/19/25/33 % in steps tied to basic
needs); social contributions abolished, employers pass at least 80 % of the contributions that disappear into wages; a strong safety net (health,
long-term care, minimum pension, basic needs) without premiums; a monthly transformation dividend for every adult; compulsory saving of 10 % into a
personal account locked until retirement; VAT as a label; legacy debt and pension promises in a common fund.</p>
<h2>Five reference countries, 2028 (single employee, change per month)</h2>
<table><thead><tr><th>Country</th><th>½ × av. wage</th><th>1 × av. wage</th><th>2 × av. wage</th><th>Legacy surcharge</th></tr></thead><tbody>{tz}</tbody></table>
<h2>Method and limits</h2>
<ul><li>One open chain of calculations, official statistics (Eurostat, OECD, national offices) and published surveys; every correction numbered in the log
({KORR} so far). Country models checked against OECD Taxing Wages 2026.</li>
<li>Static: no behavioural responses in labour supply, saving or migration; pass-through, avoidance and take-up as assumptions or bands. A qualitative
review of behavioural effects is available.</li>
<li>Three reviews commissioned by the initiative (October 2026), last covering version {GEPRUEFT}: calculation core confirmed, findings documented.
Later changes (up to {VERSION}) not yet reviewed. Independent review is invited.</li>
<li>Largest undocumented position: the base of company taxation where customers are.</li></ul>
<h2>Figures to cite</h2>
<table><thead><tr><th>No.</th><th>Item</th><th>Value</th><th>Unit</th><th>Reference</th><th>Status</th></tr></thead><tbody>{zeilen}</tbody></table>
<p class="meta">Origin of each figure (file and path): figures-to-cite.csv. "adopted": under the decisions of the initiative; "check": cross-check or sensitivity.</p>
<h2>Citation</h2><p>{html.escape(ZITAT)}</p>
</body></html>"""


def daten(ziel):
    kopf = ["id", "item", "value", "unit", "reference", "file_path", "status", "model_version"]
    with open(ziel / "data" / "figures-to-cite.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(kopf)
        for z in FIGURES:
            w.writerow(list(z) + [VERSION])
    (ziel / "data" / "figures-to-cite.json").write_text(json.dumps(
        dict(model_version=VERSION, date=DATUM, licence="CC BY 4.0", citation=ZITAT,
             figures=[dict(zip(kopf, list(z) + [VERSION])) for z in FIGURES]), ensure_ascii=False, indent=1), encoding="utf-8")
    import shutil
    for n in ("verrechnung_haushalte.json", "laenderseiten.json", "gini.json"):
        shutil.copy(F.AGG / n, ziel / "data" / n)


def nebenbei(ziel):
    seiten = ["", "households.html", "fund.html", "vat.html", "marginal.html", "reviews.html", "kit.html",
              "de/", "de/faelle-42000.html", "de/fonds.html", "de/mwst.html", "de/grenzbelastung.html", "de/pruefungen.html", "de/kit.html"]
    (ziel / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "".join(f"<url><loc>{PAGES}{s}</loc></url>\n" for s in seiten) + "</urlset>\n", encoding="utf-8")
    (ziel / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {PAGES}sitemap.xml\n", encoding="utf-8")
    (ziel / "CITATION.cff").write_text(f"""cff-version: 1.2.0
message: "Please cite the figure number (Z01–Z34) and the model version."
title: "The Golden Third – research kit and figures to cite"
type: dataset
authors:
  - name: "Initiative 28:28"
version: "{VERSION}"
license: CC-BY-4.0
url: "{PAGES}"
repository-code: "https://github.com/archicrowd/goldenes-drittel"
doi: "{F.DOI_KONZEPT}"
keywords: [tax policy, social protection, basic income, transformation dividend, microsimulation, public debt, Europe]
""", encoding="utf-8")
    (ziel / ".zenodo.json").write_text(json.dumps(dict(
        title=f"The Golden Third – research kit and figures to cite (model version {VERSION})", upload_type="dataset",
        description=("Calculations, reviews and citable figures (Z01–Z34) for the proposal 'The Golden Third': taxation and social protection shared by "
                     "a group of states. Static model; reviews commissioned by the initiative covered model versions up to " + GEPRUEFT + "."),
        creators=[dict(name="Initiative 28:28")], license="cc-by-4.0", version=VERSION, language="eng",
        keywords=["tax policy", "social protection", "basic income", "microsimulation", "public debt", "Europe"]), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def schreiben(ziel):
    for name, f in (("index.html", p_index), ("households.html", p_households), ("fund.html", p_fund), ("vat.html", p_vat),
                    ("marginal.html", p_marginal), ("reviews.html", p_reviews), ("kit.html", p_kit)):
        (ziel / name).write_text(f(), encoding="utf-8")
    daten(ziel)
    nebenbei(ziel)


def pdf(ziel):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        s = b.new_page()
        s.set_content(kit_html(), wait_until="load")
        s.pdf(path=str(ziel / "downloads" / "Research-Kit-Golden-Third.pdf"), format="A4", margin=dict(top="18mm", bottom="18mm", left="18mm", right="18mm"))
        b.close()
