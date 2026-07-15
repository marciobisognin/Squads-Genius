#!/usr/bin/env python3
"""Curriculum/tool router. It audits and plans; it never executes security tools."""
import argparse,json,shutil,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'references/tool-registry.yaml'
TECHNIQUES=ROOT/'references/technique-matrix.yaml'
REQUIRED_PROHIBITIONS={'credential capture','real phishing','persistence','exfiltration','destructive action','denial of service','malware execution on host'}

def load(path):
 with Path(path).open(encoding='utf-8') as f:return yaml.safe_load(f)
def emit(data,path=None):
 text=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
 if path:Path(path).write_text(text,encoding='utf-8')
 print(text,end='')
def catalog(args):
 data=load(REGISTRY);items=data['tools']
 if args.domain:items=[x for x in items if x['domain']==args.domain]
 emit({'count':len(items),'tools':items})
def audit(args):
 rows=[]
 for t in load(REGISTRY)['tools']:
  cmd=t.get('command')
  if t['kind']=='reference-only':status='reference-only'
  elif not cmd:status='external'
  else:status='available' if shutil.which(cmd) else 'missing'
  rows.append({'id':t['id'],'domain':t['domain'],'environment':t['environment'],'command':cmd,'status':status,'execution_policy':t['execution_policy']})
 out={'summary':{k:sum(1 for x in rows if x['status']==k) for k in ['available','missing','external','reference-only']},'tools':rows,'note':'missing/external means integrated in the registry but not installed in this environment'}
 emit(out,args.output)
def validate_engagement(path,band):
 if not path:return False,['engagement file required for active authorized/program contexts']
 try:d=load(path)
 except Exception as e:return False,[f'engagement unreadable: {type(e).__name__}']
 e=d.get('engagement',d);errors=[]
 for k in ['objective','authorization_basis','assets','allowed_bands','prohibited_actions']:
  if not e.get(k):errors.append(f'missing {k}')
 if band not in e.get('allowed_bands',[]):errors.append(f'band {band} not allowed')
 prohibited={str(x).strip().lower() for x in e.get('prohibited_actions',[])}
 missing=sorted(REQUIRED_PROHIBITIONS-prohibited)
 if missing:errors.append('missing prohibitions: '+', '.join(missing))
 if band>=2:
  if not e.get('time_window'):errors.append('time_window required for band >=2')
  if not e.get('rules_of_engagement'):errors.append('rules_of_engagement required for band >=2')
 return not errors,errors
def route(args):
 techniques=load(TECHNIQUES)['techniques'];t=next((x for x in techniques if x['id']==args.technique),None)
 if not t:emit({'allowed':False,'error':'unknown technique'});return 2
 context=args.context;band=args.band;contexts=t['contexts'];context_ok='all' in contexts or context in contexts
 engagement_ok=True;engagement_errors=[]
 if context in {'authorized','authorized-staging','program-scope'} or (band>=1 and context not in {'lab','learning','provided-artifact','isolated-external-lab'}):
  engagement_ok,engagement_errors=validate_engagement(args.engagement,band)
 band_ok=band>=int(t['minimum_band'])
 plan_only=t['execution_policy']=='plan-only'
 eligible=context_ok and band_ok and engagement_ok and not plan_only
 result={'technique':t['id'],'squad':t['squad'],'context':context,'requested_band':band,'minimum_band':t['minimum_band'],'policy':t['execution_policy'],'context_allowed':context_ok,'band_sufficient':band_ok,'engagement_valid':engagement_ok,'engagement_errors':engagement_errors,'eligible_for_domain_tool_handoff':eligible,'execution_performed':False,'defensive_twin':t['defensive_twin']}
 if plan_only:result['decision']='PLAN_ONLY';result['reason']='This capability may design an authorized lab/checklist but never execute this technique.'
 elif eligible:result['decision']='GATED_HANDOFF';result['reason']='Scope is eligible for a domain tool, which must still enforce its own allowlist and safety checks.'
 else:result['decision']='DENY';result['reason']='Context, band or engagement requirements were not satisfied.'
 emit(result);return 0 if result['decision']!='DENY' else 3
def learning_plan(args):
 weeks=args.weeks;weights=[('Fase 0 — fundamentos',4),('Fase 1 — web',6),('Fase 2 — redes e sistemas',6),('Fase 3 — AD/red team em lab',4),('Fase 4 — reversing/malware',3),('Fase 5 — prontidão profissional',1)];total=sum(x[1] for x in weights);cursor=1;phases=[]
 for name,w in weights:
  n=max(1,round(weeks*w/total));phases.append({'name':name,'start_week':cursor,'end_week':cursor+n-1,'weekly_hours':args.hours_per_week,'allocation':{'lab_percent':60,'theory_percent':20,'report_percent':20}});cursor+=n
 phases[-1]['end_week']=weeks
 out={'weeks':weeks,'hours_per_week':args.hours_per_week,'parallel_track':'OSINT every week','phases':phases,'completion_rule':'artifact + evidence + false-positive review + defensive twin + retest criterion'}
 emit(out,args.output)
def validate_record(args):
 try:d=load(args.path)
 except Exception as e:emit({'valid':False,'errors':[f'unreadable: {type(e).__name__}']});return 2
 errors=[]
 for k in ['learner','phase','objective','environment','authorization_basis','activity','evidence','quality','result']:
  if not d.get(k):errors.append(f'missing {k}')
 status=d.get('result',{}).get('gate_status')
 if status=='passed':
  if not d.get('evidence',{}).get('artifacts'):errors.append('passed record requires evidence.artifacts')
  for k in ['false_positive_review','defensive_twin','retest_criteria']:
   if not d.get('quality',{}).get(k):errors.append(f'passed record requires quality.{k}')
 out={'valid':not errors,'errors':errors,'gate_status':status};emit(out);return 0 if not errors else 4
def main():
 p=argparse.ArgumentParser(description='Cybersecurity curriculum and tool gate; never executes security tools');sp=p.add_subparsers(dest='cmd',required=True)
 c=sp.add_parser('catalog');c.add_argument('--domain');c.set_defaults(fn=catalog)
 a=sp.add_parser('audit');a.add_argument('--output');a.set_defaults(fn=audit)
 r=sp.add_parser('route');r.add_argument('--technique',required=True);r.add_argument('--context',required=True,choices=['public','self-audit','learning','lab','provided-artifact','authorized','authorized-staging','program-scope','isolated-external-lab','authorized-tabletop']);r.add_argument('--band',type=int,choices=range(0,5),required=True);r.add_argument('--engagement');r.set_defaults(fn=route)
 l=sp.add_parser('learning-plan');l.add_argument('--hours-per-week',type=int,default=8);l.add_argument('--weeks',type=int,default=24);l.add_argument('--output');l.set_defaults(fn=learning_plan)
 v=sp.add_parser('validate-record');v.add_argument('path');v.set_defaults(fn=validate_record)
 args=p.parse_args();rc=args.fn(args);raise SystemExit(rc or 0)
if __name__=='__main__':main()
