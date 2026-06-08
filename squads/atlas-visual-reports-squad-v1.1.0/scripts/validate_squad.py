#!/usr/bin/env python3
from pathlib import Path
import sys, re, json
root=Path(__file__).resolve().parents[1]
required=['squad.yaml','README.md','BRD.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json','scripts/build_report.py','scripts/smoke_test.py','templates/report_template.html','templates/pdf_print.css','references/incoming-big4-audit-expansion/big4-compliance-research-notes.md']
agents=list((root/'agents').glob('*.md'))
missing=[p for p in required if not (root/p).exists()]
errors=[]
if missing: errors.append('missing: '+', '.join(missing))
if len(agents)<28: errors.append(f'expected >=28 agents, got {len(agents)}')
for a in agents:
    t=a.read_text(encoding='utf-8')
    if '*help' not in t or '*exit' not in t: errors.append(f'missing universal commands: {a.name}')
needed_agents=['partner-report-orchestrator.md','audit-evidence-quality-auditor.md','compliance-report-architect.md','internal-controls-matrix-builder.md','risk-heatmap-materiality-designer.md','cyber-privacy-assurance-reviewer.md','tax-regulatory-report-reviewer.md','forensic-red-flag-reviewer.md','strategy-coherence-reviewer.md','technology-digital-controls-reviewer.md','devils-advocate-red-team-reviewer.md']
for n in needed_agents:
    if not (root/'agents'/n).exists(): errors.append(f'missing new agent: {n}')
patterns=['g'+'ho_','github'+'_pat_','s'+'k-'+'[A-Za-z0-9]{20,}','BEGIN '+'(RSA |OPENSSH |EC |DSA )?'+'PRIVATE KEY']
secret_re=re.compile('|'.join(patterns))
for p in root.rglob('*'):
    if p == Path(__file__).resolve(): continue
    if any(part in {'.git','node_modules','__pycache__'} for part in p.parts): continue
    if p.is_file() and p.suffix.lower() in ['.md','.yaml','.yml','.json','.py','.html','.css','.txt']:
        if secret_re.search(p.read_text(encoding='utf-8',errors='ignore')):
            errors.append(f'possible secret: {p.relative_to(root)}')
print(json.dumps({'status':'pass' if not errors else 'fail','agents':len(agents),'errors':errors},ensure_ascii=False,indent=2))
sys.exit(0 if not errors else 1)
