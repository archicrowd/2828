// Baut dokumente/entwurf/TAX-Drittel-Konzept.docx: das Konzept des Drittel-Systems mit den Beschlüssen bis v3.51 und den neuen Begriffen
// (Goldenes Drittel, starkes Netz, Transformationsdividende, eigene Route, Zukunftsschatz). Entwurf zur Prüfung; die Gesamtrechnung (28:28) und das
// veröffentlichte Gesamtkonzept bleiben unberührt. Jede Zahl kommt aus daten/aggregate/*.json (Prüfrechnungen modell/*33.py, altlasten.py).
// Aufruf aus dem Repository-Wurzelordner: NODE_PATH=/opt/npm-tools/node_modules node dokumente/werkzeuge/konzept33-bau.js
const KURZ=process.argv.includes('--kurz');   // v4.0: Kurzfassung = Titel, Abschnitte 1 und 2
const d=require('docx');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,Table,TableRow,TableCell,WidthType,ShadingType,AlignmentType,BorderStyle,PageBreak,
       Footer,PageNumber,LevelFormat,TableOfContents}=d;
const fs=require('fs'); const path=require('path');
const WURZEL=path.resolve(__dirname,'..','..');
const lies=n=>JSON.parse(fs.readFileSync(path.join(WURZEL,'daten','aggregate',n),'utf8'));
const SV=lies('systemvarianten.json'), PJ=lies('projektion33.json'), NZ=lies('netz33.json'), H=lies('haushalte33.json'), RA=lies('haushalte33_raster.json'),
      AL=lies('altlasten.json'), EW=lies('einwanderung33.json'), DY=lies('dynamik33.json'), G=lies('gesamtrechnung.json'), MR=lies('moeglichkeitsraum33.json'), NS=lies('neustart33.json');
// v4.8/v4.11: Grundauskommen (vorher „Boden“), Kinderanteil 0,8, Kindergewicht, Härtefall, Gini
const GL=lies('gesamtlast33.json'), RBJ=lies('regel_boden.json'), HF=lies('haertefall.json'), GI=lies('gini.json'), KG=lies('kindergewicht.json'), GF=lies('gini_frankreich.json'), RK=lies('rentner_kombi.json');
const WS=lies('weitergabe_sensitivitaet.json'), FZ=lies('fondszins.json'), FK=lies('fonds_klub.json'), PN=lies('preisniveau33.json'), AW=lies('ausweichen33.json'), WR=lies('weitergabe_rueckfall.json');   // v4.18
const TOPF=RBJ.topf, SK=RBJ.regel.kinderanteil, KW=RBJ.regel.skala.kind;
const dv=x=>x*TOPF;   // Dividende je Erwachsenem bei Kinderanteil 0,8 (gleicher Topf)
const de=(x,nk=0)=>Number(x).toLocaleString('de-DE',{minimumFractionDigits:nk,maximumFractionDigits:nk});
const pr=(x,nk=1)=>de(x,nk)+' %';
const eu=x=>de(x)+' €';
const vz=x=>(x>=0?'+':'−')+de(Math.abs(x))+' €';

// ---- Zahlen
const V=SV.varianten.find(v=>v.id===PJ.system);
const PR=Object.fromEntries(PJ.reihe.map(r=>[r.jahr,r]));
const NB=NZ.varianten.find(v=>v.grundrente===`mindestrente_${NZ.beschluss.pflicht_satz}`).reihe;
const vr=NZ.varianten.find(v=>v.grundrente==='volksrente'&&v.gesundheit_kuerzung===NZ.beschluss.gesundheit_kuerzung).reihe;
const z3=NZ.varianten.find(v=>v.grundrente==='zwei_drittel').reihe;
const gem=j=>V.quote_kern-PR[j].dach_ohne_zins-PR[j].dividende_ohne_trends_pct_bip;
const deck=j=>PR[j].deckung+PR[j].progression;
const FG=lies('fonds_geltend.json'), AB=FG;   // v4.20: geltender Fonds der 30 Staaten
const fall=(hh,zu,j=2028)=>H.faelle.find(f=>f.jahr===j&&f.haushalt===hh&&f.weitergabe_ag===0.8&&f.vorsorge_satz===0.1&&f.zuschlag_pct===zu);
const ZU=Math.max(...H.faelle.map(f=>f.zuschlag_pct));
const zl=(f,b)=>f.zeilen.find(z=>z.brutto===b);
const gi=RA.grenz_brutto.indexOf(55000);
const rent=(r,zu)=>H.rentner.find(x=>x.rente_monat===r&&x.zuschlag_pct===zu);
const dyn=(b,ki,kv)=>DY.szenarien.find(x=>x.beschaeftigung_pct===b&&x.ki_pp===ki&&x.kapital_verschiebung_pp===kv).reihe['2060'];
const dyn0=dyn(0,0,0);
const ew=(m,a)=>EW.szenarien.find(s=>s.zusatz_pct===m&&s.integration===a);
const G26=12348, f26=1.0404;
const kind28=dv(NB['2028'].dividende_erw_eur2026)*SK;
const dRent=0;   // v4.10, Korrektur 65: Die Dividende ist in der Bestandsrente enthalten (Fonds zahlt nur den Anspruch darüber); R1 ändert das Rentnernetto nicht

// ---- Bausteine des Dokuments
const W=9026,grau="F2F2F2",akz="E8EEF7",gold="FFF4D6";
const F="Calibri";
const P=(t,{b,i,sz=21,sp=120,al}={})=>new Paragraph({alignment:al,spacing:{after:sp},children:[new TextRun({text:t,bold:!!b,italics:!!i,size:sz,font:F})]});
const R=(r,{sp=120}={})=>new Paragraph({spacing:{after:sp},children:r.map(x=>new TextRun({text:x[0],bold:!!x[1],italics:!!x[2],size:21,font:F}))});
const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:340,after:140},children:[new TextRun({text:t,font:F,bold:true,size:28,color:"1F3864"})]});
const H2=t=>new Paragraph({heading:HeadingLevel.HEADING_2,spacing:{before:220,after:120},children:[new TextRun({text:t,font:F,bold:true,size:23,color:"1F3864"})]});
const L=(t,lvl=0)=>new Paragraph({numbering:{reference:"punkte",level:lvl},spacing:{after:60},children:(Array.isArray(t)?t:[[t]]).map(x=>new TextRun({text:x[0],bold:!!x[1],size:21,font:F}))});
const c=(t,{w,b,fill,al}={})=>new TableCell({width:{size:w,type:WidthType.DXA},shading:fill?{type:ShadingType.CLEAR,fill,color:"auto"}:undefined,
  margins:{top:60,bottom:60,left:100,right:100},children:[new Paragraph({alignment:al,spacing:{after:0},children:[new TextRun({text:String(t),bold:!!b,size:19,font:F})]})]});
const tab=(cols,rows,{hl={}}={})=>{const ws=cols.map(x=>x.w);const s=ws.reduce((a,b)=>a+b,0);
  return new Table({columnWidths:ws,width:{size:s,type:WidthType.DXA},rows:[new TableRow({tableHeader:true,children:cols.map(x=>c(x.t,{w:x.w,b:true,fill:grau,al:x.al}))}),
    ...rows.map((r,i)=>new TableRow({children:r.map((t,j)=>c(t,{w:ws[j],b:!!hl[i],fill:hl[i]?(hl[i]===2?gold:akz):undefined,al:cols[j].al}))}))]})};
const Q=t=>P(t,{i:true,sz:18,sp:200});
const BR=()=>new Paragraph({children:[new PageBreak()]});
const RT=AlignmentType.RIGHT;
const kasten=(titel,zeilen)=>new Table({columnWidths:[W],width:{size:W,type:WidthType.DXA},rows:[new TableRow({children:[new TableCell({width:{size:W,type:WidthType.DXA},
  shading:{type:ShadingType.CLEAR,fill:gold,color:"auto"},margins:{top:120,bottom:120,left:180,right:180},
  children:[new Paragraph({spacing:{after:80},children:[new TextRun({text:titel,bold:true,size:22,font:F,color:"7A5A00"})]}),
    ...zeilen.map(z=>new Paragraph({spacing:{after:60},children:[new TextRun({text:z,size:21,font:F})]}))]})]})]});

const inhalt=[];
const add=(...x)=>inhalt.push(...x);

// ---- Titel
add(new Paragraph({spacing:{before:1800,after:200},children:[new TextRun({text:"Das Goldene Drittel",font:F,bold:true,size:56,color:"1F3864"})]}),
  P("Bauplan für ein einfaches Steuer- und Sozialsystem: höchstens ein Drittel auf jeden Euro, ein starkes Netz als Grundversorgung, eine Transformationsdividende für alle",{sz:28,sp:400}),
  P("Initiative 28:28 · "+(KURZ?"Kurzfassung · ":"")+"Fassung 4.39 · 24. Oktober 2026 (zur Freigabe)",{sz:22}),
  P("Alle Zahlen stammen aus offenen Prüfrechnungen (Repository, Ordner modell/ und daten/aggregate/). Beträge in Euro sind, wenn nicht anders angegeben, Euro je Monat in Kaufkraft 2026 für Deutschland als Referenzland; Anteile sind Prozent der Wirtschaftsleistung (BIP) im Durchschnitt der zehn gerechneten Staaten.",{i:true,sz:19,sp:200}),
  P("Lizenz: Text und Ergebnisse CC BY 4.0, Skripte MIT.",{sz:18}),
  ...(KURZ?[]:[BR(),new TableOfContents("Inhalt",{hyperlink:true,headingStyleRange:"1-2"}),BR()]));

// ---- 1 Kurzfassung
add(H1("1  Kurzfassung"),
  kasten("Der Bauplan in vier Sätzen",[
    "Sie zahlen höchstens das Goldene Drittel: 33 % auf jeden Euro, ob aus Arbeit, Kapital, Gewinn oder Erbe – keine Sozialbeiträge, keine Prämien.",
    "Das starke Netz trägt Sie: eine brauchbare Grundversorgung ohne Extras – geknüpft aus vielen Knoten, jeder hält mit, keiner fällt durch.",
    "Die Transformationsdividende kommt jeden Monat aufs Konto: Sie gibt zurück, was der Wandel einbringt, und wird kleiner, wenn das Schädliche verschwindet.",
    "Alles darüber ist Ihre eigene Route: eigene Vorsorge auf Ihrem Konto, Zusatzversicherungen, eigener Einsatz."]),
  P("",{sp:120}),
  tab([{t:"Kennzahl",w:5426},{t:"Wert",w:3600,al:RT}],[
    ["Höchstsatz auf jedes Einkommen","33 %"],
    ["Sozialbeiträge, Prämien","0 €"],
    ["Pflichtvorsorge auf eigenem Konto",pr(NZ.beschluss.pflicht_satz*100,0)+" des Lohns"],
    ["Mehrwertsteuer (Label) im Mittel",pr(V.label_effektiv,1)],
    ["Steuern insgesamt (Goldenes Drittel), 2028",pr(V.deckung,1)+" des BIP"],
    ["Starkes Netz, 2028",pr(NB['2028'].netz_pct_bip,1)+" des BIP"],
    ["Transformationsdividende je Erwachsenem, 2028 / 2060",eu(dv(NB['2028'].dividende_erw_eur2026))+" / "+eu(dv(NB['2060'].dividende_erw_eur2026))],
    ["Transformationsdividende je Kind, 2028",eu(kind28)+" ("+pr(SK*100,0)+" der Erwachsenen)"],
    ["Grundauskommen: Grundbedarf, weitere Erwachsene / Kinder","× 0,5 / × "+de(KW,2)+"; eigenes Einkommen zur Hälfte angerechnet"],
    ["Alleinstehend, 42.000 € brutto, mit Altlastenzuschlag: mehr im Monat",vz(RBJ.beispiele_de['alleinstehend']['42000'].mehr)],
    ["Beschäftigte mit mehr verfügbarem Einkommen (heute mit Bürgergeld, Haushaltstypen)",pr(Math.min(...Object.values(RBJ.staaten.DE.anteil)),0)+" bis "+pr(Math.max(...Object.values(RBJ.staaten.DE.anteil)),0)],
    ["Rentnerinnen und Rentner (Renten 900–2.200 €), mit Altlastenzuschlag",vz(Math.max(...H.rentner.filter(r=>r.zuschlag_pct===ZU).map(r=>r.differenz_monat))+dRent)+" bis "+vz(Math.min(...H.rentner.filter(r=>r.zuschlag_pct===ZU).map(r=>r.differenz_monat))+dRent)],
    ["Ungleichheit (Gini, 0–100): heute 2025 / 2028",de(GI.staaten.DE.gini_amtlich_2025,1)+" / "+de(GI.staaten.DE.reihe.find(z=>z.jahr===2028).mitte,1)],
    ["Pflichtzahlungen 2028 in % des BIP: heute / neu (Steuern + Altlastenfonds; mit Pflichtvorsorge aufs eigene Konto)",de(GL.heute,1)+" / "+de(GL.reihe[0].a_steuern_und_fonds,1)+" ("+de(GL.reihe[0].b_mit_pflichtvorsorge,1)+")"],
    ["Grenzbelastung bei 55.000 € brutto: heute / neu",pr(RA.grenz_heute[gi],0)+" / "+pr(RA.grenz_neu['0.8'][gi],0)]]),
  P("",{sp:120}),
  P("Was das System leistet, liegt nicht in einer großen Geldzahlung, sondern in drei Dingen: Arbeit wird nicht mehr doppelt belastet, jeder ist ohne Prämie grundversorgt, und was jemand darüber hinaus verdient und spart, gehört ihm. Der Bauplan nimmt aus vielen erprobten Vorbildern die besten Teile; jeder Staat kann ihn übernehmen."));

// ---- 2 Begriffe
add(H1("2  Begriffe"),
  P("Die Begriffe sind Vorschläge der Initiative (17. Oktober 2026); markenrechtlich nicht geprüft."),
  tab([{t:"Begriff",w:2300},{t:"Bedeutung",w:6726}],[
    ["Das Goldene Drittel","Die Einnahmeregel: Kein Euro wird mit mehr als einem Drittel besteuert – Einkommen, Kapitalerträge, Unternehmensgewinne, Erbschaften. Umfasst alle Steuern des Systems."],
    ["Das starke Netz","Die Grundversorgung ohne Prämie: Gesundheit, Pflege als Teilkasko, Mindestrente, Grundbedarf bei Invalidität und Arbeitslosigkeit, Waisen, Härtefall. Keine Extras."],
    ["Transformationsdividende","Monatliche Zahlung an jeden Erwachsenen (Kinder 80 %), ohne Antrag. Sie ist der Rest nach allen Aufgaben und gibt vor allem zurück, was Lenkungssteuern einbringen."],
    ["Ihre eigene Route","Alles über der Grundversorgung: Pflichtvorsorge auf eigenem, vererbbarem Konto, freiwillige Vorsorge, Zusatzversicherungen (Komfort, Lohnersatz, Berufsunfähigkeit)."],
    ["Pflichtvorsorge","10 % des Bruttolohns auf ein eigenes Konto. Kein Beitrag an den Staat: Das Geld gehört dem Sparer."],
    ["Mindestrente","Aufstockung ab 67 bis zum Grundbedarf, die eigene Rente wird nur zur Hälfte angerechnet."],
    ["Grundauskommen","Was jedem Haushalt sicher bleibt: Grundbedarf des Landes, je weitere/n Erwachsene/n × 0,5, je Kind × "+de(KW,2)+". Wer darunter liegt, wird aufgestockt – im Erwerbsalter wie im Alter (dort Mindestrente genannt). Dividenden und Renten aus dem alten System zählen voll, selbst verdientes Einkommen und eigene Vorsorge zur Hälfte. Pflichtvorsorge ab dem ersten Euro."],
    ["Härtefall","Zuschlag zum Grundauskommen für Wohnkosten über dem Wohnanteil, Mehrbedarf und einmalige Notlagen; ausgezahlt von der Gemeinde."],
    ["Rentenbeginn","67 Jahre; steigt um zwei Drittel des Zuwachses der Lebenserwartung mit 65 (ab 2030, 15 Jahre im Voraus festgestellt). Gilt für Mindestrente und Altansprüche."],
    ["Grundbedarf","Das steuerliche Existenzminimum ("+eu(G26)+" im Jahr 2026). Erste Stufe des Tarifs und Maß des Netzes; folgt zu 70 % den Preisen und zu 30 % den Löhnen."],
    ["Zukunftsschatz","Wahlweise: Bürgerfonds, in den ein Teil der Lenkungseinnahmen fließt; nur der Ertrag wird ausgeschüttet (Vorbild Norwegen)."],
    ["Starke Gemeinden","Die Gemeinde erhält feste Beträge je Einwohner und je Kind und entscheidet selbst über ihre Aufgaben und die Weitergabe an andere Verwaltungen. Sie zahlt Aufstockung und Härtefall vor Ort aus; Höhe und Anrechnung legt das Land fest."],
    ["Das gemeinsame Dach","Die europäische Ebene für das, was nur gemeinsam geht (Verteidigung, Binnenmarkt, digitale Souveränität); mit Obergrenze."],
    ["Altlasten","Staatsschulden und Rentenzusagen aus dem alten System. Sache der einzelnen Staaten; der Bauplan bietet Werkzeuge an."],
    ["Lenkung","Steuern, die Schädliches verteuern (CO₂-Preis, Sonderstufe 33 %, Energie- und Tabaksteuer). Ihr Aufkommen soll mit dem Erfolg sinken."]]));

const N_KURZ=inhalt.length;
// ---- 3 Regeln
const st=[1,1.5,2,3].map(x=>eu(G26*x));
add(H1("3  Die Regeln"),
  H2("3.1  Das Goldene Drittel: Einnahmen"),
  tab([{t:"Einkommen im Jahr (Kaufkraft 2026)",w:5426},{t:"Satz",w:3600,al:RT}],[
    ["bis "+st[0]+" (Grundbedarf)","0 %"],["bis "+st[1]+" (1,5-facher Grundbedarf)","11 %"],["bis "+st[2]+" (2-fach)","19 %"],["bis "+st[3]+" (3-fach)","25 %"],["darüber – Obergrenze","33 %"]]),
  P("",{sp:80}),
  L([["Einkommen: ",true],["Besteuert wird das Brutto ohne Abzüge und ohne Splitting; die Dividende zählt mit. Die Stufen hängen am Grundbedarf."]]),
  L([["Kapital: ",true],["alle Erträge einschließlich Veräußerungsgewinnen höchstens 33 %."]]),
  L([["Unternehmen und Plattformen: ",true],["33 % am Ort der Kunden."]]),
  L([["Erbschaft: ",true],["33 % über 100.000 € je Erwerb, ohne Verschonungsausnahmen, mit Stundung."]]),
  L([["Große Vermögen: ",true],["1,5 % ab 2 Mio. €, anrechenbar auf die Einkommensteuer."]]),
  L([["Boden: ",true],["Die Gemeinde erhebt 0,1 bis 1 % auf den Bodenwert, nicht auf das Gebäude."]]),
  L([["Klima: ",true],["europäischer CO₂-Preis; das Aufkommen geht über die Transformationsdividende zurück."]]),
  L([["Konsum: ",true],["Die Mehrwertsteuer wird zum Label: A+ 5 % (Grundbedarf, Reparatur), A 11 % (nachhaltige Güter), B 17 % (Standardgüter), C 25 % (ressourcenintensiv, Luxus); Sonderstufe S 33 % nur für Schädliches: Tabak, Alkohol, Kraftstoffe, Fahrzeuge mit Verbrennungsmotor. Im Mittel "+pr(V.label_effektiv,1)+" (heute in Deutschland rund 16,0 %)."]]),
  L([["Weitergabe: ",true],["Betriebe müssen mindestens 80 % der wegfallenden Arbeitgeberbeiträge in den Lohn geben. Durchsetzung (Beschluss 20.10.2026): Ein Gesetz verpflichtet, alle Arbeitsverträge bis zum Stichtag der Einführung entsprechend anzupassen – neuer Bruttolohn = bisheriger Bruttolohn + mindestens 80 % des bisherigen Arbeitgeberbeitrags. Ein unabhängiges Monitoring der Bruttolöhne je Branche begleitet die ersten Jahre. Wer die Anpassung unterlässt, führt die Differenz an den Altlastenfonds ab; das Einbehalten bringt dem Betrieb damit nichts (bei 50 % tatsächlicher Weitergabe flössen 2,4 bis 2,8 % des BIP an den Fonds, modell/weitergabe_rueckfall.py). Ohne jede Weitergabe bliebe der Vorteil in Deutschland positiv (42.000 €: "+vz(WS.varianten["0.0"].de_mehr_monat.alleinstehend["42000"])+" statt "+vz(WS.varianten["0.8"].de_mehr_monat.alleinstehend["42000"])+" im Monat), in Frankreich und Spanien nicht (modell/weitergabe_sensitivitaet.py). Über die Lohnentwicklung nach dem Stichtag entscheidet wieder der Arbeitsmarkt; die Inzidenzforschung ist dazu uneinheitlich."]]),
  tab([{t:"Aufkommen 2028 (% des BIP)",w:5426},{t:"Wert",w:3600,al:RT}],
    Object.entries(V.deckung_positionen).map(([k,v])=>[k,de(v,2)]).concat([["Summe",de(V.deckung,2)]]),{hl:{[Object.keys(V.deckung_positionen).length]:1}}),
  Q("Aufkommen auf deutscher Basis gerechnet und auf die zehn Staaten übertragen; Ausweichreaktionen nicht eingerechnet (Annahme)."),

  H2("3.2  Das starke Netz: Grundversorgung ohne Extras"),
  P("Das Netz ist geknüpft aus vielen Knoten – jeder hält mit, keiner fällt durch. Es bietet eine brauchbare Grundversorgung; was darüber geht, ist die eigene Route. So bleibt stets Raum und Anreiz für eigenes Engagement."),
  tab([{t:"Knoten",w:2100},{t:"Leistung",w:4126},{t:"Darüber: eigene Route",w:2800}],[
    ["Gesundheit","Behandlung, Arznei, Vorsorge, Notfall; Leistungskatalog ohne Extras ("+pr(NZ.beschluss.gesundheit_kuerzung*100,0)+" schlanker als heute, Annahme)","Einzelzimmer, Wahlleistungen, Komfort"],
    ["Pflege","Teilkasko wie heute in Deutschland","Zuzahlung aus eigenem Einkommen, Pflegezusatz"],
    ["Alter","Mindestrente ab 67: Aufstockung bis zum Grundbedarf, eigene Rente nur zur Hälfte angerechnet","Pflichtvorsorge 10 % und freiwillige Vorsorge"],
    ["Invalidität","Grundbedarf bei voller Erwerbsminderung","Berufsunfähigkeitsversicherung"],
    ["Arbeitslosigkeit","Grundbedarf; Hinzuverdienst zur Hälfte angerechnet","Lohnersatz privat oder tariflich (Vorbild dänische Arbeitslosenkassen)"],
    ["Hinterbliebene","Jeder Erwachsene hat eigene Dividende und Mindestrente; Waisen den Grundbedarf eines Kindes","Risikolebensversicherung"],
    ["Härtefall","H1 Wohnkosten über dem Wohnanteil bis zur örtlichen Grenze; H2 Mehrbedarf (landeseinheitlich); H3 einmalige Notlagen (Ermessen der Gemeinde)","–"]]),
  P("",{sp:80}),
  P("Eine Regel für Grundauskommen, Erwerb und Härtefall: Aufstockung = Grundauskommen + Härtefall − Dividenden − ½ × eigenes Einkommen, mindestens null. Damit lohnt jeder verdiente Euro, und der Härtefall läuft mit steigendem Einkommen von selbst aus. Die Gemeinde zahlt Aufstockung und Härtefall aus (eine Stelle vor Ort); Grundauskommen, Anrechnung und Mehrbedarfe legt das Land fest, die Gemeinde darf sie nicht unterschreiten, aber aus eigenen Mitteln ergänzen. Ermessen hat sie bei der Mietgrenze im Korridor des Landes, bei Einmalbedarfen und bei Angeboten zu Arbeit und Bildung. Das Land erstattet den Rechtsanspruch vollständig; eine mit der Bezugsdauer sinkende Erstattung wie in Dänemark wird nicht übernommen, weil sie dort nach einer Auswertung (VIVE 2020, erstes Reformjahr) schwer vermittelbare Menschen benachteiligte. Vorbilder: Dänemark und Schweden (Kommunen zahlen nach nationalen Sätzen; Wohnkosten im Einzelfall)."),
  tab([{t:"Kosten im Erwerbsalter 2028 (% des BIP)",w:2626},...["DE","FR","IT","ES","PL"].map(c=>({t:c,w:1280,al:RT}))],[
    ["Aufstockung bis zum Grundauskommen",...["DE","FR","IT","ES","PL"].map(c=>de(HF.staaten[c].band.untere.boden,2)+"–"+de(HF.staaten[c].band.obere.boden,2))],
    ["Härtefall H1–H3",...["DE","FR","IT","ES","PL"].map(c=>{const u=HF.staaten[c].band.untere,o=HF.staaten[c].band.obere;return de(u.h1+u.h2+u.h3,2)+"–"+de(o.h1+o.h2+o.h3,2);})],
    ["Budget im Netz (Härtefall, Arbeitslosigkeit, Invalidität)",...["DE","FR","IT","ES","PL"].map(c=>de(HF.staaten[c].budget_pct_bip,2))],
    ["Reserve (untere / obere Schätzung)",...["DE","FR","IT","ES","PL"].map(c=>de(HF.staaten[c].band.untere.reserve,2)+" / "+de(HF.staaten[c].band.obere.reserve,2))]]),
  Q("Schätzung aus EU-SILC-Dezilen (Eurostat ilc_di01) mit Annahmen zu Haushaltsmischung und Transfers (modell/boden_kosten.toml). H1 aus den anerkannten Wohnkosten im Bürgergeld nach Haushaltstyp (März 2025, BT-Drs. 21/1069) gegen den Wohnanteil des Grundauskommens: im Mittel "+de(HF.h1_mietdaten_de.je_aequivalent_monat,0)+" € je Äquivalenzerwachsenem und Monat (Band "+de(HF.h1_mietdaten_de.band['0.2'],0)+"–"+de(HF.h1_mietdaten_de.band['0.4'],0)+" €); andere Länder nach Grundbedarf übertragen (ohne eigene Mietdaten); H2 und H3 Annahmen (haertefall.toml). "+(()=>{const k=["DE","FR","IT","ES","PL"].filter(c=>HF.staaten[c].band.obere.reserve<0);return k.length?"In der oberen Schätzung reicht das Budget nicht in "+k.map(c=>({DE:"Deutschland",FR:"Frankreich",IT:"Italien",ES:"Spanien",PL:"Polen"})[c]+" (Erwachsenendividende rund −"+de(HF.staaten[c].band.obere.dividende_minus_monat,0)+(c==="PL"?" zł":" €")+" im Monat)").join(", ")+".":"Das Budget reicht in allen fünf Ländern.";})()),
  P("",{sp:80}),
  tab([{t:"Kosten des Netzes (% des BIP)",w:4226},{t:"2028",w:1200,al:RT},{t:"2060",w:1200,al:RT},{t:"Dauerzustand",w:1400,al:RT}],
    Object.keys(NB['2028'].positionen).map(k=>[k,de(NB['2028'].positionen[k],2),de(NB['2060'].positionen[k],2),de(NB.dauer.positionen[k],2)])
      .concat([["Starkes Netz zusammen",de(NB['2028'].netz_pct_bip,2),de(NB['2060'].netz_pct_bip,2),de(NB.dauer.netz_pct_bip,2)],
               ["Wert je Einwohner und Monat (Durchschnitt)",eu(NB['2028'].netz_eur_kopf_monat),eu(NB['2060'].netz_eur_kopf_monat),eu(NB.dauer.netz_eur_kopf_monat)]]),{hl:{7:1}}),
  Q("Dauerzustand: nach Auslauf aller Rentenansprüche aus der Zeit vor 2028. Mengen: 1,8 Mio. Erwerbsminderungsrenten Ende 2024 (DRV); Arbeitslosenquote Euroraum 6,2 % (Eurostat, Dezember 2025); Langzeitpflege 1,7 % BIP (Ageing Report 2024, maschinell gelesen). Faktor der Mindestrente aus der Einkommensverteilung des Kernmodells (10 % Pflichtvorsorge, 40 Sparjahre, 2,5 % real, 10 % mit langen Lücken: Annahmen)."),

  H2("3.3  Warum die Mindestrente mit Pflichtvorsorge"),
  tab([{t:"Variante der Grundrente",w:4626},{t:"Dividende 2060",w:2200,al:RT},{t:"Dividende Dauerzustand",w:2200,al:RT}],[
    ["Volksrente = Grundbedarf für alle ab 67 (Vorbild Niederlande)",eu(dv(vr['2060'].dividende_erw_eur2026)),eu(dv(vr.dauer.dividende_erw_eur2026))+" (nicht tragfähig)"],
    ["Volksrente 2/3 des Grundbedarfs",eu(dv(z3['2060'].dividende_erw_eur2026)),eu(dv(z3.dauer.dividende_erw_eur2026))],
    ["Mindestrente mit Pflichtvorsorge 10 % (Beschluss)",eu(dv(NB['2060'].dividende_erw_eur2026)),eu(dv(NB.dauer.dividende_erw_eur2026))]],{hl:{2:1}}),
  P("",{sp:80}),
  P("Die Mindestrente ist die einzige gerechnete Variante, die dauerhaft eine spürbare Dividende lässt. Sie verbindet Sicherheit (niemand liegt im Alter unter dem Grundbedarf) mit Eigenverantwortung (das Konto gehört dem Sparer und ist vererbbar). Die halbe Anrechnung der eigenen Rente sorgt dafür, dass sich Sparen auch bei kleinen Einkommen lohnt; sie wirkt dort aber wie eine Belastung von 50 % auf die eigene Rente."),

  H2("3.4  Die Transformationsdividende"),
  P("Jeder Erwachsene erhält jeden Monat denselben Betrag, Kinder "+pr(SK*100,0)+" davon, ohne Antrag; die Dividende ist steuerpflichtig wie jedes Einkommen. Sie ist der Rest nach Dach, Gemeinden und Netz. Rund "+pr(PR[2028].lenkung_pct_bip/V.dividende_pct_bip_2028*100,0)+" ihres Ausgangswerts stammen aus Lenkungseinnahmen; sie wird kleiner, wenn Verbrenner und Emissionen verschwinden – das ist gewollt."),
  tab([{t:"Jahr",w:2000},{t:"je Erwachsenem",w:2400,al:RT},{t:"je Kind",w:2200,al:RT},{t:"% des BIP",w:2426,al:RT}],
    ['2028','2035','2045','2060','dauer'].map(j=>[j==='dauer'?'Dauerzustand':j,eu(dv(NB[j].dividende_erw_eur2026)),eu(dv(NB[j].dividende_erw_eur2026)*SK),de(NB[j].dividende_pct_bip,2)])),
  Q("Kaufkraft 2026, Deutschland. Die Kinderdividende ("+eu(kind28)+" im Jahr 2028) liegt über dem heutigen Kindergeld (259 €). Kinderanteil 80 % (Beschluss R1, 18.10.2026): Existenzminimum eines Kindes einschließlich Betreuung, Erziehung, Ausbildung im Verhältnis zu dem eines Erwachsenen (0,79); aus demselben Topf, die Erwachsenendividende sinkt dadurch um "+pr((1-TOPF)*100,1)+"."),

  H2("3.5  Ihre eigene Route"),
  P("Alles über der Grundversorgung liegt beim Einzelnen: die Pflichtvorsorge von 10 % des Lohns auf eigenem Konto, freiwillige Vorsorge, Zusatzversicherungen für Komfort in Gesundheit und Pflege, für Lohnersatz bei Arbeitslosigkeit und für Berufsunfähigkeit. Jeder zusätzlich verdiente und gesparte Euro bleibt dem, der ihn verdient: von jedem weiteren Euro höchstens ein Drittel Steuer."),

  H2("3.6  Starke Gemeinden und das gemeinsame Dach"),
  P("Statt fünf Ebenen gibt es zwei. Die Gemeinde erhält den größten Teil des Geldes nach einer festen Formel je Einwohner und je Kind und entscheidet selbst. Das Dach behält höchstens "+pr(G.obergrenze,0)+" dessen, was es einzieht, und nur, was seine Aufgaben kosten; der Rest fließt an Gemeinden und Dividende."),
  P("Bildung, Forschung und Kultur: Für jedes Kind von 5 bis 19 Jahren erhält die Gemeinde einen festen Betrag (Deutschland "+eu(G.gemeinde_kind_de)+" im Jahr; heute rund 10.500 € je Schülerin und Schüler, Destatis 2024 über Sekundärquelle); Schulen, Betreuung und Förderung trägt sie vor Ort (in der Gesamtrechnung Schulen "+de(G.tabelle_b[0][1],2)+" % und Kultur, Sport, Gemeinschaft "+de(G.tabelle_b[3][1],2)+" % des BIP). Betreuung, Erziehung und Ausbildung erhalten die Kinder als Sachleistung der Gemeinde; deshalb zählt im Grundauskommen nur der sachliche Bedarf eines Kindes ("+de(KW,2)+" des Grundbedarfs). Grundlagenforschung und Hochschulen gehören zu den Aufgaben des Dachs ("+de(G.tabelle_a[2][1],2)+" und "+de(G.tabelle_a[3][1],2)+" % des BIP)."),

  H2("3.7  Verteilung: der Gini-Koeffizient"),
  tab([{t:"Gini (0–100)",w:2626},...["DE","FR","IT","ES","PL"].map(c=>({t:c,w:1280,al:RT}))],[
    ["heute (2025, amtlich)",...["DE","FR","IT","ES","PL"].map(c=>de(GI.staaten[c].gini_amtlich_2025,1))],
    ["Goldenes Drittel 2028",...["DE","FR","IT","ES","PL"].map(c=>de(GI.staaten[c].reihe.find(z=>z.jahr===2028).mitte,1))],
    ["Goldenes Drittel 2060",...["DE","FR","IT","ES","PL"].map(c=>de(GI.staaten[c].reihe.find(z=>z.jahr===2060).mitte,1))],
    ["2028, Rentnerhaushalte unverändert",...["DE","FR","IT","ES","PL"].map(c=>{const z=GI.staaten[c].reihe.find(z=>z.jahr===2028);return de((z.untere.gini_rentner_unveraendert+z.obere.gini_rentner_unveraendert)/2,1);})]]),
  Q("Statische Rechnung (modell/gini.py): heutige Verteilung aus EU-SILC 2025 (Dezilgrenzen, Anteile D1 und D10), Abbildung heute → neu je Äquivalenzerwachsenem mit dem Grundauskommen; ausgewiesen amtlicher Wert plus Modelländerung. Ohne Verhaltensänderung, Kapitaleinkommen und Vermögen. Zum Vergleich heute: Dänemark "+de(GI.vergleich_amtlich_2025.DK,1)+", Schweden "+de(GI.vergleich_amtlich_2025.SE,1)+". In Frankreich stieg der Gini ohne Deckel auf 32,7 (Korrektur 64, modell/gini_frankreich.py): Die Arbeitgeberbeiträge haben dort für Kranken- und Familienversicherung keine Bemessungsgrenze, hohe Löhne stiegen um 24–41 %, beim Mindestlohn fallen wegen der Beitragsentlastung (RGDU) kaum Beiträge an, und die prime d'activité entfällt. Beschluss vom 23.10.2026 (erste Ausnahme von den gleichen Regeln je Land): Die Weitergabe zählt in Frankreich nur bis zum Beitrag beim 1,6-fachen Durchschnittslohn – das Verhältnis der deutschen Bemessungsgrenze der Rentenversicherung zum deutschen Durchschnittslohn. Damit Gini 2028 "+de(GI.staaten.FR.reihe.find(z=>z.jahr===2028).mitte,1)+" gegen amtlich "+de(GI.staaten.FR.gini_amtlich_2025,1)+"; bei Abbildung über Familienhaushalte "+de(GF.staaten.FR.gini_abbildung_familie,1)+". Der Deckel ändert nichts an den Verlusten bei kleinen Löhnen (prime d'activité). Die Rechnung zählt weitergegebene Beiträge als Einkommen, obwohl damit heute Rentenansprüche nach Lohnhöhe (AGIRC-ARRCO) und Arbeitslosengeld finanziert werden; der Vorteil hoher Löhne ist deshalb als verfügbares Einkommen richtig, als Wohlfahrtsgewinn überzeichnet."),

  H2("3.8  Altlasten: Sache der Staaten"),
  P("Staatsschulden und Rentenzusagen stammen aus dem alten System. Jeder Staat regelt sie selbst; eigene Lösungen sind erwünscht. Für die Altansprüche gelten vier einfache Regeln (Beschlüsse 18. und 22.10.2026):"),
  L([["Grundbedarf garantiert, Zusagen darüber geteilt: ",true],["Gesetzliche Renten und Pensionen beruhen auf Zusagen, die nicht angespart sind. Auf den Teil über dem Grundbedarf (1.029 € je Person) werden sie um 15 % gekürzt; eigene Vorsorge (Betriebs- und Privatrenten) bleibt ungekürzt. Kranken- und Pflegebeiträge entfallen. Bei 1.500 € beträgt die Kürzung 71 €, bei 2.500 € 221 € im Monat."]]),
  L([["Anteilig: ",true],["Wer nach 2028 in Rente geht, erhält seinen Altanspruch im Verhältnis der Erwerbsjahre vor 2028; nur dieser Anteil wird mit der Dividende verrechnet. Der Übergang ist gleitend."]]),
  L([["Grundauskommen auch im Bestand: ",true],["Kein Rentnerhaushalt erhält weniger als die heutige Grundsicherung (1.083 € allein, 1.632 € zu zweit); die Bestandsrente zählt voll."]]),
  L([["Ein Rentenbeginn: ",true],["67, gekoppelt an zwei Drittel des Zuwachses der Lebenserwartung, für alte und neue Ansprüche gleich (Vorbilder Niederlande, Dänemark)."]]),
  P("Als Werkzeug bietet der Bauplan einen gemeinsamen Fonds an:"),
  tab([{t:"Altlastenfonds (30 Staaten, alle Altrenten nach Kürzung)",w:6026},{t:"Wert",w:3000,al:RT}],[
    ["Gleichbleibender Beitrag bis 2098",pr(AB.beitrag_pct_bip,2)+" des BIP"],
    ["als Zuschlag auf alle Steuern (gemeinsamer Satz, ab 2058 für alle)",pr(AB.zuschlag_auf_alle_steuern_pct,1)],
    ["Verrechnung je Staat 2028 (Beschluss 24.10.2026): Deutschland / Frankreich / Italien / Spanien / Polen",["DE","FR","IT","ES","PL"].map(c=>pr(AB.verrechnung.laender[c].reihe["2028"].zuschlag_pct,1)).join(" / ")],
    ["Schuldenquote des Fonds: Spitze",pr(AB.schuldenquote_spitze,0)+" ("+AB.spitzenjahr+")"],
    ["vollständig getilgt",String(AB.zieljahr)]]),
  Q("Zins des Fonds "+pr(FG.zins,2)+": Mittel der Renditen zehnjähriger Staatsanleihen im Euroraum 2006–2025 (Eurostat, Konvergenzkriterium); Wachstum nominal 3 % (Annahme der Gesamtrechnung). Gerechnet für die zehn Staaten des Beschlusses und auf alle 30 übertragen (modell/fonds_klub.py). Jeder Staat trägt anfangs nach seiner eigenen Altlast (Zinsen auf die Schuld und Altrenten über der Dividende 2028); der Unterschied schmilzt in 30 Jahren auf den gemeinsamen Satz ab. Die Haushaltsrechnungen nutzen den Satz des eigenen Staates. Liegt der Zins beim Wachstum, steigt der Beitrag. Mehreinnahmen über dem Fünfjahresdurchschnitt tilgen zusätzlich."));

// ---- 3.8 Neustartverfahren
const nsv=(c,sn,k)=>NS.staaten[c].varianten.find(v=>v.schnitt===sn&&v.altrenten_kuerzung===k).zuschlag_pct;
add(H2("3.8  Neustartverfahren für überschuldete Staaten"),
  P("Griechenland wurde ungeordnet saniert: 288,7 Mrd. € Hilfskredite (2010–2018), 2012 ein Schnitt von 53,5 % auf rund 197 Mrd. € privater Anleihen (Schuld rund 107 Mrd. € niedriger), danach längere Laufzeiten und Zinsaufschub der öffentlichen Gläubiger; Bürger verloren in mehreren Runden Teile ihrer Renten, Gerichte erklärten Kürzungen später für verfassungswidrig. Der Bauplan bietet dafür ein geordnetes Verfahren an:"),
  L([["Antrag und Prüfung: ",true],["Der Staat beantragt; eine unabhängige Prüfstelle des Dachs stellt fest, ob die Altlasten tragfähig sind."]]),
  L([["Stillhalten: ",true],["höchstens zwölf Monate keine Zahlungen an Altgläubiger; Netz, Gemeinden und Dividende laufen weiter."]]),
  L([["Beiträge in fester Reihenfolge: ",true],["private Gläubiger (Schnitt oder Laufzeit per Mehrheitsklausel), öffentliche Gläubiger (Laufzeit, Zins), Vermögende (befristete Abgabe nach dem Muster des Lastenausgleichs 1952), Altansprüche über der Grundversorgung (gestaffelt, kleine Renten geschützt, begründet und verhältnismäßig)."]]),
  L([["Geschützt: ",true],["Grundbedarf, starkes Netz, eigene Vorsorgekonten, Gemeindeformel."]]),
  L([["Neustart: ",true],["Der Rest geht in den Altlastenfonds mit gemeinsamem Zins; wer dauerhaft nicht mitwirkt, verliert die Zinsgarantie."]]),
  tab([{t:"Altlasten-Zuschlag (eigener Fonds bis 2098)",w:3626},{t:"ohne",w:1350,al:RT},{t:"Schnitt 33 %",w:1350,al:RT},{t:"Altrenten −10 %",w:1350,al:RT},{t:"beides",w:1350,al:RT}],
    Object.keys(NS.staaten).slice(0,4).map(c=>[NS.staaten[c].name,pr(nsv(c,0,0)),pr(nsv(c,0.33,0)),pr(nsv(c,0,0.1)),pr(nsv(c,0.33,0.1))])),
  Q("Solange der gemeinsame Zins ("+pr(FG.zins,2)+") unter dem Wachstum (3 %) liegt, schmilzt alte Schuld von selbst; der Schnitt bringt dann wenig, die Rentenzusagen wiegen schwerer. Das Verfahren sichert vor allem den Fall ab, dass der Zins über dem Wachstum liegt. Rechtlich offen: Eigentums- und Vertrauensschutz der Renten, Art. 125 AEUV. Quellen: ESM; Wissenschaftliche Dienste des Bundestags (WD 4-176/08); griechischer Staatsrat über Sekundärquellen."));

// ---- 4 Finanzierung
const jahre=[2028,2035,2045,2060];
add(H1("4  Finanzierung auf einen Blick"),
  tab([{t:"% des BIP",w:3626},...jahre.map(j=>({t:String(j),w:1350,al:RT}))],[
    ["Das Goldene Drittel (Steuern)",...jahre.map(j=>de(deck(j),1))],
    ["Gemeinsames Dach",...jahre.map(j=>de(PR[j].dach_ohne_zins,1))],
    ["Starke Gemeinden",...jahre.map(j=>de(gem(j),1))],
    ["Das starke Netz",...jahre.map(j=>de(NB[String(j)].netz_pct_bip,1))],
    ["Transformationsdividende",...jahre.map(j=>de(NB[String(j)].dividende_pct_bip,1))],
    ["Altlasten (Staaten, Fonds-Beispiel)",...jahre.map(()=>de(AB.beitrag_pct_bip,1))]],{hl:{0:1}}),
  Q("Ausgaben ohne Altlasten = Steuern abzüglich eines Überschusses von "+de(V.punkte['2028'].saldo,2)+" Punkten. Das Dach wächst bis 2035 mit dem Verteidigungspfad der Gesamtrechnung (1,4 → 2,5 % BIP)."),
  P("Warum die Steuerquote bis 2060 sinkt: Die Lenkungseinnahmen erodieren mit ihrem Erfolg ("+de(PR[2028].lenkung_pct_bip,2)+" → "+de(PR[2060].lenkung_pct_bip,2)+" % des BIP). Dagegen wirkt das Wachstum: Wer mehr verdient, rückt in höhere Stufen (+"+de(PR[2060].progression,2)+" Punkte 2060, weil der Grundbedarf nur zu 30 % den Löhnen folgt). Gesundheit und Pflege steigen mit der Alterung um "+de(PR[2060].gesundheit_plus,2)+" Punkte (Ageing Report 2024)."));

// ---- 5 Haushalte
const hhs=['alleinstehend','alleinerziehend, 1 Kind','Paar, ein Einkommen, 2 Kinder'];
add(H1("5  Was bei den Menschen ankommt"),
  P("Netto im Monat heute (Recht 2026, mit Bürgergeld) gegen das Drittel-System im Jahr 2028, Kaufkraft 2026. Neu: nach Einkommensteuer, Dividende des Haushalts (Kinder 80 %), höherer Mehrwertsteuer, Pflichtvorsorge 10 %, Weitergabe von 80 % der Arbeitgeberbeiträge, Altlastenzuschlag und Aufstockung bis zum Grundauskommen."),
  tab([{t:"Haushalt",w:2826},{t:"Brutto im Jahr",w:1500,al:RT},{t:"heute",w:1500,al:RT},{t:"neu",w:1500,al:RT},{t:"mehr im Monat",w:1700,al:RT}],
    hhs.flatMap(h=>[20000,42000,75000].map(b=>{const z=RBJ.beispiele_de[h][String(b)];return [h,de(b)+" €",eu(z.heute),eu(z.neu),vz(z.mehr)];}))),
  Q("Gerechnet mit modell/regel_boden.py (heute mit Bürgergeld; Wohngeld und Kinderzuschlag nicht berücksichtigt). Weitere Erwachsene ohne eigenes Einkommen."),
  L([["Kleine Löhne: ",true],["Bei halbem Vollzeit-Mindestlohn bleiben von einem zusätzlich verdienten Euro heute "+pr(100-RBJ.staaten.DE.lohnabstand.alleinstehend.belastung_zusatzeuro_bei_halbem_mindestlohn.heute,0)+", neu "+pr(100-RBJ.staaten.DE.lohnabstand.alleinstehend.belastung_zusatzeuro_bei_halbem_mindestlohn.neu,0)+" (alleinstehend)."]]),
  L([["Rentner: ",true],["Eine Rente von 1.200 € wird auf den Teil über dem Grundbedarf um 15 % gekürzt; Kranken- und Pflegebeiträge entfallen. Mit der höheren Mehrwertsteuer bleiben "+vz(rent(1200,0).differenz_monat+dRent)+" im Monat (mit Zuschlag "+vz(rent(1200,ZU).differenz_monat+dRent)+"). Gesundheit und Pflege bleiben ohne Prämie."]]),
  L([["Anreiz: ",true],["Von einem zusätzlichen Euro Arbeitskosten kommen bei 55.000 € brutto heute "+pr(100-RA.grenz_heute[gi],0)+" beim Haushalt an, neu "+pr(100-RA.grenz_neu['0.8'][gi],0)+"."]]),
  L([["Woher das Mehr kommt: ",true],["aus dem Wegfall der Sozialbeiträge, der breiteren Belastung von Kapital, Gewinnen und Erbschaften und der schlanken Grundversorgung – und zu einem Teil aus der Streckung der Altlasten über den Fonds bis 2098."]]));

// ---- 6 Zeitpfad, Trends, Automatisierung, Einwanderung
const d0=dyn0.dividende_erw_eur2026;
add(H1("6  Bis 2060: Trends, Automatisierung, Einwanderung"),
  H2("6.1  Belegte Trends"),
  L("Verkehr: Neuwagen 2025 zu 17,4 % elektrisch (ACEA); EU-Recht sieht ab 2035 keine CO₂-Emissionen neuer Pkw vor (Lockerung auf 90 % vorgeschlagen). Verkehrsemissionen in Deutschland bis 2040 auf rund ein Drittel (Projektionsbericht 2026)."),
  L("Alterung: öffentliche Ausgaben für Gesundheit +0,4 und Pflege +0,8 Punkte des BIP 2022–2070 (EU27, Ageing Report 2024)."),
  L("Heute: Sozialbeiträge in Deutschland 2035 voraussichtlich 48,6 % (IGES für DAK, eine Studie)."),
  H2("6.2  Automatisierung und Arbeit"),
  P("Im heutigen System kostet eine Verschiebung von Einkommen von der Arbeit zum Kapital Aufkommen, weil Arbeit stärker belastet ist. Im Drittel-System trägt jeder Euro sein Drittel; Automatisierung schwächt die Finanzierung nicht. Szenarien (Änderung der Dividende 2060 gegen den Grundpfad):"),
  tab([{t:"Szenario",w:6026},{t:"Dividende 2060",w:3000,al:RT}],[
    ["KI, untere Schätzung (+0,07 Pp Produktivität je Jahr; Acemoglu 2024)",vz(dv(dyn(0,0.07,0).dividende_erw_eur2026-d0))],
    ["KI, obere Schätzung (+0,6 Pp; OECD 2024)",vz(dv(dyn(0,0.6,0).dividende_erw_eur2026-d0))],
    ["Mehr Arbeit durch billigere Arbeit (+4,6 % Arbeitsvolumen)",vz(dv(dyn(4.6,0,0).dividende_erw_eur2026-d0))],
    ["Alles zusammen mit Verschiebung zum Kapital (KI 0,3 bis 0,6)",vz(dv(dyn(4.6,0.3,3).dividende_erw_eur2026-d0))+" bis "+vz(dv(dyn(4.6,0.6,3).dividende_erw_eur2026-d0))]]),
  Q("Wachstum kommt vor allem als Lohn und Gewinn bei den Menschen an; die Dividende ist ein kleiner Rest des BIP und wächst nur im selben Verhältnis."),
  H2("6.3  Kontrollierte Einwanderung"),
  tab([{t:"2060",w:3626},{t:"ohne",w:1500,al:RT},{t:"+0,5 Mio./Jahr",w:1950,al:RT},{t:"+1 Mio./Jahr",w:1950,al:RT}],[
    ["Menschen über 65 je Person im Erwerbsalter",de(ew(0.2,'kontrolliert').reihe['2060'].altenquotient_basis,2),de(ew(0.2,'kontrolliert').reihe['2060'].altenquotient,2),de(ew(0.4,'kontrolliert').reihe['2060'].altenquotient,2)],
    ["BIP je Einwohner (gut / schwierig integriert)","–",pr(ew(0.2,'kontrolliert').reihe['2060'].bip_je_kopf_pct)+" / "+pr(ew(0.2,'schwierig').reihe['2060'].bip_je_kopf_pct),pr(ew(0.4,'kontrolliert').reihe['2060'].bip_je_kopf_pct)+" / "+pr(ew(0.4,'schwierig').reihe['2060'].bip_je_kopf_pct)],
    ["Beitrag Altlastenfonds, zehn Staaten (% BIP)",de(AL.beschluss.beitrag_pct_bip,2),de(ew(0.2,'kontrolliert').fonds_beitrag_pct_bip,2),de(ew(0.4,'kontrolliert').fonds_beitrag_pct_bip,2)]]),
  Q("Einwanderung im Erwerbsalter mildert die Alterung und verdünnt die festen Altlasten; sie gleicht die Alterung nicht aus. Eingewanderte erwerben im neuen System keine Ansprüche über der Grundversorgung. Annahmen: Erwerbstätigkeit und Produktivität der Eingewanderten, Altenquotient interpoliert."));

// ---- 6.4 Möglichkeitsraum
const ml=Object.values(MR.laender).sort((a,b)=>b.einwohner_mio-a.einwohner_mio);
add(H2("6.4  Der Möglichkeitsraum: 30 Staaten"),
  P("Der Bauplan ist für jeden Staat gerechnet, für den Eurostat vergleichbare Daten führt (27 EU-Staaten, Norwegen, Island, Schweiz; "+de(MR.raum.einwohner_mio,1)+" Mio. Menschen). Vereinigtes Königreich und Kanada fehlen mangels harmonisierter Daten. Das Aufkommen des Goldenen Drittels folgt der eigenen Steuerbasis jedes Staates: Einkommen dem Arbeitnehmerentgelt, Kapital und Unternehmen dem Betriebsüberschuss, Konsum dem privaten Verbrauch (je im Verhältnis zu Deutschland). Das Netz folgt den Landesdaten, der Grundbedarf dem Preisniveau; die Dividende ist in deutscher Kaufkraft angegeben."),
  tab([{t:"Staat",w:1626},{t:"Abgaben heute",w:1050,al:RT},{t:"Steuern neu",w:1050,al:RT},{t:"Netz 2028",w:950,al:RT},{t:"Dividende 2028",w:1150,al:RT},{t:"Dividende Dauer",w:1150,al:RT},{t:"Altlasten-Zuschlag",w:1100,al:RT},{t:"Last neu",w:950,al:RT}],
    ml.map(e=>[e.name,pr(e.abgabenquote_heute),pr(e.z2028.deckung_pct_bip),pr(e.z2028.netz_pct_bip),eu(dv(e.z2028.dividende_erw_kaufkraft_de)),e.dauer.dividende_erw_kaufkraft_de<0?"Lücke "+eu(-e.dauer.dividende_erw_kaufkraft_de):eu(e.dauer.dividende_erw_kaufkraft_de),pr(e.altlasten.zuschlag_pct),pr(e.gesamtlast_2028)])
      .concat([["Alle 30",pr(MR.raum.abgabenquote_heute),pr(MR.raum.deckung_pct_bip_2028),pr(MR.raum.netz_pct_bip_2028),eu(dv(MR.raum.dividende_erw_kaufkraft_de_2028)),eu(dv(MR.raum.dividende_erw_kaufkraft_de_dauer)),pr(MR.raum.zuschlag_pct),"–"]]),{hl:{[ml.length]:1}}),
  P("",{sp:80}),
  P("Über Europa hinaus: Die Regeln sind nicht an Europa gebunden; sie passen überall dort, wo die Wertebasis übereinstimmt – Rechtsstaat, Demokratie, soziale Marktwirtschaft, Selbstverwaltung der Gemeinden. Wegen des vorliegenden Datenbestands und Modellstands ist das noch nicht weiter bearbeitet."),
  P("Wo die Dividende im Dauerzustand gegen null geht oder eine Lücke bleibt (Schweden, Dänemark, Tschechien, Frankreich), tragen die eigenen Steuern das Netz nur knapp: hohe Ausgaben für Gesundheit, Invalidität oder Arbeitslosigkeit treffen auf eine schmalere Steuerbasis. Diese Staaten brauchen eine eigene Lösung – etwa die Bodenwertabgabe bis 2 %, eine schlankere Grundversorgung oder einen Zukunftsschatz aus den Lenkungseinnahmen der Übergangszeit."),
  Q("Abgaben heute: Steuern und Sozialbeiträge 2024 (Eurostat). Last neu: Goldenes Drittel plus eigener Altlastenfonds bis 2098, ohne Pflichtvorsorge (eigenes Konto). Staaten mit niedriger Abgabenquote heute (Irland, Schweiz, Rumänien, Bulgarien, Malta) hätten eine höhere Last als heute, Staaten mit hoher eine niedrigere. Irland: BIP durch Konzerngewinne überzeichnet. Schweiz: obligatorische Krankenversicherung als Annahme eingerechnet. Altrenten auf die ungedeckten staatlichen Ansprüche der Eurostat-Tabelle 29 (2021) begrenzt, ohne Altersprofil je Staat. Schulden Norwegen, Island, Schweiz: Annahme."));

// ---- 7 Vorbilder
add(H1("7  Vorbilder"),
  tab([{t:"Staat",w:1800},{t:"Was übernommen wird",w:7226}],[
    ["Dänemark","Sozialstaat aus Steuern (Sozialbeiträge 0,7 % des BIP); freiwillige Arbeitslosenkassen für Lohnersatz; starke Kommunen, die die Mindestsicherung nach gesetzlichen Sätzen auszahlen"],
    ["Schweden","Kommunen zahlen die Sozialhilfe nach einer landesweiten Norm; Wohnkosten nach dem Einzelfall (Vorbild Härtefall H1)"],
    ["Estland","einfache, digitale Einkommensteuer; Grundsteuer allein auf den Bodenwert seit 1993"],
    ["Schweiz","CO₂-Abgabe gleichmäßig an alle zurück; Grundversicherung mit Kostenbeteiligung, Komfort privat; Gemeinden setzen ihre Steuern selbst"],
    ["Niederlande","Volksrente (AOW) als Vergleich; als Dauerlösung zu teuer"],
    ["Australien","Pflichtvorsorge auf eigenem Konto (12 % seit 1.7.2025) und bedarfsgeprüfte Grundrente"],
    ["Alaska, Norwegen","Dividende für alle (seit 1982); Staatsfonds, der nur den Ertrag ausschüttet (Vorbild Zukunftsschatz)"]]));

// ---- 8 Grenzen
add(H1("8  Was noch offen ist"),
  L("Weitergabe: Gesetz zur Vertragsanpassung bis zum Stichtag beschlossen, dazu Monitoring der Bruttolöhne je Branche und Rückfallregel (Differenz an den Altlastenfonds). Offen: Nachweis im Einzelfall und neue Verträge nach dem Stichtag."),
  L("Mikrosimulation (externe Rechnung, eine Quelle): Der Kulturverein Ribbeck e.V. hat 60.000 Vollzeitbeschäftigte in einer synthetischen, auf die Verdiensterhebung 2024 geeichten Bevölkerung gerechnet. Ergebnis: 99,0 % haben mehr verfügbares Einkommen, bei halber Weitergabe 98,4 %, ohne jede Weitergabe 92,0 %; im obersten Lohndezil ohne Weitergabe 47 %. Grenzen: nur Vollzeit, heute ohne bedarfsgeprüfte Leistungen und neu ohne Grundauskommen, Zuschlag 15,8 % (Stand v4.18) (beitraege/kvribbeck-2028)."),
  L("Eigene synthetische Mikrosimulation (Prüfrechnung, v4.22 bis v4.26): 37 Mio. Haushalte, geeicht auf Beschäftigte nach Vollzeit, Teilzeit und Minijob, Haushaltstypen, Kinder und Bürgergeld; Bruttolohnsumme und Lohnsteuer 2025 ohne Eichung um 3 bzw. 5 % getroffen. Ergebnis bei 80 % Weitergabe: Haushalte mit Vollzeit-Hauptverdiener 99 %, mit Teilzeit 100 %, alle Haushalte erwerbsfähigen Alters 89 %; Bürgergeldhaushalte ohne Erwerb 15 % (im Mittel −45 € im Monat), Rentnerhaushalte nach der Regel vom 22.10.2026 30 % (im Mittel −129 € im Monat; allein −106 €, Paare −153 €; Haushaltseinkommen aus EU-SILC 2025, Einkommensarten nach dem Alterssicherungsbericht 2024). Beamte (20 % der Beihilfe-Ersparnis weitergegeben, Beschluss 23.10.2026) 56 %, Selbständige 77 %. Über alle Haushalte einschließlich Rentner haben 69 % mehr, 77 % der Personen. Grenzen: gleiche Zusammensetzung der Alterseinkommen über alle Einkommen (Annahme), Bezüge und Krankenversicherung der Beamten und Einkommen der Selbständigen als Annahmen bzw. aus einem Online-Panel (modell/mikro_de.py, modell/mikro_rentner_de.py)."),
  L("Preise: Der höhere Mehrwertsteuersatz hebt die Verbraucherpreise einmalig um "+pr(PN.reihe[0].mwst_spanne_pct[0],1)+" bis "+pr(PN.reihe[0].mwst_spanne_pct[1],1)+" (Überwälzung 73 bis 100 %, Anteil des Konsums mit Mehrwertsteuer "+de(PN.anteil_konsum_mit_mwst[0]*100)+" bis "+de(PN.anteil_konsum_mit_mwst[1]*100)+" %). Geben die Betriebe die Senkung ihrer Arbeitskosten zur Hälfte weiter, bleiben netto "+pr(PN.netto_2028_pct['0.5'][0],1)+" bis "+pr(PN.netto_2028_pct['0.5'][1],1)+". Das ist eine Niveauverschiebung, keine dauerhafte Inflation; Zweitrundeneffekte sind nicht gerechnet (modell/preisniveau33.py). Die Haushaltsrechnungen setzen die volle Differenz auf den gesamten Konsum an."),
  L("Architektur: Variante „Regelwerk statt Dach“ (Staaten ziehen ein, Ausgleichsstelle zahlt nach Formel; projekt/Variante-Regelwerk-statt-Dach-2026-10-20.md) zur Entscheidung."),
  L("Rentner: Regel beschlossen (22.10.2026): Grundbedarf garantiert auf dem Niveau der heutigen Grundsicherung, Zusagen über dem Grundbedarf um 15 % gekürzt, eigene Vorsorge ungekürzt; dazu anteilige Verrechnung und gekoppelter Rentenbeginn. Rentnerhaushalte nach Fünfteln des heutigen Nettos (Mikrosimulation mit Haushaltseinkommen): "+RK.varianten.at(-1).fuenftel_monat.map(x=>vz(x)).join(" / ")+" im Monat, im Mittel "+vz(RK.varianten.at(-1).mittel_monat)+" (bisherige Regel 7,5 %: "+vz(RK.varianten[0].mittel_monat)+"). Eigentumsschutz der Anwartschaften (Art. 14 GG) juristisch prüfen."),
  L("Familien: Kindergewicht im Grundauskommen "+de(KW,2)+" (Vorschlag zur Freigabe; geprüft 0,3 bis 0,8, modell/kindergewicht.py). Bei 0,7–0,8 reicht das Netzbudget in Frankreich, Italien und Polen in der oberen Schätzung nicht."),
  L("Härtefall: Kosten mit Mietdaten nach Haushaltstyp nachrechnen; Pflichten und Zugangsbedingungen (Aktivität, Aufenthaltsdauer) sind nicht geregelt."),
  L("Deckel der Weitergabe (Beschluss E2, einheitliche Regel): In allen Staaten werden die Arbeitgeberbeiträge nur bis zum Lohn beim Sechsfachen des Grundbedarfs weitergegeben (Deutschland 74.088 €, nahe der Bemessungsgrenze der Krankenversicherung); der Rest bleibt beim Betrieb (E10). Ohne Deckel stieg die Ungleichheit in Frankreich nach dem Modell um gut 2 Punkte (Korrektur 64); mit Deckel liegt der Gini 2028 beim amtlichen Wert."),
  L("Grundversorgung: Kürzung des Gesundheitskatalogs (5 %), Mengen bei Invalidität und Arbeitslosigkeit und die Verteilung der eigenen Renten sind Annahmen ohne Mikrodaten."),
  L("Dividende: Sie sinkt bis 2060; ein Zukunftsschatz könnte einen Teil auf Dauer sichern."),
  L("Altlasten: Der Fonds verschiebt Lasten in die Zukunft (Schuldenspitze "+pr(AB.schuldenquote_spitze,0)+"); jeder Staat entscheidet. Gerechnet ist mit "+pr(FG.zins,2)+" Zins (Mittel 2006–2025); die Marktzinsen lagen im Oktober 2026 darüber (Bundesanleihen rund "+pr(FZ.markt_oktober_2026.bund_10j,1)+", EU-Anleihen rund "+pr(FZ.markt_oktober_2026.eu_10j,1)+", Sekundärquellen). Mit 3,5 bzw. 4 % stiege der Zuschlag auf "+pr(FZ.varianten[2].zuschlag_pct,1)+" bzw. "+pr(FZ.varianten[3].zuschlag_pct,1)+", der Vorteil bei 42.000 € brutto sänke von "+eu(FZ.varianten[0].haushalt_de.mehr_monat_42000.alleinstehend)+" auf "+eu(FZ.varianten[3].haushalt_de.mehr_monat_42000.alleinstehend)+" im Monat (modell/fondszins.py). Der Fonds umfasst alle 30 Staaten; mit nur den zehn des ersten Beschlusses läge der Satz bei "+pr(FK.klubs[0].zuschlag_skaliert_pct,1)+", mit den zehn und Italien bei "+pr(FK.klubs[1].zuschlag_skaliert_pct,1)+" (modell/fonds_klub.py)."),
  L("Deckung auf deutscher Basis; Trends als Setzungen aus Quellen, keine eigene Prognose. Ausweichreaktionen: Gehen bei der Erbschaft die Hälfte und bei großen Vermögen drei Viertel verloren (statt der Hälfte), fehlen "+de(-AW.faelle[AW.faelle.length-1].delta_pct_bip,2).replace('.',',')+" % des BIP; die Dividende sinkt 2028 um "+de(-AW.faelle[AW.faelle.length-1].dividende_2028_eur)+" € und 2060 um "+de(-AW.faelle[AW.faelle.length-1].dividende_2060_eur)+" € je Erwachsenem (modell/ausweichen33.py)."),
  L("Korrektur 61: Frühere Fassungen (v3.47, v3.48) hielten den Anteil der Einkommensteuer fest und unterschätzten die Dividende 2060."));

// ---- 9 Quellen
add(H1("9  Quellen"),
  ...[
   "Europäische Kommission (2024): 2024 Ageing Report, Institutional Paper 279 (Gesundheit, Pflege, Wachstum).",
   "Rat der EU (2024): ST 9160/24, Schlussfolgerungen zum Ageing Report.",
   "Umweltbundesamt (2026): Projektionsbericht 2026 für Deutschland; Indikator Umweltbezogene Steuern.",
   "VO (EU) 2019/631 i. d. F. VO (EU) 2023/851; Rat der EU ST 10065/1/26 (Flottengrenzwerte).",
   "ACEA (27.1.2026): New car registrations 2025.",
   "Rat der EU (9.10.2026): ETS2, Marktstabilitätsreserve.",
   "Bundesministerium für Gesundheit (2025): Finanzentwicklung der GKV, 1.–4. Quartal 2024.",
   "Deutsche Rentenversicherung über sozialpolitik-aktuell.de: Renten wegen verminderter Erwerbsfähigkeit 2024.",
   "Destatis über Deutsches Ärzteblatt (28.3.2025): Grundsicherung im Alter 2024.",
   "Eurostat (2026): Arbeitslosenquote Euroraum Dezember 2025; COFOG gov_10a_exp; Rentenansprüche nasa_10_pens1.",
   "OECD (2025): Taxing Wages 2025.",
   "IGES für DAK-Gesundheit (2024), berichtet im Deutschen Ärzteblatt (25.6.2024): Sozialbeiträge 2035.",
   "Acemoglu, D. (2024): The Simple Macroeconomics of AI, NBER Working Paper 32487.",
   "Filippucci, F.; Gal, P.; Schief, M. (2024): Miracle or Myth? OECD Artificial Intelligence Papers 29.",
   "CaixaBank Research (2024): Levers to mitigate the impact of demographics on public finances (Sekundärquelle zum Ageing Report).",
   "ESM: Greece exit factsheet (2018); What was private sector debt restructuring in March 2012.",
   "Wissenschaftliche Dienste des Deutschen Bundestages: WD 4-176/08 (Lastenausgleich).",
   "Sachverständigenrat (2015): Sondergutachten Maastricht 2.0, Pressemitteilung.",
   "To Vima (11.6.2015); European Pensions (15.7.2020): Urteile des griechischen Staatsrats (Sekundärquellen).",
   "Eurostat (2026): ilc_di01, ilc_di12 (EU-SILC 2025: Einkommensverteilung, Gini).",
   "borger.dk: Kontanthjælp, Sätze 2026; STAR: Reform L 13 (2024); VIVE (2020): Refusionstrappen.",
   "Socialstyrelsen: Riksnormen för försörjningsstöd 2026; Meddelandeblad 4/2026; Prop. 2025/26:201.",
   "Statistisches Bundesamt (2026), berichtet von Münster Aktuell (12.3.2026): Ausgaben je Schülerin und Schüler 2024 (Sekundärquelle)."
  ].map(t=>L(t)),
  Q("Bewertung der einzelnen Angaben (amtlich, Sekundärquelle, Annahme): seite/entwurf/QUELLEN-33.md und Logbuch Band III, v3.47 bis v3.51."));

const doc=new Document({
  creator:"Initiative 28:28", title:"Das Goldene Drittel – "+(KURZ?"Kurzfassung":"Konzept")+" (Fassung 4.39)",
  styles:{default:{document:{run:{font:F,size:21}}},
    paragraphStyles:[{id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:28,bold:true,font:F,color:"1F3864"},paragraph:{spacing:{before:340,after:140},outlineLevel:0}},
                     {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:23,bold:true,font:F,color:"1F3864"},paragraph:{spacing:{before:220,after:120},outlineLevel:1}}]},
  numbering:{config:[{reference:"punkte",levels:[{level:0,format:LevelFormat.BULLET,text:"–",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:440,hanging:260}}}},
                                                 {level:1,format:LevelFormat.BULLET,text:"·",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:880,hanging:260}}}}]}]},
  features:{updateFields:true},
  sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1300,bottom:1300,left:1440,right:1440}}},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:"Das Goldene Drittel · Fassung 4.39 · Seite ",size:16,font:F,color:"808080"}),new TextRun({children:[PageNumber.CURRENT],size:16,font:F,color:"808080"})]})]})},
    children:KURZ?inhalt.slice(0,N_KURZ):inhalt}]});
const ziel=path.join(WURZEL,'dokumente','entwurf',KURZ?'TAX-Drittel-Kurzfassung.docx':'TAX-Drittel-Konzept.docx');
fs.mkdirSync(path.dirname(ziel),{recursive:true});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(ziel,b);console.log('geschrieben:',path.relative(WURZEL,ziel),b.length,'Bytes');});
