#!/usr/bin/env python3
import subprocess, sys, re
from pathlib import Path
root = Path(__file__).resolve().parents[1]
cmd = [
    sys.executable,
    str(root / 'scripts/create_poprock_ballad_blueprint.py'),
    '--tema', 'duas pessoas que se reencontram depois de anos',
    '--emocao', 'saudade, desejo contido e reencontro',
    '--simbolo', 'olhos',
    '--voz', 'masculina grave/média, quente e expressiva',
    '--output', str(root / 'validation/smoke-output'),
]
res = subprocess.run(cmd, cwd=root, text=True, capture_output=True)
print(res.stdout)
if res.returncode:
    print(res.stderr)
    sys.exit(res.returncode)
out = root / 'validation/smoke-output/poprock_ballad_blueprint.md'
text = out.read_text(encoding='utf-8')
required = ['## Letra', '## Voz', '## Instrumentos', '## Tags para IA musical', '## Prompt musical', 'Pop rock romântico']
missing = [x for x in required if x not in text]
forbidden = ['Deus', 'Senhor', 'oração', 'louvor', 'worship', 'gospel', 'devocional']
leaks = [x for x in forbidden if re.search(r'(?<![A-Za-zÀ-ÿ])' + re.escape(x.lower()) + r'(?![A-Za-zÀ-ÿ])', text.lower())]
if missing or leaks:
    print('MISSING', missing)
    print('LEAKS', leaks)
    sys.exit(2)
print('SMOKE_TEST_OK', out)
