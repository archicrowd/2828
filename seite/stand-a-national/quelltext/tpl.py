# -*- coding: utf-8 -*-
"""HTML-Gerüst. Platzhalter {{schluessel}} werden aus lang/<code>.json gefüllt."""

HTML = r"""<!DOCTYPE html><html lang="{{_lang}}"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{title}}</title>
<meta name="description" content="{{meta_desc}}">
<meta name="robots" content="noindex, nofollow">
<style>{{_css}}</style>
</head>
<body>

<nav class="titleblock" id="top" aria-label="{{nav_aria}}">
  <div class="wrap">
    <a class="tb-left" href="#top">TAX 28:28</a>
    <div class="tb-right">
      <a href="#concept">{{nav_concept}}</a>
      <a href="#calc">{{nav_calc}}</a>
      <a class="opt" href="#simulation">{{nav_sim}}</a>
      <a class="opt" href="#safeguards">{{nav_safe}}</a>
      <a href="#club">{{nav_club}}</a>
      <a class="opt" href="#evidence">{{nav_ev}}</a>
      <span class="langsel">{{_langsel}}</span>
    </div>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <svg class="hero-mark" viewBox="0 0 560 300" role="img" aria-label="TAX 28:28">
      <text x="60" y="168" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="196" fill="#0F3B5C" textLength="440" lengthAdjust="spacing">TAX</text>
      <text x="60" y="286" font-family="Space Grotesk,sans-serif" font-weight="700" font-size="116" fill="#0F3B5C" letter-spacing="-2" textLength="440" lengthAdjust="spacing">28:28</text>
    </svg>
    <h1>{{hero_h1}}</h1>
    <p class="claim2">{{hero_claim2}}</p>
    <p class="sub">{{hero_sub}}</p>
    <div class="cta-row">
      <a class="btn primary" href="#calc">{{hero_cta1}}</a>
      <a class="btn ghost" href="#concept">{{hero_cta2}}</a>
    </div>
    <p class="opensrc">{{hero_open}}</p>
    <div class="stamps">
      <div class="stamp"><div class="val">515&nbsp;€</div><div class="lbl">{{stamp1}}</div></div>
      <div class="stamp"><div class="val">{{stamp2v}}</div><div class="lbl">{{stamp2}}</div></div>
      <div class="stamp"><div class="val">+21&nbsp;%</div><div class="lbl">{{stamp3}}</div></div>
    </div>
    <p class="fineprint" style="text-align:center;margin:16px auto 0">{{stamp_note}}</p>
  </div>
</header>

<section id="diagnosis">
  <div class="wrap">
    <h2>{{diag_h2}}</h2>
    <p class="lede">{{diag_lede}}</p>
    <div class="befund-grid">
      <div class="befund"><div class="num">20.000+</div><h3>{{diag1t}}</h3><p>{{diag1p}}</p></div>
      <div class="befund"><div class="num">~40&nbsp;%</div><h3>{{diag2t}}</h3><p>{{diag2p}}</p></div>
      <div class="befund"><div class="num">80–90&nbsp;%</div><h3>{{diag3t}}</h3><p>{{diag3p}}</p></div>
      <div class="befund"><div class="num">0&nbsp;€</div><h3>{{diag4t}}</h3><p>{{diag4p}}</p></div>
    </div>
    <p class="fineprint">{{diag_fine}}</p>
  </div>
</section>

<section id="concept">
  <div class="wrap">
    <h2>{{con_h2}}</h2>
    <p class="lede">{{con_lede}}</p>
    <div class="mass-grid">

      <div class="mass"><div class="pos">{{p01pos}}</div><h3>{{p01t}}</h3>
        <div class="taxlbl" role="img" aria-label="{{p01aria}}">
          <div><b class="t1">0&nbsp;%</b><em>{{p01s1}}</em></div>
          <div><b class="t2">9&nbsp;%</b><em>{{p01s2}}</em></div>
          <div><b class="t3">16&nbsp;%</b><em>{{p01s3}}</em></div>
          <div><b class="t4">21&nbsp;%</b><em>{{p01s4}}</em></div>
          <div><b class="t5">26&nbsp;%</b><em>{{p01s5}}</em></div>
          <div><b class="t6">28&nbsp;%</b><em>{{p01s6}}</em></div>
        </div>
        <p>{{p01p}}</p></div>

      <div class="mass"><div class="pos">{{p02pos}}</div><h3>{{p02t}}</h3><span class="regel">{{p02r}}</span><p>{{p02p}}</p></div>

      <div class="mass"><div class="pos">{{p03pos}}</div><h3>{{p03t}}</h3><span class="regel">{{p03r}}</span><p>{{p03p}}</p></div>

      <div class="mass"><div class="pos">{{p04pos}}</div><h3>{{p04t}}</h3><span class="regel">{{p04r}}</span><p>{{p04p}}</p></div>

      <div class="mass"><div class="pos">{{p05pos}}</div><h3>{{p05t}}</h3><span class="regel">{{p05r}}</span><p>{{p05p}}</p></div>

      <div class="mass"><div class="pos">{{p06pos}}</div><h3>{{p06t}}</h3>
        <div class="vatlbl" role="img" aria-label="{{p06aria}}">
          <div><b class="v1">A+ &middot; 5&nbsp;%</b><em>{{p06s1}}</em></div>
          <div><b class="v2">A &middot; 11&nbsp;%</b><em>{{p06s2}}</em></div>
          <div><b class="v3">B &middot; 17&nbsp;%</b><em>{{p06s3}}</em></div>
          <div><b class="v4">C &middot; 22&nbsp;%</b><em>{{p06s4}}</em></div>
          <div><b class="v5">D &middot; 28&nbsp;%</b><em>{{p06s5}}</em></div>
        </div>
        <p>{{p06p}}</p></div>

      <div class="mass"><div class="pos">{{p07pos}}</div><h3>{{p07t}}</h3><span class="regel">{{p07r}}</span><p>{{p07p}}</p></div>

      <div class="mass"><div class="pos">{{p08pos}}</div><h3>{{p08t}}</h3>
        <svg class="spark" viewBox="0 0 260 86" role="img" aria-label="{{p08aria}}">
          <line x1="8" y1="72" x2="252" y2="72" stroke="#D8E1E8"></line>
          <path d="M8 56 H90 V36 H172 V16 H252" fill="none" stroke="#1D7A4F" stroke-width="2.5" stroke-linejoin="round"></path>
          <text x="10" y="50" font-family="IBM Plex Mono,monospace" font-size="10" fill="#1D7A4F">515 €</text>
          <text x="94" y="30" font-family="IBM Plex Mono,monospace" font-size="10" fill="#1D7A4F">566 €</text>
          <text x="176" y="11" font-family="IBM Plex Mono,monospace" font-size="10" fill="#1D7A4F">617 €</text>
          <text x="10" y="82" font-family="IBM Plex Mono,monospace" font-size="8.5" fill="#5A7186">50 %</text>
          <text x="94" y="82" font-family="IBM Plex Mono,monospace" font-size="8.5" fill="#5A7186">55 %</text>
          <text x="176" y="82" font-family="IBM Plex Mono,monospace" font-size="8.5" fill="#5A7186">60 %</text></svg>
        <p>{{p08p}}</p></div>

      <div class="mass"><div class="pos">{{p09pos}}</div><h3>{{p09t}}</h3><span class="regel">{{p09r}}</span><p>{{p09p}}</p></div>

      <div class="mass"><div class="pos">{{p10pos}}</div><h3>{{p10t}}</h3><span class="regel">{{p10r}}</span><p>{{p10p}}</p></div>
    </div>

    <div class="erbbox">
      <h3 class="sub-h">{{erb_h3}}</h3>
      <p>{{erb_p1}}</p>
      <p>{{erb_p2}}</p>
      <p>{{erb_p3}}</p>
    </div>
  </div>
</section>

<section id="calc">
  <div class="wrap">
    <h2>{{calc_h2}}</h2>
    <p class="lede">{{calc_lede}}</p>
    <p class="calibrate">{{calc_calib}}</p>
    <div class="calc">
      <div>
        <label class="lbl" for="brutto">{{calc_gross}}</label>
        <div class="bigval" id="bOut">–</div>
        <input type="range" id="brutto" min="0" max="200000" step="1000" value="42000" aria-describedby="bOut">
        <label class="lbl" id="lSt">{{calc_stage}}</label>
        <div class="seg" role="group" aria-labelledby="lSt">
          <button type="button" data-stufe="50" aria-pressed="true">515 € &middot; {{calc_start}}</button>
          <button type="button" data-stufe="55" aria-pressed="false">566 €</button>
          <button type="button" data-stufe="60" aria-pressed="false">617 €</button>
        </div>
        <label class="lbl" id="lKi">{{calc_kids}}</label>
        <div class="seg" role="group" aria-labelledby="lKi">
          <button type="button" data-kinder="0" aria-pressed="true">0</button>
          <button type="button" data-kinder="1" aria-pressed="false">1</button>
          <button type="button" data-kinder="2" aria-pressed="false">2</button>
          <button type="button" data-kinder="3" aria-pressed="false">3</button>
        </div>
        <label class="lbl">{{calc_hh}}</label>
        <div class="chk"><input type="checkbox" id="partner"><label for="partner" style="all:unset;cursor:pointer">{{calc_partner}}</label></div>
      </div>
      <div aria-live="polite">
        <div class="res-row"><span class="k">{{calc_r1}}</span><span class="v today" id="rHeute">–</span></div>
        <div class="res-row"><span class="k">{{calc_r2}}</span><span class="v new" id="rNeu">–</span></div>
        <div class="res-row"><span class="k">{{calc_r3}}</span><span class="v" id="rDD">–</span></div>
        <div class="res-row"><span class="k">{{calc_r4}}</span><span class="v" id="rEff">–</span></div>
        <div class="res-row"><span class="k">{{calc_r5}}</span><span class="v" id="rMw">–</span></div>
        <div class="bars" aria-hidden="true">
          <div class="bar-lbl"><span>{{calc_today}}</span><span id="bT"></span></div>
          <div class="bar today"><i id="barT" style="width:40%"></i></div>
          <div class="bar-lbl"><span>{{calc_new}}</span><span id="bN"></span></div>
          <div class="bar new"><i id="barN" style="width:60%"></i></div>
        </div>
        <div class="plus-box"><div class="plus" id="rPlus">–</div><div class="sub" id="rPlusSub">&nbsp;</div></div>
      </div>
    </div>
    <p class="fineprint">{{calc_fine}}</p>

    <h3 class="sub-h">{{hh_h3}}</h3>
    {{_tbl_hh}}
    <p class="fineprint">{{hh_fine}}</p>
  </div>
</section>

<section id="simulation">
  <div class="wrap">
    <h2>{{sim_h2}}</h2>
    <p class="lede">{{sim_lede}}</p>
    <div class="chart-card">
      <div class="tabs" role="group" aria-label="{{sim_pick}}" id="tabs"></div>
      <div class="unit" id="unit"></div>
      <svg id="chart" viewBox="0 0 960 400" role="img" aria-label="{{sim_aria}}"></svg>
      <div class="legend">
        <span class="l-hist"><i></i>{{sim_l1}}</span>
        <span class="l-ohne"><i></i>{{sim_l2}}</span>
        <span class="l-mit"><i></i>{{sim_l3}}</span>
      </div>
      <p class="fineprint">{{sim_fine}}</p>
    </div>
    <div class="split">
      <div>
        <h3>{{bud_h3}}</h3>
        <p>{{bud_p1}}</p>
        <p class="fineprint" style="margin-top:0">{{bud_p2}}</p>
      </div>
      <div>{{_tbl_sc}}</div>
    </div>
  </div>
</section>

<section id="safeguards">
  <div class="wrap">
    <h2>{{safe_h2}}</h2>
    <p class="lede">{{safe_lede}}</p>
    <div class="sich">
      <div><div><b>{{r1b}}</b><p>{{r1p}}</p></div></div>
      <div><div><b>{{r2b}}</b><p>{{r2p}}</p></div></div>
      <div><div><b>{{r3b}}</b><p>{{r3p}}</p></div></div>
      <div><div><b>{{r4b}}</b><p>{{r4p}}</p></div></div>
      <div><div><b>{{r5b}}</b><p>{{r5p}}</p></div></div>
    </div>
  </div>
</section>

<section id="club">
  <div class="wrap">
    <h2>{{cl_h2}}</h2>
    <p class="lede">{{cl_lede}}</p>

    <div class="timeline">
      <div><div class="y">{{cl_t1y}}</div><div class="t">{{cl_t1}}</div></div>
      <div><div class="y">{{cl_t2y}}</div><div class="t">{{cl_t2}}</div></div>
      <div><div class="y">{{cl_t3y}}</div><div class="t">{{cl_t3}}</div></div>
      <div><div class="y">{{cl_t4y}}</div><div class="t">{{cl_t4}}</div></div>
    </div>

    <div class="reg-grid">
      <div class="reg"><div class="n">{{cl_g1n}}</div><h3>{{cl_g1t}}</h3><p>{{cl_g1p}}</p></div>
      <div class="reg"><div class="n">{{cl_g2n}}</div><h3>{{cl_g2t}}</h3><p>{{cl_g2p}}</p></div>
      <div class="reg"><div class="n">{{cl_g3n}}</div><h3>{{cl_g3t}}</h3><p>{{cl_g3p}}</p></div>
    </div>

    <h3 class="sub-h" style="margin-top:8px">{{cl_ex_h3}}</h3>
    <p class="lede">{{cl_ex_p}}</p>
    <div class="flagrow">{{_flags}}</div>
    {{_tbl_club}}
    <p class="fineprint">{{cl_tbl_fine}}</p>

    <div class="effects">
      <div><h3>{{cl_e1t}}</h3><p>{{cl_e1p}}</p></div>
      <div><h3>{{cl_e2t}}</h3><p>{{cl_e2p}}</p></div>
      <div><h3>{{cl_e3t}}</h3><p>{{cl_e3p}}</p></div>
      <div><h3>{{cl_e4t}}</h3><p>{{cl_e4p}}</p></div>
      <div><h3>{{cl_e5t}}</h3><p>{{cl_e5p}}</p></div>
      <div><h3>{{cl_e6t}}</h3><p>{{cl_e6p}}</p></div>
    </div>

    <div class="box">
      <h3>{{cl_ee_h3}}</h3>
      <p>{{cl_ee_p}}</p>
      <ul>
        <li>{{cl_ee_l1}}</li>
        <li>{{cl_ee_l2}}</li>
        <li>{{cl_ee_l3}}</li>
        <li>{{cl_ee_l4}}</li>
      </ul>
    </div>

    <div class="box warn">
      <h3>{{cl_ie_h3}}</h3>
      <p>{{cl_ie_p}}</p>
      <ul>
        <li>{{cl_ie_l1}}</li>
        <li>{{cl_ie_l2}}</li>
        <li>{{cl_ie_l3}}</li>
        <li>{{cl_ie_l4}}</li>
      </ul>
    </div>

    <p class="fineprint">{{cl_limits}}</p>
  </div>
</section>

<section id="evidence">
  <div class="wrap">
    <h2>{{ev_h2}}</h2>
    <p class="lede">{{ev_lede}}</p>
    {{_tbl_beleg}}
    <p class="fineprint">{{ev_leg}}</p>
    <div class="calibrate" style="margin-top:18px;margin-bottom:0">{{ev_note}}</div>
  </div>
</section>

<section id="annex">
  <div class="wrap">
    <h2>{{anx_h2}}</h2>
    <p class="lede">{{anx_lede}}</p>
    <div class="anl">
      <button type="button" class="doclink" data-doc="doc-model"><span class="t">{{anx1t}}</span><span class="d">{{anx1d}}</span><span class="f">modell-2828.py &middot; Python</span></button>
      <button type="button" class="doclink" data-doc="doc-calc"><span class="t">{{anx2t}}</span><span class="d">{{anx2d}}</span><span class="f">rechner-2828.js &middot; JavaScript</span></button>
      <button type="button" class="doclink" data-doc="doc-club"><span class="t">{{anx3t}}</span><span class="d">{{anx3d}}</span><span class="f">klub10.py &middot; Python</span></button>
      <button type="button" class="doclink" data-doc="doc-src"><span class="t">{{anx4t}}</span><span class="d">{{anx4d}}</span><span class="f">{{anx4f}}</span></button>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <div><h4>{{ft_m_h}}</h4><p>{{ft_m_p}}</p><p class="verstamp">{{ver_label}} <b>{{ver_val}}</b></p></div>
    <div><h4>{{ft_c_h}}</h4><p>{{ft_c_p}}<br><a href="#top">{{ft_top}}</a></p></div>
    <div><h4>{{ft_i_h}}</h4><p>{{ft_i_p}}</p></div>
  </div>
  <p class="translation-note">{{ft_note}}</p>
</footer>

<div class="docmodal" id="docmodal" role="dialog" aria-modal="true" aria-labelledby="doctitle">
  <div class="docpanel">
    <div class="dochead"><b id="doctitle"></b><button type="button" id="docclose">{{doc_close}}</button></div>
    <div class="docbody">
      <div class="docitem" id="doc-model" data-title="{{anx1t}}"><pre>{{_src_model}}</pre></div>
      <div class="docitem" id="doc-calc" data-title="{{anx2t}}"><pre>{{_src_calc}}</pre></div>
      <div class="docitem" id="doc-club" data-title="{{anx3t}}"><pre>{{_src_club}}</pre></div>
      <div class="docitem" id="doc-src" data-title="{{anx4t}}"><pre>{{src_text}}</pre></div>
    </div>
  </div>
</div>

<script>
/* ---- Rechnerlogik: Recht 2026 gegen 28:28. Alle Beträge EUR/Jahr, Preise 2026. ---- */
const P={exmin:12348,dd:{50:515,55:566,60:617},kindAnteil:.5,
 tarifGrenzen:[12348,25000,40000,55000,70000,Infinity],tarifSaetze:[0,.09,.16,.21,.26,.28],
 svAN:{50:.14,55:.14,60:.09},bbgKV:69750,bbgRV:101400,anKVPV:.1055,anKinderlos:.006,
 anRVAV:.106,kindergeld:259,wk:1230,sa:36,soliFG:20350};
function est2026(z){z=Math.floor(Math.max(0,z));
 if(z<=12348)return 0;
 if(z<=17799){const y=(z-12348)/1e4;return Math.floor((914.51*y+1400)*y);}
 if(z<=69878){const x=(z-17799)/1e4;return Math.floor((173.10*x+2397)*x+1034.87);}
 if(z<=277825)return Math.floor(.42*z-11135.63);
 return Math.floor(.45*z-19470.38);}
function soli2026(e,sp){const fg=P.soliFG*(sp?2:1);return e<=fg?0:Math.min(.055*e,.119*(e-fg));}
function heute(b,k,p){const sv=(P.anKVPV+(k===0?P.anKinderlos:0))*Math.min(b,P.bbgKV)+P.anRVAV*Math.min(b,P.bbgRV);
 const z=Math.max(0,b-sv-(b>0?P.wk:0)-P.sa*(p?2:1));
 const e=p?2*est2026(z/2):est2026(z),s=soli2026(e,p);
 return {netto:b-sv-e-s+k*P.kindergeld*12,steuer:e+s,sv:sv};}
function est2828(x){let s=0,pr=0;for(let i=0;i<P.tarifSaetze.length;i++){const g=P.tarifGrenzen[i];
 if(x>pr)s+=(Math.min(x,g)-pr)*P.tarifSaetze[i];pr=g;if(x<=g)break;}return s;}
function neu(b,k,p,a){const dd=P.dd[a]*12,sv=P.svAN[a]*b,e=est2828(b+dd);
 const kd=k*P.dd[a]*P.kindAnteil*12,pt=p?dd-est2828(dd):0;
 return {netto:b-sv-e+dd+kd+pt,steuer:e,sv:sv,dividende:dd+kd+pt};}
function last(r,b){return b>0?(r.steuer+r.sv)/b*100:0;}

const LOC='{{_loc}}';
const $=id=>document.getElementById(id);
/* useGrouping:'always' — ohne das lassen es-ES und et-EE vierstellige Zahlen
   ungetrennt, was in einer Spalte neben 29.120 wie ein Fehler aussieht. */
const eur=v=>Math.round(v).toLocaleString(LOC,{useGrouping:'always'})+' €';
let stufe=50,kinder=0;
function konsumquote(n){return n<25000?.95:n<50000?.85:n<80000?.75:.60;}
function labelKosten(n){const r=.20,r0=.165;return n*konsumquote(n)*(r/(1+r)-r0/(1+r0));}
function calc(){
 const b=+$('brutto').value,p=$('partner').checked;
 $('bOut').textContent=eur(b);
 const h=heute(b,kinder,p),n=neu(b,kinder,p,stufe);
 const mw=labelKosten(n.netto),d=n.netto-mw-h.netto;
 $('rHeute').textContent=eur(h.netto);$('rNeu').textContent=eur(n.netto);
 $('rDD').textContent=eur(n.dividende);$('rMw').textContent='−'+eur(mw);
 $('rEff').textContent=b>0?last(h,b).toFixed(0)+' % → '+last(n,b).toFixed(0)+' %':'–';
 const mx=Math.max(h.netto,n.netto,1);
 $('barT').style.width=(h.netto/mx*100)+'%';$('barN').style.width=(n.netto/mx*100)+'%';
 $('bT').textContent=eur(h.netto);$('bN').textContent=eur(n.netto);
 const pl=$('rPlus');pl.textContent=(d>=0?'+':'−')+eur(Math.abs(d));pl.classList.toggle('neg',d<0);
 $('rPlusSub').textContent=(d>=0?'{{js_more}}':'{{js_less}}')+' '+(d>=0?'+':'−')+eur(Math.abs(d)/12)+' {{js_month}}';}
['brutto'].forEach(i=>$(i).addEventListener('input',calc));
$('partner').addEventListener('change',calc);
document.querySelectorAll('[data-stufe]').forEach(bt=>bt.addEventListener('click',()=>{stufe=+bt.dataset.stufe;
 document.querySelectorAll('[data-stufe]').forEach(x=>x.setAttribute('aria-pressed',x===bt));calc();}));
document.querySelectorAll('[data-kinder]').forEach(bt=>bt.addEventListener('click',()=>{kinder=+bt.dataset.kinder;
 document.querySelectorAll('[data-kinder]').forEach(x=>x.setAttribute('aria-pressed',x===bt));calc();}));
calc();

/* ---- Zeitreihen ---- */
const YEARS=[];for(let y=2010;y<=2035;y++)YEARS.push(y);
const METRICS={{_metrics}};
let metric=0;
const NS='http://www.w3.org/2000/svg';
function el(t,a){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e;}
const tabs=$('tabs');
METRICS.forEach((m,i)=>{const b=document.createElement('button');b.type='button';b.textContent=m.name;
 b.setAttribute('aria-pressed',i===0);b.addEventListener('click',()=>{metric=i;
 [...tabs.children].forEach((x,j)=>x.setAttribute('aria-pressed',j===i));draw();});tabs.appendChild(b);});
function draw(){
 const m=METRICS[metric],svg=$('chart');svg.innerHTML='';$('unit').textContent=m.unit;
 const W=960,H=400,L=64,R=26,T=20,B=40;
 const all=[...m.hist,...m.ohne,...m.mit];
 let lo=Math.min(...all),hi=Math.max(...all);const pad=(hi-lo)*.12||1;lo-=pad;hi+=pad;
 const X=i=>L+(W-L-R)*i/(YEARS.length-1);
 const Y=v=>T+(H-T-B)*(1-(v-lo)/(hi-lo));
 for(let g=0;g<=4;g++){const v=lo+(hi-lo)*g/4,y=Y(v);
  svg.appendChild(el('line',{x1:L,y1:y,x2:W-R,y2:y,class:'grid'}));
  const t=el('text',{x:L-10,y:y+4,'text-anchor':'end',class:'axis'});
  t.textContent=v.toLocaleString(LOC,{minimumFractionDigits:m.dec,maximumFractionDigits:m.dec});svg.appendChild(t);}
 YEARS.forEach((yr,i)=>{if(yr%5===0){const t=el('text',{x:X(i),y:H-B+24,'text-anchor':'middle',class:'axis'});
  t.textContent=yr;svg.appendChild(t);}});
 const x28=X(YEARS.indexOf(2028));
 svg.appendChild(el('line',{x1:x28,y1:T,x2:x28,y2:H-B,class:'marker'}));
 const lb=el('text',{x:x28+6,y:T+12,class:'axis'});lb.textContent='{{js_start}}';svg.appendChild(lb);
 const path=(v,i0,c)=>{let d='';v.forEach((y,i)=>{d+=(i?'L':'M')+X(i0+i).toFixed(1)+' '+Y(y).toFixed(1);});
  svg.appendChild(el('path',{d:d,class:c}));};
 const lastI=m.hist.length-1;
 path(m.hist,0,'hist');path([m.hist[lastI],...m.ohne],lastI,'ohne');path([m.hist[lastI],...m.mit],lastI,'mit');
 [['#B4452F',m.ohne],['#1D7A4F',m.mit]].forEach(([c,a])=>{
  const t=el('text',{x:X(YEARS.length-1)+4,y:Y(a[a.length-1])+4,'text-anchor':'start',
   'font-family':'IBM Plex Mono,monospace','font-size':12,'font-weight':500,fill:c});
  t.textContent=a[a.length-1].toLocaleString(LOC,{minimumFractionDigits:m.dec,maximumFractionDigits:m.dec});
  svg.appendChild(t);});}
draw();

/* ---- Anlagen ---- */
(function(){const modal=$('docmodal'),title=$('doctitle');
 document.querySelectorAll('.doclink').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();
  document.querySelectorAll('.docitem').forEach(d=>d.style.display='none');
  const d=$(a.dataset.doc);d.style.display='block';title.textContent=d.dataset.title;
  modal.style.display='flex';document.body.style.overflow='hidden';
  modal.querySelector('.docbody').scrollTop=0;}));
 const close=()=>{modal.style.display='none';document.body.style.overflow='';};
 $('docclose').addEventListener('click',close);
 modal.addEventListener('click',e=>{if(e.target===modal)close();});
 document.addEventListener('keydown',e=>{if(e.key==='Escape')close();});})();
</script>
</body></html>
"""
