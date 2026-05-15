#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def w(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def bullets(xs):
    return '\n'.join(f'- {x}' for x in xs)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--case', required=True)
    ap.add_argument('--output', required=True)
    args=ap.parse_args()
    data=json.loads(Path(args.case).read_text(encoding='utf-8'))
    out=Path(args.output); out.mkdir(parents=True, exist_ok=True)
    footer='Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.'
    w(out/'customer-profile.md', f"""# Customer Profile\n\n## Cliente\n{data.get('customer')}\n\n## Jobs\n{bullets(data.get('jobs', []))}\n\n## Pains\n{bullets(data.get('pains', []))}\n\n## Gains\n{bullets(data.get('gains', []))}\n\n## Evidências necessárias\n- entrevistas com usuários reais;\n- observação de comportamento;\n- compromisso mensurável com o próximo passo.\n\n{footer}\n""")
    w(out/'value-map.md', f"""# Value Map\n\n## Solução\n{data.get('solution')}\n\n## Produtos/serviços\n- oferta principal;\n- materiais de apoio;\n- acompanhamento leve.\n\n## Pain relievers\n{bullets(['reduz incerteza', 'simplifica aplicação prática', 'diminui tempo até o primeiro resultado'])}\n\n## Gain creators\n{bullets(['gera clareza', 'aumenta confiança operacional', 'cria artefatos reutilizáveis'])}\n\n{footer}\n""")
    w(out/'fit-matrix.md', f"""# Fit Matrix\n\n| Necessidade do cliente | Resposta da proposta | Evidência atual | Próximo teste |\n|---|---|---|---|\n| falta de tempo | microtarefas e templates | suposição | teste concierge de 5 usuários |\n| medo de erro | orientação com limites de uso | suposição | entrevista de risco percebido |\n| necessidade de resultado | artefato prático por semana | suposição | piloto de 7 dias |\n\n## Decisão preliminar\nFit promissor, mas ainda dependente de validação comportamental.\n\n{footer}\n""")
    w(out/'hypothesis-backlog.md', f"""# Hypothesis Backlog\n\n1. O público aceita investir 10–15 minutos por dia para aprender IA aplicada.\n2. Templates reduzem barreira de entrada mais do que aulas longas.\n3. Um piloto curto gera evidência suficiente para decidir avanço.\n\n{footer}\n""")
    w(out/'experiment-sprint.md', f"""# Experiment Sprint\n\n## Duração\n7 dias.\n\n## Experimentos\n- Entrevista com 5 usuários do público.\n- Landing page simples com proposta e inscrição.\n- Sessão concierge com 3 participantes.\n\n## Métricas\n- taxa de inscrição;\n- comparecimento;\n- entrega de tarefa;\n- pedido espontâneo de continuidade.\n\n{footer}\n""")
    w(out/'visual-canvas-brief.md', f"""# Visual Canvas Brief\n\n## Layout\nCanvas 3 colunas: Cliente → Fit → Valor.\n\n## Cores\n- Azul: perfil do cliente.\n- Laranja: dores.\n- Verde: ganhos.\n- Roxo: proposta de valor.\n- Amarelo: evidência/teste.\n\n## Componentes\nCards, setas de conexão, matriz de fit e bloco de decisão.\n\n{footer}\n""")
    slides=['Gancho: A ideia não é evidência','Quem é o cliente?','Quais tarefas ele tenta realizar?','Quais dores bloqueiam o progresso?','Que ganhos ele deseja?','Como a solução alivia dores?','Como cria ganhos?','Qual hipótese mata a ideia?','Qual teste barato começa agora?']
    w(out/'carousel-outline.md', '# Carousel Outline\n\n'+'\n'.join(f'{i+1}. {s}' for i,s in enumerate(slides))+f"\n\n{footer}\n")
    w(out/'pitch-storyboard.md', f"""# Pitch Storyboard\n\n1. Problema: usuários querem aplicar IA, mas têm medo e pouco tempo.\n2. Promessa: aprendizagem prática em microtarefas.\n3. Mecanismo: templates + desafios + exemplos reais.\n4. Prova a buscar: piloto de 7 dias com entrega real.\n5. Chamada para ação: participar do primeiro ciclo piloto.\n\n## Prompts visuais\n- dashboard dark neon mostrando cliente, dores, ganhos e proposta de valor em camadas;\n- carrossel didático 3:4 com ícones simples e blocos coloridos;\n- canvas visual limpo com setas entre dores e aliviadores.\n\n{footer}\n""")
    w(out/'executive-decision-report.md', f"""# Executive Decision Report\n\n## Decisão recomendada\nAvançar para piloto pequeno antes de construir produto completo.\n\n## Por quê\nA proposta tem lógica clara de valor, mas ainda precisa de evidência comportamental.\n\n## Próximo passo\nExecutar sprint de 7 dias e revisar métricas.\n\n{footer}\n""")
    print(json.dumps({'ok': True, 'output': str(out), 'files': len(list(out.glob('*.md')))}, ensure_ascii=False))
if __name__=='__main__': main()
