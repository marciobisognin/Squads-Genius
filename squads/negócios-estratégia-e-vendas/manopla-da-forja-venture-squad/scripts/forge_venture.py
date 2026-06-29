#!/usr/bin/env python3
import argparse, datetime
from pathlib import Path

def build(idea, audience, output):
    now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    doc=f"""# 🟣 Manopla de Negócios — Forja Executiva

Gerado em: {now}

## 1. Minério Bruto
**Ideia/oportunidade:** {idea}

**Público preliminar:** {audience}

## 2. Joia da Mente — Blueprint Estratégico
- Problema provável: dor recorrente, custosa ou lenta que pode ser reduzida por IA e automação.
- Tese central: transformar a ideia em oferta clara, com promessa mensurável e validação rápida.
- Hipótese de valor: se o público percebe ganho de tempo, redução de risco ou melhoria de decisão, há base para MVP.

## 3. Joia da Alma — Comunidade e ICP
- ICP inicial: {audience}
- Dores a validar: urgência, custo da inação, frequência do problema e linguagem usada pelo público.
- Critério de coesão: nenhuma peça de design deve contradizer o vocabulário e as dores reais do ICP.

## 4. Joia do Espaço — Portais e Integrações
- Canais: Telegram/Web/Notion/Drive/WhatsApp conforme contexto.
- Dados: documentos, formulários, APIs públicas, bases internas e histórico operacional.
- Riscos técnicos: credenciais, privacidade, permissões, latência e qualidade das fontes.

## 5. Joia da Realidade — Identidade e Narrativa
- Promessa: converter complexidade em decisão acionável.
- Tom: técnico, claro, confiável e orientado a resultado.
- Landing outline: problema → custo da inação → solução → prova → entrega → chamada para piloto.

## 6. Joia do Poder — Viabilidade e Automação
- MVP enxuto: intake estruturado + análise automática + relatório executivo.
- Métricas: tempo economizado, acurácia de triagem, custo por entrega, margem e recorrência.
- Automações: geração de relatórios, matriz de riscos, alertas e checklist de revisão humana.

## 7. Joia do Tempo — Roadmap e Tendências
### Alfa — 7 a 14 dias
- Validar dor com 3 a 5 usuários reais.
- Gerar protótipo manual assistido por IA.

### Beta — 30 a 45 dias
- Padronizar fluxo, templates e dashboard mínimo.
- Medir tempo, custo e satisfação.

### Geral — 60 a 90 dias
- Criar oferta recorrente, onboarding e rotinas de automação.
- Avaliar break-even e canais de aquisição.

## 8. Gate de Consistência Semântica
Status: **aprovado com revisão humana recomendada**.

## 9. Próximo melhor passo
Realizar entrevista curta com o público-alvo e executar um piloto com um caso real.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(doc, encoding='utf-8')
    print(output)
if __name__ == '__main__':
    ap=argparse.ArgumentParser(description='Forja uma Manopla de Negócios a partir de uma ideia.')
    ap.add_argument('--idea', required=True)
    ap.add_argument('--audience', default='público-alvo a validar')
    ap.add_argument('--output', default='output/manopla-demo.md')
    args=ap.parse_args(); build(args.idea,args.audience,args.output)
