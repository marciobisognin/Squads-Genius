#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re,hashlib,unicodedata
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
ROOT=Path(__file__).resolve().parents[1]
SENSITIVE=re.compile(r'token|secret|pass|api.?key|credential|signature|session|jwt|auth',re.I)

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,o):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def safe_url(u):
 try:
  z=urlsplit(u);netloc=(z.hostname or '')+((':'+str(z.port)) if z.port else '');q=[(k,'[REDACTED]' if SENSITIVE.search(k) else v) for k,v in parse_qsl(z.query,keep_blank_values=True)];return urlunsplit((z.scheme,netloc,z.path,urlencode(q,safe='[]'),''))
 except:return ''
def cmd_init(a):
 d=load(a.input);required=['case_id','objective','legitimate_purpose','subject_type'];missing=[x for x in required if not d.get(x)]
 if missing:raise SystemExit('missing: '+', '.join(missing))
 out=Path(a.output);out.mkdir(parents=True,exist_ok=True);dump(out/'case.json',d)
 text=['# Plano de coleta OSINT',f"- Caso: {d['case_id']}",f"- Objetivo: {d['objective']}",f"- Finalidade: {d['legitimate_purpose']}",'','## Regras','- fontes públicas e lícitas','- sem login com dados vazados','- sem contato enganoso ou doxxing','- URL, timestamp e confiança obrigatórios']
 (out/'collection-plan.md').write_text('\n'.join(text)+'\n',encoding='utf-8');print(json.dumps({'valid':True,'output':str(out)},ensure_ascii=False))
def cmd_normalize(a):
 data=load(a.input);rows=data if isinstance(data,list) else data.get('records',[]);out=[];seen=set()
 for i,r in enumerate(rows,1):
  url=safe_url(str(r.get('source_url','')));claim=re.sub(r'\s+',' ',str(r.get('claim','')).strip());entity=re.sub(r'\s+',' ',str(r.get('entity','')).strip())
  if not url or not claim:continue
  key=(url.lower(),claim.lower())
  if key in seen:continue
  seen.add(key);out.append({'id':r.get('id') or f'R-{i:04d}','entity':entity or 'unresolved','claim':claim,'source_url':url,'source_type':r.get('source_type','secondary'),'retrieved_at':r.get('retrieved_at',''),'confidence':r.get('confidence','low'),'status':r.get('status','observed'),'limitations':r.get('limitations',[])})
 dump(a.output,{'records':out,'count':len(out),'privacy':'query credentials redacted; no private collection performed'});print(json.dumps({'input':len(rows),'normalized':len(out),'output':a.output},ensure_ascii=False))
def cmd_correlate(a):
 records=load(a.input).get('records',[]);nodes={};edges=[]
 for r in records:
  entity_key=unicodedata.normalize('NFKC',r['entity']).strip().casefold()
  eid='entity:'+hashlib.sha256(entity_key.encode()).hexdigest()[:16];sid='source:'+hashlib.sha256(r['source_url'].encode()).hexdigest()[:16];cid='claim:'+r['id']
  nodes[eid]={'id':eid,'type':'entity','label':r['entity']};nodes[sid]={'id':sid,'type':'source','label':r['source_url']};nodes[cid]={'id':cid,'type':'claim','label':r['claim'],'confidence':r['confidence']};edges += [{'source':sid,'target':cid,'relation':'supports'},{'source':cid,'target':eid,'relation':'about'}]
 graph={'nodes':sorted(nodes.values(),key=lambda x:x['id']),'edges':edges,'caveat':'correlation is not identity attribution'};dump(a.output,graph)
 csv_path=Path(a.output).with_name('evidence_matrix.csv')
 with csv_path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['id','entity','claim','source_url','source_type','retrieved_at','confidence','status']);w.writeheader();w.writerows([{k:r.get(k,'') for k in w.fieldnames} for r in records])
 print(json.dumps({'nodes':len(graph['nodes']),'edges':len(edges),'graph':a.output,'matrix':str(csv_path)},ensure_ascii=False))
def cmd_report(a):
 graph=load(a.graph);records=load(a.records).get('records',[]);counts={x:sum(r.get('confidence')==x for r in records) for x in ['high','medium','low']};lines=['# Relatório Trace Mosaic','','## BLUF',f"Foram normalizados {len(records)} registros públicos e {len(graph.get('nodes',[]))} nós. Correlação não equivale a atribuição de identidade.",'','## Confiança',f"- Alta: {counts['high']}",f"- Média: {counts['medium']}",f"- Baixa: {counts['low']}",'','## Matriz resumida']
 for r in records:lines.append(f"- **{r['entity']}** — {r['claim']} ({r['confidence']}; [fonte]({r['source_url']}))")
 lines+=['','## Limitações','- Somente fontes fornecidas; nenhuma coleta privada ou contato com sujeitos.','- Homônimos e contradições exigem revisão humana.']
 Path(a.output).write_text('\n'.join(lines)+'\n',encoding='utf-8');print(a.output)
def cmd_validate(a):
 p=Path(a.path);required=['squad.yaml','README.md','PRD.md','workflows/main.yaml','scripts/tracemosaic.py','examples/demo-input.json','LICENSE','.ip/ownership.json'];missing=[x for x in required if not (p/x).is_file()];result={'valid':not missing and len(list((p/'agents').glob('*.md')))>=7 and len(list((p/'tasks').glob('*.md')))>=8,'missing':missing};print(json.dumps(result,indent=2));raise SystemExit(0 if result['valid'] else 2)
def main():
 ap=argparse.ArgumentParser(description='Trace Mosaic ethical OSINT CLI');sp=ap.add_subparsers(required=True)
 p=sp.add_parser('init');p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_init)
 p=sp.add_parser('normalize');p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_normalize)
 p=sp.add_parser('correlate');p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_correlate)
 p=sp.add_parser('report');p.add_argument('--records',required=True);p.add_argument('--graph',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_report)
 p=sp.add_parser('validate');p.add_argument('--path',default=str(ROOT));p.set_defaults(fn=cmd_validate)
 a=ap.parse_args();a.fn(a)
if __name__=='__main__':main()
