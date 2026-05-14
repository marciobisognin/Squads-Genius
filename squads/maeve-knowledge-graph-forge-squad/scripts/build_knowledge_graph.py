#!/usr/bin/env python3
import argparse,json,re
from pathlib import Path
from collections import Counter
STOP=set("a o os as um uma de do da dos das e em para por com sem que como mais menos sobre entre ou se no na nos nas ao aos é são foi ser ter pode podem cada este esta isso aquele aquela seu sua seus suas".split())
def read_text(path):
    if path.suffix.lower() in ['.txt','.md','.markdown','.html','.htm','.json','.yaml','.yml','.csv']:
        return path.read_text(encoding='utf-8',errors='ignore')
    return ''
def tokenize(txt):
    return [w for w in re.findall(r'[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9_-]{3,}',txt.lower()) if w not in STOP and len(w)>3]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output',required=True); ap.add_argument('--max-concepts',type=int,default=60); args=ap.parse_args()
    src=Path(args.input).expanduser().resolve(); out=Path(args.output).expanduser().resolve(); out.mkdir(parents=True,exist_ok=True)
    files=[p for p in src.rglob('*') if p.is_file()]; docs=[]; counts=Counter(); doc_terms={}
    for p in files:
        words=tokenize(read_text(p))
        if not words: continue
        rel=str(p.relative_to(src)); docs.append({'id':'doc:'+rel,'label':rel,'type':'document','path':rel,'size':p.stat().st_size})
        c=Counter(words); doc_terms[rel]=c; counts.update(c)
    concepts=[w for w,_ in counts.most_common(args.max_concepts)]
    nodes=docs+[{'id':'concept:'+w,'label':w,'type':'concept','weight':counts[w]} for w in concepts]
    links=[]
    for rel,c in doc_terms.items():
        for w,n in c.most_common(20):
            if w in concepts: links.append({'source':'doc:'+rel,'target':'concept:'+w,'type':'mentions','weight':n})
    co=Counter()
    for rel,c in doc_terms.items():
        present=[w for w in concepts if c[w]>0][:25]
        for i,a in enumerate(present):
            for b in present[i+1:]: co[tuple(sorted((a,b)))] += 1
    for (a,b),ww in co.most_common(120): links.append({'source':'concept:'+a,'target':'concept:'+b,'type':'cooccurs','weight':ww})
    graph={'nodes':nodes,'links':links,'stats':{'documents':len(docs),'concepts':len(concepts),'links':len(links)}}
    (out/'graph.json').write_text(json.dumps(graph,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'knowledge_inventory.json').write_text(json.dumps({'source':str(src),'files':[{'path':str(p.relative_to(src)),'size':p.stat().st_size,'suffix':p.suffix} for p in files]},ensure_ascii=False,indent=2),encoding='utf-8')
    summary=['# Síntese da base','','## Estatísticas',f'- Documentos com texto: {len(docs)}',f'- Conceitos: {len(concepts)}',f'- Conexões: {len(links)}','','## Conceitos centrais']+[f'- {w}: {counts[w]} ocorrências' for w in concepts[:20]]+['','## Próxima ação','Escolha se deseja estudar, criar sistema, desenvolver aplicação, criar curso/conteúdo, cruzar áreas ou gerar squad derivado.']
    (out/'knowledge_summary.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
    (out/'learning_paths.md').write_text('# Trilha de aprendizagem\n\n1. Leia os documentos mais conectados.\n2. Estude os 10 conceitos centrais.\n3. Revise conexões fortes no grafo.\n4. Transforme conceitos em projeto prático.\n',encoding='utf-8')
    (out/'application_opportunities.md').write_text('# Oportunidades de aplicação\n\n- Sistema de busca conceitual.\n- Curso baseado nos clusters.\n- Workflow de estudo.\n- Squad derivado para o domínio analisado.\n',encoding='utf-8')
    data=json.dumps(graph,ensure_ascii=False)
    html="""<!doctype html><html><head><meta charset="utf-8"><title>Knowledge Graph</title><style>body{font-family:Arial;background:#0b1020;color:#f8fafc}#wrap{display:flex;gap:20px}canvas{background:#111936;border:1px solid #334155;border-radius:16px}.panel{max-width:360px}li{margin:6px 0}</style></head><body><h1>Knowledge Graph</h1><div id="wrap"><canvas id="c" width="900" height="650"></canvas><div class="panel"><h2>Conceitos centrais</h2><ol id="list"></ol><p>Azul: documentos. Dourado: conceitos.</p></div></div><script>const graph=__DATA__;const c=document.getElementById('c'),ctx=c.getContext('2d');const nodes=graph.nodes,links=graph.links;const W=c.width,H=c.height;nodes.forEach((n,i)=>{let angle=2*Math.PI*i/nodes.length;let r=n.type==='document'?230:270;n.x=W/2+Math.cos(angle)*r*(0.7+Math.random()*0.3);n.y=H/2+Math.sin(angle)*r*(0.7+Math.random()*0.3);});function draw(){ctx.clearRect(0,0,W,H);ctx.globalAlpha=.25;links.forEach(l=>{let a=nodes.find(n=>n.id===l.source),b=nodes.find(n=>n.id===l.target);if(!a||!b)return;ctx.strokeStyle=l.type==='cooccurs'?'#94a3b8':'#38bdf8';ctx.lineWidth=Math.min(6,1+l.weight/2);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();});ctx.globalAlpha=1;nodes.forEach(n=>{ctx.fillStyle=n.type==='document'?'#38bdf8':'#f5b84b';ctx.beginPath();ctx.arc(n.x,n.y,n.type==='document'?8:5+Math.min(10,(n.weight||1)/2),0,Math.PI*2);ctx.fill();ctx.fillStyle='#f8fafc';ctx.font='11px Arial';ctx.fillText(String(n.label).slice(0,24),n.x+8,n.y+4);});}draw();document.getElementById('list').innerHTML=nodes.filter(n=>n.type==='concept').sort((a,b)=>(b.weight||0)-(a.weight||0)).slice(0,25).map(n=>`<li>${n.label}</li>`).join('');</script></body></html>""".replace('__DATA__',data)
    (out/'graph.html').write_text(html,encoding='utf-8')
    print(json.dumps(graph['stats'],ensure_ascii=False))
if __name__=='__main__': main()
