#!/usr/bin/env python3
import json, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]; errors=[]; manifest=json.loads((root/'squad.yaml').read_text(encoding='utf-8'))
for key in ['agents','tasks','workflows','scripts','templates']:
    for rel in manifest.get(key,[]):
        if not (root/rel).exists(): errors.append(f'missing {key}: {rel}')
for ag in (root/'agents').glob('*.md'):
    txt=ag.read_text(encoding='utf-8')
    if '*help' not in txt or '*exit' not in txt: errors.append(f'missing universal commands: {ag.name}')
for f in ['image_inventory.json','visual_element_map.json','agent_route.md','final_artifact.md','qa_report.json']:
    if not (root/'output/demo'/f).exists(): errors.append(f'missing demo output: {f}')
print(json.dumps({'ok':not errors,'errors':errors,'agents':len(list((root/'agents').glob('*.md'))),'tasks':len(list((root/'tasks').glob('*.md')))}, ensure_ascii=False, indent=2)); sys.exit(1 if errors else 0)
