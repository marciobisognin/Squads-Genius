---
task:
  name: scenario-planning
  id: scenario-planning
  title: "Planejamento de Cenários, Wind Tunnel e Roadmap Robusto"
  icon: "🧭"
  description: >
    Tarefa de construção dos quatro cenários futuros, análise de implicações estratégicas,
    teste de robustez das estratégias atuais (wind tunneling) e construção do roadmap
    robusto com indicadores de alerta precoce.
  estimated_duration: "3 a 4 dias úteis"
  squad: mobius-chair-strategic-foresight-squad
  workflow: strategic-foresight-pipeline.yaml
  output_format: Documento dos Quatro Cenários + Roadmap Estratégico Robusto
  prerequisite_task: horizon-scanning.md

inputs:
  required:
    - megatendencias: "Relatório de Megatendências STEEP da task horizon-scanning"
    - sinais_fracos: "Relatório de Sinais Fracos e Wildcards da task horizon-scanning"
    - tecnologias_emergentes: "Mapa de Tecnologias Emergentes da task horizon-scanning"
  optional:
    - estrategias_atuais: "Estratégias atuais da organização para teste no wind-tunnel"

outputs:
  primary:
    - name: "Documento dos Quatro Cenários"
      description: "Matriz 2x2 com narrativas, características e sinais de materialização"
    - name: "Roadmap Estratégico Robusto"
      description: "Ações no-regret, apostas direcionais e opções de hedge"
  secondary:
    - "Relatório de Implicações Estratégicas por Cenário"
    - "Resultados do Wind Tunnel"
    - "Dashboard de Indicadores de Alerta Precoce"

hitl_checkpoints:
  - id: uncertainty_axes_validation
    description: "Validação dos eixos de incerteza crítica antes da construção dos cenários"
    required: true
    blocker: true
  - id: scenario_narratives_review
    description: "Revisão humana das narrativas dos quatro cenários"
    required: true
    blocker: true
  - id: robust_roadmap_approval
    description: "Aprovação do roadmap robusto antes da entrega final"
    required: true
    blocker: true
---

# Tarefa: Planejamento de Cenários, Wind Tunnel e Roadmap Robusto

## Visão Geral

Com a varredura de horizontes concluída, esta tarefa constrói o núcleo estratégico do
squad: os quatro cenários futuros, suas implicações para a organização, o teste de
robustez das estratégias atuais e o roadmap que se sustenta através de múltiplos futuros.

**Pré-requisito:** Relatórios de megatendências, sinais fracos e tecnologias emergentes já aprovados.

## Passo a Passo

### Passo 1 — Seleção dos Eixos de Incerteza Crítica

**Agente responsável:** scenario-architect

**Ações:**
1. Listar todas as incertezas críticas identificadas nos relatórios de varredura
2. Selecionar as 2 incertezas mais críticas e genuinamente incertas (não correlacionadas)
3. Propor a matriz 2x2 resultante

**Output:** Proposta de Eixos de Incerteza

---

### Passo 2 — HITL: Validação dos Eixos de Incerteza

**Responsável:** Usuário/Cliente

**O que revisar:**
- Os eixos escolhidos são realmente críticos para o resultado da organização
- Os eixos são genuinamente incertos, não apenas hipóteses já decididas

**Gate de qualidade:** gate `uncertainty_axes_validation`

---

### Passo 3 — Construção dos Quatro Cenários

**Agente responsável:** scenario-architect

**Ações:**
1. Construir os 4 cenários da matriz com nome, narrativa e características-chave
2. Verificar que os cenários são distintos entre si e plausíveis individualmente
3. Definir sinais de materialização preliminares por cenário

**Output:** Documento dos Quatro Cenários (rascunho)

---

### Passo 4 — Implicações Estratégicas por Cenário

**Agente responsável:** strategic-implications-analyst

**Ações:**
1. Mapear implicações específicas para a organização em cada cenário (produto, mercado, operação, talento, posicionamento)
2. Identificar ameaças e oportunidades por cenário
3. Sinalizar implicações comuns entre múltiplos cenários

**Output:** Relatório de Implicações Estratégicas por Cenário

---

### Passo 5 — HITL: Revisão das Narrativas e Implicações

**Responsável:** Usuário/Cliente

**O que revisar:**
- As narrativas dos 4 cenários fazem sentido para o contexto real da organização
- As implicações mapeadas são específicas, não genéricas de setor

**Gate de qualidade:** gate `scenario_narratives_review`

---

### Passo 6 — Wind Tunnel: Teste das Estratégias Atuais

**Agente responsável:** windtunnel-tester

**Ações:**
1. Testar cada estratégia atual informada pelo cliente contra os 4 cenários
2. Atribuir veredito (Sobrevive/Ajuste/Falha) com diagnóstico por cenário
3. Calcular score de robustez geral por estratégia

**Output:** Resultados do Wind Tunnel

---

### Passo 7 — Construção do Roadmap Robusto

**Agente responsável:** roadmap-forger

**Ações:**
1. Identificar ações no-regret a partir dos resultados do wind tunnel
2. Mapear apostas direcionais condicionadas a cenários específicos
3. Definir opções de hedge de baixo custo

**Output:** Roadmap Estratégico Robusto

---

### Passo 8 — Indicadores de Alerta Precoce

**Agente responsável:** early-indicator-designer

**Ações:**
1. Projetar 3 a 5 indicadores observáveis por cenário
2. Definir fonte de verificação, frequência e threshold de alerta para cada indicador

**Output:** Dashboard de Indicadores de Alerta Precoce

---

### Passo 9 — HITL: Aprovação do Roadmap Robusto

**Responsável:** Usuário/Cliente

**O que revisar:**
- As ações no-regret são realmente viáveis com os recursos da organização
- As apostas direcionais têm indicadores de gatilho claros

**Gate de qualidade:** gate `robust_roadmap_approval`

---

## Critérios de Qualidade

| Critério | Padrão Mínimo |
|----------|---------------|
| Distinção dos cenários | Os 4 cenários são plausíveis, distintos e consistentes internamente |
| Cobertura de implicações | Todas as 5 dimensões cobertas em cada um dos 4 cenários |
| Wind tunnel completo | Toda estratégia informada testada contra os 4 cenários |
| Roadmap robusto | Ações no-regret priorizadas antes de apostas direcionais |
| Indicadores mensuráveis | Cada indicador tem fonte de verificação e threshold claro |

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
