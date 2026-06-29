#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys, re
root=Path(__file__).resolve().parents[1]
required=['squad.yaml','README.md','references/memoria-viva-reference-dna.md','scripts/generate_song_package.py']
missing=[p for p in required if not (root/p).exists()]
if missing:
    print('MISSING', missing); sys.exit(1)
out=root/'generated/smoke-song-package.md'
subprocess.check_call([sys.executable, str(root/'scripts/generate_song_package.py'), '--theme', 'recomeçar depois de uma perda', '--output', str(out)])
txt=out.read_text()
checks=['## Letra','## Estilo musical','## Voz','## Instrumentos','## Prompt para IA musical','Checklist de originalidade']
fail=[c for c in checks if c not in txt]
if fail:
    print('FAILED', fail); sys.exit(1)
print('SMOKE_TEST_OK', out)
