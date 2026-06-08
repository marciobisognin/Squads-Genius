#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
required=['squad.yaml','README.md','BRD.md','scripts/build_html.py','scripts/build_pdf.py','scripts/validate_pdf.py','scripts/build_report.py','scripts/smoke_test.py','templates/executive-visual-layer.html','templates/analytical-visual-layer.html','templates/technical-appendix.html','templates/premium_report.css','contracts/project_brief.schema.json','contracts/data_profile.schema.json','contracts/design_system.schema.json','contracts/chart_spec.schema.json','contracts/qa_report.schema.json']
errors=[]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'missing:{rel}')
agents=list((ROOT/'agents').glob('*.md'))
if len(agents)<16: errors.append('agent_count_below_16')
for p in agents:
    t=p.read_text(encoding='utf-8',errors='ignore')
    if '*help' not in t or '*exit' not in t: errors.append(f'universal_commands_missing:{p.name}')
# simple secret scan, skip validator literals
patterns=[r'gho_[A-Za-z0-9_]+',r'github_pat_[A-Za-z0-9_]+',r'sk-[A-Za-z0-9]{20,}',r'BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY']
for p in ROOT.rglob('*'):
    if p.is_file() and p.name!='validate_squad.py' and p.suffix.lower() in {'.md','.py','.json','.yaml','.yml','.html','.css','.txt'}:
        txt=p.read_text(encoding='utf-8',errors='ignore')
        for pat in patterns:
            if re.search(pat,txt): errors.append(f'secret_pattern:{p.relative_to(ROOT)}')
print(json.dumps({'status':'pass' if not errors else 'fail','agents':len(agents),'errors':errors},ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)
