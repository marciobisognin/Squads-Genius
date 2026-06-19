---
task:
  name: data-architecture
  id: data-architecture
  title: "Arquitetura de Dados, Pipelines e Qualidade"
  icon: "⚙️"
  description: >
    Tarefa de fundação técnica do squad: modelagem de dados, design de pipelines ETL/ELT
    e definição de baseline de qualidade de dados. Base para a árvore de métricas e
    storytelling executivo nas etapas seguintes.
  estimated_duration: "2 a 4 dias úteis"
  squad: vector-sigma-data-forge-squad
  workflow: data-intelligence-pipeline.yaml
  output_format: Data Architecture Blueprint + Data Pipeline Design Document

inputs:
  required:
    - problema_de_negocio: "Descrição do problema de negócio ou pergunta analítica"
    - fontes_de_dados: "Fontes de dados disponíveis (bancos, arquivos, APIs, SaaS)"
  optional:
    - esquemas_existentes: "Esquemas existentes ou documentação técnica de dados"
    - contexto_de_uso: "BI, ML, produto data-driven ou relatório executivo"

outputs:
  primary:
    - name: "Data Architecture Blueprint"
      description: "Modelo dimensional, ERD e contratos de dados"
    - name: "Data Pipeline Design Document"
      description: "Design de ETL/ELT com idempotência e boas práticas"
  secondary:
    - "Data Quality Scorecard com regras de validação"

hitl_checkpoints:
  - id: data_governance_validated
    description: "Conformidade LGPD e governança de dados confirmadas"
    required: true
    blocker: true
---

# Tarefa: Arquitetura de Dados, Pipelines e Qualidade

## Visão Geral

Esta tarefa estabelece a fundação técnica de qualquer iniciativa de dados: como os dados
são modelados, como fluem entre sistemas e como sua qualidade é garantida continuamente.
É pré-requisito para a construção de métricas confiáveis e narrativas executivas.

## Passo a Passo

### Passo 1 — HITL: Validação de Governança de Dados

**Responsável:** Usuário/Cliente

**O que confirmar:**
- Dados pessoais presentes nas fontes foram identificados
- Tratamento de dados sensíveis está em conformidade com a LGPD
- Classificação de sensibilidade dos dados está documentada

**Gate de qualidade:** gate `data_governance_validated` do quality-gates.yaml

---

### Passo 2 — Modelagem de Dados

**Agente responsável:** data-architecture-designer

**Ações:**
1. Mapear entidades de negócio e seus relacionamentos a partir das fontes de dados
2. Construir modelo dimensional (fatos e dimensões) ou ERD conforme o caso de uso
3. Definir contratos de dados entre domínios produtores e consumidores
4. Documentar decisões de modelagem (desnormalização, granularidade, chaves)

**Output:** Data Architecture Blueprint

---

### Passo 3 — Design de Pipelines ETL/ELT

**Agente responsável:** etl-pipeline-engineer

**Ações:**
1. Projetar fluxo de extração, transformação e carga conforme as fontes identificadas
2. Definir estratégia de idempotência (upsert, particionamento, watermarking)
3. Especificar orquestração, frequência de execução e tratamento de falhas
4. Documentar linhagem de dados (data lineage) ponta a ponta

**Output:** Data Pipeline Design Document

---

### Passo 4 — Baseline de Qualidade de Dados

**Agente responsável:** data-quality-sentinel

**Ações:**
1. Definir regras de validação: completude, unicidade, consistência, atualidade
2. Estabelecer thresholds de alerta por métrica de qualidade
3. Documentar plano de monitoramento contínuo de qualidade

**Output:** Data Quality Scorecard com regras de validação

---

## Critérios de Qualidade

| Critério | Padrão Mínimo |
|----------|---------------|
| Governança | Conformidade LGPD validada antes de qualquer modelagem |
| Modelagem | Modelo dimensional/ERD documentado e consistente |
| Idempotência | Pipeline seguro para reprocessamento sem duplicação |
| Qualidade | Regras de validação cobrem as 4 dimensões essenciais (completude, unicidade, consistência, atualidade) |

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
