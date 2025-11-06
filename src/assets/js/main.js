const LS_KEY = 'relatorio_final';
const LS_TREND = 'trend_pages';
const LS_SEL = 'pagina_selecionada';

function saveState(state){
  localStorage.setItem(LS_KEY, JSON.stringify(state));
  document.getElementById('statusSave').textContent = 'Salvo localmente ('+new Date().toLocaleTimeString()+')';
}

function loadState(){
  try { return JSON.parse(localStorage.getItem(LS_KEY)) || defaultState(); }
  catch(e) { return defaultState(); }
}

function saveTrend(arr){ localStorage.setItem(LS_TREND, JSON.stringify(arr)); }
function loadTrend(){ try{ return JSON.parse(localStorage.getItem(LS_TREND)) || []; }catch(e){ return []; } }
function defaultState(){ return [{id:1,titulo:'Página 1',imagem:null,texto:''}]; }

let pages = loadState();
let trends = loadTrend();
let selected = Number(localStorage.getItem(LS_SEL)) || 0;

const thumbsEl = document.getElementById('thumbs');
const novaBtn = document.getElementById('novaPagina');
const pageTitle = document.getElementById('pageTitle');
const pageText = document.getElementById('pageText');
const selectTrend = document.getElementById('selectTrend');
const inserirImg = document.getElementById('inserirImg');
const uploadTrend = document.getElementById('uploadTrend');
const pageImage = document.getElementById('pageImage');
const imgWrap = document.getElementById('imgWrap');
const noImgMsg = document.getElementById('noImgMsg');
const removerImg = document.getElementById('removerImg');
const deletePagina = document.getElementById('deletePagina');
const moveUp = document.getElementById('moveUp');
const moveDown = document.getElementById('moveDown');
const exportAllPdf = document.getElementById('exportAllPdf');
const exportPagePdf = document.getElementById('exportPagePdf');
const importBtn = document.getElementById('importBtn');
const exportJsonBtn = document.getElementById('exportJsonBtn');

function renderThumbs(){
  thumbsEl.innerHTML = '';
  pages.forEach((p,idx)=>{
    const btn = document.createElement('div');
    btn.className='thumb-btn'+(idx===selected?' active':'');
    btn.onclick = ()=>{ selected=idx; localStorage.setItem(LS_SEL,selected); render(); };

    const img = document.createElement('img');
    img.alt = p.titulo;
    img.src = p.imagem || (trends[0] ? trends[0].data : 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="120"><rect width="100%" height="100%" fill="#eef2ff" /></svg>');

    const info = document.createElement('div'); info.style.flex='1';
    const title = document.createElement('div'); title.textContent = p.titulo; title.style.fontWeight='600';
    const small = document.createElement('div'); small.className='tiny'; small.textContent = p.texto ? p.texto.slice(0,80) : '';
    info.appendChild(title); info.appendChild(small);

    btn.appendChild(img); btn.appendChild(info);
    thumbsEl.appendChild(btn);
  });
}

function renderTrendSelect(){
  selectTrend.innerHTML='';
  const empty = document.createElement('option'); empty.value=''; empty.textContent='-- selecione --';
  selectTrend.appendChild(empty);
  trends.forEach(t=>{
    const opt=document.createElement('option'); opt.value=t.name; opt.textContent=t.name;
    selectTrend.appendChild(opt);
  });
}

function renderPage(){
  const p = pages[selected];
  pageTitle.textContent = '📌 '+p.titulo;
  pageText.value = p.texto || '';
  if(p.imagem){
    pageImage.src=p.imagem; pageImage.style.display='block'; noImgMsg.style.display='none';
  } else {
    pageImage.src=''; pageImage.style.display='none'; noImgMsg.style.display='block';
  }
}

function render(){ renderThumbs(); renderTrendSelect(); renderPage(); saveState(pages); saveTrend(trends); }

novaBtn.addEventListener('click', ()=>{ 
  pages.push({id:pages.length+1,titulo:'Página '+(pages.length+1),imagem:null,texto:''}); 
  selected = pages.length-1; localStorage.setItem(LS_SEL,selected); render(); 
});

pageText.addEventListener('input', e=>{ pages[selected].texto = e.target.value; saveState(pages); });

inserirImg.addEventListener('click', ()=>{
  const nome = selectTrend.value; if(!nome){ alert('Selecione uma imagem da lista primeiro.'); return; }
  const t = trends.find(x=>x.name===nome);
  if(t){ pages[selected].imagem = t.data; render(); alert('Imagem adicionada!'); }
});

uploadTrend.addEventListener('change', async (ev)=>{
  const files = Array.from(ev.target.files);
  for(const f of files){
    const data = await fileToDataURL(f);
    trends.push({name:f.name,data});
  }
  render(); uploadTrend.value='';
});

removerImg.addEventListener('click', ()=>{ pages[selected].imagem=null; render(); });

deletePagina.addEventListener('click', ()=>{
  if(pages.length===1){ alert('Não é possível excluir a última página.'); return; }
  if(!confirm('Excluir esta página?')) return;
  pages.splice(selected,1);
  pages = pages.map((p,i)=>({...p,id:i+1,titulo:'Página '+(i+1)}));
  if(selected>=pages.length) selected = pages.length-1;
  localStorage.setItem(LS_SEL,selected);
  render();
});

moveUp.addEventListener('click', ()=>{ if(selected<=0)return; [pages[selected-1],pages[selected]]=[pages[selected],pages[selected-1]]; selected--; render(); });
moveDown.addEventListener('click', ()=>{ if(selected>=pages.length-1)return; [pages[selected+1],pages[selected]]=[pages[selected],pages[selected+1]]; selected++; render(); });

exportAllPdf.addEventListener('click', ()=>{ exportPDF(true); });
exportPagePdf.addEventListener('click', ()=>{ exportPDF(false); });

importBtn.addEventListener('click', ()=>{
  const txt = prompt('Cole aqui o JSON para importar (isso substituirá o estado atual)');
  if(!txt) return; 
  try{
    const obj = JSON.parse(txt);
    if(!Array.isArray(obj)) throw 'Formato inválido';
    pages = obj; trends = loadTrend(); selected=0; saveState(pages); render(); alert('Importado');
  }catch(e){ alert('Erro ao importar: '+e); }
});

exportJsonBtn.addEventListener('click', ()=>{
  const blob = new Blob([JSON.stringify(pages,null,2)],{type:'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href=url; a.download='relatorio_final.json'; a.click(); URL.revokeObjectURL(url);
});

function fileToDataURL(file){ return new Promise((res,rej)=>{ const fr=new FileReader(); fr.onload=()=>res(fr.result); fr.onerror=rej; fr.readAsDataURL(file); }); }

function exportPDF(all=true){
  if(all){
    const wrap=document.createElement('div'); wrap.style.padding='20px'; wrap.style.background='#fff';
    pages.forEach(p=>{
      const card=document.createElement('div'); card.style.marginBottom='18px'; card.style.border='1px solid #ddd'; card.style.padding='12px';
      const t=document.createElement('h3'); t.textContent=p.titulo; card.appendChild(t);
      const ta=document.createElement('div'); ta.textContent=p.texto||''; ta.style.marginBottom='8px'; card.appendChild(ta);
      if(p.imagem){ const im=document.createElement('img'); im.src=p.imagem; im.style.maxWidth='100%'; card.appendChild(im); }
      wrap.appendChild(card);
    });
    html2pdf().set({margin:10,filename:'relatorio_todo.pdf',image:{type:'jpeg',quality:0.95},html2canvas:{scale:2}}).from(wrap).save();
  } else {
    const p=pages[selected];
    const wrap=document.createElement('div'); wrap.style.padding='20px'; wrap.style.background='#fff';
    const t=document.createElement('h2'); t.textContent=p.titulo; wrap.appendChild(t);
    const ta=document.createElement('div'); ta.textContent=p.texto||''; ta.style.marginBottom='8px'; wrap.appendChild(ta);
    if(p.imagem){ const im=document.createElement('img'); im.src=p.imagem; im.style.maxWidth='100%'; wrap.appendChild(im); }
    html2pdf().set({margin:10,filename:p.titulo.replace(/\s+/g,'_')+'.pdf',image:{type:'jpeg',quality:0.95},html2canvas:{scale:2}}).from(wrap).save();
  }
}

render();
