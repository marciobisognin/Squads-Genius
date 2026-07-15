#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,html,re,socket,ssl,time,secrets,ipaddress
from pathlib import Path
from urllib.parse import urlparse,parse_qsl,urlencode,urlunparse
from urllib.request import Request,build_opener,HTTPRedirectHandler
from urllib.error import HTTPError

class NoRedirect(HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):return None
OPENER=build_opener(NoRedirect)

ROOT=Path(__file__).resolve().parents[1]
REQUIRED={'objective','authorization_basis','assets','allowed_bands','prohibited_actions'}

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def validate_engagement(d):
 errors=[]
 for k in REQUIRED:
  if k not in d:errors.append('missing:'+k)
 if not isinstance(d.get('assets'),list) or not d.get('assets'):errors.append('assets must be non-empty list')
 bands=d.get('allowed_bands',[])
 if not isinstance(bands,list) or any(x not in [0,1] for x in bands):errors.append('collector accepts Bands 0-1 only')
 return errors

def _redact_url(u):
 try:
  z=urlparse(u);q=[(k,'[REDACTED]' if re.search(r'token|secret|pass|key|auth|session',k,re.I) else v) for k,v in parse_qsl(z.query,keep_blank_values=True)];return urlunparse((z.scheme,z.netloc,z.path,z.params,urlencode(q,safe='[]'),''))
 except:return '[unparseable]'
def fetch(url,timeout=15):
 req=Request(url,headers={'User-Agent':'ScopeSentinel/1.0 authorized-low-impact-audit'})
 try:r=OPENER.open(req,timeout=timeout);body=r.read(2_000_000);status=r.status;headers=dict(r.headers.items());final=r.geturl()
 except HTTPError as e:body=e.read(2_000_000);status=e.code;headers=dict(e.headers.items());final=e.geturl()
 except Exception as e:return {'url':url,'error':str(e)}
 text=body[:200000].decode('utf-8','replace');m=re.search(r'<title[^>]*>(.*?)</title>',text,re.I|re.S)
 safe_headers={k:(_redact_url(v) if k.lower()=='location' else v) for k,v in headers.items() if k.lower() not in {'set-cookie','authorization','proxy-authorization','refresh'}}
 return {'url':url,'final_url':final,'status':status,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'content_type':headers.get('Content-Type'),'title':html.unescape(re.sub(r'\s+',' ',m.group(1)).strip())[:200] if m else None,'headers':safe_headers,'set_cookie_present':any(k.lower()=='set-cookie' for k in headers),'redirect_followed':False}

def cmd_plan(a):
 d=load(a.input);errors=validate_engagement(d)
 if errors:raise SystemExit('; '.join(errors))
 out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 plan={'valid':True,'objective':d['objective'],'assets':d['assets'],'max_band':max(d['allowed_bands']),'rate_limit':min(float(d.get('request_rate_limit',5)),5),'steps':['scope','dns','http-baseline','public-discovery-files','soft-404-control','manual-review','report-and-retest'],'prohibited_actions':d['prohibited_actions']}
 dump(out/'plan.json',plan);(out/'plan.md').write_text('# Plano Scope Sentinel\n\n- Objetivo: '+d['objective']+'\n- Ativos: '+', '.join(d['assets'])+'\n- Banda máxima: '+str(plan['max_band'])+'\n- Nenhuma autenticação, exploração, força bruta ou alteração de estado.\n',encoding='utf-8');print(json.dumps(plan,ensure_ascii=False))

def cmd_collect(a):
 d=load(a.input);errors=validate_engagement(d)
 if errors:raise SystemExit('; '.join(errors))
 rate=max(.2,1/min(float(d.get('request_rate_limit',2)),5));rows=[]
 for asset in d['assets']:
  u=urlparse(asset)
  if u.scheme not in ('http','https') or not u.hostname:rows.append({'asset':asset,'error':'only explicit http(s) URL assets are accepted'});continue
  if u.username or u.password:rows.append({'asset':'[REDACTED]','error':'embedded URL credentials are prohibited'});continue
  try:ips=sorted(set(x[4][0] for x in socket.getaddrinfo(u.hostname,u.port or (443 if u.scheme=='https' else 80),type=socket.SOCK_STREAM)))
  except Exception as e:ips=[]
  if not ips:rows.append({'asset':asset,'hostname':u.hostname,'ips':[],'error':'DNS resolution failed; no request sent'});continue
  try:parsed_ips=[ipaddress.ip_address(str(x).split('%')[0]) for x in ips]
  except:parsed_ips=[]
  if any(x.is_link_local or x.is_unspecified for x in parsed_ips):rows.append({'asset':asset,'hostname':u.hostname,'ips':ips,'error':'link-local/unspecified targets are blocked'});continue
  private=any(x.is_private or x.is_loopback for x in parsed_ips)
  basis=str(d.get('authorization_basis','')).lower()
  if private and (d.get('private_asset_approval') is not True or not any(k in basis for k in ['local lab','owner','written authorization','private infrastructure'])):rows.append({'asset':asset,'hostname':u.hostname,'ips':ips,'error':'private/loopback target requires private_asset_approval=true and explicit local-lab/ownership basis'});continue
  base=f'{u.scheme}://{u.netloc}';paths=['/','/robots.txt','/sitemap.xml','/.well-known/security.txt','/'+secrets.token_hex(12)];responses=[]
  for p in paths:responses.append(fetch(base+p));time.sleep(rate)
  root_hash=responses[0].get('sha256')
  for r in responses[1:]:r['soft_fallback']=bool(root_hash and r.get('sha256')==root_hash)
  rows.append({'asset':asset,'hostname':u.hostname,'ips':ips,'responses':responses})
 result={'tool':'Scope Sentinel','mode':'Bands 0-1','authorization_basis':d['authorization_basis'],'collected_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'assets':rows,'limitations':['no authentication','no exploit payloads','fixed five-request path set per asset','no port scan in collector']}
 dump(a.output,result);print(json.dumps({'assets':len(rows),'output':str(a.output)},ensure_ascii=False))

def cmd_report(a):
 d=load(a.input);lines=['# Relatório Scope Sentinel','','## Escopo',f"- Base de autorização: {d.get('authorization_basis','')}",f"- Ativos: {len(d.get('assets',[]))}",'','## Observações']
 for x in d.get('assets',[]):
  lines+=['',f"### {x.get('asset')}",f"- IPs resolvidos: {', '.join(x.get('ips',[])) or 'nenhum'}"]
  for r in x.get('responses',[]):
   state='soft fallback' if r.get('soft_fallback') else ('erro' if r.get('error') else str(r.get('status')))
   lines.append(f"- `{r.get('url')}` — {state}; {r.get('bytes','?')} bytes")
 lines+=['','## Limitações']+[f'- {x}' for x in d.get('limitations',[])]+['','## Próximo passo','Revisão manual, correlação de versões/advisories e reteste após remediação.']
 Path(a.output).write_text('\n'.join(lines)+'\n',encoding='utf-8');print(a.output)

def cmd_validate(a):
 p=Path(a.path);required=['squad.yaml','README.md','PRD.md','workflows/main.yaml','scripts/scopesentinel.py','examples/demo-input.json','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json'];missing=[x for x in required if not (p/x).is_file()];agents=list((p/'agents').glob('*.md'));tasks=list((p/'tasks').glob('*.md'));result={'valid':not missing and len(agents)>=6 and len(tasks)>=7,'missing':missing,'agents':len(agents),'tasks':len(tasks)};print(json.dumps(result,indent=2));raise SystemExit(0 if result['valid'] else 2)

def main():
 ap=argparse.ArgumentParser(description='Scope Sentinel authorized low-impact CLI');sp=ap.add_subparsers(required=True)
 p=sp.add_parser('plan');p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_plan)
 p=sp.add_parser('collect');p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_collect)
 p=sp.add_parser('report');p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.set_defaults(fn=cmd_report)
 p=sp.add_parser('validate');p.add_argument('--path',default=str(ROOT));p.set_defaults(fn=cmd_validate)
 a=ap.parse_args();a.fn(a)
if __name__=='__main__':main()
