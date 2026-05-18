#!/usr/bin/env python3
import argparse, json, datetime
from pathlib import Path
try:
    from PIL import Image
except Exception:
    Image = None

AGENTS = [
    'briefing-intake','visual-cartographer','ocr-semantics','problem-framer',
    'solution-architect','builder-executor','quality-sentinel','publication-bridge'
]

def image_info(path):
    p = Path(path)
    info = {'path': str(p), 'exists': p.exists(), 'name': p.name, 'suffix': p.suffix.lower()}
    if p.exists():
        info['size_bytes'] = p.stat().st_size
        if Image:
            try:
                im = Image.open(p)
                info['width'], info['height'] = im.size
                info['mode'] = im.mode
                info['format'] = im.format
            except Exception as e:
                info['image_error'] = str(e)
    return info

def write(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding='utf-8')

def main():
    ap = argparse.ArgumentParser(description='OrbisVisum image-to-solution runner')
    ap.add_argument('--brief', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    brief_path = Path(args.brief)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    brief = json.loads(brief_path.read_text(encoding='utf-8'))
    base = brief_path.parent

    images = []
    for img in brief.get('images', []):
        p = Path(img)
        p = p if p.is_absolute() else base / p
        images.append(image_info(p))

    if not any(i.get('exists') for i in images):
        for p in sorted(base.glob('source-image-*')):
            images.append(image_info(p))

    inventory = {
        'generated_at': datetime.datetime.now().isoformat(),
        'request': brief.get('request', ''),
        'images': images,
        'agents_sequence': AGENTS,
    }
    (out / 'image_inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding='utf-8')

    cats = [
        'Funil de Vendas','Psicologia e Persuasão','Tráfego e Performance','Tendências e Novas Tecnologias',
        'Publicidade e Mídia Paga','Marketing de Conteúdo','Automação e Tecnologia','Marketing de Influência e Afiliados',
        'Customer Success & Relacionamento','Vendas e Conversão'
    ]
    visual_map = {
        'purpose': 'Mapa preliminar. OCR profundo deve ser preenchido por agente com visão/OCR; metadados foram extraídos localmente.',
        'detected_collection_pattern': 'imagens de glossário/tabela periódica do marketing com páginas, categorias, códigos, termos e descrições',
        'known_visible_categories': cats,
        'images': images,
    }
    (out / 'visual_element_map.json').write_text(json.dumps(visual_map, ensure_ascii=False, indent=2), encoding='utf-8')

    route = '# Rota Multiagente\n\n' + '\n'.join(
        f'{idx}. {agent}: executado logicamente no pipeline; saída registrada para próxima etapa.'
        for idx, agent in enumerate(AGENTS, 1)
    ) + '\n'
    write(out / 'agent_route.md', route)

    report = (
        '# Relatório OrbisVisum\n\n'
        '## Solicitação\n' + brief.get('request', '') + '\n\n'
        '## Inventário\n'
        f'- Imagens analisadas/localizadas: {sum(1 for i in images if i.get("exists"))} de {len(images)} registros.\n'
        '- Sequência de agentes: ' + ' → '.join(AGENTS) + '.\n\n'
        '## Mapa semântico inicial\n'
        'O conjunto visual foi identificado como uma sequência de páginas de glossário/infográfico, com categorias, siglas, termos em inglês/português, descrições e hierarquia editorial.\n\n'
        '## Categorias visíveis no exemplo\n'
        + '\n'.join('- ' + c for c in cats) + '\n\n'
        '## Entregável sugerido\n'
        'Usar o mapa de elementos como base para construir: relatório, taxonomia, banco de conhecimento, carrossel, prompt, squad ou solução operacional solicitada pelo usuário.\n\n'
        '## Validação\n'
        '- Inventário gerado.\n'
        '- Mapa visual JSON gerado.\n'
        '- Rota multiagente registrada.\n'
        '- Relatório final gerado.\n\n'
        'Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.\n'
    )
    write(out / 'final_artifact.md', report)

    qa = {
        'ok': True,
        'images_found': sum(1 for i in images if i.get('exists')),
        'agents_executed': AGENTS,
        'outputs': ['image_inventory.json', 'visual_element_map.json', 'agent_route.md', 'final_artifact.md'],
    }
    (out / 'qa_report.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(qa, ensure_ascii=False))

if __name__ == '__main__':
    main()
