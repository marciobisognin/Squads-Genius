#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

SQUADS = [
    ('Nemeton Survey Engine','pesquisa e evidências'),
    ('Cerridwen Offerbook Forge','oferta e mercado'),
    ('Sersi Reality Studio','design e experiência'),
    ('Nuada MVP Crucible','MVP e automação'),
    ('Manannán Connector Fleet','integrações e APIs'),
    ('Ogma Memory Codex','memória e conhecimento'),
    ('Taranis Benchmark Observatory','benchmark e métricas'),
    ('Ariadne Contract Loom','proposta, contrato e rastreabilidade'),
    ('Eirene Risk Citadel','riscos e quality gates'),
    ('Ananke Launch Chronogram','roadmap e lançamento'),
]

def score(idea):
    txt=idea.lower()
    flags=[]
    if any(w in txt for w in ['pesquisa','formulário','dados','vídeo','video','transcrição']): flags.append('Nemeton Survey Engine')
    if any(w in txt for w in ['oferta','venda','preço','produto','cliente','mercado']): flags.append('Cerridwen Offerbook Forge')
    if any(w in txt for w in ['design','landing','dashboard','apresentação','visual']): flags.append('Sersi Reality Studio')
    if any(w in txt for w in ['mvp','app','sistema','automação','script','software']): flags.append('Nuada MVP Crucible')
    if any(w in txt for w in ['api','integração','whatsapp','telegram','mcp','cli']): flags.append('Manannán Connector Fleet')
    if not flags: flags=['Nemeton Survey Engine','Cerridwen Offerbook Forge','Nuada MVP Crucible']
    return flags

def forge(args):
    idea=args.idea.strip()
    selected=score(idea)
    pack={
        'system':'Bigorna de Annwn — Super Sistema de Squads',
        'idea': idea,
        'selected_squads': selected,
        'method':'DSPC: Dor -> Squad -> Pitch -> Contrato',
        'outputs': ['PRD Master','Offerbook','MVP Blueprint','Design Brief','Quality Gate','Launch Chronogram'],
        'next_steps': [
            'Coletar evidências e fontes',
            'Gerar Offerbook preliminar',
            'Definir MVP mínimo vendável',
            'Criar validação por pré-venda ou piloto',
            'Submeter ao Eirene Risk Citadel antes de publicar ou vender'
        ]
    }
    out=Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('# Annwn Forge Pack — Demo\n\n```json\n'+json.dumps(pack,ensure_ascii=False,indent=2)+'\n```\n')
    print(json.dumps({'ok':True,'output':str(out),'selected_squads':selected}, ensure_ascii=False))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--idea', required=True)
    ap.add_argument('--output', default='output/annwn_forge_demo.md')
    forge(ap.parse_args())
