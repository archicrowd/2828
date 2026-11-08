// Weltkarte für das Rechenspiel „Bauen Sie die Gemeinschaft“ (Logbuch v4.79, v4.80 in die Seite übernommen).
// Eingabe: countries.geo.json aus github.com/johan/world.geo.json (Unlicense; abgeleitet aus Natural Earth, gemeinfrei; Sekundärquelle,
// Herkunft laut README des Datensatzes nicht vollständig belegt). Nicht im Repository (Rohdaten); Pfad als Argument.
// Ausgabe: karte.json im Ordner dieses Skripts: Pfade je ISO-3-Code (Projektion Natural Earth 1, 960 × 500, ohne Antarktis), Schwerpunkte,
// Kreise für Kleinstaaten, die im Datensatz fehlen oder zu klein sind.
// Aufruf: NODE_PATH=/opt/npm-tools/node_modules node seite/werkzeuge/karte/karte_bau.js <countries.geo.json>
const fs = require("fs"), path = require("path"), d3 = require("d3-geo");
const geo = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
geo.features = geo.features.filter(f => f.id !== "ATA" && f.id !== "-99");
// Ringe so drehen, wie d3-geo sie erwartet (Fläche < Halbkugel)
for (const f of geo.features) {
  if (d3.geoArea(f) > 2 * Math.PI) {
    const g = f.geometry;
    const rev = poly => poly.map(r => r.slice().reverse());
    g.coordinates = g.type === "Polygon" ? rev(g.coordinates) : g.coordinates.map(rev);
  }
}
const W = 960, H = 500;
const proj = d3.geoNaturalEarth1().fitExtent([[4, 4], [W - 4, H - 4]], geo);
const pfad = d3.geoPath(proj).digits(1);
const out = { breite: W, hoehe: H, laender: {}, kreise: {} };
for (const f of geo.features) {
  const c = pfad.centroid(f);
  out.laender[f.id] = { d: pfad(f), x: Math.round(c[0]), name: f.properties.name };
}
// Kleinstaaten (Längen- und Breitengrad, eigene Kenntnis, gerundet)
const klein = { BRB: [-59.55, 13.17], MUS: [57.55, -20.25], MLT: [14.45, 35.9], LUX: [6.13, 49.61],
  AND: [1.52, 42.51], LIE: [9.55, 47.17], MCO: [7.42, 43.74], SMR: [12.46, 43.94] };
for (const [k, ll] of Object.entries(klein)) { const p = proj(ll); out.kreise[k] = [Math.round(p[0] * 10) / 10, Math.round(p[1] * 10) / 10]; }
// Ausschnitt Europa für die Voreinstellungen „Nur Europa“ und „Die 30 gerechneten“
const a = proj([-25, 72]), b = proj([45, 33]);
out.europa = [Math.round(a[0]), Math.round(a[1]), Math.round(b[0] - a[0]), Math.round(b[1] - a[1])];
fs.writeFileSync(path.join(__dirname, "karte.json"), JSON.stringify(out));
console.log("Länder", Object.keys(out.laender).length, "Bytes", JSON.stringify(out).length, "Europa", out.europa);
