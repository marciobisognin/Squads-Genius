#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'output/demo'
cmd=[sys.executable, str(root/'scripts/athena_mimir_venture_forge.py'), str(root/'examples/caso-demo.json'), '--output', str(out)]
res=subprocess.run(cmd, capture_output=True, text=True)
if res.returncode!=0:
    print(res.stdout); print(res.stderr); raise SystemExit(res.returncode)
required=['mapa-labirinto-hipoteses.md','cartao-runa-teste.md','travessia-bifrost-sprint.md','oraculo-de-decisao.md']
for name in required:
    p=out/name
    if not p.exists() or p.stat().st_size < 100:
        raise SystemExit(f'MISSING_OR_SMALL: {p}')
print('SMOKE_TEST_OK')
