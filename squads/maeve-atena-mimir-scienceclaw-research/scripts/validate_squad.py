#!/usr/bin/env python3
import argparse, re, sys, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--path', default='.')
    root=Path(ap.parse_args().path)
    errors=[]
    manifest=root/'squad.yaml'
    if not manifest.exists(): errors.append('squad.yaml ausente')
    text=manifest.read_text(encoding='utf-8') if manifest.exists() else ''
    for rel in re.findall(r'    - ([\w./-]+)', text):
        if rel.startswith(('agents/','tasks/','workflows/','checklists/','templates/','scripts/','references/','examples/')) and not (root/rel).exists():
            errors.append(f'arquivo listado ausente: {rel}')
    for agent in (root/'agents').glob('*.md'):
        s=agent.read_text(encoding='utf-8')
        if '*help' not in s or '*exit' not in s: errors.append(f'agente sem comandos universais: {agent.name}')
    required=['README.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json','TEXTO_PUBLICACAO_REDES_BLOG.md']
    for r in required:
        if not (root/r).exists(): errors.append(f'arquivo obrigatório ausente: {r}')
    demo=root/'output/demo'
    for r in ['metodologia_busca.md','matriz_evidencias.csv','relatorio_pesquisa.md','referencias_verificadas.md','manifest.json']:
        if not (demo/r).exists(): errors.append(f'demo ausente: {r}')
    result={'ok': not errors, 'errors': errors, 'agents': len(list((root/'agents').glob('*.md'))), 'tasks': len(list((root/'tasks').glob('*.md')))}
    (root/'validation/validation-report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if not errors else 1)
if __name__=='__main__': main()
