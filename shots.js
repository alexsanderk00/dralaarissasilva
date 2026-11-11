const { chromium } = require('playwright');
const { spawn } = require('child_process');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const srv = spawn('python3', ['-m', 'http.server', '8791'], { cwd: __dirname, stdio: 'ignore' }); await sleep(900);
  const b = await chromium.launch(); const errs = []; const mode = process.argv[2] || 'film';
  const hook = p => { p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); };
  if (mode === 'film') {
    const p = await b.newPage({ viewport: { width: 1360, height: 820 }, deviceScaleFactor: 1 }); hook(p);
    await p.goto('http://127.0.0.1:8791/test.html'); await sleep(900);
    const top = await p.evaluate(() => document.getElementById('story').offsetTop);
    await p.evaluate(y => scrollTo(0, y + 5), top); await sleep(300);
    const jobs = JSON.parse(process.argv[3]);   // [[cond, s, w|null, nome], ...]
    for (const [c, s, w, name] of jobs) {
      await p.evaluate(([c, s, w]) => window.__esquema.set(c, s, w), [c, s, w]); await sleep(450);
      await (await p.$('#film')).screenshot({ path: `prints/${name}.png` });
    }
  } else {
    const [w, h] = mode === 'mobile' ? [390, 780] : [1360, 820];
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 }); hook(p);
    await p.goto('http://127.0.0.1:8791/test.html'); await sleep(900);
    await p.screenshot({ path: `prints/${mode}-full.png` });
    const top = await p.evaluate(() => document.getElementById('story').offsetTop);
    const total = await p.evaluate(() => document.getElementById('story').offsetHeight - innerHeight);
    let i = 0; for (const f of [0.02, 0.13, 0.23, 0.47, 0.75, 0.97]) { await p.evaluate(y => scrollTo(0, y), top + total * f); await sleep(1900); await p.screenshot({ path: `prints/${mode}-story${i++}.png` }); }
    const ys = await p.evaluate(() => ['cuidado', 'trata', 'videos', 'sobre', 'perguntas', 'agendar'].map(id => document.getElementById(id).offsetTop));
    i = 0; for (const y of ys) { await p.evaluate(y => scrollTo(0, y), y); await sleep(1300); await p.screenshot({ path: `prints/${mode}-sec${i++}.png` }); }
    const ty = await p.evaluate(() => document.querySelector('.common').getBoundingClientRect().top + scrollY - 20); await p.evaluate(y => scrollTo(0, y), ty); await sleep(1300); await p.screenshot({ path: `prints/${mode}-common.png` });
    console.log('overflow-x:', await p.evaluate(() => document.documentElement.scrollWidth - innerWidth));
  }
  console.log('erros:', errs.length ? errs : 'nenhum'); await b.close(); srv.kill();
})();
