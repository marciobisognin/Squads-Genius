#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'output/demo'
out.mkdir(parents=True, exist_ok=True)
cmds=[
 [sys.executable, str(root/'scripts/lumen_leitura.py'), 'diagnostico', '--nome', 'Demo', '--idade', '7', '--trava', 'reconhece letras mas trava ao juntar sílabas', '--saida', str(out/'diagnostico-demo.md')],
 [sys.executable, str(root/'scripts/lumen_leitura.py'), 'sessao', '--foco', 'M + vogais', '--nivel', 'sílabas abertas', '--saida', str(out/'sessao-demo.md')],
 [sys.executable, str(root/'scripts/lumen_leitura.py'), 'semana', '--nome', 'Demo', '--foco', 'som antes do nome da letra', '--saida', str(out/'trilha-demo.md')],
]
for c in cmds:
    r=subprocess.run(c, cwd=root, text=True, capture_output=True)
    if r.returncode:
        print(r.stderr); sys.exit(r.returncode)
required=[root/'squad.yaml',root/'README.md',root/'agents/alfabetizacao-strategist.md',root/'workflows/diagnostico-e-plano.yaml',out/'diagnostico-demo.md',out/'sessao-demo.md',out/'trilha-demo.md']
missing=[str(p) for p in required if not p.exists() or p.stat().st_size==0]
if missing:
    print('MISSING', missing); sys.exit(2)
print('SMOKE_TEST_OK')
