# Gera as 4 páginas de cada problema (joanete.html, haglund.html, tendao-de-aquiles.html, entorse-de-tornozelo.html).
# Os textos médicos vêm dos MESMOS lugares da página principal (TXT e PARTS do ctrl_v3.js, cards e perguntas do head_v3.html),
# já revisados pela Dra. Larissa: mudou lá, muda aqui no próximo build. Só os títulos das seções e o resumo de cada página são daqui.
import datetime, html, json, re

REVISADO = '2026-11-12'   # data da revisão médica dos textos pela Dra. Larissa: trocar quando ela revisar de novo

PAGINAS = [
    dict(slug='joanete', cond='joanete', card='Joanete', h1='Joanete', sub='hálux valgo',
         title='Joanete: avaliação e cirurgia minimamente invasiva', img='{{IMG_PE_CIMA}}', alt='Pé com joanete visto de cima',
         faq=[0, 1, 4], dor='Calombo na lateral do dedão, que dói no sapato', cuidado=True),
    dict(slug='haglund', cond='haglund', card='Haglund', h1='Deformidade de Haglund', sub='dor atrás do calcanhar',
         title='Deformidade de Haglund: dor atrás do calcanhar', img='{{IMG_PE_LADO}}', alt='Pé visto de lado, com o calcanhar à esquerda',
         faq=[2, 4], dor='Calombo atrás do calcanhar, onde o sapato encosta', oque=2, dentro=[0, 1]),
    dict(slug='tendao-de-aquiles', cond='aquiles', card='Tendão de Aquiles', h1='Tendão de Aquiles', sub='ruptura do tendão',
         title='Ruptura do tendão de Aquiles', img='{{IMG_PE_LADO}}', alt='Pé visto de lado, com o tendão atrás do tornozelo',
         faq=[2, 4], dor=None),   # o texto revisado fala de ruptura; o sintoma da lista é de tendinite
    dict(slug='entorse-de-tornozelo', cond='tornozelo', card='Tornozelo', h1='Entorse de tornozelo', sub='ligamentos e tornozelo que falseia',
         title='Entorse de tornozelo e tornozelo que falseia', img='{{IMG_PE_LADO}}', alt='Pé visto de lado, com o tornozelo',
         faq=[3, 4], dor='Torceu o pé e semanas depois ainda incha', cuidado=True),
]

CSS_PAG = '''
/* páginas de cada problema */
.ph{background:var(--brand-deep);color:#fff;position:relative;overflow:hidden}
.ph::after{content:"";position:absolute;inset:0;background:radial-gradient(80% 90% at 85% 40%,rgba(114,198,162,.14),transparent 60%);pointer-events:none}
.ph .wrap{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:clamp(1.2rem,5vw,4rem);align-items:end;padding-top:clamp(8.5rem,17vh,11rem);padding-bottom:clamp(2.4rem,6vw,4rem)}
.ph .caps{color:var(--brand-lite)}
.ph h1{color:#fff;font-size:clamp(2.5rem,7vw,5rem);line-height:.98;margin:.9rem 0 .5rem}
.ph h1 small{display:block;font-family:var(--sans);font-stretch:100%;font-weight:500;font-size:clamp(1rem,2.2vw,1.25rem);letter-spacing:0;color:var(--brand-lite);margin-top:.6rem}
.ph .lead{color:rgba(255,255,255,.86);font-size:1.1rem;max-width:36rem;margin:1rem 0 1.4rem}
.ph .acts{display:flex;flex-wrap:wrap;align-items:center;gap:.8rem 1.4rem}
.ph .more{color:#fff;font-weight:600;font-size:.95rem;text-decoration:none;border-bottom:1.5px solid currentColor;padding-bottom:1px}
.ph .more:hover{color:var(--brand-lite)}
.ph figure{margin:0;width:clamp(8rem,22vw,17rem);aspect-ratio:3/4;border-radius:var(--r-film);overflow:hidden;background:radial-gradient(120% 90% at 30% 20%,var(--film-2),var(--film) 70%);border:1px solid rgba(255,255,255,.14);box-shadow:0 30px 60px -24px rgba(0,0,0,.6)}
.ph figure img{width:100%;height:100%;object-fit:contain;object-position:50% 70%;display:block}
.ph figure img.lado{object-fit:cover;object-position:0 100%;transform:scale(1.7);transform-origin:28% 96%}   /* foto de lado: o pé fica embaixo, à esquerda; amplia nele */
.ph .crumbs{font-family:var(--mono);font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.6)}
.ph .crumbs a{color:inherit}
.art .wrap{display:grid;grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr);gap:clamp(1.2rem,5vw,4.5rem);padding-block:var(--space) 0}
.art section{display:contents}
.art h2{font-size:clamp(1.5rem,3.2vw,2.2rem);margin:0}
.art .txt{max-width:40rem;color:var(--ink-2);font-size:1.05rem}
.art .txt p{margin:0 0 1rem}
.art .txt .nota{font-size:.92rem;color:var(--ink-3)}
.obs{display:grid;grid-template-columns:repeat(auto-fill,minmax(14rem,1fr));gap:.8rem;margin:0;max-width:44rem}
.obs div{background:var(--card);border:1px solid var(--rule);border-radius:var(--r);padding:1rem 1.1rem}
.obs dt{font-family:var(--display);font-stretch:125%;font-weight:600;color:var(--brand-deep);font-size:1.05rem}
.obs dt small{display:block;font-family:var(--mono);font-stretch:100%;font-weight:500;font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;color:var(--brand);margin-top:.2rem}
.obs dd{margin:.5rem 0 0;color:var(--ink-2);font-size:.94rem}
.obs dd b{color:var(--ink);font-weight:600}
.pag-faq{padding-top:var(--space)}
.outros .wrap{padding-block:0 var(--space)}
.outros ul{list-style:none;padding:0;margin:1rem 0 0;display:flex;flex-wrap:wrap;gap:.6rem}
.outros a{display:inline-block;border:1.5px solid var(--brand-deep);border-radius:999px;padding:.6rem 1.1rem;text-decoration:none;color:var(--brand-deep);font-weight:600;font-size:.92rem}
.outros a:hover{background:var(--brand-deep);color:#fff}
.pcta{background:var(--brand-deep);color:#fff}
.pcta .wrap{padding-block:clamp(2.6rem,6vw,4rem);display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1.2rem}
.pcta h2{color:#fff;font-size:clamp(1.6rem,4vw,2.4rem);margin:0}.pcta h2 em{color:var(--brand-lite)}
.pcta p{margin:.5rem 0 0;color:rgba(255,255,255,.75)}
@media (max-width:860px){.art .wrap{grid-template-columns:minmax(0,1fr);gap:.8rem}.art h2{margin-top:1.4rem}}
.obs{min-width:0}
@media (max-width:520px){.obs{grid-template-columns:minmax(0,1fr)}}
@media (max-width:520px){.ph .wrap{grid-template-columns:1fr}.ph figure{width:9rem;justify-self:end;margin-top:-.5rem}}
'''

def _js_strings(block):
    return [s for s in re.findall(r"'((?:[^'\\]|\\.)*)'", block)]

def dados(src_ctrl, src_head):
    txt = {}
    for c in ('joanete', 'haglund', 'aquiles', 'tornozelo'):
        m = re.search(c + r":\{name:'[^']*',steps:\[(.*?)\]\]\}", src_ctrl, flags=re.S)
        steps = re.findall(r"\[('(?:[^'\\]|\\.)*'(?:,'(?:[^'\\]|\\.)*')*)\]", m.group(1) + ']')   # o ']]}' do fim engoliu o ']' da última etapa
        txt[c] = [_js_strings(s) for s in steps]
        assert len(txt[c]) == 5, c
    parts = {k: _js_strings(v) for k, v in re.findall(r"\n  (\w+):\[('[^\n]*')\]", src_ctrl.split('const PARTS=')[1].split('};')[0])}
    plist = {k: re.findall(r"'(\w+)'", v) for k, v in re.findall(r"(\w+):\[([^\]]*)\]", src_ctrl.split('const PARTLIST=')[1].split('};')[0])}
    cards = dict(re.findall(r'<h3>([^<]+)</h3><p>(.*?)</p>', src_head.split('id="trata"')[1].split('class="common"')[0]))
    faq = re.findall(r'<details[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>', src_head.split('id="perguntas"')[1].split('</section>')[0])
    cuidado = re.search(r'<h2>Primeiro, <em>sem cirurgia.</em></h2>\s*<p>(.*?)</p>', src_head).group(1)
    return txt, parts, plist, cards, faq, cuidado

def gerar(src_head, src_ctrl, img_url, URL, logo_url, fav_v):
    txt, parts, plist, cards, faq, cuidado = dados(src_ctrl, src_head)
    css = re.search(r'<style>(.*?)</style>', src_head, flags=re.S).group(1)
    links = ''.join(l + '\n' for l in src_head.splitlines() if l.startswith('<link '))
    header = re.search(r'<header class="top">.*?</header>', src_head, flags=re.S).group(0)
    header = header.replace('href="#inicio"', 'href="./"').replace('href="#', 'href="./#').replace('{{IMG_LOGO}}', logo_url)
    cookies = re.search(r'<div class="cookies" id="cookies".*?</div>\n</div>', src_head, flags=re.S).group(0)
    footer = re.search(r'<footer><div class="wrap">.*?</footer>', src_head, flags=re.S).group(0)
    ga = '<script>' + src_ctrl.rsplit('<script>', 1)[1]
    hoje = datetime.date.today().isoformat()
    out = []
    for p in PAGINAS:
        c = p['cond']; s = txt[c]
        tira = lambda x: x.replace(' Role para ver por dentro.', '')
        o_que = [tira(s[p.get('oque', 0)][0])]
        dentro = [tira(s[i][0]) for i in p.get('dentro', [1, 2])]
        url = URL + p['slug'] + '.html'
        title = p['title'] + ' · Dra. Larissa Silva, ortopedista no Rio de Janeiro'
        desc = html.unescape(re.sub('<[^>]+>', '', o_que[0] + ' ' + cards[p['card']]))
        lead = cards[p['card']]   # o 'o que é' já vem logo abaixo: aqui só o que eu faço
        obs = ''.join('<div><dt>%s<small>%s</small></dt><dd>%s</dd><dd><b>Na consulta eu observo:</b> %s</dd></div>' % (parts[k][0], parts[k][1], parts[k][2], parts[k][3]) for k in plist[c])
        perg = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', faq[j][0], faq[j][1]) for i, j in enumerate(p['faq']))
        outros = ''.join('<li><a href="%s.html">%s</a></li>' % (q['slug'], q['h1']) for q in PAGINAS if q is not p)
        par = lambda xs, nota=True: ''.join('<p%s>%s</p>' % (' class="nota"' if (nota and i > 0) else '', x) for i, x in enumerate(xs))
        ld = {'@context': 'https://schema.org', '@type': 'MedicalWebPage', 'name': p['title'], 'url': url, 'inLanguage': 'pt-BR', 'lastReviewed': REVISADO,
              'about': {'@type': 'MedicalCondition', 'name': p['h1']},
              'author': {'@type': 'Physician', 'name': 'Dra. Larissa Silva', 'url': URL},
              'reviewedBy': {'@type': 'Physician', 'name': 'Dra. Larissa Silva', 'url': URL}}
        doc = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#113358">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="img/web/favicon.png?v={fav_v}">
<meta property="og:type" content="article"><meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{html.escape(p['title'])} · Dra. Larissa Silva">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{URL}img/web/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{links}<style>{css}{CSS_PAG}
:root{{color-scheme:light}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}
</style>
</head>
<body>
{header}

<section class="ph"><div class="wrap">
  <div>
    <span class="crumbs"><a href="./">Início</a> · Pé e tornozelo</span>
    <h1>{p['h1']}<small>{p['sub']}</small></h1>
    <p class="lead">{lead}</p>
    <div class="acts"><a class="btn primary" href="./#agendar">Agendar avaliação</a><a class="more" href="./#esquema-{c}">Ver no esquema →</a></div>
  </div>
  <figure><img{' class="lado"' if p['img']=='{{IMG_PE_LADO}}' else ''} src="{img_url[p['img']]}" alt="{p['alt']}" width="569" height="852"></figure>
</div></section>

<main class="art"><div class="wrap">
  <section><h2>O que é</h2><div class="txt">{par(o_que)}{('<p class="nota">Costuma aparecer assim: “' + p['dor'] + '”.</p>') if p['dor'] else ''}</div></section>
  <section><h2>Por dentro</h2><div class="txt">{par(dentro, False)}</div></section>
  <section><h2>Tratamento</h2><div class="txt">{('<p>' + cuidado + '</p>') if p.get('cuidado') else ''}{par(s[3])}</div></section>
  <section><h2>Depois</h2><div class="txt">{par(s[4])}</div></section>
  <section><h2>O que eu observo na consulta</h2><dl class="obs">{obs}</dl></section>
</div></main>

<section class="faq pag-faq"><div class="wrap">
  <div><span class="caps">Perguntas</span><h2 style="margin-top:.7rem">O que todo mundo <em>pergunta.</em></h2></div>
  <div>{perg}</div>
</div></section>

<section class="outros"><div class="wrap">
  <span class="caps">Outros problemas que eu trato</span>
  <ul>{outros}</ul>
</div></section>

<section class="pcta"><div class="wrap">
  <div><h2>Traga o sapato que <em>mais dói.</em></h2><p>Rua General Venâncio Flores, 184 · Leblon · Rio de Janeiro</p></div>
  <a class="btn primary" href="./#agendar">Agendar avaliação</a>
</div></section>

{cookies}

{footer}
{ga}
</body>
</html>
'''
        open(p['slug'] + '.html', 'w', encoding='utf-8').write(doc)
        out.append(url)
    return out
