# Mother Box Experience Squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-premium--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


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

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/mother-box-experience-squad/squad.yaml` e `squads/mother-box-experience-squad/workflows/experience-intelligence-pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/mother-box-experience-squad/agents/experience-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/mother-box-experience-squad/agents/experience-orchestrator.md`
> e conduza o fluxo definido em `squads/mother-box-experience-squad/`. Siga `squads/mother-box-experience-squad/workflows/experience-intelligence-pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/mother-box-experience-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/mother-box-experience-squad/workflows/experience-intelligence-pipeline.yaml. Conduza o fluxo para o briefing: <...>
```
- Use **`@caminho/arquivo`** para dar contexto preciso (autocompleta no prompt).
- Disponível em **CLI, app desktop/web (claude.ai/code) e extensões VS Code / JetBrains**.

</details>

<details>
<summary><b>🟦 Cursor</b></summary>

<br>

1. Abra a pasta do repositório no Cursor.
2. No **Chat / Composer (⌘/Ctrl + I)**, referencie os arquivos com `@`:
   ```text
   @squads/mother-box-experience-squad/squad.yaml @squads/mother-box-experience-squad/workflows/experience-intelligence-pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/mother-box-experience-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/mother-box-experience-squad/squad.yaml #file:squads/mother-box-experience-squad/workflows/experience-intelligence-pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/mother-box-experience-squad/squad.yaml @squads/mother-box-experience-squad/workflows/experience-intelligence-pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/mother-box-experience-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/mother-box-experience-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/mother-box-experience-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/mother-box-experience-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/mother-box-experience-squad/squad.yaml` e `squads/mother-box-experience-squad/workflows/experience-intelligence-pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
