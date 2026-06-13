# Mother Box Experience Squad

## Visão Geral

O Mother Box Experience Squad é um squad multiagente de inteligência de experiência do cliente inspirado na Mother Box dos New Gods da DC Comics — a tecnologia viva que responde às necessidades do portador e abre Boom Tubes entre dimensões. Da mesma forma, este squad abre portais entre a voz do cliente e as decisões de negócio.

O squad cobre o ciclo completo de inteligência de experiência: mapeamento de jornada (As-Is e To-Be), síntese da voz do cliente, pesquisa UX qualitativa, análise emocional, identificação e priorização de friction points, design de blueprint de serviço (frontstage e backstage) e design do framework de métricas CX — tudo integrado em um pipeline multiagente com quality gates rigorosos e humano no loop nas decisões de impacto estratégico.

## Para quem é

- Diretores e gerentes de Customer Experience que precisam de inteligência estruturada sobre a jornada do cliente.
- Product Managers e UX Designers que querem sintetizar pesquisa qualitativa em insights acionáveis.
- Líderes de operações que precisam entender os processos de backstage que determinam a experiência do cliente.
- Times de Marketing e CRM que querem usar sinais de emoção e voz do cliente para personalizar comunicação.
- Executivos e CEOs que precisam de um framework de métricas CX conectado a resultados de negócio.

## Agentes

| Agente | Papel |
|---|---|
| `experience-orchestrator` | Coordenador central com gates de validação humana: roteia inputs, gerencia o pipeline e consolida outputs. |
| `journey-cartographer` | Mapeia a jornada do cliente nos estados As-Is e To-Be com etapas, canais e momentos da verdade. |
| `voice-of-customer-miner` | Minera e sintetiza a voz do cliente de NPS, reviews, tickets e redes sociais em insights estruturados. |
| `ux-research-synthesizer` | Sintetiza pesquisa qualitativa (entrevistas, testes de usabilidade) em insights acionáveis e rastreáveis. |
| `emotion-signal-analyst` | Analisa sinais emocionais, detecta momentos da verdade e constrói a Customer Emotion Curve. |
| `friction-removal-engineer` | Identifica e prioriza friction points com matriz impacto × esforço e CX Backlog estruturado. |
| `service-blueprint-architect` | Projeta blueprint de serviço completo com frontstage, backstage, atores, sistemas e pontos de falha. |
| `experience-metrics-designer` | Desenha framework de métricas CX: NPS, CSAT, CES, CLV, churn prediction e dashboard por camada. |

## Pipeline

O pipeline do Mother Box Experience Squad opera em 10 fases com quality gates entre as etapas críticas:

```
[Intake e Validação de Dados CX]
           ↓
[Mapeamento de Jornada As-Is]
           ↓
[Mineração da Voz do Cliente]     [Síntese de Pesquisa UX]
           ↓                                ↓
[Análise de Sinais Emocionais]
           ↓
[Identificação e Priorização de Fricções] ← GATE HUMANO
           ↓
[Design do Blueprint de Serviço] ← GATE HUMANO (times operacionais)
           ↓
[Design de Métricas de Experiência] ← GATE HUMANO (stakeholders)
           ↓
[Projeção da Jornada To-Be] ← GATE HUMANO (negócio)
           ↓
[Consolidação do CX Intelligence Pack]
```

Três fases exigem aprovação explícita de stakeholders antes de avançar: Blueprint de Serviço, Framework de Métricas e Jornada To-Be.

## Como Usar

### Pipeline Completo

Para executar o pipeline completo de inteligência de experiência do cliente, acione o `experience-orchestrator`:

```
Ative o Mother Box Experience Squad para análise completa de experiência.
Dados disponíveis: [informe quais dados você tem — NPS, tickets, entrevistas, analytics, etc.]
Escopo da jornada: [produto/serviço específico, canal, segmento de cliente]
Foco prioritário: [mapeamento de jornada / friction removal / blueprint / métricas CX]
```

### Sprint de Friction Removal

Para uma análise focada em remoção de fricções com base em dados existentes:

```
Acione o friction-removal-engineer com os seguintes dados de feedback: [dados]
Objetivo: identificar e priorizar os principais friction points para sprint de melhoria.
```

### Design de Métricas CX

Para projetar ou revisar o framework de métricas:

```
Acione o experience-metrics-designer.
Contexto: [setor, tamanho da operação, métricas já existentes]
Objetivo: [estruturar framework completo / revisar NPS / modelar churn]
```

### Comandos Universais

Todos os agentes respondem a:
- `*help` — lista capacidades do agente e como usá-lo.
- `*exit` — encerra a interação e devolve o controle ao fluxo principal.

## Inputs Necessários

- Dados de NPS, CSAT e CES (por canal, produto ou etapa da jornada)
- Tickets e transcrições de suporte ao cliente
- Avaliações em plataformas de reviews e redes sociais
- Gravações ou transcrições de entrevistas com usuários
- Relatórios de testes de usabilidade
- Dados de comportamento em produto (analytics, heatmaps, funis de conversão)
- Dados de churn e pesquisas de cancelamento
- Dados demográficos de clientes (com conformidade LGPD)

## Outputs

| Output | Descrição |
|---|---|
| Mapa de Jornada do Cliente | Jornada As-Is e To-Be estruturadas por etapa, canal e momento da verdade. |
| Blueprint de Serviço | Frontstage, backstage, atores, sistemas e pontos de falha documentados. |
| CX Backlog | Friction points priorizados por impacto × esforço com recomendações de remoção. |
| Relatório de Voz do Cliente | Temas, verbatins, tendências e segmentação do feedback de clientes. |
| Dashboard de Métricas CX | KPIs de experiência em 3 camadas: executiva, tática e operacional. |
| Customer Emotion Curve | Arco emocional do cliente ao longo da jornada com momentos da verdade. |

## Guardrails

- Dados pessoais de clientes tratados em conformidade com a LGPD (Lei 13.709/2018).
- Jornadas construídas com dados reais de clientes, não com perspectiva interna da empresa.
- Insights claramente separados em: observado, padrão, inferência e recomendação.
- Análise de sentimento com limitações explicitamente documentadas.
- Decisões de investimento e mudança de processo aprovadas por stakeholders antes de avançar.
- Nenhuma fonte proprietária ou sistema de terceiros reproduzido sem autorização.

## Estrutura de Arquivos

```
mother-box-experience-squad/
├── squad.yaml
├── README.md
├── agents/
│   ├── experience-orchestrator.md
│   ├── journey-cartographer.md
│   ├── voice-of-customer-miner.md
│   ├── ux-research-synthesizer.md
│   ├── emotion-signal-analyst.md
│   ├── friction-removal-engineer.md
│   ├── service-blueprint-architect.md
│   └── experience-metrics-designer.md
├── workflows/
│   ├── experience-intelligence-pipeline.yaml
│   └── quality-gates.yaml
└── tasks/
    ├── journey-mapping.md
    └── cx-metrics-design.md
```

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
