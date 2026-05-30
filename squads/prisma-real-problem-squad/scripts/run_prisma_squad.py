#!/usr/bin/env python3
import argparse, textwrap, json, datetime

AGENTS = [
    'Arquiteto de Contexto e Problema',
    'Estrategista Sistêmico',
    'Prototipador de Inovação',
    'Governança, Ética e Risco',
    'Diplomacia, Pessoas e Cultura',
    'Evidências, Pesquisa e Números',
    'Comunicação, Ensino e Narrativa',
    'Operações e Execução',
]

def run(problem):
    return {
        'timestamp': datetime.datetime.now().isoformat(timespec='seconds'),
        'problem': problem,
        'workflow': [
            {'phase': 'intake', 'agent': AGENTS[0], 'output': 'problema delimitado, objetivo e critérios de aceite'},
            {'phase': 'systems_strategy', 'agent': AGENTS[1], 'output': 'causas, efeitos, restrições e pontos de alavancagem'},
            {'phase': 'prototype', 'agent': AGENTS[2], 'output': 'alternativas e plano de protótipo'},
            {'phase': 'risk_review', 'agent': AGENTS[3], 'output': 'riscos, limites e mitigação'},
            {'phase': 'people', 'agent': AGENTS[4], 'output': 'adesão, comunicação e stakeholders'},
            {'phase': 'evidence', 'agent': AGENTS[5], 'output': 'premissas, lacunas e validação'},
            {'phase': 'communication', 'agent': AGENTS[6], 'output': 'síntese e narrativa de apresentação'},
            {'phase': 'execution', 'agent': AGENTS[7], 'output': 'tarefas, prazos, responsáveis e checklist'},
        ],
        'final_template': {
            'diagnostico': 'descrever a natureza do problema em linguagem clara',
            'solucao_recomendada': 'selecionar uma alternativa com justificativa',
            'plano_acao': ['ação 1', 'ação 2', 'ação 3'],
            'riscos': ['risco 1', 'risco 2'],
            'criterios_sucesso': ['critério 1', 'critério 2']
        }
    }

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--problem', required=True)
    args = ap.parse_args()
    print(json.dumps(run(args.problem), ensure_ascii=False, indent=2))
