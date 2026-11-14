# Gera as 4 páginas de cada problema (joanete.html, haglund.html, tendao-de-aquiles.html, entorse-de-tornozelo.html).
# Os textos médicos vêm dos MESMOS lugares da página principal (TXT e PARTS do ctrl_v3.js, cards e perguntas do head_v3.html),
# já revisados pela Dra. Larissa: mudou lá, muda aqui no próximo build. Só os títulos das seções e o resumo de cada página são daqui.
import datetime, html, json, re

REVISADO = '2026-11-12'   # data da revisão médica dos textos pela Dra. Larissa: trocar quando ela revisar de novo

PAGINAS = [
    dict(slug='joanete', desc='Joanete (hálux valgo): o que é, quando tratar sem cirurgia e como é a cirurgia minimamente invasiva. Dra. Larissa Silva, ortopedista no Leblon, Rio.', cond='joanete', card='Joanete', h1='Joanete', sub='hálux valgo',
         title='Joanete: avaliação e cirurgia minimamente invasiva', img='{{IMG_PE_CIMA}}', alt='Pé com joanete visto de cima',
         faq=[0, 1, 4], dor='Calombo na lateral do dedão, que dói no sapato', cuidado=True,
         en=dict(desc='Bunion (hallux valgus): what it is, when to treat it without surgery and how minimally invasive surgery works. Dr. Larissa Silva, Rio de Janeiro.', h1='Bunion', sub='hallux valgus', title='Bunion: evaluation and minimally invasive surgery', alt='Foot with a bunion seen from above',
                 dor='A bump on the side of the big toe that hurts in shoes')),
    dict(slug='haglund', desc='Dor atrás do calcanhar, onde o sapato encosta: deformidade de Haglund, tratamento sem cirurgia e quando operar. Dra. Larissa Silva, Leblon, Rio.', cond='haglund', card='Haglund', h1='Deformidade de Haglund', sub='dor atrás do calcanhar',
         title='Deformidade de Haglund: dor atrás do calcanhar', img='{{IMG_PE_LADO}}', alt='Pé visto de lado, com o calcanhar à esquerda',
         faq=[2, 4], dor='Calombo atrás do calcanhar, onde o sapato encosta', oque=2, dentro=[1],   # a etapa 0 é o calcanhar normal visto por fora: não entra em "Por dentro"
         en=dict(desc='Pain at the back of the heel where the shoe rubs: Haglund’s deformity, non-surgical care and when surgery is considered. Dr. Larissa Silva, Rio.', h1='Haglund’s deformity', sub='pain at the back of the heel', title='Haglund’s deformity: pain at the back of the heel', alt='Foot seen from the side, heel on the left',
                 dor='A bump at the back of the heel, where the shoe rubs')),
    dict(slug='tendao-de-aquiles', desc='Ruptura do tendão de Aquiles: sintomas, tratamento com bota ou cirurgia e recuperação por fases. Dra. Larissa Silva, ortopedista no Leblon, Rio.', cond='aquiles', card='Tendão de Aquiles', h1='Tendão de Aquiles', sub='ruptura do tendão',
         title='Ruptura do tendão de Aquiles', img='{{IMG_PE_LADO}}', alt='Pé visto de lado, com o tendão atrás do tornozelo',
         faq=[2, 4], dor=None,   # o texto revisado fala de ruptura; o sintoma da lista é de tendinite
         en=dict(desc='Achilles tendon rupture: symptoms, treatment with a boot or surgery, and recovery in phases. Dr. Larissa Silva, orthopedic surgeon in Rio.', h1='Achilles tendon', sub='tendon rupture', title='Achilles tendon rupture', alt='Foot seen from the side, with the tendon behind the ankle', dor=None)),
    dict(slug='entorse-de-tornozelo', desc='Entorse de tornozelo e tornozelo que falseia: quando procurar avaliação, reabilitação e reparo do ligamento. Dra. Larissa Silva, Leblon, Rio.', cond='tornozelo', card='Tornozelo', h1='Entorse de tornozelo', sub='ligamentos e tornozelo que falseia',
         title='Entorse de tornozelo e tornozelo que falseia', img='{{IMG_PE_LADO}}', alt='Pé visto de lado, com o tornozelo',
         faq=[3, 4], dor='Torceu o pé e semanas depois ainda incha', cuidado=True,
         en=dict(desc='Ankle sprain and an ankle that gives way: when to get checked, rehabilitation and ligament repair. Dr. Larissa Silva, Rio de Janeiro.', h1='Ankle sprain', sub='ligaments and an ankle that gives way', title='Ankle sprain and an ankle that gives way', alt='Foot seen from the side, showing the ankle',
                 dor='Twisted the foot and weeks later it is still swollen')),
]

T = {
    'pt': dict(lang='pt-BR', locale='pt_BR', sufixo=' · Dra. Larissa Silva', og=' · Dra. Larissa Silva', inicio='Início', area='Pé e tornozelo',
               agendar='Agendar avaliação', ver='Ver no esquema →', oque='O que é', aparece='Costuma aparecer assim', dentro='Por dentro', trat='Tratamento',
               depois='Depois', obs='O que eu observo na consulta', observo='Na consulta eu observo:', perg='Perguntas', perg_h='O que todo mundo <em>pergunta.</em>',
               outros='Outros problemas que eu trato', cta='Traga o sapato que <em>mais dói.</em>', nome='Dra. Larissa Silva'),
    'en': dict(lang='en', locale='en_US', sufixo=' · Dr. Larissa Silva', og=' · Dr. Larissa Silva', inicio='Home', area='Foot and ankle',
               agendar='Book an appointment', ver='See it in the diagram →', oque='What it is', aparece='How it often shows up', dentro='Inside', trat='Treatment',
               depois='Afterwards', obs='What I look at in the visit', observo='In the visit I look at:', perg='Questions', perg_h='What everyone <em>asks.</em>',
               outros='Other problems I treat', cta='Bring the shoe that <em>hurts the most.</em>', nome='Dr. Larissa Silva'),
}

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
.ph figure img.lado{object-fit:cover;object-position:0 100%;transform:scale(1.7);transform-origin:28% 96%}
.ph figure img.lado.atras{transform:scale(1.55);transform-origin:4% 96%}   /* Haglund e Aquiles: o assunto é a parte de trás do calcanhar */   /* foto de lado: o pé fica embaixo, à esquerda; amplia nele */
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
@media (max-width:520px){.ph .wrap{grid-template-columns:minmax(0,1fr) auto;column-gap:1rem;align-items:center}.ph .wrap>div{display:contents}.ph .crumbs,.ph h1,.ph .lead{grid-column:1/-1}.ph .acts{grid-column:1;min-width:0;flex-direction:column;align-items:flex-start;gap:1.1rem}.ph .acts .btn{white-space:normal;text-align:center;max-width:100%}.ph figure{grid-column:2;width:clamp(6rem,28vw,8.5rem);justify-self:end;margin:0}}   /* celular: botões e foto lado a lado */
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
    cards = dict(re.findall(r'<a class="ico"[^>]*data-go="(\w+)"[^>]*>.*?<h3>[^<]+</h3><p>(.*?)</p>', src_head.split('id="trata"')[1].split('class="common"')[0], flags=re.S))   # chave = aba (vale nos dois idiomas)
    faq = re.findall(r'<details[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>', src_head.split('id="perguntas"')[1].split('</section>')[0])
    cuidado = re.search(r'<p>(.*?)</p>', src_head.split('id="cuidado"')[1]).group(1)   # 1º parágrafo da seção do cuidado
    return txt, parts, plist, cards, faq, cuidado

def gerar(src_head, src_ctrl, img_url, URL, logo_url, fav_v, lang='pt', pares=()):
    # lang='en': mesmos dados, com os textos do site passados por traducao_en.json; páginas em en/, arquivos na raiz (../)
    L = T[lang]; pre = '' if lang == 'pt' else '../'; pasta = '' if lang == 'pt' else 'en/'
    for pt, eng in pares:
        src_head = src_head.replace(pt, eng); src_ctrl = src_ctrl.replace(pt, eng)
    img_url = {k: pre + v for k, v in img_url.items()}; logo_url = pre + logo_url
    txt, parts, plist, cards, faq, cuidado = dados(src_ctrl, src_head)
    css = re.search(r'<style>(.*?)</style>', src_head, flags=re.S).group(1)
    links = ''.join(l + '\n' for l in src_head.splitlines() if l.startswith('<link '))
    header = re.search(r'<header class="top">.*?</header>', src_head, flags=re.S).group(0)
    header = header.replace('href="#inicio"', 'href="./"').replace('href="#', 'href="./#').replace('{{IMG_LOGO}}', logo_url)
    cookies = re.search(r'<div class="cookies" id="cookies".*?</div>\n</div>', src_head, flags=re.S).group(0).replace('href="privacidade.html"', 'href="' + pre + 'privacidade.html"')
    footer = re.search(r'<footer><div class="wrap">.*?</footer>', src_head, flags=re.S).group(0).replace('href="privacidade.html"', 'href="' + pre + 'privacidade.html"').replace('href="ortopedista-leblon', 'href="' + pre + 'ortopedista-leblon')
    ga = '<script>' + src_ctrl.rsplit('<script>', 1)[1]
    hoje = datetime.date.today().isoformat()
    import hashlib; og_v = hashlib.md5(open('img/web/og.jpg', 'rb').read()).hexdigest()[:8]   # mesma versão da prévia que o build.py gera
    csp = re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*>', src_head).group(0)   # mesma regra de segurança da página principal
    out = []
    for p in PAGINAS:
        c = p['cond']; s = txt[c]; X = dict(p, **p['en']) if lang == 'en' else p   # textos da página no idioma
        tira = lambda x: re.sub(r'\s*(Role para|Scroll to) [^.]*\.$', '', x)
        o_que = [tira(s[p.get('oque', 0)][0])]
        dentro = [tira(s[i][0]) for i in p.get('dentro', [1, 2])]
        url = URL + pasta + p['slug'] + '.html'
        url_pt = URL + p['slug'] + '.html'; url_en = URL + 'en/' + p['slug'] + '.html'
        title = X['title'] + L['sufixo']
        desc = X.get('desc') or html.unescape(re.sub('<[^>]+>', '', o_que[0] + ' ' + cards[c]))
        lead = cards[c]   # o 'o que é' já vem logo abaixo: aqui só o que eu faço
        obs = ''.join(('<div><dt>%s<small>%s</small></dt><dd>%s</dd><dd><b>' + L['observo'] + '</b> %s</dd></div>') % (parts[k][0], parts[k][1], parts[k][2], parts[k][3]) for k in plist[c])
        perg = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', faq[j][0], faq[j][1]) for i, j in enumerate(p['faq']))
        outros = ''.join('<li><a href="%s.html">%s</a></li>' % (q['slug'], (q['en']['h1'] if lang == 'en' else q['h1'])) for q in PAGINAS if q is not p)
        if lang == 'pt': outros += ''.join('<li><a href="%s.html">%s</a></li>' % (q['slug'], q['h1']) for q in NOVAS if q['revisado']) + '<li><a href="%s.html">Avaliação no Leblon</a></li>' % LEBLON['slug']
        LANG_EN = '<a class="lang" href="en/" hreflang="en" lang="en" aria-label="English version">EN</a>'
        cab = header.replace(LANG_EN, ('<a class="lang" href="en/' + p['slug'] + '.html" hreflang="en" lang="en" aria-label="English version">EN</a>') if lang == 'pt'
                             else ('<a class="lang" href="../' + p['slug'] + '.html" hreflang="pt-BR" lang="pt-BR" aria-label="Versão em português">PT</a>'))
        par = lambda xs, nota=True: ''.join('<p%s>%s</p>' % (' class="nota"' if (nota and i > 0) else '', x) for i, x in enumerate(xs))
        ld = {'@context': 'https://schema.org', '@type': 'MedicalWebPage', 'name': X['title'], 'url': url, 'inLanguage': L['lang'], 'lastReviewed': REVISADO,
              'about': {'@type': 'MedicalCondition', 'name': X['h1']},
              'author': {'@type': 'Physician', 'name': L['nome'], 'url': URL},
              'reviewedBy': {'@type': 'Physician', 'name': L['nome'], 'url': URL}}
        doc = f'''<!doctype html>
<html lang="{L['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{csp}
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#113358">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="pt-BR" href="{url_pt}"><link rel="alternate" hreflang="en" href="{url_en}"><link rel="alternate" hreflang="x-default" href="{url_pt}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="{pre}img/web/favicon.png?v={fav_v}"><link rel="apple-touch-icon" href="{pre}img/web/favicon.png?v={fav_v}">
<meta property="og:type" content="article"><meta property="og:locale" content="{L['locale']}">
<meta property="og:title" content="{html.escape(X['title'] + L['og'])}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{URL}img/web/og.jpg?v={og_v}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{links}<style>{css}{CSS_PAG}
:root{{color-scheme:light}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}
</style>
</head>
<body>
{cab}

<section class="ph"><div class="wrap">
  <div>
    <span class="crumbs"><a href="./">{L['inicio']}</a> · {L['area']}</span>
    <h1>{X['h1']}<small>{X['sub']}</small></h1>
    <p class="lead">{lead}</p>
    <div class="acts"><a class="btn primary" href="./#agendar">{L['agendar']}</a><a class="more" href="./#esquema-{c}">{L['ver']}</a></div>
  </div>
  <figure><img{(' class="lado atras"' if p['slug'] in ('haglund', 'tendao-de-aquiles') else ' class="lado"') if p['img']=='{{IMG_PE_LADO}}' else ''} src="{img_url[p['img']]}" alt="{X['alt']}" width="569" height="852"></figure>
</div></section>

<main class="art"><div class="wrap">
  <section><h2>{L['oque']}</h2><div class="txt">{par(o_que)}{('<p class="nota">' + L['aparece'] + ': “' + X['dor'] + '”.</p>') if X['dor'] else ''}</div></section>
  <section><h2>{L['dentro']}</h2><div class="txt">{par(dentro, False)}</div></section>
  <section><h2>{L['trat']}</h2><div class="txt">{('<p>' + cuidado + '</p>') if p.get('cuidado') else ''}{par(s[3])}</div></section>
  <section><h2>{L['depois']}</h2><div class="txt">{par(s[4])}</div></section>
  <section><h2>{L['obs']}</h2><dl class="obs">{obs}</dl></section>
</div></main>

<section class="faq pag-faq"><div class="wrap">
  <div><span class="caps">{L['perg']}</span><h2 style="margin-top:.7rem">{L['perg_h']}</h2></div>
  <div>{perg}</div>
</div></section>

<section class="outros"><div class="wrap">
  <span class="caps">{L['outros']}</span>
  <ul>{outros}</ul>
</div></section>

<section class="pcta"><div class="wrap">
  <div><h2>{L['cta']}</h2><p>Rua General Venâncio Flores, 184 · Leblon · Rio de Janeiro</p></div>
  <a class="btn primary" href="./#agendar">{L['agendar']}</a>
</div></section>

{cookies}

{footer}
{ga}
</body>
</html>
'''
        open(pasta + p['slug'] + '.html', 'w', encoding='utf-8').write(doc)
        out.append(url)
    return out


# ======================================================================================================
# Páginas novas (proposta Growth360, 13/11/2026)
# 1) Avaliação no Leblon: página para a busca "ortopedista pé e tornozelo Leblon", montada SÓ com textos já revisados
#    (Quem sou, ficha, "Como é o cuidado", lista de sintomas, perguntas, endereço). Texto novo: só títulos e chamadas.
# 2) Problemas da lista "O que mais aparece" que ainda não têm página: texto médico NOVO. Enquanto `revisado` for False,
#    a página sai em _rascunho/ (fora do git e da Vercel, com noindex) para a Dra. Larissa ler. Revisou? revisado=True:
#    a página vai para a raiz, entra no sitemap, nas listas "Outros problemas" e na página do Leblon.
# ======================================================================================================

REVISADO_NOVAS = '2026-11-13'   # aprovação da Dra. Larissa das páginas novas

NOVAS = [
    dict(slug='fascite-plantar', desc='Fascite plantar: dor embaixo do calcanhar ao pisar. Tratamento sem cirurgia e ondas de choque. Dra. Larissa Silva, ortopedista no Leblon, Rio de Janeiro.', h1='Fascite plantar', sub='dor embaixo do calcanhar', revisado=True, esq='fascite',
         title='Fascite plantar: dor embaixo do calcanhar ao pisar', img='{{IMG_PE_SOLA}}', alt='Sola do pé, do calcanhar aos dedos', wh=(1500, 2000),
         dor='Dor embaixo do calcanhar ao levantar da cama', faq=[2, 4],
         lead='Trato a dor embaixo do calcanhar quase sempre sem cirurgia: alongamento, calçado, palmilha e, quando indicado, ondas de choque.',
         oque=['A fáscia plantar é uma faixa firme que vai do calcanhar até a base dos dedos e sustenta o arco do pé. Com sobrecarga repetida, ela se desgasta e dói no ponto onde se prende ao calcanhar.'],
         aparece=['A dor é mais forte nos primeiros passos da manhã ou depois de ficar sentado, alivia um pouco ao andar e volta no fim do dia. É comum em quem passa muito tempo em pé, corre, ganhou peso ou usa calçado baixo e duro.',
                  'O esporão de calcâneo que aparece na radiografia pode acompanhar a fascite, mas não é ele que causa a dor.'],
         trat=['Na grande maioria dos casos, o tratamento é conservador: alongamento da panturrilha e da fáscia, calçado que amortece, palmilha, ajuste do treino e fisioterapia. Quando a dor persiste, a terapia por ondas de choque é uma opção.',
               'A melhora costuma ser gradual. A cirurgia é rara e fica para quem não melhora depois de um tratamento bem feito por vários meses.'],
         quando=['Procure avaliação se a dor dura mais de algumas semanas, se começou depois de uma pancada, se há dormência ou se dói também à noite, em repouso. Nesses casos, investigo outras causas.'],
         # ondas de choque: texto NOVO (14/11/2026), para a Dra. Larissa aprovar
         secoes=[('Ondas de choque', ['A terapia por ondas de choque aplica pulsos de energia sobre a pele, no ponto da dor, sem corte e sem ponto. O objetivo é estimular a cicatrização do tecido desgastado na origem da fáscia, no calcanhar.']),   # frase do curso SMBTOC: volta no dia 23/11/2026, a pedido do Alexsander
                 ('Como é a sessão', ['Você fica de barriga para baixo, na maca. Localizo o ponto da dor, passo um gel e apoio o aplicador na pele do calcanhar. A aplicação dura poucos minutos e é feita sem anestesia.',
                                      'Durante os pulsos é comum sentir incômodo no ponto da dor; a intensidade é ajustada ao longo da sessão. Depois, você sai andando. Por um ou dois dias, evite corrida e impacto. A região pode ficar vermelha, dolorida ou com pequenos roxos.',
                                      'Costumam ser algumas sessões, com cerca de uma semana entre elas. O número depende do seu caso.']),
                 ('Quando é indicada', ['É indicada quando a dor continua apesar de alongamento, calçado, palmilha e fisioterapia bem feitos. Não substitui esses cuidados: os exercícios continuam durante e depois das sessões.',
                                        'Nem todo mundo pode fazer. Gravidez, alterações da coagulação ou uso de anticoagulante, infecção ou tumor no local, entre outros casos, contraindicam. Avalio isso na consulta.',
                                        'A resposta varia de pessoa para pessoa e a melhora costuma ser gradual, nas semanas seguintes.'])]),
    dict(slug='neuroma-de-morton', desc='Dor na bola do pé, como pedrinha no sapato: neuroma de Morton e metatarsalgia, causas e tratamento. Dra. Larissa Silva, ortopedista no Leblon, Rio.', h1='Neuroma de Morton', sub='metatarsalgia · dor na bola do pé', revisado=True,
         title='Neuroma de Morton e metatarsalgia: dor na bola do pé', img='{{IMG_PE_SOLA}}', alt='Sola do pé, do calcanhar aos dedos', wh=(1500, 2000),
         dor='Dor na “bola” do pé, como pedrinha no sapato', faq=[4],
         lead='A dor na “bola” do pé tem várias causas. Investigo a causa e começo pelo calçado e pela palmilha.',
         oque=['Metatarsalgia é o nome geral da dor na “bola” do pé, a região de apoio logo atrás dos dedos. Uma das causas é o neuroma de Morton: um espessamento do nervo que passa entre os ossos, mais comum entre o terceiro e o quarto dedo.'],
         aparece=['Sensação de pedrinha ou de meia dobrada dentro do sapato, queimação, choque ou dormência que corre para os dedos. Piora com salto alto e bico fino e alivia ao tirar o sapato e massagear o pé.'],
         trat=['Começo pelo calçado: mais largo, de salto baixo e sola que amortece. Uma palmilha com apoio logo atrás da bola do pé tira a pressão do nervo e dos ossos. Fisioterapia e, em alguns casos, infiltração entram como opções.',
               'A cirurgia fica para quando a dor continua apesar desses cuidados.'],
         quando=['Dormência que não passa, dor que acorda à noite ou inchaço no peito do pé pedem avaliação, porque podem ter outra causa, como fratura por estresse.']),
    dict(slug='halux-rigido', desc='Hálux rígido: artrose e dor no dedão ao dobrar. Calçado, palmilha e, se preciso, cirurgia. Dra. Larissa Silva, ortopedista no Leblon, Rio de Janeiro.', h1='Hálux rígido', sub='artrose do dedão', revisado=True,
         title='Hálux rígido: artrose e dor no dedão', img='{{IMG_PE_SOLA}}', alt='Sola do pé, do calcanhar aos dedos', wh=(1500, 2000),
         dor='Dedão duro, que dói ao dobrar', faq=[4],
         lead='Dedão duro e dolorido não é joanete. Trato primeiro com calçado e palmilha e, se a dor continuar, avalio a cirurgia pelo grau do desgaste.',
         oque=['É o desgaste da articulação na base do dedão. A cartilagem afina, o osso forma bicos nas bordas e o dedão perde a capacidade de dobrar para cima.'],
         aparece=['Dor e rigidez no dedão ao andar, subir escada, agachar ou usar salto. Às vezes aparece um calombo em cima da articulação, que machuca no sapato. No joanete, o dedão desvia para o lado; no hálux rígido, ele fica duro.'],
         trat=['Calçado de sola mais rígida e bico alto, palmilha que limita o movimento do dedão, ajuste das atividades e fisioterapia aliviam muitos casos.',
               'Se a dor persiste, a cirurgia depende do grau do desgaste: da retirada dos bicos de osso, em alguns casos por técnica minimamente invasiva, até a fixação da articulação nos casos avançados.'],
         quando=['Procure avaliação se o dedão dói e endurece há semanas, se incha e fica vermelho de repente ou se a dor muda o seu jeito de pisar.']),
    dict(slug='pe-plano-do-adulto', desc='Pé plano do adulto: o arco que desaba e o tendão tibial posterior. Palmilha, fortalecimento e quando operar. Dra. Larissa Silva, Leblon, Rio.', h1='Pé plano do adulto', sub='o arco que desabou', revisado=True, esq='peplano',
         title='Pé plano do adulto: o arco que desabou', img='{{IMG_PE_LADO}}', alt='Pé visto de lado',
         dor='Arco que desabou, dor por dentro do tornozelo', faq=[4],
         lead='Quando o arco do pé desaba na vida adulta, na maioria das vezes há um tendão envolvido. Quanto antes avaliar, mais opções de tratamento sem cirurgia.',
         oque=['Muita gente tem pé plano desde a infância, sem dor. No adulto, o arco também pode desabar com o tempo, na maioria das vezes porque o tendão tibial posterior, que sustenta o arco por dentro do tornozelo, perde força.'],
         aparece=['Dor e inchaço por dentro do tornozelo, cansaço ao andar, o arco mais baixo de um lado só e o calcanhar desviando para fora. Em fases mais avançadas, a dor passa para a parte de fora do pé.'],
         trat=['No início, palmilha com apoio do arco, calçado firme, fortalecimento e fisioterapia controlam a dor e ajudam a frear a progressão.',
               'Quando o pé continua deformando ou doendo, a cirurgia é planejada caso a caso, conforme a rigidez e o estágio.'],
         quando=['Procure avaliação se o pé mudou de formato de um lado só, se a dor por dentro do tornozelo não passa ou se ficou difícil subir na ponta do pé. Quem tem diabetes e nota o pé quente, inchado e com o arco desabando de repente precisa de avaliação urgente.']),
]

LEBLON = dict(slug='ortopedista-leblon-pe-tornozelo',
              title='Ortopedista no Leblon · Pé e tornozelo · Dra. Larissa Silva',   # "Ortopedista de Pé e Tornozelo" não é área registrada no CFM: manter separado
              desc='Avaliação do pé e do tornozelo no Leblon, Rio, com a Dra. Larissa Silva, ortopedista formada pelo INTO. Presencial ou teleconsulta. Primeiro, sem cirurgia.')

def _casca(src_head, src_ctrl, pre, logo_url, home):
    # pedaços comuns: CSS, fontes, cabeçalho, aviso de cookies, rodapé, GA e regra de segurança da página principal
    css = re.search(r'<style>(.*?)</style>', src_head, flags=re.S).group(1)
    links = ''.join(l + '\n' for l in src_head.splitlines() if l.startswith('<link '))
    header = re.search(r'<header class="top">.*?</header>', src_head, flags=re.S).group(0)
    header = (header.replace('href="en/"', 'href="' + pre + 'en/"').replace('href="#inicio"', 'href="' + home + '"')
              .replace('href="#', 'href="' + home + '#').replace('{{IMG_LOGO}}', logo_url))
    cookies = re.search(r'<div class="cookies" id="cookies".*?</div>\n</div>', src_head, flags=re.S).group(0).replace('href="privacidade.html"', 'href="' + pre + 'privacidade.html"')
    footer = re.search(r'<footer><div class="wrap">.*?</footer>', src_head, flags=re.S).group(0).replace('href="privacidade.html"', 'href="' + pre + 'privacidade.html"').replace('href="ortopedista-leblon', 'href="' + pre + 'ortopedista-leblon')
    ga = '<script>' + src_ctrl.rsplit('<script>', 1)[1]
    csp = re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*>', src_head).group(0)
    import hashlib; og_v = hashlib.md5(open('img/web/og.jpg', 'rb').read()).hexdigest()[:8]
    return css, links, header, cookies, footer, ga, csp, og_v

CSS_NOVAS = '''
.art .txt ol.trail{margin-top:.4rem}
.art .txt .obs{margin-top:1rem}
.lst{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:.6rem;max-width:44rem}
.lst a,.lst span.it{display:block;height:100%;box-sizing:border-box;background:var(--card);border:1px solid var(--rule);border-radius:var(--r);padding:.85rem 1rem;text-decoration:none;color:var(--ink-2);font-size:.92rem}
.lst b{display:block;font-family:var(--display);font-stretch:125%;font-weight:600;color:var(--brand-deep);font-size:1rem;margin-bottom:.2rem}
.lst a:hover{border-color:var(--brand-deep)}
.lst a b::after{content:" →";color:var(--brand)}
.lst li,.art .txt .obs dd,.art .txt .obs li{text-align:start;hyphens:manual;-webkit-hyphens:manual}   /* cartões estreitos: justificado abre buracos entre as palavras */
.ph figure img.foto{object-fit:cover;object-position:50% 30%}
.rasc{background:#FFF4D6;color:#5A4300;font:600 .85rem/1.4 var(--sans);text-align:center;padding:.6rem 1rem;position:relative;z-index:60}
@media (max-width:520px){.lst{grid-template-columns:minmax(0,1fr)}}
'''

def _doc(csp, title, desc, url, fav_v, pre, og_v, ld, links, css, extra_head, cab, corpo, cookies, footer, ga, og_type='article', og_title=None):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{csp}
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#113358">
{extra_head}<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="{pre}img/web/favicon.png?v={fav_v}"><link rel="apple-touch-icon" href="{pre}img/web/favicon.png?v={fav_v}">
<meta property="og:type" content="{og_type}"><meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{html.escape(og_title or title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://dralaarissasilva.com.br/img/web/og.jpg?v={og_v}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{links}<style>{css}{CSS_PAG}{CSS_NOVAS}
:root{{color-scheme:light}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}
</style>
</head>
<body>
{cab}
{corpo}
{cookies}

{footer}
{ga}
</body>
</html>
'''

def _sintomas(src_head):
    # lista "O que mais aparece": [(sintoma, problema)], na ordem do site
    return re.findall(r'<button type="button" data-r="[^"]*"[^>]*><span class="q">(.*?)</span><span class="a">(.*?)</span></button>', src_head)

PAGINA_DO_PROBLEMA = {'Joanete': 'joanete', 'Entorse de tornozelo': 'entorse-de-tornozelo', 'Tendinite de Aquiles': 'tendao-de-aquiles', 'Deformidade de Haglund': 'haglund',
                      'Fascite plantar': 'fascite-plantar', 'Metatarsalgia e neuroma de Morton': 'neuroma-de-morton', 'Hálux rígido (artrose)': 'halux-rigido', 'Pé plano do adulto': 'pe-plano-do-adulto'}

def _pagina_de(problema):
    # problema da lista → página publicada (as 4 revisadas e as novas já revisadas); None se ainda não tem
    s = PAGINA_DO_PROBLEMA.get(problema)
    if s and any(n['slug'] == s and not n['revisado'] for n in NOVAS): return None
    return s

def gerar_novas(src_head, src_ctrl, img_url, URL, logo_url, fav_v):
    # problemas novos: revisados → raiz (vão para o sitemap); não revisados → _rascunho/ (noindex, fora do git e da Vercel)
    import os
    faq = re.findall(r'<details[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>', src_head.split('id="perguntas"')[1].split('</section>')[0])
    L = T['pt']; publicadas = []
    for p in NOVAS:
        pasta = '' if p['revisado'] else '_rascunho/'; pre = '' if p['revisado'] else '../'; home = pre or './'
        if pasta: os.makedirs(pasta, exist_ok=True)
        css, links, header, cookies, footer, ga, csp, og_v = _casca(src_head, src_ctrl, pre, pre + logo_url, home)
        url = URL + p['slug'] + '.html'
        par = lambda xs: ''.join('<p%s>%s</p>' % (' class="nota"' if i > 0 else '', x) for i, x in enumerate(xs))
        perg = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', faq[j][0], faq[j][1]) for i, j in enumerate(p['faq']))
        # links: as 4 revisadas (na raiz) + as novas já revisadas; no rascunho, as outras novas também (ficam lado a lado em _rascunho/)
        irmas = [(pre + q['slug'], q['h1']) for q in PAGINAS]
        for q in NOVAS:
            if q is p: continue
            if q['revisado']: irmas.append((pre + q['slug'], q['h1']))   # publicada, na raiz
            elif not p['revisado']: irmas.append((q['slug'], q['h1']))   # outro rascunho, na mesma pasta
        outros = ''.join('<li><a href="%s.html">%s</a></li>' % s for s in irmas) + '<li><a href="%s.html">Avaliação no Leblon</a></li>' % (pre + LEBLON['slug'])
        ld = {'@context': 'https://schema.org', '@type': 'MedicalWebPage', 'name': p['title'], 'url': url, 'inLanguage': 'pt-BR',
              'about': {'@type': 'MedicalCondition', 'name': p['h1']}, 'author': {'@type': 'Physician', 'name': L['nome'], 'url': URL}}
        if p['revisado']: ld['reviewedBy'] = {'@type': 'Physician', 'name': L['nome'], 'url': URL}; ld['lastReviewed'] = REVISADO_NOVAS
        aviso = '' if p['revisado'] else '<div class="rasc">RASCUNHO para revisão da Dra. Larissa · esta página ainda não está no site</div>\n'
        corpo = aviso + f'''
<section class="ph"><div class="wrap">
  <div>
    <span class="crumbs"><a href="{home}">{L['inicio']}</a> · {L['area']}</span>
    <h1>{p['h1']}<small>{p['sub']}</small></h1>
    <p class="lead">{p['lead']}</p>
    <div class="acts"><a class="btn primary" href="{home}#agendar">{L['agendar']}</a>{('<a class="more" href="' + home + '#esquema-' + p['esq'] + '">' + L['ver'] + '</a>') if p.get('esq') else ''}</div>
  </div>
  <figure><img{' class="lado"' if p['img'] == '{{IMG_PE_LADO}}' else ''} src="{pre + img_url[p['img']]}" alt="{p['alt']}" width="{p.get('wh', (569, 852))[0]}" height="{p.get('wh', (569, 852))[1]}"></figure>
</div></section>

<main class="art"><div class="wrap">
  <section><h2>{L['oque']}</h2><div class="txt">{par(p['oque'])}<p class="nota">{L['aparece']}: “{p['dor']}”.</p></div></section>
  <section><h2>Como aparece</h2><div class="txt">{par(p['aparece'])}</div></section>
  <section><h2>{L['trat']}</h2><div class="txt">{par(p['trat'])}</div></section>
{''.join('<section><h2>' + h + '</h2><div class="txt">' + ''.join('<p>' + x + '</p>' for x in xs) + '</div></section>' for h, xs in p.get('secoes', []))}
  <section><h2>Quando procurar</h2><div class="txt">{par(p['quando'])}</div></section>
</div></main>

<section class="faq pag-faq"><div class="wrap">
  <div><span class="caps">{L['perg']}</span><h2 style="margin-top:.7rem">{L['perg_h']}</h2></div>
  <div>{perg}</div>
</div></section>

<section class="outros"><div class="wrap">
  <span class="caps">{L['outros']}</span>
  <ul>{outros}</ul>
</div></section>

<section class="pcta"><div class="wrap">
  <div><h2>{L['cta']}</h2><p>Rua General Venâncio Flores, 184 · Leblon · Rio de Janeiro</p></div>
  <a class="btn primary" href="{home}#agendar">{L['agendar']}</a>
</div></section>
'''
        extra = '' if p['revisado'] else '<meta name="robots" content="noindex,nofollow">\n'
        open(pasta + p['slug'] + '.html', 'w', encoding='utf-8').write(
            _doc(csp, p['title'] + L['sufixo'], p.get('desc') or re.sub('<[^>]+>', '', p['oque'][0]), url, fav_v, pre, og_v, ld, links, css, extra, header, corpo, cookies, footer, ga, og_title=p['title'] + L['og']))
        if p['revisado']: publicadas.append(url)
    return publicadas

def gerar_leblon(src_head, src_ctrl, img_url, URL, logo_url, fav_v, ld_medico):
    # "Ortopedista de pé e tornozelo no Leblon": só textos já revisados da página principal
    css, links, header, cookies, footer, ga, csp, og_v = _casca(src_head, src_ctrl, '', logo_url, './')
    quem = re.search(r'<span class="caps"><b>06</b>[^<]*</span>\s*<h2>.*?</h2>\s*<p>(.*?)</p>', src_head, flags=re.S).group(1)
    ficha = re.search(r'<dl class="ficha">(.*?)</dl>', src_head, flags=re.S).group(1)
    cuid = src_head.split('id="cuidado"')[1]
    intro = re.search(r'<h2>.*?</h2>\s*<p>(.*?)</p>', cuid, flags=re.S).group(1)
    trail = re.search(r'<ol class="trail" id="trail">(.*?)</ol>', cuid, flags=re.S).group(1)
    agendar = src_head.split('id="agendar"')[1]
    lead_ag = re.search(r'<p class="lead">(.*?)</p>', agendar).group(1)
    assert lead_ag.startswith('E os exames que você já tem. '), lead_ag[:40]   # na página principal continua o título "Traga o sapato que mais dói"
    lead_ag = 'Traga o sapato que mais dói e os exames que você já tem. ' + lead_ag.split('. ', 1)[1]
    contato = re.search(r'<dl>(.*?)</dl>', agendar, flags=re.S).group(1)
    maps = re.search(r'href="(https://www\.google\.com/maps/[^"]*)"', agendar).group(1)
    faq = re.findall(r'<details[^>]*><summary>(.*?)</summary><p>(.*?)</p></details>', src_head.split('id="perguntas"')[1].split('</section>')[0])
    def item(q, a):
        s = _pagina_de(a)
        return ('<li><a href="%s.html"><b>%s</b>%s</a></li>' % (s, a, q)) if s else ('<li><span class="it"><b>%s</b>%s</span></li>' % (a, q))
    lista = ''.join(item(q, a) for q, a in _sintomas(src_head))
    assert lista.count('<li>') == 12, 'lista de sintomas mudou'
    perg = ''.join('<details%s><summary>%s</summary><p>%s</p></details>' % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(faq))
    url = URL + LEBLON['slug'] + '.html'
    ld = {'@context': 'https://schema.org', '@type': 'MedicalWebPage', 'name': LEBLON['title'], 'url': url, 'inLanguage': 'pt-BR', 'about': ld_medico}
    corpo = f'''
<section class="ph"><div class="wrap">
  <div>
    <span class="crumbs"><a href="./">Início</a> · Leblon, Rio de Janeiro</span>
    <h1>Ortopedista no Leblon<small>Pé e tornozelo · consulta presencial ou por teleconsulta</small></h1>
    <p class="lead">{intro}</p>
    <div class="acts"><a class="btn primary" href="./#agendar">Agendar avaliação</a><a class="more" href="{maps}" target="_blank" rel="noopener">Como chegar →</a></div>
  </div>
  <figure><img class="foto" src="{img_url['{{IMG_CONSULTORIO}}']}" alt="Dra. Larissa Silva no consultório, sentada à mesa" width="1043" height="1800"></figure>
</div></section>

<main class="art"><div class="wrap">
  <section><h2>Quem atende</h2><div class="txt"><p>{quem}</p><dl class="obs">{ficha}</dl></div></section>
  <section><h2>Como é a avaliação</h2><div class="txt"><ol class="trail">{trail}</ol></div></section>
  <section><h2>O que eu trato</h2><div class="txt"><ul class="lst">{lista}</ul></div></section>
  <section><h2>Contato e endereço</h2><div class="txt"><p>{lead_ag}</p><dl class="obs">{contato}</dl></div></section>
</div></main>

<section class="faq pag-faq"><div class="wrap">
  <div><span class="caps">Perguntas</span><h2 style="margin-top:.7rem">O que todo mundo <em>pergunta.</em></h2></div>
  <div>{perg}</div>
</div></section>

<section class="pcta"><div class="wrap">
  <div><h2>Traga o sapato que <em>mais dói.</em></h2><p>Rua General Venâncio Flores, 184 · Leblon · Rio de Janeiro</p></div>
  <a class="btn primary" href="./#agendar">Agendar avaliação</a>
</div></section>
'''
    open(LEBLON['slug'] + '.html', 'w', encoding='utf-8').write(
        _doc(csp, LEBLON['title'], LEBLON['desc'], url, fav_v, '', og_v, ld, links, css, '', header, corpo, cookies, footer, ga, 'website'))
    return [url]
