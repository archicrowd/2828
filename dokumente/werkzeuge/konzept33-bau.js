// Baut dokumente/entwurf/TAX-Drittel-Konzept.docx: das Konzept des Drittel-Systems mit den Beschlüssen bis v3.51 und den neuen Begriffen
// (Goldenes Drittel, starkes Netz, Transformationsdividende, eigene Route, Zukunftsschatz). Entwurf zur Prüfung; die Gesamtrechnung (28:28) und das
// veröffentlichte Gesamtkonzept bleiben unberührt. Jede Zahl kommt aus daten/aggregate/*.json (Prüfrechnungen modell/*33.py, altlasten.py).
// Aufruf aus dem Repository-Wurzelordner: NODE_PATH=/opt/npm-tools/node_modules node dokumente/werkzeuge/konzept33-bau.js
const d=require('docx');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,Table,TableRow,TableCell,WidthType,ShadingType,AlignmentType,BorderStyle,PageBreak,
       Footer,PageNumber,LevelFormat,TableOfContents}=d;
const fs=require('fs'); const path=require('path');
const WURZEL=path.resolve(__dirname,'..','..');
const lies=n=>JSON.parse(fs.readFileSync(path.join(WURZEL,'daten','aggregate',n),'utf8'));
const SV=lies('systemvarianten.json'), PJ=lies('projektion33.json'), NZ=lies('netz33.json'), H=lies('haushalte33.json'), RA=lies('haushalte33_raster.json'),
      AL=lies('altlasten.json'), EW=lies('einwanderung33.json'), DY=lies('dynamik33.json'), G=lies('gesamtrechnung.json');
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
const AB=AL.beschluss;
const fall=(hh,zu,j=2028)=>H.faelle.find(f=>f.jahr===j&&f.haushalt===hh&&f.weitergabe_ag===0.8&&f.vorsorge_satz===0.1&&f.zuschlag_pct===zu);
const ZU=Math.max(...H.faelle.map(f=>f.zuschlag_pct));
const zl=(f,b)=>f.zeilen.find(z=>z.brutto===b);
const gi=RA.grenz_brutto.indexOf(55000);
const rent=(r,zu)=>H.rentner.find(x=>x.rente_monat===r&&x.zuschlag_pct===zu);
const dyn=(b,ki,kv)=>DY.szenarien.find(x=>x.beschaeftigung_pct===b&&x.ki_pp===ki&&x.kapital_verschiebung_pp===kv).reihe['2060'];
const dyn0=dyn(0,0,0);
const ew=(m,a)=>EW.szenarien.find(s=>s.zusatz_pct===m&&s.integration===a);
const G26=12348, f26=1.0404;
const kind28=NB['2028'].dividende_erw_eur2026/2;

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
  P("Initiative 28:28 · Entwurf zur Prüfung · Modellstand "+NZ.version+" · 17. Oktober 2026",{sz:22}),
  P("Alle Zahlen stammen aus offenen Prüfrechnungen (Repository, Ordner modell/ und daten/aggregate/). Beträge in Euro sind, wenn nicht anders angegeben, Euro je Monat in Kaufkraft 2026 für Deutschland als Referenzland; Anteile sind Prozent der Wirtschaftsleistung (BIP) im Durchschnitt der zehn gerechneten Staaten.",{i:true,sz:19,sp:200}),
  P("Lizenz: Text und Ergebnisse CC BY 4.0, Skripte MIT.",{sz:18}),
  BR(),
  new TableOfContents("Inhalt",{hyperlink:true,headingStyleRange:"1-2"}),BR());

// ---- 1 Kurzfassung
add(H1("1  Kurzfassung"),
  kasten("Der Bauplan in vier Sätzen",[
    "Du zahlst höchstens das Goldene Drittel: 33 % auf jeden Euro, ob aus Arbeit, Kapital, Gewinn oder Erbe – keine Sozialbeiträge, keine Prämien.",
    "Das starke Netz trägt Dich: eine brauchbare Grundversorgung ohne Extras – geknüpft aus vielen Knoten, jeder hält mit, keiner fällt durch.",
    "Die Transformationsdividende kommt jeden Monat aufs Konto: Sie gibt zurück, was der Wandel einbringt, und wird kleiner, wenn das Schädliche verschwindet.",
    "Alles darüber ist Deine eigene Route: eigene Vorsorge auf Deinem Konto, Zusatzversicherungen, eigener Einsatz."]),
  P("",{sp:120}),
  tab([{t:"Kennzahl",w:5426},{t:"Wert",w:3600,al:RT}],[
    ["Höchstsatz auf jedes Einkommen","33 %"],
    ["Sozialbeiträge, Prämien","0 €"],
    ["Pflichtvorsorge auf eigenem Konto",pr(NZ.beschluss.pflicht_satz*100,0)+" des Lohns"],
    ["Mehrwertsteuer (Label) im Mittel",pr(V.label_effektiv,1)],
    ["Steuern insgesamt (Goldenes Drittel), 2028",pr(V.deckung,1)+" des BIP"],
    ["Starkes Netz, 2028",pr(NB['2028'].netz_pct_bip,1)+" des BIP"],
    ["Transformationsdividende je Erwachsenem, 2028 / 2060",eu(NB['2028'].dividende_erw_eur2026)+" / "+eu(NB['2060'].dividende_erw_eur2026)],
    ["Alleinstehend, 42.000 € brutto, mit Altlastenzuschlag: mehr im Monat",vz(zl(fall('alleinstehend',ZU),42000).differenz_monat)],
    ["Grenzbelastung bei 55.000 € brutto: heute / neu",pr(RA.grenz_heute[gi],0)+" / "+pr(RA.grenz_neu['0.8'][gi],0)]]),
  P("",{sp:120}),
  P("Was das System leistet, liegt nicht in einer großen Geldzahlung, sondern in drei Dingen: Arbeit wird nicht mehr doppelt belastet, jeder ist ohne Prämie grundversorgt, und was jemand darüber hinaus verdient und spart, gehört ihm. Der Bauplan nimmt aus vielen erprobten Vorbildern die besten Teile; jeder Staat kann ihn übernehmen."));

// ---- 2 Begriffe
add(H1("2  Begriffe"),
  P("Die Begriffe sind Vorschläge der Initiative (17. Oktober 2026); markenrechtlich nicht geprüft."),
  tab([{t:"Begriff",w:2300},{t:"Bedeutung",w:6726}],[
    ["Das Goldene Drittel","Die Einnahmeregel: Kein Euro wird mit mehr als einem Drittel besteuert – Einkommen, Kapitalerträge, Unternehmensgewinne, Erbschaften. Umfasst alle Steuern des Systems."],
    ["Das starke Netz","Die Grundversorgung ohne Prämie: Gesundheit, Pflege als Teilkasko, Mindestrente, Grundbedarf bei Invalidität und Arbeitslosigkeit, Waisen, Härtefall. Keine Extras."],
    ["Transformationsdividende","Monatliche Zahlung an jeden Erwachsenen (Kinder die Hälfte), ohne Antrag. Sie ist der Rest nach allen Aufgaben und gibt vor allem zurück, was Lenkungssteuern einbringen."],
    ["Deine eigene Route","Alles über der Grundversorgung: Pflichtvorsorge auf eigenem, vererbbarem Konto, freiwillige Vorsorge, Zusatzversicherungen (Komfort, Lohnersatz, Berufsunfähigkeit)."],
    ["Pflichtvorsorge","10 % des Bruttolohns auf ein eigenes Konto. Kein Beitrag an den Staat: Das Geld gehört dem Sparer."],
    ["Mindestrente","Aufstockung ab 67 bis zum Grundbedarf, die eigene Rente wird nur zur Hälfte angerechnet."],
    ["Grundbedarf","Das steuerliche Existenzminimum ("+eu(G26)+" im Jahr 2026). Erste Stufe des Tarifs und Maß des Netzes; folgt zu 70 % den Preisen und zu 30 % den Löhnen."],
    ["Zukunftsschatz","Wahlweise: Bürgerfonds, in den ein Teil der Lenkungseinnahmen fließt; nur der Ertrag wird ausgeschüttet (Vorbild Norwegen)."],
    ["Starke Gemeinden","Die Gemeinde erhält feste Beträge je Einwohner und je Kind und entscheidet selbst über ihre Aufgaben und die Weitergabe an andere Verwaltungen."],
    ["Das gemeinsame Dach","Die europäische Ebene für das, was nur gemeinsam geht (Verteidigung, Binnenmarkt, digitale Souveränität); mit Obergrenze."],
    ["Altlasten","Staatsschulden und Rentenzusagen aus dem alten System. Sache der einzelnen Staaten; der Bauplan bietet Werkzeuge an."],
    ["Lenkung","Steuern, die Schädliches verteuern (CO₂-Preis, Sonderstufe 33 %, Energie- und Tabaksteuer). Ihr Aufkommen soll mit dem Erfolg sinken."]]));

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
  L([["Weitergabe: ",true],["Betriebe müssen mindestens 80 % der wegfallenden Arbeitgeberbeiträge in den Lohn geben."]]),
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
    ["Härtefall","Wohnkosten über dem Grundbedarf, besondere Lagen, Eingliederung","–"]]),
  P("",{sp:80}),
  tab([{t:"Kosten des Netzes (% des BIP)",w:4226},{t:"2028",w:1200,al:RT},{t:"2060",w:1200,al:RT},{t:"Dauerzustand",w:1400,al:RT}],
    Object.keys(NB['2028'].positionen).map(k=>[k,de(NB['2028'].positionen[k],2),de(NB['2060'].positionen[k],2),de(NB.dauer.positionen[k],2)])
      .concat([["Starkes Netz zusammen",de(NB['2028'].netz_pct_bip,2),de(NB['2060'].netz_pct_bip,2),de(NB.dauer.netz_pct_bip,2)],
               ["Wert je Einwohner und Monat (Durchschnitt)",eu(NB['2028'].netz_eur_kopf_monat),eu(NB['2060'].netz_eur_kopf_monat),eu(NB.dauer.netz_eur_kopf_monat)]]),{hl:{7:1}}),
  Q("Dauerzustand: nach Auslauf aller Rentenansprüche aus der Zeit vor 2028. Mengen: 1,8 Mio. Erwerbsminderungsrenten Ende 2024 (DRV); Arbeitslosenquote Euroraum 6,2 % (Eurostat, Dezember 2025); Langzeitpflege 1,7 % BIP (Ageing Report 2024, maschinell gelesen). Faktor der Mindestrente aus der Einkommensverteilung des Kernmodells (10 % Pflichtvorsorge, 40 Sparjahre, 2,5 % real, 10 % mit langen Lücken: Annahmen)."),

  H2("3.3  Warum die Mindestrente mit Pflichtvorsorge"),
  tab([{t:"Variante der Grundrente",w:4626},{t:"Dividende 2060",w:2200,al:RT},{t:"Dividende Dauerzustand",w:2200,al:RT}],[
    ["Volksrente = Grundbedarf für alle ab 67 (Vorbild Niederlande)",eu(vr['2060'].dividende_erw_eur2026),eu(vr.dauer.dividende_erw_eur2026)+" (nicht tragfähig)"],
    ["Volksrente 2/3 des Grundbedarfs",eu(z3['2060'].dividende_erw_eur2026),eu(z3.dauer.dividende_erw_eur2026)],
    ["Mindestrente mit Pflichtvorsorge 10 % (Beschluss)",eu(NB['2060'].dividende_erw_eur2026),eu(NB.dauer.dividende_erw_eur2026)]],{hl:{2:1}}),
  P("",{sp:80}),
  P("Die Mindestrente ist die einzige gerechnete Variante, die dauerhaft eine spürbare Dividende lässt. Sie verbindet Sicherheit (niemand liegt im Alter unter dem Grundbedarf) mit Eigenverantwortung (das Konto gehört dem Sparer und ist vererbbar). Die halbe Anrechnung der eigenen Rente sorgt dafür, dass sich Sparen auch bei kleinen Einkommen lohnt; sie wirkt dort aber wie eine Belastung von 50 % auf die eigene Rente."),

  H2("3.4  Die Transformationsdividende"),
  P("Jeder Erwachsene erhält jeden Monat denselben Betrag, Kinder die Hälfte, ohne Antrag; die Dividende ist steuerpflichtig wie jedes Einkommen. Sie ist der Rest nach Dach, Gemeinden und Netz. Rund "+pr(PR[2028].lenkung_pct_bip/V.dividende_pct_bip_2028*100,0)+" ihres Ausgangswerts stammen aus Lenkungseinnahmen; sie wird kleiner, wenn Verbrenner und Emissionen verschwinden – das ist gewollt."),
  tab([{t:"Jahr",w:2000},{t:"je Erwachsenem",w:2400,al:RT},{t:"je Kind",w:2200,al:RT},{t:"% des BIP",w:2426,al:RT}],
    ['2028','2035','2045','2060','dauer'].map(j=>[j==='dauer'?'Dauerzustand':j,eu(NB[j].dividende_erw_eur2026),eu(NB[j].dividende_erw_eur2026/2),de(NB[j].dividende_pct_bip,2)])),
  Q("Kaufkraft 2026, Deutschland. Die Kinderdividende ("+eu(kind28)+" im Jahr 2028) liegt unter dem heutigen Kindergeld (259 €)."),

  H2("3.5  Deine eigene Route"),
  P("Alles über der Grundversorgung liegt beim Einzelnen: die Pflichtvorsorge von 10 % des Lohns auf eigenem Konto, freiwillige Vorsorge, Zusatzversicherungen für Komfort in Gesundheit und Pflege, für Lohnersatz bei Arbeitslosigkeit und für Berufsunfähigkeit. Jeder zusätzlich verdiente und gesparte Euro bleibt dem, der ihn verdient: von jedem weiteren Euro höchstens ein Drittel Steuer."),

  H2("3.6  Starke Gemeinden und das gemeinsame Dach"),
  P("Statt fünf Ebenen gibt es zwei. Die Gemeinde erhält den größten Teil des Geldes nach einer festen Formel je Einwohner und je Kind und entscheidet selbst. Das Dach behält höchstens "+pr(G.obergrenze,0)+" dessen, was es einzieht, und nur, was seine Aufgaben kosten; der Rest fließt an Gemeinden und Dividende."),

  H2("3.7  Altlasten: Sache der Staaten"),
  P("Staatsschulden und Rentenzusagen stammen aus dem alten System. Jeder Staat regelt sie selbst; eigene Lösungen sind erwünscht. Beschlossen ist: Bestehende Renten werden um die Sozialbeiträge gekürzt, die im neuen System entfallen (Annahme für die Rechnung: 12,35 % wie in Deutschland; je Staat verschieden). Als Werkzeug bietet der Bauplan einen gemeinsamen Fonds an:"),
  tab([{t:"Altlastenfonds (zehn Staaten, alle Altrenten nach Kürzung)",w:6026},{t:"Wert",w:3000,al:RT}],[
    ["Gleichbleibender Beitrag bis 2098",pr(AB.beitrag_pct_bip,2)+" des BIP"],
    ["als Zuschlag auf alle Steuern",pr(AB.zuschlag_auf_alle_steuern_pct,1)],
    ["Schuldenquote des Fonds: Spitze",pr(AB.schuldenquote_spitze,0)+" ("+AB.spitzenjahr+")"],
    ["vollständig getilgt",String(AB.zieljahr)]]),
  Q("Zins des Fonds 2,5 %, Wachstum nominal 3 % (Annahmen der Gesamtrechnung). Liegt der Zins beim Wachstum, steigt der Beitrag. Mehreinnahmen über dem Fünfjahresdurchschnitt tilgen zusätzlich."));

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
  P("Netto im Monat heute (Recht 2026) gegen das Drittel-System im Jahr 2028, Kaufkraft 2026. Neu: nach Einkommensteuer, Dividende des Haushalts, höherer Mehrwertsteuer, Pflichtvorsorge 10 % und Weitergabe von 80 % der Arbeitgeberbeiträge. Hauptfall mit dem Altlastenzuschlag von "+pr(ZU,1)+"."),
  tab([{t:"Haushalt",w:2826},{t:"Brutto im Jahr",w:1500,al:RT},{t:"heute",w:1500,al:RT},{t:"neu",w:1500,al:RT},{t:"mehr im Monat",w:1700,al:RT}],
    hhs.flatMap(h=>[20000,42000,75000].map(b=>{const z=zl(fall(h,ZU),b);return [h,de(b)+" €",eu(z.netto_heute/12),eu(z.netto_33/12),vz(z.differenz_monat)];}))),
  Q("Ohne Altlastenzuschlag (der Staat finanziert die Altlasten anders) sind es zum Beispiel "+vz(zl(fall('alleinstehend',0),42000).differenz_monat)+" bei 42.000 € (alleinstehend). Gerechnet mit dem Kernmodell; Bürgergeld und Wohngeld nicht berücksichtigt."),
  L([["Rentner: ",true],["Eine Rente von 1.200 € wird um die entfallenden Kranken- und Pflegebeiträge gekürzt; mit der höheren Mehrwertsteuer bleiben "+vz(rent(1200,0).differenz_monat)+" im Monat (mit Zuschlag "+vz(rent(1200,ZU).differenz_monat)+"). Das ist ein kleines Minus; Gesundheit und Pflege bleiben ohne Prämie."]]),
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
    ["KI, untere Schätzung (+0,07 Pp Produktivität je Jahr; Acemoglu 2024)",vz(dyn(0,0.07,0).dividende_erw_eur2026-d0)],
    ["KI, obere Schätzung (+0,6 Pp; OECD 2024)",vz(dyn(0,0.6,0).dividende_erw_eur2026-d0)],
    ["Mehr Arbeit durch billigere Arbeit (+4,6 % Arbeitsvolumen)",vz(dyn(4.6,0,0).dividende_erw_eur2026-d0)],
    ["Alles zusammen mit Verschiebung zum Kapital (KI 0,3 bis 0,6)",vz(dyn(4.6,0.3,3).dividende_erw_eur2026-d0)+" bis "+vz(dyn(4.6,0.6,3).dividende_erw_eur2026-d0)]]),
  Q("Wachstum kommt vor allem als Lohn und Gewinn bei den Menschen an; die Dividende ist ein kleiner Rest des BIP und wächst nur im selben Verhältnis."),
  H2("6.3  Kontrollierte Einwanderung"),
  tab([{t:"2060",w:3626},{t:"ohne",w:1500,al:RT},{t:"+0,5 Mio./Jahr",w:1950,al:RT},{t:"+1 Mio./Jahr",w:1950,al:RT}],[
    ["Menschen über 65 je Person im Erwerbsalter",de(ew(0.2,'kontrolliert').reihe['2060'].altenquotient_basis,2),de(ew(0.2,'kontrolliert').reihe['2060'].altenquotient,2),de(ew(0.4,'kontrolliert').reihe['2060'].altenquotient,2)],
    ["BIP je Einwohner (gut / schwierig integriert)","–",pr(ew(0.2,'kontrolliert').reihe['2060'].bip_je_kopf_pct)+" / "+pr(ew(0.2,'schwierig').reihe['2060'].bip_je_kopf_pct),pr(ew(0.4,'kontrolliert').reihe['2060'].bip_je_kopf_pct)+" / "+pr(ew(0.4,'schwierig').reihe['2060'].bip_je_kopf_pct)],
    ["Beitrag Altlastenfonds (% BIP)",de(AB.beitrag_pct_bip,2),de(ew(0.2,'kontrolliert').fonds_beitrag_pct_bip,2),de(ew(0.4,'kontrolliert').fonds_beitrag_pct_bip,2)]]),
  Q("Einwanderung im Erwerbsalter mildert die Alterung und verdünnt die festen Altlasten; sie gleicht die Alterung nicht aus. Eingewanderte erwerben im neuen System keine Ansprüche über der Grundversorgung. Annahmen: Erwerbstätigkeit und Produktivität der Eingewanderten, Altenquotient interpoliert."));

// ---- 7 Vorbilder
add(H1("7  Vorbilder"),
  tab([{t:"Staat",w:1800},{t:"Was übernommen wird",w:7226}],[
    ["Dänemark","Sozialstaat aus Steuern (Sozialbeiträge 0,7 % des BIP); freiwillige Arbeitslosenkassen für Lohnersatz; starke Kommunen"],
    ["Estland","einfache, digitale Einkommensteuer; Grundsteuer allein auf den Bodenwert seit 1993"],
    ["Neuseeland","Mehrwertsteuer mit breiter Basis und wenigen Ausnahmen"],
    ["Schweiz","CO₂-Abgabe gleichmäßig an alle zurück; Grundversicherung mit Kostenbeteiligung, Komfort privat; Gemeinden setzen ihre Steuern selbst"],
    ["Niederlande","Volksrente (AOW) als Vergleich; als Dauerlösung zu teuer"],
    ["Australien","Pflichtvorsorge auf eigenem Konto (12 % seit 1.7.2025) und bedarfsgeprüfte Grundrente"],
    ["Alaska, Norwegen","Dividende für alle (seit 1982); Staatsfonds, der nur den Ertrag ausschüttet (Vorbild Zukunftsschatz)"]]));

// ---- 8 Grenzen
add(H1("8  Was noch offen ist"),
  L("Weitergabe: Wie sich die Pflicht, 80 % der Arbeitgeberbeiträge in den Lohn zu geben, durchsetzen lässt."),
  L("Rentner: kleines Minus durch Kürzung und Mehrwertsteuer; Ausgleich (höherer Freibetrag für Renten) zu prüfen."),
  L("Familien: Die Kinderdividende liegt unter dem heutigen Kindergeld."),
  L("Grundversorgung: Kürzung des Gesundheitskatalogs (5 %), Mengen bei Invalidität und Arbeitslosigkeit und die Verteilung der eigenen Renten sind Annahmen ohne Mikrodaten."),
  L("Dividende: Sie sinkt bis 2060; ein Zukunftsschatz könnte einen Teil auf Dauer sichern."),
  L("Altlasten: Der Fonds verschiebt Lasten in die Zukunft (Schuldenspitze "+pr(AB.schuldenquote_spitze,0)+"); jeder Staat entscheidet."),
  L("Deckung auf deutscher Basis; keine Ausweichreaktionen; Trends als Setzungen aus Quellen, keine eigene Prognose."),
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
   "CaixaBank Research (2024): Levers to mitigate the impact of demographics on public finances (Sekundärquelle zum Ageing Report)."
  ].map(t=>L(t)),
  Q("Bewertung der einzelnen Angaben (amtlich, Sekundärquelle, Annahme): seite/entwurf/QUELLEN-33.md und Logbuch Band III, v3.47 bis v3.51."));

const doc=new Document({
  creator:"Initiative 28:28", title:"Das Goldene Drittel – Konzept (Entwurf)",
  styles:{default:{document:{run:{font:F,size:21}}},
    paragraphStyles:[{id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:28,bold:true,font:F,color:"1F3864"},paragraph:{spacing:{before:340,after:140},outlineLevel:0}},
                     {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:23,bold:true,font:F,color:"1F3864"},paragraph:{spacing:{before:220,after:120},outlineLevel:1}}]},
  numbering:{config:[{reference:"punkte",levels:[{level:0,format:LevelFormat.BULLET,text:"–",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:440,hanging:260}}}},
                                                 {level:1,format:LevelFormat.BULLET,text:"·",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:880,hanging:260}}}}]}]},
  features:{updateFields:true},
  sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1300,bottom:1300,left:1440,right:1440}}},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:"Das Goldene Drittel · Entwurf "+NZ.version+" · Seite ",size:16,font:F,color:"808080"}),new TextRun({children:[PageNumber.CURRENT],size:16,font:F,color:"808080"})]})]})},
    children:inhalt}]});
const ziel=path.join(WURZEL,'dokumente','entwurf','TAX-Drittel-Konzept.docx');
fs.mkdirSync(path.dirname(ziel),{recursive:true});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(ziel,b);console.log('geschrieben:',path.relative(WURZEL,ziel),b.length,'Bytes');});
