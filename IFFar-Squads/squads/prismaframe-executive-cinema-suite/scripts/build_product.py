#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, html, re, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FORBIDDEN=[r'prompt',r'agente',r'agent',r'squad',r'pipeline',r'gerado por',r'created by',r'modelo',r'LLM']
def esc(x): return html.escape(str(x), quote=False)
def read(p): return Path(p).read_text(encoding='utf-8')
def card(k): return f'<article class="card"><span>{esc(k.get("label","Indicador"))}</span><b>{esc(k.get("value","—"))}</b><small>{esc(k.get("note",""))}</small></article>'
def render_sections(sections):
    return ''.join(f'<section class="section"><h2>{esc(s.get("title","Seção"))}</h2><p>{esc(s.get("body",""))}</p></section>' for s in sections)
def render_timeline(items):
    return ''.join(f'<div>{esc(x)}</div>' for x in items)
def build(brief_path:Path,out:Path):
    b=json.loads(read(brief_path)); css=read(ROOT/'templates/style.css')
    data={
        'title':esc(b.get('title','Material Executivo')),
        'subtitle':esc(b.get('subtitle','Síntese visual')),
        'audience':esc(b.get('audience','Público executivo')),
        'thesis':esc(b.get('thesis','Síntese para decisão.')),
        'css':css,
        'kpi_cards':''.join(card(k) for k in b.get('kpis',[])[:4]),
        'sections':render_sections(b.get('sections',[])),
        'timeline':render_timeline(b.get('timeline',[])[:4])
    }
    out.mkdir(parents=True, exist_ok=True)
    for name,tpl in [('index.html','templates/index.html'),('deck.html','templates/index.html'),('motion-composition.html','templates/motion-composition.html'),('print-ready.html','templates/index.html')]:
        s=read(ROOT/tpl)
        for k,v in data.items(): s=s.replace('{{'+k+'}}',v)
        (out/name).write_text(s,encoding='utf-8')
    manifest={'title':b.get('title'),'files':['index.html','deck.html','motion-composition.html','print-ready.html'],'composition':{'composition_id':'executive-briefing','duration':12,'width':1920,'height':1080},'source_hash':hashlib.sha256(read(brief_path).encode()).hexdigest()}
    (out/'final-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in out.glob('*.html'))
    findings=[pat for pat in FORBIDDEN if re.search(pat,text,re.I)]
    qa={'status':'fail' if findings else 'pass','checks':[{'name':'cleanroom_forbidden_markers','status':'fail' if findings else 'pass','findings':findings},{'name':'required_files','status':'pass'}]}
    (out/'qa-cleanroom-report.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    if findings: raise SystemExit(json.dumps(qa,ensure_ascii=False))
    print(json.dumps({'status':'pass','output':str(out),'files':manifest['files']},ensure_ascii=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--brief',default=str(ROOT/'examples/demo/project_brief.json'))
    ap.add_argument('--output',default=str(ROOT/'generated/demo/final'))
    a=ap.parse_args(); build(Path(a.brief),Path(a.output))
