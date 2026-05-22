#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path

LISTED_FILE_RE = re.compile(r'^\s*-\s+([\w./-]+)\s*$')

EXPECTED_DEMO_RESEARCH = [
    'metodologia_busca.md', 'matriz_evidencias.csv', 'relatorio_pesquisa.md',
    'referencias_verificadas.md', 'manifest.json'
]
EXPECTED_DEMO_ARTICLE = [
    'artigo_imrad.md', 'parecer_revisao_pares.md', 'auditoria_integridade.md',
    'resposta_revisores.md', 'passaporte_material.yaml', 'manifest.json'
]

def listed_files(manifest_text):
    files=[]
    for line in manifest_text.splitlines():
        m=LISTED_FILE_RE.match(line)
        if not m:
            continue
        rel=m.group(1)
        if rel.startswith(('agents/','tasks/','workflows/','checklists/','templates/','scripts/','references/','examples/','config/')):
            files.append(rel)
    return files

def main():
    ap=argparse.ArgumentParser(description='Valida o squad Maeve Atena Mimir.')
    ap.add_argument('--path', default='.')
    args=ap.parse_args()
    root=Path(args.path)
    errors=[]; warnings=[]

    manifest=root/'squad.yaml'
    if not manifest.exists():
        errors.append('squad.yaml ausente')
        text=''
    else:
        text=manifest.read_text(encoding='utf-8')
        if 'license: MIT' not in text:
            errors.append('squad.yaml não declara license: MIT')
        if 'academic_research_skills:' not in text:
            warnings.append('referência clean-room ao academic-research-skills não encontrada no manifesto')

    for rel in listed_files(text):
        if not (root/rel).exists():
            errors.append(f'arquivo listado ausente: {rel}')

    agents_dir=root/'agents'
    for agent in agents_dir.glob('*.md'):
        s=agent.read_text(encoding='utf-8')
        if '*help' not in s or '*exit' not in s:
            errors.append(f'agente sem comandos universais: {agent.name}')
        if 'Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.' not in s:
            warnings.append(f'agente sem rodapé explícito: {agent.name}')

    required=['README.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json','TEXTO_PUBLICACAO_REDES_BLOG.md']
    for r in required:
        if not (root/r).exists():
            errors.append(f'arquivo obrigatório ausente: {r}')

    if not (root/'references/academic-research-skills-integration.md').exists():
        errors.append('referência de integração clean-room ausente')

    demo=root/'output/demo'
    for r in EXPECTED_DEMO_RESEARCH:
        if not (demo/r).exists():
            errors.append(f'demo pesquisa ausente: {r}')
    article_demo=root/'output/demo_article'
    for r in EXPECTED_DEMO_ARTICLE:
        if not (article_demo/r).exists():
            errors.append(f'demo artigo ausente: {r}')

    # Workflow sanity: every declared agent id must have a matching file.
    for wf in (root/'workflows').glob('*.yaml'):
        wft=wf.read_text(encoding='utf-8')
        for aid in re.findall(r'^\s*agent:\s*([\w-]+)\s*$', wft, flags=re.M):
            if not (root/'agents'/f'{aid}.md').exists():
                errors.append(f'workflow {wf.name} referencia agente ausente: {aid}')

    result={
        'ok': not errors,
        'errors': errors,
        'warnings': warnings,
        'agents': len(list(agents_dir.glob('*.md'))),
        'tasks': len(list((root/'tasks').glob('*.md'))),
        'workflows': len(list((root/'workflows').glob('*.yaml'))),
        'license': 'MIT',
        'integration_mode': 'clean-room adaptation; no upstream CC BY-NC files copied'
    }
    (root/'validation').mkdir(exist_ok=True)
    (root/'validation/validation-report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if not errors else 1)

if __name__=='__main__':
    main()
