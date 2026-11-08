// Ländernamen in sechs Sprachen für die Weltkarte der Gemeinschaft der Staaten (Logbuch v4.80).
// Quelle: Unicode CLDR über die ICU-Daten von Node.js (Intl.DisplayNames); Ausgabe namen.json. Aufruf: node namen_bau.js
const fs = require('fs');
const C = ['AT','BE','BG','CH','CY','CZ','DE','DK','EE','GR','ES','FI','FR','HR','HU','IE','IS','IT','LT','LU','LV','MT','NL','NO','PL','PT',
  'RO','SE','SI','SK','AU','BB','CA','CL','CR','JP','KR','NZ','GB','UY','MU','US','SG','BW',
  'AL','AD','AM','AZ','BA','GE','LI','MD','MC','ME','MK','SM','RS','TR','UA'];
const out = {quelle: 'Unicode CLDR (ICU ' + process.versions.icu + ', Node ' + process.version + ')'};
for (const l of ['de','en','fr','it','es','pl']) {
  const dn = new Intl.DisplayNames([l], {type: 'region'});
  out[l] = Object.fromEntries(C.map(c => [c, dn.of(c)]));
}
fs.writeFileSync(__dirname + '/namen.json', JSON.stringify(out, null, 1) + '\n');
console.log('namen.json:', C.length, 'Staaten,', out.quelle);
