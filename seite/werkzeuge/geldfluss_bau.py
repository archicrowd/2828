#!/usr/bin/env python3
"""Webseite: Abschnitt „Wohin das Geld fließt“ – Flussbild heute ↔ Goldenes Drittel, Beispiel Deutschland, sechs Sprachen (Logbuch v4.97).

Läuft nach gemeinschaft_bau.py und setzt in seite/stand-c/{de,en,fr,it,es,pl}.html hinter den Abschnitt „ebenen“ einen Abschnitt „geldfluss“
(vorhandener Abschnitt wird ersetzt, das Skript ist wiederholbar). Zahlen: daten/aggregate/haushaltsplan_de.json (Eurostat 2024; geltende Rechnung
2028). Zeichnung ohne Bibliothek (SVG, eigenes Flusslayout). Übersetzungen en/fr/it/es/pl: durch KI, gegenzulesen.
"""
import json
import re
from pathlib import Path

W = Path(__file__).resolve().parents[2]
ZIEL = W / "seite" / "stand-c"
D = json.loads((W / "daten" / "aggregate" / "haushaltsplan_de.json").read_text(encoding="utf-8"))
SPRACHEN = ["de", "en", "fr", "it", "es", "pl"]

E, A, F = D["einnahmen"], D["ausgaben"], D["fondskonto"]
h = lambda L, s: next(x for x in L if x["position"].startswith(s) or (x.get("nachher_position") or "").startswith(s))
hv = lambda L, s: h(L, s)["heute_pct_bip"] or 0.0
nv = lambda L, s: h(L, s)["nachher_pct_bip"] or 0.0
sozial_heute = sum(x["heute_pct_bip"] for x in E if x["gruppe"] == "Sozialbeiträge")
r2 = lambda x: round(x, 2)

QUELLEN_HEUTE = [("est", hv(E, "Lohn")), ("mwst", hv(E, "Mehrwert")), ("unt", hv(E, "Körperschaft")),
                 ("ueb", hv(E, "Verbrauch") + hv(E, "Emission") + hv(E, "Grundsteuer") + hv(E, "Erbschaft")),
                 ("sv", sozial_heute), ("geb", hv(E, "Verkäufe")), ("kred", -D["summen"]["finanzierungssaldo_heute_pct"])]
QUELLEN_NEU = [("ein", nv(E, "Einkommen") + nv(E, "Kapital") + nv(E, "Progression")), ("label", nv(E, "Konsum")), ("unt2", nv(E, "Unternehmen")),
               ("ueb2", nv(E, "Übrige") + nv(E, "CO₂") + nv(E, "Grundstück") + nv(E, "Erbschaften") + nv(E, "Große") + nv(E, "Subvention")),
               ("zus", nv(E, "Altlastenzuschlag")), ("fkred", F["finanzierung"][0]["pct_bip"])]
ZIELE = [  # gleiche Ziele in beiden Zuständen: (Schlüssel, heute, nachher, Konto nachher)
    ("rente", hv(A, "Alter"), F["ausgaben"][0]["pct_bip"], "fonds"),
    ("div", 0.0, nv(A, "Dividende"), "haus"),
    ("ges", hv(A, "Gesundheit"), nv(A, "Gesundheit"), "haus"),
    ("netz", hv(A, "Krankheit") + hv(A, "Arbeitslos") + hv(A, "Familie"), nv(A, "Krankheit") + nv(A, "Arbeitslos") + nv(A, "Familie"), "haus"),
    ("bild", hv(A, "Schulen") + hv(A, "Hochschulen"), nv(A, "Schulen") + nv(A, "Hochschulen"), "haus"),
    ("wirt", hv(A, "Wirtschaft") + hv(A, "Umwelt"), nv(A, "Wirtschaft") + nv(A, "Umwelt"), "haus"),
    ("verw", hv(A, "Allgemeine"), nv(A, "Allgemeine"), "haus"),
    ("sich", hv(A, "Verteidigung") + hv(A, "Öffentliche"), nv(A, "Verteidigung") + nv(A, "Öffentliche"), "haus"),
    ("komm", hv(A, "Wohnen") + hv(A, "Freizeit"), nv(A, "Wohnen") + nv(A, "Freizeit"), "haus"),
    ("zins", hv(A, "Zinsen"), F["ausgaben"][1]["pct_bip"], "fonds"),
    ("plus", 0.0, max(0.0, D["summen"]["saldo_nachher_pct"]), "haus"),
]
DATEN = dict(
    heute=dict(quellen=[(k, r2(v)) for k, v in QUELLEN_HEUTE], ziele=[(k, r2(a)) for k, a, _, _ in ZIELE if a > 0]),
    neu=dict(quellen=[(k, r2(v)) for k, v in QUELLEN_NEU], ziele=[(k, r2(b), konto) for k, _, b, konto in ZIELE if b > 0]),
    summe=dict(heute=r2(D["summen"]["ausgaben_heute_pct"]), neu=r2(D["summen"]["ausgaben_konsolidiert_nachher_pct"])),
    sozial=r2(sozial_heute), dividende_eur=D["dividende_eur"]["geltend"]["2028"])

T = {
 "de": dict(h2="Wohin das Geld fließt", lede="Beispiel Deutschland: der ganze Staat mit Bund, Ländern, Kommunen und Sozialversicherung – heute und im Goldenen Drittel. "
            "Die Breite der Bänder ist der Anteil an der Wirtschaftsleistung. Heute trägt fast die Hälfte der Sozialbeiträge; im Goldenen Drittel tragen die Steuern, "
            "und ein eigener Fonds trägt die alten Renten und Schulden ab.", heute="Heute (2024)", neu="Goldenes Drittel (2028)", auto="Wechsel anhalten", auto_an="Im Wechsel zeigen",
            mitte_heute="Staat und Sozialversicherung", haus="Haushalt", fonds="Altlastenfonds",
            est="Einkommensteuer", mwst="Mehrwertsteuer", unt="Unternehmenssteuern", ueb="übrige Steuern", sv="Sozialbeiträge", geb="Gebühren und Erträge", kred="neue Schulden",
            ein="Einkommen und Kapital", label="Mehrwertsteuer-Label", unt2="Unternehmen", ueb2="Klima, Erbe, Boden u. a.", zus="Altlastenzuschlag", fkred="Kredite des Fonds",
            rente="Renten und Pensionen", div="Transformationsdividende", ges="Gesundheit", netz="Pflege, Familie, Grundsicherung u. a.", bild="Bildung und Forschung",
            wirt="Wirtschaft, Verkehr, Umwelt", verw="Verwaltung", sich="Sicherheit und Verteidigung", komm="Wohnen, Kultur, Gemeinwesen", zins="Zinsen", plus="Überschuss",
            k1="Ausgaben in % der Wirtschaftsleistung", k2="davon aus Sozialbeiträgen", k3="Dividende je Erwachsenem und Monat",
            wisch="Grafik seitlich verschieben ⇆", fuss="Quellen: Eurostat (Staatsfinanzen 2024, vorläufig); Rechnung der Initiative 28:28 (geltende Rechnung 2028). Heute einschließlich Gebühren und Entgelte, "
                 "im Goldenen Drittel sind Kommunen und Staat netto gerechnet; die private Pflichtvorsorge (eigenes Konto) ist nicht enthalten. Kredite sind keine Einnahme, "
                 "sondern Finanzierung; die Kredite des Fonds werden bis 2098 getilgt."),
 "en": dict(h2="Where the money flows", lede="Example Germany: the whole state with federal, regional and local government and social insurance – today and in the Golden Third. "
            "The width of each band is its share of economic output. Today social contributions carry almost half; in the Golden Third taxes carry the load, "
            "and a separate fund pays off old pensions and debt.", heute="Today (2024)", neu="Golden Third (2028)", auto="Stop switching", auto_an="Show alternately",
            mitte_heute="State and social insurance", haus="Budget", fonds="Legacy fund",
            est="Income tax", mwst="VAT", unt="Company taxes", ueb="Other taxes", sv="Social contributions", geb="Fees and income", kred="New borrowing",
            ein="Income and capital", label="VAT label", unt2="Companies", ueb2="Climate, inheritance, land etc.", zus="Legacy surcharge", fkred="Fund borrowing",
            rente="Pensions", div="Transformation dividend", ges="Health", netz="Care, family, basic support etc.", bild="Education and research",
            wirt="Economy, transport, environment", verw="Administration", sich="Security and defence", komm="Housing, culture, community", zins="Interest", plus="Surplus",
            k1="Spending as % of economic output", k2="of which from social contributions", k3="Dividend per adult per month",
            wisch="Swipe the chart sideways ⇆", fuss="Sources: Eurostat (government finance 2024, provisional); calculation of Initiative 28:28 (current model 2028). Today including fees and charges; "
                 "in the Golden Third local and central government are net. Mandatory private pensions (own account) are not included. Borrowing is financing, not revenue; "
                 "the fund's loans are repaid by 2098."),
 "fr": dict(h2="Où va l'argent", lede="Exemple de l'Allemagne : l'ensemble de l'État avec la fédération, les Länder, les communes et la sécurité sociale – aujourd'hui et dans le Tiers d'or. "
            "La largeur des bandes correspond à la part de la production économique. Aujourd'hui, les cotisations sociales en portent près de la moitié ; dans le Tiers d'or, "
            "les impôts portent la charge et un fonds distinct rembourse les anciennes retraites et dettes.", heute="Aujourd'hui (2024)", neu="Tiers d'or (2028)", auto="Arrêter l'alternance", auto_an="Afficher en alternance",
            mitte_heute="État et sécurité sociale", haus="Budget", fonds="Fonds des charges héritées",
            est="Impôt sur le revenu", mwst="TVA", unt="Impôts des entreprises", ueb="Autres impôts", sv="Cotisations sociales", geb="Redevances et revenus", kred="Nouvel emprunt",
            ein="Revenus et capital", label="Label TVA", unt2="Entreprises", ueb2="Climat, héritage, sol…", zus="Surtaxe héritage", fkred="Emprunts du fonds",
            rente="Retraites et pensions", div="Dividende de transition", ges="Santé", netz="Dépendance, famille, minimum social…", bild="Éducation et recherche",
            wirt="Économie, transports, environnement", verw="Administration", sich="Sécurité et défense", komm="Logement, culture, vie locale", zins="Intérêts", plus="Excédent",
            k1="Dépenses en % de la production", k2="dont cotisations sociales", k3="Dividende par adulte et par mois",
            wisch="Faire défiler le graphique ⇆", fuss="Sources : Eurostat (finances publiques 2024, provisoire) ; calcul de l'Initiative 28:28 (modèle en vigueur 2028). Aujourd'hui y compris redevances ; "
                 "dans le Tiers d'or, communes et État en net. La prévoyance obligatoire privée (compte propre) n'est pas incluse. L'emprunt est un financement, pas une recette ; "
                 "les emprunts du fonds sont remboursés d'ici 2098."),
 "it": dict(h2="Dove va il denaro", lede="Esempio Germania: tutto lo Stato con federazione, Länder, comuni e previdenza sociale – oggi e nel Terzo d'oro. "
            "La larghezza delle bande è la quota della produzione economica. Oggi i contributi sociali ne portano quasi la metà; nel Terzo d'oro portano le imposte, "
            "e un fondo separato estingue vecchie pensioni e debiti.", heute="Oggi (2024)", neu="Terzo d'oro (2028)", auto="Ferma l'alternanza", auto_an="Mostra in alternanza",
            mitte_heute="Stato e previdenza sociale", haus="Bilancio", fonds="Fondo degli oneri ereditati",
            est="Imposta sul reddito", mwst="IVA", unt="Imposte sulle imprese", ueb="Altre imposte", sv="Contributi sociali", geb="Tariffe e proventi", kred="Nuovo debito",
            ein="Redditi e capitale", label="Etichetta IVA", unt2="Imprese", ueb2="Clima, eredità, suolo…", zus="Sovrattassa oneri", fkred="Prestiti del fondo",
            rente="Pensioni", div="Dividendo di transizione", ges="Sanità", netz="Assistenza, famiglia, reddito minimo…", bild="Istruzione e ricerca",
            wirt="Economia, trasporti, ambiente", verw="Amministrazione", sich="Sicurezza e difesa", komm="Abitazione, cultura, comunità", zins="Interessi", plus="Avanzo",
            k1="Spesa in % della produzione", k2="di cui da contributi sociali", k3="Dividendo per adulto al mese",
            wisch="Scorrere il grafico ⇆", fuss="Fonti: Eurostat (finanza pubblica 2024, provvisoria); calcolo dell'Iniziativa 28:28 (modello vigente 2028). Oggi incluse tariffe; "
                 "nel Terzo d'oro comuni e Stato al netto. La previdenza privata obbligatoria (conto proprio) non è inclusa. Il debito è finanziamento, non entrata; "
                 "i prestiti del fondo sono rimborsati entro il 2098."),
 "es": dict(h2="Adónde va el dinero", lede="Ejemplo de Alemania: todo el Estado con federación, Länder, municipios y seguridad social – hoy y en el Tercio de oro. "
            "El ancho de cada banda es su parte de la producción económica. Hoy las cotizaciones sociales soportan casi la mitad; en el Tercio de oro lo soportan los impuestos, "
            "y un fondo propio amortiza las pensiones y deudas antiguas.", heute="Hoy (2024)", neu="Tercio de oro (2028)", auto="Detener la alternancia", auto_an="Mostrar alternando",
            mitte_heute="Estado y seguridad social", haus="Presupuesto", fonds="Fondo de cargas heredadas",
            est="Impuesto sobre la renta", mwst="IVA", unt="Impuestos de empresas", ueb="Otros impuestos", sv="Cotizaciones sociales", geb="Tasas e ingresos", kred="Nueva deuda",
            ein="Renta y capital", label="Etiqueta del IVA", unt2="Empresas", ueb2="Clima, herencia, suelo…", zus="Recargo de cargas", fkred="Préstamos del fondo",
            rente="Pensiones", div="Dividendo de transformación", ges="Salud", netz="Dependencia, familia, ingreso mínimo…", bild="Educación e investigación",
            wirt="Economía, transporte, medio ambiente", verw="Administración", sich="Seguridad y defensa", komm="Vivienda, cultura, comunidad", zins="Intereses", plus="Superávit",
            k1="Gasto en % de la producción", k2="de ello, de cotizaciones sociales", k3="Dividendo por adulto y mes",
            wisch="Desplace el gráfico ⇆", fuss="Fuentes: Eurostat (finanzas públicas 2024, provisional); cálculo de la Iniciativa 28:28 (modelo vigente 2028). Hoy incluidas tasas; "
                 "en el Tercio de oro, municipios y Estado en neto. La previsión privada obligatoria (cuenta propia) no se incluye. La deuda es financiación, no ingreso; "
                 "los préstamos del fondo se amortizan hasta 2098."),
 "pl": dict(h2="Dokąd płyną pieniądze", lede="Przykład Niemiec: całe państwo – federacja, kraje związkowe, gminy i ubezpieczenia społeczne – dziś i w Złotej Trzeciej. "
            "Szerokość pasm to udział w produkcie gospodarki. Dziś prawie połowę niosą składki społeczne; w Złotej Trzeciej niosą je podatki, "
            "a osobny fundusz spłaca dawne emerytury i długi.", heute="Dziś (2024)", neu="Złota Trzecia (2028)", auto="Zatrzymaj zmianę", auto_an="Pokazuj na zmianę",
            mitte_heute="Państwo i ubezpieczenia społeczne", haus="Budżet", fonds="Fundusz zobowiązań",
            est="Podatek dochodowy", mwst="VAT", unt="Podatki firm", ueb="Inne podatki", sv="Składki społeczne", geb="Opłaty i dochody", kred="Nowy dług",
            ein="Dochody i kapitał", label="Etykieta VAT", unt2="Firmy", ueb2="Klimat, spadki, grunty…", zus="Dopłata na zobowiązania", fkred="Kredyty funduszu",
            rente="Emerytury", div="Dywidenda transformacyjna", ges="Zdrowie", netz="Opieka, rodzina, minimum socjalne…", bild="Edukacja i badania",
            wirt="Gospodarka, transport, środowisko", verw="Administracja", sich="Bezpieczeństwo i obrona", komm="Mieszkalnictwo, kultura, wspólnota", zins="Odsetki", plus="Nadwyżka",
            k1="Wydatki w % produktu gospodarki", k2="w tym ze składek społecznych", k3="Dywidenda na dorosłego miesięcznie",
            wisch="Przewiń wykres w bok ⇆", fuss="Źródła: Eurostat (finanse publiczne 2024, wstępne); obliczenia Inicjatywy 28:28 (obowiązujący model 2028). Dziś wraz z opłatami; "
                 "w Złotej Trzeciej gminy i państwo netto. Obowiązkowa prywatna emerytura (własne konto) nie jest uwzględniona. Kredyt to finansowanie, nie dochód; "
                 "kredyty funduszu są spłacane do 2098."),
}
DEZ = {"de": ",", "en": ".", "fr": ",", "it": ",", "es": ",", "pl": ","}

CSS = """<style>
#geldfluss .gf-knoepfe{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 10px}
#geldfluss .gf-knoepfe button{font:600 14px var(--disp);padding:8px 14px;border:1px solid var(--ink);background:var(--paper);color:var(--ink);border-radius:999px;cursor:pointer}
#geldfluss .gf-knoepfe button[aria-pressed=true]{background:var(--ink);color:#fff}
#geldfluss .gf-knoepfe .gf-auto{border-color:var(--line);color:var(--dim);font-weight:500}
#geldfluss .gf-bild{position:relative;overflow-x:auto}
#geldfluss .gf-wisch{display:none;font-family:var(--mono);font-size:12px;color:var(--dim);margin:0 0 6px}
@media (max-width:760px){#geldfluss .gf-wisch{display:block}}
#geldfluss .gf-bild svg{display:block;min-width:720px;width:100%;height:auto;transition:opacity .6s}
#geldfluss .gf-bild svg+svg{position:absolute;inset:0 auto auto 0}
#geldfluss .gf-bild text{font-family:var(--disp);font-size:12px;fill:var(--ink)}
#geldfluss .gf-bild text.w{font-family:var(--mono);font-size:10.5px;fill:var(--dim)}
#geldfluss .gf-kz{display:flex;flex-wrap:wrap;gap:12px;margin-top:14px}
#geldfluss .gf-kz div{flex:1 1 180px;border-top:2px solid var(--ink);padding-top:6px}
#geldfluss .gf-kz b{display:block;font:600 22px var(--mono)}
#geldfluss .gf-kz span{font-size:13px;color:var(--dim)}
#geldfluss .gf-fuss{font-size:12.5px;color:var(--dim);margin-top:14px;max-width:80ch}
@media (prefers-reduced-motion:reduce){#geldfluss .gf-bild svg{transition:none}}
</style>"""

JS = r"""<script>(function(){
const D=__D__, T=__T__, DZ=__DZ__;
const f=x=>x.toFixed(1).replace('.',DZ);
const NS='http://www.w3.org/2000/svg';
const C={st:'#0F3B5C',sv:'#B4452F',fo:'#6A4C93',kr:'#9AA6B0',div:'#1D7A4F',ziel:'#8FA6B8',mitte:'#0F3B5C'};
const W=960, PX=8.6, PAD=7, NW=12, X=[225,445,665];
function el(n,a,p){const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e;}
function farbe(k){return k==='sv'?C.sv:(k==='geb'||k==='kred'||k==='fkred')?C.kr:k==='zus'?C.fo:C.st;}
function zielfarbe(k,konto){return k==='div'?C.div:konto==='fonds'?C.fo:C.ziel;}
function band(g,x0,y0a,y0b,x1,y1a,y1b,col){const m=(x0+x1)/2;
  el('path',{d:`M${x0},${y0a}C${m},${y0a} ${m},${y1a} ${x1},${y1a}L${x1},${y1b}C${m},${y1b} ${m},${y0b} ${x0},${y0b}Z`,fill:col,'fill-opacity':.42},g);}
function zeichne(zustand){
  const S=D[zustand], H=Math.max(S.quellen.length,S.ziele.length)*PAD+PX*Math.max(D.summe.heute+1,0)+40;
  const svg=el('svg',{viewBox:`0 0 ${W} ${Math.round(H)}`,role:'img','aria-label':T[zustand==='heute'?'heute':'neu']});
  const g=el('g',{},svg);
  // Mittelknoten
  let mitte;
  if(zustand==='heute'){mitte=[{k:'staat',v:S.quellen.reduce((a,q)=>a+q[1],0),name:T.mitte_heute,col:C.mitte}];}
  else{const haus=S.quellen.filter(q=>['zus','fkred'].indexOf(q[0])<0).reduce((a,q)=>a+q[1],0);
       const fo=S.quellen.filter(q=>['zus','fkred'].indexOf(q[0])>=0).reduce((a,q)=>a+q[1],0);
       mitte=[{k:'haus',v:haus,name:T.haus,col:C.mitte},{k:'fonds',v:fo,name:T.fonds,col:C.fo}];}
  // Lage der Mittelknoten
  let y=20; const mpos={};
  mitte.forEach(m=>{mpos[m.k]={y0:y,y1:y+m.v*PX,inA:y,outA:y};y+=m.v*PX+PAD*3;});
  // Quellen
  y=20; const zuMitte=q=>zustand==='heute'?'staat':(['zus','fkred'].indexOf(q)>=0?'fonds':'haus');
  // Reihenfolge der Quellen nach Mittelknoten, damit sich Bänder nicht kreuzen
  const qs=S.quellen.slice().sort((a,b)=>(zuMitte(a[0])==='fonds')-(zuMitte(b[0])==='fonds'));
  qs.forEach(([k,v])=>{const h=v*PX, m=mpos[zuMitte(k)];
    el('rect',{x:X[0]-NW,y:y,width:NW,height:Math.max(1,h),fill:farbe(k)},g);
    band(g,X[0],y,y+h,X[1],m.inA,m.inA+h,farbe(k)); m.inA+=h;
    const t=el('text',{x:X[0]-NW-8,y:y+h/2+4,'text-anchor':'end'},g); t.textContent=T[k];
    if(h>26){const w=el('text',{class:'w',x:X[0]-NW-8,y:y+h/2+16,'text-anchor':'end'},g); w.textContent=f(v)+' %';}
    y+=h+PAD;});
  // Ziele
  y=20; const zs=S.ziele.slice();
  if(zustand==='neu') zs.sort((a,b)=>(a[2]==='fonds')-(b[2]==='fonds'));
  zs.forEach(z=>{const k=z[0], v=z[1], konto=zustand==='heute'?'staat':(z[2]==='fonds'?'fonds':'haus'), h=v*PX, m=mpos[konto], col=zielfarbe(k,z[2]);
    el('rect',{x:X[2],y:y,width:NW,height:Math.max(1,h),fill:col},g);
    band(g,X[1]+NW,m.outA,m.outA+h,X[2],y,y+h,col); m.outA+=h;
    const t=el('text',{x:X[2]+NW+8,y:y+h/2+4},g); t.textContent=T[k];
    if(h>26){const w=el('text',{class:'w',x:X[2]+NW+8,y:y+h/2+16},g); w.textContent=f(v)+' %';}
    y+=h+PAD;});
  mitte.forEach(m=>{const p=mpos[m.k];
    el('rect',{x:X[1],y:p.y0,width:NW,height:p.y1-p.y0,fill:m.col},g);
    const t=el('text',{x:X[1]+NW/2,y:p.y0-6,'text-anchor':'middle','font-weight':'700'},g); t.textContent=m.name+' '+f(m.v)+' %';});
  return svg;}
const box=document.getElementById('gf-bild'); if(!box)return;
const s1=zeichne('heute'), s2=zeichne('neu'); box.appendChild(s1); box.appendChild(s2);
const kz=document.getElementById('gf-kz');
const zeigen=z=>{s1.style.opacity=z==='heute'?1:0; s2.style.opacity=z==='neu'?1:0;
  s1.style.visibility=z==='heute'?'visible':'hidden'; s2.style.visibility=z==='neu'?'visible':'hidden';
  document.getElementById('gf-b-heute').setAttribute('aria-pressed',z==='heute'); document.getElementById('gf-b-neu').setAttribute('aria-pressed',z==='neu');
  kz.innerHTML=`<div><b>${f(z==='heute'?D.summe.heute:D.summe.neu)} %</b><span>${T.k1}</span></div><div><b>${f(z==='heute'?D.sozial:0)} %</b><span>${T.k2}</span></div>`+
    `<div><b>${z==='heute'?'0':D.dividende_eur} €</b><span>${T.k3}</span></div>`; aktuell=z;};
let aktuell='heute', uhr=null;
const ruhig=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const auto=document.getElementById('gf-auto');
const start=()=>{uhr=setInterval(()=>zeigen(aktuell==='heute'?'neu':'heute'),6000);auto.textContent=T.auto;};
const stop=()=>{clearInterval(uhr);uhr=null;auto.textContent=T.auto_an;};
document.getElementById('gf-b-heute').onclick=()=>{stop();zeigen('heute');};
document.getElementById('gf-b-neu').onclick=()=>{stop();zeigen('neu');};
auto.onclick=()=>{uhr?stop():start();};
zeigen('heute'); if(!ruhig)start(); else stop();
})();</script>"""


def abschnitt(L):
    t = T[L]
    js = JS.replace("__D__", json.dumps(DATEN, ensure_ascii=False)).replace("__T__", json.dumps(t, ensure_ascii=False)).replace("__DZ__", json.dumps(DEZ[L]))
    return (f'<section id="geldfluss">\n  <div class="wrap">\n    <h2>{t["h2"]}</h2>\n    <p class="lede">{t["lede"]}</p>\n'
            f'    <div class="gf-knoepfe"><button type="button" id="gf-b-heute" aria-pressed="true">{t["heute"]}</button>'
            f'<button type="button" id="gf-b-neu" aria-pressed="false">{t["neu"]}</button><button type="button" class="gf-auto" id="gf-auto">{t["auto"]}</button></div>\n'
            f'    <p class="gf-wisch">{t["wisch"]}</p>\n    <div class="gf-bild" id="gf-bild"></div>\n    <div class="gf-kz" id="gf-kz"></div>\n    <p class="gf-fuss">{t["fuss"]}</p>\n'
            f'  </div>\n{CSS}\n{JS and js}\n</section>')


for L in SPRACHEN:
    p = ZIEL / f"{L}.html"
    H = p.read_text(encoding="utf-8")
    H = re.sub(r'\n?<section id="geldfluss">.*?</section>', "", H, flags=re.S)
    i = H.index('<section id="ebenen">')
    j = H.index("</section>", i) + len("</section>")
    H = H[:j] + "\n" + abschnitt(L) + H[j:]
    p.write_text(H, encoding="utf-8")
    print(f"{L}: Abschnitt geldfluss gesetzt")
