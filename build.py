import base64
# junta os 3 arquivos editáveis em src.html
s=''.join(open(f,encoding='utf-8').read() for f in ['head_v3.html','geom_v3.js','ctrl_v3.js'])
open('src.html','w',encoding='utf-8').write(s)
for k,f,mime in [('{{IMG_JOANETE}}','img/joanete.jpg','jpeg'),('{{IMG_BAILARINA}}','img/bailarina.jpg','jpeg'),('{{IMG_RETRATO}}','img/retrato.jpg','jpeg'),('{{IMG_CIRURGIA}}','img/cirurgia.jpg','jpeg'),('{{IMG_CURSO}}','img/curso.jpg','jpeg'),('{{IMG_LOGO}}','img/logo.png','png'),('{{IMG_PE_CIMA}}','img/pe_cima.webp','webp'),('{{IMG_PE_LADO}}','img/pe_lado.webp','webp')]:
    s=s.replace(k,'data:image/'+mime+';base64,'+base64.b64encode(open(f,'rb').read()).decode())
open('dra-larissa.html','w',encoding='utf-8').write(s)
t='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light;padding:env(safe-area-inset-top,0) 0 env(safe-area-inset-bottom,0)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>'+s.replace('<link rel="stylesheet" href="https://fonts.googleapis.com','<link rel="x" href="x')+'</body></html>'
open('test.html','w',encoding='utf-8').write(t); print(len(s)//1024,'KB')
# versão avulsa para abrir direto no navegador / subir em hospedagem
full='<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="description" content="Dra. Larissa da Silva, ortopedista de pé e tornozelo. Joanete, Haglund, tendão de Aquiles e tornozelo explicados no esquema, do pé ao osso.">\n<style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n'+s+'\n</body>\n</html>\n'
open('index.html','w',encoding='utf-8').write(full)
