// Serves the built site, renders one post in headless Chromium, checks it, and
// writes a full-page PNG and a PDF for the author to review.
// usage: node render_preview.js <siteDir> <urlPath> <outDir> <postFile>
const http = require('http');
const fs = require('fs');
const path = require('path');

const [siteDir, urlPath, outDir, postFile] = process.argv.slice(2);
const MIME = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml',
  '.gif': 'image/gif', '.webp': 'image/webp', '.xml': 'application/xml', '.json': 'application/json',
  '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.ico': 'image/x-icon' };

function resolveFile(urlPathname) {
  let p = path.join(siteDir, decodeURIComponent(urlPathname.split('?')[0].split('#')[0]));
  if (!p.startsWith(siteDir)) return null;
  if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
  if (!fs.existsSync(p) && fs.existsSync(p + '.html')) p += '.html';
  return fs.existsSync(p) ? p : null;
}

function frontMatter(file) {
  const fm = (fs.readFileSync(file, 'utf8').split(/^---\s*$/m)[1]) || '';
  const get = (k) => { const m = fm.match(new RegExp('^' + k + ':\\s*"?([^"\\n]+?)"?\\s*$', 'm')); return m ? m[1] : null; };
  return { series: get('series'), project: get('project'), evolution: get('evolution_number'), featured: get('featured') };
}

(async () => {
  const problems = [], notes = [];
  if (!resolveFile(urlPath)) {
    console.log(`PREVIEW FAILED: ${urlPath} was not generated. Check the date, filename and permalink.`);
    process.exit(1);
  }
  const server = http.createServer((req, res) => {
    const f = resolveFile(req.url);
    if (!f) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${server.address().port}`;

  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  const failed = [];
  page.on('pageerror', (e) => problems.push(`JavaScript error on page: ${e.message}`));
  page.on('requestfailed', (r) => failed.push(r.url()));
  page.on('response', (r) => { if (r.status() >= 400) failed.push(`${r.status()} ${r.url()}`); });

  await page.goto(base + urlPath, { waitUntil: 'load' });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(1500); // mermaid renders after load

  const info = await page.evaluate(() => {
    const q = (s) => Array.from(document.querySelectorAll(s));
    const article = document.querySelector('.page__content') || document.body;
    return {
      title: (document.querySelector('.page__title') || {}).textContent || '',
      hero: !!document.querySelector('.page__hero--overlay'),
      words: article.innerText.split(/\s+/).length,
      toc: q('.toc__menu a').length,
      h1InBody: q('.page__content h1').length,
      mermaidBlocks: q('.mermaid').length,
      mermaidRendered: q('.mermaid svg').length,
      mermaidUnprocessed: q('pre code.language-mermaid').length,
      mermaidErrors: q('.mermaid').filter((d) => /Syntax error/i.test(d.textContent)).length,
      brokenImages: q('img').filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.getAttribute('src')),
      links: q('.page__content a[href]').map((a) => a.getAttribute('href')),
      rawLiquid: /\{%|%\}|\{\{|\}\}/.test(article.innerText.replace(/```[\s\S]*?```/g, '')),
      wideTables: q('.page__content table').filter((t) => t.scrollWidth > t.parentElement.clientWidth + 4).length,
      emptyTaxonomy: q('.page__taxonomy-item').length === 0,
    };
  });

  if (!info.title.trim()) problems.push('Title is not rendered');
  if (!info.hero) problems.push('Header overlay image is not rendered (check header.overlay_image)');
  if (info.h1InBody) problems.push('Body contains an H1 heading');
  if (info.brokenImages.length) problems.push('Broken images: ' + info.brokenImages.join(', '));
  if (info.mermaidErrors) problems.push(`${info.mermaidErrors} mermaid diagram(s) have syntax errors`);
  if (info.mermaidUnprocessed) problems.push('Mermaid blocks were not processed (is "mermaid: true" set?)');
  if (info.emptyTaxonomy) problems.push('No categories/tags rendered at the foot of the post');
  if (info.wideTables) notes.push(`${info.wideTables} table(s) overflow the content width at desktop size`);
  if (info.toc < 2) notes.push('Table of contents has fewer than 2 entries (add H2 sections)');

  const external = failed.filter((u) => !u.includes('127.0.0.1'));
  const local = failed.filter((u) => u.includes('127.0.0.1'));
  if (local.length) problems.push('Local resources failed to load: ' + local.join(', '));
  const mermaidCdnDown = external.some((u) => /mermaid/.test(u));
  if (info.mermaidBlocks && info.mermaidRendered < info.mermaidBlocks && !info.mermaidErrors) {
    (mermaidCdnDown ? notes : problems).push(mermaidCdnDown
      ? 'Mermaid CDN unreachable here, so diagrams show as text in this preview (they render on the live site). Review diagram syntax carefully.'
      : `Only ${info.mermaidRendered} of ${info.mermaidBlocks} mermaid diagrams rendered`);
  }
  if (info.rawLiquid) notes.push('Text that looks like unrendered Liquid ({% %} or {{ }}) is visible on the page; confirm it is intentional');

  // Internal links must resolve in the built site.
  const dead = [...new Set(info.links.filter((h) => h.startsWith('/') && !h.startsWith('//')))]
    .filter((h) => !resolveFile(h));
  if (dead.length) problems.push('Internal links that do not exist: ' + dead.join(', '));

  // The post must show up everywhere it is supposed to be listed.
  const fm = frontMatter(postFile);
  const listings = ['/', '/posts/', '/categories/', '/tags/'];
  if (fm.series) listings.push(`/series/${fm.series}/`, '/series/');
  if (fm.project) {
    const pid = fm.project.toLowerCase().replace(/ /g, '-');
    listings.push(`/projects/${pid}/posts/`);
    if (fm.evolution && fm.evolution !== '0') listings.push(`/projects/${pid}/evolution-${fm.evolution}/`);
  }
  const listed = [];
  for (const l of listings) {
    const f = resolveFile(l);
    if (!f) { problems.push(`Listing page ${l} does not exist`); continue; }
    const html = fs.readFileSync(f, 'utf8');
    const has = l === '/series/' ? html.includes(`/series/${fm.series}/`) : html.includes(`href="${urlPath}"`);
    if (has) listed.push(l);
    else if (l === '/') notes.push('Not linked from the home page (expected unless it is recent or featured)');
    else problems.push(`Post is not listed on ${l}`);
  }

  const slug = urlPath.replace(/\/$/, '').split('/').pop();
  const png = path.join(outDir, `${slug}.png`);
  const pdf = path.join(outDir, `${slug}.pdf`);
  await page.evaluate(() => { const b = document.getElementById('back-to-top'); if (b) b.style.display = 'none'; window.scrollTo(0, 0); });
  // Chromium cannot capture images taller than ~16000px, so long posts are captured at 1x.
  const pageHeight = await page.evaluate(() => document.documentElement.scrollHeight);
  if (pageHeight * 2 <= 16000) {
    await page.screenshot({ path: png, fullPage: true });
  } else {
    const flat = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
    await flat.goto(base + urlPath, { waitUntil: 'load' });
    await flat.waitForLoadState('networkidle').catch(() => {});
    await flat.waitForTimeout(1500);
    await flat.evaluate(() => { const b = document.getElementById('back-to-top'); if (b) b.style.display = 'none'; });
    await flat.screenshot({ path: png, fullPage: true });
    await flat.close();
    if (pageHeight > 16000) notes.push('Page is very long; the PNG may be cut off at the bottom. Use the PDF for the full page.');
  }
  await page.emulateMedia({ media: 'screen' });
  await page.pdf({ path: pdf, width: '1440px', height: '2000px', printBackground: true });
  // Small screenshot of the top of the page for a quick look at hero + sidebar.
  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await mobile.goto(base + urlPath, { waitUntil: 'load' });
  await mobile.waitForTimeout(1200);
  const mobilePng = path.join(outDir, `${slug}-mobile.png`);
  await mobile.screenshot({ path: mobilePng, fullPage: false });
  await browser.close();
  server.close();

  console.log(`\nPreview of ${urlPath}`);
  console.log(`  title: ${info.title.trim().replace(/\s+/g, ' ')}`);
  console.log(`  words: ~${info.words}   toc entries: ${info.toc}   mermaid: ${info.mermaidRendered}/${info.mermaidBlocks} rendered`);
  console.log(`  listed on: ${listed.join('  ') || '(none)'}`);
  console.log(`  desktop: ${png}\n  mobile:  ${mobilePng}\n  pdf:     ${pdf}`);
  notes.forEach((n) => console.log(`  NOTE  ${n}`));
  problems.forEach((p) => console.log(`  ERROR ${p}`));
  console.log(`\nRESULT: ${problems.length ? 'FAILED - fix every ERROR and re-run' : 'OK'}`);
  process.exit(problems.length ? 1 : 0);
})().catch((e) => { console.error('PREVIEW FAILED:', e.message); process.exit(1); });
