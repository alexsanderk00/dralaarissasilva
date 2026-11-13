<script>
(()=>{
/* ---------- utilidades ---------- */
const NS='http://www.w3.org/2000/svg';
const el=(t,a={},p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e};
const clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const mix=(a,b,t)=>a+(b-a)*t;
const mixP=(a,b,t)=>[mix(a[0],b[0],t),mix(a[1],b[1],t)];
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]];
const ease=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const seg=(s,a,b)=>ease(clamp((s-a)/(b-a)));
const win=(s,a,b,c,d)=>Math.min(clamp((s-a)/(b-a)),1-clamp((s-c)/(d-c)));
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const f1=n=>n.toFixed(1);

/* curva suave por pontos (Catmull-Rom → Bézier) */
function spline(pts,closed=true){
  const n=pts.length,P=i=>closed?pts[(i+n)%n]:pts[clamp(i,0,n-1)];
  let d='M'+f1(pts[0][0])+' '+f1(pts[0][1]);
  for(let i=0;i<(closed?n:n-1);i++){
    const p0=P(i-1),p1=P(i),p2=P(i+1),p3=P(i+2);
    d+='C'+f1(p1[0]+(p2[0]-p0[0])/6)+' '+f1(p1[1]+(p2[1]-p0[1])/6)+' '+f1(p2[0]-(p3[0]-p1[0])/6)+' '+f1(p2[1]-(p3[1]-p1[1])/6)+' '+f1(p2[0])+' '+f1(p2[1]);
  }
  return d+(closed?'Z':'');
}
/* osso longo: base A, cabeça B, larguras na base, no meio e na cabeça; t0–t1 recorta um fragmento */
function bone(A,B,wA,wM,wB,t0=0,t1=1,off=[0,0]){
  const dx=B[0]-A[0],dy=B[1]-A[1],L=Math.hypot(dx,dy)||1,ux=dx/L,uy=dy/L,nx=-uy,ny=ux;
  const hw=t=>t<.5?wM/2+(wA-wM)/2*Math.pow(1-t/.5,2.3):wM/2+(wB-wM)/2*Math.pow((t-.5)/.5,2.3);
  let ts=[0,.07,.18,.32,.5,.68,.82,.93,1].filter(t=>t>t0+.02&&t<t1-.02);ts=[t0,...ts,t1];
  const at=(t,h)=>[A[0]+ux*L*t+nx*h+off[0],A[1]+uy*L*t+ny*h+off[1]];
  const k=t=>(t<=0||t>=1)?.78:1;
  const ring=ts.map(t=>at(t,hw(t)*k(t)));
  if(t1>=1)ring.push(at(1+wB*.3/L,0));else ring.push(at(t1+.004,hw(t1)*.6),at(t1+.004,-hw(t1)*.6));
  ring.push(...ts.slice().reverse().map(t=>at(t,-hw(t)*k(t))));
  if(t0<=0)ring.push(at(-wA*.3/L,0));else ring.push(at(t0-.004,-hw(t0)*.6),at(t0-.004,hw(t0)*.6));
  return {d:spline(ring),at,hw,u:[ux,uy],n:[nx,ny],L};
}
function blob(c,rx,ry,rot=0,sq=.08,k=10){
  const pts=[];for(let i=0;i<k;i++){const a=i/k*Math.PI*2,r=1+sq*Math.cos(a*2+1)+sq*.6*Math.sin(a*3);
    const x=Math.cos(a)*rx*r,y=Math.sin(a)*ry*r;pts.push([c[0]+x*Math.cos(rot)-y*Math.sin(rot),c[1]+x*Math.sin(rot)+y*Math.cos(rot)])}
  return spline(pts);
}
const dir=a=>[Math.sin(a),-Math.cos(a)];
/* rótulo com marcador (ponto + anel), linha até a borda mais próxima do texto e texto em até 2 linhas sobre uma placa escura.
   Os rótulos ficam fora do recorte do raio-X: some o rótulo cujo ponto está do lado da pele, em vez de cortar a palavra ao meio. */
const small=matchMedia('(max-width:979px)');
const WIPE={x:600,dir:'left'};      // posição da linha de varredura no filme, atualizada por setWipe
const fontsReady=document.fonts?document.fonts.ready:Promise.resolve();
function label(parent,cool,getK=()=>1,toFilm=p=>p){
  const g=el('g',{class:'lb'+(cool?' cool':'')},parent),ln=el('path',{},g),plate=el('rect',{class:'plate'},g),ring=el('circle',{class:'ring'},g),dot=el('circle',{class:'dot'},g),tx=el('text',{},g);let last='',bb=null;
  fontsReady.then(()=>{last=''});
  return (p,q,text,o=1,anchor='start')=>{
    const fp=toFilm(p),side=WIPE.dir==='left'?WIPE.x-fp[0]:fp[0]-WIPE.x;o*=clamp((side+12)/36);
    g.style.opacity=o;g.style.display=o<.01?'none':'';if(o<.01)return;
    const k=getK()*(small.matches?1.18:1),sgn=anchor==='start'?1:-1;ring.setAttribute('r',8.5*k);dot.setAttribute('r',3.6*k);ln.style.strokeWidth=1.6*k;
    ring.setAttribute('cx',p[0]);ring.setAttribute('cy',p[1]);dot.setAttribute('cx',p[0]);dot.setAttribute('cy',p[1]);
    const key=text+anchor+f1(q[0])+f1(q[1])+k;if(key!==last){last=key;tx.style.fontSize=(13.6*k)+'px';tx.style.letterSpacing=(small.matches?1.1:1.8)*k+'px';tx.style.strokeWidth=5*k+'px';
      tx.textContent='';const lines=text.split('\n');
      lines.forEach((l,i)=>{const t=el('tspan',{x:q[0]+sgn*9*k,y:q[1]+5.5*k+(i-(lines.length-1)/2)*19*k},tx);t.textContent=l});
      tx.setAttribute('text-anchor',anchor);
      const b=tx.getBBox(),px=6*k,py=3*k;bb={x:b.x-px,y:b.y-py,w:b.width+2*px,h:b.height+2*py};
      plate.setAttribute('x',f1(bb.x));plate.setAttribute('y',f1(bb.y));plate.setAttribute('width',f1(bb.w));plate.setAttribute('height',f1(bb.h));plate.setAttribute('rx',4*k)}
    // linha: de lado com cotovelo quando o ponto está à esquerda ou à direita da placa; reta até a borda de cima ou de baixo quando está acima ou abaixo
    let d='';const x0=bb.x,x1=bb.x+bb.w,y0=bb.y,y1=bb.y+bb.h,cy=clamp(q[1],y0,y1);
    if(p[0]<x0||p[0]>x1){const ex=p[0]<x0?x0:x1,s=p[0]<x0?-1:1,elx=ex+s*22*k,el2=(s<0?p[0]<elx:p[0]>elx)?[elx,cy]:null;
      d='M'+f1(p[0])+' '+f1(p[1])+(el2?'L'+f1(el2[0])+' '+f1(el2[1]):'')+'L'+f1(ex)+' '+f1(cy)}
    else if(p[1]<y0||p[1]>y1)d='M'+f1(p[0])+' '+f1(p[1])+'L'+f1(p[0])+' '+f1(p[1]<y0?y0:y1);
    ln.setAttribute('d',d||'M0 0');ln.style.display=d?'':'none';
  };
}
const setD=(e,d)=>e.setAttribute('d',d);
const show=(e,o)=>{e.style.opacity=o;e.style.display=o<.01?'none':''};

const svg=document.getElementById('svg');
const defs=el('defs',{},svg);
function fadeMask(id,x1,y1,x2,y2){const g=el('linearGradient',{id:id+'g',gradientUnits:'userSpaceOnUse',x1,y1,x2,y2},defs);el('stop',{offset:0,'stop-color':'#fff'},g);el('stop',{offset:1,'stop-color':'#000'},g);
  const m=el('mask',{id,maskUnits:'userSpaceOnUse',x:-3000,y:-3000,width:9000,height:9000},defs);el('rect',{x:-3000,y:-3000,width:9000,height:9000,fill:'url(#'+id+'g)'},m)}
fadeMask('mB',0,1085,0,1215);fadeMask('mR',452,0,640,0);fadeMask('mRp',470,0,610,0);
const cXr=el('rect',{y:-20,height:700},el('clipPath',{id:'cX'},defs)),cSr=el('rect',{y:-20,height:700},el('clipPath',{id:'cS'},defs));
/* a mesma foto, fria e apagada, faz o papel do tecido mole no lado do raio-X */
const xt=el('filter',{id:'xrayTint','color-interpolation-filters':'sRGB'},defs);el('feColorMatrix',{type:'matrix',values:'.13 .26 .05 0 0  .21 .42 .08 0 .01  .24 .47 .09 0 .03  0 0 0 .62 0'},xt);

/* =====================================================================
   CENA 1 · vista de cima (joanete), desenhada no espaço da foto (1400 × 1867 px; 55 px ≈ 1 cm). A foto (img/pe_cima.webp) é deformada para esse espaço; ver CLAUDE.md
   ===================================================================== */
function Dorsal(){
  const SC=.5,TR='translate(-112 -66) scale(.5)',G=(x,y)=>[(x+112)/SC,(y+66)/SC];      // G: posição no filme (0–600) → espaço da foto
  const xr=el('g',{'clip-path':'url(#cX)'},svg),sk=el('g',{'clip-path':'url(#cS)','pointer-events':'none'},svg),root=el('g',{transform:TR},xr),body=el('g',{mask:'url(#mB)'},root),skRoot=el('g',{transform:TR,mask:'url(#mB)'},sk),parts={};
  const PH={href:'{{IMG_PE_CIMA}}',x:420,y:270,width:590,height:1110};
  const ghost=el('image',Object.assign({filter:'url(#xrayTint)'},PH),body);el('image',PH,skRoot);
  const soft=el('g',{class:'soft',opacity:0,style:'stroke-width:92px'},body),dimG=el('g',{class:'bn dim'},body),hiG=el('g',{class:'bn hi'},body);
  const tool=el('g',{},root),ann=el('g',{},root),lbG=el('g',{transform:TR},svg),lb=c=>label(lbG,c,()=>1/SC,p=>[p[0]*SC-112,p[1]*SC-66]);
  const mk=(grp,part)=>{const s=el('path',{style:'stroke-width:inherit'},soft),b=el('path',part?{'data-part':part}:{},grp);if(part)(parts[part]=parts[part]||[]).push(b);
    return{set:d=>{setD(s,d);setD(b,d)},vis:v=>{s.style.display=b.style.display=v?'':'none'}}};
  // ossos fixos: tarsos, metatarsos 2–5 e dedos menores (cabeça → ponta do dedo, medidos na foto)
  [[[852,1150],60,52,0],[[768,1152],40,50,.1],[[698,1158],40,50,.1],[[602,1178],64,56,.2]].forEach(([c,rx,ry,r])=>mk(dimG).set(blob(c,rx,ry,r)));
  const RAYS=[{b:[772,1092],h:[776,742],tip:[712,395]},{b:[702,1098],h:[692,768],tip:[625,425]},{b:[632,1104],h:[612,798],tip:[562,495]},{b:[562,1112],h:[534,838],tip:[508,588]}];   // pontas medidas no pé da foto atual (IMG_0200)
  RAYS.forEach(r=>{mk(dimG,'metas').set(bone(r.b,r.h,62,32,60).d);
    const v=[r.tip[0]-r.h[0],r.tip[1]-r.h[1]],L=Math.hypot(v[0],v[1]),u=[v[0]/L,v[1]/L],at=t=>[r.h[0]+u[0]*t,r.h[1]+u[1]*t];
    const a=14,z=L-20,l1=(z-a)*.48,l2=(z-a)*.29;
    [[a,a+l1-5,[46,26,38]],[a+l1+5,a+l1+l2-4,[34,22,30]],[a+l1+l2+4,z,[28,20,24]]].forEach(([t0,t1,w])=>mk(dimG,'dedos').set(bone(at(t0),at(t1),...w).d))});
  const ses=[mk(dimG,'sesamoides'),mk(dimG,'sesamoides')];
  const eminP=el('path',{style:'stroke:none'},hiG),emin={set:d=>setD(eminP,d),vis:v=>{eminP.style.display=v?'':'none'}};
  const m1=mk(hiG,'m1'),m1a=mk(hiG,'m1'),m1b=mk(hiG,'m1'),p1=mk(hiG,'halux'),p2=mk(hiG,'halux');
  const calP=el('path',{style:'stroke:none;fill:rgba(236,243,252,.82)'},hiG),callus={set:d=>setD(calP,d),vis:v=>{calP.style.display=v?'':'none'}};
  const A=[862,1078],B=[906,728];
  // marcações (traços em px da foto: o dobro do que aparece no filme)
  const axM=el('path',{class:'cor','stroke-width':4.4},ann),axH=el('path',{class:'cor','stroke-width':4.4},ann),wedge=el('path',{fill:'rgba(240,113,76,.28)',stroke:'#F0714C','stroke-width':4},ann);
  const cut=el('path',{class:'cor','stroke-width':5.2,'stroke-dasharray':'10 10'},ann),portals=el('path',{class:'cor','stroke-width':8},ann);
  const burr=el('g',{},tool),burrL=el('path',{stroke:'#DCE6F2','stroke-width':6.4,'stroke-linecap':'round',fill:'none'},burr),burrH=el('path',{stroke:'#DCE6F2','stroke-width':18,'stroke-linecap':'round',fill:'none',opacity:.9},burr);
  const scr=[0,1].map(()=>({l:el('path',{stroke:'#fff','stroke-width':8.4,'stroke-linecap':'round',fill:'none'},tool),t:el('path',{stroke:'#113358','stroke-width':8.4,'stroke-dasharray':'2.8 8',fill:'none',opacity:.55},tool),h:el('circle',{r:9,fill:'#fff'},tool)}));
  const arrow=el('path',{class:'cor','stroke-width':4.8},ann);
  const L={m1:lb(1),hal:lb(1),ses:lb(1),jo:lb(0),dev:lb(0),fur:lb(0),bro:lb(0),des:lb(0),par:lb(0),con:lb(1),eixo:lb(1)};
  const pt=p=>f1(p[0])+' '+f1(p[1]);
  function update(s){
    const shift=seg(s,1.5,1.85),dev=1-shift,full=bone(A,B,112,70,116),u=full.u,nM=full.n[0]>0?full.n:[-full.n[0],-full.n[1]];   // nM: normal para o lado medial (direita)
    const cutT=.72,cP=full.at(cutT,0),off=[-nM[0]*46*shift,-nM[1]*46*shift],split=s>=1.44;
    m1.vis(!split);m1a.vis(split);m1b.vis(split);
    if(!split)m1.set(full.d);else{m1a.set(bone(A,B,112,70,116,0,cutT).d);m1b.set(bone(A,B,112,70,116,cutT,1,off).d)}
    const head=add(B,off);
    ses[0].set(blob(add(B,[-66*nM[0],20]),15,19));ses[1].set(blob(add(B,[-30*nM[0],24]),15,19));
    // dedão: na foto ele aponta 18° para os outros dedos; a correção traz o eixo de volta
    const a=mix(-.07,-.322,dev),pA=add(head,[u[0]*10-6*dev,u[1]*10-26]),pB=add(pA,[dir(a)[0]*176,dir(a)[1]*176]),qA=add(pB,[dir(a)[0]*12,dir(a)[1]*12]),qB=add(qA,[dir(a)[0]*128,dir(a)[1]*128]);
    p1.set(bone(pA,pB,96,62,80).d);p2.set(bone(qA,qB,78,50,60).d);
    const k=1-shift*.92;emin.vis(k>.03);if(k>.03)emin.set(blob(add(head,[nM[0]*42,nM[1]*42+10]),26*k,52*k,-.1,.03));
    const cal=seg(s,2.25,2.9);callus.vis(cal>.02);if(cal>.02)callus.set(blob(add(cP,[-12,2]),44*cal,26*cal,.12,.02));
    ghost.style.opacity=.9*(1-shift);soft.setAttribute('opacity',.085*shift);
    // eixos e ângulo
    const o0=1-clamp((s-.22)/.25),o1=win(s,.55,.9,1.06,1.22),o3=seg(s,2.55,2.9);
    show(axM,o1);setD(axM,'M'+pt(add(A,[u[0]*60,u[1]*60]))+'L'+pt(add(B,[u[0]*170,u[1]*170])));
    show(axH,o1);setD(axH,'M'+pt(pA)+'L'+pt(add(pA,[dir(a)[0]*330,dir(a)[1]*330])));
    const r=128,w0=add(pA,[u[0]*r,u[1]*r]),w1=add(pA,[dir(a)[0]*r,dir(a)[1]*r]);show(wedge,o1);setD(wedge,'M'+pt(pA)+'L'+pt(w0)+'A'+r+' '+r+' 0 0 0 '+pt(w1)+'Z');
    // corte, furinhos, broca, parafusos
    const hw=full.hw(cutT)+14,c0=add(cP,[nM[0]*hw,nM[1]*hw]),c1=add(cP,[-nM[0]*hw,-nM[1]*hw]),cp=seg(s,1.25,1.45);
    show(cut,win(s,1.2,1.27,2.2,2.6));setD(cut,'M'+pt(c0)+'L'+pt(mixP(c0,c1,cp)));
    const sS=[add(full.at(.44,0),[nM[0]*37,nM[1]*37]),add(full.at(.32,0),[nM[0]*40,nM[1]*40])],pp=[add(c0,[nM[0]*34,nM[1]*34]),add(sS[1],[nM[0]*30,nM[1]*30])];
    show(portals,win(s,1,1.1,2.25,2.6));setD(portals,pp.map(p=>'M'+pt(add(p,[0,-13]))+'L'+pt(add(p,[0,13]))).join(''));
    const bo=win(s,1.04,1.14,1.5,1.62),slide=mix(220,0,seg(s,1.05,1.25))+mix(0,260,seg(s,1.5,1.64)),jit=(cp>0&&cp<1&&!reduced)?Math.sin(performance.now()/38)*3:0;
    const tip=add(mixP(c0,c1,cp*.92),[slide,jit]),tail=add(tip,[300,-68]);show(burr,bo);
    setD(burrL,'M'+pt(tip)+'L'+pt(tail));setD(burrH,'M'+pt(add(tip,[124,-28]))+'L'+pt(tail));
    const sE=[add(head,[-18,18]),add(head,[16,10])];
    scr.forEach((o,i)=>{const pr=seg(s,1.8+i*.05,1.95+i*.05),e=mixP(sS[i],sE[i],pr),op=pr>0?mix(1,.62,seg(s,2.3,2.8)):0;[o.l,o.t,o.h].forEach(x=>show(x,op));
      const d='M'+pt(sS[i])+'L'+pt(e);setD(o.l,d);setD(o.t,d);o.h.setAttribute('cx',sS[i][0]);o.h.setAttribute('cy',sS[i][1])});
    const ah=add(head,[nM[0]*104,-12]);show(arrow,win(s,1.5,1.56,1.84,1.92));setD(arrow,'M'+pt(add(ah,[68,0]))+'L'+pt(ah)+'M'+pt(add(ah,[18,-14]))+'L'+pt(ah)+'L'+pt(add(ah,[18,14])));
    // rótulos (posições no filme, convertidas por G)
    L.hal(mixP(pA,pB,.5),G(410,222),'DEDÃO\n(HÁLUX)',o0);L.ses(add(B,[-66*nM[0],20]),G(410,318),'SESAMOIDES',o0);L.m1(full.at(.45,0),G(410,400),'1º METATARSO',o0);
    L.jo(add(head,[nM[0]*60,12]),G(410,330),'JOANETE',o1);L.dev(mixP(qA,qB,.45),G(410,150),'DEDÃO\nDESVIADO',o1);
    L.fur(pp[1],G(410,500),'FURINHOS\nNA PELE',win(s,1.02,1.12,1.48,1.58));L.bro(add(tip,[190,-44]),G(410,300),'BROCA FINA',win(s,1.12,1.22,1.48,1.58));
    L.des(add(head,[nM[0]*40,-4]),G(410,262),'CABEÇA VOLTA\nPARA O LUGAR',win(s,1.56,1.66,1.8,1.9));
    L.par(sS[0],G(410,452),'PARAFUSOS',win(s,1.9,2,2.3,2.5));
    L.con(add(cP,[12,8]),G(410,412),'OSSO\nCONSOLIDADO',o3);L.eixo(mixP(pA,pB,.5),G(410,222),'DEDÃO\nALINHADO',o3);
    return cp>0&&cp<1;
  }
  return{xr,sk,an:lbG,update,parts,view:'Vista de cima',dir:'right',endW:()=>1,geo:{A,B,RAYS}};
}

/* =====================================================================
   CENA 3 · vista de baixo (fascite plantar), desenhada no espaço da foto da sola (1500 × 2000 px, img/pe_sola.webp: pé direito pela planta,
   dedão à direita, calcanhar embaixo). Pontos medidos na foto: ponta e base de cada dedo, cabeças dos metatarsos, calcanhar.
   ===================================================================== */
function Plantar(){
  const SC=.36,OX=0,OY=-41,TR='translate('+OX+' '+OY+') scale('+SC+')',G=(x,y)=>[(x-OX)/SC,(y-OY)/SC];   // G: posição no filme (0–600) → espaço da foto
  const xr=el('g',{'clip-path':'url(#cX)'},svg),sk=el('g',{'clip-path':'url(#cS)','pointer-events':'none'},svg),root=el('g',{transform:TR},xr),skRoot=el('g',{transform:TR},sk),parts={};
  const PH={href:'{{IMG_PE_SOLA}}',x:0,y:0,width:1500,height:2000};
  const ghost=el('image',Object.assign({filter:'url(#xrayTint)',opacity:.9},PH),root);el('image',PH,skRoot);
  const dimG=el('g',{class:'bn dim'},root),midG=el('g',{class:'bn mid'},root),hiG=el('g',{class:'bn hi'},root);
  const reg=(e,part)=>{if(part){e.setAttribute('data-part',part);(parts[part]=parts[part]||[]).push(e)}return e};
  const P=(g,d,part)=>reg(el('path',{d},g),part);
  // retropé e mediopé
  P(dimG,blob([870,1440],95,85,.2));                                   // cabeça do tálus (por cima do calcâneo)
  const calc=P(hiG,blob([770,1555],150,205,-.1,.05,12),'calcaneo');
  P(midG,blob([915,1335],100,58,-.25));P(midG,blob([600,1295],86,96,.15));   // navicular, cuboide
  [[960,1225,58,68],[852,1200,44,56],[752,1215,44,56]].forEach(([x,y,rx,ry])=>P(midG,blob([x,y],rx,ry,.05)));   // cuneiformes
  // metatarsos (base → cabeça) e dedos (cabeça → ponta), medidos na foto
  const RAYS=[{b:[965,1150],h:[1040,790],tip:[1040,240],w:[100,62,104],big:1},{b:[835,1110],h:[790,705],tip:[722,300]},{b:[735,1130],h:[690,760],tip:[640,450]},
              {b:[645,1160],h:[592,830],tip:[528,565]},{b:[545,1215],h:[482,925],tip:[410,715]}];
  RAYS.forEach(r=>{P(midG,bone(r.b,r.h,...(r.w||[64,34,62])).d,'metas');
    const v=[r.tip[0]-r.h[0],r.tip[1]-r.h[1]],L=Math.hypot(v[0],v[1]),u=[v[0]/L,v[1]/L],at=t=>[r.h[0]+u[0]*t,r.h[1]+u[1]*t],a=34,z=L-26;
    const segs=r.big?[[a,a+(z-a)*.55-8,[92,60,78]],[a+(z-a)*.55+8,z,[80,52,62]]]:[[a,a+(z-a)*.48-6,[48,28,40]],[a+(z-a)*.48+6,a+(z-a)*.77-5,[38,24,32]],[a+(z-a)*.77+5,z,[32,22,26]]];
    segs.forEach(([t0,t1,w])=>P(dimG,bone(at(t0),at(t1),...w).d,r.big?'halux':null))});
  P(hiG,blob([995,800],28,36,.1));P(hiG,blob([1085,785],28,36,.1));   // sesamoides
  // fáscia plantar: leque que sai da tuberosidade medial do calcâneo e abre até a base de cada dedo
  const O=[815,1672],fan=reg(el('path',{class:'tendon',d:spline([[760,1665],[872,1662],[985,1330],[1100,850],[1010,760],[800,690],[688,742],[585,815],[470,915],[548,1250]])}),'fascia');
  root.insertBefore(fan,hiG);
  const slips=el('g',{},root);RAYS.forEach(r=>el('path',{d:'M'+O[0]+' '+(O[1]-40)+'Q'+f1((O[0]+r.h[0])/2)+' '+f1((O[1]+r.h[1])/2+40)+' '+r.h[0]+' '+(r.h[1]+20),stroke:'#F3DABB','stroke-width':11,'stroke-linecap':'round',fill:'none',opacity:.8},slips));
  // origem inflamada, aplicador de ondas de choque e as ondas
  const infl=el('path',{fill:'#F0714C'},root),probe=el('g',{},root),prRing=el('circle',{r:74,fill:'rgba(114,198,162,.22)',stroke:'#72C6A2','stroke-width':10},probe),
        prHandle=el('path',{fill:'#DCE6F2',stroke:'#fff','stroke-width':4},probe),waves=[0,1,2].map(()=>el('circle',{fill:'none',stroke:'#9FE3C5','stroke-width':9},root));
  const lbG=el('g',{transform:TR},svg),lb=c=>label(lbG,c,()=>1/SC,p=>[p[0]*SC+OX,p[1]*SC+OY]);
  const L={fas:lb(1),cal:lb(1),met:lb(1),dor:lb(0),des:lb(0),ond:lb(0),apl:lb(0),rec:lb(1)};
  function update(s){
    const t=performance.now()/1000,fi=seg(s,.55,1)*(1-.75*seg(s,2.3,2.9)),pul=(!reduced&&fi>.5)?1+.12*Math.sin(t*4):1;
    fan.style.opacity=mix(.3,.55,seg(s,0,.5));fan.style.fill=fi>.4?'#F3B79F':'';slips.style.opacity=mix(.6,1,seg(s,0,.5));
    show(infl,fi*.92);setD(infl,blob(O,(46+30*fi)*pul,(34+22*fi)*pul,.2,.05));
    // ondas de choque: o aplicador encosta na pele sobre o ponto da dor (de baixo é um círculo) e as ondas se abrem a partir dele
    const pin=seg(s,1.3,1.6)*(1-seg(s,2.3,2.6)),wv=win(s,1.45,1.6,2.3,2.5);show(probe,pin);
    probe.setAttribute('transform','translate('+f1(O[0]+mix(260,0,pin))+' '+f1(O[1]+mix(120,0,pin))+')');setD(prHandle,'M40 50L210 250L250 214L80 14Z');
    waves.forEach((e,i)=>{const ph=reduced?(i+1)/4:((t*.9+i/3)%1);e.setAttribute('cx',O[0]);e.setAttribute('cy',O[1]);e.setAttribute('r',f1(80+ph*190));show(e,wv*(1-ph)*.9)});
    const o0=1-clamp((s-.22)/.25),o1=win(s,.6,.9,1.06,1.22),o3=seg(s,2.55,2.9);
    L.fas([840,1250],G(445,250),'FÁSCIA\nPLANTAR',o0);L.cal([700,1640],G(445,470),'CALCÂNEO',o0);L.met([690,900],G(445,150),'METATARSOS',o0);
    L.dor(O,G(445,530),'DÓI AO PISAR,\nDE MANHÃ',o1);L.des([850,1560],G(445,400),'A FÁSCIA SE\nDESGASTA AQUI',o1);
    L.ond(O,G(445,520),'ONDAS DE\nCHOQUE,\nSEM CORTE',wv);L.apl([O[0]+150,O[1]+130],G(445,605),'APLICADOR\nNA PELE',win(s,1.5,1.65,2.3,2.5));
    L.rec(O,G(445,520),'ALONGAMENTO\nE CALÇADO',o3);
    return fi>.5||wv>0;
  }
  return{xr,sk,an:lbG,update,parts,view:'Vista de baixo',dir:'right',endW:()=>.62};
}

/* =====================================================================
   CENA 2 · vista de lado (calcanhar e tornozelo)
   ===================================================================== */
function Lateral(){
  const xr=el('g',{'clip-path':'url(#cX)'},svg),sk=el('g',{'clip-path':'url(#cS)','pointer-events':'none'},svg),phX=el('g',{mask:'url(#mRp)'},xr),root=el('g',{},xr),body=el('g',{mask:'url(#mR)'},root),phS=el('g',{mask:'url(#mRp)'},sk),parts={};let K=1,MA=[1,0,1,0,0],QQ=null;
  /* foto real de lado (1200 × 1800 px). O esqueleto é levado até ela por uma afinidade: escala em x, escala em y e inclinação da sola (perspectiva). */
  const PHL={href:'{{IMG_PE_LADO}}',x:0,y:0,width:569,height:852};el('image',Object.assign({filter:'url(#xrayTint)',opacity:.9},PHL),phX);el('image',PHL,phS);
  /* encaixe: esqueleto -> pixels da foto (x*.53, y*.85, ancorado no calcanhar e na sola) -> palco (zoom Z) */
  const FIT=(()=>{const Z=1.12,kx=.5724,ky=.517,hx=28,sy0=832,ox=44,oy=-355;   /* kx/ky medidos no pé da foto IMG_3078 (calcanhar, ponta dos dedos, dobra do tornozelo) */ const a=Z*kx,d=Z*ky,e=Z*(hx-kx*117)+ox,f=Z*(sy0-ky*530)+oy;return{MA:[a,0,d,e,f],PT:'matrix('+Z+' 0 0 '+Z+' '+ox+' '+oy+')'}})();
  let LX=54;const MP=p=>[MA[0]*p[0]+MA[3],MA[1]*p[0]+MA[2]*p[1]+MA[4]],QH=q=>[MA[0]*q[0]+MA[3]+LX,MA[2]*q[1]+MA[4]],QT=QH;
  const skin=el('path',{fill:'none',stroke:'none',display:'none'},body);
  const tib=el('g',{class:'bn dim'},body);const tibia=el('path',{},tib);
  const foot=el('g',{},body);
  const tend=el('path',{class:'tendon','data-part':'aquiles'},foot),fasc=el('path',{'data-part':'fascia',stroke:'#E9C9A4','stroke-width':6,'stroke-linecap':'round',fill:'none',opacity:.4,d:'M196 498C300 516 440 520 620 522'},foot);
  const tU=el('path',{class:'tendon','data-part':'aquiles'},foot),tL=el('path',{class:'tendon','data-part':'aquiles'},foot),tCal=el('path',{fill:'#F3DABB'},foot);
  const gDim=el('g',{class:'bn dim'},foot),gCal=el('g',{class:'bn hi'},foot),gTal=el('g',{class:'bn hi'},foot);
  const calc=el('path',{'data-part':'calcaneo'},gCal),talus=el('path',{'data-part':'talus'},gTal);
  const arcoP=[blob([450,381],17,27,.15),blob([444,442],27,22,.1),blob([497,393],25,21,.2),bone([470,447],[660,506],30,16,26).d,bone([520,402],[680,476],34,20,34).d].map(d=>el('path',{d,'data-part':'arco'},gDim));
  const fibG=el('g',{class:'bn hi'},body),fibula=el('path',{'data-part':'fibula'},fibG);
  const lig=el('g',{},body),extra=el('g',{},root);
  /* pé plano: tendão tibial posterior (passa por dentro do tornozelo, atrás do maléolo medial, até o navicular); aqui só a sombra dele, tracejada */
  const tibP=el('path',{'data-part':'tibpost',stroke:'#E9C9A4','stroke-width':7,'stroke-dasharray':'10 7','stroke-linecap':'round',fill:'none'},body);
  const eixoT=el('path',{class:'cor','stroke-width':2.6,'stroke-dasharray':'7 6'},extra),insole=el('path',{fill:'rgba(114,198,162,.55)',stroke:'#72C6A2','stroke-width':2},extra);
  const ann=el('g',{},svg);
  setD(tibia,bone([294,-260],[322,318],60,46,84).d);setD(fibula,bone([240,-260],[281,368],24,15,34).d);   /* inclinadas como a perna da foto */
  const talN=[[268,338],[292,324],[322,319],[352,326],[374,340],[400,353],[424,367],[430,388],[412,402],[380,401],[346,399],[312,403],[282,397],[264,377]];
  setD(talus,spline(talN));
  const calN=[[177,368],[202,367],[233,381],[263,399],[302,409],[346,405],[389,411],[410,429],[404,457],[364,463],[312,467],[262,481],[212,495],[173,486],[152,453],[152,404]];
  const calH=calN.map(p=>p.slice());calH[0]=[157,344];calH[1]=[198,357];calH[15]=[144,392];
  const calR=calN.map(p=>p.slice());calR[0]=[190,386];calR[1]=[214,382];calR[15]=[160,410];
  const tenN=[[184,-260],[170,120],[158,260],[149,340],[143,392],[146,432],[160,438],[166,402],[173,350],[186,260],[204,120],[226,-260]];
  const tenH=tenN.map(p=>p.slice());tenH[3]=[141,332];tenH[4]=[133,386];tenH[5]=[140,432];tenH[7]=[156,398];tenH[8]=[164,342];
  /* tendão em dois cotos (ruptura): borda de trás xp(y), borda da frente xa(y) */
  const xp=y=>y<120?184-(y+260)*14/380:y<260?170-(y-120)*12/140:y<340?158-(y-260)*9/80:y<392?149-(y-340)*6/52:143;
  const xa=y=>y<120?226-(y+260)*22/380:y<260?204-(y-120)*18/140:y<350?186-(y-260)*13/90:y<402?173-(y-350)*7/52:166;
  const YR=285,stumps=(gap,up)=>{const y1=YR-gap/2-up,y2=YR+gap/2,o=y1+up;
    return[spline([[184,-260],[170,120-up],[xp(o-44),y1-44],[xp(o)+2,y1-6],[(xp(o)+xa(o))/2,y1+3],[xa(o)-2,y1-6],[xa(o-44),y1-44],[204,120-up],[226,-260]]),
           spline([[(xp(y2)+xa(y2))/2,y2-3],[xp(y2)+2,y2+6],[149,340],[143,392],[146,432],[160,438],[166,402],[173,350],[xa(y2)-2,y2+6]]),y1,y2]};
  const skN=[[156,-260],[146,120],[137,260],[127,350],[117,410],[121,470],[141,512],[190,528],[300,529],[420,531],[540,533],[660,535],[660,444],[560,413],[480,373],[420,331],[392,281],[384,180],[392,-260]];
  const skH=skN.map(p=>p.slice());skH[3]=[119,346];skH[4]=[103,400];skH[5]=[115,468];
  const skQ=skN.map(p=>p.slice());skQ[2]=[147,284];
  // Haglund
  const bursa=el('path',{fill:'#F0714C'},extra),frag=el('path',{fill:'rgba(240,113,76,.55)',stroke:'#F0714C','stroke-width':1.6},extra),resLine=el('path',{class:'cor','stroke-width':2.6,'stroke-dasharray':'5 5'},extra);
  const shoe=el('path',{class:'cor','stroke-width':3,'stroke-dasharray':'2 7',d:'M84 286C66 350 64 432 90 494'},extra);
  const shav=el('g',{},extra);const shL=el('path',{stroke:'#DCE6F2','stroke-width':3.2,'stroke-linecap':'round',fill:'none'},shav),shH=el('path',{stroke:'#DCE6F2','stroke-width':9,'stroke-linecap':'round',fill:'none',opacity:.9},shav);
  const fDot=el('circle',{cx:206,cy:499,r:5,fill:'#9DB3CF'},extra);
  // tornozelo
  const atflA=el('path',{'data-part':'ligamento','stroke-linecap':'round',fill:'none'},lig),atflB=el('path',{'data-part':'ligamento','stroke-linecap':'round',fill:'none'},lig),cfl=el('path',{'data-part':'ligamento',stroke:'#F0DCC0','stroke-width':8,'stroke-linecap':'round',fill:'none',opacity:.75},lig);
  const fray=el('path',{class:'cor','stroke-width':2},lig),anch=el('g',{},lig),anchL=el('path',{stroke:'#fff','stroke-width':5,'stroke-linecap':'round'},anch),anchB=el('path',{stroke:'#fff','stroke-width':1.6,fill:'none'},anch),sut=el('path',{stroke:'#fff','stroke-width':1.5,'stroke-dasharray':'3 3',fill:'none'},lig);
  const dArrow=el('path',{class:'cor','stroke-width':2.4},extra);
  const tFray=el('path',{class:'cor','stroke-width':2.2},extra),tSut=el('path',{stroke:'#fff','stroke-width':1.8,'stroke-dasharray':'4 3',fill:'none','stroke-linecap':'round'},extra);
  [tend,tU,tL,fasc,calc,talus,fibula,atflA,atflB,cfl,tibP,...arcoP].forEach(e=>{const k=e.getAttribute('data-part');(parts[k]=parts[k]||[]).push(e)});
  const lb=c=>{const f=label(ann,c,()=>1);return(p,q,t,o,an)=>f(MP(p),QQ(q),t,o,an)};
  const L={ten:lb(1),bur:lb(1),cal:lb(1),sal:lb(0),sap:lb(0),fas:lb(1),ret:lb(0),esp:lb(1),fib:lb(1),tal:lb(1),lg:lb(1),rom:lb(0),fol:lb(0),anc:lb(0),rep:lb(1),rup:lb(0),enc:lb(0),sut:lb(0),cic:lb(1),pa:lb(1),pt:lb(1),pe:lb(1),pdes:lb(0),pinc:lb(0),pfr:lb(0),ppal:lb(0),pap:lb(1)};
  function update(s,cond){
    const H=cond==='haglund',T=cond==='tornozelo',Q=cond==='aquiles',P=cond==='peplano',t=performance.now()/1000,sc=1;K=1;
    MA=FIT.MA;LX=Q?0:(H?80:54);QQ=T?QT:QH;root.setAttribute('transform','matrix('+MA[0]+' '+MA[1]+' 0 '+MA[2]+' '+MA[3]+' '+MA[4]+')');
    const PT=FIT.PT;phX.setAttribute('transform',PT);phS.setAttribute('transform',PT);
    gCal.setAttribute('class','bn '+(H?'hi':'mid'));gTal.setAttribute('class','bn '+(P?'hi':'mid'));fibG.setAttribute('class','bn '+(T?'hi':'mid'));gDim.setAttribute('class','bn '+(P?'mid':'dim'));
    tend.style.opacity=(T||P)?.28:(Q?.8:.6);show(lig,T?1:0);
    // ---- Haglund
    const hg=H?ease(clamp(s)):0,rs=H?seg(s,1.45,1.85):0,ring=calN.map((p,i)=>mixP(mixP(p,calH[i],hg),calR[i],rs));
    setD(calc,spline(ring));
    const tk=hg*(1-rs);setD(tend,spline(tenN.map((p,i)=>mixP(p,tenH[i],tk))));const qt=Q?ease(clamp(s)):0,qr=Q?seg(s,1.45,1.9):0,ql=qt*(1-qr),qh=Q?seg(s,2.3,2.9):0;
    const skd=spline(skN.map((p,i)=>Q?mixP(p,skQ[i],ql):mixP(p,skH[i],H?hg*(1-rs*.6):0)));setD(skin,skd);
    const infl=H?hg*(1-seg(s,1.9,2.6)):0,pulse=(!reduced&&infl>.5)?1+.1*Math.sin(t*4):1;
    show(bursa,H?mix(.0,.9,infl)+(1-infl)*.0:0);
    setD(bursa,blob(mixP([180,356],[178,338],hg),(5+5*infl)*pulse,(9+7*infl)*pulse,.5,.04));
    if(H&&infl<.05){bursa.setAttribute('fill','#9DB3CF');show(bursa,.55)}else bursa.setAttribute('fill','#F0714C');
    show(shoe,H?win(s,.6,.9,1.05,1.2):0);show(fDot,H?win(s,.6,.9,1.05,1.2):0);
    show(resLine,H?win(s,1.2,1.3,1.9,2.2):0);const rp=seg(s,1.25,1.45);setD(resLine,'M146 408L'+f1(mix(146,214,rp))+' '+f1(mix(408,378,rp)));
    const fo=H?win(s,1.42,1.46,1.6,1.9):0;show(frag,fo);const fd=seg(s,1.5,1.9);frag.setAttribute('transform','translate('+f1(-26*fd)+' '+f1(-34*fd)+') rotate('+f1(-18*fd)+' 170 360)');
    setD(frag,spline([[146,398],[150,366],[160,348],[182,352],[202,362],[212,378],[186,388],[160,402]]));
    const so=H?win(s,1.05,1.15,1.5,1.62):0,sl=mix(100,0,seg(s,1.05,1.25))+mix(0,120,seg(s,1.5,1.64)),jit=(rp>0&&rp<1&&!reduced)?Math.sin(t*26)*1.6:0,tip=[mix(150,208,rp)-sl,mix(406,380,rp)-sl*.9+jit];
    show(shav,so);setD(shL,'M'+f1(tip[0])+' '+f1(tip[1])+'L'+f1(tip[0]-120)+' '+f1(tip[1]-110));setD(shH,'M'+f1(tip[0]-50)+' '+f1(tip[1]-46)+'L'+f1(tip[0]-120)+' '+f1(tip[1]-110));
    // ---- tornozelo
    const tear=T?ease(clamp(s)):0,rep=T?seg(s,1.5,1.9):0,loose=tear*(1-rep),wob=(!reduced&&loose>.6)?Math.sin(t*2.2)*2.5:0,dx=T?loose*9+wob:0;
    foot.setAttribute('transform','translate('+f1(dx)+' 0)');
    const o=[295,353],ins=[346+dx,373],gap=.5*(.34*loose),m0=mixP(o,ins,.5-gap),m1=mixP(o,ins,.5+gap),sag=loose*7;
    const col=loose>.3?'#F0714C':'#F6E6CF',wd=mix(11,12,rep);
    [atflA,atflB].forEach(e=>{e.setAttribute('stroke',col);e.setAttribute('stroke-width',wd);e.setAttribute('opacity',mix(.85,1,rep))});
    setD(atflA,'M'+f1(o[0])+' '+f1(o[1])+'Q'+f1((o[0]+m0[0])/2)+' '+f1((o[1]+m0[1])/2+sag)+' '+f1(m0[0])+' '+f1(m0[1]+sag*.6));
    setD(atflB,'M'+f1(m1[0])+' '+f1(m1[1]+sag*.6)+'Q'+f1((ins[0]+m1[0])/2)+' '+f1((ins[1]+m1[1])/2+sag)+' '+f1(ins[0])+' '+f1(ins[1]));
    setD(cfl,'M283 378L'+f1(254+dx)+' 426');
    show(fray,T?clamp((loose-.4)/.3):0);setD(fray,'M'+f1(m0[0])+' '+f1(m0[1]+sag*.6)+'l5 -6m-5 6l7 1m-7 -1l4 7M'+f1(m1[0])+' '+f1(m1[1]+sag*.6)+'l-5 -6m5 6l-7 1m7 -1l-4 7');
    const ap=T?seg(s,1.25,1.5):0,ao=T?(ap>0?mix(1,.7,seg(s,2.3,2.8)):0):0;show(anch,ao);
    const a0=[mix(322,298,ap),mix(338,354,ap)],a1=[a0[0]-13,a0[1]+9];anchL.setAttribute('d','M'+f1(a0[0])+' '+f1(a0[1])+'L'+f1(a1[0])+' '+f1(a1[1]));setD(anchB,'M'+f1(a1[0]+5)+' '+f1(a1[1]-9)+'l-6 2M'+f1(a1[0]+9)+' '+f1(a1[1]-5)+'l-2 6');
    show(sut,T?win(s,1.5,1.6,2.4,2.8):0);setD(sut,'M'+f1(a0[0])+' '+f1(a0[1])+'L'+f1(mix(o[0],ins[0],.55))+' '+f1(mix(o[1],ins[1],.55)-5)+'L'+f1(mix(o[0],ins[0],.72))+' '+f1(mix(o[1],ins[1],.72)+5));
    const da=T?win(s,.6,.9,1.3,1.5):0;show(dArrow,da);setD(dArrow,'M388 330L'+f1(420+dx)+' 330M'+f1(411+dx)+' 323L'+f1(420+dx)+' 330L'+f1(411+dx)+' 337');
    // ---- Aquiles: ruptura, sutura, cicatrização
    const split=Q&&s>.02&&qh<1,st=stumps(30*ql+1,18*ql),xm=(xp(YR)+xa(YR))/2;
    tend.style.display=split?'none':'';show(tU,split?.8:0);show(tL,split?.8:0);
    if(split){setD(tU,st[0]);setD(tL,st[1])}
    show(tCal,Q?qh*.85:0);if(Q)setD(tCal,blob([xm,YR],15,40,-.1,.02));
    show(tFray,Q?clamp((ql-.35)/.3):0);if(Q){const a=st[2],b=st[3];setD(tFray,'M'+f1(xm-9)+' '+f1(a+2)+'l-3 9m8 -8l1 10m7 -11l4 9M'+f1(xm-9)+' '+f1(b-2)+'l-3 -9m8 8l1 -10m7 11l4 -9')}
    show(tSut,Q?win(s,1.45,1.6,2.5,2.9):0);if(Q){const a=st[2],b=st[3];setD(tSut,'M'+f1(xp(a)+5)+' '+f1(a-30)+'L'+f1(xa(b)-5)+' '+f1(b+30)+'M'+f1(xa(a)-5)+' '+f1(a-30)+'L'+f1(xp(b)+5)+' '+f1(b+30)+'M'+f1(xp(a)+4)+' '+f1(a-16)+'L'+f1(xa(a)-4)+' '+f1(a-16)+'M'+f1(xp(b)+4)+' '+f1(b+16)+'L'+f1(xa(b)-4)+' '+f1(b+16))}
    // ---- pé plano: o tálus inclina para baixo, o meio do pé desce, o calcâneo abaixa; a palmilha apoia o arco
    const pc=P?ease(clamp(s))*(1-.25*seg(s,1.45,1.9)):0,pins=P?seg(s,1.3,1.7):0;
    const rot=(p,c,a)=>{const r=a*Math.PI/180,x=p[0]-c[0],y=p[1]-c[1];return[c[0]+x*Math.cos(r)-y*Math.sin(r),c[1]+x*Math.sin(r)+y*Math.cos(r)]};
    gTal.setAttribute('transform',P?'rotate('+f1(14*pc)+' 330 335)':'');gDim.setAttribute('transform',P?'rotate('+f1(-6*pc)+' 670 500)':'');gCal.setAttribute('transform',P?'rotate('+f1(5*pc)+' 170 490)':'');
    show(tibP,P?.85:0);tibP.setAttribute('stroke',P&&pc>.5&&s<1.6?'#F0714C':'#E9C9A4');tibP.setAttribute('stroke-width',P?mix(7,4,clamp(pc*1.5)):7);
    setD(tibP,'M262 150C258 300 262 380 300 410C340 '+f1(438+12*pc)+' 400 '+f1(420+18*pc)+' 446 '+f1(400+22*pc));
    const e0=rot([330,360],[330,335],14*pc),e1=rot([430,388],[330,335],14*pc),ev=[e1[0]-e0[0],e1[1]-e0[1]],eL=Math.hypot(ev[0],ev[1]),eEnd=[e0[0]+ev[0]/eL*360,e0[1]+ev[1]/eL*360];
    show(eixoT,P?win(s,-.3,-.02,2.3,2.6):0);setD(eixoT,'M'+f1(e0[0]-ev[0]/eL*40)+' '+f1(e0[1]-ev[1]/eL*40)+'L'+f1(eEnd[0])+' '+f1(eEnd[1]));
    show(insole,P?pins*.95:0);setD(insole,'M176 534C250 528 330 '+f1(mix(530,506,pins))+' 440 '+f1(mix(531,500,pins))+'C540 '+f1(mix(532,508,pins))+' 610 530 664 534L664 '+f1(mix(534,546,pins))+'L176 '+f1(mix(534,546,pins))+'Z');
    // ---- rótulos
    const o0=1-clamp((s-.22)/.25),o1=win(s,.6,.9,1.06,1.22),o3=seg(s,2.55,2.9);
    // Aquiles: o tendão é estreito e não sobra fundo atrás dele, então os rótulos vão à frente do tendão, sobre a perna, em placa
    if(Q)L.ten([166,236],[236,150],'TENDÃO\nDE AQUILES',o0);else L.ten([166,236],[92,196],'TENDÃO\nDE AQUILES',H?o0:0,'end');
    L.rup([xm,YR],[236,330],'RUPTURA',Q?o1:0);L.enc([xm+4,st[2]-40],[236,215],'A PANTURRILHA\nPUXA PARA CIMA',Q?win(s,.7,.95,1.3,1.5):0);
    L.sut([xm,YR],[236,330],'PONTOS UNEM\nAS DUAS PONTAS',Q?win(s,1.6,1.75,2.3,2.5):0);L.cic([xm,YR],[236,330],'TENDÃO\nCICATRIZADO',Q?o3:0);L.bur([180,356],[92,300],'BURSA',H?o0:0,'end');L.cal([290,446],Q?[500,566]:[318,566],'CALCÂNEO',(H||Q)?o0:0);
    L.sal([160,352],[92,250],'SALIÊNCIA\nDO OSSO',H?o1:0,'end');L.sap([74,472],[176,560],'O SAPATO\nENCOSTA AQUI',H?o1:0,'end');L.fas([206,499],[322,560],'FASCITE DÓI AQUI,\nEMBAIXO',H?o1:0);
    L.ret(mixP([176-26*fd,366-34*fd],[192,385],seg(s,1.78,1.95)),[92,226],'OSSO\nRETIRADO',H?win(s,1.5,1.6,2.3,2.5):0,'end');
    L.esp([178,388],[92,300],'TENDÃO LIVRE\nDO ATRITO',H?o3:0,'end');
    L.fib([270,268],[212,236],'FÍBULA',T?o0:0,'end');L.tal([378,372],[424,318],'TÁLUS',T?o0:0);L.lg(mixP(o,ins,.5),[424,232],'LIGAMENTO\nTALOFIBULAR',T?o0:0);
    L.rom(mixP(o,ins,.5),[424,232],'LIGAMENTO\nROMPIDO',T?o1:0);L.fol([420+dx,330],[436,330],'O TÁLUS\nGANHA FOLGA',T?win(s,.75,.95,1.3,1.5):0);
    L.anc(a0,[424,232],'ÂNCORA\nE SUTURA',T?win(s,1.5,1.6,2.3,2.5):0);L.rep(mixP(o,ins,.5),[424,232],'LIGAMENTO\nREPARADO',T?o3:0);
    // pé plano
    L.pt(rot([378,372],[330,335],14*pc),[400,262],'TÁLUS',P?o0:0);L.pa(rot([470,400],[670,500],-6*pc),[520,330],'ARCO DO PÉ',P?o0:0);
    L.pe(mixP(e0,eEnd,.55),[520,440],'EIXO DO TÁLUS\nNO METATARSO',P?win(s,-.3,-.02,.75,.9):0);
    L.pdes(rot([470,400],[670,500],-6*pc),[520,330],'O ARCO DESABA',P?o1:0);L.pinc(mixP(e0,eEnd,.75),[520,440],'EIXO DO TÁLUS\nPARA O CHÃO',P?o1:0);
    L.pfr([262,300],[400,190],'TENDÃO TIBIAL\nPOSTERIOR\nPERDE FORÇA',P?o1:0);
    L.ppal([420,515],[600,470],'PALMILHA\nAPOIA O ARCO',P?win(s,1.45,1.6,2.3,2.5):0);L.pap([420,515],[580,470],'PALMILHA E\nFORTALECIMENTO',P?o3:0);
    return (infl>.5)||(loose>.6)||(rp>0&&rp<1);
  }
  return{xr,sk,an:ann,update,parts,view:'Vista de lado',dir:'left',endW:c=>c==='tornozelo'?1:.58,geo:{talN,calN,calH,tenN,tenH,skN,skH,skQ,stumps}};
}

