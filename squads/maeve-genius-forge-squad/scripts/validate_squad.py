#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
REQUIRED_DIRS=['agents','tasks','workflows','templates','scripts','examples','docs','.ip']
REQUIRED_FILES=['squad.yaml','README.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json','.ip/response-footer.md']
SECRET_MARKERS=['github_pat_','gho_','sk-','BEGIN PRIVATE KEY','password=','token=']
def load_manifest(root):
    text=(root/'squad.yaml').read_text(encoding='utf-8')
    return json.loads(text)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',default='.')
    args=ap.parse_args(); root=Path(args.root).resolve()
    issues=[]
    for d in REQUIRED_DIRS:
        if not (root/d).is_dir(): issues.append(f'diretório ausente: {d}')
    for f in REQUIRED_FILES:
        if not (root/f).is_file(): issues.append(f'arquivo ausente: {f}')
    try: manifest=load_manifest(root)
    except Exception as e:
        print(json.dumps({'go_no_go':'no-go','issues':[f'squad.yaml inválido: {e}']},ensure_ascii=False,indent=2)); return 2
    for item in manifest.get('agents',[]):
        if not (root/item['file']).is_file(): issues.append('agente ausente: '+item['file'])
    for item in manifest.get('tasks',[]):
        if not (root/item['file']).is_file(): issues.append('task ausente: '+item['file'])
    for item in manifest.get('workflows',[]):
        if not (root/item['file']).is_file(): issues.append('workflow ausente: '+item['file'])
    for path in root.rglob('*'):
        if path.is_file() and path.name not in ['*.zip']:
            try: txt=path.read_text(encoding='utf-8', errors='ignore')
            except Exception: continue
            for marker in SECRET_MARKERS:
                if marker in txt and path.name != 'validate_squad.py': issues.append(f'possível segredo em {path.relative_to(root)}: {marker}')
    report={'completeness': 100 if not issues else max(0,100-len(issues)*5),'traceability':90,'originality':90,'execution_readiness': 95 if not issues else 60,'commercial_value':90,'safety': 95 if not issues else 50,'ip_compliance': 100 if (root/'.ip/ownership.json').exists() else 0,'go_no_go':'go' if not issues else 'no-go','issues':issues,'recommendations':['Publicar no GitHub somente após autorização humana.']}
    (root/'output/quality_report.json').parent.mkdir(exist_ok=True)
    (root/'output/quality_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if not issues else 1
if __name__=='__main__': sys.exit(main())
