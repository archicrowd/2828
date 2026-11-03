#!/usr/bin/env python3
"""Working Paper (englisch) aus den Ergebnisdateien, Logbuch v4.60.

Alle Zahlen kommen über forschung_bau / forschung_en aus daten/aggregate/ (keine Zahl von Hand). Ausgabe:
dokumente/working-paper/Golden-Third-Working-Paper.html und .pdf (Chromium). Prüfung in der Kette wie bei der Forschungsseite:
ohne --pdf schlägt die Stufe fehl, wenn sich der Text (ohne Datum) seit dem letzten PDF geändert hat.
"""
import hashlib, html, importlib.util, sys
from pathlib import Path

W = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("forschung_en_wp", W / "seite" / "werkzeuge" / "forschung_en.py")
E = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(E)
F = E.F
J = F.J
OUT = W / "dokumente" / "working-paper"
DATUM = "1 November 2026"
VERSION = F.VERSION
en, pm, cur, NAME, V, LS, G = E.en, E.pm, E.cur, E.NAME, E.V, E.LS, E.G
LAENDER = E.LAENDER

NZ0 = F.NZ["beschluss"]["reihe"][0]
NZ60 = [r for r in F.NZ["beschluss"]["reihe"] if r["jahr"] == 2060][0]
MR = J("moeglichkeitsraum33.json")["raum"]
KL = J("kuerzung_laender.json")
WS = J("weitergabe_sensitivitaet.json")["varianten"]
AW = J("ausweichen33.json")["faelle"]
FZ = F.FZ
GB = F.GB
MB = F.MB
RE = F.RE
MI_V = F.MI["basis"]["validierung_2025"]
BOD = F.RB["staaten"]["DE"]["boden_monat"]
KS = sorted((v["satz"], c) for c, v in KL["laender"].items())
TYP = list(E.TYP_EN)
import tomllib
DY = J("dynamik33.json")["szenarien"]
DYP = tomllib.loads((W / "modell" / "dynamik33.toml").read_text(encoding="utf-8"))


def dy(b, ki, kv):
    return [s for s in DY if s["beschaeftigung_pct"] == b and s["ki_pp"] == ki and s["kapital_verschiebung_pp"] == kv][0]


def t_objectives():
    d0, dk = dy(0.0, 0.0, 0.0), dy(0.0, 0.0, 3.0)
    gz = {z["brutto"]: z for z in GB["zeilen"]}
    gs = ", ".join(f"{c} {pm(G[c]['reihe'][0]['mitte'] - G[c]['gini_amtlich_2025'], 1)}" for c in LAENDER)
    z = [
     ["<b>Tax fairness</b>", "one ceiling of 33 % for all kinds of income; no contributions on wages only; profits taxed where customers are",
      f"Gini 2025 → 2028: {gs} points. Marginal burden at € 42,000 {en(gz[42000]['heute_pct'], 1)} → {en(gz[42000]['neu_2028_pct'], 1)} %; at € 100,000 "
      f"{en(gz[100000]['heute_pct'], 1)} → {en(gz[100000]['neu_2028_pct'], 1)} %. Effective burden per euro: labour {en(100 * DYP['belastung_arbeit_heute'])} → "
      f"{en(100 * DYP['belastung_arbeit_33'])} %, capital {en(100 * DYP['belastung_kapital_heute'])} → {en(100 * DYP['belastung_kapital_33'])} % (approximation)",
      "base of company taxation where customers are; avoidance at the top only as a band"],
     ["<b>Intergenerational fairness</b>", "legacy debt and pension promises in a fund repaid by 2098; pension promises above basic need reduced; own funded account",
      f"fund {en(F.FG['beitrag_pct_bip'], 2)} % of GDP until {F.FG['zieljahr']}, peak {en(F.FG['schuldenquote_spitze'], 1)} % ({F.FG['spitzenjahr']}); "
      f"German pensioner households: mean {en(RE['mittel_monat'])} € per month, lowest fifth {pm(RE['fuenftel_monat'][0])} €, highest fifth {en(RE['fuenftel_monat'][4])} €",
      "no generational accounting by birth cohort; dividend path of later cohorts only as average"],
     ["<b>Climate</b>", "carbon price and 33 % rate on harmful goods returned as a dividend; lower VAT for certified goods",
      f"steering revenue {en(NZ0['lenkung_pct_bip'], 2)} % of GDP (2028) → {en(NZ60['lenkung_pct_bip'], 2)} % (2060); dividend "
      f"{en(NZ0['dividende_pct_bip'], 2)} → {en(NZ60['dividende_pct_bip'], 2)} % of GDP",
      "emissions are an exogenous path; no estimate of emission reductions caused by the rules"],
     ["<b>Digital transformation of work</b>", "social protection financed from all income, not from wages; dividend and net independent of employment; platforms taxed where customers are",
      f"shift of 3 GDP points from labour to capital income by 2060: revenue today {pm(dk['heute_aufkommen_aenderung_2060_pct_bip'], 2)} % of GDP, "
      f"new system {pm(dk['reihe']['2060']['aufkommen_aenderung_33_pct_bip'], 2)} %; dividend 2060 {pm(100 * (dk['reihe']['2060']['dividende_erw_eur2026'] / d0['reihe']['2060']['dividende_erw_eur2026'] - 1))} % (Table 12)",
      "scenario assumptions; platform revenue not quantified separately"],
    ]
    return tab(["Objective", "Rules that serve it", "Indicator in the model (Germany unless stated)", "Not covered"], z,
               notiz="Effective burden per euro: today tax wedge on labour (OECD) against flat capital income tax in Germany; new system revenue relative to "
                     "the income base (dynamik33.toml, approximation). Marginal burden: single, Germany, without compulsory saving.")


LABEL = [("A+", 5, "basic needs, repairs, circular products"), ("A", 11, "certified sustainable goods"), ("B", 17, "standard goods"),
         ("C", 25, "resource-intensive goods"), ("Special", 33, "harmful goods (e.g. combustion-engine vehicles, tobacco, alcohol)")]


def t_label():
    b = 1.17
    z = [[k, f"{s} %", d, pm(100 * ((1 + s / 100) / b - 1), 1) + " %", pm(100 * (b / (1 + s / 100) - 1), 1) + " %"] for k, s, d in LABEL]
    return tab(["Class", "Rate", "Goods (examples)", "Price vs B (1)", "Revenue vs B (2)"], z,
               rechts=(1, 3, 4),
               notiz="(1) Consumer price relative to class B at the same net price. (2) Supplier net revenue relative to class B at the same consumer price. Mechanical price signals from the rates alone. Which share of a rate difference reaches consumers or stays with suppliers depends on "
                     "pass-through, which is asymmetric for VAT changes (Benzarti et al. 2020). Assignment of goods to classes is set by law; lower classes "
                     "A+ and A are reached through certification.")


def t_digital():
    zeilen = []
    base = dy(0.0, 0.0, 0.0)["reihe"]["2060"]["dividende_erw_eur2026"]
    for b, ki, kv, name in [(0.0, 0.0, 0.0, "Baseline"), (0.0, 0.0, 3.0, "Capital share +3 points"), (0.0, 0.07, 0.0, "AI productivity +0.07 pp/year"),
                            (0.0, 0.3, 0.0, "AI productivity +0.3 pp/year"), (0.0, 0.6, 0.0, "AI productivity +0.6 pp/year"),
                            (2.8, 0.0, 0.0, "Employment +2.8 %"), (4.6, 0.3, 3.0, "Employment +4.6 %, AI +0.3, capital +3")]:
        s = dy(b, ki, kv)
        d = s["reihe"]["2060"]["dividende_erw_eur2026"]
        zeilen.append([name, pm(100 * (d / base - 1)) + " %", en(s["fondsbeitrag_naeherung_pct_bip"], 2)])
    return tab(["Scenario (2060)", "Dividend vs baseline", "Fund contribution (% GDP)"], zeilen, rechts=(1, 2),
               notiz="dynamik33.json. AI range: Acemoglu (2024) to Filippucci, Gal and Schief (2024); employment from lower labour costs and lower marginal "
                     "burden with assumed elasticities; capital share shift: assumption. Fund contribution as approximation.")


def tab(kopf, zeilen, rechts=(), notiz=""):
    th = "".join(f'<th{" class=z" if i in rechts else ""}>{k}</th>' for i, k in enumerate(kopf))
    tr = "".join("<tr>" + "".join(f'<td{" class=z" if i in rechts else ""}>{x}</td>' for i, x in enumerate(z)) + "</tr>" for z in zeilen)
    n = f'<p class="note">{notiz}</p>' if notiz else ""
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>{n}"


def t_households():
    z = []
    for c in LAENDER:
        for t in TYP:
            m = V[c]["mehr_monat_typen"][t]
            z.append([NAME[c] if t == TYP[0] else "", E.TYP_EN[t], cur(c, m["0.5"]), cur(c, m["1"]), cur(c, m["2"]), f"{V[c]['anteil_mehr'][t]} %"])
    return tab(["Country", "Household", "½ × AW", "1 × AW", "2 × AW", "Better off"], z, rechts=(2, 3, 4, 5),
               notiz=f"Change in monthly disposable income, 2028, purchasing power 2026; Poland in złoty. AW: average wage, OECD Taxing Wages 2024 ({E.AW_TEXT}). "
                     "Better off: share of employees of this household type across the wage distribution; the German wage distribution is scaled to each "
                     "country's average wage (assumption). Each country carries its own legacy surcharge after netting in the common fund.")


def t_gini():
    z = [[NAME[c], en(G[c]["gini_amtlich_2025"], 1), en(G[c]["reihe"][0]["mitte"], 1), pm(G[c]["reihe"][0]["mitte"] - G[c]["gini_amtlich_2025"], 1),
          en(LS[c]["fonds"]["zuschlag_pct"], 1) + " %"] for c in LAENDER]
    return tab(["Country", "Gini 2025 (official)", "Gini 2028 (model)", "Change", "Legacy surcharge 2028"], z, rechts=(1, 2, 3, 4),
               notiz="Gini coefficient of equivalised disposable income (0–100). 2025: Eurostat ilc_di12 (EU-SILC 2025). 2028: official value plus the change "
                     "computed in the model from the decile distribution (Eurostat ilc_di01); not a microsimulation except for Germany.")


def t_validation():
    z = [[NAME[c], en(x["allein_100"]["modell_keil"], 1), en(x["allein_100"]["oecd_keil"], 1), pm(x["allein_100"]["abw_pp"], 1),
          en(x["paar_ein_einkommen_2k"]["modell_keil"], 1), en(x["paar_ein_einkommen_2k"]["oecd_keil"], 1), pm(x["paar_ein_einkommen_2k"]["abw_pp"], 1)]
         for c, x in F.VL["keil"].items()]
    return tab(["Country", "Single: model", "OECD", "Diff. (pp)", "Couple, 2 ch.: model", "OECD", "Diff. (pp)"], z, rechts=(1, 2, 3, 4, 5, 6),
               notiz="Tax wedge in % of labour costs at the average wage. Model: 2026 law; OECD: Taxing Wages 2026 (2025 data).")


def t_net():
    pos = {"Gesundheit (Grundversorgung)": "Health care (basic coverage)", "Pflege (Teilkasko)": "Long-term care (partial)",
           "Grundrente (ab 67)": "Minimum pension (67+)", "Invalidität (Grundbedarf)": "Disability (basic need)",
           "Arbeitslosigkeit (Grundbedarf)": "Unemployment (basic need)", "Waisen": "Orphans", "Härtefall": "Hardship (housing, special needs)"}
    z = [[pos.get(k, k), en(NZ0["positionen"][k], 2), en(NZ60["positionen"][k], 2)] for k in NZ0["positionen"]]
    z.append(["<b>Strong net, total</b>", f"<b>{en(NZ0['netz_pct_bip'], 2)}</b>", f"<b>{en(NZ60['netz_pct_bip'], 2)}</b>"])
    z.append(["Transformation dividend", en(NZ0["dividende_pct_bip"], 2), en(NZ60["dividende_pct_bip"], 2)])
    z.append(["of which financed by steering taxes", en(NZ0["lenkung_pct_bip"], 2), en(NZ60["lenkung_pct_bip"], 2)])
    return tab(["Germany, % of GDP", "2028", "2060"], z, rechts=(1, 2),
               notiz="netz33.json (decision path). Quantities (pensioners, disabled, unemployed) and the reduction of the benefit catalogue are assumptions.")


def t_fund():
    vz = FG_V = F.FG["verrechnung"]["laender"]
    z = [[NAME[c], en(vz[c]["reihe"]["2028"]["beitrag_pct_bip"], 2), en(vz[c]["reihe"]["2028"]["zuschlag_pct"], 1)] for c in LAENDER]
    return tab(["State", "Contribution 2028 (% GDP)", "Surcharge 2028 (%)"], z, rechts=(1, 2),
               notiz=f"After netting in the common fund; converging to the common rate ({en(F.FG['zuschlag_auf_alle_steuern_pct'], 1)} %) by 2058.")


def t_interest():
    nm = lambda s: s.replace("fest ", "fixed ").replace("Übergang", "transition")
    z = [[nm(v["fall"]), en(v["beitrag_pct_bip"], 2), en(v["zuschlag_pct"], 1), pm(v["haushalt_de"]["mehr_monat_42000"]["alleinstehend"]) + " €"] for v in FZ["varianten"]]
    return tab(["Fund interest", "Contribution (% GDP)", "Surcharge (%)", "DE single, € 42,000"], z, rechts=(1, 2, 3),
               notiz=f"Nominal growth {en(FZ['wachstum_nominal'], 1)} %. Market yields October 2026 (secondary sources): German federal bonds "
                     f"{en(FZ['markt_oktober_2026']['bund_10j'], 2)} %, EU bonds {en(FZ['markt_oktober_2026']['eu_10j'], 2)} %.")


def t_grid():
    z = [[en(r["zins"], 2) + " %", en(r["wachstum"], 1) + " %", en(r["beitrag_pct_bip"], 2), en(r["zuschlag_pct"], 1),
          en(r["beschlussbeitrag_fest"]["restschuld_2098_zehn"], 1)] for r in FZ["zins_wachstum"]]
    return tab(["Interest", "Nominal growth", "Contribution (% GDP)", "Surcharge (%)", "Debt 2098 at fixed contribution (% GDP)"], z, rechts=(2, 3, 4),
               notiz="Contribution and surcharge needed for repayment by 2098; last column: remaining debt (ten states) if the contribution stays at the adopted value.")


def t_passthrough():
    z = []
    for k in ("0.0", "0.5", "0.8", "1.0"):
        a = WS[k]["anteil_mit_mehr"]
        z.append([f"{int(float(k) * 100)} %", pm(WS[k]["de_mehr_monat"]["alleinstehend"]["42000"]) + " €"] + [f"{a[c]['alleinstehend']} %" for c in LAENDER])
    return tab(["Pass-through", "DE single € 42,000"] + [f"Better off {c}" for c in LAENDER], z, rechts=tuple(range(1, 7)),
               notiz="Share of the employer contributions that disappear which is passed into gross wages; the remainder stays with the employer. "
                     "Better off: single employees. 80 % is the adopted value (legal obligation with fallback rule).")


def t_marginal():
    z = [[en(r["brutto"]) + " €", en(r["heute_pct"], 1), " / ".join(en(r["heute_bereinigt_pct"][a], 1) for a in ("0.5", "1.0")),
          en(r["neu_2028_pct"], 1), en(r["neu_2028_mit_vorsorge_pct"], 1)] for r in GB["zeilen"] if r["brutto"] in (20000, 42000, 60000, 100000, 250000)]
    return tab(["Gross wage", "Today", "Today, adjusted (0.5 / 1)", "New 2028", "New incl. compulsory saving"], z, rechts=(1, 2, 3, 4),
               notiz="Germany, single, % per additional euro of gross wage. Adjusted: the part of the pension contribution that creates an own entitlement "
                     "is treated as saving (equivalence 0.5 or 1, assumption). Employer side and means-tested benefits not included.")


def t_vat():
    z = [[k["klasse"].replace(">=", "≥ ") + " €", en(k["phi"]["mit_vorsteuer"][0], 2)] for k in F.MV["klassen"]]
    fr = F.ML["staaten"]["FR"]["fuenftel"]
    z2 = [[f"Q{q['fuenftel']}", en(q["phi"][0], 2)] for q in fr]
    return (tab(["Germany: household net income per month", "Factor"], z, rechts=(1,),
                notiz="EVS 2023. Factor: additional VAT burden relative to the mean, as share of consumption.")
            + tab(["France: income quintile", "Factor"], z2, rechts=(1,), notiz="Eurostat HBS 2020 (hbs_str_t223, values flagged as estimated)."))


def t_figures():
    z = [[x[0], html.escape(x[1]), f"<b>{E.wert(x[2])}</b>", x[3], x[6]] for x in E.FIGURES]
    return tab(["No.", "Item", "Value", "Unit", "Status"], z, rechts=(2,),
               notiz=f"Source file and path of each figure: figures-to-cite.csv in the research kit (DOI {F.DOI_KONZEPT}). "
                     "adopted: under the decisions of the initiative; check: cross-check or sensitivity.")


REFS = [
 "Acemoglu, D. (2024): The Simple Macroeconomics of AI. NBER Working Paper 32487.",
 "Benzarti, Y., Carloni, D., Harju, J., Kosonen, T. (2020): What Goes Up May Not Come Down: Asymmetric Incidence of Value-Added Taxes. Journal of Political Economy 128(12).",
 "Bhargava, S., Manoli, D. (2015): Psychological Frictions and the Incomplete Take-Up of Social Benefits. American Economic Review 105(11).",
 "Bick, A., Fuchs-Schündeln, N. (2018): Taxation and Labour Supply of Married Couples across Countries. Review of Economic Studies 85(3).",
 "Chetty, R., Friedman, J., Leth-Petersen, S., Nielsen, T., Olsen, T. (2014): Active vs. Passive Decisions and Crowd-Out in Retirement Savings Accounts. Quarterly Journal of Economics 129(3).",
 "Chetty, R., Looney, A., Kroft, K. (2009): Salience and Taxation: Theory and Evidence. American Economic Review 99(4).",
 "Council of the European Union (2022): Council Directive (EU) 2022/542 of 5 April 2022 amending Directives 2006/112/EC and (EU) 2020/285 as regards rates of value added tax. Official Journal L 107.",
 "Court of Justice of the European Union (2022): Case C-515/20, B & L Elektrotechnik (reduced VAT rates and the principle of fiscal neutrality); cited after a secondary source.",
 "DREES (2022): Mesurer régulièrement le non-recours au RSA et à la prime d'activité. Les Dossiers de la DREES 92.",
 "Dranove, D., Jin, G. Z. (2010): Quality Disclosure and Certification: Theory and Practice. Journal of Economic Literature 48(4).",
 "Douenne, T., Fabre, A. (2022): Yellow Vests, Pessimistic Beliefs, and Carbon Tax Aversion. American Economic Journal: Economic Policy 14(1).",
 "Eurofound (2015): Access to social benefits: Reducing non-take-up. Luxembourg: Publications Office of the European Union.",
 "Eurostat: datasets gov_10a_exp, gov_10a_taxag, gov_10dd_edpt1, nama_10_gdp, nasa_10_pens1, demo_pjanind, une_rt_a, prc_ppp_ind (retrieved 17 October 2026); ilc_di12, ilc_di01 (EU-SILC 2025, retrieved 18 October 2026); hbs_str_t223 (Household Budget Survey 2020, retrieved 24 October 2026).",
 "Filippucci, F., Gal, P., Schief, M. (2024): Miracle or myth? Assessing the macroeconomic productivity gains from artificial intelligence. OECD; summary on VoxEU, 8 December 2024.",
 "Jakobsen, K., Jakobsen, K., Kleven, H., Zucman, G. (2020): Wealth Taxation and Wealth Accumulation: Theory and Evidence from Denmark. Quarterly Journal of Economics 135(1).",
 "Jones, D., Marinescu, I. (2022): The Labor Market Impacts of Universal and Permanent Cash Transfers: Evidence from the Alaska Permanent Fund. American Economic Journal: Economic Policy 14(2).",
 "Kleven, H., Landais, C., Saez, E., Schultz, E. (2014): Migration and Wage Effects of Taxing Top Earners. Quarterly Journal of Economics 129(1).",
 "Madrian, B., Shea, D. (2001): The Power of Suggestion: Inertia in 401(k) Participation and Savings Behavior. Quarterly Journal of Economics 116(4).",
 "Mildenberger, M., Lachapelle, E., Harrison, K., Stadelmann-Steffen, I. (2022): Limited impacts of carbon tax rebate programmes on public support for carbon pricing. Nature Climate Change 12(2).",
 "OECD (2025): Taxing Wages 2025. Paris: OECD Publishing. – OECD (2026): Taxing Wages 2026. Paris: OECD Publishing.",
 "Potter, C., Bastounis, A., Hartmann-Boyce, J., Stewart, C., Frie, K., Tudor, K., Bianchi, F., Cartwright, E., Cook, B., Rayner, M., Jebb, S. A. (2021): The Effects of Environmental Sustainability Labels on Selection, Purchase, and Consumption of Food and Drink Products: A Systematic Review. Environment and Behavior 53(8).",
 "Saez, E., Schoefer, B., Seim, D. (2019): Payroll Taxes, Firm Behavior, and Rent Sharing: Evidence from a Young Workers' Tax Cut in Sweden. American Economic Review 109(5).",
 "Statistisches Bundesamt (Destatis): Einkommens- und Verbrauchsstichprobe (EVS) 2023, Konsumausgaben privater Haushalte.",
 "STM – Ministry of Social Affairs and Health, Finland (2020): Results of Finland's basic income experiment.",
 "Umweltbundesamt et al. (2026): Projektionsbericht 2026 für Deutschland (with-measures scenario, transport).",
 "Vivalt, E., Rhodes, E., Bartik, A., Broockman, D., Miller, S. (2024): The Employment Effects of a Guaranteed Income: Experimental Evidence from Two U.S. States. NBER Working Paper 32719.",
 "World Justice Project (2025): Rule of Law Index 2025. Washington, DC.",
]


def text():
    eu = ("DE", "FR", "IT", "ES")
    g42 = [F.fall(2028, t, 0.8, F.ZU_DE, 0.1)["differenz_monat"] for t in F.TYPEN]
    av = AW
    worst = min(av, key=lambda f: f["dividende_2028_eur"])
    best = max(av, key=lambda f: f["dividende_2028_eur"])
    v35 = [v for v in FZ["varianten"] if v["fall"] == "fest 3.5 %"][0]
    pn = F.PN["reihe"][0]
    s0 = WS["0.0"]
    gz100 = [z for z in GB["zeilen"] if z["brutto"] == 100000][0]
    gz250 = [z for z in GB["zeilen"] if z["brutto"] == 250000][0]
    dk = dy(0.0, 0.0, 3.0)
    gmin = min(LAENDER, key=lambda c: G[c]["reihe"][0]["mitte"] - G[c]["gini_amtlich_2025"])
    return f"""
<header class="titel">
<p class="kicker">Working paper · for discussion</p>
<h1>The Golden Third</h1>
<p class="sub">A static costing and distributional model of a shared tax and social-protection framework for a group of European states</p>
<p class="autor">Initiative 28:28</p>
<p class="meta">Model version {VERSION} · {DATUM} · Licence CC BY 4.0 · Research kit and figures to cite: <a href="https://doi.org/{F.DOI_KONZEPT}">doi.org/{F.DOI_KONZEPT}</a>
· Website: <a href="{F.PAGES}">{F.PAGES.replace("https://", "")}</a> · Contact: {F.KONTAKT}</p>
</header>

<section class="abstract"><h2>Abstract</h2>
<p>We describe a proposal under which a group of states adopts common rules for income taxation and social protection, and we document a
transparent, static model of its costs and distributional effects. The proposal pursues four objectives: tax fairness across labour, capital and
automation; fairness between generations; coping with climate change; and coping with the digital transformation of work. Income of every kind is taxed in steps of 0, 11, 19, 25 and 33 per cent tied to
each country's basic need; social contributions are abolished and employers must pass at least 80 per cent of the employer contributions that
disappear into wages; a tax-financed safety net covers health care, long-term care and basic needs; every adult receives a monthly transformation
dividend; 10 per cent of gross wages go into a personal, locked pension account; and public debt and unfunded pension promises are moved into a
common fund repaid by 2098. For 2028, in purchasing power of 2026, a single employee at the average wage gains between
{en(min(V[c]['mehr_monat']['1'] for c in eu))} € and {en(max(V[c]['mehr_monat']['1'] for c in eu))} € per month in Germany, France, Italy and Spain and
{en(V['PL']['mehr_monat']['1'])} zł in Poland. The Gini coefficient falls in all five countries, by {en(-(G[gmin]['reihe'][0]['mitte'] - G[gmin]['gini_amtlich_2025']), 1)} points
at most. The common fund requires {en(F.FG['beitrag_pct_bip'], 2)} per cent of GDP a year, a surcharge of {en(F.FG['zuschlag_auf_alle_steuern_pct'], 1)} per cent on
all taxes at an interest rate of {en(F.FG['zins'], 2)} per cent, and peaks at {en(F.FG['schuldenquote_spitze'], 1)} per cent of GDP in {F.FG['spitzenjahr']}.
Losers are German pensioner households (only {en(RE['anteil_mehr_pct'], 1)} per cent better off), single earners in France at half the average wage, and
one-earner couples at twice the average wage. The model has no behavioural responses; the main uncertainties are the pass-through of employer
contributions, the fund interest rate and the tax base of company profits taxed where customers are. Measured against its objectives, the
model supports the claims on distribution and on the robustness of revenue to a shift from labour to capital income; it shows tensions between
climate success and the size of the dividend, and between legacy repayment and today's pensioners; and it cannot yet show effects on emissions.</p>
<p class="kw"><b>Keywords:</b> tax reform, social protection, basic income, transformation dividend, payroll tax incidence, public debt, Europe.
<b>JEL:</b> H20, H24, H55, H63, I38.</p>
</section>

<h2>1 Introduction</h2>
<p>Most European states finance social protection to a large extent through contributions levied on wages, combine them with progressive income
taxes and an array of means-tested benefits, and carry public debt and unfunded pension promises from the past. The resulting systems are
complex, and the marginal burden on additional earnings is high in parts of the income distribution. The proposal examined here – named
<i>The Golden Third</i> after its upper tax rate of one third – replaces this structure with a small number of common rules that a group of states
could adopt jointly.</p>
<p>This paper does not derive an optimal tax system. It is a costing and distributional accounting exercise: given the rules, what does the
system cost, who gains and who loses compared with the law of 2026, and how sensitive are these results to the main assumptions? All figures come
from one calculation chain of {F.STUFEN} stages based on official statistics. Every change to the model is recorded in a log, and every error found is
numbered as a correction ({F.KORREKTUREN} so far). The chain was recalculated in three internal reviews, carried out with a different AI model from the one used to build the calculation; the last review covered
model version {F.GEPRUEFT} (section 10).</p>
<p>Section 2 states the objectives, section 3 the rules, section 4 the model and data, section 5 the results, section 6 the sensitivity to key
assumptions. Section 7 assesses the results against the objectives, including the tensions between them. Section 8 summarises behavioural evidence
that the static model does not capture, section 9 limitations and open questions, section 10 the review history.</p>

<h2>2 Objectives</h2>
<p>The initiative states four objectives. They are normative choices of the initiative; this paper does not argue for them but asks whether the rules
are consistent with them and what the model can show.</p>
<p><b>Tax fairness.</b> Today labour carries most of the burden: in Germany the tax wedge on an average wage is about
{en(F.VL['keil']['DE']['allein_100']['oecd_keil'], 1)} % of labour costs (OECD 2026), while capital income is taxed at a flat rate of about 26 %. Social
contributions fall on human work only, so replacing work by machines saves contributions. The proposal treats labour, capital and automation alike:
no income is taxed at more than one third, without deductions, and company profits – explicitly including digital platforms – are taxed where the
customers are, because profits can be shifted but customers cannot. Fairness is also vertical: a floor at basic need and a dividend for everyone.</p>
<p><b>Intergenerational fairness.</b> Public debt and unfunded pension promises are commitments made by earlier generations that today's
systems pass on to later ones. The proposal makes them explicit, moves them into a common fund and repays them by 2098. Pension promises above
basic need are reduced, so that today's pensioners carry a share; basic need is guaranteed. New saving for old age is funded on an own account
rather than promised by later contributors. The dividend is justified as a share for everyone in what earlier generations built – knowledge,
technology, infrastructure.</p>
<p><b>Climate change.</b> The proposal relies on economic incentives rather than on control of individual products and firms. A carbon price
and a special VAT rate of 33 % on harmful goods make harmful consumption more expensive; their revenue is returned to everyone through the
dividend, so that households that consume little gain. VAT becomes a label with five classes. Suppliers move their products into lower classes by
certification at approved bodies under state supervision: the state supervises the certifiers, not each product. The intended result is a
competition for sustainability in which a lower rate is a price advantage that suppliers earn. The dividend shrinks as emissions fall; the
initiative regards this as intended.</p>
<p><b>Digital transformation of work.</b> If more output is produced by machines and software and less by paid work, systems financed from wages
lose their base and tie protection to employment that becomes less stable. The proposal finances social protection from all income, makes the
net and the dividend independent of employment, keeps the pension account portable across jobs, and taxes platforms where their customers are.
The dividend is meant to give everyone a share of what automation and digitalisation bring in.</p>

<h2>3 The proposal</h2>
<table><tbody>
<tr><td><b>Income tax</b></td><td>Rates 0 / 11 / 19 / 25 / 33 % in brackets defined as multiples of each country's basic need. Gross income without
deductions; individual taxation (no splitting or family quotient). Capital income, profits and inheritance are taxed at most at 33 %; company
profits are taxed where customers are, including digital platforms.</td></tr>
<tr><td><b>Contributions</b></td><td>Social contributions are abolished. Employers are legally obliged to pass at least 80 % of the employer
contributions to social security that disappear into gross wages, up to six times basic need; a fallback rule applies if contracts are not adjusted
by the start date.</td></tr>
<tr><td><b>Strong net</b></td><td>Health care, long-term care (partial), minimum pension, basic needs in disability and unemployment, financed from
general taxes. A floor equal to basic need times an equivalence scale (0.5 for each further adult, 0.55 per child) is guaranteed; own earnings
count by half. In Germany the floor is {en(BOD['alleinstehend'])} € per month for a single person (2028, purchasing power 2026). Low earners are topped
up on an application that the authority pre-fills.</td></tr>
<tr><td><b>Dividend</b></td><td>Monthly payment to every adult, 80 % for children, without application; financed from steering taxes (carbon and
other) and from gains of digitalisation. It falls as emissions fall.</td></tr>
<tr><td><b>Own route</b></td><td>Compulsory saving of 10 % of gross wages into a personal account, locked until retirement age, with few investment
options and a default fund.</td></tr>
<tr><td><b>VAT label</b></td><td>Rates 5 / 11 / 17 / 25 %, special rate 33 % only for harmful goods. Suppliers obtain lower rates through certification
by supervised bodies.</td></tr>
<tr><td><b>Legacy</b></td><td>Public debt and unfunded pension promises above the dividend move into a common fund of the participating states,
financed by a surcharge on all taxes. Existing pension promises above basic need are reduced by 15 %; own savings are not reduced (pension rule E).
The effective reduction of pension payments differs by state, from {en(100 * KS[0][0], 1)} % to {en(100 * KS[-1][0], 1)} %
({en(100 * KL['kuerzung_de'], 2)} % in Germany).</td></tr>
</tbody></table>

<h2>4 Model and data</h2>
<p><b>Scope.</b> The calculations cover a possibility space of {MR['staaten']} European states with {en(MR['einwohner_mio'], 1)} million inhabitants and a GDP of
{en(MR['bip_mrd_eur_2024'])} billion euro (2024). Ten states are calculated in detail; the common fund of 30 states is the decision of the ten scaled by the
ratio 30/10 from the possibility space (assumption). Household results are computed for five reference countries: Germany, France, Italy, Spain and
Poland.</p>
<p><b>Revenue and expenditure.</b> Tax bases (wages, profits, consumption, wealth, inheritance) and current expenditure come from Eurostat national and
government accounts (gov_10a_exp, gov_10a_taxag, nama_10_gdp); unfunded pension claims from the supplementary pension tables (nasa_10_pens1, table 29);
debt from gov_10dd_edpt1. The tax base of company profits taxed where customers are is the largest position that is not yet documented against an
independent source.</p>
<p><b>Households today.</b> Each reference country has a simplified model of 2026 law: income tax, employee and employer contributions and cash benefits
including minimum income schemes (Germany: Bürgergeld approximation with housing and child supplements; France: APL and prime d'activité; Italy:
Assegno di Inclusione; Spain: Ingreso Mínimo Vital and child supplement; Poland: zasiłek okresowy). Parameters come partly from official sources and
partly from secondary sources; the parameter files mark each block as official, secondary or assumption. The models were checked against the OECD
tax wedge: {F.VL['bestanden'].split(' ')[0]} of 10 household types lie within ±2 percentage points (Table 3).</p>
<p><b>Germany.</b> A synthetic microsimulation, calibrated to official totals, covers employees, civil servants, self-employed, minimum-income recipients
and pensioners. Validation against 2025: gross wages {pm(MI_V['bruttolohnsumme']['abweichung_pct'], 1)} %, wage tax {pm(MI_V['lohnsteuer']['abweichung_pct'], 1)} %.
Pensioner incomes come from EU-SILC 2025 and the German old-age income survey (ASID 2023), both as published aggregates. No micro data are used.</p>
<p><b>Distribution.</b> The Gini coefficient for 2028 is the official value for 2025 (EU-SILC) plus the change computed on the published decile
distribution. VAT burdens by income come from the German household budget survey (EVS 2023) and, for France, from Eurostat's Household Budget Survey
2020; Italy, Spain and Poland use a factor of 1 so far.</p>
<p><b>Conventions.</b> Amounts for 2028 are in purchasing power of 2026. The model is static: labour supply, saving, prices beyond a one-off level effect
and migration do not respond. Pass-through of employer contributions, take-up, avoidance and VAT incidence enter as parameters or bands. Take-up of
the floor is assumed to be complete.</p>

<h2>5 Results</h2>
<h3>5.1 Households in five countries</h3>
<p>Table 1 shows the change in disposable income for three household types at half, once and twice the average wage. In Germany a single employee
at the average wage gains {pm(V['DE']['mehr_monat']['1'])} € per month; at a gross wage of € 42,000, about two thirds of the average wage, the gain is
{pm(g42[0])} € for a single person, {pm(g42[1])} € for a single parent and {pm(g42[2])} € for a one-earner couple with two children.</p>
<p class="cap">Table 1: Change in monthly disposable income, 2028</p>
{t_households()}
<p>Three patterns stand out. First, one-earner couples with higher wages lose part of today's joint taxation (German splitting, French quotient familial),
because every adult is taxed individually and receives an own dividend; around twice the average wage the gain is close to zero in Germany
({pm(V['DE']['mehr_monat_typen'][TYP[2]]['2'])} €) and France ({pm(V['FR']['mehr_monat_typen'][TYP[2]]['2'])} €). Second, single earners in France at half the
average wage lose {en(-V['FR']['mehr_monat']['0.5'])} € per month: today's in-work benefit and family allowances are replaced by the dividend and the floor,
and employer contributions near the minimum wage are already largely waived today, so little is passed on. Third, in Italy, Spain and Poland, where
minimum income schemes reach fewer households today, the floor and the dividend raise low incomes more strongly.</p>
<p class="cap">Table 2: Inequality and legacy surcharge</p>
{t_gini()}
<p class="cap">Table 3: Validation of the country models against the OECD tax wedge</p>
{t_validation()}
<p class="note">Poland: the OECD counts neither accident insurance nor the labour and guarantee funds on the employer side, and treats the health
contribution differently (open). France, couple: the model pays the prime d'activité at this wage level, consistent with ministry examples for the 2026
reform; the OECD apparently does not (to be checked).</p>

<h3>5.2 Germany: all households and pensioners</h3>
<p>In the German microsimulation {en(MB['erwerbsfaehige_haushalte']['anteil_mehr_haushalte_pct'], 1)} % of working-age households and
{en(MB['gesamt']['anteil_mehr_haushalte_pct'], 1)} % of all households are better off. By status of the main earner: full-time
{en(MB['status']['Hauptperson Vollzeit']['anteil_mehr_haushalte_pct'], 1)} %, part-time {en(MB['status']['Hauptperson Teilzeit']['anteil_mehr_haushalte_pct'], 1)} %,
self-employed {en(MB['status']['Hauptperson selbständig']['anteil_mehr_haushalte_pct'], 1)} %, civil servants
{en(MB['status']['Hauptperson Beamte']['anteil_mehr_haushalte_pct'], 1)} %, mini-job {en(MB['status']['Hauptperson Minijob']['anteil_mehr_haushalte_pct'], 1)} %,
households without earnings {en(MB['status']['ohne Erwerb (Bürgergeld)']['anteil_mehr_haushalte_pct'], 1)} %. Under pension rule E,
{en(RE['anteil_mehr_pct'], 1)} % of pensioner households are better off; the mean change is {en(RE['mittel_monat'])} € per month, from
{pm(RE['fuenftel_monat'][0])} € in the lowest to {en(RE['fuenftel_monat'][4])} € in the highest fifth. Pensioners lose because their contributions to health
and long-term care disappear while pension promises above basic need are reduced, and because the dividend does not fully replace these amounts in
the upper part of the distribution.</p>

<h3>5.3 Public finances</h3>
<p>Table 4 shows the strong net and the dividend for Germany. The dividend amounts to {en(F.DIV_ERW)} € per adult and {en(F.DIV_ERW * 0.8)} € per child and
month in 2028 (Table 4 shows the dividend in per cent of GDP). Its share of GDP falls from {en(NZ0['dividende_pct_bip'], 2)} % in 2028 to {en(NZ60['dividende_pct_bip'], 2)} % in 2060 because
steering revenue falls with emissions. The total burden of taxes and fund is {en(F.ZR['a_steuern_und_fonds'], 1)} % of GDP in 2028 against
{en(F.GL['heute'], 2)} % today (Eurostat 2024); including compulsory saving, which goes to an own account, it is {en(F.ZR['b_mit_pflichtvorsorge'], 1)} %.</p>
<p class="cap">Table 4: Strong net and dividend, Germany</p>
{t_net()}
<p>The common fund takes over public debt and pension claims above the dividend (on average {en(F.AL['beschluss']['verhandlungsmasse_z_2028_pct_bip'], 2)} % of
GDP in 2028). At a fund interest rate of {en(F.FG['zins'], 2)} % – the euro-area average of 2006–2025 – it requires {en(F.FG['beitrag_pct_bip'], 2)} % of GDP a
year, financed by a surcharge of {en(F.FG['zuschlag_auf_alle_steuern_pct'], 1)} % on all taxes. Its debt peaks at {en(F.FG['schuldenquote_spitze'], 1)} % of GDP in
{F.FG['spitzenjahr']} and is repaid in {F.FG['zieljahr']}. Netting by state means that states with larger legacies carry a higher surcharge until 2058
(Table 5).</p>
<p class="cap">Table 5: Contribution and surcharge by state after netting</p>
{t_fund()}

<h3>5.4 VAT label and price level</h3>
<p>The additional VAT burden is moderately progressive: relative to the mean it ranges from {en(F.MV['klassen'][0]['phi']['mit_vorsteuer'][0], 2)} in the
lowest to {en(F.MV['klassen'][-1]['phi']['mit_vorsteuer'][0], 2)} in the highest German income class, because rent, health, education and insurance are exempt
(Table 6). The one-off price-level effect in 2028 is {en(pn['mechanisch_pct'], 2)} % mechanically and {en(pn['mwst_spanne_pct'][0], 1)} to
{en(pn['mwst_spanne_pct'][1], 1)} % with partial pass-through on taxable consumption only. VAT increases are passed on more strongly than cuts
(Benzarti et al. 2020), so the upper end of the band is more likely; an asymmetric variant is not yet computed.</p>
<p class="cap">Table 6: VAT label burden by income</p>
{t_vat()}

<h3>5.5 Marginal burden</h3>
<p>Comparing new taxes with today's taxes alone would overstate the gain, because health, care and pensions are financed by contributions today and by
taxes in the new system. Table 7 therefore adjusts today's burden for the part of the pension contribution that buys an own entitlement. At € 60,000 the
burden on an additional euro falls from {en(GB['zeilen'][5]['heute_pct'], 1)} % today to {en(GB['zeilen'][5]['neu_2028_pct'], 1)} % in 2028.</p>
<p class="cap">Table 7: Marginal burden, Germany, single</p>
{t_marginal()}

<h2>6 Sensitivity</h2>
<p><b>Pass-through of employer contributions.</b> This is the most important single assumption. Evidence from Sweden shows that employers did not pass
a cut in payroll taxes for young workers into their wages individually (Saez, Schoefer and Seim 2019); the proposal therefore makes pass-through a legal
obligation with a fallback rule. Without any pass-through, the German single at € 42,000 still gains {pm(s0['de_mehr_monat']['alleinstehend']['42000'])} €,
but in France only {s0['anteil_mit_mehr']['FR']['alleinstehend']} % and in Spain {s0['anteil_mit_mehr']['ES']['alleinstehend']} % of single employees would be better off (Table 8).</p>
<p class="cap">Table 8: Pass-through of employer contributions</p>
{t_passthrough()}
<p><b>Fund interest and growth.</b> At a fixed rate of 3.5 %, close to German federal bond yields in October 2026, the surcharge rises to
{en(v35['zuschlag_pct'], 1)} % and the German single at € 42,000 gains {pm(v35['haushalt_de']['mehr_monat_42000']['alleinstehend'])} € instead of
{pm(g42[0])} € (Table 9). Sustainability depends on the gap between interest and growth: with low nominal growth and a contribution fixed at the adopted
value, debt would not be repaid by 2098 (Table 10). Holding the pension claims Z constant in per cent of GDP across growth paths is a simplification.</p>
<p class="cap">Table 9: Fund interest rate</p>
{t_interest()}
<p class="cap">Table 10: Interest and nominal growth</p>
{t_grid()}
<p><b>Avoidance at the top.</b> Revenue from inheritance ({en(J('ausweichen33.json')['positionen_pct_bip']['erbschaften'], 2)} % of GDP) and large wealth
({en(J('ausweichen33.json')['positionen_pct_bip']['grosse_vermoegen'], 2)} % of GDP after avoidance) depends on behaviour at the top of the distribution, where
responses are strong (Jakobsen et al. 2020; Kleven et al. 2014). Across the avoidance band the German dividend changes by
{pm(worst['dividende_2028_eur'])} to {pm(best['dividende_2028_eur'])} € per adult and month in 2028.</p>
<p><b>Take-up.</b> The model assumes complete take-up of the floor. Today, non-take-up of minimum income is high in Germany and France (DREES 2022;
Eurofound 2015); a payment without application and a pre-filled top-up are designed to reduce it, which raises costs that are already fully counted.</p>

<h2>7 Assessment against the objectives</h2>
<p>Table 11 relates each objective to the rules that serve it, to an indicator the model computes, and to what the model does not cover.</p>
<p class="cap">Table 11: Objectives, indicators and gaps</p>
{t_objectives()}
<p><b>Tax fairness.</b> Inequality of disposable income falls in all five countries. The burden on labour falls and the burden on capital rises,
which is the intended shift. The marginal burden on high wages also falls, however: at € 100,000 from {en(gz100['heute_pct'], 1)} % to
{en(gz100['neu_2028_pct'], 1)} %, at € 250,000 from {en(gz250['heute_pct'], 1)} % to {en(gz250['neu_2028_pct'], 1)} % (Table 7). The proposal thus gives up part of the
progressivity on high wages in exchange for equal treatment of income types;
whether this is fair depends on whether top incomes actually pay the 33 % on capital income, inheritance and profits, which the model treats with an
avoidance band (section 6). One-earner couples lose the advantage of joint taxation; this is consistent with individual taxation but is a loss for
these households.</p>
<p><b>Intergenerational fairness.</b> Repayment by 2098 means that taxpayers after 2098 no longer carry today's legacy. The cost falls on taxpayers until
then through the surcharge, and on pensioners with promises above basic need: German pensioner households lose {en(-RE['mittel_monat'])} € per month on
average, while the lowest fifth gains slightly. A full assessment would need generational accounts by birth cohort, which the model does not compute.</p>
<p><b>Climate: incentive instead of control.</b> The rules are consistent with the objective in that harmful consumption is taxed and the revenue
returned. Three elements work through prices rather than prohibitions:</p>
<ul>
<li><b>Carbon price.</b> The European carbon price for buildings and transport (ETS2) enters as a revenue path; its revenue falls with emissions
even though the price rises. Road transport fuel expenditure follows the German projection report 2026 (with-measures scenario).</li>
<li><b>Special rate on harmful goods.</b> Goods classified as harmful to health or the environment carry 33 % – in the model
combustion-engine vehicles, tobacco and alcohol. The model assumes that the share of
combustion engines in vehicle purchases falls from 80 % in 2028 to 10 % in 2035 (assumption, oriented to EU vehicle CO₂ standards).</li>
<li><b>VAT label.</b> Table 13 shows the price signal implied by the rates alone. For the same net price, a certified product in class A costs
{en(-100 * (1.11 / 1.17 - 1), 1)} % less than a standard product; a harmful product costs {en(100 * (1.33 / 1.17 - 1), 1)} % more. A supplier who keeps the consumer price
unchanged earns {en(100 * (1.17 / 1.11 - 1), 1)} % more per unit after moving from B to A. Certification pays if its cost is lower than this advantage.</li>
</ul>
<p class="cap">Table 13: VAT label classes and the price signal</p>
{t_label()}
<p>The label is distributionally progressive in its burden (Table 6), and the revenue returns per head through the dividend. Evidence supports the
direction of the mechanism but not its size: consumers respond more strongly to taxes shown at the point of purchase (Chetty, Looney and Kroft 2009);
in a systematic review of environmental labels on food, 60 of 76 comparisons favoured the labelled option, with many studies at unclear or high
risk of bias (Potter et al. 2021). Certification works only if certifiers are independent and supervised (Dranove and Jin 2010). VAT cuts are passed on
to consumers less than increases (Benzarti et al. 2020), so part of the advantage of class A may stay with suppliers – which still rewards
certification, but weakens the price signal to consumers. Carbon rebates are often underestimated by recipients (Mildenberger et al. 2022).</p>
<p>The model does not estimate how far the rules reduce emissions: emissions are an exogenous path, and the demand response to the label is not
quantified for the current rates. The legal frame is open. Current EU law allows at most two reduced rates of at least 5 % and one lower rate
(Council Directive (EU) 2022/542), while the label has three rates below the standard class; rates that depend on a supplier's certification rather
than on the product raise the question of fiscal neutrality (CJEU case C-515/20; secondary source). The same directive already points in the direction
of the label: it permits reduced rates for solar panels and ends reduced rates for fossil fuels from 2030.</p>
<p>The success of climate policy reduces steering revenue from {en(NZ0['lenkung_pct_bip'], 2)} % of GDP in 2028 to {en(NZ60['lenkung_pct_bip'], 2)} % in 2060
and is the main reason why the dividend falls. Later cohorts therefore receive a smaller dividend – a tension with intergenerational fairness that
the initiative accepts as intended.</p>
<p><b>Digital transformation of work.</b> The clearest quantitative result concerns the tax base. Today a shift of three points of GDP from labour
to capital income by 2060 would reduce revenue by {en(-dk['heute_aufkommen_aenderung_2060_pct_bip'], 2)} % of GDP, because capital income is taxed more lightly;
in the new system the same shift raises revenue by {en(dk['reihe']['2060']['aufkommen_aenderung_33_pct_bip'], 2)} % of GDP. Faster productivity growth from
automation raises the dividend in all scenarios (Table 12). Protection no longer depends on a job. Whether displacement by automation is large, and
how labour markets adjust, is outside the model; the scenarios are assumptions.</p>
<p class="cap">Table 12: Dividend in 2060 under employment and automation scenarios</p>
{t_digital()}

<h2>8 Behavioural effects not in the model</h2>
<p>A qualitative review of the literature (available in German in the research kit) assessed the expected responses to each building block:</p>
<ul>
<li><b>Dividend:</b> experimental and quasi-experimental evidence finds small reductions in hours and little reduction in employment (Jones and Marinescu
2022; Vivalt et al. 2024; STM 2020).</li>
<li><b>Payment without application:</b> lowers non-take-up (Bhargava and Manoli 2015; Eurofound 2015); costs are already fully counted.</li>
<li><b>Compulsory saving with a default fund:</b> raises saving of passive savers, with partial crowd-out among active savers (Madrian and Shea 2001;
Chetty et al. 2014).</li>
<li><b>Individual taxation:</b> raises hours of second earners (Bick and Fuchs-Schündeln 2018).</li>
<li><b>VAT label:</b> cuts reach consumers less than increases (Benzarti et al. 2020); consumers respond more strongly to taxes that are
visible at the point of purchase (Chetty, Looney and Kroft 2009), which may strengthen the steering effect of a label (not tested).</li>
<li><b>Carbon price with rebate:</b> rebates are underestimated and do not reliably raise support (Douenne and Fabre 2022; Mildenberger et al. 2022).</li>
<li><b>Pension rule E:</b> loss aversion and resistance in the largest group of voters are an acceptance risk not captured by the model.</li>
</ul>
<p>None of these findings questions the calculation as such; several show that outcomes depend on design details that are not yet fixed. A
quantitative stage is open.</p>

<h2>9 Limitations and open questions</h2>
<ul>
<li>The model is static; behavioural responses are discussed but not quantified.</li>
<li>Country models are simplified: one earner per household; regional rules and housing benefits beyond those named are not modelled; several
parameters rest on secondary sources.</li>
<li>The share of employees better off uses the German wage distribution scaled to each country's average wage; national wage distributions and
two-earner couples are open.</li>
<li>VAT burdens by income are available only for Germany and France. The demand response to the label and the effect of the rules on emissions
are not quantified; the label requires changes to EU VAT law.</li>
<li>The tax base of company profits taxed where customers are has not been checked against an independent source.</li>
<li>The common fund of 30 states is scaled from ten states; interest and growth are assumptions with a wide band.</li>
<li>Compatibility with EU law and national constitutions has not been assessed.</li>
<li>Which states could adopt common rules is open. Broad acceptance and reliable enforcement are preconditions; the World Justice Project's Rule of
Law Index (2025) is one possible criterion. States outside Europe are not calculated.</li>
</ul>

<h2>10 Reviews, corrections and access</h2>
<p>The calculation chain was recalculated in three internal reviews in October 2026, initiated by the initiative and carried out with a different AI model from the one used to build the calculation; they are not independent reviews. The second and third reviews re-implemented
the core in their own code and confirmed it at rounding level; their findings and the responses are documented. The last review covered model version
{F.GEPRUEFT}; the changes since then (up to {VERSION}) are listed on the website; a follow-up review of them is under way, in which the fund grid (D1) and the marginal burden (D2) have been reproduced in full so far.
Independent review is invited.</p>
<p>The log records every version with date, change, data source, moved figure and how it was noticed; {F.KORREKTUREN} corrections have been numbered
so far. The research kit with all figures to cite, the result files and the review documents is archived at
<a href="https://doi.org/{F.DOI_KONZEPT}">doi.org/{F.DOI_KONZEPT}</a>. Scripts, parameters and the full log are public at <a href="{F.REPO}">{F.REPO.replace("https://", "")}</a>.</p>

<h2>References</h2>
<ol class="refs">{''.join(f'<li>{html.escape(r)}</li>' for r in REFS)}</ol>

<h2 class="neu">Appendix: Figures to cite</h2>
{t_figures()}
"""


CSS = """
@page{size:A4;margin:22mm 20mm 20mm 20mm}
body{font:10.3pt/1.5 Georgia,'Times New Roman',serif;color:#1d2a33;margin:0}
h1{font:700 24pt/1.15 Arial,Helvetica,sans-serif;color:#0f3b5c;margin:0 0 4pt}
h2{font:700 13pt/1.3 Arial,Helvetica,sans-serif;color:#0f3b5c;margin:18pt 0 5pt;break-after:avoid}
h3{font:700 11pt/1.3 Arial,Helvetica,sans-serif;color:#0f3b5c;margin:12pt 0 4pt;break-after:avoid}
h2.neu{break-before:page}
p{margin:0 0 7pt;text-align:justify;hyphens:auto}
a{color:#0f3b5c}
.titel{border-bottom:1.2pt solid #0f3b5c;padding-bottom:10pt;margin-bottom:12pt}
.kicker{font:700 9pt Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#5a7186;margin:0 0 6pt}
.sub{font:13pt/1.35 Georgia,serif;color:#0f3b5c;margin:0 0 8pt;text-align:left}
.autor{font:700 11pt Arial,sans-serif;margin:0 0 4pt}
.meta,.note,.cap{font:8.3pt/1.4 Arial,Helvetica,sans-serif;color:#5a7186;text-align:left}
.cap{font-weight:700;color:#1d2a33;margin:10pt 0 3pt;break-after:avoid}
.abstract{background:#f3f6f8;padding:8pt 11pt;margin:6pt 0 10pt}
.abstract h2{margin-top:2pt}
.kw{font:8.8pt/1.4 Arial,sans-serif;text-align:left}
table{border-collapse:collapse;width:100%;font:8.4pt/1.35 Arial,Helvetica,sans-serif;margin:2pt 0 4pt;break-inside:auto}
tr{break-inside:avoid}
th,td{border-bottom:.5pt solid #d8e1e8;padding:2.6pt 4pt;text-align:left;vertical-align:top}
th{color:#5a7186;font-weight:700}
td.z,th.z{text-align:right;white-space:nowrap}
ul{margin:0 0 7pt;padding-left:15pt}li{margin:0 0 3pt}
.refs{font-size:9pt;padding-left:18pt}.refs li{margin-bottom:3pt}
"""


def seite():
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>The Golden Third – working paper ({VERSION})</title>'
            f'<style>{CSS}</style></head><body>{text()}</body></html>')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    h = seite()
    (OUT / "Golden-Third-Working-Paper.html").write_text(h, encoding="utf-8")
    summe = hashlib.sha256(h.replace(DATUM, "").encode("utf-8")).hexdigest()
    marke = OUT / "quellen.sha256"
    if "--pdf" in sys.argv:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            s = b.new_page()
            s.set_content(h, wait_until="load")
            fuss = ('<div style="font:7.5pt Arial,sans-serif;color:#5a7186;width:100%;padding:0 20mm;display:flex;justify-content:space-between">'
                    f'<span>The Golden Third · working paper · model version {VERSION}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
            s.pdf(path=str(OUT / "Golden-Third-Working-Paper.pdf"), format="A4", display_header_footer=True, header_template="<span></span>",
                  footer_template=fuss, margin=dict(top="20mm", bottom="20mm", left="20mm", right="20mm"))
            b.close()
        marke.write_text(summe + "\n", encoding="utf-8")
    elif not marke.exists() or marke.read_text(encoding="utf-8").strip() != summe:
        print("Working Paper: PDF veraltet – neu bauen mit: python3 dokumente/werkzeuge/working_paper_bau.py --pdf")
        return 1
    print(f"Working Paper {VERSION}: {len(E.FIGURES)} Zahlen im Anhang, {len(REFS)} Quellen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
