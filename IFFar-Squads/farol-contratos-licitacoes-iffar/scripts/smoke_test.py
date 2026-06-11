#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys, json
root=Path(__file__).resolve().parents[1]
required=['squad.yaml','README.md','scripts/analisar_dfd.py','workflows/auditoria-dfd.yaml']
missing=[p for p in required if not (root/p).exists()]
if missing:
    raise SystemExit('Arquivos ausentes: '+', '.join(missing))
print(json.dumps({'status':'ok','required_files':required}, ensure_ascii=False, indent=2))
