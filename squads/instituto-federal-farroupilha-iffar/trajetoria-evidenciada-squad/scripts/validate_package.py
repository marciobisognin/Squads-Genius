#!/usr/bin/env python3
import json, sys, re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
required=['README.md','squad.yaml','LICENSE','NOTICE.md','AUTHORS.md','scripts/trajetoria_evidenciada_demo.py']
required += [str(p.relative_to(root)) for p in (root/'agents').glob('*.md')]
missing=[p for p in required if not (root/p).exists()]
errors=[]
if missing:
    errors.append({'missing':missing})
for p in (root/'agents').glob('*.md'):
    t=p.read_text(encoding='utf-8')
    if '*help' not in t or '*exit' not in t:
        errors.append({'agent_missing_commands':str(p)})
    if 'Licença: MIT' not in t:
        errors.append({'agent_missing_footer':str(p)})
sy=(root/'squad.yaml').read_text(encoding='utf-8')
for line in sy.splitlines():
    s=line.strip()
    if s.startswith('- '):
        item=s[2:].strip()
        if item.startswith(('agents/','tasks/','workflows/','templates/','scripts/')):
            if not (root/item).exists():
                errors.append({'manifest_missing_file':item})
report={'ok':not errors,'errors':errors,'agents':len(list((root/'agents').glob('*.md'))),'tasks':len(list((root/'tasks').glob('*.md')))}
(root/'validation/package-validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
sys.exit(0 if not errors else 1)
