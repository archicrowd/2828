# -*- coding: utf-8 -*-
"""Baut die Sprachfassungen von TAX 28:28.

  index.html  Englisch        de.html  Deutsch      fr.html  Französisch
  es.html     Spanisch        nl.html  Niederländ.  da.html  Dänisch
  et.html     Estnisch

Alle Zahlen stammen aus modell-2828.py (Haushalt, Haushalte) und klub7.py (Klub).
Die Sprachbausteine liegen in lang/<code>.json.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from css import CSS
from tpl import HTML

OUT = os.path.join(HERE, 'dist')
os.makedirs(OUT, exist_ok=True)

# Reihenfolge der Sprachumschaltung, Datei, Anzeigekürzel, JS-Locale, Trennzeichen
LANGS = [
    ('en', 'index.html', 'EN', 'en-GB', ',', '.'),
    ('de', 'de.html',    'DE', 'de-DE', '.', ','),
    ('fr', 'fr.html',    'FR', 'fr-FR', ' ', ','),
    ('es', 'es.html',    'ES', 'es-ES', '.', ','),
    ('nl', 'nl.html',    'NL', 'nl-NL', '.', ','),
    ('da', 'da.html',    'DA', 'da-DK', '.', ','),
    ('sl', 'sl.html',    'SL', 'sl-SI', '.', ','),
    ('et', 'et.html',    'ET', 'et-EE', ' ', ','),
]

NBSP = ' '


def mk_fmt(thou, dec):
    def f(v, d=0, sign=False):
        if v is None:
            return '–'
        s = f'{abs(v):,.{d}f}'
        s = s.replace(',', '\x00').replace('.', dec).replace('\x00', thou)
        if sign:
            s = ('+' if v >= 0 else '−') + s
        elif v < 0:
            s = '−' + s
        return s
    return f


# ---------------------------------------------------------------- Modelldaten
# Zehn geprüfte Haushalte, Startstufe 515 EUR (aus modell-2828.py)
HAUSHALTE = [
    ('hh01', None,   None,  6180,  6033, None),
    ('hh02', 28000,  20180, 27653, 6884, 34),
    ('hh03', 28000,  23414, 30743, 6674, 29),
    ('hh04', 42000,  28193, 37044, 8062, 29),
    ('hh05', 51944,  33632, 43351, 8796, 26),
    ('hh06', 55000,  35262, 45185, 8960, 25),
    ('hh07', 63000,  50620, 62345, 10554, 21),
    ('hh08', 80000,  48544, 59861, 10193, 21),
    ('hh09', 150000, 85528, 100461, 13424, 16),
    ('hh10', 10560,  12720, 15481, 2393, 19),
]
# Drei Rechenwege (aus modell-2828.py)
SZENARIEN = [
    ('sc1', 60, 0, '2030', '2032', 100, False),
    ('sc2', 55, 0, '2030', '2038', 100, True),
    ('sc3', 30, 0, '–', '–', 85, False),
]
KLUB_JSON = json.load(open(os.path.join(HERE, 'klub10-daten.json'), encoding='utf-8'))
KL_ORDER = ['Deutschland', 'Frankreich', 'Spanien', 'Niederlande', 'Irland',
            'Belgien', 'Österreich', 'Dänemark', 'Slowenien', 'Estland']
KL_KEY = dict(zip(KL_ORDER, ['c_de', 'c_fr', 'c_es', 'c_nl', 'c_ie',
                             'c_be', 'c_at', 'c_dk', 'c_si', 'c_ee']))
KL_CODE = dict(zip(KL_ORDER, ['DE', 'FR', 'ES', 'NL', 'IE', 'BE',
                              'AT', 'DK', 'SI', 'EE']))
# Irland: Bezugsgrösse ist GNI*, nicht das durch Konzernbilanzen überhöhte BIP.
KL_FN = {'Irland': '²'}

METRICS = [
 {"name": "m1", "unit": "u1", "dec": 0,
  "hist": [82,79,81,78,75,72,69,65,62,59,68,69,66,64,63,63],
  "ohne": [64,65,65,66,66,67,67,68,68,69],
  "mit":  [64,65,62.3,62.9,62.9,63.7,63.4,64.0,63.5,64.0]},
 {"name": "m2", "unit": "u2", "dec": 2,
  "hist": [.286,.288,.289,.292,.293,.295,.297,.299,.300,.297,.300,.305,.308,.310,.311,.312],
  "ohne": [.313,.313,.314,.314,.315,.315,.316,.316,.317,.317],
  "mit":  [.313,.313,.274,.274,.269,.269,.269,.269,.270,.270]},
 {"name": "m3", "unit": "u3", "dec": 0,
  "hist": [942,922,926,944,904,907,911,894,858,800,730,762,750,674,650,620],
  "ohne": [608,596,584,572,560,549,538,527,516,505],
  "mit":  [608,596,578,552,524,496,470,446,424,404]},
 {"name": "m4", "unit": "u4", "dec": 0,
  "hist": [35.0,35.2,35.4,35.5,35.6,35.7,35.8,35.9,36.0,35.8,35.9,36.1,36.3,36.4,36.5,36.5],
  "ohne": [36.7,36.8,36.9,37.0,37.1,37.2,37.3,37.4,37.5,37.6],
  "mit":  [36.7,36.8,29.8,29.8,30.3,30.3,30.4,30.5,30.6,30.7]},
]


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ------------------------------------------------------------------ Tabellen
def tbl_hh(T, f):
    h = ''.join(f'<th scope="col">{T[k]}</th>' for k in
                ('th_hh', 'th_gross', 'th_today', 'th_new', 'th_plus', 'th_pct'))
    rows = ''
    for key, br, ht, nu, pl, pc in HAUSHALTE:
        rows += (f'<tr><td>{T[key]}</td>'
                 f'<td>{f(br)+NBSP+"€" if br else "–"}</td>'
                 f'<td>{(f(ht)+NBSP+"€") if ht else T["hh_fn"]}</td>'
                 f'<td>{f(nu)}{NBSP}€</td>'
                 f'<td class="pos">{f(pl, sign=True)}{NBSP}€</td>'
                 f'<td class="pos">{(f(pc, sign=True)+NBSP+"%") if pc else "–"}</td></tr>')
    return (f'<div class="tscroll"><table><thead><tr>{h}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def tbl_sc(T, f):
    h = ''.join(f'<th scope="col">{T[k]}</th>' for k in
                ('th_sc', 'th_y1', 'th_gap', 'th_566', 'th_617', 'th_inv'))
    rows = ''
    for key, y1, gap, s55, s60, inv, mark in SZENARIEN:
        name = f'<b>{T[key]}</b><br><span style="font-size:13px;color:var(--dim)">{T["sc_base"]}</span>' \
               if mark else T[key]
        rows += (f'<tr><td>{name}</td><td>{f(y1, sign=True)}{NBSP}{T["bn"]}</td>'
                 f'<td>{gap}</td><td>{s55}</td><td>{s60}</td><td>{inv}{NBSP}%</td></tr>')
    return (f'<div class="tscroll"><table><thead><tr>{h}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def tbl_club(T, f):
    h = ''.join(f'<th scope="col">{T[k]}</th>' for k in
                ('th_country', 'th_dd', 'th_cost', 'th_pit', 'th_cit', 'th_debt', 'th_lvl'))
    rows = ''
    for name in KL_ORDER:
        d = KLUB_JSON[name]
        fn = KL_FN.get(name, '')
        rows += (f'<tr><td>{T[KL_KEY[name]]}</td>'
                 f'<td>{f(d["dd"])}{NBSP}€</td>'
                 f'<td>{f(d["quote_bezug"],1)}{NBSP}%{fn}</td>'
                 f'<td>{f(d["est"],1)}{NBSP}%</td>'
                 f'<td>{f(d["kst"],1)}{NBSP}%</td>'
                 f'<td>{f(d["schuld"],1)}{NBSP}%</td>'
                 f'<td>{f(d["l"],1)}</td></tr>')
    k = KLUB_JSON['_klub']
    rows += (f'<tr class="tot"><td>{T["c_club"]}</td><td>–</td>'
             f'<td>{f(10.8,1)}{NBSP}%</td><td>–</td><td>–</td>'
             f'<td>–</td><td>–</td></tr>')
    return (f'<div class="tscroll"><table><thead><tr>{h}</tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')



# Belegstand: (Positionsschluessel, Behauptung, Stufe 0-3, Grundlage)
BELEG = [('p01pos', 'p01t', 1, 'ev_g1'), ('p02pos', 'p02t', 1, 'ev_g2'), ('p03pos', 'p03t', 3, 'ev_g3'), ('p04pos', 'p04t', 0, 'ev_g4'), ('p05pos', 'p05t', 2, 'ev_g5'), ('p06pos', 'p06t', 1, 'ev_g6'), ('p07pos', 'p07t', 2, 'ev_g7'), ('p08pos', 'p08t', 3, 'ev_g8'), ('p09pos', 'p09t', 0, 'ev_g9'), ('p10pos', 'p10t', 1, 'ev_g10')]


def tbl_beleg(T, f):
    """Stufe erscheint als Blockanzeige UND als Wort — nie nur als Farbe."""
    h = ''.join('<th scope="col">%s</th>' % T[k]
                for k in ('ev_c1', 'ev_c2', 'ev_c3', 'ev_c4'))
    blocks = '<span class="meter"><i></i><i></i><i></i></span>'
    rows = ''
    for pos, claim, stufe, grund in BELEG:
        wort = T['ev_s%d' % stufe]
        rows += ('<tr><td>%s</td><td class="claim">%s</td>'
                 '<td class="st s%d">%s<span class="w">%s</span></td>'
                 '<td>%s</td></tr>'
                 % (T[pos], T[claim], stufe, blocks, wort, T[grund]))
    cols = ('<colgroup><col class="c1"><col class="c2">'
            '<col class="c3"><col class="c4"></colgroup>')
    return ('<div class="tscroll belegwrap"><table class="beleg">%s'
            '<thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>' % (cols, h, rows))

def flags(T, f):
    out = ''
    for name in KL_ORDER:
        out += (f'<div><div class="c">{f(KLUB_JSON[name]["dd"])}{NBSP}€</div>'
                f'<div class="n">{T[KL_KEY[name]]}</div></div>')
    return out


# --------------------------------------------------------------------- Bauen
def read(p):
    return open(p, encoding='utf-8').read()

SRC_MODEL = read('/mnt/user-data/outputs/horizon25-broschure/modell-2828.py')
SRC_CALC = read('/mnt/user-data/outputs/horizon25-broschure/rechner-2828.js')
SRC_CLUB = read(os.path.join(HERE, 'klub10.py'))


def build(code, fname, disp, loc, thou, dec):
    # Englisch dient als Rückfallebene: fehlt ein Baustein, erscheint der englische.
    base = json.load(open(os.path.join(HERE, 'lang', 'en.json'), encoding='utf-8'))
    own = json.load(open(os.path.join(HERE, 'lang', code + '.json'), encoding='utf-8'))
    T = {**base, **own}
    if code != 'en':
        fb = sorted(set(base) - set(own))
        if fb:
            print(f'  i {code}: englischer Rückfall für {len(fb)} Bausteine: {fb}')
    f = mk_fmt(thou, dec)
    act = ' class="active"'
    sel = ''.join(
        '<a href="%s"%s lang="%s">%s</a>' % (fn, act if c == code else '', c, dp)
        for c, fn, dp, _, _, _ in LANGS)
    met = json.dumps([{**m, 'name': T[m['name']], 'unit': T[m['unit']]} for m in METRICS],
                     ensure_ascii=False)
    ctx = dict(T)
    # Bausteine, die in JavaScript-Zeichenketten landen, maskieren
    for k in ('js_more', 'js_less', 'js_month', 'js_start'):
        ctx[k] = str(T[k]).replace('\\', '\\\\').replace("'", "\\'")
    ctx.update({
        '_lang': code, '_css': CSS, '_langsel': sel, '_loc': loc, '_metrics': met,
        '_tbl_hh': tbl_hh(T, f), '_tbl_sc': tbl_sc(T, f), '_tbl_club': tbl_club(T, f),
        '_flags': flags(T, f), '_tbl_beleg': tbl_beleg(T, f),
        '_src_model': esc(SRC_MODEL), '_src_calc': esc(SRC_CALC), '_src_club': esc(SRC_CLUB),
    })
    missing = set()

    def sub(m):
        k = m.group(1)
        if k not in ctx:
            missing.add(k)
            return '{{' + k + '}}'
        return str(ctx[k])

    html = re.sub(r'\{\{([A-Za-z0-9_]+)\}\}', sub, HTML)
    if missing:
        print(f'  ! {code}: fehlende Bausteine: {sorted(missing)}')
    unused = sorted(set(T) - set(re.findall(r'\{\{([A-Za-z0-9_]+)\}\}', HTML))
                    - {m['name'] for m in METRICS} - {m['unit'] for m in METRICS}
                    - set(KL_KEY.values()) - {'c_club', 'bn', 'sc_base', 'hh_fn'}
                    - {k for k, *_ in HAUSHALTE} - {k for k, *_ in SZENARIEN}
                    - {'th_hh','th_gross','th_today','th_new','th_plus','th_pct',
                       'th_sc','th_y1','th_gap','th_566','th_617','th_inv',
                       'th_country','th_dd','th_cost','th_pit','th_cit','th_debt','th_lvl'})
    if unused:
        print(f'  ? {code}: unbenutzte Bausteine: {unused}')
    open(os.path.join(OUT, fname), 'w', encoding='utf-8').write(html)
    print(f'  {fname:<12} {len(html)/1024:6.1f} kB')


if __name__ == '__main__':
    only = sys.argv[1:] or [c for c, *_ in LANGS]
    print('TAX 28:28 — Sprachfassungen')
    for code, fname, disp, loc, thou, dec in LANGS:
        if code in only and os.path.exists(os.path.join(HERE, 'lang', code + '.json')):
            build(code, fname, disp, loc, thou, dec)
