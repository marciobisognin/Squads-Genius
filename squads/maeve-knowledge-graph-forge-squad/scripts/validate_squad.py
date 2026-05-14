#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
REQ=['squad.yaml','README.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json','scripts/build_knowledge_graph.py','scripts/validate_squad.py']
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); args=ap.parse_args(); root=Path(args.root); issues=[]
    for f in REQ:
        if not (root/f).exists(): issues.append('ausente: '+f)
    try: m=json.loads((root/'squad.yaml').read_text(encoding='utf-8'))
    except Exception as e: issues.append('squad.yaml inválido: '+str(e)); m={}
    for k in ['agents','tasks','workflows']:
        for item in m.get(k,[]):
            if not (root/item['file']).exists(): issues.append(k+' ausente: '+item['file'])
    report={'go_no_go':'go' if not issues else 'no-go','issues':issues,'checks':{'agents':len(m.get('agents',[])),'tasks':len(m.get('tasks',[])),'workflows':len(m.get('workflows',[]))}}
    (root/'output').mkdir(exist_ok=True); (root/'output/quality_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if not issues else 1
if __name__=='__main__': sys.exit(main())
