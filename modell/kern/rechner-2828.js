/* 28:28 – Rechnerlogik (Recht 2026 vs. 28:28). Alle Beträge EUR/Jahr, Preise 2026.
   Quelle heute: § 32a EStG 2026, SV-Rechengrößen 2026, Soli-Freigrenze 2026, Kindergeld 259 €. */
const P = {
  exmin: 12348, dd: {50: 515, 55: 566, 60: 617}, kindAnteil: 0.5,
  tarifGrenzen: [12348, 25000, 40000, 55000, 70000, Infinity],
  tarifSaetze:  [0, .09, .16, .21, .26, .28],
  svAN: {50: .14, 55: .14, 60: .09},
  bbgKV: 69750, bbgRV: 101400, anKVPV: .1055, anKinderlos: .006, anRVAV: .106,
  kindergeld: 259, wk: 1230, sa: 36, soliFG: 20350
};
function est2026(zve){ zve=Math.floor(Math.max(0,zve));
  if(zve<=12348) return 0;
  if(zve<=17799){const y=(zve-12348)/1e4; return Math.floor((914.51*y+1400)*y);}
  if(zve<=69878){const z=(zve-17799)/1e4; return Math.floor((173.10*z+2397)*z+1034.87);}
  if(zve<=277825) return Math.floor(.42*zve-11135.63);
  return Math.floor(.45*zve-19470.38); }
function soli2026(e,split){const fg=P.soliFG*(split?2:1); return e<=fg?0:Math.min(.055*e,.119*(e-fg));}
function heute(b,kinder,partner){
  const sv=(P.anKVPV+(kinder===0?P.anKinderlos:0))*Math.min(b,P.bbgKV)+P.anRVAV*Math.min(b,P.bbgRV);
  const zve=Math.max(0,b-sv-(b>0?P.wk:0)-P.sa*(partner?2:1));
  const e=partner?2*est2026(zve/2):est2026(zve); const s=soli2026(e,partner);
  return {netto:b-sv-e-s+kinder*P.kindergeld*12, steuer:e+s, sv:sv};
}
function est2828(x){let s=0,prev=0;
  for(let i=0;i<P.tarifSaetze.length;i++){const g=P.tarifGrenzen[i];
    if(x>prev) s+=(Math.min(x,g)-prev)*P.tarifSaetze[i]; prev=g; if(x<=g) break;}
  return s;}
function neu(b,kinder,partner,anteil=50){
  const dd=P.dd[anteil]*12, sv=P.svAN[anteil]*b, e=est2828(b+dd);
  const kind=kinder*P.dd[anteil]*P.kindAnteil*12;
  const p=partner?dd-est2828(dd):0;
  return {netto:b-sv-e+dd+kind+p, steuer:e, sv:sv, dividende:dd+kind+p};
}
/* Effektive Abgabenlast (Anzeige "heute → neu"): (Steuer + SV) / Brutto; neu inkl. Steuer auf die Dividende */
function abgabenlast(r,b){return b>0?(r.steuer+r.sv)/b*100:0;}
