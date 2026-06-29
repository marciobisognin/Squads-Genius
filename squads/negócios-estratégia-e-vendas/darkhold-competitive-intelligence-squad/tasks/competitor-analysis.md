---
task:
  name: competitor-analysis
  id: competitor-analysis
  title: "Análise Completa de Concorrentes"
  icon: "🕵️"
  description: >
    Tarefa de análise competitiva completa: do briefing ao Dossier de Inteligência
    Competitiva consolidado, com rastreabilidade de fontes, SWOT expandido, mapa de
    pricing, análise de patentes, sinais fracos e oportunidades de mercado.
  estimated_duration: "3 a 5 dias úteis (dependendo do número de concorrentes)"
  squad: darkhold-competitive-intelligence-squad
  workflow: competitive-intelligence-pipeline.yaml
  output_format: Dossier de Inteligência Competitiva em formato estruturado

inputs:
  required:
    - nome_do_cliente: "Nome da empresa/produto a ser analisado"
    - lista_de_concorrentes: "Lista de 3 a 10 concorrentes prioritários"
    - perguntas_estrategicas: "3 a 5 perguntas que o dossier deve responder"
    - horizonte_temporal: "Horizonte de análise prospectiva (ex: 6 meses, 12 meses)"
  optional:
    - dominio_tecnologico: "Área tecnológica para análise de patentes"
    - segmentos_prioritarios: "Segmentos de mercado de interesse específico"
    - concorrentes_secundarios: "Players de atenção secundária a monitorar"
    - restricoes_escopo: "O que NÃO deve estar no escopo desta análise"

outputs:
  primary:
    - name: "Dossier de Inteligência Competitiva"
      description: "Documento executivo consolidado com todos os achados e rastreabilidade"
    - name: "Log de Fontes e Rastreabilidade"
      description: "Registro auditável de todas as fontes, datas e níveis de confiança"
  secondary:
    - "Relatório de Movimentos dos Concorrentes (por concorrente)"
    - "Relatório de Sinais Fracos e Wildcards"
    - "SWOT Expandido com Fontes Rastreáveis (cliente + concorrentes)"
    - "Mapa de Precificação Competitiva"
    - "Relatório de Análise de Patentes (se domínio tecnológico definido)"
    - "Whitespace Matrix e Ranking de Oportunidades"

hitl_checkpoints:
  - id: scope_validation
    phase: 1
    description: "Aprovação do escopo pelo cliente antes de iniciar monitoramento"
  - id: dossier_review
    phase: 3
    description: "Revisão do dossier preliminar antes da fase adversarial"
  - id: publication_go_no_go
    phase: 6
    description: "Aprovação final antes da entrega do dossier"
---

# Tarefa: Análise Completa de Concorrentes

## Visão Geral

Esta tarefa aciona o pipeline completo de Inteligência Competitiva do Darkhold Squad para produzir um Dossier rastreável e fundamentado sobre o cenário competitivo do cliente. A tarefa segue as 6 fases do `competitive-intelligence-pipeline.yaml` com gates de qualidade e aprovação humana nos pontos críticos.

## Passo a Passo

### Passo 1 — Definição de Escopo e Lista de Concorrentes (HITL)

**Agente responsável:** darkhold-orchestrator

**Ações:**
1. Coletar do cliente:
   - Nome da empresa e do produto a ser posicionado
   - Lista de concorrentes prioritários (máximo 10 — priorizar 3 a 5 para análise profunda)
   - Perguntas estratégicas que o dossier deve responder (exemplos abaixo)
   - Horizonte temporal de análise (6 ou 12 meses)
   - Segmentos de mercado de maior interesse
2. Identificar gaps no briefing e fazer perguntas de clarificação
3. Redigir documento de escopo com premissas e limitações
4. **HITL:** Submeter escopo ao cliente para validação formal antes de prosseguir

**Exemplos de perguntas estratégicas:**
- "Qual concorrente tem mais chances de lançar um produto que afete nosso segmento core nos próximos 6 meses?"
- "Em quais segmentos de mercado somos mais vulneráveis a ataques competitivos?"
- "Onde existem oportunidades de mercado que nenhum concorrente está explorando adequadamente?"
- "Como nosso pricing se compara à percepção de valor que os clientes têm de nós vs. concorrentes?"

**Output:** Documento de escopo validado pelo cliente

---

### Passo 2 — Ativação do Competitor Radar para Cada Concorrente

**Agente responsável:** competitor-radar

**Ações:**
1. Para cada concorrente da lista aprovada:
   - Monitorar site: mudanças em produto, pricing, features e posicionamento
   - Analisar vagas de emprego: padrões que revelam intenção estratégica
   - Rastrear cobertura de mídia: notícias, press releases, menções
   - Monitorar redes sociais: LinkedIn, Twitter/X, posicionamento
   - Analisar changelogs e release notes
2. Registrar cada dado com: fonte URL, data de captura, data original do evento
3. Escalar alertas críticos imediatamente ao darkhold-orchestrator

**Output:** Relatório de Movimentos por Concorrente + Alertas de Mudanças Críticas

---

### Passo 3 — Execução da Análise SWOT com Verificação de Fontes

**Agente responsável:** swot-deep-analyst

**Ações:**
1. Conduzir SWOT expandido do cliente com nível de confiança por item
2. Conduzir SWOT de cada concorrente prioritário
3. Gerar matriz SWOT comparativa (cliente vs. concorrentes)
4. Sinalizar itens de baixa confiança para revisão HITL
5. Extrair implicações estratégicas por dimensão do SWOT

**Critério de qualidade:** 100% dos itens SWOT com fonte rastreável, data e nível de confiança

**Output:** SWOT Expandido com Fontes + Matriz Comparativa + Implicações Estratégicas

---

### Passo 4 — Mapeamento do Cenário de Pricing

**Agente responsável:** pricing-intel-agent

**Ações:**
1. Mapear pricing de cada concorrente: modelo, tiers, preços, condições
2. Reconstruir histórico de mudanças de preço (via Wayback Machine e fontes secundárias)
3. Analisar posicionamento valor-preço de cada player
4. Identificar vulnerabilidades de pricing exploráveis pelo cliente
5. Mapear comportamentos de desconto e sazonalidade

**Output:** Mapa de Precificação Competitiva + Análise Valor-Preço + Vulnerabilidades de Pricing

---

### Passo 5 — Análise de Portfólio de Patentes

**Agente responsável:** patent-trend-analyst

**Ações (quando domínio tecnológico for relevante):**
1. Pesquisar portfólio de patentes de cada concorrente no Google Patents, USPTO e bases locais
2. Identificar clusters de patentes que revelam apostas tecnológicas
3. Analisar aceleração/desaceleração de depósitos por área
4. Rastrear publicações acadêmicas de P&D corporativo
5. Sinalizar riscos de freedom-to-operate para revisão jurídica especializada

**Output:** Relatório de Análise de Patentes + Mapa de Tendências Tecnológicas + Alertas de Risco de PI

---

### Passo 6 — Detecção de Sinais Fracos e Ameaças Emergentes

**Agente responsável:** weak-signal-detector

**Ações:**
1. Varrer bases de startups (Crunchbase, AngelList, YC cohorts)
2. Monitorar sinais regulatórios em rascunho
3. Identificar tendências tecnológicas emergentes no domínio
4. Mapear migrações de talentos entre players do mercado
5. Gerar lista de wildcards: baixa probabilidade, alto impacto

**Output:** Relatório de Sinais Fracos + Radar de Startups Emergentes + Lista de Wildcards

---

### Passo 7 — HITL: Revisão dos Achados Iniciais

**Responsável:** Usuário/Analista Sênior

**O que revisar:**
- Consistência entre achados de diferentes agentes
- Itens SWOT sinalizados como baixa confiança
- Alertas de mudanças críticas identificados pelo competitor-radar
- Wildcards identificados pelo weak-signal-detector

**Decisão possível:**
- Aprovar dossier preliminar e avançar para fase adversarial
- Solicitar aprofundamento em área específica antes de prosseguir
- Ajustar escopo ou adicionar concorrentes à lista

---

### Passo 8 — Geração do Dossier de Inteligência Competitiva

**Agente responsável:** darkhold-orchestrator

**Ações:**
1. Consolidar todos os outputs dos passos 2 a 6 em dossier unificado
2. Executar quality gates: verificar rastreabilidade, confiança e conformidade ética
3. Gerar sumário executivo com top 5 findings e recomendações priorizadas
4. Gerar log completo de fontes e rastreabilidade
5. **HITL:** Submeter dossier para aprovação final go/no-go antes da entrega

**Estrutura do Dossier Final:**

```
## DOSSIER DE INTELIGÊNCIA COMPETITIVA
Cliente: [nome]
Data de geração: [data]
Período de análise: [período]
Concorrentes analisados: [lista]
Status de aprovação: HITL go/no-go aprovado em [data] por [responsável]

### SUMÁRIO EXECUTIVO
[Top 5 findings + 5 recomendações priorizadas]

### 1. PERFIS E MOVIMENTOS DOS CONCORRENTES
[Por concorrente: movimentos recentes, vagas estratégicas, alertas]

### 2. ANÁLISE SWOT COMPARATIVA
[Matriz SWOT completa com fontes e implicações]

### 3. CENÁRIO DE PRICING COMPETITIVO
[Mapa de pricing + vulnerabilidades identificadas]

### 4. TENDÊNCIAS TECNOLÓGICAS E PATENTES
[Apostas tecnológicas dos concorrentes + riscos de PI]

### 5. SINAIS FRACOS E AMEAÇAS EMERGENTES
[Startups, wildcards, sinais regulatórios]

### 6. OPORTUNIDADES DE MERCADO INEXPLORADAS
[Whitespace matrix + ranking de oportunidades]

### 7. LOG DE FONTES E RASTREABILIDADE
[Registro auditável de todas as fontes]
```

---

## Critérios de Qualidade

| Critério | Padrão Mínimo |
|----------|---------------|
| Rastreabilidade | 100% das afirmações com fonte, data e confiança |
| Cobertura de concorrentes | Todos os concorrentes da lista aprovada analisados |
| HITL gates | Todos os 3 gates executados e registrados |
| Quality gates | Todos os 5 gates do quality-gates.yaml aprovados |
| Conformidade ética | Zero fontes de origem não pública ou não autorizada |

---

## Avisos Importantes

- Esta tarefa utiliza **apenas dados públicos e autorizados**
- Nenhum dado obtido por meios não éticos é aceito em nenhuma fase
- Análise de patentes não substitui parecer jurídico especializado em PI
- HITL gates são obrigatórios — o pipeline não entrega sem aprovação humana nos pontos críticos

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
