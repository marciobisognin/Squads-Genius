#!/usr/bin/env python3
from pathlib import Path
import json, sys
root=Path(__file__).resolve().parents[1]
errors=[]
required=['README.md','squad.yaml','docs/PRD_MASTER_SQU_ORACULO_AION.md','references/documento_fonte_extraido.txt','scripts/squ_aion_demo.py']
for r in required:
    if not (root/r).exists(): errors.append(f'missing {r}')
data=json.loads((root/'squad.yaml').read_text())
for a in data.get('agents',[]):
    p=root/'agents'/f"{a['id']}.md"
    if not p.exists(): errors.append(f"missing agent {a['id']}")
    else:
        t=p.read_text()
        if '*help' not in t or '*exit' not in t: errors.append(f"agent missing universal commands {a['id']}")
if 'Não prometer lucro' not in '\n'.join(data.get('guardrails',[])):
    errors.append('missing no-profit-promise guardrail')
for w in data.get('workflows',[]):
    if not (root/w).exists(): errors.append(f'missing workflow {w}')
if errors:
    print('VALIDATION_FAILED')
    print('\n'.join(errors))
    sys.exit(1)
print('VALIDATION_OK')
print(f"agents={len(data.get('agents',[]))} internal_squads={len(data.get('internal_squads',[]))}")
