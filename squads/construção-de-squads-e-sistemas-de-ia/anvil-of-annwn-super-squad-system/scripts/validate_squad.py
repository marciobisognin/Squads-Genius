#!/usr/bin/env python3
from pathlib import Path
import json, sys
root=Path(__file__).resolve().parents[1]
errors=[]
required=['README.md','squad.yaml','docs/PRD_SUPER_SISTEMA_BIGORNA_DE_ANNWN.md','scripts/annwn_forge.py']
for r in required:
    if not (root/r).exists(): errors.append(f'missing {r}')
data=json.loads((root/'squad.yaml').read_text())
for agent in data.get('agents',[]):
    p=root/'agents'/f"{agent['id']}.md"
    if not p.exists(): errors.append(f"missing agent {agent['id']}")
    else:
        txt=p.read_text()
        if '*help' not in txt or '*exit' not in txt: errors.append(f"agent lacks universal commands {agent['id']}")
for w in data.get('workflows',[]):
    if not (root/w).exists(): errors.append(f'missing workflow {w}')
if errors:
    print('VALIDATION_FAILED')
    print('\n'.join(errors))
    sys.exit(1)
print('VALIDATION_OK')
print(f"agents={len(data.get('agents',[]))} squads={len(data.get('internal_squads',[]))}")
