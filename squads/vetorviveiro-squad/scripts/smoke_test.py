#!/usr/bin/env python3
import json, subprocess, sys, zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
errors=[]
required=['squad.yaml','README.md','workflows/pipeline-operacional.yaml','scripts/vetorviveiro_cli.py']
for r in required:
    if not (root/r).exists(): errors.append('missing '+r)
for agent in (root/'agents').glob('*.md'):
    t=agent.read_text(encoding='utf-8')
    if '*help' not in t or '*exit' not in t: errors.append('agent commands missing '+agent.name)
out=root/'output'/'demo'
res=subprocess.run([sys.executable,str(root/'scripts'/'vetorviveiro_cli.py'),'--input',str(root/'examples'/'demo_input.json'),'--output',str(out)],capture_output=True,text=True)
if res.returncode: errors.append('cli failed '+res.stderr)
for r in ['diagnostico.md','plano_operacional.md','manifest.json']:
    if not (out/r).exists(): errors.append('demo missing '+r)
report={'ok':not errors,'errors':errors,'agents':len(list((root/'agents').glob('*.md'))),'tasks':len(list((root/'tasks').glob('*.md')))}
(root/'validation'/'smoke-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
sys.exit(0 if not errors else 1)
