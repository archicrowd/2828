# -*- coding: utf-8 -*-
"""Stylesheet. Grundlage: die ausgelieferte Seite 2525.archicrowd.de/index.html;
ergaenzt um Tabellen, Klub-Abschnitt und Hinweiszeilen."""

CSS = r"""
@font-face{font-family:'Space Grotesk';font-style:normal;font-weight:400;font-display:swap;src:url('fonts/SpaceGrotesk-400.woff2') format('woff2')}
@font-face{font-family:'Space Grotesk';font-style:normal;font-weight:500;font-display:swap;src:url('fonts/SpaceGrotesk-500.woff2') format('woff2')}
@font-face{font-family:'Space Grotesk';font-style:normal;font-weight:700;font-display:swap;src:url('fonts/SpaceGrotesk-700.woff2') format('woff2')}
@font-face{font-family:'Source Serif 4';font-style:normal;font-weight:400;font-display:swap;src:url('fonts/SourceSerif4-400.woff2') format('woff2')}
@font-face{font-family:'Source Serif 4';font-style:normal;font-weight:600;font-display:swap;src:url('fonts/SourceSerif4-600.woff2') format('woff2')}
@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400;font-display:swap;src:url('fonts/IBMPlexMono-400.woff2') format('woff2')}
@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:500;font-display:swap;src:url('fonts/IBMPlexMono-500.woff2') format('woff2')}

:root{
  --paper:#F6F7F4; --ink:#0F3B5C; --line:#B9C9D6; --line-soft:#D8E1E8;
  --accent:#1D7A4F; --accent-bg:#E7F2EC; --warn:#B4452F; --dim:#5A7186;
  --mono:'IBM Plex Mono',ui-monospace,monospace;
  --disp:'Space Grotesk',system-ui,sans-serif;
  --body:'Source Serif 4',Georgia,serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
body{background:var(--paper);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.65}
.wrap{max-width:1060px;margin:0 auto;padding:0 24px;min-width:0}
a{color:var(--ink)}
::selection{background:var(--ink);color:var(--paper)}

/* Navigationsleiste */
.titleblock{border-bottom:1.5px solid var(--ink);background:var(--paper);position:sticky;top:0;z-index:50}
.titleblock .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px;padding-top:12px;padding-bottom:12px}
.tb-left{font-family:var(--disp);font-size:20px;font-weight:700;letter-spacing:-.5px;text-decoration:none;white-space:nowrap}
.tb-right{display:flex;gap:20px;align-items:center;font-family:var(--mono);font-size:12px;letter-spacing:.06em;flex-wrap:wrap;justify-content:flex-end}
.tb-right a{text-decoration:none;color:var(--dim);text-transform:uppercase}
.tb-right a:hover,.tb-right a:focus-visible{color:var(--ink)}
.langsel{display:flex;gap:0;border:1px solid var(--line);border-radius:2px;overflow:hidden}
.langsel a{padding:5px 7px;font-size:11px;border-right:1px solid var(--line);color:var(--dim)}
.langsel a:last-child{border-right:none}
.langsel a.active{background:var(--ink);color:var(--paper)}
@media(max-width:860px){.tb-right .opt{display:none}}
@media(max-width:640px){.tb-right{gap:10px}.tb-right a{font-size:11px}.tb-left{font-size:17px}}

/* Kopf */
.hero{padding:64px 0 52px;border-bottom:1px solid var(--line)}
.hero-mark{display:block;margin:0 auto 6px;max-width:520px;width:100%;height:auto}
.hero h1{font-family:var(--disp);font-weight:700;font-size:clamp(25px,3.7vw,38px);line-height:1.15;text-align:center;max-width:820px;margin:16px auto 6px;text-wrap:balance}
.hero .claim2{font-family:var(--disp);font-weight:500;font-size:clamp(17px,2.1vw,21px);text-align:center;color:var(--accent);margin:0 auto 16px}
.hero p.sub{text-align:center;max-width:660px;margin:0 auto 26px;color:var(--dim);font-size:18px}
.cta-row{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-bottom:14px}
.btn{font-family:var(--disp);font-weight:500;font-size:16px;text-decoration:none;padding:13px 26px;border:1.5px solid var(--ink);border-radius:3px;transition:background .15s,color .15s}
.btn.primary{background:var(--ink);color:var(--paper)}
.btn.primary:hover{background:#0a2c46}
.btn.ghost:hover{background:var(--ink);color:var(--paper)}
.btn:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.opensrc{text-align:center;font-family:var(--mono);font-size:12.5px;color:var(--dim);margin-bottom:34px}
.stamps{display:flex;gap:0;justify-content:center;flex-wrap:wrap;border:1px solid var(--line);max-width:880px;margin:0 auto}
.stamp{flex:1 1 240px;padding:18px 20px;border-right:1px solid var(--line);text-align:center}
.stamp:last-child{border-right:none}
.stamp .val{font-family:var(--mono);font-size:26px;font-weight:500;color:var(--accent)}
.stamp .lbl{font-family:var(--mono);font-size:11.5px;letter-spacing:.06em;color:var(--dim);text-transform:uppercase;margin-top:5px;line-height:1.45}
@media(max-width:720px){.stamp{border-right:none;border-bottom:1px solid var(--line)}.stamp:last-child{border-bottom:none}}

/* Sektionen */
section{padding:60px 0;border-bottom:1px solid var(--line);overflow-x:clip;scroll-margin-top:72px}
h2{font-family:var(--disp);font-weight:700;font-size:clamp(23px,3vw,31px);margin-bottom:14px;text-wrap:balance}
.lede{max-width:700px;color:#2c4a63;margin-bottom:34px}
.fineprint{font-size:13.5px;color:var(--dim);margin-top:20px;line-height:1.6;max-width:820px}

/* Befund */
.befund-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(224px,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
.befund{background:var(--paper);padding:22px}
.befund .num{font-family:var(--mono);font-size:24px;color:var(--warn);font-weight:500}
.befund h3{font-family:var(--disp);font-size:16.5px;font-weight:500;margin:8px 0 6px}
.befund p{font-size:15px;color:var(--dim);line-height:1.55}

/* Bauteile */
.mass-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.mass{border:1px solid var(--line);border-radius:3px;padding:20px 22px;background:#fff}
.mass .pos{font-family:var(--mono);font-size:11.5px;color:var(--dim);letter-spacing:.08em;text-transform:uppercase}
.mass h3{font-family:var(--disp);font-size:17px;font-weight:500;margin:6px 0 4px}
.mass .regel{font-family:var(--mono);font-size:13px;color:var(--ink);background:var(--paper);border:1px solid var(--line-soft);border-radius:2px;padding:3px 8px;display:inline-block;margin:4px 0 8px}
.mass p{font-size:15px;color:var(--dim);line-height:1.55}
.vatlbl,.taxlbl{display:block;margin:10px 0}
.vatlbl>div,.taxlbl>div{display:flex;align-items:center;gap:8px;margin-bottom:3px}
.vatlbl b,.taxlbl b{font-weight:400;height:19px;line-height:19px;font-family:var(--mono);font-size:10.5px;
 letter-spacing:.02em;padding:0 11px 0 8px;white-space:nowrap;flex:0 0 auto;
 clip-path:polygon(0 0,calc(100% - 8px) 0,100% 50%,calc(100% - 8px) 100%,0 100%)}
.vatlbl em,.taxlbl em{font-style:normal;font-family:var(--mono);font-size:10.5px;color:var(--dim);
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.vatlbl b{color:#fff}
/* Leiter um 8px verbreitert: "A+ · 5 %" brauchte 60px bei 52px Kasten.
   Abstand von 12px je Stufe bleibt, die Proportion also auch. */
.vatlbl .v1{width:60px;background:#1D7A4F}
.vatlbl .v2{width:72px;background:#5A9E3C}
.vatlbl .v3{width:84px;background:#B79A1E}
.vatlbl .v4{width:96px;background:#C9702A}
.vatlbl .v5{width:108px;background:#B4452F}
.taxlbl .t1{width:46px;background:#DCE7EF;color:var(--ink)}
.taxlbl .t2{width:58px;background:#B9CFE0;color:var(--ink)}
.taxlbl .t3{width:70px;background:#8FB3CD;color:var(--ink)}
.taxlbl .t4{width:82px;background:#6497B8;color:#fff}
.taxlbl .t5{width:94px;background:#3D7196;color:#fff}
.taxlbl .t6{width:106px;background:#0F3B5C;color:#fff}
.spark{width:100%;height:auto;display:block;margin:10px 0 8px}

/* Tabellen */
.tscroll{overflow-x:auto;max-width:100%;min-width:0;border:1px solid var(--line);background:#fff}
table{border-collapse:collapse;width:100%;font-size:15px}
th,td{text-align:right;padding:9px 12px;border-bottom:1px solid var(--line-soft);white-space:nowrap}
th:first-child,td:first-child{text-align:left;white-space:normal;min-width:150px}
thead th{font-family:var(--mono);font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--dim);border-bottom:1.5px solid var(--ink);vertical-align:bottom;font-weight:400;white-space:normal;max-width:110px;line-height:1.35}
tbody td{font-family:var(--mono);font-size:14px}
tbody td:first-child{font-family:var(--body);font-size:15px}
tbody tr:last-child td{border-bottom:none}
td.pos{color:var(--accent);font-weight:500}
td.neg{color:var(--warn);font-weight:500}
tr.tot td{border-top:1.5px solid var(--ink);font-weight:500}

/* Rechner */
.calibrate{font-size:13px;color:var(--dim);border-left:2px solid var(--line);padding:6px 12px;margin-bottom:22px;background:#fff}
.calc{display:grid;grid-template-columns:1fr 1.2fr;gap:36px;border:1.5px solid var(--ink);border-radius:3px;background:#fff;padding:30px}
@media(max-width:860px){.calc{grid-template-columns:1fr;padding:22px}}
.calc label.lbl{display:block;font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--dim);margin:18px 0 8px}
.calc label.lbl:first-child{margin-top:0}
.calc input[type=range]{width:100%;accent-color:var(--ink)}
.calc .bigval{font-family:var(--mono);font-size:30px;font-weight:500}
.seg{display:flex;border:1px solid var(--line);border-radius:3px;overflow:hidden;width:100%}
.seg button{flex:1;font-family:var(--mono);font-size:12.5px;padding:9px 4px;background:#fff;border:none;border-right:1px solid var(--line);cursor:pointer;color:var(--dim)}
.seg button:last-child{border-right:none}
.seg button[aria-pressed=true]{background:var(--ink);color:var(--paper)}
.seg button:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.chk{display:flex;align-items:center;gap:10px;font-size:15.5px;color:var(--ink);margin-top:6px}
.chk input{width:17px;height:17px;accent-color:var(--ink)}
.res-row{display:flex;justify-content:space-between;align-items:baseline;padding:10px 0;border-bottom:1px solid var(--line-soft);gap:12px}
.res-row .k{font-family:var(--mono);font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--dim)}
.res-row .v{font-family:var(--mono);font-size:18px;white-space:nowrap}
.res-row .v.today{color:var(--warn)}
.res-row .v.new{color:var(--ink);font-weight:500}
.plus-box{margin-top:18px;background:var(--accent-bg);border:1.5px solid var(--accent);border-radius:3px;padding:16px 20px;text-align:center}
.plus-box .plus{font-family:var(--mono);font-size:32px;font-weight:500;color:var(--accent)}
.plus-box .plus.neg{color:var(--warn)}
.plus-box .sub{font-family:var(--mono);font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--accent);margin-top:4px;line-height:1.45}
.bars{margin-top:18px}
.bar-lbl{display:flex;justify-content:space-between;font-family:var(--mono);font-size:12px;color:var(--dim);margin-bottom:4px}
.bar{height:14px;background:var(--line-soft);border-radius:2px;overflow:hidden;margin-bottom:12px}
.bar>i{display:block;height:100%;transition:width .35s}
.bar.today>i{background:var(--warn)}
.bar.new>i{background:var(--accent)}
h3.sub-h{font-family:var(--disp);font-size:21px;font-weight:700;margin:40px 0 10px}

/* Diagramm */
.chart-card{border:1.5px solid var(--ink);border-radius:3px;background:#fff;padding:26px}
@media(max-width:640px){.chart-card{padding:16px}}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.tabs button{font-family:var(--mono);font-size:12.5px;padding:8px 12px;border:1px solid var(--line);background:#fff;border-radius:3px;cursor:pointer;color:var(--dim)}
.tabs button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.tabs button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.unit{font-family:var(--mono);font-size:12px;color:var(--dim);margin-bottom:6px}
.legend{display:flex;gap:24px;flex-wrap:wrap;font-family:var(--mono);font-size:12.5px;color:var(--dim);margin-top:12px}
.legend i{display:inline-block;width:22px;height:0;border-top:3px solid;vertical-align:middle;margin-right:8px}
.legend .l-hist i{border-color:var(--ink)}
.legend .l-ohne i{border-color:var(--warn);border-top-style:dashed}
.legend .l-mit i{border-color:var(--accent)}
#chart{width:100%;height:auto;display:block}
#chart .grid{stroke:var(--line-soft)}
#chart .axis{font-family:var(--mono);font-size:12px;fill:var(--dim)}
#chart .hist{stroke:var(--ink);fill:none;stroke-width:2.5;stroke-linecap:round}
#chart .ohne{stroke:var(--warn);fill:none;stroke-width:2.5;stroke-dasharray:7 6;stroke-linecap:round}
#chart .mit{stroke:var(--accent);fill:none;stroke-width:3.5;stroke-linecap:round}
#chart .marker{stroke:var(--line);stroke-dasharray:3 4}
.split{display:grid;grid-template-columns:1fr 1.35fr;gap:34px;margin-top:38px;align-items:start}
.split>div{min-width:0}
@media(max-width:860px){.split{grid-template-columns:1fr;gap:22px}}
.split h3{font-family:var(--disp);font-size:21px;font-weight:700;margin-bottom:8px}
.split p{margin-bottom:10px}

/* Sicherungen */
.sich{max-width:800px;border-top:1.5px solid var(--ink);counter-reset:s}
.sich>div{display:flex;gap:18px;padding:18px 0;border-bottom:1px solid var(--line-soft)}
.sich>div::before{counter-increment:s;content:counter(s);font-family:var(--disp);font-weight:700;font-size:34px;color:var(--accent);line-height:1;min-width:38px}
.sich b{font-family:var(--disp);font-weight:500;font-size:19px;display:block;margin-bottom:2px}
.sich p{font-size:15.5px;color:var(--dim)}

/* Klub der Sieben */
.reg-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:14px;margin-bottom:34px}
.reg{border:1px solid var(--line);border-radius:3px;background:#fff;padding:20px 22px}
.reg .n{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.reg h3{font-family:var(--disp);font-size:17px;font-weight:500;margin:6px 0 6px}
.reg p{font-size:15px;color:var(--dim);line-height:1.55}
.flagrow{display:grid;grid-template-columns:repeat(10,1fr);border:1px solid var(--line);border-bottom:none;margin-bottom:26px;background:#fff}
.flagrow div{text-align:center;padding:14px 4px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.flagrow div:nth-child(10n){border-right:none}
.flagrow .c{font-family:var(--mono);font-size:17px;font-weight:500;color:var(--accent);white-space:nowrap}
.flagrow .n{font-family:var(--mono);font-size:10.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--dim);margin-top:4px;line-height:1.35}
@media(max-width:980px){.flagrow{grid-template-columns:repeat(5,1fr)}.flagrow div:nth-child(10n){border-right:1px solid var(--line)}.flagrow div:nth-child(5n){border-right:none}}
@media(max-width:560px){.flagrow{grid-template-columns:repeat(3,1fr)}.flagrow div:nth-child(5n){border-right:1px solid var(--line)}.flagrow div:nth-child(3n){border-right:none}}
.effects{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin-top:34px}
.effects>div{background:var(--paper);padding:20px 22px}
.effects h3{font-family:var(--disp);font-size:16.5px;font-weight:500;margin-bottom:6px}
.effects p{font-size:15px;color:var(--dim);line-height:1.55}
.box{border:1.5px solid var(--accent);background:var(--accent-bg);border-radius:3px;padding:22px 24px;margin-top:34px}
.box h3{font-family:var(--disp);font-size:19px;font-weight:700;margin-bottom:8px}
.box.warn{border-color:var(--warn);background:#FBF0ED}
.box.warn h3{color:var(--warn)}
.box p{font-size:15.5px;margin-bottom:8px}
.box ul{margin:8px 0 0 20px;font-size:15.5px}
.box li{margin:5px 0}
.timeline{display:flex;flex-wrap:wrap;gap:0;border:1px solid var(--line);margin:0 0 34px;background:#fff}
.timeline div{flex:1 1 200px;padding:16px 18px;border-right:1px solid var(--line)}
.timeline div:last-child{border-right:none}
.timeline .y{font-family:var(--mono);font-size:15px;font-weight:500;color:var(--accent)}
.timeline .t{font-size:14.5px;color:var(--dim);margin-top:4px;line-height:1.5}
@media(max-width:700px){.timeline div{border-right:none;border-bottom:1px solid var(--line)}.timeline div:last-child{border-bottom:none}}

/* Anlagen */
.anl{display:grid;grid-template-columns:repeat(auto-fit,minmax(228px,1fr));gap:16px}
.anl button{all:unset;cursor:pointer;border:1.5px solid var(--ink);border-radius:3px;padding:20px;background:#fff;display:block}
.anl button:hover{border-color:var(--accent)}
.anl button:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.anl .t{font-family:var(--disp);font-weight:700;font-size:18px;display:block}
.anl .d{font-size:14.5px;color:var(--dim);display:block;margin-top:4px;line-height:1.5}
.anl .f{font-family:var(--mono);font-size:11.5px;color:var(--accent);display:block;margin-top:10px}

footer{padding:44px 0 60px;font-size:14.5px;color:var(--dim)}
footer .wrap{display:grid;grid-template-columns:2fr 1fr 1fr;gap:34px}
@media(max-width:720px){footer .wrap{grid-template-columns:1fr}}
footer h4{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);margin-bottom:10px}
footer a{color:var(--dim)}
.translation-note{max-width:1060px;margin:18px auto 0;padding:0 24px;font-family:var(--mono);font-size:11.5px;color:var(--dim);text-align:center;letter-spacing:.04em;line-height:1.6}

/* Anlagen-Leser */
.docmodal{display:none;position:fixed;inset:0;background:rgba(15,59,92,.45);z-index:100;align-items:flex-start;justify-content:center;padding:4vh 16px}
.docpanel{background:var(--paper);border:1.5px solid var(--ink);border-radius:3px;max-width:900px;width:100%;max-height:92vh;display:flex;flex-direction:column}
.dochead{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:14px 20px;border-bottom:1.5px solid var(--ink)}
.dochead b{font-family:var(--mono);font-size:12.5px;letter-spacing:.06em}
.dochead button{font-family:var(--mono);font-size:13px;background:none;border:1px solid var(--ink);border-radius:2px;padding:6px 12px;cursor:pointer;color:var(--ink)}
.dochead button:hover{background:var(--ink);color:var(--paper)}
.docbody{overflow-y:auto;padding:22px 26px}
.docbody pre{font-family:var(--mono);font-size:12.5px;line-height:1.65;white-space:pre-wrap;word-wrap:break-word;color:#1c3a52}
.docitem{display:none}

/* ---- Belegstand: Stufe doppelt kodiert, als Blockanzeige und als Wort ---- */
table.beleg{table-layout:fixed;width:100%;min-width:720px}
.beleg th,.beleg td{text-align:left;white-space:normal;vertical-align:top;
  font-family:var(--body);font-size:14px;line-height:1.5}
.beleg col.c1{width:15%}.beleg col.c2{width:21%}.beleg col.c3{width:16%}.beleg col.c4{width:48%}
.beleg tbody td:first-child{font-family:var(--mono);font-size:12px;color:var(--dim);
  text-transform:uppercase;letter-spacing:.03em;line-height:1.4}
.beleg tbody td.claim{font-weight:500;color:var(--ink);font-size:14.5px}
.beleg td.st{font-family:var(--mono);font-size:12px;letter-spacing:.02em}
.beleg td.st .w{display:block;margin-top:5px}
.meter{display:flex;gap:3px}
.meter i{width:10px;height:10px;border:1.4px solid var(--line);display:block;border-radius:1px}
.st.s3 .meter i{background:var(--accent);border-color:var(--accent)}
.st.s2 .meter i:nth-child(-n+2){background:var(--accent);border-color:var(--accent)}
.st.s1 .meter i:nth-child(1){background:#9A6B18;border-color:#9A6B18}
.st.s0 .meter i{border-color:var(--warn)}
.st.s3,.st.s2{color:var(--accent)}
.st.s1{color:#7A5413}
.st.s0{color:var(--warn)}
.verstamp{font-family:var(--mono);font-size:12px;margin-top:12px!important;color:var(--dim)}
.verstamp b{color:var(--accent);font-weight:500}
@media(max-width:720px){
  /* Unter 720px keine Tabelle mehr: je Position ein Block. Sonst scrollt die
     Begruendungsspalte aus dem Bild und laesst leere hohe Zeilen zurueck. */
  .belegwrap{overflow:visible;border:none;background:transparent}
  table.beleg,.beleg tbody,.beleg tr,.beleg td{display:block;width:auto;min-width:0}
  .beleg thead,.beleg colgroup{display:none}
  .beleg tr{border:1px solid var(--line);background:#fff;padding:15px 16px;margin-bottom:10px}
  .beleg td{border:none;padding:0}
  .beleg tbody td:first-child{margin-bottom:5px}
  .beleg tbody td.claim{font-size:16.5px;line-height:1.35;margin-bottom:9px}
  .beleg td.st{display:flex;align-items:center;gap:9px;margin-bottom:9px}
  .beleg td.st .w{display:inline;margin-top:0}
  .beleg tbody td:last-child{font-size:14px;color:var(--dim)}
}

/* ---- Regeltext zur Stundung unter den Positionen ---- */
.erbbox{margin-top:36px;max-width:760px}
.erbbox .sub-h{margin-top:0}
.erbbox p{font-size:16px;line-height:1.65;color:var(--ink);margin-bottom:14px}
.erbbox p:last-child{margin-bottom:0;color:var(--dim)}
"""
