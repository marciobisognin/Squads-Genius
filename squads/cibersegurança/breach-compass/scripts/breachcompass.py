#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,ipaddress,json,re
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,o):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def cmd_triage(a):
 d=load(a.input);req=['incident_id','reported_at','summary','assets'];missing=[x for x in req if not d.get(x)]
 if missing:raise SystemExit('missing: '+', '.join(missing))
 out={'incident_id':d['incident_id'],'status':'identification','severity':d.get('severity','unknown'),'summary':d['summary'],'assets':d['assets'],'known_indicators':d.get('known_indicators',[]),'immediate_questions':['What happened and when?','Which assets/accounts/data may be affected?','Which evidence is volatile?','What containment is reversible?','Who must approve service-affecting action?'],'preservation':['record timezone and clocks','copy logs and alerts','hash collected files','avoid reboot before volatile-evidence decision'],'containment_requires_approval':True,'malware_policy':'static-first; dynamic only in approved disposable isolated lab','limitations':['synthetic/offline triage; no production action executed']}
 dump(a.output,out);print(json.dumps({'incident_id':out['incident_id'],'output':a.output},ensure_ascii=False))
def parse_time(x):
 try:return datetime.fromisoformat(str(x).replace('Z','+00:00'))
 except:return datetime.max
def cmd_timeline(a):
 data=load(a.input);events=data if isinstance(data,list) else data.get('events',[]);rows=[]
 for i,e in enumerate(events,1):rows.append({'timestamp':e.get('timestamp',''),'source':e.get('source',''),'asset':e.get('asset',''),'event':re.sub(r'\s+',' ',str(e.get('event','')).strip()),'confidence':e.get('confidence','medium'),'id':e.get('id') or f'E-{i:04d}'})
 rows.sort(key=lambda x:(parse_time(x['timestamp']),x['id']));p=Path(a.output);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=['timestamp','id','source','asset','event','confidence']);w.writeheader();w.writerows(rows)
 print(json.dumps({'events':len(rows),'output':a.output},ensure_ascii=False))
def cmd_ioc(a):
 text=Path(a.input).read_text(encoding='utf-8',errors='replace');ips=set();domains=set();hashes=set()
 for x in re.findall(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',text):
  try:ips.add(str(ipaddress.ip_address(x)))
  except:pass
 for x in re.findall(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,63}\b',text):
  if not x.lower().endswith(('.local','.internal')):domains.add(x.lower())
 for x in re.findall(r'\b(?:[A-Fa-f0-9]{64}|[A-Fa-f0-9]{40}|[A-Fa-f0-9]{32})\b',text):hashes.add(x.lower())
 out={'source_file':Path(a.input).name,'source_sha256':hashlib.sha256(Path(a.input).read_bytes()).hexdigest(),'indicators':{'ip':sorted(ips),'domain':sorted(domains),'hash':sorted(hashes)},'counts':{'ip':len(ips),'domain':len(domains),'hash':len(hashes)},'caveat':'indicators are leads; reputation and context not inferred'};dump(a.output,out);print(json.dumps(out['counts']))
def cmd_report(a):
 tri=load(a.triage);iocs=load(a.iocs);timeline=Path(a.timeline);events=max(0,sum(1 for _ in timeline.open(errors='replace'))-1) if timeline.exists() else 0;lines=['# Relatório Breach Compass','',f"## Incidente {tri['incident_id']}",tri['summary'],'',f"- Status: {tri['status']}",f"- Severidade inicial: {tri['severity']}",f"- Ativos: {', '.join(tri.get('assets',[]))}",f"- Eventos na timeline: {events}",'','## Indicadores',f"- IPs: {iocs['counts']['ip']}",f"- Domínios: {iocs['counts']['domain']}",f"- Hashes: {iocs['counts']['hash']}",'','## Decisões','- Preservar evidência antes de alteração.','- Contenção, revogação, bloqueio, isolamento ou remoção exigem aprovação humana.','- Malware permanece static-first; nenhuma amostra foi executada.','','## Próximos passos','1. Confirmar escopo e impacto.','2. Revisar timeline e hipóteses concorrentes.','3. Aprovar contenção reversível.','4. Erradicar, recuperar, monitorar e retestar.']
 Path(a.output).write_text('\n'.join(lines)+'\n',encoding='utf-8');print(a.output)
def cmd_validate(a):
 p=Path(a.path);required=['squad.yaml','README.md','PRD.md','workflows/main.yaml','scripts/breachcompass.py','examples/demo-input.json','LICENSE','.ip/ownership.json'];missing=[x for x in required if not (p/x).is_file()];result={'valid':not missing and len(list((p/'agents').glob('*.md')))>=8 and len(list((p/'tasks').glob('*.md')))>=8,'missing':missing};print(json.dumps(result,indent=2));raise SystemExit(0 if result['valid'] else 2)
def main():
 ap=argparse.ArgumentParser(description='Breach Compass defensive IR CLI');sp=ap.add_subparsers(required=True)
 p=sp.add_parser('triage');p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_triage)
 p=sp.add_parser('timeline');p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_timeline)
 p=sp.add_parser('ioc-extract');p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_ioc)
 p=sp.add_parser('report');p.add_argument('--triage',required=True);p.add_argument('--timeline',required=True);p.add_argument('--iocs',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_report)
 p=sp.add_parser('validate');p.add_argument('--path',default=str(ROOT));p.set_defaults(fn=cmd_validate)
 a=ap.parse_args();a.fn(a)
if __name__=='__main__':main()
