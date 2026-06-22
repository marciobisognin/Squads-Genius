# 🧠 Cerebro Sales Intelligence Squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-premium--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


> *"Com o Cerebro, Xavier pode detectar qualquer mutante no planeta. Com este squad, você detecta cada oportunidade de receita — por mais invisível que seja."*

---

## Visão Geral

O **Cerebro Sales Intelligence Squad** é um sistema multiagente especializado em inteligência de vendas que amplifica a capacidade analítica de times comerciais — detectando oportunidades, padrões e riscos de receita que passariam despercebidos sem amplificação inteligente.

Assim como o Cerebro (Marvel — X-Men) amplifica a mente do Professor Xavier para detectar mutantes em qualquer lugar do mundo, este squad amplifica a inteligência comercial da organização: cada agente é um sensor especializado que capta sinais específicos do ambiente de vendas e os transforma em ação concreta.

**Versão:** 1.0.0
**Licença:** MIT
**Criador:** Marcio Bisognin
**Instagram:** @marciobisognin
**Status:** Premium Ready

---

## Artefato de Inspiração

**Cerebro — Marvel Comics / X-Men**

O Cerebro é uma máquina extraordinária criada por Charles Xavier e Magneto nos anos iniciais dos X-Men. Quando o Professor X usa o Cerebro, sua telepátia é amplificada a um nível planetário — ele consegue detectar a presença de qualquer mutante na Terra, sentir suas emoções e localizar exatamente onde estão.

O squad segue a mesma lógica de amplificação:
- **O usuário** = Professor Xavier — tem o conhecimento do negócio e as perguntas certas
- **O squad** = O Cerebro — amplifica a capacidade analítica e detecta o que o olho nu não vê
- **Os agentes** = Os sensores especializados do Cerebro — cada um sintonizado em um tipo específico de sinal comercial

Assim como Xavier precisa do Cerebro para ver além das paredes da Escola Xavier, líderes de vendas precisam do squad para ver além dos relatórios superficiais do CRM.

---

## Domínio e Casos de Uso

Este squad é ideal para organizações que:

- Querem parar de perder deals sem entender o porquê
- Têm uma base de leads mas não sabem quais priorizar
- Precisam de um forecast de receita confiável para planejar contratações e investimentos
- Querem replicar o que seus melhores vendedores fazem para o time inteiro
- Precisam entender por que o pipeline está crescendo mas o revenue não
- Querem documentar e padronizar seu processo de vendas em um playbook acionável

---

## Agentes do Squad

O squad conta com **8 agentes especializados** organizados em grafo de dependências com coordenação dinâmica:

### 🧠 cerebro-orchestrator
**Papel:** Coordenador Central com Gateway de Privacidade LGPD

Orquestra todos os agentes, aplica o gate de privacidade LGPD antes de qualquer processamento de dados pessoais, monitora o status do pipeline e consolida todos os insights em relatório executivo acionável. É a mente amplificadora do squad.

**Gate LGPD:** Nenhum dado pessoal de leads/clientes é processado sem verificação de base legal, anonimização adequada e log de processamento.

---

### 🎯 icp-profiler
**Papel:** Especialista em Perfil de Cliente Ideal

Define o ICP com dados firmográficos, tecnográficos e comportamentais. Identifica os 20% de clientes que geram 80% do valor, mapeia atributos em comum, define personas de comprador e cria o scorecard de qualificação. Também define o Anti-ICP: critérios de exclusão explícitos.

**Output principal:** ICP Playbook com scorecard, personas e mapa de gatilhos de entrada.

---

### 📊 lead-scorer
**Papel:** Especialista em Scoring e Qualificação de Leads

Modela e aplica um sistema de scoring multidimensional (fit firmográfico, comportamento digital, engajamento comercial, sinais de intenção) com pesos justificados e thresholds de qualificação MQL/SQL/SRL/Hot. Elimina o subjetivismo da qualificação.

**Output principal:** Modelo de scoring documentado + ranking priorizado de leads.

---

### 🎙️ conversation-intelligence-analyst
**Papel:** Especialista em Inteligência de Conversas de Vendas

Analisa transcrições de chamadas e sequências de e-mail para extrair padrões de vitória, catalogar objeções por tipo e frequência, identificar o que top performers fazem diferente e detectar danger signals de deals em risco.

**Output principal:** Sales Conversation Intelligence Guide + Objection Playbook.

---

### 🔬 pipeline-health-monitor
**Papel:** Especialista em Saúde e Integridade do Pipeline

Monitora velocidade de pipeline, taxas de conversão estágio-a-estágio, deal slippage, cobertura de quota e concentração de risco. É o sistema de detecção precoce do squad — identifica problemas antes que se tornem crises de revenue.

**Output principal:** Pipeline Health Report + Deal Slippage Report + Coverage Dashboard.

---

### 🏆 win-loss-analyst
**Papel:** Especialista em Análise de Vitórias e Derrotas

Conduz análise sistemática de deals ganhos e perdidos: tabula e prioriza razões de perda, identifica root cause (não apenas sintomas), extrai win patterns e gera competitive battle cards. Aprende com o passado para vencer no futuro.

**Output principal:** Win/Loss Intelligence Report + Battle Cards + Root Cause Matrix.

---

### 📖 sales-playbook-engineer
**Papel:** Especialista em Engenharia de Playbooks de Vendas

Integra outputs de todos os outros agentes para criar o Sales Playbook Master: segmentado por vertical, persona e tipo de objeção, com scripts de discovery, templates de e-mail, battle cards e guia de ramp para novos vendedores. Codifica o conhecimento implícito em sistema explícito.

**Output principal:** Sales Playbook Master + Email Templates + Battle Cards + Ramp Guide.

---

### 📈 revenue-forecast-modeler
**Papel:** Especialista em Modelagem de Forecast de Receita

Constrói modelos probabilísticos de forecast com três cenários (conservador, realista, otimista), análise de sensibilidade e pipeline gap analysis. Substitui "achismo" por modelos fundamentados em dados com premissas explícitas e intervalos de confiança.

**Output principal:** Revenue Forecast Report (3 cenários) + Sensitivity Analysis + Pipeline Gap Analysis.

---

## Pipeline do Squad

```
Briefing do Usuário
        │
        ▼
┌─────────────────────────────┐
│  1. Intake e Contexto       │ ← cerebro-orchestrator
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  2. GATE LGPD (BLOQUEANTE)  │ ← cerebro-orchestrator
└─────────────────────────────┘
        │ (aprovado)
        ▼
   ┌────┴────┐
   │         │
   ▼         ▼
┌──────┐  ┌──────────────────┐
│ ICP  │  │  Pipeline Health │
│Profil│  │    Monitor       │
└──┬───┘  └──────┬───────────┘
   │              │
   ▼              ▼
┌──────────┐  ┌──────────────┐
│  Lead    │  │  Win/Loss    │
│  Scorer  │  │  Analyst     │
└──────────┘  └──────────────┘
        │              │
        │    ┌──────────────────────┐
        │    │ Conversation         │
        │    │ Intelligence Analyst │
        │    └──────────────────────┘
        │              │
        └──────┬────────┘
               ▼
     ┌─────────┴──────────┐
     │                    │
     ▼                    ▼
┌──────────────┐  ┌──────────────────┐
│ Sales        │  │ Revenue Forecast │
│ Playbook     │  │ Modeler          │
│ Engineer     │  └──────────────────┘
└──────────────┘          │
         │                │
         └──────┬──────────┘
                ▼
┌──────────────────────────────┐
│  CONSOLIDAÇÃO EXECUTIVA      │ ← cerebro-orchestrator
│  (Gate de Aprovação Final)   │
└──────────────────────────────┘
                │
                ▼
      Relatório Executivo +
      Todos os Artefatos
```

---

## Como Usar

### Opção 1 — Pipeline Completo (Recomendado)
Forneça ao `cerebro-orchestrator`:
1. **Briefing**: objetivos comerciais, segmento de mercado, produto/serviço, metas de receita
2. **Dados de clientes**: lista de clientes com indicadores de saúde (anonimizados)
3. **Dados de pipeline**: export do CRM ou descrição do pipeline atual
4. **Dados de win/loss**: histórico de deals fechados (últimos 6-12 meses)
5. **Dados de conversa**: transcrições de chamadas (anonimizadas) e/ou sequências de e-mail

O orchestrator conduzirá o pipeline completo, aplicando o gate LGPD e acionando os agentes na sequência correta.

### Opção 2 — Análise Específica
Você pode acionar agentes individualmente para análises específicas:

```
# Apenas ICP e Scoring
→ Falar diretamente com icp-profiler e lead-scorer
→ Fornecer: dados de clientes atuais e base de leads

# Apenas diagnóstico de pipeline
→ Falar diretamente com pipeline-health-monitor
→ Fornecer: export do CRM e quota do período

# Apenas win/loss
→ Falar diretamente com win-loss-analyst
→ Fornecer: histórico de deals fechados (won + lost)

# Apenas forecast
→ Falar diretamente com revenue-forecast-modeler
→ Fornecer: pipeline atual, win rate histórico e quota
```

### Opção 3 — Geração de Playbook a Partir de Insights Existentes
Se você já tem análises de ICP, win/loss e conversas:
```
→ Falar diretamente com sales-playbook-engineer
→ Fornecer: todos os insights disponíveis
→ Receber: Sales Playbook Master integrado
```

---

## Outputs Esperados

| Artefato | Agente Responsável | Quando |
|----------|-------------------|--------|
| ICP Playbook | icp-profiler | Fase 3 |
| Modelo de Lead Scoring | lead-scorer | Fase 4 |
| Ranking Priorizado de Leads | lead-scorer | Fase 4 |
| Sales Conversation Intelligence Guide | conversation-intelligence-analyst | Fase 5 |
| Objection Playbook | conversation-intelligence-analyst | Fase 5 |
| Pipeline Health Report | pipeline-health-monitor | Fase 6 |
| Deal Slippage Report | pipeline-health-monitor | Fase 6 |
| Win/Loss Intelligence Report | win-loss-analyst | Fase 7 |
| Competitive Battle Cards | win-loss-analyst | Fase 7 |
| Sales Playbook Master | sales-playbook-engineer | Fase 8 |
| Revenue Forecast (3 cenários) | revenue-forecast-modeler | Fase 8 |
| Pipeline Gap Analysis | revenue-forecast-modeler | Fase 8 |
| **Relatório Executivo Consolidado** | cerebro-orchestrator | Fase 9 |

---

## Princípios do Squad

- **Separar sempre**: observado, inferido, hipótese, recomendação e risco
- **LGPD first**: nenhum dado pessoal processado sem base legal e gate de privacidade
- **Root cause, não sintomas**: a razão declarada de perda raramente é a causa real
- **Acionabilidade**: toda análise termina com ação específica, owner e métrica de sucesso
- **Dados sobre intuição**: scoring e forecast substituem o "achismo" por modelos auditáveis
- **Transparência de premissas**: todo modelo declara suas limitações e hipóteses

---

## Requisitos de Dados Mínimos

Para análise completa:
- [ ] Pelo menos 20 clientes atuais com dados básicos (setor, porte, status de saúde)
- [ ] Pelo menos 20 deals fechados nos últimos 12 meses (won + lost)
- [ ] Pipeline atual com estágios, valores e close dates
- [ ] Metas de quota do período
- [ ] Pelo menos 10 transcrições de chamadas ou sequências de e-mail (opcional, enriquece muito)

Para análise parcial (qualquer subconjunto acima permite insights parciais mas valiosos).

---

## Privacidade e LGPD

Este squad foi projetado com privacidade por padrão:
- O `cerebro-orchestrator` aplica um **gate de bloqueio LGPD** antes de qualquer processamento de dados pessoais
- Todos os dados de leads e clientes devem ser **anonimizados ou pseudonimizados** antes de processamento
- O squad **não solicita nem armazena** CPF, e-mail pessoal, telefone pessoal ou qualquer dado sensível
- Análises de performance por vendedor são para uso interno de coaching exclusivamente
- Logs de processamento são gerados para auditoria de conformidade

---

## Estrutura de Arquivos

```
cerebro-sales-intelligence-squad/
├── squad.yaml                              # Manifesto do squad
├── README.md                               # Este arquivo
├── agents/
│   ├── cerebro-orchestrator.md             # Coordenador + gate LGPD
│   ├── icp-profiler.md                     # ICP e personas
│   ├── lead-scorer.md                      # Scoring multidimensional
│   ├── conversation-intelligence-analyst.md # Análise de chamadas e e-mails
│   ├── pipeline-health-monitor.md          # Saúde e diagnóstico de pipeline
│   ├── win-loss-analyst.md                 # Análise win/loss e competição
│   ├── sales-playbook-engineer.md          # Geração de playbooks
│   └── revenue-forecast-modeler.md         # Forecast probabilístico
├── workflows/
│   ├── sales-intelligence-pipeline.yaml    # Pipeline principal (9 fases)
│   └── quality-gates.yaml                  # Definição detalhada dos gates
└── tasks/
    ├── icp-and-scoring.md                  # Task: ICP + Lead Scoring
    └── pipeline-analysis.md                # Task: Pipeline + Win/Loss + Forecast
```

---

## Contribuição e Licença

Este squad é parte do repositório **Squads-Genius**, criado por Marcio Bisognin.

Contribuições são bem-vindas via Pull Request. Mantenha os créditos de autoria em todos os arquivos derivados.

---

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/cerebro-sales-intelligence-squad/squad.yaml` e `squads/cerebro-sales-intelligence-squad/workflows/sales-intelligence-pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/cerebro-sales-intelligence-squad/agents/cerebro-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/cerebro-sales-intelligence-squad/agents/cerebro-orchestrator.md`
> e conduza o fluxo definido em `squads/cerebro-sales-intelligence-squad/`. Siga `squads/cerebro-sales-intelligence-squad/workflows/sales-intelligence-pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/cerebro-sales-intelligence-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/cerebro-sales-intelligence-squad/workflows/sales-intelligence-pipeline.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/cerebro-sales-intelligence-squad/squad.yaml @squads/cerebro-sales-intelligence-squad/workflows/sales-intelligence-pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/cerebro-sales-intelligence-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/cerebro-sales-intelligence-squad/squad.yaml #file:squads/cerebro-sales-intelligence-squad/workflows/sales-intelligence-pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/cerebro-sales-intelligence-squad/squad.yaml @squads/cerebro-sales-intelligence-squad/workflows/sales-intelligence-pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/cerebro-sales-intelligence-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/cerebro-sales-intelligence-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/cerebro-sales-intelligence-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/cerebro-sales-intelligence-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/cerebro-sales-intelligence-squad/squad.yaml` e `squads/cerebro-sales-intelligence-squad/workflows/sales-intelligence-pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
