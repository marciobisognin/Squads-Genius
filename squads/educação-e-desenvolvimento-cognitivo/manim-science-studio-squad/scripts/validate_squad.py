#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, py_compile
from pathlib import Path
try:
    import yaml
except Exception:
    yaml=None
REQ=['README.md','PRD.md','squad.yaml','LICENSE','NOTICE.md','AUTHORS.md','requirements.txt','pyproject.toml','quality_report.json']
DIRS=['agents','tasks','workflows','scripts','tests','examples','docs','schemas']
def load_yaml(path):
    text=path.read_text(encoding='utf-8')
    return yaml.safe_load(text) if yaml else json.loads(text)
def validate(root: Path):
    issues=[]
    for f in REQ:
        if not (root/f).is_file(): issues.append(f'arquivo ausente: {f}')
    for d in DIRS:
        if not (root/d).is_dir(): issues.append(f'diretório ausente: {d}')
    try: manifest=load_yaml(root/'squad.yaml')
    except Exception as exc: manifest={}; issues.append(f'squad.yaml inválido: {exc}')
    for sec in ['agents','tasks','workflows']:
        for item in manifest.get(sec,[]):
            rel=item.get('file')
            if not rel or not (root/rel).is_file(): issues.append(f'{sec} ausente: {rel}')
    for p in root.rglob('*.py'):
        if '__pycache__' in p.parts: continue
        try: py_compile.compile(str(p), doraise=True)
        except Exception as exc: issues.append(f'python inválido {p.relative_to(root)}: {exc}')
    return {'go_no_go':'go' if not issues else 'no-go','issues':issues,'checked_files':len([p for p in root.rglob('*') if p.is_file()])}
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--root', default='.')
    report=validate(Path(parser.parse_args().root).resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['go_no_go']=='go' else 1
if __name__=='__main__': raise SystemExit(main())
