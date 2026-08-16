/* Vivarcus website English pages — automated test suite (puppeteer). */
let puppeteer;
try {
  puppeteer = require('puppeteer');
} catch (e) {
  // fallback: puppeteer bundled with global mermaid-cli
  const { execSync } = require('child_process');
  const root = execSync('npm root -g').toString().trim();
  puppeteer = require(root + '/@mermaid-js/mermaid-cli/node_modules/puppeteer');
}

/* 运行：先起静态服务（python3 -m http.server 8099），再 node tools/test_en_pages.js */

const BASE = 'http://localhost:8099';
const results = [];
let failures = 0;

function check(name, ok, detail) {
  results.push({ name, ok, detail });
  if (!ok) failures++;
  console.log((ok ? '  ✓ ' : '  ✗ ') + name + (detail ? ' — ' + detail : ''));
}

// pages that should render fully in English with ?lang=en
const EN_PAGES = [
  'ctcae.html', 'glossary.html', 'tmf-checker.html', 'pd-decision-tree.html',
  'timeline-calendar.html', 'templates.html', 'edl-generator.html',
  'audit-findings.html', 'tmf-reference.html',
  'template-monitoring-visit-report.html', 'template-mvr-example.html',
  'template-site-initiation-report.html', 'template-closeout-visit-report.html',
  'template-protocol-deviation-log.html', 'template-icf-checklist.html',
  'template-tmf-index.html', 'template-sop-framework.html',
  'template-audit-readiness-checklist.html', 'template-training-log.html',
  'template-sae-report.html', 'template-site-initiation-checklist.html',
  'template-monitoring-visit-checklist.html', 'template-closeout-checklist.html',
  'template-metadata-review-sop.html', 'template-data-correction-sop.html', 'template-access-register.html',
  // regulations hub + generated regulation/whitepaper pages (batch 3)
  'regulations.html', 'gcp-2026.html', 'ich-e6r3.html', 'audit-trail.html',
  'annex-c.html', 'retention.html', 'safety-reporting.html',
  'ethics-review.html', 'submission.html',
  'whitepaper.html', 'cde-trials.html',
  'visit-calculator.html', 'sample-size-calculator.html',
  'contact.html',
];

async function visibleChinese(page) {
  return page.evaluate(() => {
    // text of visible elements only, excluding JSON data script tags
    const out = [];
    document.querySelectorAll('body *:not(script):not(style)').forEach((el) => {
      const style = getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden') return;
      for (const node of el.childNodes) {
        if (node.nodeType === Node.TEXT_NODE) {
          const t = node.textContent.trim();
          if (t) out.push(t);
        }
      }
    });
    const full = out.join(' ');
    const zh = full.match(/[一-鿿]+/g) || [];
    return zh.slice(0, 6).join(' | ');
  });
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome',
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });

  // ---------- 1. all pages: ?lang=en renders no visible Chinese, no console errors ----------
  console.log('\n== 1. English render sweep ==');
  for (const p of EN_PAGES) {
    const errors = [];
    page.removeAllListeners('console');
    page.on('console', (msg) => { if (msg.type() === 'error') errors.push(msg.text()); });
    page.removeAllListeners('pageerror');
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto(`${BASE}/${p}?lang=en`, { waitUntil: 'networkidle0' });
    await new Promise((r) => setTimeout(r, 400));
    let zh = await visibleChinese(page);
    if (p === 'template-mvr-example.html') {
      // 虚构示例中的人名按翻译规范保留中文（数据非 UI 文案）
      zh = zh.split(' | ').filter((t) => !/^(张一|李二|王三|赵四)$/.test(t)).join(' | ');
    }
    check(p, !zh && errors.length === 0, zh ? `zh残留: ${zh}` : errors.join('; '));
  }

  // ---------- 2. zh regression (no lang param) ----------
  console.log('\n== 2. zh regression ==');
  for (const p of ['ctcae.html', 'glossary.html', 'templates.html', 'audit-findings.html', 'template-sae-report.html', 'gcp-2026.html', 'regulations.html', 'whitepaper.html', 'annex-c.html', 'retention.html', 'safety-reporting.html', 'template-metadata-review-sop.html']) {
    await page.evaluate(() => localStorage.removeItem('vivarcus-lang'));
    await page.goto(`${BASE}/${p}`, { waitUntil: 'networkidle0' });
    await new Promise((r) => setTimeout(r, 400));
    const h1 = await page.evaluate(() => document.querySelector('h1').textContent.trim());
    check(p + ' zh', /[一-鿿]/.test(h1), 'h1: ' + h1);
  }

  // ---------- 3. interactions ----------
  console.log('\n== 3. interactions ==');

  // 3.1 ctcae search (en): search "neutropenia" opens term
  await page.goto(`${BASE}/ctcae.html?lang=en`, { waitUntil: 'networkidle0' });
  await page.type('#ctcae-search-input', 'neutropenia');
  await new Promise((r) => setTimeout(r, 300));
  const ctcaeHit = await page.evaluate(() => {
    const visible = document.querySelectorAll('.ctcae-term:not(.hidden)').length;
    return visible;
  });
  check('ctcae search en', ctcaeHit >= 1, `visible terms: ${ctcaeHit}`);

  // 3.1b ctcae search in zh chars (en mode haystack includes zh)
  await page.evaluate(() => { const i = document.querySelector('#ctcae-search-input'); i.value = ''; i.dispatchEvent(new Event('input')); });
  await page.type('#ctcae-search-input', '贫血');
  await new Promise((r) => setTimeout(r, 300));
  const ctcaeHitZh = await page.evaluate(() => document.querySelectorAll('.ctcae-term:not(.hidden)').length);
  check('ctcae search en-mode zh term', ctcaeHitZh >= 1, `visible: ${ctcaeHitZh}`);

  // 3.2 tmf-checker: check an item, progress updates, generate report in EN
  await page.goto(`${BASE}/tmf-checker.html?lang=en`, { waitUntil: 'networkidle0' });
  await page.evaluate(() => {
    const box = document.querySelector('.chk-box');
    box.click();
    box.dispatchEvent(new Event('change', { bubbles: true }));
  });
  await page.click('#chk-report-btn');
  await new Promise((r) => setTimeout(r, 400));
  const chkReport = await page.evaluate(() => ({
    title: document.querySelector('#gap-report h2').textContent.trim(),
    visible: !document.getElementById('gap-report').hidden,
    progress: document.getElementById('chk-progress').textContent.trim(),
  }));
  check('tmf-checker report en', chkReport.visible && /Self-Check Report/.test(chkReport.title), JSON.stringify(chkReport));

  // 3.3 pd decision tree: answer major path in EN
  await page.goto(`${BASE}/pd-decision-tree.html?lang=en`, { waitUntil: 'networkidle0' });
  await page.evaluate(() => pdResult('major'));
  const pdTitle = await page.evaluate(() => document.getElementById('pd-result-title').textContent);
  check('pd result en', /Major Deviation Path/.test(pdTitle), pdTitle);

  // 3.4 glossary zh column hidden in EN, visible in ZH
  await page.goto(`${BASE}/glossary.html?lang=en`, { waitUntil: 'networkidle0' });
  const glEn = await page.evaluate(() => {
    const th = document.querySelector('.gl-table th:nth-child(3)');
    return getComputedStyle(th).display;
  });
  check('glossary zh col hidden in EN', glEn === 'none', 'display: ' + glEn);

  // 3.5 template page runtime toggle en→zh→en
  await page.goto(`${BASE}/template-monitoring-visit-report.html?lang=en`, { waitUntil: 'networkidle0' });
  const tplTitles = await page.evaluate(() => {
    const el = document.getElementById('tpl-content');
    const before = el.querySelector('h2').textContent.trim();
    window.I18N.setLang('zh');
    const zh = el.querySelector('h2').textContent.trim();
    window.I18N.setLang('en');
    const back = el.querySelector('h2').textContent.trim();
    return { before, zh, back };
  });
  check('template toggle', /^\d/.test(tplTitles.before) && /[一-鿿]/.test(tplTitles.zh) && tplTitles.back === tplTitles.before, JSON.stringify(tplTitles));

  // 3.6 audit-findings filter + search in EN
  await page.goto(`${BASE}/audit-findings.html?lang=en`, { waitUntil: 'networkidle0' });
  await page.select('#af-chapter', 'ch5');
  await new Promise((r) => setTimeout(r, 300));
  const afRows = await page.evaluate(() => document.querySelectorAll('#af-preview tbody tr').length);
  const afStats = await page.evaluate(() => document.getElementById('af-stats').textContent.trim());
  check('audit chapter filter en', afRows > 0 && /Total \d+/.test(afStats), `${afRows} rows, ${afStats}`);

  // 3.7 edl-generator dept filter in EN
  await page.goto(`${BASE}/edl-generator.html?lang=en`, { waitUntil: 'networkidle0' });
  await page.select('#edl-dept', 'safety__c');
  await new Promise((r) => setTimeout(r, 300));
  const edlRows = await page.evaluate(() => document.querySelectorAll('#edl-preview tbody tr').length);
  check('edl dept filter en', edlRows > 0, `${edlRows} rows`);

  // 3.8 timeline dates computed
  await page.goto(`${BASE}/timeline-calendar.html?lang=en`, { waitUntil: 'networkidle0' });
  const tlRows = await page.evaluate(() => document.querySelectorAll('#tl-body tr').length);
  check('timeline rows', tlRows === 8, `${tlRows} rows`);

  // 3.9 regulation page body swap en→zh→en (generated .en.md twin)
  await page.goto(`${BASE}/gcp-2026.html?lang=en`, { waitUntil: 'networkidle0' });
  const regSwap = await page.evaluate(() => {
    const el = document.querySelector('.content-inner');
    const before = el.querySelector('h2').textContent.trim();
    window.I18N.setLang('zh');
    const zh = el.querySelector('h2').textContent.trim();
    window.I18N.setLang('en');
    const back = el.querySelector('h2').textContent.trim();
    return { before, zh, back };
  });
  check('gcp-2026 body swap', /^\d\./.test(regSwap.before) && /[一-鿿]/.test(regSwap.zh) && regSwap.back === regSwap.before, JSON.stringify(regSwap));

  // 3.10 cde ranking renders EN labels + top-N toggle stays lang-aware
  await page.goto(`${BASE}/cde-trials.html?lang=en`, { waitUntil: 'networkidle0' });
  const cdeRank = await page.evaluate(() => {
    const first = document.querySelector('#viz-ranking .viz-tick').textContent.trim();
    const toggle = document.getElementById('rank-toggle');
    toggle.value = '10';
    toggle.dispatchEvent(new Event('change'));
    return { first, rows: document.querySelectorAll('#viz-ranking rect').length };
  });
  check('cde ranking en', cdeRank.first === 'Oncology' && cdeRank.rows === 10, JSON.stringify(cdeRank));

  // 3.11 whitepaper embedded CDE charts: baked EN labels, zh body has zh charts
  await page.goto(`${BASE}/whitepaper.html?lang=en`, { waitUntil: 'networkidle0' });
  const wpCharts = await page.evaluate(() => {
    const svgs = document.querySelectorAll('.content-inner svg.viz-svg');
    const svgText = Array.from(svgs).map((s) => s.textContent).join(' ');
    const subs = Array.from(document.querySelectorAll('.content-inner .viz-chart-sub')).map((s) => s.textContent).join(' ');
    return { n: svgs.length, enSub: /Biological products/.test(subs), svgZh: /[一-鿿]/.test(svgText) };
  });
  check('whitepaper charts en', wpCharts.n === 2 && wpCharts.enSub && !wpCharts.svgZh, JSON.stringify(wpCharts));

  // 3.12 visit calculator: schedule rows + dates in EN
  await page.goto(`${BASE}/visit-calculator.html?lang=en`, { waitUntil: 'networkidle0' });
  const vcRes = await page.evaluate(() => {
    const set = (id, v) => { const el = document.getElementById(id); el.value = v; };
    set('vc-c1d1', '2026-08-15'); set('vc-cycle', '21'); set('vc-window', '3');
    set('vc-cycles', '6'); set('vc-screen', '28'); set('vc-fu', '30');
    vcCalc();
    const first = document.querySelector('#vc-body tr td').textContent.trim();
    const dates = Array.from(document.querySelectorAll('#vc-body td.vc-date')).map(td => td.textContent.trim()).join('|');
    return { rows: document.querySelectorAll('#vc-body tr').length, first, dates };
  });
  check('visit calc rows', vcRes.rows === 8 && /Screening visit/.test(vcRes.first), JSON.stringify(vcRes));
  check('visit calc dates', /2026-07-18/.test(vcRes.dates) && /2026-09-26/.test(vcRes.dates) && /2026-12-28/.test(vcRes.dates), vcRes.dates);

  // 3.13 sample size calculator: proportions default + means mode, EN
  await page.goto(`${BASE}/sample-size-calculator.html?lang=en`, { waitUntil: 'networkidle0' });
  const ssProp = await page.evaluate(() => {
    const set = (id, v) => { const el = document.getElementById(id); el.value = v; };
    set('ss-p1', '0.8'); set('ss-p2', '0.6'); set('ss-ratio', '1'); set('ss-dropout', '0');
    ssCalc();
    return document.getElementById('ss-out').textContent.replace(/\s+/g, ' ');
  });
  check('sample size prop', /n₁ = 82/.test(ssProp) && /n₂ = 82/.test(ssProp) && /Total sample size: 164/.test(ssProp), ssProp.slice(0, 160));
  const ssMean = await page.evaluate(() => {
    document.querySelector('input[name="ss-mode"][value="mean"]').click();
    const set = (id, v) => { const el = document.getElementById(id); el.value = v; };
    set('ss-delta', '1'); set('ss-sigma', '3');
    ssCalc();
    return document.getElementById('ss-out').textContent.replace(/\s+/g, ' ');
  });
  check('sample size mean', /n₁ = 142/.test(ssMean) && /n₂ = 142/.test(ssMean), ssMean.slice(0, 160));

  // 3.14 footer structure: 4 columns (products/resources/tools/links), not nested
  await page.goto(`${BASE}/`, { waitUntil: 'networkidle0' });
  const foot = await page.evaluate(() => {
    const grid = document.querySelector('.footer-grid');
    const cols = grid.querySelectorAll(':scope > .footer-col');
    const counts = Array.from(cols).map(c => c.querySelectorAll('a').length);
    const nested = grid.querySelectorAll('.footer-col .footer-col').length;
    return { colCount: cols.length, counts, nested };
  });
  check('footer structure', foot.colCount === 4 && JSON.stringify(foot.counts) === '[3,8,9,6]' && foot.nested === 0, JSON.stringify(foot));

  // 3.15 annex-c body swap + full 52-entry table present in both languages
  await page.goto(`${BASE}/annex-c.html?lang=en`, { waitUntil: 'networkidle0' });
  const annexc = await page.evaluate(() => {
    const el = document.querySelector('.content-inner');
    const before = el.querySelector('h2').textContent.trim();
    const tables = Array.from(document.querySelectorAll('.content-inner .content-table'));
    const mainRows = tables.length ? tables[tables.length - 1].querySelectorAll('tbody tr').length : 0;
    const hasMap = mainRows ? tables[tables.length - 1].textContent : '';
    window.I18N.setLang('zh');
    const zh = el.querySelector('h2').textContent.trim();
    window.I18N.setLang('en');
    const back = el.querySelector('h2').textContent.trim();
    return { before, zh, back, tables: tables.length, mainRows, hasMap };
  });
  check('annex-c body swap',
    /^\d\./.test(annexc.before) && /[一-鿿]/.test(annexc.zh) && annexc.back === annexc.before,
    JSON.stringify({ before: annexc.before, zh: annexc.zh }));
  check('annex-c 52-entry table',
    annexc.tables === 3 && annexc.mainRows === 62 && /02\.01\.01/.test(annexc.hasMap) && /Investigator's Brochure/.test(annexc.hasMap),
    `tables ${annexc.tables}, rows ${annexc.mainRows}`);

  // 3.16 retention body swap + quick-reference table in both languages
  await page.goto(`${BASE}/retention.html?lang=en`, { waitUntil: 'networkidle0' });
  const retention = await page.evaluate(() => {
    const el = document.querySelector('.content-inner');
    const before = el.querySelector('h2').textContent.trim();
    const text = el.textContent;
    const enOk = /5 years after marketing approval/.test(text) && /whichever is the longest/.test(text) && /Art\. 28\(2\)/.test(text);
    window.I18N.setLang('zh');
    const zhText = el.textContent;
    const zh = el.querySelector('h2').textContent.trim();
    window.I18N.setLang('en');
    const back = el.querySelector('h2').textContent.trim();
    return { before, zh, back, enOk, zhOk: /获批上市后 5 年/.test(zhText) && /以较长者为准/.test(zhText) };
  });
  check('retention body swap',
    /^\d\./.test(retention.before) && /[一-鿿]/.test(retention.zh) && retention.back === retention.before,
    JSON.stringify({ before: retention.before, zh: retention.zh }));
  check('retention quick-ref table', retention.enOk && retention.zhOk, JSON.stringify(retention));

  // 3.17 data governance template pack: body swap + companion links to audit-trail
  await page.goto(`${BASE}/template-data-correction-sop.html?lang=en`, { waitUntil: 'networkidle0' });
  const dgPack = await page.evaluate(() => {
    const el = document.getElementById('tpl-content');
    const before = el.querySelector('h2').textContent.trim();
    const enOk = /Data Correction Log/.test(el.textContent) && /written PI consent/.test(el.textContent);
    window.I18N.setLang('zh');
    const zhOk = /数据更正记录表/.test(el.textContent) && /PI 书面同意/.test(el.textContent);
    const zh = el.querySelector('h2').textContent.trim();
    window.I18N.setLang('en');
    const back = el.querySelector('h2').textContent.trim();
    return { before, zh, back, enOk, zhOk };
  });
  check('dg pack body swap',
    /^[1-9]\./.test(dgPack.before) && /[一-鿿]/.test(dgPack.zh) && dgPack.back === dgPack.before,
    JSON.stringify({ before: dgPack.before, zh: dgPack.zh }));
  check('dg pack content', dgPack.enOk && dgPack.zhOk, JSON.stringify(dgPack));

  // 3.18 templates index shows the data governance section
  await page.goto(`${BASE}/templates.html?lang=en`, { waitUntil: 'networkidle0' });
  const tplDg = await page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('a[href^="template-"]')).map(a => a.getAttribute('href'));
    const title = Array.from(document.querySelectorAll('h2')).map(h => h.textContent.trim()).join(' | ');
    return { hasNew: links.includes('template-metadata-review-sop.html') && links.includes('template-data-correction-sop.html') && links.includes('template-access-register.html'), title };
  });
  check('templates index dg section', tplDg.hasNew && /Data Governance Template Pack/.test(tplDg.title), tplDg.title.slice(0, 80));

  // 3.19 safety reporting body swap + timeline table in both languages
  await page.goto(`${BASE}/safety-reporting.html?lang=en`, { waitUntil: 'networkidle0' });
  const safety = await page.evaluate(() => {
    const el = document.querySelector('.content-inner');
    const before = el.querySelector('h2').textContent.trim();
    const text = el.textContent;
    const enOk = /7 days/.test(text) && /whichever/i.test(text) === false && /Expedited report/.test(text) && /3\.13\.2\(c\)/.test(text);
    window.I18N.setLang('zh');
    const zhText = el.textContent;
    const zh = el.querySelector('h2').textContent.trim();
    window.I18N.setLang('en');
    const back = el.querySelector('h2').textContent.trim();
    return { before, zh, back, enOk, zhOk: /获知后立即/.test(zhText) && /SUSAR 快速报告/.test(zhText) && /第二十六条/.test(zhText) };
  });
  check('safety body swap',
    /^\d\./.test(safety.before) && /[一-鿿]/.test(safety.zh) && safety.back === safety.before,
    JSON.stringify({ before: safety.before, zh: safety.zh }));
  check('safety timeline table', safety.enOk && safety.zhOk, JSON.stringify(safety));

  // ---------- 4. language switch via button on one page ----------
  console.log('\n== 4. lang toggle button ==');
  await page.goto(`${BASE}/templates.html`, { waitUntil: 'networkidle0' });
  // 强制 zh 起步；注意此前测试的 syncLangURL 会把 URL 改成 ?lang=en，
  // 需重新导航到干净 URL 让 localStorage 生效（URL 参数优先级最高）
  await page.evaluate(() => localStorage.setItem('vivarcus-lang', 'zh'));
  await page.goto(`${BASE}/templates.html`, { waitUntil: 'networkidle0' });
  const before = await page.evaluate(() => document.querySelector('h1').textContent.trim());
  await page.click('[data-lang-toggle]');
  await new Promise((r) => setTimeout(r, 400));
  const after = await page.evaluate(() => document.querySelector('h1').textContent.trim());
  check('toggle button zh→en', before === '临床运营模板库' && after === 'Clinical Operations Template Library', before + ' -> ' + after);

  await browser.close();
  console.log(`\n==== RESULT: ${results.length} checks, ${failures} failures ====`);
  process.exit(failures ? 1 : 0);
})().catch((e) => { console.error('SUITE ERROR:', e); process.exit(2); });
