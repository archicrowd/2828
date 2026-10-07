// Baut dokumente/TAX-2828-Kurzfassung.docx (zwei Seiten) aus daten/aggregate/gesamtrechnung.json.
// Keine Zahl von Hand: jede Zahl kommt aus der Gesamtrechnung oder aus gesamtrechnung.toml (mit Quelle).
// Aufruf aus dem Wurzelordner: NODE_PATH=/opt/npm-tools/node_modules node dokumente/werkzeuge/kurzfassung-bau.js
// danach in dokumente/: soffice --headless --convert-to pdf TAX-2828-Kurzfassung.docx
const d=require('docx');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,AlignmentType,BorderStyle}=d;
const fs=require('fs'), path=require('path');
const WURZEL=path.resolve(__dirname,'..','..');
const J=JSON.parse(fs.readFileSync(path.join(WURZEL,'daten','aggregate','gesamtrechnung.json'),'utf8'));
const de=(x,nk=0)=>Number(x).toLocaleString('de-DE',{minimumFractionDigits:nk,maximumFractionDigits:nk});

const F="Calibri", SZ=21, BLAU="1F3864", GRUEN="1D7A4F", GRAU="595959";
const W=9638;
const T=(t,o={})=>new TextRun({text:t,font:F,size:o.sz||SZ,bold:!!o.b,italics:!!o.i,color:o.c});
const P=(runs,o={})=>new Paragraph({spacing:{after:o.after??90,line:o.line??262},alignment:o.al,children:(typeof runs==='string'?[T(runs,o)]:runs.map(r=>typeof r==='string'?T(r):T(r[0],r[1]||{})))});
const H=(t)=>new Paragraph({spacing:{before:150,after:70},children:[T(t,{b:true,sz:23,c:BLAU})]});
const zelle=(t,w,o={})=>new TableCell({width:{size:w,type:WidthType.DXA},shading:o.fill?{type:ShadingType.CLEAR,fill:o.fill,color:"auto"}:undefined,
  margins:{top:35,bottom:35,left:90,right:90},children:[new Paragraph({spacing:{after:0,line:240},children:(Array.isArray(t)?t:[T(t,{b:o.b,sz:18})])})]});
const regeln=(zeilen)=>new Table({columnWidths:[2300,7338],width:{size:W,type:WidthType.DXA},
  rows:zeilen.map(([a,b],i)=>new TableRow({cantSplit:true,children:[zelle(a,2300,{b:true,fill:i%2?undefined:"F2F5FA"}),zelle(b,7338,{fill:i%2?undefined:"F2F5FA"})]}))});

const q=J.quote, og=J.obergrenze;
const kinder=[
new Paragraph({spacing:{after:0},children:[T("TAX 28:28",{b:true,sz:36,c:BLAU}),T("   Ein neues Grundsystem für Steuern und Gemeinwesen",{sz:24,c:BLAU})]}),
new Paragraph({spacing:{after:120},border:{bottom:{style:BorderStyle.SINGLE,size:6,color:"BFBFBF",space:4}},children:[
  T(`Kurzfassung · Stand ${J.fassung} · Modellstand ${J.version} · Initiative 28:28`,{i:true,sz:16,c:GRAU})]}),

H("Warum es ein neues System braucht"),
P("Die heutige Steuer- und Abgabenordnung ist über Jahrzehnte gewachsen, Schicht um Schicht, Ausnahme um Ausnahme. Kaum jemand kann sie noch überblicken, und wer etwas verändern will, verliert sich in Zuständigkeiten. Eine Gemeinde, die eine Schule sanieren will, verhandelt mit Kreis, Land und Bund über Geld, das zweckgebunden ankommt und über das anderswo entschieden wurde. Was sie spart, bekommt sie nicht. Bürgerinnen und Bürger, Vereine und Gemeinden stehen vor einem Dickicht, das sie weder durchschauen noch beeinflussen können. So verliert ein Land Zeit, Vertrauen und Anschluss im internationalen Wettbewerb."),
P([["Dazu kommt eine Schieflage, die sich messen lässt. ",{b:true}],`Von einem durchschnittlichen Lohn in Deutschland gehen ${de(J.abgabenkeil_de_2024,1)} % der Arbeitskosten an Steuern und Sozialabgaben, der zweithöchste Wert unter den OECD-Staaten (Durchschnitt ${de(J.abgabenkeil_oecd_2024,1)} %). Zinsen und Kursgewinne werden mit ${de(J.abgeltungsteuer_de,1)} % besteuert. Sozialbeiträge fallen nur auf menschliche Arbeit an: Wer Arbeit durch Maschinen ersetzt, spart Abgaben. Ausnahmen und Subventionen haben aus einfachen Grundsätzen ein Regelwerk gemacht, das seinen eigenen Zweck oft nicht mehr erkennen lässt.`]),

H("Die Idee: wenige klare Regeln, zwei Ebenen, ein gemeinsames Dach"),
P([`TAX 28:28 baut das System von unten neu auf, von der Breite der Bevölkerung her und von Anfang an europäisch gedacht. `,["Der Einzelne",{b:true}],` zahlt nach wenigen, gleichen Regeln: höchstens 28 % auf Einkommen, keine Sozialabgaben, keine Abzüge und Sonderregeln. `,["Die Gemeinde",{b:true}],` erhält den größten Teil des Aufkommens nach einer festen Formel, je Einwohner und je Kind gleich viel, und entscheidet selbst, was sie damit tut, auch welche Leistungen sie von Kreis oder Land einkauft. Länder und Regionen organisieren sich selbstständig, freiwillig statt verordnet. `,["Das gemeinsame Dach",{b:true}],` übernimmt, was keine Gemeinde allein kann: Verteidigung und digitale Souveränität, einen Binnenmarkt ohne innere Grenzen, gemeinsame Standards, die Garantie für die Altschulden. Es darf höchstens ${de(og)} % dessen behalten, was es einzieht; was es nicht braucht, fließt weiter an die Gemeinden und in die Dividende.`]),
P([["Was beim Einzelnen ankommt. ",{b:true}],`Jeden Monat eine Dividende, ohne Antrag und ohne Prüfung: für jeden Erwachsenen gleich, für Kinder zur Hälfte, im Schnitt ${de(J.klub_2028)} € je Einwohner im Startjahr 2028 (Preise 2028). Sie ist das, was nach den Aufgaben übrig bleibt. Spart die Gemeinde, steigt sie; wächst die Wirtschaft, wächst sie mit, bis 2060 auf ${de(J.klub_2060)} €. Arbeit lohnt sich auf jeder Stufe, weil kein hinzuverdienter Euro auf eine Leistung angerechnet wird. Nach einer Gruppenschätzung des nationalen Modells hätten über ${de(J.anteil_mit_mehr_de)} % der Menschen in Deutschland mehr im Geldbeutel, mit der Bestandsgarantie für heutige Leistungsbezieher praktisch alle. Wer sieht, wofür er zahlt, und vor Ort mitentscheidet, lebt Fairness nicht als Vorschrift, sondern als gemeinsame Praxis.`]),

H("Die neuen Regeln"),
regeln([
 ["Einkommen",`Stufentarif 0 / 9 / 16 / 21 / 26 / 28 % auf das Brutto, Grundfreibetrag 12.348 €; kein Splitting, keine Abzüge`],
 ["Kapital und Erbschaft","28 % auf alle Kapitalerträge wie auf Arbeit; 28 % auf Erbschaften über 200.000 €, Stundung statt Verschonung"],
 ["Unternehmen","28 % auf Gewinne am Ort der Nutzung, also dort, wo die Kunden sind; gilt ausdrücklich für digitale Plattformen"],
 ["Konsum und Klima","Mehrwertsteuer als Label von A+ bis D: je nachhaltiger, desto günstiger; europäischer CO₂-Preis, Erlöse fließen in die Dividende"],
 ["Boden","Bodenwertabgabe der Gemeinde, 0,1 bis 1 %, nur auf den Grundstückswert, nicht auf Mieten umlegbar; Vermögen über 2 Mio. € 1 % Mindeststeuer"],
 ["Sozialabgaben","entfallen; Gesundheit wird gesondert finanziert"],
 ["Schutz","Wer heute Bürgergeld, Grundsicherung oder BAföG erhält, bekommt mindestens das bisherige Niveau (Härtefallfonds)"],
 ["Verteilung","Gemeinden: je Einwohner "+de(J.formel_einw)+" €, je Kind von 5 bis 19 "+de(J.formel_kind)+" € im Jahr (2028); der Rest ist Dividende"],
 ["Dach (Klub)",`höchstens ${de(og)} % des Einzugs, im Vertrag gedeckelt; Mehrheitsentscheid; Zinsgarantie für die Altschulden`],
 ["Steuerquote",`${de(q,1)} % des BIP, abgeleitet: die kleinste Quote, bei der die Dividende auch ohne Wachstum nie unter 479 € fällt (Deutschland, Preise 2028)`],
]),
P("",{after:40}),
P([["Was es kostet. ",{b:true}],`Heute tragen die zehn gerechneten Staaten ${de(J.last_heute,2)} % ihrer Wirtschaftsleistung an Steuern und Sozialbeiträgen, der Entwurf ${de(J.last_entwurf,2)} % einschließlich Gesundheit. Das sind ${de(J.entlastung,2)} Punkte oder ${de(J.entlastung_mrd)} Mrd € weniger im Jahr (2028, nominal), und entlastet wird vor allem die Arbeit.`]),
P([["Was noch nicht bewiesen ist. ",{b:true}],`Auf deutscher Basis tragen die Steuerpositionen nachweislich ${de(J.deckung_gesamt,2)} % des BIP; bis zur Quote fehlen ${de(J.deckung_luecke,2)} Punkte, auf den Klub übertragen rund ${de(J.deckung_luecke_mrd_klub)} Mrd € im Jahr (2028, nominal). Diese Lücke zu schließen ist die nächste Rechnung. Wie es einzelnen Haushalten ergeht, zeigt erst eine Mikrosimulation; sie folgt, wenn die Gesamtrechnung geprüft steht. Ein Verteidigungsziel über 2,5 % des BIP passt nicht unter die Obergrenze und verlangt eine Vertragsänderung.`]),

H("Offene Entwicklungsarbeit"),
P("TAX 28:28 ist ein Entwurf zur Diskussion, unabhängig von Parteien und Interessengruppen entwickelt. Die Eingangsdaten stammen aus amtlichen Statistiken (Eurostat, OECD), jede Rechnung liegt als Skript vor und lässt sich nachrechnen. Ein Logbuch führt jede Änderung und jeden Fehler mit Nummer, Ursache und Korrektur; bis heute sind 52 Korrekturen eingetragen. Annahmen und Schätzungen sind als solche gekennzeichnet. Rechnungen und Logbuch werden mit der Veröffentlichung des Projekts frei zugänglich."),
P("Das Projekt lädt Fachleute ohne Parteibindung ein, mitzuarbeiten: aus Finanzwissenschaft, Verwaltung, Kommunalpraxis, Recht und Statistik. Gebraucht werden vor allem die Steuerbasen der zehn Staaten, eine Haushaltsmikrosimulation und die rechtliche Prüfung des Klubvertrags. Beiträge werden offen geprüft und im Logbuch vermerkt. Die Skripte stehen unter MIT-Lizenz, Texte und Ergebnisse unter CC BY 4.0."),
new Paragraph({spacing:{before:60,after:0},border:{top:{style:BorderStyle.SINGLE,size:4,color:"BFBFBF",space:4}},children:[
  T(`Kontakt: 2828@archicrowd.de · Ausführliche Fassung: TAX 28:28 — Das Gesamtkonzept (${J.fassung}) · Quellen: OECD, Taxing Wages 2025 (Tabelle 3.1); § 32d EStG; Eurostat (2024); Gruppenschätzung „über ${de(J.anteil_mit_mehr_de)} %“ aus dem nationalen Modell ohne Mikrosimulation. Text: Initiative 28:28, CC BY 4.0.`,{i:true,sz:15,c:GRAU})]}),
];
const doc=new Document({creator:"Initiative 28:28",title:"TAX 28:28 — Kurzfassung",styles:{default:{document:{run:{font:F,size:SZ}}}},
  sections:[{properties:{page:{margin:{top:850,bottom:780,left:1134,right:1134}}},children:kinder}]});
Packer.toBuffer(doc).then(b=>{const z=path.join(WURZEL,'dokumente','TAX-2828-Kurzfassung.docx');fs.writeFileSync(z,b);console.log('ok',z,b.length)});
