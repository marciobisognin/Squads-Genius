#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
required=['squad.yaml','README.md','scripts/build_product.py','scripts/build_pdf.py','scripts/smoke_test.py','scripts/validate_squad.py','examples/demo/project_brief.json','templates/index.html','templates/motion-composition.html','templates/style.css','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json']
errors=[]
for r in required:
    if not (ROOT/r).exists(): errors.append(f'missing {r}')
for d,minn in [('agents',16),('tasks',9),('workflows',3),('contracts',4)]:
    files=list((ROOT/d).glob('*'))
    if len(files)<minn: errors.append(f'{d} has {len(files)} < {minn}')
for p in (ROOT/'agents').glob('*.md'):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    if '*help' not in txt or '*exit' not in txt: errors.append(f'{p.name} missing universal commands')
# Build sensitive markers by concatenation and skip this validator file so the
# scanner does not flag its own rules as false positives.
secret_patterns=['gh'+'o_','github_'+'pat_','-----BEGIN '+'PRIVATE KEY-----']
for p in ROOT.rglob('*'):
    if p.name == 'validate_squad.py' or 'validation' in p.parts:
        continue
    if p.is_file() and p.suffix.lower() in {'.md','.py','.yaml','.json','.html','.css','.txt'}:
        txt=p.read_text(encoding='utf-8',errors='ignore')
        for pat in secret_patterns:
            if pat in txt: errors.append(f'possible secret {pat} in {p.relative_to(ROOT)}')
report={'status':'fail' if errors else 'pass','errors':errors}
(ROOT/'validation/structure-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
sys.exit(1 if errors else 0)
