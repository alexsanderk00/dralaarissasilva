/* ---------- textos (rascunho para revisão médica) ---------- */
const TXT={
  joanete:{name:'Joanete',steps:[
    ['Por fora, o joanete é o calombo na lateral do dedão, com o dedão inclinado para os outros dedos. Role, ou arraste a linha, para ver por dentro.'],
    ['Por dentro não existe osso novo. São os mesmos ossos, fora do lugar: o osso longo do dedão, o primeiro metatarso, abriu para fora, e a cabeça dele saiu de cima dos sesamoides.'],
    ['O primeiro metatarso abre para um lado e o dedão entorta para o outro. É o ângulo entre os dois que se mede na radiografia. O “calombo” é a cabeça do osso.'],
    ['Quando calçado largo, palmilha e fisioterapia não controlam a dor, a cirurgia realinha o osso. Na técnica minimamente invasiva, uma broca fina corta o osso por furinhos na pele, a cabeça é deslocada para o lugar e fixada com parafusos.','A técnica depende do grau do desvio. Toda cirurgia tem riscos, como infecção, rigidez e retorno do desvio.'],
    ['O osso consolida na nova posição ao longo das semanas. O apoio, o calçado e a volta às atividades seguem o plano definido para o seu caso.','O resultado e a recuperação variam de pessoa para pessoa.']]},
  haglund:{name:'Calcanhar · Haglund',steps:[
    ['Por fora, o calcanhar tem contorno liso atrás, bem onde o contraforte do sapato encosta. Role, ou arraste a linha, para ver por dentro.'],
    ['Atrás do calcanhar, o tendão de Aquiles desce e se prende no osso. Entre os dois há uma pequena bolsa de líquido, a bursa, que reduz o atrito.'],
    ['Na deformidade de Haglund, uma saliência do osso atrita com o tendão e com o sapato. A bursa inflama, incha e dói. Não é calo e não é fascite: fascite dói embaixo do calcanhar.'],
    ['O primeiro passo não é cirurgia. Calçado com a parte de trás macia, calcanheira e exercício orientado melhoram a maioria. Quando não resolve, a cirurgia retira o excesso de osso e limpa a região inflamada.','Pode ser aberta ou por vídeo, conforme o caso. Toda cirurgia tem riscos.'],
    ['Sem a saliência, o tendão deixa de ser comprimido contra o osso. O tempo de proteção e a fisioterapia dependem do que foi feito no tendão.','O resultado e a recuperação variam de pessoa para pessoa.']]},
  aquiles:{name:'Tendão de Aquiles',steps:[
    ['Por fora, o tendão de Aquiles é a corda firme atrás do tornozelo, logo acima do calcanhar. Role, ou arraste a linha, para ver por dentro.'],
    ['O tendão de Aquiles liga a panturrilha ao osso do calcanhar. É ele que dá o impulso para andar, correr e ficar na ponta do pé.'],
    ['Na ruptura, o tendão arrebenta alguns centímetros acima do calcanhar, muitas vezes numa arrancada ou num salto. A sensação é de pedrada atrás da perna. As pontas se afastam e falta força para ficar na ponta do pé.'],
    ['A ruptura pode ser tratada com bota e reabilitação ou com cirurgia. Na cirurgia, as duas pontas são aproximadas e costuradas, por corte aberto ou por pequenos cortes.','A escolha depende da idade, da atividade e do tempo desde a lesão. Toda cirurgia tem riscos.'],
    ['O tendão cicatriza e fica mais espesso no ponto do reparo. A volta ao esporte acontece por fases, com fisioterapia, ao longo de meses.','O resultado e a recuperação variam de pessoa para pessoa.']]},
  tornozelo:{name:'Tornozelo · ligamento',steps:[
    ['Por fora, o tornozelo tem um osso saliente de cada lado. Os ligamentos que mais rompem ficam logo à frente e abaixo do de fora. Role, ou arraste a linha.'],
    ['Do lado de fora do tornozelo, ligamentos curtos prendem a fíbula ao tálus e ao calcâneo. São eles que seguram o pé quando você pisa torto.'],
    ['Na entorse, o ligamento da frente é o que mais rompe. A maioria cicatriza com proteção e fisioterapia. Quando cicatriza frouxo, o tálus ganha folga e o tornozelo passa a falsear.'],
    ['Se a instabilidade continua depois da reabilitação, o ligamento pode ser reparado: ele é preso de volta no osso com pequenas âncoras e suturas.','Em muitos casos por vídeo. Toda cirurgia tem riscos.'],
    ['O ligamento reparado volta a limitar o movimento do tálus. Fisioterapia de força e equilíbrio faz parte do tratamento, antes e depois.','O resultado e a recuperação variam de pessoa para pessoa.']]}
};
const PARTS={
  halux:['Dedão (hálux)','2 falanges','É o dedo que mais empurra o chão no fim do passo.','para onde ele aponta, quanto dobra e se dói ao mexer.'],
  m1:['1º metatarso','osso do joanete','Osso longo que sustenta o dedão. Quando abre para fora, a cabeça dele forma o joanete.','o ângulo dele na radiografia feita em pé.'],
  sesamoides:['Sesamoides','2 ossinhos','Ficam embaixo da cabeça do 1º metatarso e funcionam como roldana do tendão do dedão.','se continuam embaixo do osso ou se saíram do lugar.'],
  dedos:['Dedos menores','2º ao 5º','Sofrem quando o dedão empurra: podem entortar em garra e criar calos.','calos, apoio e mobilidade de cada dedo.'],
  metas:['Metatarsos','2º ao 5º','Dividem o peso na frente do pé. Sobrecarga aqui dá dor na “bola” do pé.','pontos de dor e calos na planta.'],
  aquiles:['Tendão de Aquiles','panturrilha ao calcanhar','Liga a panturrilha ao calcanhar e dá o impulso do passo.','espessura, pontos de dor e força na ponta do pé.'],
  calcaneo:['Calcâneo','osso do calcanhar','Recebe o primeiro impacto do passo. Atrás prende o Aquiles; embaixo, a fáscia plantar.','se a dor é atrás ou embaixo: muda o diagnóstico.'],
  fascia:['Fáscia plantar','sola do pé','Faixa firme que sustenta o arco. Inflamada, dói embaixo do calcanhar nos primeiros passos do dia.','dor ao apertar a origem dela, no calcanhar.'],
  talus:['Tálus','encaixe do tornozelo','Fica entre a perna e o calcanhar e faz o pé subir e descer.','folga e estalos ao mover o tornozelo.'],
  fibula:['Fíbula','osso de fora','A ponta dela é o osso saliente do lado de fora do tornozelo, de onde saem os ligamentos que mais rompem.','dor ao apertar o osso, que pode indicar fratura.'],
  ligamento:['Ligamentos','fíbula ao tálus','Seguram o pé quando você pisa torto.','testes de gaveta e de inclinação, comparando os dois lados.']
};
const PARTLIST={joanete:['halux','m1','sesamoides','dedos','metas'],haglund:['aquiles','calcaneo','fascia','talus'],aquiles:['aquiles','calcaneo','talus','fascia'],tornozelo:['fibula','talus','ligamento','calcaneo']};

/* ---------- cenas, varredura e alça ---------- */
const scenes={dorsal:Dorsal(),lateral:Lateral()};
const hand=el('g',{},svg),edge=el('line',{id:'edge',y1:-20,y2:660},hand),grip=el('g',{id:'grip',tabindex:0,role:'slider','aria-label':'Arraste para ver por fora ou em raio-x','aria-valuemin':0,'aria-valuemax':100},hand);
el('circle',{r:29},grip);el('path',{d:'M-17 -3l-6 5 6 5M17 -3l6 5-6 5'},grip);{const t=el('text',{y:-7},grip);t.textContent='ARRASTE'}
const GY=604;
function setWipe(dir,w){
  const e=dir==='right'?600*(1-w):600*w;WIPE.x=e;WIPE.dir=dir;
  if(dir==='right'){cXr.setAttribute('x',f1(e));cXr.setAttribute('width',f1(620-e));cSr.setAttribute('x',-20);cSr.setAttribute('width',f1(e+20))}
  else{cXr.setAttribute('x',-20);cXr.setAttribute('width',f1(e+20));cSr.setAttribute('x',f1(e));cSr.setAttribute('width',f1(620-e))}
  edge.setAttribute('x1',f1(e));edge.setAttribute('x2',f1(e));edge.style.opacity=(w>.004&&w<.996)?1:0;
  grip.setAttribute('transform','translate('+f1(clamp(e,34,566))+' '+GY+')');grip.setAttribute('aria-valuenow',Math.round(w*100));
}

/* ---------- estado ---------- */
const story=document.getElementById('story'),stepsLi=[...document.querySelectorAll('#steps li')],stepDesc=document.getElementById('stepDesc'),
      meter=document.getElementById('meter'),viewTag=document.getElementById('viewTag'),kicker=document.getElementById('kicker'),tabs=[...document.querySelectorAll('.tab')],
      partgrid=document.getElementById('partgrid'),partinfo=document.getElementById('partinfo'),xrayToggle=document.getElementById('xrayToggle');
let cond='joanete',target=-1,s=-1,active=-1,dirty=true,w=0,wUser=null,sel=null;
const scene=()=>cond==='joanete'?scenes.dorsal:scenes.lateral;
const STOPS=[[0,-1],[.05,-1],[.2,0],[.26,0],[.44,1],[.5,1],[.72,2],[.78,2],[.93,3],[1,3]];
function mapS(p){for(let i=1;i<STOPS.length;i++){const[a,va]=STOPS[i-1],[b,vb]=STOPS[i];if(p<=b)return va+(vb-va)*clamp((p-a)/(b-a))}return 3}
const REST=[.02,.23,.47,.75,.97];
function readScroll(){const r=story.getBoundingClientRect(),total=story.offsetHeight-innerHeight;target=mapS(clamp(-r.top/total))}
const wipeAuto=()=>s<0?seg(s,-1,-.05):1-(1-scene().endW(cond))*seg(s,2.62,3);

function infoHTML(box,id){
  box.textContent='';
  if(!id){const c=document.createElement('span');c.className='caps';c.textContent='O que a avaliação olha';box.appendChild(c);box.appendChild(document.createTextNode('Escolha um osso, aqui ou no desenho, para ver o que ele faz e o que a Dra. observa nele.'));return}
  const P=PARTS[id],c=document.createElement('span');c.className='caps';c.textContent=P[0];box.appendChild(c);
  box.appendChild(document.createTextNode(P[2]+' '));const b=document.createElement('b');b.textContent='Na avaliação: ';box.appendChild(b);box.appendChild(document.createTextNode(P[3]));
}
function select(id){
  sel=(id===sel)?null:id;
  svg.querySelectorAll('.sel').forEach(e=>e.classList.remove('sel'));
  if(sel)(scene().parts[sel]||[]).forEach(e=>e.classList.add('sel'));
  partgrid.querySelectorAll('.part').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.p===sel)));
  infoHTML(partinfo,sel);
  if(sel){wUser=1;if(getComputedStyle(partinfo.parentElement).display==='none')infoHTML(stepDesc,sel)}else stepText();
  dirty=true;
}
function stepText(){const T=TXT[cond].steps[Math.max(active,0)];stepDesc.textContent=T[0];if(T[1]){const sm=document.createElement('small');sm.textContent=T[1];stepDesc.appendChild(sm)}}
function fill(){
  const T=TXT[cond];stepsLi.forEach((li,i)=>{const d=li.querySelector('.d>div');d.textContent='';const p=document.createElement('span');p.textContent=T.steps[i][0];d.appendChild(p);if(T.steps[i][1]){const sm=document.createElement('small');sm.textContent=T.steps[i][1];d.appendChild(sm)}});
  viewTag.textContent=T.name;kicker.textContent=scene().view;
  for(const k in scenes){const on=scenes[k]===scene();scenes[k].xr.style.display=scenes[k].sk.style.display=scenes[k].an.style.display=on?'':'none'}
  partgrid.textContent='';PARTLIST[cond].forEach(id=>{const b=document.createElement('button');b.type='button';b.className='part';b.dataset.p=id;b.id='part-'+id;b.setAttribute('aria-pressed','false');
    const t=document.createElement('b');t.textContent=PARTS[id][0];const u=document.createElement('span');u.textContent=PARTS[id][1];b.append(t,u);b.addEventListener('click',()=>select(id));partgrid.appendChild(b)});
  sel=null;svg.querySelectorAll('.sel').forEach(e=>e.classList.remove('sel'));infoHTML(partinfo,null);
  active=-1;dirty=true;
}
function setActive(i){if(i===active)return;active=i;wUser=null;stepsLi.forEach((li,j)=>li.classList.toggle('on',j===i));
  if(sel&&getComputedStyle(partinfo.parentElement).display==='none'){sel=null;svg.querySelectorAll('.sel').forEach(e=>e.classList.remove('sel'))}
  stepText();meter.querySelectorAll('span').forEach((sp,j)=>sp.classList.toggle('on',j===i))}

tabs.forEach(b=>b.addEventListener('click',()=>{if(b.dataset.c===cond)return;cond=b.dataset.c;tabs.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));fill();wUser=null;w=0;const total=story.offsetHeight-innerHeight,top=story.getBoundingClientRect().top+scrollY;scrollTo({top:top+total*REST[0],behavior:reduced?'auto':'smooth'})}));  // w=0: a troca de aba refaz a varredura
stepsLi.forEach((li,i)=>li.querySelector('button').addEventListener('click',()=>{const total=story.offsetHeight-innerHeight,top=story.getBoundingClientRect().top+scrollY;scrollTo({top:top+total*REST[i],behavior:reduced?'auto':'smooth'})}));
svg.addEventListener('click',e=>{const p=e.target.closest&&e.target.closest('[data-part]');if(p)select(p.dataset.part)});
xrayToggle.addEventListener('click',()=>{wUser=(w>.5)?0:1});
/* arrastar a alça */
let drag=false;
const toW=e=>{const r=svg.getBoundingClientRect(),x=clamp((e.clientX-r.left)/r.width),d=scene().dir;return d==='right'?1-x:x};
grip.addEventListener('pointerdown',e=>{drag=true;grip.setPointerCapture(e.pointerId);e.preventDefault()});
grip.addEventListener('pointermove',e=>{if(drag){wUser=toW(e);w=wUser}});
['pointerup','pointercancel'].forEach(t=>grip.addEventListener(t,()=>{drag=false}));
grip.addEventListener('keydown',e=>{const d=scene().dir==='right'?-1:1;if(e.key==='ArrowLeft'){wUser=clamp(w-.08*d);e.preventDefault()}if(e.key==='ArrowRight'){wUser=clamp(w+.08*d);e.preventDefault()}});

addEventListener('scroll',readScroll,{passive:true});addEventListener('resize',readScroll);
let vis=true;new IntersectionObserver(([e])=>vis=e.isIntersecting,{threshold:0}).observe(story);
let live=false;
function frame(){
  const ps=s,pw=w;s=reduced?target:mix(s,target,.11);if(Math.abs(s-target)<.0008)s=target;
  setActive(s<-.5?0:Math.round(s)+1);
  const wt=wUser!=null?wUser:wipeAuto();w=(reduced||drag)?wt:mix(w,wt,.16);if(Math.abs(w-wt)<.002)w=wt;
  if(vis&&(dirty||s!==ps||w!==pw||live)){
    const sc=scene(),sv=Math.max(s,0);
    live=cond==='joanete'?sc.update(sv):sc.update(sv,cond);setWipe(sc.dir,w);dirty=false;
    xrayToggle.textContent=w>.5?'Ver por fora':'Ver em raio-x';
    const f=(s+1)/4;meter.querySelector('i').style.width=(f*100)+'%';meter.querySelector('u').style.left=(f*100)+'%';
  }
  requestAnimationFrame(frame);
}
fill();readScroll();s=target;w=wipeAuto();frame();
window.__esquema={set(c,v,wv){cond=c;tabs.forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.c===c)));fill();target=s=v;setActive(v<-.5?0:Math.round(v)+1);wUser=(wv==null?null:wv);w=wUser!=null?wUser:wipeAuto();dirty=true},select};

/* ---------- miniaturas (filme do topo, cartões e capa em produção) ---------- */
const P=(host,d,fill,stroke,sw=0,op=1)=>el('path',{d,fill:fill||'none',stroke:stroke||'none','stroke-width':sw,opacity:op,'stroke-linejoin':'round','stroke-linecap':'round'},host);
const HI='rgba(236,243,252,.92)',DIM='rgba(170,196,228,.32)',MID='rgba(205,222,243,.55)',AL='#FF9A7B';
const ring=(host,c,r=1)=>{el('circle',{cx:c[0],cy:c[1],r:6*r,fill:AL},host);el('circle',{cx:c[0],cy:c[1],r:15*r,fill:'none',stroke:AL,'stroke-width':2.6*r},host)};
function miniDorsal(host){
  const g=scenes.dorsal.geo;
  g.RAYS.forEach(r=>{P(host,bone(r.b,r.h,62,32,60).d,DIM);const v=[r.tip[0]-r.h[0],r.tip[1]-r.h[1]],L=Math.hypot(v[0],v[1]),u=[v[0]/L,v[1]/L],at=t=>[r.h[0]+u[0]*t,r.h[1]+u[1]*t],z=L-20,l1=(z-14)*.48,l2=(z-14)*.29;
    [[14,14+l1-5,[46,26,38]],[14+l1+5,14+l1+l2-4,[34,22,30]],[14+l1+l2+4,z,[28,20,24]]].forEach(([a,b,w])=>P(host,bone(at(a),at(b),...w).d,DIM))});
  const f=bone(g.A,g.B,112,70,116),nM=f.n[0]>0?f.n:[-f.n[0],-f.n[1]];
  P(host,blob(add(g.B,[nM[0]*42,nM[1]*42+10]),26,52,-.1,.03),HI);P(host,f.d,HI,'#fff',3);
  const a=-.322,pA=add(g.B,[f.u[0]*10-6,f.u[1]*10-26]),pB=add(pA,[dir(a)[0]*176,dir(a)[1]*176]),qA=add(pB,[dir(a)[0]*12,dir(a)[1]*12]),qB=add(qA,[dir(a)[0]*128,dir(a)[1]*128]);
  P(host,bone(pA,pB,96,62,80).d,HI,'#fff',3);P(host,bone(qA,qB,78,50,60).d,HI,'#fff',3);
  ring(host,add(g.B,[nM[0]*60,12]),2.3);
}
function miniLateral(host,mode){
  const g=scenes.lateral.geo,heel=mode==='heel';
  P(host,spline(heel?g.skH:g.skN),'rgba(255,255,255,.06)','rgba(255,255,255,.22)',2);
  if(mode==='aquiles'){const st=g.stumps(30,16);P(host,st[0],'#E9C9A4','none',0,.85);P(host,st[1],'#E9C9A4','none',0,.85)}else P(host,spline(heel?g.tenH:g.tenN),'#E9C9A4','none',0,heel?.6:.3);
  P(host,bone([316,-260],[322,318],60,46,84).d,DIM);
  P(host,spline(heel?g.calH:g.calN),heel?HI:(mode==='run'?MID:DIM),heel?'#fff':'none',2);
  P(host,spline(g.talN),MID);
  [blob([450,381],17,27,.15),blob([444,442],27,22,.1),blob([497,393],25,21,.2)].forEach(d=>P(host,d,mode==='run'?MID:DIM));
  P(host,bone([470,447],[660,506],30,16,26).d,mode==='run'?HI:DIM,mode==='run'?'#fff':'none',1.6);P(host,bone([520,402],[680,476],34,20,34).d,mode==='run'?HI:DIM,mode==='run'?'#fff':'none',1.6);
  P(host,bone([262,-260],[281,368],24,15,34).d,mode==='ankle'?HI:MID,mode==='ankle'?'#fff':'none',1.6);
  if(mode==='ankle'){P(host,'M295 353L346 373','none','#F6E6CF',11);P(host,'M283 378L254 426','none','#F0DCC0',8,.8);ring(host,[320,363],.9)}
  if(heel){ring(host,[160,352]);el('circle',{cx:206,cy:499,r:7,fill:'#9DBBC0'},host)}
  if(mode==='aquiles')ring(host,[167,285],1.1);
}
miniDorsal(document.getElementById('miniHero'));miniDorsal(document.getElementById('icoJoanete'));
miniLateral(document.getElementById('icoHeel'),'heel');miniLateral(document.getElementById('icoAnkle'),'ankle');miniLateral(document.getElementById('icoAquiles'),'aquiles');
const goEsq=c=>{const b=document.getElementById('tab-'+c);if(b)b.click();const total=story.offsetHeight-innerHeight,top=story.getBoundingClientRect().top+scrollY;scrollTo({top:top+total*REST[0],behavior:reduced?'auto':'smooth'})};
document.querySelectorAll('[data-go]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();goEsq(a.dataset.go)}));
miniLateral(document.getElementById('miniHeel'),'heel');

/* ---------- entrada suave das seções (só o que está abaixo da dobra) ---------- */
const trail=document.getElementById('trail');
if(!reduced&&'IntersectionObserver' in window){
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.remove('pre');io.unobserve(e.target)}}),{threshold:.15});
  document.querySelectorAll('.rv').forEach(n=>{if(n.getBoundingClientRect().top>innerHeight*.9){n.classList.add('pre');io.observe(n)}});
  if(trail.getBoundingClientRect().top>innerHeight*.8){trail.classList.add('pre');io.observe(trail)}
}

/* ---------- bilhete: monta o pedido e leva ao WhatsApp ---------- */
const note=document.getElementById('note'),noteOut=document.getElementById('noteOut'),noteSend=document.getElementById('noteSend');
const rxOnde=document.getElementById('rxOnde'),rxQuando=document.getElementById('rxQuando');
function compose(){const o=note.querySelector('input[name=onde]:checked').value,q=note.querySelector('input[name=quando]:checked').value;rxOnde.textContent=o;rxQuando.textContent=q;
  const m='Olá, Dra. Larissa. Quero agendar uma avaliação. Sinto dor '+o+' e posso ir '+q+'.';noteOut.textContent='“'+m+'”';noteSend.href='https://wa.me/5521972896222?text='+encodeURIComponent(m)}
note.addEventListener('change',compose);note.addEventListener('submit',e=>e.preventDefault());compose();

/* ---------- toque onde dói: região do pé ↔ lista ↔ pedido do WhatsApp ---------- */
// onde: qual opção do bilhete recebe a região; v: como a região entra na frase (sem v, fica o texto da opção)
const DOR={dedao:{n:'Dedão',onde:1},dedos:{n:'Dedos',onde:4,v:'nos dedos'},bola:{n:'Bola do pé',onde:4,v:'na bola do pé'},arco:{n:'Arco, por dentro',onde:4,v:'no arco do pé'},
  calcbaixo:{n:'Calcanhar, embaixo',onde:2,v:'embaixo do calcanhar'},calctras:{n:'Calcanhar, atrás',onde:2,v:'atrás do calcanhar'},tornozelo:{n:'Tornozelo',onde:3},
  peito:{n:'Peito do pé',onde:4,v:'no peito do pé'},todo:{n:'O pé todo',onde:4,v:'no pé (tenho diabetes)'}};
const mapSola=document.getElementById('mapSola'),mapLado=document.getElementById('mapLado'),dorinfo=document.getElementById('dorinfo'),symp=document.getElementById('symp'),
      rows=[...symp.querySelectorAll('div[data-r]')],dortodo=document.querySelector('.dortodo');
const rg=(host,id)=>{const g=el('g',{class:'rg','data-r':id,tabindex:0,role:'button','aria-pressed':'false','aria-label':DOR[id].n},host);g.addEventListener('click',()=>pickDor(id));
  g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();pickDor(id)}});return g};
const ell=(host,cx,cy,rx,ry,r=0,cls)=>el('ellipse',Object.assign({cx,cy,rx,ry,transform:'rotate('+r+' '+cx+' '+cy+')'},cls?{class:cls}:{}),host);
// sola do pé direito (dedão à esquerda), desenhada à mão em 160 × 320
el('path',{class:'pele',d:'M78 314C56 314 46 296 47 270C48 246 54 228 50 206C46 184 34 164 30 138C26 112 30 92 46 84C66 75 110 76 128 86C144 95 146 118 140 146C134 176 126 206 124 238C122 270 118 314 78 314Z'},mapSola);
const TOES=[[82,44,10,14,-4],[103,50,9,12,4],[121,62,8,11,12],[136,78,7,10,20]];
ell(mapSola,52,52,16,23,-8,'pele');TOES.forEach(t=>ell(mapSola,...t,'pele'));
{const g=rg(mapSola,'dedao');ell(g,52,52,16,23,-8);el('path',{d:'M32 92C34 84 46 80 62 82L64 122C52 126 38 122 33 112Z'},g)}
{const g=rg(mapSola,'dedos');TOES.forEach(t=>ell(g,...t))}
el('path',{d:'M66 82C90 78 116 80 130 88C140 96 140 112 136 126C112 130 86 128 66 124Z'},rg(mapSola,'bola'));
el('path',{d:'M36 140C44 136 60 138 70 146L72 214C64 222 54 222 50 210C48 190 42 162 36 140Z'},rg(mapSola,'arco'));
ell(rg(mapSola,'calcbaixo'),84,278,32,28);
// lado de fora: o mesmo contorno de pele do esquema
el('path',{class:'pele',d:spline(scenes.lateral.geo.skN)},mapLado);
{const lg=el('linearGradient',{id:'ladoFade',x1:0,y1:0,x2:0,y2:1},el('defs',{},mapLado));el('stop',{offset:0,'stop-color':'#fff'},lg);el('stop',{offset:1,'stop-color':'#fff','stop-opacity':0},lg);
 el('rect',{x:90,y:148,width:600,height:150,fill:'url(#ladoFade)'},mapLado)}   // a perna some no alto, sem corte reto
el('path',{d:spline([[108,330],[150,322],[176,420],[204,498],[150,532],[104,472]])},rg(mapLado,'calctras'));
el('circle',{cx:300,cy:366,r:40},rg(mapLado,'tornozelo'));
el('path',{d:spline([[400,334],[480,372],[560,412],[604,430],[592,470],[470,440],[394,396]])},rg(mapLado,'peito'));
let dsel=null;
function setOnde(id){const D=DOR[id],r=document.getElementById('onde-'+D.onde);if(!r)return;
  if(D.onde===4){r.value=D.v;r.nextElementSibling.textContent=D.n}else if(D.v)r.value=D.v;r.checked=true;compose()}
function dorHTML(){dorinfo.textContent='';const c=document.createElement('span');c.className='caps';
  if(!dsel){c.textContent='Toque numa região';dorinfo.append(c,'O mapa mostra os problemas mais comuns de cada lugar do pé. Quem confirma o que é, é a avaliação.');return}
  c.textContent=DOR[dsel].n;dorinfo.append(c,'Pode estar ligado a: ');
  const rs=rows.filter(r=>r.dataset.r===dsel);rs.forEach((r,i)=>{const b=document.createElement('b');b.textContent=r.querySelector('dd').textContent;dorinfo.append(b,i<rs.length-1?', ':'.')});
  const acts=document.createElement('div');acts.className='acts';const ag=document.createElement('a');ag.className='btn primary';ag.href='#agendar';ag.textContent='Agendar avaliação';
  ag.addEventListener('click',()=>setOnde(dsel));acts.appendChild(ag);
  rs.filter(r=>r.dataset.esq).forEach(r=>{const m=document.createElement('a');m.className='more';m.href='#esquema';m.textContent='Ver '+r.querySelector('dd').textContent.toLowerCase()+' no esquema';
    m.addEventListener('click',e=>{e.preventDefault();goEsq(r.dataset.esq)});acts.appendChild(m)});
  const sm=document.createElement('small');sm.textContent='Só a avaliação confirma o que é. Ao agendar, a região já vai no pedido.';dorinfo.append(acts,sm)}
function pickDor(id){dsel=(id===dsel)?null:id;
  document.querySelectorAll('.dormap .rg').forEach(g=>{const on=g.dataset.r===dsel;g.classList.toggle('on',on);g.setAttribute('aria-pressed',String(on))});
  dortodo.setAttribute('aria-pressed',String(dsel==='todo'));symp.classList.toggle('has-sel',!!dsel);rows.forEach(r=>r.classList.toggle('on',r.dataset.r===dsel));
  if(dsel)setOnde(dsel);dorHTML()}
rows.forEach(r=>r.addEventListener('click',()=>pickDor(r.dataset.r)));dortodo.addEventListener('click',()=>pickDor('todo'));dorHTML();

/* ---------- barra de agendar no celular: fora do topo, do esquema (que precisa da tela inteira) e da seção Agendar ---------- */
const dock=document.getElementById('dock'),dockBtn=dock.querySelector('a'),seen=new Map();
if('IntersectionObserver' in window){
  const io=new IntersectionObserver(es=>{es.forEach(e=>seen.set(e.target.id,e.isIntersecting));const on=![...seen.values()].some(Boolean);
    dock.classList.toggle('on',on);dockBtn.tabIndex=on?0:-1;dock.setAttribute('aria-hidden',String(!on))},{threshold:0});
  ['inicio','story','agendar'].forEach(id=>io.observe(document.getElementById(id)));
}
})();
</script>
