#!/usr/bin/env python3
import json, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'squad.yaml').read_text(encoding='utf-8'))
missing=[]
for key in ['agents','tasks','workflows','templates','scripts','examples']:
    for item in manifest[key]:
        path=item['file'] if isinstance(item,dict) else item
        if not (root/path).exists(): missing.append(path)
for agent in manifest['agents']:
    txt=(root/agent['file']).read_text(encoding='utf-8')
    if '*help' not in txt or '*exit' not in txt: missing.append(agent['file']+':commands')
report={'ok':not missing,'missing':missing,'agents':len(manifest['agents']),'tasks':len(manifest['tasks'])}
(root/'validation/smoke-test-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
sys.exit(0 if report['ok'] else 1)
