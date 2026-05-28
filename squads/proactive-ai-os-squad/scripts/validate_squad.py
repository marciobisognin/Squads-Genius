#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
required=['README.md','squad.yaml','docs/PRD.md','docs/RND.md','LICENSE','NOTICE.md','AUTHORS.md','TEXTO_PUBLICACAO_REDES_BLOG.md']
missing=[p for p in required if not (root/p).exists()]
agents=list((root/'agents').glob('*.md')); workflows=list((root/'workflows').glob('*.md')); skills=list((root/'skills').glob('*/SKILL.md'))
if len(agents)<8: missing.append('agents>=8')
if len(workflows)<5: missing.append('workflows>=5')
if len(skills)<3: missing.append('skills>=3')
if 'Maeve' in (root/'README.md').read_text(encoding='utf-8'): missing.append('README contains Maeve')
if missing:
    print({'ok':False,'missing':missing}); sys.exit(1)
print({'ok':True,'agents':len(agents),'workflows':len(workflows),'skills':len(skills)})
