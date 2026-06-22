# ⚙️ Vector Sigma Data Forge Squad

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-premium--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


> *"Onde os dados ganham consciência de negócio."*

Squad premium de engenharia de dados e analytics, operado por 10 agentes especializados,
que transforma dados brutos em inteligência viva: arquitetura de dados, pipelines, qualidade,
árvore de métricas, dashboards, narrativa executiva, análise estatística e prontidão para ML.

---

## Artefato de Inspiração: Vector Sigma (Transformers G1)

O **Vector Sigma** é o supercomputador ancestral de Cybertron capaz de conceder
inteligência e personalidade aos Transformers — transformando matéria inerte em seres
conscientes. Este squad é o equivalente para dados: transforma dados brutos e
desestruturados em ativos conscientes de negócio, prontos para mover decisões.

- **A centelha de vida do Vector Sigma = a transformação de dado bruto em insight.**
- **A consciência concedida aos Transformers = a narrativa executiva que dá sentido aos números.**
- **A precisão ancestral de Cybertron = o rigor estatístico e a governança de dados aplicados em cada etapa.**

---

## Visão Geral do Squad

O Vector Sigma Squad cobre o ciclo completo de dados: da modelagem e pipelines à
governança de qualidade, da árvore de métricas ao design de dashboards, da análise
estatística à narrativa executiva, e da prontidão técnica até a viabilidade de ML em
produção.

**Diferencial central:** Gate de governança de dados e privacidade LGPD obrigatório antes
de qualquer modelagem, garantindo que toda a arquitetura de dados nasce em conformidade.

---

## Domínio e Casos de Uso

### Para quem este squad foi criado

- Times de dados e analytics que precisam estruturar arquitetura e pipelines do zero
- Empresas que precisam de árvore de métricas clara com ownership definido
- Times executivos que recebem dashboards mas não decisões acionáveis
- Organizações avaliando prontidão para iniciativas de Machine Learning

### Casos de uso típicos

| Situação | Como o Squad Ajuda |
|----------|-------------------|
| Dados espalhados sem modelo claro | Data Architecture Blueprint com modelo dimensional e contratos de dados |
| Pipelines frágeis e não idempotentes | Data Pipeline Design Document com estratégia de idempotência |
| Métricas sem dono ou sem North Star | Árvore de Métricas com ownership e alertas |
| Dashboards bonitos mas inacionáveis | Executive Data Story Report com recomendações concretas |
| Incerteza sobre prontidão para ML | MLOps Readiness Assessment |

---

## Agentes do Squad

### 1. vector-sigma-orchestrator
Coordenador central com gate de governança de dados e privacidade LGPD.

### 2. data-architecture-designer
Modelagem de dados: dimensional, ERD, data mesh, data contracts e design de domínios.

### 3. etl-pipeline-engineer
Design de pipelines ETL/ELT com idempotência, linhagem, testes e padrões de orquestração.

### 4. data-quality-sentinel
Perfis de qualidade de dados, detecção de anomalias, scorecards e documentação de linhagem.

### 5. metric-tree-architect
Design de árvore de métricas do North Star à operação, com ownership e alertas.

### 6. sql-analyst-pro
Análise SQL avançada, EDA, otimização de queries e templates reutilizáveis.

### 7. visualization-director
Design de dashboards com princípios Tufte/Cairo: layout, tipos de gráfico e hierarquia visual.

### 8. narrative-data-storyteller
Transforma análise em narrativa executiva orientada a ação com framing de impacto de negócio.

### 9. statistical-insight-miner
Análise estatística descritiva e inferencial, hipóteses, A/B test, correlação e outliers.

### 10. mlops-readiness-advisor
Avaliação de prontidão para ML em produção: pré-requisitos de dados, feature engineering e monitoramento.

---

## Pipeline de Execução

Workflow completo: [`workflows/data-intelligence-pipeline.yaml`](workflows/data-intelligence-pipeline.yaml)
Quality gates: [`workflows/quality-gates.yaml`](workflows/quality-gates.yaml)

Tarefas associadas:
- [`tasks/data-architecture.md`](tasks/data-architecture.md) — modelagem, pipelines e qualidade de dados
- [`tasks/data-storytelling.md`](tasks/data-storytelling.md) — métricas, visualização e narrativa executiva

---

## Entregáveis

- Data Architecture Blueprint (modelo dimensional, ERD, contratos de dados)
- Data Pipeline Design Document (ETL/ELT com boas práticas)
- Data Quality Scorecard com regras de validação
- Árvore de Métricas (Metric Tree) com North Star e métricas derivadas
- Dashboard Design System
- Executive Data Story Report
- Statistical Analysis Report
- MLOps Readiness Assessment

---

## Quality Gates

- `data_governance_validated`
- `schema_design_reviewed`
- `pipeline_idempotency_confirmed`
- `data_quality_baseline_set`
- `metric_tree_approved_by_business`
- `dashboard_ux_reviewed`
- `narrative_actionability_confirmed`

---

## Como Usar

1. Descreva o problema de negócio ou pergunta analítica e as fontes de dados disponíveis
2. Valide a governança de dados e conformidade LGPD (HITL obrigatório)
3. Acompanhe a modelagem de dados e design de pipelines
4. Aprove a árvore de métricas com seus stakeholders de negócio
5. Receba dashboards, relatório narrativo executivo e avaliação de prontidão para ML

---

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/vector-sigma-data-forge-squad/squad.yaml` e `squads/vector-sigma-data-forge-squad/workflows/data-intelligence-pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/vector-sigma-data-forge-squad/agents/vector-sigma-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/vector-sigma-data-forge-squad/agents/vector-sigma-orchestrator.md`
> e conduza o fluxo definido em `squads/vector-sigma-data-forge-squad/`. Siga `squads/vector-sigma-data-forge-squad/workflows/data-intelligence-pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/vector-sigma-data-forge-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/vector-sigma-data-forge-squad/workflows/data-intelligence-pipeline.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/vector-sigma-data-forge-squad/squad.yaml @squads/vector-sigma-data-forge-squad/workflows/data-intelligence-pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/vector-sigma-data-forge-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/vector-sigma-data-forge-squad/squad.yaml #file:squads/vector-sigma-data-forge-squad/workflows/data-intelligence-pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/vector-sigma-data-forge-squad/squad.yaml @squads/vector-sigma-data-forge-squad/workflows/data-intelligence-pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/vector-sigma-data-forge-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/vector-sigma-data-forge-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/vector-sigma-data-forge-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/vector-sigma-data-forge-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/vector-sigma-data-forge-squad/squad.yaml` e `squads/vector-sigma-data-forge-squad/workflows/data-intelligence-pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
