---
task:
  name: adversarial-scenarios
  id: adversarial-scenarios
  title: "Planejamento de Cenários Adversariais e Red Team Competitivo"
  icon: "🎯"
  description: >
    Tarefa focada na construção de cenários adversariais prospectivos e análise de
    red team competitivo. Antecipa movimentos dos concorrentes nos próximos 6 a 12 meses,
    identifica vulnerabilidades do cliente e desenvolve planos de defesa preventiva.
    Requer aprovação HITL para cenários de alto impacto.
  estimated_duration: "2 a 3 dias úteis"
  squad: darkhold-competitive-intelligence-squad
  workflow: competitive-intelligence-pipeline.yaml
  output_format: Relatório de Cenários Adversariais + Relatório de Vulnerabilidades Estratégicas
  prerequisite_task: competitor-analysis.md

inputs:
  required:
    - dossier_preliminar: "Outputs das fases de monitoramento e análise (passo 1 a 6 da task competitor-analysis)"
    - perguntas_estrategicas: "O que queremos antecipar? Quais movimentos nos preocupam mais?"
    - horizonte_temporal: "Horizonte de análise prospectiva (6 meses, 12 meses)"
    - lista_concorrentes: "Lista de concorrentes para simular ataques"
  optional:
    - segmentos_criticos: "Segmentos de clientes que mais nos preocupam perder"
    - eventos_gatilho: "Eventos específicos a monitorar como gatilhos de cenários"
    - restricoes: "Restrições do cliente ao tipo de cenário (ex: não incluir cenários de M&A)"

outputs:
  primary:
    - name: "Relatório de Cenários Adversariais"
      description: "3 a 5 cenários com probabilidade, impacto, alertas precoces e respostas — HITL aprovado"
    - name: "Relatório de Vulnerabilidades Estratégicas"
      description: "Mapa de vulnerabilidades do cliente com plano de defesa preventiva"
  secondary:
    - "Matriz de Priorização Probabilidade × Impacto"
    - "Lista de Indicadores de Alerta Precoce Consolidados"
    - "Simulações de Ataque por Concorrente"
    - "Mapa de Blind Spots Estratégicos"

hitl_checkpoints:
  - id: adversarial_scenarios_approval
    description: "Aprovação humana de cenários com impacto ≥ 4 e probabilidade ≥ 30%"
    required: true
    blocker: true
---

# Tarefa: Planejamento de Cenários Adversariais e Red Team

## Visão Geral

Esta tarefa é a fase adversarial do pipeline Darkhold. Enquanto a task `competitor-analysis` coleta e analisa o cenário atual, esta task projeta o futuro: o que os concorrentes provavelmente farão e onde o cliente está exposto. Dois agentes trabalham em perspectivas complementares — o adversarial-scenario-planner antecipa movimentos dos concorrentes, o red-team-strategist adota a perspectiva do atacante para revelar vulnerabilidades.

**Pré-requisito:** Esta tarefa pressupõe que o dossier preliminar da task `competitor-analysis` está concluído e aprovado no HITL de revisão intermediária.

## Passo a Passo

### Passo 1 — Definição das Questões Estratégicas

**Agente responsável:** darkhold-orchestrator

**Ações:**
1. Revisar o dossier preliminar e identificar as perguntas estratégicas mais urgentes:
   - Quais concorrentes têm maior capacidade de ataque nos próximos 6-12 meses?
   - Quais movimentos competitivos nos preocupam mais?
   - Em quais segmentos somos mais vulneráveis?
2. Definir o horizonte temporal para os cenários
3. Identificar eventos-gatilho prioritários a monitorar
4. Briefar os agentes adversariais com contexto do dossier preliminar

**Output:** Briefing adversarial estruturado para os agentes especializados

---

### Passo 2 — Análise de Red Team (Nossas Vulnerabilidades)

**Agente responsável:** red-team-strategist

**Ações:**
1. Adotar a perspectiva de cada concorrente principal:
   - "Se eu fosse o [Concorrente X], como atacaria a posição de mercado do cliente?"
2. Identificar segmentos de clientes mais vulneráveis a ataques competitivos
3. Mapear gaps de produto e pricing que concorrentes podem explorar
4. Identificar blind spots: assunções estratégicas do cliente que podem estar erradas
5. Para cada vulnerabilidade identificada: definir uma recomendação defensiva correspondente

**Critério de qualidade:** Cada vulnerabilidade tem: evidência de base, concorrente mais provável de explorar, impacto estimado e recomendação defensiva

**Output:** Mapa de Vulnerabilidades Estratégicas + Simulações de Ataque + Blind Spots

---

### Passo 3 — Construção dos Cenários Adversariais com Avaliação de Probabilidade

**Agente responsável:** adversarial-scenario-planner

**Ações:**
1. Com base no dossier preliminar e no red team, construir 3 a 5 cenários adversariais:
   - Cada cenário descreve um movimento específico que um concorrente poderia executar
   - Cenários são baseados em sinais observados — não especulação pura
2. Para cada cenário, atribuir:
   - Probabilidade (%) com justificativa explícita
   - Impacto para o cliente (escala 1-5)
   - Horizonte temporal (0-3m, 3-6m, 6-12m)
   - Gatilhos aceleradores (eventos que, se ocorrerem, aceleram o cenário)
3. Garantir cobertura de pelo menos um cenário por tipo:
   - Lançamento de produto/feature
   - Movimento de pricing
   - Expansão geográfica ou de segmento
   - Parceria estratégica ou M&A (se aplicável ao contexto)

**Output:** Rascunho de 3-5 Cenários Adversariais com Probabilidade e Impacto

---

### Passo 4 — Definição de Indicadores de Alerta Precoce por Cenário

**Agente responsável:** adversarial-scenario-planner

**Ações:**
1. Para cada cenário adversarial, definir 3 a 5 indicadores de alerta precoce:
   - Sinais monitoráveis publicamente que indicam que o cenário está se materializando
   - Fontes onde esses sinais seriam observados primeiro
2. Organizar indicadores em dashboard de monitoramento contínuo
3. Definir frequência de verificação para cada indicador

**Exemplos de indicadores:**
- Vagas específicas abertas → indício de expansão geográfica
- Changelog com feature X → indício de ataque ao diferencial do cliente
- Notícia de captação de rodada → indício de capacidade de guerra de preços
- Parceria anunciada com player Y → indício de movimento de ecossistema

**Output:** Dashboard de Indicadores de Alerta Precoce por Cenário

---

### Passo 5 — Desenvolvimento de Planos de Contingência

**Agente responsável:** adversarial-scenario-planner

**Ações:**
1. Para cada cenário de alta prioridade (probabilidade ≥ 30% ou impacto ≥ 4):
   - Esboçar plano de resposta imediata (primeiros 30 dias se o cenário se materializar)
   - Definir gatilhos para ativação do plano de resposta
   - Identificar recursos necessários para a resposta
2. Priorizar cenários na Matriz Probabilidade × Impacto:
   - Alta prob. + alto impacto: Ação imediata — desenvolver resposta detalhada
   - Alta prob. + baixo impacto: Monitorar — resposta padrão suficiente
   - Baixa prob. + alto impacto: Contingência — preparar plano básico
   - Baixa prob. + baixo impacto: Ignorar por ora

**Output:** Planos de Resposta Priorizados por Cenário

---

### Passo 6 — HITL: Aprovação de Cenários Críticos

**Responsável:** Usuário/Gestor Estratégico

**O que revisar:**
- Todos os cenários com impacto ≥ 4 e probabilidade ≥ 30%
- Justificativas de probabilidade: fazem sentido com o conhecimento interno do gestor?
- Blind spots identificados pelo red team: há discordância ou contexto adicional a adicionar?
- Recomendações defensivas: são executáveis com os recursos disponíveis?

**Decisão possível:**
- Aprovar cenários para inclusão no relatório final
- Solicitar ajuste de probabilidade com justificativa adicional
- Adicionar contexto interno que modifica a análise
- Remover cenário por não ser aplicável ao contexto real

**Gate de qualidade:** gate `adversarial_scenarios_reviewed_by_human` do quality-gates.yaml

---

### Passo 7 — Entrega do Relatório de Cenários Adversariais

**Agente responsável:** darkhold-orchestrator

**Ações:**
1. Consolidar cenários aprovados no Relatório Final de Cenários Adversariais
2. Consolidar vulnerabilidades aprovadas no Relatório de Vulnerabilidades Estratégicas
3. Integrar ambos os relatórios ao Dossier de Inteligência Competitiva (se task vinculada ao pipeline completo)
4. Registrar aprovações HITL no log de rastreabilidade

**Estrutura do Relatório Final:**

```
## RELATÓRIO DE CENÁRIOS ADVERSARIAIS E RED TEAM
Cliente: [nome]
Data: [data]
Horizonte de análise: [período]
Status HITL: Aprovado em [data] por [responsável]

### SUMÁRIO EXECUTIVO ADVERSARIAL
[Top 3 cenários de maior prioridade + top 3 vulnerabilidades críticas]

### CENÁRIOS ADVERSARIAIS (Aprovados por HITL)
[Para cada cenário: título, descrição, probabilidade, impacto, horizonte,
gatilhos, indicadores de alerta precoce, plano de resposta]

### MATRIZ DE PRIORIZAÇÃO (Probabilidade × Impacto)
[Quadrante com posicionamento de cada cenário]

### RELATÓRIO DE VULNERABILIDADES ESTRATÉGICAS
[Para cada vulnerabilidade: descrição, concorrente mais provável,
segmento exposto, impacto, recomendação defensiva, urgência]

### BLIND SPOTS IDENTIFICADOS
[Assunções estratégicas do cliente que merecem revisão]

### DASHBOARD DE INDICADORES DE ALERTA PRECOCE
[Lista integrada de todos os sinais a monitorar por fonte]

### PLANOS DE DEFESA PREVENTIVA
[Por vulnerabilidade de alta prioridade: ação, responsável, prazo]

### LOG DE RASTREABILIDADE
[Fontes e aprovações HITL documentadas]
```

---

## Critérios de Qualidade

| Critério | Padrão Mínimo |
|----------|---------------|
| Número de cenários | 3 a 5 cenários (não mais, não menos) |
| Cobertura de concorrentes | Todos os concorrentes prioritários com ao menos 1 cenário |
| Probabilidade justificada | 100% dos cenários com justificativa explícita |
| HITL obrigatório | Todos os cenários de impacto ≥ 4 ou prob ≥ 30% aprovados por humano |
| Indicadores monitoráveis | Cada cenário com 3 a 5 indicadores de alerta precoce públicos |
| Recomendações defensivas | 100% das vulnerabilidades com recomendação correspondente |

---

## Avisos Importantes

- Cenários adversariais são projeções fundamentadas em dados públicos — não previsões certas
- Probabilidades são estimativas estratégicas, não cálculos probabilísticos formais
- A análise de red team não revela informações confidenciais dos concorrentes
- HITL obrigatório: cenários de alto impacto nunca são entregues sem aprovação humana
- Recomendações defensivas são estratégicas — implementação requer avaliação do cliente com seu contexto interno

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
