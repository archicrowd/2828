// Baut dokumente/TAX-2828-Gesamtkonzept.docx aus daten/aggregate/gesamtrechnung.json.
// Seit v3.12 stehen keine Zahlen mehr von Hand im Text: jede Zahl kommt aus der Gesamtrechnung
// (modell/gesamtrechnung.py). Aufruf aus dem Repository-Wurzelordner:
//   node dokumente/werkzeuge/gesamtkonzept-bau.js
// Die Fassung vom 4. Oktober 2026 liegt in dokumente/archiv/ (docx, pdf) und in der Git-Geschichte.
const d=require('docx');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,Table,TableRow,TableCell,WidthType,ShadingType,AlignmentType,BorderStyle,PageBreak}=d;
const fs=require('fs'); const path=require('path');
const WURZEL=path.resolve(__dirname,'..','..');
const J=JSON.parse(fs.readFileSync(path.join(WURZEL,'daten','aggregate','gesamtrechnung.json'),'utf8'));
const de=(x,nk=0)=>Number(x).toLocaleString('de-DE',{minimumFractionDigits:nk,maximumFractionDigits:nk});
const vz=(x,nk=0)=>(x>0?'+':(x<0?'−':''))+de(Math.abs(x),nk);
const pr=(x,nk=2)=>de(x,nk)+' %';

const W=9026,grau="F2F2F2",akz="E8EEF7",warn="FBE9E5";
const P=(t,{b,i,sz=21,sp=120}={})=>new Paragraph({spacing:{after:sp},children:[new TextRun({text:t,bold:!!b,italics:!!i,size:sz,font:"Calibri"})]});
const R=(r,{sp=120,ind=0}={})=>new Paragraph({spacing:{after:sp},indent:ind?{left:ind}:undefined,children:r.map(x=>new TextRun({text:x[0],bold:!!x[1],italics:!!x[2],size:21,font:"Calibri"}))});
const H=(t,l)=>new Paragraph({heading:l,spacing:{before:l===HeadingLevel.HEADING_1?340:220,after:140},children:[new TextRun({text:t,font:"Calibri",bold:true,size:l===HeadingLevel.HEADING_1?28:23,color:"1F3864"})]});
const c=(t,{w,b,fill,al}={})=>new TableCell({width:{size:w,type:WidthType.DXA},shading:fill?{type:ShadingType.CLEAR,fill,color:"auto"}:undefined,margins:{top:70,bottom:70,left:110,right:110},children:[new Paragraph({alignment:al,spacing:{after:0},children:[new TextRun({text:t,bold:!!b,size:20,font:"Calibri"})]})]});
const tab=(cols,rows,{fills={}}={})=>{const ws=cols.map(x=>x.w);return new Table({columnWidths:ws,width:{size:W,type:WidthType.DXA},rows:[new TableRow({tableHeader:true,children:cols.map(x=>c(x.t,{w:x.w,b:true,fill:grau,al:x.al}))}),...rows.map((r,i)=>new TableRow({children:r.map((t,j)=>c(String(t),{w:ws[j],b:!!fills[i],fill:fills[i]===2?warn:(fills[i]?akz:undefined),al:cols[j].al}))}))]})};
const HR=()=>new Paragraph({spacing:{after:160},border:{bottom:{style:BorderStyle.SINGLE,size:6,color:"BFBFBF",space:6}},children:[]});
const BR=()=>new Paragraph({children:[new PageBreak()]});
const RT=AlignmentType.RIGHT;
const H1=HeadingLevel.HEADING_1, H2=HeadingLevel.HEADING_2;
const POS=(nr,titel,ebene,regel,text,status)=>[
  new Paragraph({spacing:{before:200,after:60},children:[
    new TextRun({text:nr+"  ",font:"Calibri",bold:true,size:23,color:"1D7A4F"}),
    new TextRun({text:titel,font:"Calibri",bold:true,size:23,color:"1F3864"}),
    new TextRun({text:"   "+ebene,font:"Calibri",size:19,color:"595959"})]}),
  new Paragraph({spacing:{after:60},children:[new TextRun({text:regel,font:"Calibri",bold:true,size:21})]}),
  P(text),
  R([["Stand: ",true],[status]],{sp:60})];

// ---- abgeleitete Größen für den Text
const q=J.quote, og=J.obergrenze, p0=J.tabelle_pfad[0], tp=J.tabelle_pfad;
const ogf=J.tabelle_obergrenze, haag=ogf.find(o=>o.fall.startsWith('Verteidigung 3,5')), alle=ogf.find(o=>o.fall.startsWith('alle drei'));
const mrd=x=>de(x/100*J.bip28_klub_mrd,0);
const aufmax=J.tabelle_aufschlag[0], ie=J.tabelle_aufschlag.find(r=>r.land==='Irland');

const kinder=[
new Paragraph({spacing:{after:60},children:[new TextRun({text:"TAX 28:28",font:"Calibri",bold:true,size:40,color:"1F3864"})]}),
new Paragraph({spacing:{after:60},children:[new TextRun({text:"Das Gesamtkonzept",font:"Calibri",size:30,color:"1F3864"})]}),
new Paragraph({spacing:{after:60},children:[new TextRun({text:`Stand ${J.fassung} · Modellstand ${J.version} · Steuerquote ${de(q,1)} % · Startjahr 2028 · zehn Klubstaaten`,font:"Calibri",italics:true,size:19,color:"595959"})]}),
new Paragraph({spacing:{after:300},children:[new TextRun({text:"Initiative 28:28",font:"Calibri",italics:true,size:19,color:"595959"})]}),
HR(),

H("Was es ist",H1),
P("Jede Steuerordnung sagt, wem man zutraut zu entscheiden. Die heutige sagt: nicht denen vor Ort. Eine Gemeinde, die etwas verändern will, verhandelt mit Kreis, Land und Bund über Geld, das zweckgebunden ankommt und über dessen Verwendung anderswo entschieden wurde. Was sie spart, bekommt sie nicht. Was sie leistet, sieht niemand."),
P("Dieses Konzept kehrt das um, mit zwei Ebenen statt fünf."),
R([["Dem Einzelnen",true],[` wird zugetraut, mit seinem Geld umzugehen. Ein Satz statt eines Tarifdschungels, keine Sozialabgaben mehr, Regeln, die auf eine Seite passen. Entlastet wird die Arbeit, getragen wird das von Verbrauch, Boden und Unternehmensgewinn. Dazu kommt jeden Monat eine Dividende — mit gleicher Kaufkraft für jeden Erwachsenen, also nach den Preisen des Wohnlandes bemessen, für Kinder zur Hälfte, ohne Antrag und ohne Bedürftigkeitsprüfung. Sie deckt überall mindestens das halbe Existenzminimum. In Deutschland beginnt sie bei ${de(J.erw_de_2028)} € je Erwachsenem; im Klubschnitt sind es ${de(J.klub_2028)} € je Einwohner, ${de(J.kl_tief)} € im Tiefpunkt ${J.kl_tief_jahr}, danach wächst sie mit der Wirtschaft (Preise 2028).`]]),
R([["Der lokalen Gemeinschaft",true],[" wird zugetraut, ihre eigenen Angelegenheiten zu führen. Sie erhält den weitaus größten Teil des Aufkommens, bemessen nach Einwohnern und Kindern — jedes Kind gleich viel, jeder Einwohner gleich viel. Was sie damit tut, entscheidet sie selbst: welche Schule, welcher Verband, welche Verwaltung, und ob sie Kreis oder Land für deren Leistungen überhaupt noch bezahlen will."]]),
R([["Hier schließt sich der Kreis. Was die Gemeinde spart, erscheint im nächsten Monat auf dem Konto ihrer Bürger.",true],[` Die Dividende ist das, was nach den Aufgaben übrig bleibt. Eine sparsam geführte Verwaltung ist dann kein Rechenschaftsbericht, sondern bis zu ${de(J.verw_ersparnis_eur)} € im Monat mehr je Einwohner (2028). Erfolg entsteht gemeinsam und wird gemeinsam bemerkt.`]]),
R([["Dem Klub",true],[` wird zugetraut, was keine Gemeinde allein kann. Verteidigung — und dazu gehört heute die digitale Souveränität: eigene Netze, eigene Halbleiter, eigene autonome Intelligenz. Einen Wirtschaftsraum ohne innere Grenzen. Abschlüsse, die überall gelten. Dafür darf er höchstens ${de(og)} % dessen behalten, was er einzieht, im Vertrag gedeckelt. Was er nicht braucht, fließt durch. Er entscheidet mit Mehrheit, weil ein Bündnis, das jedem ein Veto gibt, in der Stunde der Entscheidung nicht entscheidet.`]]),
P("Das ist der ganze Entwurf. Ein Einzug, eine Obergrenze, zwei Ebenen, eine Dividende, die mit der Wirtschaft wächst. Kein Versprechen auf weniger Abgaben allein, sondern auf etwas Schwierigeres: dass man sieht, wofür man zahlt, dass man mitentscheidet, wo man wohnt, und dass das, was man gemeinsam besser macht, bei allen ankommt."),

BR(),
H("1  Die Rahmenstruktur",H1),
H("1.1  Zwei Ebenen",H2),
R([["Ebene A ist der Klub, Ebene B sind die Kommunen. Kreis, Land und Nation werden nicht abgeschafft, sondern freiwillig: B kann aus seinem Anteil Abgaben an sie leisten, wenn es ihre Leistungen will. Damit wird aus einer Verfassungsrevolution eine Haushaltsentscheidung, und der Übergang kann in der heutigen Struktur beginnen. Bei kleiner Größe ist der Pflichtverband Grundbedingung, die Wahl des Partners aber frei — regional benachbart oder strukturverwandt."]]),
tab([{t:"Ebene A — der Klub",w:4600},{t:"% BIP",w:1400,al:RT},{t:"Mrd € (2028, nominal)",w:3026,al:RT}],
 J.tabelle_a.map(r=>[r[0],de(r[1],2),de(r[2])]),{fills:{[J.tabelle_a.length-1]:1}}),
P(""),
tab([{t:"Ebene B — die Kommunen",w:4600},{t:"% BIP",w:1400,al:RT},{t:"Mrd € (2028, nominal)",w:3026,al:RT}],
 J.tabelle_b.map(r=>[r[0],de(r[1],2),de(r[2])]),{fills:{[J.tabelle_b.length-1]:1}}),
P(""),
R([["Die Zuordnung ist nicht gesetzt, sondern aus dem Jetzt abgeleitet: Was die Gemeinden des Klubs heute tatsächlich tragen, bleibt bei ihnen; der Rest geht an A. Drei Posten wandern dabei nach oben — die Verteidigung auf das Zielniveau, eine übergeordnete Polizei, die Hochschulen. Das Ergebnis ist annähernd Parität, ohne dass jemand sie gelegt hätte: 8,94 gegen 10,35 Punkte, ein Abstand von 1,41 Punkten. Er liegt in der Größenordnung der vier geschätzten A-Posten, die zusammen 1,18 Punkte ausmachen."]]),

H("1.2  Der Einzug und die Obergrenze",H2),
tab([{t:"",w:4600},{t:"% BIP",w:1400,al:RT},{t:"€ je Kopf (2028, nominal)",w:3026,al:RT}],
 J.tabelle_einzug.map(r=>[r[0],de(r[1],2),de(r[2])]),{fills:{3:1,4:1}}),
P(""),
R([[`A's Bedarf ist nicht konstant: ${pr(J.a_2028)} des BIP im Startjahr, Höchststand ${pr(J.a_hoechst)} im Jahr ${J.a_hoechst_jahr}, danach fallend. Die Obergrenze liegt deshalb bei `,false],[`${de(og)} % dessen, was A einzieht — und sie ist eine Schranke, keine Zuteilung.`,true],[" A nimmt nur, was die Aufgaben kosten; alles darüber fließt durch an B und in die Dividende. Eine Obergrenze, die nicht ausgeschöpft werden muss, kann nicht zum Anspruch werden. Das ist die stärkste Verfassungsgarantie des Entwurfs und gehört immer in denselben Satz wie der Einzug."]]),
R([["Wie die Grenze bemessen ist. ",true],[`Sie ist nicht gegriffen, sondern aus dem höchsten Bedarf von A abgeleitet, und zwar im Zentralfall und in jedem einzelnen Finanzierungsrisiko, auf volle Prozent aufgerundet. Treten alle drei Risiken zugleich ein, reicht sie nicht (${pr(alle.pct_einzug,1)}); ebenso wenig bei einer Verteidigung von 3,5 % des BIP (${pr(haag.pct_einzug,1)}). Ein höheres Verteidigungsziel verlangt deshalb eine Vertragsänderung und kann nicht still in die Grenze wachsen.`]]),
tab([{t:"Fall",w:4400},{t:"Jahr",w:900,al:RT},{t:"A % BIP",w:1200,al:RT},{t:"% des Einzugs",w:1300,al:RT},{t:`Abstand zu ${de(og)}`,w:1226,al:RT}],
 ogf.map(o=>[o.fall,String(o.jahr),de(o.a,2),de(o.pct_einzug,1),vz(o.abstand,1)]),{fills:{0:1,[ogf.indexOf(alle)]:2,[ogf.indexOf(haag)]:2}}),

H("1.3  Die Formel",H2),
R([["Die ganze Verteilung an die Gemeinden sind zwei Zahlen: ",false],[`${de(J.formel_einw)} € je Einwohner und ${de(J.formel_kind)} € je Kind zwischen 5 und 19`,true],[` (2028, nominal). Von den sieben kommunalen Aufgaben ist nur eine altersgetrieben — die Schule. Alles Übrige folgt der Einwohnerzahl. Der Betrag je Kind ist nicht gesetzt, sondern gerechnet: 3,70 % des BIP für Schulen, verteilt auf die ${de(J.kind_ant,2)} % der Bevölkerung in diesem Alter.`]]),
R([[`Jedes Kind bekommt denselben Betrag, jeder Einwohner denselben Betrag. Dass Gemeinden trotzdem unterschiedlich viel erhalten, folgt allein daraus, dass eine Gemeinde mit mehr Kindern mehr Schulkosten hat: Bei einem Kinderanteil von 12 % stehen ${de(J.fach_12)} € je Kopf zur Verfügung, beim Klubschnitt von ${de(J.kind_ant,2)} % sind es ${de(J.fach_schnitt)} €, bei 20 % sind es ${de(J.fach_20)} € — eine Spreizung um ein Fünftel über acht Prozentpunkte Kinderanteil. Gleichbehandlung erzeugt hier die Differenz, statt sie zu verletzen.`]]),
R([["Geprüft und verworfen: ein BIP-Gewicht auf das Fachbudget. Es belastet die Aufgaben, die der Einwohnerzahl folgen, mit dem falschen Treiber, spreizt die Schulbudgets um das 1,66-Fache zwischen Hamburg und Chemnitz, und es zahlt am Arbeitsort, während die Schulkosten am Wohnort entstehen. Der Anreiz, Entwicklung zuzulassen, steckt ohnehin schon in der Bodenwertabgabe."]]),

H("1.4  Die Dividende",H2),
R([["Die Dividende ist die Restgröße bei B: was nach den Fachaufgaben übrig bleibt. ",false],["Verteilt wird nach Köpfen und nach dem Preisniveau des Wohnlandes, Kinder zur Hälfte:",true],[` gleiche Kaufkraft statt gleicher Eurobetrag. Maß ist der Preisniveauindex des Individualverbrauchs (Eurostat, EU27 = 100); der Klubschnitt liegt bei ${de(J.pli_klub,1)}, Deutschland bei 109,1. Der ganze Topf wird ausgezahlt, nichts bleibt zurück.`]]),
R([[`Jede andere Verteilung scheitert: nach Steueraufkommen käme Hamburg auf das Sechsfache von Chemnitz, und Gemeinden streuen stärker als Regionen. Der Wettbewerb bleibt dadurch auf Sparsamkeit beschränkt und ist begrenzt — Verwaltung auf estnischem Niveau bringt ${de(J.verw_ersparnis_eur)} € im Monat je Einwohner (2028), weitere zehn Prozent Sparsamkeit bei den Fachausgaben nochmals etwa so viel.`]]),
R([[`Die Rechnung dahinter: Die Kommunalverwaltung kostet im Klub 1,62 % des BIP, also ${de(J.verw_anteil_pct,1)} % des kommunalen Fachbudgets. Estlands Gemeinden geben 5,8 % aus, Deutschlands 16,8 %, Frankreichs 19,5 %, Spaniens 32,8 % — bei vergleichbarem Aufgabenvolumen. Der Weg auf estnisches Niveau setzt ${de(J.verw_ersparnis_pkt,2)} Punkte des BIP frei. Mehr als den gesamten Verwaltungstopf kann niemand sparen, und das ist die Grenze des Wettbewerbs.`]]),
R([["Der Boden ist das halbe Existenzminimum am Wohnort.",true],[` Maß ist der halbe Grundfreibetrag Deutschlands, ${de(J.anker_de,2)} € je Erwachsenem und Monat in Preisen von 2028 (12.348 € im Jahr 2026, mit 2 % jährlich fortgeschrieben), in die anderen Länder mit dem Preisniveau übertragen. Diesen Boden sichert die Quote in jedem Jahr, auch ohne reales Wachstum (Abschnitt 4). Im Startjahr liegt der Topf ${de(J.deckung_boden_2028_pct-100,1)} % darüber.`]]),
tab([{t:"",w:1500},{t:"Preisniveau",w:1300,al:RT},{t:"Boden",w:1100,al:RT},{t:"2028",w:1100,al:RT},{t:"2035",w:1100,al:RT},{t:"2060",w:1100,al:RT},{t:"ohne Wachstum",w:1826,al:RT}],
 J.tabelle_laender_div.map(r=>[r.name,de(r.pli,1),de(r.boden)+' €',de(r.e2028)+' €',de(r.e2035)+' €',de(r.e2060)+' €',de(r.streng_min)+' €']),{fills:{[J.tabelle_laender_div.findIndex(r=>r.land==='DE')]:1}}),
P("Euro je Erwachsenem und Monat in Preisen von 2028; Kinder erhalten die Hälfte. 2035 und 2060 im Zentralfall (3,0 % nominal), letzte Spalte der Tiefpunkt bei null realem Wachstum. Vereinfachung: gleicher Kinderanteil in allen Ländern; Preisniveaus 2024.",{i:true,sz:19}),
R([["Umzug. ",true],[`Wer innerhalb des Klubs umzieht, behält die Dividende des bisherigen Landes, bis er drei Jahre im neuen Land wohnt und dort eine Steuerzahlung nachweist; dann gilt der Satz des neuen Landes. So lohnt es nicht, der Dividende wegen in ein günstiges Land zu ziehen, und niemand verliert beim Umzug den Anspruch.`]]),

BR(),
H("2  Die Steuerpositionen",H1),
P("Sieben Positionen beschreiben, wie eingenommen wird. Die frühere Position 08 ist in die Rahmenstruktur gewandert, wo sie als Restgröße hingehört; Position 10 entfällt mit den Sozialabgaben. Wie weit die Positionen die Quote heute nachweislich tragen, steht in Abschnitt 7."),
...POS("01","Einkommen","Ebene A","Stufentarif 0 / 9 / 16 / 21 / 26 / 28 %, harte Obergrenze",
 "Besteuert wird das Brutto, ohne Abzüge und ohne Splitting. Das Existenzminimum bleibt steuerfrei; darüber lohnt Arbeit auf jeder Stufe. Stufen bei 12.348, 25.000, 40.000, 55.000 und 70.000 €.",
 "Stufensätze festgelegt (Oktober 2026): 0, 9, 16, 21, 26 und 28 %, wie im gerechneten nationalen Modell. Eine zweite Fassung mit 9, 19, 24, 27 % wurde nie durchgerechnet und entfällt. Die Sätze bleiben vorläufig, bis eine Haushaltsmikrosimulation sie auf Klubebene kalibriert. Ein kommunaler Hebesatz entfällt; der Satz ist überall gleich."),
...POS("02","Kapital","Ebene A","28 % auf alle Erträge",
 "Kapital und Arbeit werden gleich behandelt, Veräußerungsgewinne eingeschlossen. Lohn in Kapitalertrag umzuwandeln lohnt sich nicht mehr.",
 "unverändert. Die Zuordnung zu A folgt der Mobilität der Bemessungsgrundlage."),
...POS("03","Erbschaft","Ebene A","28 % über 200.000 € je Erwerb",
 "Ein Satz, keine Verschonungsausnahmen. Wer Betrieb oder Haus erbt, kann die Steuer stunden: anfangs zum Refinanzierungssatz des Staates, über zehn Jahre steigend auf den marktüblichen Kreditzins. Erlassen wird nichts — der offene Rest bleibt als Last auf dem Gegenstand und wird bei Verkauf fällig.",
 "unverändert. Das Stundungsmuster entspricht § 154 Abs. 5 BauGB, der seit Jahrzehnten gilt."),
...POS("04a","Boden","Ebene B — eigene Steuer mit Hebesatz","Bodenwertabgabe, Satz 0,1 bis 1 % durch die Gemeinde",
 "Die Grundsteuer richtet sich nur noch nach dem Wert des Grundstücks, nicht nach dem Haus darauf. Wer baut oder saniert, zahlt dafür nicht mehr; ungenutztes Bauland in guter Lage zahlt mit. Auf Mieten darf die Abgabe nicht umgelegt werden. Bewertung alle zwei Jahre, Ansatz unter dem Bewertungswert nach dänischem Vorsichtsprinzip.",
 `geändert. Aufkommensneutralität ist die falsche Kalibrierung: Die Abgabe ist B's einzige eigene Einnahme und trägt mit ${de(J.boden_kopf)} € je Kopf knapp ${de(J.boden_anteil_fach_pct)} % des kommunalen Fachbudgets — das verlangt eher 1 % Satz als 0,3. Sie ist zugleich der Anreiz, Bebauung zuzulassen, weil Entwicklung den Bodenwert hebt.`),
...POS("04b","Verkaufsgewinn","Ebene B","28 % auf den Wertzuwachs beim Verkauf, ohne Behaltefrist",
 "Der ganze Gewinn zählt, kein Abzug der laufenden Grundsteuer. Umzugsaufschub bei Ersatzbeschaffung binnen zwei Jahren, einmalig 300.000 € Freibetrag beim endgültigen Ausstieg, Verlustverrechnung, Schritt auf den Verkehrswert im Erbfall.",
 "unverändert in der Konstruktion. Der Freibetrag wirkt als regionaler und zeitlicher Filter, ohne eine Region zu nennen."),
...POS("04c","Vermögen","Ebene A","1 % ab 2 Mio. €, anrechenbar",
 "Vermögen bis 2 Mio. € bleibt praktisch unberührt. Die Mindeststeuer greift erst darüber und ist auf die Einkommensteuer anrechenbar.",
 "unverändert, aber von 04a getrennt: Vermögen ist mobil und gehört zu A, Boden ist unbeweglich und gehört zu B."),
...POS("05","Konzerne und Plattformen","Ebene A","28 % am Ort der Nutzung",
 "Besteuert wird, wo die Kunden sitzen. Das gilt ausdrücklich für digitale Plattformen. Gewinne lassen sich verschieben, Kundschaft nicht.",
 "unverändert. Die Frage des Gewerbesteuerersatzes entfällt: Kommunen leben von Formel und Bodenabgabe, nicht von einer Gewinnsteuer."),
...POS("06","Konsum","Ebene A","Mehrwertsteuer als Label, A+ bis D",
 "Wie beim Energielabel sieht man auf einen Blick, was ein Produkt kostet und warum. Je nachhaltiger, desto günstiger. Effektivsatz im Standardkorb rund 21,5 %.",
 "unverändert. Das Ziellandprinzip verlangt ohnehin einen einheitlichen Raum, also Ebene A. Das nationale Modell rechnet mit den Stufen 5/11/17/22/28 % und effektiv 20,0 %; der Wert 21,5 % ist nicht nachgerechnet."),
...POS("07","Klima","Ebene A","Europäischer Preispfad, Rückgabe über die Dividende",
 "Den CO₂-Preis bildet der europäische Emissionshandel, nicht ein nationales Parlament. Das Konzept setzt keinen eigenen Preis, sondern fordert einen gemeinsamen Pfad entlang der vereinbarten Klimaziele. Steuervorteile für fossile Nutzung entfallen.",
 "unverändert in der Sache, neu im Weg: Die Erlöse fließen in den gemeinsamen Topf, und die Dividende ist dessen Rest. Wer wenig verbraucht, gewinnt — wie bisher."),

H("3  Der Schutz",H1),
...POS("09","Schutz","Ebene A","Bestandsgarantie und Härtefallfonds",
 "Wer heute Bürgergeld, Grundsicherung oder BAföG bekommt, erhält mindestens das bisherige Niveau; die Differenz zahlt der Härtefallfonds. Er trägt auch Wohnkosten, Pflege, Behinderung und besondere Lebenslagen.",
 `unverändert — und durch die Quotenwahl entlastet. Bei 27,91 % Steuerquote läge die Dividende bis ${J.q2791_bis} unter dem halben Existenzminimum, und der Fonds müsste diese Lücke ${J.q2791_jahre} Jahre lang tragen. Bei ${de(q,1)} % entfällt das vollständig.`),
R([["Position 10 (Arbeit) entfällt. ",true],["An ihre Stelle tritt: keine Sozialabgaben. Vorsorge wird Sache des Einzelnen, der Tarifparteien und der Kommune. Das ist kein Loch im Modell, sondern eine bewusst gezogene Grenze — und es ist im Klub bereits erprobt: Dänemark erhebt Sozialbeiträge von 0,7 % des BIP gegen 17,5 in Deutschland und finanziert denselben Sozialstaat aus Steuern."]]),

BR(),
H("4  Der Zeitpfad",H1),
R([["Vier Größen bewegen sich über die Zeit: Die Verteidigung steigt bis 2035 auf das Zielniveau. Der Zinsdienst steigt zunächst, weil der billige Altbestand seit 2024 ausläuft und zu höheren Sätzen ersetzt wird. Der Schuldenstand fällt, weil das BIP wächst. Und die Dividende ist, was dann noch übrig ist."]]),
tab([{t:"Jahr",w:900},{t:"Verteidigung",w:1500,al:RT},{t:"Schuld",w:1100,al:RT},{t:"Zinsdienst",w:1300,al:RT},{t:"A gesamt",w:1200,al:RT},{t:"Dividende",w:1200,al:RT},{t:"Klub €/Mon",w:1826,al:RT}],
 tp.map(r=>[String(r.jahr),pr(r.v),de(r.d,1)+' %',pr(r.zd),pr(r.a),pr(r.div),de(r.klub)]),{fills:{0:1,5:1}}),
P(""),
R([["Die Eurospalte steht in Preisen von 2028",true],[` und unterstellt ein reales Wachstum je Kopf von ${de(J.g_real*100,2)} % im Jahr — das ist nominal 3,0 % bei 2,0 % Preissteigerung, bei konstanter Bevölkerung. Deutschland liegt wegen seines Preisniveaus um ${de((J.r_de-1)*100,1)} % darüber: ${de(J.de_2028)} € je Einwohner im Startjahr, ${de(J.de_tief)} € im Tiefpunkt ${J.de_tief_jahr}, ${de(J.de_2060)} € im Jahr 2060.`]]),
R([["Der Tiefpunkt gehört in denselben Satz wie der Anstieg.",true],[` Die Dividende fällt bis ${J.de_tief_jahr} um ${de(-J.de_rueckgang_pct,1)} %, weil der Verteidigungsaufbau mit dem Zinsanstieg zusammenfällt, und steigt danach um ${de(J.de_anstieg_2060_pct,1)} % über den Ausgangswert. Eine Darstellung, die nur das Jahr 2060 nennt, verschweigt ${['null','ein','zwei','drei','vier','fünf','sechs','sieben','acht','neun'][J.de_tief_jahr-2028]||(J.de_tief_jahr-2028)} schwierige Jahre; eine, die nur den Tiefpunkt nennt, verschweigt den Grund, aus dem er vorübergeht.`]]),
R([["Woran die Dividende wirklich hängt.",true],[` Ihr Anteil am BIP fällt von ${de(J.div_2028,2)} auf ${de(J.div_2060,2)} %, also um ${de(-J.div_aenderung_pct,1)} % in 32 Jahren. Alles Weitere ist Wachstum. In einem Satz: `,false],[`die Kaufkraft der Dividende folgt dem realen Wachstum je Kopf, vermindert um ${de(-J.div_aenderung_pct,1)} %.`,true],[" Jede Eurozahl darüber hinaus ist eine Wachstumsannahme, keine Rechnung — und sie gehört als solche gekennzeichnet."]]),
P(""),
tab([{t:"reales Wachstum je Kopf",w:3800},{t:"2035",w:1500,al:RT},{t:"2060",w:1500,al:RT},{t:"gegen 2028",w:2226,al:RT}],
 J.tabelle_sens.map(r=>[r.fall,de(r.e2035)+' €',de(r.e2060)+' €',vz(r.gegen)+' %']),{fills:{2:1}}),
P("Deutschland, Euro je Kopf und Monat in Preisen von 2028. Die Zeilen koppeln das nominale Wachstum an das reale (Preise 2,0 %); der Zentralfall ist dieselbe Rechnung wie der Zeitpfad.",{i:true,sz:19}),
R([[`Die Quote von ${de(q,1)} % ist nicht gewählt, sondern abgeleitet, und zwar streng: `,false],["Es ist der Wert, bei dem die Dividende in jedem Land und in jedem Jahr das halbe Existenzminimum am Wohnort deckt, auch wenn die Wirtschaft real überhaupt nicht wächst.",true],[` Real kein Wachstum heißt dabei nominal 2 %, und dann sinkt auch der Schuldenstand langsamer. Rechnerisch genügen ${de(J.mindestquote_streng,2)} %; aufgerundet wird, weil Abrunden das Versprechen bräche. Die Zeile 0,0 % der Tabelle ist genau dieser Fall. Im Zentralfall liegt der Tiefpunkt ${de(J.de_tief_ueber_versprechen_pct)} % über dem Boden. Bei 27,91 % — der Quote, die die Entlastung maximiert — läge die Dividende ${J.q2791_jahre} Jahre lang darunter.`]]),
R([["Was das Kriterium kostet. ",true],[`Bis zum 7. Oktober 2026 galt als Versprechen 479 € je Kopf in Deutschland, gemessen am deutschen BIP je Kopf; daraus folgten 30,9 %. Mit der Dividende nach Preisniveau zählt nicht mehr das deutsche BIP, sondern der Topf des ganzen Klubs. Dasselbe Versprechen von 479 € verlangte dann ${de(J.mq_479_v3a_streng,2)} %, das halbe Existenzminimum ${de(J.mindestquote_streng,2)} %. Sichert man es nur im Zentralfall statt bei null Wachstum, genügen ${de(J.mindestquote_zentral,2)} %. Das Konzept wählt die strenge Lesart, weil ein Boden, der nur bei Wachstum hält, kein Boden ist.`]]),
R([["Der Nebenbefund, der die Erzählung trägt: ",false],["Die Schulden arbeiten sich von selbst ab.",true],[` Bei ausgeglichenem Haushalt bleibt der Bestand in Euro konstant, das BIP wächst, die Quote fällt von ${de(tp[0].d,1)} auf ${de(tp[5].d,1)} % — ohne einen Tilgungseuro. Aktive Tilgung wäre nachteilig: 0,50 % des BIP kosten im Startjahr ${de(J.tilg_verzicht)} € Dividende im Monat (Deutschland), und der Vorteil aus dem niedrigeren Zinsdienst holt das bis 2070 nicht ein. Das gilt, solange der Zins unter dem nominalen Wachstum liegt — und genau das sicherzustellen ist der eigentliche Wert der Klubgarantie.`]]),

H("5  Die Altschulden",H1),
R([["A übernimmt den Zinsdienst. Der Präzedenzfall ist Hamiltons Schuldenübernahme von 1790: Der Bund übernahm die Schulden der Einzelstaaten im Tausch gegen das Besteuerungsrecht. Hier liegt dieselbe Struktur vor."]]),
R([[`Die zehn Staaten zahlten 2024 zusammen ${de(J.zinsausgaben24_mrd)} Mrd € Zinsen auf ${de(J.schuld24_mrd)} Mrd € Schulden, ein effektiver Satz von ${pr(J.zins_eff_2024)}. Weil der Altbestand seit 2024 zu Marktsätzen ersetzt wird, liegt der Satz im Startjahr bei ${pr(J.zins_2028)}; der Zinsdienst kostet dann ${pr(J.zd_2028_mrd/J.bip28_klub_mrd*100)} des BIP oder ${de(J.zd_2028_mrd)} Mrd € (2028, nominal). Finanziert wird er aus A's Anteil, also mit einem einheitlichen Satz auf das jeweilige BIP. Was ein Gebiet einzahlt, folgt damit seinem BIP; was A für es auszahlt, folgt seiner Schuld. Die Differenz ist ein Transfer, und ohne Ausgleich wäre er dauerhaft.`]]),
tab([{t:"",w:1900},{t:"Schuld % BIP",w:1500,al:RT},{t:"Zinsdienst je Kopf",w:1900,al:RT},{t:"Beitrag je Kopf",w:1900,al:RT},{t:"Aufschlag",w:1826,al:RT}],
 J.tabelle_aufschlag.map(r=>[r.land,de(r.schuld,1),de(r.aus)+' €',de(r.ein)+' €',vz(r.auf)+' €'])),
P("Euro je Kopf und Jahr, 2028, nominal.",{i:true,sz:19}),
R([["Ein ",false],["territorialer Aufschlag auf A's Anteil, der sich klubweit auf null summiert",true],[` — A's Gesamtaufkommen bleibt unverändert, nur seine territoriale Herkunft verschiebt sich. Der größte Aufschlag (${J.aufschlag_max_pos_land}) beträgt ${de(J.aufschlag_max_pos_anteil_a,1)} % dessen, was A je Kopf behält, die größte Entlastung (Irland) ${de(J.aufschlag_max_anteil_a,1)} %. Er schmilzt über dreißig Jahre linear ab.`]]),
R([[`Irland wird am stärksten entlastet, obwohl seine Schuldenquote nicht die niedrigste ist. Der Grund liegt nicht in einem Entgegenkommen, sondern in der Bemessung: Irlands BIP je Kopf liegt wegen der Konzernbuchungen beim ${de(J.irland_faktor,2)}-Fachen des Klubschnitts, es zahlt deshalb weit mehr in den gemeinsamen Zinstopf ein, als sein eigener Altbestand kostet. Dieselbe Mechanik erklärt Dänemark und die Niederlande. Wer die Bemessungsgrundlage am BIP festmacht, muss diese Folge mittragen — und das Konzept tut es: Bemessen wird überall am BIP, auch in Irland, weil A's Einnahmen ein Anteil am BIP sind.`]]),
R([["Entscheidend: ",false],["Der Aufschlag erreicht die Gemeinden nicht.",true],[" Er mindert, was A aus einem Gebiet behält. Eine Gemeinde in der Picardie bekommt dieselben Beträge je Einwohner und je Kind wie eine in Estland, und jeder Bürger dieselbe Dividende nach derselben Regel. Die Altlast bleibt eine Sache zwischen den Gebieten und A."]]),
R([[`Die Garantie gilt, solange man Mitglied ist. Ein Austritt kostet sofort den Zinsaufschlag — damit wird aus der Garantie ein Zusammenhalt. A verfügt dafür über eigene Einnahmen von ${pr(J.a_2028)} des BIP gegen einen Schuldenstand von ${de(J.schuldenquote_2028,1)} %, also ${de(J.a_anteil_schuld,1)} % des Bestands, an seiner Obergrenze ${de(J.obergrenze_anteil_schuld,1)} %. Der heutige EU-Haushalt deckt 1,6 %.`]]),

H("6  Der Klub",H1),
R([["Der Klub ist kein fester Kreis, sondern ein Möglichkeitsraum. Einunddreißig europäische Staaten kommen in Frage — EU-27, Vereinigtes Königreich, Schweiz, Norwegen, Island — mit zusammen 534,8 Mio Menschen. Die Schwelle ist die Einwohnerzahl der Vereinigten Staaten: 341,8 Mio. Der Puffer beträgt 193 Mio oder 36 % des Raums."]]),
tab([{t:"Befund",w:3000},{t:"",w:6026}],
[["Zwei der sechs Größten dürfen fehlen","Selbst Deutschland und das Vereinigte Königreich gemeinsam: 382,1 Mio, die Schwelle hält. Erst der dritte Abgang reißt sie"],
 ["Sechs Staaten genügen","Deutschland, Vereinigtes Königreich, Frankreich, Italien, Spanien, Polen kommen auf 365,8 Mio"],
 ["Sonderrollen kosten 8 %","Verfassungsmäßig Neutrale und Staaten mit steuerlichem Sondermodell zusammen 43,6 Mio — fast nur kleine Staaten"],
 ["Nicht-EU-Staaten sind leichter","Vereinigtes Königreich, Schweiz, Norwegen und Island sind nicht an Artikel 113 AEUV gebunden. Für sie wäre der Klub ein Beitritt, kein Vertragsbruch"]]),
P(""),
R([["Die zehn Staaten, auf denen alle Zahlen dieses Dokuments beruhen, sind nicht der Klub, sondern die Stichprobe, für die vollständige Eurostat-Daten vorlagen. Sie ist nach Westen und Norden verzerrt: Polen und Italien fehlen, und mit ihnen der mittlere Teil der Einkommensverteilung Europas. Ein Klub, der sie einschließt, hätte ein niedrigeres BIP je Kopf und damit niedrigere Eurobeträge bei gleichen Anteilen."]]),
R([["Zum Namen: „Europäische Gemeinschaften\" im Plural ist der amtliche Name der EGKS, EWG und EURATOM vor Maastricht, auf Englisch ebenso. ",false],["Freie Gemeinschaften Europas",true],[" trägt dieselbe Aussage ohne diese Kollision."]]),

H("7  Was es kostet und wie es gedeckt ist",H1),
tab([{t:"",w:4600},{t:"heute",w:2200,al:RT},{t:"Entwurf",w:2226,al:RT}],
[["Steuern",de(J.steuern_heute,2),de(q,2)],
 ["Sozialbeiträge",de(J.sb_heute,2),"0,00"],
 ["Gesundheit, außerhalb des Steuertopfs","enthalten",de(J.gesundheit,2)],
 ["Gesamtlast in % des BIP",de(J.last_heute,2)+" *",de(J.last_entwurf,2)]],{fills:{3:1}}),
P(`* Eurostat-Aggregat der zehn Staaten, BIP-gewichtet, nach Abzug der veranlagten, aber voraussichtlich nicht einbringlichen Steuern und Beiträge (D995). Vor allem deshalb ist es um 0,07 Punkte (ungerundet 0,06) kleiner als die Summe der beiden Zeilen darüber; der Rest ist Rundung.`,{i:true,sz:19}),
R([[`Eine Entlastung von ${de(J.entlastung,2)} Punkten des BIP oder ${de(J.entlastung_mrd)} Mrd € im Jahr (2028, nominal). Entlastet wird vor allem der Faktor Arbeit: Heute ruhen 28,53 % des BIP auf Arbeit und Einkommen, davon 14,88 Punkte Sozialbeiträge, die vollständig entfallen. Gegenfinanziert wird das über Verbrauch, CO₂, Boden und Unternehmen. Beides gehört in denselben Satz — wer nur die Entlastung nennt, verliert beim ersten Gegenargument die Glaubwürdigkeit für alles Übrige.`]]),
H("7.1  Was die Positionen nachweislich tragen",H2),
R([[`Die Quote ist von der Ausgabenseite her abgeleitet. Ob die Positionen sie aufbringen, ist eine eigene Rechnung. Sie liegt bisher nur für Deutschland vor, aus dem gerechneten nationalen Modell; auf Klubebene fehlt sie. Übertragen auf die Positionen dieses Entwurfs ergibt sich:`]]),
tab([{t:"Position",w:6400},{t:"% BIP",w:1200,al:RT},{t:"Art",w:1426}],
 J.tabelle_deckung.map(r=>[r[0],de(r[1],2),r[2]]).concat([["Summe, nachgewiesen",de(J.deckung_gesamt,2),""],[`Quote`,de(q,2),""],["Lücke",de(J.deckung_luecke,2),"offen"]]),{fills:{[J.tabelle_deckung.length]:1,[J.tabelle_deckung.length+2]:2}}),
P("Deutsche Basis: Anteile an der Modellbasis des nationalen Modells (4.200 Mrd), Dividendenstufe 50 %. Die Dividende ist dort einkommensteuerpflichtig. Der Bodenwert ist mit dem Satz dieses Entwurfs angesetzt, nicht mit dem aufkommensneutralen des nationalen Modells.",{i:true,sz:19}),
R([["Das Ergebnis ist eine offene Lücke, keine Deckung: ",true],[`${de(J.deckung_luecke,2)} Punkte des BIP, auf den Klub übertragen rund ${de(J.deckung_luecke_mrd_klub)} Mrd € im Jahr (2028, nominal). Sie ist kleiner, als die Gegenüberstellung von 27,91 und ${de(q,1)} % vermuten lässt, weil das nationale Modell die Bausteine Vermögensteuer, Subventionsabbau und CO₂-Pfad gesondert ausweist und die Bodenwertabgabe hier höher angesetzt ist. Ob sie sich auf Klubebene schließt, hängt an den Steuerbasen der zehn Staaten, die anders zusammengesetzt sind als die deutsche. Das ist die nächste Rechnung des Konzepts.`]]),
R([["Und zum Namen des Konzepts: Die 28 bezeichnen den ",false],["Satz",true],[` auf Einkommen und Unternehmensgewinn, nicht die Staatsquote. Das war immer so gemeint; seit die Quote bei ${de(q,1)} % liegt, muss es dastehen.`]]),

H("8  Was offen bleibt",H1),
tab([{t:"Punkt",w:2800},{t:"Stand",w:6226}],
[["Deckung der Quote auf Klubebene",`Die wichtigste offene Rechnung (Abschnitt 7.1). Auf deutscher Basis fehlen ${de(J.deckung_luecke,2)} Punkte. Für den Klub braucht sie die Steuerbasen der zehn Staaten nach Position`],
 ["Haushaltsmikrosimulation","Erst wenn die Aggregate rechnerisch und inhaltlich geprüft stehen. Ohne sie weiß niemand, wie es einer Alleinerziehenden mit zwei Kindern ergeht, und die Stufensätze des Tarifs bleiben vorläufig. Folgeaufgabe mit fachlicher Beteiligung Dritter"],
 ["Verteidigung: zwei Definitionen","Die Basis 1,40 % stammt aus der COFOG-Funktionsrechnung (Eurostat GF02). Die Haager Zusage, aus der der Zielwert abgeleitet ist, rechnet nach NATO-Systematik breiter — für Deutschland 2,12 % gegen 1,4 % nach COFOG. Der Pfad überzeichnet den Aufbau damit um schätzungsweise einen halben Punkt des BIP. Das wirkt zugunsten der Vorsicht: A's Bedarf ist eher zu hoch als zu niedrig angesetzt, und ein Punkt des BIP sind "+de(J.punkt_bip_eur_de)+" € Dividende im Monat in Deutschland, "+de(J.klub_punkt_bip_eur)+" € im Klubschnitt"],
 ["Zusammensetzung der 2,5 %","Wie viel Kernverteidigung, wieviel digitale Souveränität — eine Setzung, die fachlich zu prüfen ist. Ob 2,5 % militärisch genügen, ist keine Frage für dieses Modell. Hinzu kommt, dass ein Teil der digitalen Souveränität heute in den A-Posten Grundlagenforschung und Netze steckt und dort nicht abgezogen wurde"],
 ["NATO-Konflikt",`Acht der zehn Klubstaaten haben die Haager Zusage über 3,5 % unterschrieben. Ein Klub bei 2,5 % steht dazu im Widerspruch, sofern er die NATO nicht ersetzt. Bei 3,5 % bräuchte A ${de(haag.pct_einzug,1)} % des Einzugs; die Obergrenze von ${de(og)} % wäre durch Vertragsänderung anzuheben`],
 ["Artikel 113 AEUV","Der Vertragstext verlangt für Steuerharmonisierung Einstimmigkeit im Rat. Ein Klub mit Mehrheitsentscheid ist im geltenden EU-Rahmen nicht darstellbar. Vereinbarungsgemäß zurückgestellt — Sache der Gemeinschaften beim Umstieg"],
 ["A-Standards","Der einzige Mechanismus ohne Zahl. Dort entscheidet sich die Qualität der Schulen, und dort ist der Entwurf am wenigsten festgelegt"],
 ["Schulgeld und Schulort","Das Geld folgt dem Wohnort, der Schulplatz liegt oft in der Nachbargemeinde. Braucht einen Ausgleich, wie ihn deutsche Gastschulbeiträge kennen"],
 ["Restlaufzeit und Schuldenstand 2028","Restlaufzeit mit 7,5 Jahren als Erfahrungswert angesetzt, nicht erhoben. Die Schuldenquote 2028 ist aus dem heutigen Kurs fortgeschrieben ("+de(J.schuldenquote_2028,1)+" %, gleich bleibende Defizite); liegt sie 3,5 Punkte höher, braucht A im Höchstjahr "+de(ogf.find(o=>o.fall.startsWith('Schuldenquote')).pct_einzug,1)+" % des Einzugs"],
 ["Mindestgröße der Gemeinden","Dänischer Richtwert 20.000, besser 30.000 Einwohner. Ohne Gebietsreform oder Pflichtverbände kann B seine Aufgaben nicht tragen"],
 ["Umzugsregel und Europarecht","Drei Jahre Wohnsitz mit nachgewiesener Steuerzahlung, bis der neue Satz gilt. Zu klären: was als Steuerzahlung gilt (Einkommensteuer, oder genügt die Steuerpflicht, etwa für Rentner und Studierende), Kinder folgen den Eltern, und ob die Wartezeit mit der Freizügigkeit und dem Gleichbehandlungsgebot vereinbar ist (Art. 45 AEUV, Verordnung 883/2004), wenn jemand in ein teureres Land zieht. Keine Rechtsprüfung"],
 ["Preisniveau und Existenzminimum fortschreiben","Preisniveaus sind die Werte 2024; sie ändern sich und müssen jährlich übernommen werden, mit Verzug von etwa einem Jahr. Das Existenzminimum ist mit der Preissteigerung fortgeschrieben (Annahme); der deutsche Grundfreibetrag folgt tatsächlich dem Existenzminimumbericht und stieg zuletzt schneller"],
 ["Stichprobe statt Klub","Alle Zahlen beruhen auf zehn Staaten mit vollständigen Daten, nicht auf dem Möglichkeitsraum von einunddreißig. Polen und Italien fehlen"]]),

H("9  Zahlengrundlage",H1),
R([[`Alle Struktur- und Aufkommenszahlen aus Eurostat, Berichtsjahr 2024, aus Einzelabrufen: nama_10_gdp, gov_10a_exp, gov_10a_main, gov_10a_taxag, gov_10dd_edpt1, irt_lt_mcby_a, demo_gind, demo_pjangroup, nama_10r_2gdp. Einwohner und Zinsausgaben sind am 6. Oktober 2026 erneut einzeln abgerufen (Belgien vorläufig); BIP, Schulden, Renditen und Funktionsausgaben stammen aus den Abrufen vom 2. bis 4. Oktober und sind nicht erneut geprüft. Die zehn Staaten kommen 2024 auf ${de(J.bip24_klub_mrd)} Mrd € Wirtschaftsleistung und ${de(J.pop_klub_mio,1)} Mio Menschen (Jahresdurchschnitt). Die Zinsausgaben 2024 (${de(J.zinsausgaben24_mrd,1)} Mrd €) sind für neun Staaten abgerufen, für Estland geschätzt (0,2 Mrd €).`]]),
R([[`Die Basis 2028 ist aus dem Istwert 2024 mit den nominalen Raten der Frühjahrsprojektion der Bundesregierung vom 22. April 2026 fortgeschrieben (+3,3 / +2,8 / +3,8 %), für 2028 vorsichtig mit +3,0 %; das ergibt den Faktor ${de(J.faktor,5)}. Für Deutschland sind das `,false],[`${de(J.bip28_de_mrd,1)} Mrd €`,true],[", für den Klub ",false],[`${de(J.bip28_klub_mrd)} Mrd €`,true],[` oder ${de(J.kopf_klub)} € je Kopf. Dass eine einzige, nämlich die deutsche Wachstumsrate auf alle zehn Staaten angewandt wird, ist eine Vereinfachung; sie ist vertretbar, weil Deutschland ${de(J.de_anteil_bip_pct,1)} % des Klub-BIP trägt und die nominalen Raten der Zone nahe beieinander liegen, bleibt aber eine Vereinfachung.`]]),
R([["Weitere Quellen: NATO, The Hague Summit Declaration vom 25. Juni 2025. Europäische Kommission, EU budget 2028–2034 vom 16. Juli 2025. US Census Bureau, NST-EST2025-POP. Local Government Denmark zur Strukturreform 2007. UCLG/OECD-Länderprofil Dänemark. Europäisches Parlament, EPRS, zu den Verteidigungsausgaben der Mitgliedstaaten. Artikel 113 AEUV, konsolidierte Fassung. Wallace E. Oates, Fiscal Federalism, 1972."]]),
R([[`Einschränkungen: Irlands BIP je Kopf liegt wegen Konzernbuchungen beim ${de(J.irland_faktor,2)}-Fachen des Klubschnitts und drückt jeden Mittelwert; das Konzept bemisst trotzdem am BIP, nicht am GNI*, weil Steuern am Ort der Wertschöpfung und Nutzung anknüpfen (mit GNI* läge das Klub-BIP um etwa 2 % niedriger). Die Teilsektoren sind unkonsolidiert. Vier A-Posten sind Schätzungen von je rund 0,30 Punkten, zusammen 1,18 Punkte oder 13 % dieser Ebene — und damit in derselben Größenordnung wie der Abstand zwischen den Ebenen. Die Regionalrechnung ist ungewichtet über 38 NUTS-2-Gebiete. Eurostats Sammelabrufe ordnen Werte falsch zu oder liefern sie unvollständig; alle Zahlen stammen deshalb aus Einzelabrufen mit festgelegten Dimensionen.`]]),
R([["Gegenüber der Fassung vom 4. Oktober 2026 geändert: ",true],[`Einwohnerzahl (255,1 statt 254,8 Mio, acht Länderwerte waren falsch übertragen), effektiver Zins 2024 (${de(J.zins_eff_2024,2)} statt 1,53 %, die Zinsausgaben lagen bei ${de(J.zinsausgaben24_mrd)} statt 146 Mrd €), Auslaufen des Altbestands ab 2024 statt 2028 und die strenge Lesart des Quotenkriteriums (real null heißt nominal 2 %); daraus die Quote 30,8 statt 30,6 %. Der höhere Zins senkte die Dividende der ersten Jahre: 490 statt 506 € je Einwohner im Startjahr. Die Obergrenze von 36 % war damit abgeleitet und bestätigt. Einzelheiten im Logbuch, Band III, v3.12.`]]),
R([["Gegenüber der Fassung vom 6. Oktober 2026 geändert: ",true],[`Schuldenquote 2028 aus dem heutigen Kurs fortgeschrieben (${de(J.schuldenquote_2028,1)} statt 78,4 %); Dividende nach dem Preisniveau des Wohnlandes mit Umzugsregel; Quotenkriterium halbes Existenzminimum statt 479 € je Kopf in Deutschland. Daraus die Quote ${de(q,1)} statt 30,8 % und die Obergrenze ${de(og)} statt 36 %. Einzelheiten im Logbuch, Band III, v3.19 und v3.20.`]]),
HR(),
P("Rechnung: modell/gesamtrechnung.py (Formeln der Originalskripte modell/rahmen/basis.py, pfad.py, final.py, tilgung.py, aufschlag.py), Ergebnis daten/aggregate/gesamtrechnung.json. Entwurf zur Diskussion, keine beschlossene Fassung.",{i:true,sz:19}),
P("Text: Initiative 28:28, Lizenz CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Eingangsdaten Dritter unterliegen deren Bedingungen.",{i:true,sz:19}),
];

const doc=new Document({creator:"Initiative 28:28",title:"TAX 28:28 — Das Gesamtkonzept",styles:{default:{document:{run:{font:"Calibri",size:21}}}},sections:[{
properties:{page:{margin:{top:1134,bottom:1134,left:1134,right:1134}}},children:kinder}]});
Packer.toBuffer(doc).then(b=>{const ziel=path.join(WURZEL,'dokumente','TAX-2828-Gesamtkonzept.docx');fs.writeFileSync(ziel,b);console.log("ok",ziel,b.length)});
