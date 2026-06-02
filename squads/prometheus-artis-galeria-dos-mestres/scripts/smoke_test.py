#!/usr/bin/env python3
from pathlib import Path
import sys
root = Path(__file__).resolve().parents[1]
required = ['squad.yaml','README.md','LICENSE','NOTICE.md','AUTHORS.md','TEXTO_PUBLICACAO_REDES_BLOG.md']
missing=[p for p in required if not (root/p).exists()]
main=list((root/'agents').glob('*.md'))
artists=list((root/'agents/artists').glob('*.md'))
workflows=list((root/'workflows').glob('*.yaml'))
tasks=list((root/'tasks').glob('*.md'))
refs=list((root/'references').glob('*.md'))
templates=list((root/'templates').glob('*.md'))
errors=[]
if missing: errors.append('missing: '+', '.join(missing))
if len(main) < 16: errors.append(f'main agents <16: {len(main)}')
if len(artists) < 32: errors.append(f'artist agents <32: {len(artists)}')
if len(workflows) < 3: errors.append(f'workflows <3: {len(workflows)}')
if len(tasks) < 5: errors.append(f'tasks <5: {len(tasks)}')
if len(refs) < 4: errors.append(f'references <4: {len(refs)}')
if len(templates) < 3: errors.append(f'templates <3: {len(templates)}')
readme=(root/'README.md').read_text(encoding='utf-8')
for token in ['mermaid','Estrutura dos agentes','O que o squad entrega no final','Prometheus Artis']:
    if token not in readme: errors.append('README missing '+token)
for p in main+artists:
    txt=p.read_text(encoding='utf-8')
    if '*help' not in txt or '*exit' not in txt: errors.append(f'commands missing in {p.relative_to(root)}')
if errors:
    print('FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print('PASS')
print(f'main_agents={len(main)} artist_agents={len(artists)} workflows={len(workflows)} tasks={len(tasks)} references={len(refs)} templates={len(templates)}')
