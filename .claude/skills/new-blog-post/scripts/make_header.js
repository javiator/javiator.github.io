// Generates an abstract header/teaser image when the author has no artwork.
// usage: node make_header.js <out.png> "<seed text, e.g. the slug>" [hue 0-360]
// The theme overlays the post title on top, so the image carries no text.
const path = require('path');
const fs = require('fs');
const [out, seed = 'post', hueArg] = process.argv.slice(2);
if (!out) { console.error('usage: make_header.js <out.png> <seed> [hue]'); process.exit(2); }

let h = 2166136261;
for (const c of seed) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; }
const rnd = () => { h ^= h << 13; h >>>= 0; h ^= h >> 17; h ^= h << 5; h >>>= 0; return h / 4294967296; };
const hue = hueArg !== undefined ? Number(hueArg) : Math.floor(rnd() * 360);
const W = 1600, H = 800;

let shapes = '';
for (let i = 0; i < 9; i++) {
  const x = rnd() * W, y = rnd() * H, r = 120 + rnd() * 320;
  const hh = (hue + (rnd() - 0.5) * 70 + 360) % 360;
  shapes += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${r.toFixed(0)}" fill="hsl(${hh.toFixed(0)} 75% ${(45 + rnd() * 25).toFixed(0)}%)" opacity="${(0.18 + rnd() * 0.25).toFixed(2)}"/>`;
}
let nodes = '', lines = '';
const pts = Array.from({ length: 16 }, () => [rnd() * W, rnd() * H]);
pts.forEach(([x, y], i) => {
  nodes += `<circle cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" r="${(4 + rnd() * 5).toFixed(1)}" fill="white" opacity="0.75"/>`;
  const [x2, y2] = pts[(i + 1 + Math.floor(rnd() * 3)) % pts.length];
  lines += `<line x1="${x.toFixed(0)}" y1="${y.toFixed(0)}" x2="${x2.toFixed(0)}" y2="${y2.toFixed(0)}" stroke="white" stroke-width="1.5" opacity="0.28"/>`;
});
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="hsl(${hue} 70% 16%)"/><stop offset="1" stop-color="hsl(${(hue + 50) % 360} 65% 30%)"/></linearGradient>
<filter id="b"><feGaussianBlur stdDeviation="60"/></filter></defs>
<rect width="${W}" height="${H}" fill="url(#g)"/><g filter="url(#b)">${shapes}</g>${lines}${nodes}</svg>`;

(async () => {
  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.setContent(`<body style="margin:0">${svg}</body>`);
  fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: W, height: H } });
  await browser.close();
  console.log(`wrote ${out} (hue ${hue})`);
})();
