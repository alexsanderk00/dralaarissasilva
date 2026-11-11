import base64, hashlib, json, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

URL = 'https://alexsanderk00.github.io/dralaarissasilva/'
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
emb = src
for k, f in IMGS:
    emb = emb.replace(k, 'data:image/' + MIME[os.path.splitext(f)[1]] + ';base64,' + base64.b64encode(open(f, 'rb').read()).decode())
open('dra-larissa.html', 'w', encoding='utf-8').write(emb)
t = '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light;padding:env(safe-area-inset-top,0) 0 env(safe-area-inset-bottom,0)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>' + emb.replace('<link rel="stylesheet" href="https://fonts.googleapis.com', '<link rel="x" href="x') + '</body></html>'
open('test.html', 'w', encoding='utf-8').write(t)

# 2) site publicado: imagens como arquivos WebP em img/web/ (o HTML cai de ~640 KB para ~90 KB)
os.makedirs('img/web', exist_ok=True)
site = src
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
    site = site.replace(k, out + '?v=' + hashlib.md5(open(out, 'rb').read()).hexdigest()[:8])   # versão no nome: o navegador nunca mostra a foto antiga do cache

# imagem de prévia (WhatsApp, Instagram, Google): 1200 × 630
def font(names, size):
    for n in names:
        try: return ImageFont.truetype(n, size)
        except OSError: pass
    return ImageFont.load_default()
W, H = 1200, 630
og = Image.new('RGB', (W, H), '#F7FAF8'); d = ImageDraw.Draw(og)
ret = ImageOps.fit(Image.open('img/consultorio.jpg').convert('RGB'), (420, 525), centering=(.5, .3))
mask = Image.new('L', ret.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, *ret.size), 8, fill=255)
og.paste(ret, (W - 420 - 60, 52), mask)
logo = Image.open('img/logo.png').convert('RGBA'); logo.thumbnail((90, 90)); og.paste(logo, (64, 52), logo)
d.text((170, 72), 'Dra. Larissa Silva', fill='#113358', font=font(['C:/Windows/Fonts/seguisb.ttf'], 34))
d.text((170, 116), 'Ortopedista e Traumatologista', fill='#465A60', font=font(['C:/Windows/Fonts/segoeui.ttf'], 22))
d.text((64, 230), 'ORTOPEDIA · PÉ E TORNOZELO', fill='#146046', font=font(['C:/Windows/Fonts/consola.ttf'], 22))
d.text((60, 268), 'Seu pé,', fill='#113358', font=font(['C:/Windows/Fonts/seguisb.ttf'], 100))
d.text((60, 380), 'explicado.', fill='#146046', font=font(['C:/Windows/Fonts/seguisbi.ttf', 'C:/Windows/Fonts/seguisb.ttf'], 100))
d.text((64, 530), 'Joanete, calcanhar, Aquiles e tornozelo.', fill='#465A60', font=font(['C:/Windows/Fonts/segoeui.ttf'], 23))
og.save('img/web/og.jpg', quality=86)

# favicon quadrado: monograma sobre o claro da marca, legível em 16-32 px
fav = Image.new('RGBA', (192, 192), '#EBF4EF'); m = Image.open('img/logo.png').convert('RGBA'); m.thumbnail((150, 150), Image.LANCZOS)
fav.paste(m, ((192 - m.width) // 2, (192 - m.height) // 2), m); fav.save('img/web/favicon.png', optimize=True)

desc = 'Dra. Larissa Silva, ortopedista e traumatologista, cirurgia minimamente invasiva do pé e tornozelo no Rio de Janeiro. Joanete, Haglund, tendão de Aquiles e tornozelo explicados no esquema, do pé ao osso.'
ld = {'@context': 'https://schema.org', '@type': 'Physician', 'name': 'Dra. Larissa Silva', 'url': URL, 'image': URL + 'img/web/og.jpg',
      'description': desc, 'medicalSpecialty': 'Musculoskeletal', 'telephone': '+55-21-97289-6222',
      'address': {'@type': 'PostalAddress', 'addressLocality': 'Rio de Janeiro', 'addressRegion': 'RJ', 'addressCountry': 'BR'},
      'sameAs': ['https://www.instagram.com/dralaarissasilva/']}
head = ('<meta name="description" content="' + desc + '">\n'
        '<meta name="theme-color" content="#113358">\n'
        '<link rel="canonical" href="' + URL + '">\n'
        '<link rel="icon" type="image/png" href="img/web/favicon.png">\n<link rel="apple-touch-icon" href="img/web/favicon.png">\n'
        '<meta property="og:type" content="website">\n<meta property="og:locale" content="pt_BR">\n'
        '<meta property="og:title" content="Dra. Larissa Silva · Seu pé, explicado.">\n'
        '<meta property="og:description" content="' + desc + '">\n'
        '<meta property="og:url" content="' + URL + '">\n'
        '<meta property="og:image" content="' + URL + 'img/web/og.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n')
# versão avulsa para abrir direto no navegador / GitHub Pages: <title> e metas do topo do src vão para o <head>
import re
TOPO = r'^(?:<title>.*?</title>|<meta [^>]*>)\n'
head_src = ''.join(re.findall(TOPO, site, flags=re.M))
site = re.sub(TOPO, '', site, flags=re.M)
head = head_src + head
full = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        + head + '<style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n' + site + '\n</body>\n</html>\n')
open('index.html', 'w', encoding='utf-8').write(full)
print('artifact', len(emb) // 1024, 'KB · index', len(full) // 1024, 'KB')
