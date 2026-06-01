#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
required=['squad.yaml','README.md','workflows/forja-negocios.yaml','workflows/quality-gates.yaml','scripts/forge_venture.py']
agents=['arquiteto-sentido.md','defensor-comunidade.md','defensor-portais.md','designer-realidade.md','mestre-forja.md','cronos-anualista.md']
errors=[]
for r in required:
    if not (root/r).exists(): errors.append(f'Missing {r}')
for a in agents:
    p=root/'agents'/a
    if not p.exists(): errors.append(f'Missing agents/{a}')
    else:
        txt=p.read_text(encoding='utf-8')
        if '*help' not in txt or '*exit' not in txt: errors.append(f'Missing universal commands in {a}')
readme=(root/'README.md').read_text(encoding='utf-8') if (root/'README.md').exists() else ''
for token in ['Manopla de Negócios','Arquiteto de Sentido','Cronos-Anualista','Licença']:
    if token not in readme: errors.append(f'README missing token: {token}')
if errors:
    print('VALIDATION_FAILED')
    print('\n'.join(errors))
    sys.exit(1)
print('VALIDATION_OK')
print(f'files_checked={len(required)+len(agents)}')
