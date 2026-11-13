import base64, hashlib, json, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

URL = 'https://dralaarissasilva.com.br/'
IMGS = [('{{IMG_JOANETE}}', 'img/joanete.jpg'), ('{{IMG_BAILARINA}}', 'img/bailarina.jpg'), ('{{IMG_FOTO1}}', 'img/foto1.jpg'), ('{{IMG_FOTO2}}', 'img/foto2.jpg'), ('{{IMG_FOTO3}}', 'img/foto3.jpg'), ('{{IMG_PERFIL}}', 'img/perfil.jpg'), ('{{IMG_CONSULTORIO}}', 'img/consultorio.jpg'), ('{{IMG_LOGO}}', 'img/logo.png'),
        ('{{IMG_PE_CIMA}}', 'img/pe_cima.webp'), ('{{IMG_PE_LADO}}', 'img/pe_lado.webp'),
        ('{{IMG_PERFIL_POSTER}}', 'img/perfil_poster.jpg')]
MIME = {'.jpg': 'jpeg', '.png': 'png', '.webp': 'webp'}

# junta os 3 arquivos editáveis em src.html; vídeos entram com ?v=<hash> (o navegador nunca mostra o antigo do cache)
src = ''.join(open(f, encoding='utf-8').read() for f in ['head_v3.html', 'geom_v3.js', 'ctrl_v3.js'])
for k, f in [('{{VID_PERFIL}}', 'video/perfil.mp4')]:
    src = src.replace(k, f + '?v=' + hashlib.md5(open(f, 'rb').read()).hexdigest()[:8])
open('src.html', 'w', encoding='utf-8').write(src)

# 1) versão com imagens embutidas: tema do artifact e teste local
import re
emb = re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>\n', '', src)   # a regra de segurança é só do site publicado: no artifact ela bloquearia o próprio ambiente
for k, f in IMGS:
    emb = emb.replace(k, 'data:image/' + MIME[os.path.splitext(f)[1]] + ';base64,' + base64.b64encode(open(f, 'rb').read()).decode())
open('dra-larissa.html', 'w', encoding='utf-8').write(emb)
t = '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>:root{color-scheme:light;padding:env(safe-area-inset-top,0) 0 env(safe-area-inset-bottom,0)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + emb.replace('<link rel="stylesheet" href="https://fonts.googleapis.com', '<link rel="x" href="x') + '</body></html>'
open('test.html', 'w', encoding='utf-8').write(t)

# 2) site publicado: imagens como arquivos WebP em img/web/ (o HTML cai de ~640 KB para ~90 KB)
os.makedirs('img/web', exist_ok=True)
# ---------- avaliações do Google (avaliacoes.json) ----------
import html as _h
def secao_avaliacoes():
    A = json.load(open('avaliacoes.json', encoding='utf-8'))
    if not A.get('total'): return ''   # sem avaliações, sem seção
    url = lambda u: u if str(u).startswith('https://') else ''   # só links https
    STAR = '<svg viewBox="0 0 20 20"><path fill="currentColor" d="M10 1.6l2.6 5.4 5.8.8-4.2 4.1 1 5.8L10 15l-5.2 2.7 1-5.8L1.6 7.8l5.8-.8z"/></svg>'
    def estrelas(n, rotulo):   # cheias pela nota arredondada (4,5 → 5), as que faltam em cinza
        k = int(float(n) + 0.5)
        return '<span class="stars" role="img" aria-label="' + rotulo + '">' + STAR * k + STAR.replace('<svg ', '<svg class="off" ') * (5 - k) + '</span>'
    nota = ('%.1f' % A['nota']).replace('.', ',')
    for i in A.get('itens', []):
        for c in ('nome', 'texto', 'nota'):
            if c not in i: raise SystemExit('avaliacoes.json: avaliação sem o campo "' + c + '"')
    itens = ''.join('<li><div class="who"><span class="av" aria-hidden="true">' + _h.escape(i['nome'][:1]) + '</span><strong>' + _h.escape(i['nome']) + '</strong><small>' + _h.escape(i.get('quando', '')) + '</small></div>'
                    + estrelas(i['nota'], str(i['nota']) + ' de 5 estrelas') + '<p>' + _h.escape(i['texto']) + '</p></li>' for i in A.get('itens', []))
    avaliar = ('<a href="' + _h.escape(url(A['link_avaliar'])) + '" target="_blank" rel="noopener">Deixar uma avaliação</a>') if url(A.get('link_avaliar', '')) else ''
    return ('<section class="rev' + ('' if itens else ' solo') + '" id="avaliacoes" aria-label="Avaliações no Google"><div class="wrap">'
            '<div class="head rv"><span class="caps">Avaliações no Google</span><h2 style="margin-top:.7rem">' + ('O que dizem os <em>pacientes.</em>' if itens else 'Nota no <em>Google.</em>') + '</h2></div>'
            '<div class="score rv"><span class="g">Google</span><b>' + nota + '</b>' + estrelas(A['nota'], 'Nota ' + nota + ' de 5')
            + '<span>Com base em <strong>' + str(int(A['total'])) + '</strong> avaliações</span>'
            '<a href="' + _h.escape(url(A['link_ver'])) + '" target="_blank" rel="noopener">Ver todas no Google</a>' + avaliar + '</div>'
            + ('<ul class="list rv" aria-label="Algumas avaliações">' + itens + '</ul>' if itens else '')
            + '<p class="nota">Avaliações do Google' + (', atualizadas em ' + _h.escape(A['atualizado_em']) if A.get('atualizado_em') else '') + '. Cada caso é único; a experiência de um paciente não garante o mesmo resultado para outro.</p>'
            '</div></section>')
src = src.replace('<!--AVALIACOES-->', secao_avaliacoes())

site = src
IMG_URL = {}   # placeholder → arquivo publicado com ?v= (as páginas de cada problema usam também)
for k, f in IMGS:
    name = os.path.splitext(os.path.basename(f))[0]
    if f.endswith('.png'):
        out = 'img/web/' + name + '.png'
        Image.open(f).save(out, optimize=True)
    else:
        out = 'img/web/' + name + '.webp'
        im = ImageOps.exif_transpose(Image.open(f))
        im = im.convert('RGBA' if 'A' in im.getbands() else 'RGB')   # as fotos do pé do esquema têm fundo transparente: não perder
        if im.width > 1600: im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        im.save(out, 'WEBP', quality=78, method=6)
    IMG_URL[k] = out + '?v=' + hashlib.md5(open(out, 'rb').read()).hexdigest()[:8]
    site = site.replace(k, IMG_URL[k])   # versão no nome: o navegador nunca mostra a foto antiga do cache

# imagem de prévia (WhatsApp, Instagram, Google): 1200 × 630
def font(names, size):
    for n in names:
        try: return ImageFont.truetype(n, size)
        except OSError: pass
    return ImageFont.load_default()
W, H = 1200, 630
# mesmo visual do topo do site: foto do vídeo desfocada sob película azul, título branco + menta, foto do consultório num cartão
from PIL import ImageFilter
def bahn(size, peso='Bold'):
    f = font(['C:/Windows/Fonts/bahnschrift.ttf', 'C:/Windows/Fonts/seguisb.ttf'], size)
    try: f.set_variation_by_name(peso)
    except Exception: pass
    return f
og = ImageOps.fit(Image.open('img/perfil_poster.jpg').convert('RGB'), (W, H), centering=(.5, .35)).filter(ImageFilter.GaussianBlur(14))
veu = Image.new('RGB', (W, H), '#113358'); og = Image.blend(og, veu, .78)
grad = Image.linear_gradient('L').rotate(90).resize((W, H))   # mais escuro à esquerda, onde fica o texto
og = Image.composite(Image.new('RGB', (W, H), '#0D2A4A'), og, grad.point(lambda v: int(v * .55)))
d = ImageDraw.Draw(og)
ret = ImageOps.fit(Image.open('img/consultorio.jpg').convert('RGB'), (380, 500), centering=(.5, .3))
mask = Image.new('L', ret.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, *ret.size), 18, fill=255)
sombra = Image.new('L', (W, H), 0); ImageDraw.Draw(sombra).rounded_rectangle((W - 380 - 70 + 8, 72, W - 70 + 8, 572 + 14), 18, fill=150)
og.paste(Image.new('RGB', (W, H), '#061526'), (0, 0), sombra.filter(ImageFilter.GaussianBlur(18)))
og.paste(ret, (W - 380 - 70, 65), mask)
ImageDraw.Draw(og).rounded_rectangle((W - 380 - 70, 65, W - 70, 565), 18, outline=(255, 255, 255, 60), width=2)
logo = Image.open('img/logo.png').convert('RGBA'); logo.thumbnail((78, 78))
branco = Image.new('RGBA', logo.size, (255, 255, 255, 255)); branco.putalpha(logo.getchannel('A'))   # monograma em branco, como no cabeçalho
og.paste(branco, (64, 56), branco)
d = ImageDraw.Draw(og)
d.text((156, 66), 'Dra. Larissa Silva', fill='#FFFFFF', font=bahn(34, 'Bold'))
d.text((157, 108), 'Médica ortopedista e traumatologista', fill='#C9D6E2', font=font(['C:/Windows/Fonts/segoeui.ttf'], 21))
d.text((66, 232), 'ORTOPEDIA · PÉ E TORNOZELO', fill='#72C6A2', font=font(['C:/Windows/Fonts/consola.ttf'], 21))
d.text((60, 262), 'Seu pé,', fill='#FFFFFF', font=bahn(104, 'Bold'))
d.text((60, 372), 'explicado.', fill='#72C6A2', font=bahn(104, 'Bold'))
d.text((66, 520), 'Leblon · Rio de Janeiro · CRM 52-126334-0 · RQE 60891', fill='#C9D6E2', font=font(['C:/Windows/Fonts/segoeui.ttf'], 21))
og.save('img/web/og.jpg', quality=88)
OG_V = hashlib.md5(open('img/web/og.jpg', 'rb').read()).hexdigest()[:8]   # versão no link: WhatsApp e redes guardam a prévia antiga pelo endereço

# favicon quadrado: só o monograma, sem fundo
# fundo sólido (quadrado arredondado azul da marca) com o monograma branco: aparece no tema escuro das abas, no Google e no atalho do iPhone
fav = Image.new('RGBA', (192, 192), (0, 0, 0, 0)); ImageDraw.Draw(fav).rounded_rectangle((0, 0, 191, 191), 38, fill='#113358')
m = Image.open('img/logo.png').convert('RGBA'); m.thumbnail((140, 140), Image.LANCZOS)
br = Image.new('RGBA', m.size, (255, 255, 255, 255)); br.putalpha(m.getchannel('A'))
fav.paste(br, ((192 - m.width) // 2, (192 - m.height) // 2), br); fav.save('img/web/favicon.png', optimize=True)
fav.save('favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])   # na raiz: é onde o Google procura primeiro o ícone dos resultados de busca
FAV_V = hashlib.md5(open('img/web/favicon.png', 'rb').read()).hexdigest()[:8]   # versão no link: navegador guarda favicon no cache com força

desc = 'Dra. Larissa Silva, ortopedista e traumatologista, cirurgia minimamente invasiva do pé e tornozelo no Rio de Janeiro. Joanete, Haglund, tendão de Aquiles e tornozelo explicados no esquema, do pé ao osso.'
ld = {'@context': 'https://schema.org', '@type': 'Physician', 'name': 'Dra. Larissa Silva', 'alternateName': ['Larissa Silva', 'Dra. Larissa da Silva', 'Larissa da Silva'], 'url': URL, 'image': URL + 'img/web/og.jpg',
      'description': desc, 'medicalSpecialty': 'Musculoskeletal', 'telephone': '+55-21-97289-6222',
      'address': {'@type': 'PostalAddress', 'streetAddress': 'Rua General Venâncio Flores, 184 - Leblon', 'addressLocality': 'Rio de Janeiro', 'addressRegion': 'RJ', 'addressCountry': 'BR'},
      'areaServed': {'@type': 'City', 'name': 'Rio de Janeiro'},
      'isAcceptingNewPatients': True,
      'hasMap': 'https://www.google.com/maps/search/?api=1&query=Rua+General+Ven%C3%A2ncio+Flores%2C+184%2C+Leblon%2C+Rio+de+Janeiro',
      'knowsAbout': ['Joanete (hálux valgo)', 'Deformidade de Haglund', 'Tendão de Aquiles', 'Entorse de tornozelo', 'Instabilidade do tornozelo', 'Fascite plantar', 'Cirurgia minimamente invasiva do pé e tornozelo'],
      'availableService': [{'@type': 'MedicalProcedure', 'name': n} for n in ['Cirurgia de joanete minimamente invasiva', 'Cirurgia da deformidade de Haglund', 'Sutura do tendão de Aquiles', 'Reparo de ligamentos do tornozelo']],
      'knowsLanguage': ['pt-BR', 'en'],
      'sameAs': ['https://www.instagram.com/dralaarissasilva/', 'https://www.google.com/search?kgmid=/g/11zzlrdytf']}   # Instagram e Perfil da Empresa no Google (kgmid do perfil)
# nome do site nos resultados do Google (em cima do endereço): dado WebSite na página principal; o Google escolhe entre name e alternateName
SITE_NOME = 'Dra. Larissa Silva'   # curto: o Google costuma ignorar nome com profissão e voltar ao domínio
SITE = {'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NOME, 'alternateName': ['Larissa Silva', 'dralaarissasilva.com.br'], 'url': URL}
head = ('<meta name="description" content="' + desc + '">\n'
        '<meta name="theme-color" content="#113358">\n'
        '<link rel="canonical" href="' + URL + '">\n'
        '<link rel="alternate" hreflang="pt-BR" href="' + URL + '">\n<link rel="alternate" hreflang="en" href="' + URL + 'en/">\n<link rel="alternate" hreflang="x-default" href="' + URL + '">\n'
        '<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" type="image/png" sizes="192x192" href="img/web/favicon.png?v=' + FAV_V + '">\n<link rel="apple-touch-icon" href="img/web/favicon.png?v=' + FAV_V + '">\n'
        '<meta property="og:type" content="website">\n<meta property="og:locale" content="pt_BR">\n'
        '<meta property="og:title" content="Dra. Larissa Silva · Seu pé, explicado.">\n'
        '<meta property="og:description" content="' + desc + '">\n'
        '<meta property="og:url" content="' + URL + '">\n'
        '<meta property="og:image" content="' + URL + 'img/web/og.jpg?v=' + OG_V + '">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta property="og:site_name" content="' + SITE_NOME + '">\n'
        '<script type="application/ld+json">' + json.dumps(SITE, ensure_ascii=False) + '</script>\n'
        '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n')
# versão avulsa para abrir direto no navegador / GitHub Pages (o viewport vem do head_v3.html: sem ele o celular mostra o layout de computador encolhido): <title> e metas do topo do src vão para o <head>
import re
TOPO = r'^(?:<title>.*?</title>|<meta [^>]*>)\n'
head_src = ''.join(re.findall(TOPO, site, flags=re.M))
site = re.sub(TOPO, '', site, flags=re.M)
head = head_src + head
full = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        + head + '<style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n' + site + '\n</body>\n</html>\n')
open('index.html', 'w', encoding='utf-8').write(full)
print('artifact', len(emb) // 1024, 'KB · index', len(full) // 1024, 'KB')

# ---------- versão em inglês: en/index.html = o mesmo site com os textos de traducao_en.json (pares [pt, en], do maior para o menor) ----------
LANG_PT = '<a class="lang" href="en/" hreflang="en" lang="en" aria-label="English version">EN</a>'
TEM_EN = os.path.exists('traducao_en.json')
if TEM_EN:
    en = full
    en = en.replace(LANG_PT, '<a class="lang" href="../" hreflang="pt-BR" lang="pt-BR" aria-label="Versão em português">PT</a>')
    desc_en = ("Dr. Larissa Silva, orthopedic surgeon in Rio de Janeiro (Leblon) focused on minimally invasive foot and ankle surgery. "
               "Bunions, Haglund's deformity, Achilles tendon and ankle problems explained from skin to bone. In-person and teleconsultation (Google Meet).")
    for a, b in [('<html lang="pt-BR">', '<html lang="en">'), ('content="' + desc + '"', 'content="' + desc_en.replace("'", '&#39;') + '"'),
                 ('<link rel="canonical" href="' + URL + '">', '<link rel="canonical" href="' + URL + 'en/">'),
                 ('<meta property="og:url" content="' + URL + '">', '<meta property="og:url" content="' + URL + 'en/">'),
                 ('content="pt_BR"', 'content="en_US"'), ('Dra. Larissa Silva · Seu pé, explicado.', 'Dr. Larissa Silva · Your foot, explained.')]:
        assert a in en, a[:60]; en = en.replace(a, b)
    ld_en = dict(ld, description=desc_en, knowsAbout=['Bunion (hallux valgus)', "Haglund's deformity", 'Achilles tendon', 'Ankle sprain', 'Ankle instability', 'Plantar fasciitis', 'Minimally invasive foot and ankle surgery'],
                 availableService=[{'@type': 'MedicalProcedure', 'name': n} for n in ['Minimally invasive bunion surgery', "Haglund's deformity surgery", 'Achilles tendon repair', 'Ankle ligament repair']])
    a = json.dumps(ld, ensure_ascii=False); assert a in en; en = en.replace(a, json.dumps(ld_en, ensure_ascii=False))   # dados para o Google em inglês
    SITE_EN = dict(SITE)   # o Google tira o nome do site só da página principal da raiz: o /en/ usa o mesmo
    en = en.replace(json.dumps(SITE, ensure_ascii=False), json.dumps(SITE_EN, ensure_ascii=False)).replace('content="' + SITE_NOME + '"', 'content="' + SITE_EN['name'] + '"')
    for pt, eng in json.load(open('traducao_en.json', encoding='utf-8')): en = en.replace(pt, eng)   # depois das metas do topo, que usam o texto em português
    en = re.sub(r'<b>(\d),(\d)</b>', lambda m: '<b>' + m.group(1) + '.' + m.group(2) + '</b>', en)   # nota no formato inglês (5.0)
    en = re.sub(r'aria-label="Nota (\d),(\d) de 5"', lambda m: 'aria-label="Rated ' + m.group(1) + '.' + m.group(2) + ' out of 5"', en)
    # a página fica em /en/ e os arquivos continuam na raiz
    for q in ('"', "'"):
        for a in ('img/web/', 'video/perfil'): en = en.replace(q + a, q + '../' + a)   # só o arquivo do vídeo: "video/mp4" do atributo type não é caminho
    en = re.sub(r'href="([a-z-]+\.html)"', lambda m: 'href="' + ('' if m.group(1) in ('joanete.html', 'haglund.html', 'tendao-de-aquiles.html', 'entorse-de-tornozelo.html') else '../') + m.group(1) + '"', en)   # as 4 páginas têm versão em en/; privacidade fica na raiz
    os.makedirs('en', exist_ok=True)
    open('en/index.html', 'w', encoding='utf-8').write(en)
    print('en/index.html', len(en) // 1024, 'KB')
else:   # sem tradução: o botão EN não aparece
    full = full.replace(LANG_PT, ''); open('index.html', 'w', encoding='utf-8').write(full)

# páginas de cada problema (joanete, Haglund, Aquiles, tornozelo): textos tirados do head_v3.html e do ctrl_v3.js
import paginas
PAGS = paginas.gerar(open('head_v3.html', encoding='utf-8').read(), open('ctrl_v3.js', encoding='utf-8').read(), IMG_URL, URL, IMG_URL['{{IMG_LOGO}}'], FAV_V)
if TEM_EN:   # as mesmas 4 páginas em inglês, em en/
    PAGS += paginas.gerar(open('head_v3.html', encoding='utf-8').read(), open('ctrl_v3.js', encoding='utf-8').read(), IMG_URL, URL, IMG_URL['{{IMG_LOGO}}'], FAV_V, 'en', json.load(open('traducao_en.json', encoding='utf-8')))

# Google: mapa do site e regras de rastreamento (enviar sitemap.xml no Search Console)
import datetime
open('sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>' + u + '</loc><lastmod>' + datetime.date.today().isoformat() + '</lastmod></url>\n' for u in [URL] + ([URL + 'en/'] if TEM_EN else []) + PAGS) + '</urlset>\n')
open('robots.txt', 'w', encoding='utf-8').write('User-agent: *\nAllow: /\n\nSitemap: ' + URL + 'sitemap.xml\n')
