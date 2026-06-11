#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
required = [
    'squad.yaml',
    'README.md',
    'scripts/analisar_dfd.py',
    'scripts/compras_gov.py',
    'scripts/enriquecer_dfd_compras_gov.py',
    'workflows/auditoria-dfd.yaml',
    'references/compras-gov-integracao.md',
    'references/uso-com-codex-claude-antigravity.md',
]
missing = [p for p in required if not (root / p).exists()]
if missing:
    raise SystemExit('Arquivos ausentes: ' + ', '.join(missing))
for script in ['scripts/analisar_dfd.py', 'scripts/compras_gov.py', 'scripts/enriquecer_dfd_compras_gov.py']:
    subprocess.run([sys.executable, '-m', 'py_compile', str(root / script)], check=True)
print(json.dumps({'status': 'ok', 'required_files': required, 'python_compile': 'ok'}, ensure_ascii=False, indent=2))
