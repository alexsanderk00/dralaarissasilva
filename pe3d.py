# Copia o pé em 3D (Editor/modelo-site-medico/demo-pe-3d) para o site em /pe-3d/, com os ajustes do site oficial.
# Chamado pelo build.py. A fonte continua sendo a demo: mudou lá, roda o build aqui.
import os, re, shutil
AQUI = os.path.dirname(os.path.abspath(__file__))
DEMO = os.path.normpath(os.path.join(AQUI, '..', '..', 'modelo-site-medico', 'demo-pe-3d'))
DEST = os.path.join(AQUI, 'pe-3d')

def gerar():
    if not os.path.isdir(DEMO):
        print('pe-3d: demo não encontrada, mantendo a cópia atual'); return
    s = open(os.path.join(DEMO, 'index.html'), encoding='utf-8').read()
    def rp(a, b, n=1):
        nonlocal s
        assert s.count(a) == n, ('pe3d', a[:70], s.count(a)); s = s.replace(a, b)
    rp('<title>Onde dói · Pé em 3D</title>', '<title>Pé em 3D · Onde dói · Dra. Larissa Silva</title>\n<link rel="icon" href="/favicon.ico">')
    # noindex continua enquanto há textos não aprovados pela Dra. Larissa (ela revisa no próprio site)
    # nome no topo volta para o site; "Demonstração" sai
    rp('<div class="nome">Dra. Larissa Silva<small>', '<a class="nome" href="/" title="Voltar ao site">Dra. Larissa Silva<small>')
    rp('<i>Demonstração · modelo ilustrativo</i></div>', '<i>← voltar ao site</i></a>')
    rp('header a{pointer-events:auto;', 'header a.nome{background:none;color:inherit;padding:0;border-radius:0;white-space:normal;display:block;min-height:0}\nheader a{pointer-events:auto;')
    rp('<a href="https://dralaarissasilva.com.br/#agendar">Agendar avaliação</a>', '<a href="/#agendar">Agendar avaliação</a>')
    # ajustes do agente fiscal para o site oficial
    rp("[0, 'a broca fina corta o osso']", "[0, 'corte do osso']")   # instrumento sem nome na tela (o texto aprovado da etapa continua igual)
    rp("const SITE = 'https://dralaarissasilva.com.br/';", "const SITE = '/';")   # links para o site no mesmo domínio
    # three.js servido pelo próprio site (vendor/three-0.160.0, conferido com o hash do npm): o pé 3D não depende do jsDelivr
    T = '/pe-3d/three-0.160.0/'
    rp('https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.min.js', T + 'build/three.module.min.js', 2)
    rp('"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"', '"three/addons/":"' + T + 'examples/jsm/"')
    s = re.sub(r'<link rel="preconnect" href="https://cdn\.jsdelivr\.net"[^>]*>\n?', '', s)
    assert 'jsdelivr' not in s, 'pe3d: sobrou jsdelivr'
    # a pedido do Alexsander (23/11/2026), o site não mostra avisos de rascunho; a revisão da Dra. Larissa continua pela folha de aprovação

    s = re.sub(r"rasc:(?:true|\[[0-9, ]*\]),", "", s)
    s = re.sub(r"extra:\{(?:\d:'[^']*',?)+\},", "", s)
    s = s.replace(" (rascunho)", "")
    assert "rasc:" not in s.split("const ETAPAS")[0] and "extra:{" not in s and "(rascunho)" not in s, 'pe3d: sobrou marca de rascunho'
    os.makedirs(os.path.join(DEST, 'modelo'), exist_ok=True)
    open(os.path.join(DEST, 'index.html'), 'w', encoding='utf-8').write(s)
    for f in ['pe2.bin', 'pe2.json']:
        shutil.copyfile(os.path.join(DEMO, 'modelo', f), os.path.join(DEST, 'modelo', f))
    v = os.path.join(DEST, 'three-0.160.0')
    if os.path.isdir(v): shutil.rmtree(v)
    shutil.copytree(os.path.join(AQUI, 'vendor', 'three-0.160.0'), v)
    print('pe-3d/index.html', len(s) // 1024, 'KB')

if __name__ == '__main__':
    gerar()
