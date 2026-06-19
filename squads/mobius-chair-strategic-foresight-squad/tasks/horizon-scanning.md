---
task:
  name: horizon-scanning
  id: horizon-scanning
  title: "Varredura de Horizontes: Megatendências, Sinais Fracos e Tecnologias"
  icon: "🔭"
  description: >
    Tarefa de varredura completa do ambiente estratégico: megatendências STEEP, sinais
    fracos de fronteira e tecnologias emergentes posicionadas no hype cycle. Base
    epistemológica para a construção de cenários.
  estimated_duration: "2 a 3 dias úteis"
  squad: mobius-chair-strategic-foresight-squad
  workflow: strategic-foresight-pipeline.yaml
  output_format: Relatório de Megatendências STEEP + Relatório de Sinais Fracos + Mapa de Tecnologias

inputs:
  required:
    - nome_organizacao: "Nome da organização e setor de atuação"
    - questao_focal: "Questão estratégica focal validada"
    - horizonte_temporal: "Horizonte de análise (ex: 2030, 2035, 2040)"
  optional:
    - escopo_geografico: "Global, regional, nacional"

outputs:
  primary:
    - name: "Relatório de Megatendências STEEP"
      description: "Tendências Social, Tecnológico, Econômico, Ambiental, Político com fonte e confiança"
    - name: "Relatório de Sinais Fracos e Wildcards"
      description: "Sinais de fronteira classificados por confiança"
  secondary:
    - "Mapa de Tecnologias Emergentes no Hype Cycle"

hitl_checkpoints:
  - id: focal_question_approval
    description: "Aprovação humana do contexto estratégico e questão focal"
    required: true
    blocker: true
---

# Tarefa: Varredura de Horizontes

## Visão Geral

Esta tarefa é a fundação epistemológica do pipeline Mobius Chair. Antes de construir
qualquer cenário, é preciso varrer o ambiente estratégico com rigor: o que já é tendência
confirmada, o que ainda é sinal fraco e quais tecnologias emergentes merecem atenção.

## Passo a Passo

### Passo 1 — HITL: Validação da Questão Focal

**Responsável:** Usuário/Cliente

**O que confirmar:**
- A questão estratégica focal é específica e respondível via inteligência de futuros
- O horizonte temporal é realista para o tipo de análise solicitada

**Gate de qualidade:** gate `focal_question_approval`

---

### Passo 2 — Varredura de Megatendências STEEP

**Agente responsável:** horizon-scanner

**Ações:**
1. Varrer tendências Sociais, Tecnológicas, Econômicas, Ambientais e Políticas relevantes ao setor e horizonte
2. Classificar cada tendência por categoria epistemológica (Fato Estabelecido, Tendência Confirmada, Tendência Emergente)
3. Documentar fonte e grau de confiança para cada tendência

**Output:** Relatório de Megatendências STEEP

---

### Passo 3 — Detecção de Sinais Fracos e Wildcards

**Agente responsável:** weak-signal-detector

**Ações:**
1. Varrer fontes de fronteira: pesquisa acadêmica early-stage, patentes, comunidades de nicho, rascunhos regulatórios
2. Classificar sinais por categoria e nível de confiança (Confirmado/Isolado/Especulação/Wildcard)
3. Catalogar wildcards de baixa probabilidade e alto impacto sistêmico

**Output:** Relatório de Sinais Fracos e Wildcards

---

### Passo 4 — Mapeamento de Tecnologias Emergentes

**Agente responsável:** emerging-tech-analyst

**Ações:**
1. Identificar tecnologias emergentes relevantes ao escopo estratégico
2. Posicionar cada tecnologia no Gartner Hype Cycle com evidência de adoção real
3. Relacionar tecnologias às megatendências e sinais fracos já identificados

**Output:** Mapa de Tecnologias Emergentes no Hype Cycle

---

## Critérios de Qualidade

| Critério | Padrão Mínimo |
|----------|---------------|
| Epistemologia | 100% das afirmações rotuladas por categoria epistemológica |
| Rastreabilidade | Toda tendência e sinal fraco tem fonte e data |
| Cobertura STEEP | Todas as 5 dimensões (Social, Tecnológico, Econômico, Ambiental, Político) cobertas |
| Tecnologias com evidência | Cada tecnologia mapeada tem evidência real de adoção, não apenas hype de mídia |

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
