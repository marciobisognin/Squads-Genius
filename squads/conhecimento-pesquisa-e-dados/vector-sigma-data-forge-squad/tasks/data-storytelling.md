---
task:
  name: data-storytelling
  id: data-storytelling
  title: "Métricas, Visualização e Narrativa Executiva de Dados"
  icon: "📊"
  description: >
    Tarefa de construção da árvore de métricas, design de dashboards, análise estatística
    e tradução de dados em narrativa executiva orientada a ação. Pressupõe arquitetura de
    dados já definida.
  estimated_duration: "2 a 3 dias úteis"
  squad: vector-sigma-data-forge-squad
  workflow: data-intelligence-pipeline.yaml
  output_format: Árvore de Métricas + Dashboard Design System + Executive Data Story Report
  prerequisite_task: data-architecture.md

inputs:
  required:
    - kpis_atuais: "KPIs atuais e como são calculados"
    - contexto_de_uso: "BI, ML, produto data-driven ou relatório executivo"
  optional:
    - dashboards_atuais: "Dashboards ou relatórios atuais (quando disponíveis)"

outputs:
  primary:
    - name: "Árvore de Métricas (Metric Tree)"
      description: "North Star Metric e métricas derivadas com ownership"
    - name: "Executive Data Story Report"
      description: "Narrativa executiva orientada a ação"
  secondary:
    - "Dashboard Design System"
    - "Statistical Analysis Report"
    - "MLOps Readiness Assessment"

hitl_checkpoints:
  - id: metric_tree_approved_by_business
    description: "Aprovação da árvore de métricas pelos stakeholders de negócio"
    required: true
    blocker: true
  - id: narrative_actionability_confirmed
    description: "Confirmação de que a narrativa é acionável"
    required: true
    blocker: true
---

# Tarefa: Métricas, Visualização e Narrativa Executiva de Dados

## Visão Geral

Com a arquitetura de dados já definida, esta tarefa transforma dados estruturados em
inteligência de negócio: métricas com ownership claro, dashboards bem desenhados, análise
estatística rigorosa e narrativas que movem decisões executivas.

**Pré-requisito:** Data Architecture Blueprint e Pipeline Design Document já aprovados.

## Passo a Passo

### Passo 1 — Construção da Árvore de Métricas

**Agente responsável:** metric-tree-architect

**Ações:**
1. Definir a North Star Metric alinhada ao objetivo de negócio
2. Decompor em métricas derivadas (de entrada, de processo, de saída)
3. Atribuir ownership de cada métrica a uma área ou papel responsável
4. Definir alertas e thresholds de anomalia por métrica

**Output:** Árvore de Métricas com North Star e métricas derivadas

---

### Passo 2 — HITL: Aprovação da Árvore de Métricas

**Responsável:** Usuário/Stakeholder de Negócio

**O que revisar:**
- A North Star Metric realmente reflete o sucesso do negócio
- As métricas derivadas têm ownership claro e são monitoráveis

**Gate de qualidade:** gate `metric_tree_approved_by_business` do quality-gates.yaml

---

### Passo 3 — Análise Estatística e Exploratória

**Agentes responsáveis:** sql-analyst-pro, statistical-insight-miner

**Ações:**
1. Conduzir análise exploratória de dados (EDA) sobre as fontes definidas
2. Identificar correlações, outliers e padrões estatisticamente relevantes
3. Quando aplicável, desenhar testes de hipótese ou A/B test

**Output:** Statistical Analysis Report

---

### Passo 4 — Design do Dashboard

**Agente responsável:** visualization-director

**Ações:**
1. Definir hierarquia visual (o que é destaque, o que é detalhe)
2. Escolher tipos de gráfico adequados a cada métrica e tipo de dado
3. Documentar design system do dashboard (cores, layout, componentes reutilizáveis)

**Output:** Dashboard Design System

---

### Passo 5 — Narrativa Executiva de Dados

**Agente responsável:** narrative-data-storyteller

**Ações:**
1. Traduzir os achados estatísticos e métricas em narrativa executiva
2. Para cada insight, associar uma recomendação de ação concreta
3. Usar linguagem executiva, evitando jargão técnico desnecessário

**Output:** Executive Data Story Report

---

### Passo 6 — Avaliação de Prontidão para ML (Quando Aplicável)

**Agente responsável:** mlops-readiness-advisor

**Ações:**
1. Avaliar pré-requisitos de dados para modelos de ML em produção
2. Identificar lacunas de feature engineering e monitoramento de modelo

**Output:** MLOps Readiness Assessment

---

### Passo 7 — HITL: Confirmação de Acionabilidade da Narrativa

**Responsável:** Usuário/Stakeholder de Negócio

**O que revisar:**
- Cada insight do relatório tem recomendação de ação associada
- A narrativa é compreensível sem conhecimento técnico de dados

**Gate de qualidade:** gate `narrative_actionability_confirmed` do quality-gates.yaml

---

## Critérios de Qualidade

| Critério | Padrão Mínimo |
|----------|---------------|
| Árvore de métricas | North Star aprovada pelo negócio com ownership definido |
| Rigor estatístico | Outliers e correlações identificados com significância reportada |
| Acionabilidade | 100% dos insights com recomendação de ação associada |
| Design do dashboard | Hierarquia visual clara e tipos de gráfico adequados aos dados |

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
