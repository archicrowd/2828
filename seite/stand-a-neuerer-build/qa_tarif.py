# -*- coding: utf-8 -*-
"""QA nach der Tarifänderung: Darstellung in 8 Sprachen, zwei Breiten,
   und ein Zahlenabgleich zwischen dem Rechner-JS und der Python-Rechnung."""
import asyncio, pathlib, json
from playwright.async_api import async_playwright

SPR = ['de','index','fr','nl','da','es','et','sl']   # en liegt als index.html
PROBEN = [20000, 36000, 52000, 69000, 105000]

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        befund = []
        for breite, hoehe in ((390, 844), (1280, 900)):
            pg = await b.new_page(viewport={'width': breite, 'height': hoehe})
            for s in SPR:
                await pg.goto(f'file://{pathlib.Path("dist").resolve()}/{s}.html')
                await pg.wait_for_timeout(260)
                # 1 Überlauf der Leiterbeschriftungen
                clip = await pg.evaluate('''() => {
                  const out = [];
                  for (const e of document.querySelectorAll('.taxlbl b, .vatlbl b')) {
                    if (e.scrollWidth > e.clientWidth + 1)
                      out.push(e.className + ':' + e.textContent.trim()
                               + ' ' + e.scrollWidth + '>' + e.clientWidth);
                  }
                  return out; }''')
                # 2 waagerechter Seitenüberlauf
                ueber = await pg.evaluate(
                    'document.documentElement.scrollWidth > window.innerWidth + 1')
                if clip or ueber:
                    befund.append((breite, s, clip, ueber))
            await pg.close()

        # 3 Zahlenabgleich im Rechner
        pg = await b.new_page(viewport={'width': 1280, 'height': 900})
        await pg.goto(f'file://{pathlib.Path("dist").resolve()}/de.html')
        await pg.wait_for_timeout(200)
        js = await pg.evaluate('''(xs) => xs.map(x => {
             const n = neu(x, 0, false, 50);
             return {b:x, est:n.steuer, netto:n.netto, mw:labelKosten(n.netto)}; })''',
             PROBEN)
        await pg.close(); await b.close()
        return befund, js

befund, js = asyncio.run(main())
print('=' * 86)
print('QA NACH DER TARIFÄNDERUNG')
print('=' * 86)
print(f'\n[1] DARSTELLUNG: 8 Sprachen x 2 Breiten = 16 Seiten')
if befund:
    for breite, s, clip, ueber in befund:
        print(f'    FEHLER {breite}px {s}: clip={clip} ueberlauf={ueber}')
else:
    print('    Keine abgeschnittene Leiterbeschriftung, kein waagerechter Überlauf.')

# Python-Gegenrechnung
S = [0, .09, .19, .24, .27, .28]
G = [12348, 25000, 40000, 55000, 70000, float('inf')]
def est(x):
    t, pr = 0.0, 0.0
    for i, g in enumerate(G):
        if x > pr: t += (min(x, g) - pr) * S[i]
        pr = g
        if x <= g: break
    return t
print(f'\n[2] ZAHLENABGLEICH RECHNER-JS GEGEN PYTHON (Stufe 50 %, ohne Kinder)')
print(f'{"Brutto":>10}{"ESt JS":>11}{"ESt Python":>13}{"Differenz":>12}'
      f'{"MwSt-Mehrkosten JS":>21}')
ok = True
for r in js:
    dd = 515 * 12
    # Der Rechner besteuert Brutto + steuerpflichtige Dividende.
    p = est(r['b'] + dd)
    d = abs(r['est'] - p)
    if d > 1.0: ok = False
    print(f'{r["b"]:>10,}{r["est"]:>11,.0f}{p:>13,.0f}{d:>12,.2f}{r["mw"]:>21,.0f}'
          .replace(',', '.'))
print(f'\n    {"Übereinstimmung im Rahmen der Rundung." if ok else "ABWEICHUNG — prüfen!"}')
print(f'''    Geprüft ist damit, dass die JS-Konstanten des Rechners denen der
    Modellrechnung entsprechen — nicht, dass das Modell richtig ist.''')
