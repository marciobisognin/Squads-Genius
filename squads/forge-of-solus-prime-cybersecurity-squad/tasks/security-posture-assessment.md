---
task:
  name: security-posture-assessment
  id: security-posture-assessment
  title: "Avaliação de Postura de Segurança (Estritamente Defensiva)"
  icon: "🔱"
  description: >
    Tarefa de avaliação completa da postura de segurança: inventário de ativos, modelagem
    de ameaças, avaliação de vulnerabilidades e perspectiva adversarial conceitual.
    NENHUMA atividade ofensiva real é executada. Pressupõe autorização documentada.
  estimated_duration: "3 a 5 dias úteis"
  squad: forge-of-solus-prime-cybersecurity-squad
  workflow: cybersecurity-pipeline.yaml
  output_format: Scorecard de Postura de Segurança + Relatório de Modelagem de Ameaças

scope_restriction: |
  ⚠️ ESCOPO ESTRITAMENTE DEFENSIVO ⚠️
  Esta tarefa não inclui testes de penetração reais, exploits ou ataques simulados sem
  autorização explícita documentada. Pressupõe autorização prévia do proprietário dos
  ativos avaliados.

inputs:
  required:
    - inventario_ativos: "Inventário parcial ou completo de ativos digitais"
    - contexto_setor: "Setor e perfil de ameaças relevante"
    - autorizacao_documentada: "Documento de autorização do proprietário dos ativos"
  optional:
    - historico_incidentes: "Relatos de incidentes anteriores"

outputs:
  primary:
    - name: "Scorecard de Postura de Segurança"
      description: "Vulnerabilidades priorizadas por CVSS com plano de correção"
    - name: "Relatório de Modelagem de Ameaças"
      description: "Ameaças mapeadas via STRIDE, MITRE ATT&CK e Kill Chain"
  secondary:
    - "Relatório de Inventário de Ativos e Superfície de Ataque"
    - "Relatório de Perspectiva Adversarial para Fortalecimento Defensivo"

hitl_checkpoints:
  - id: scope_and_authorization_confirmation
    description: "Confirmação de escopo defensivo e autorização documentada"
    required: true
    blocker: true
  - id: threat_model_human_review
    description: "Revisão humana do modelo de ameaças"
    required: true
    blocker: true
---

# Tarefa: Avaliação de Postura de Segurança (Estritamente Defensiva)

## Visão Geral

Esta tarefa avalia a postura de segurança atual da organização sem executar qualquer
atividade ofensiva real. Combina inventário de ativos, modelagem de ameaças, avaliação de
vulnerabilidades conhecidas (sem exploração) e uma perspectiva adversarial puramente
conceitual para identificar onde investir esforço defensivo primeiro.

**Pré-requisito obrigatório:** autorização documentada do proprietário dos ativos.

## Passo a Passo

### Passo 1 — HITL: Confirmação de Escopo e Autorização

**Responsável:** Usuário/Responsável de Segurança

**O que confirmar:**
- O escopo da avaliação é estritamente defensivo
- Existe autorização documentada cobrindo todos os ativos a serem avaliados
- Nenhuma atividade ofensiva real será solicitada em qualquer etapa

**Gate de qualidade:** gates `escopo_defensivo_confirmado` e `autorizacao_documentada_verificada`

---

### Passo 2 — Inventário de Ativos e Superfície de Ataque

**Agente responsável:** asset-inventory-mapper

**Ações:**
1. Mapear todos os ativos digitais informados: servidores, aplicações, dados, identidades, terceiros
2. Classificar ativos por criticidade para o negócio
3. Documentar superfície de ataque exposta por categoria de ativo

**Output:** Relatório de Inventário de Ativos e Superfície de Ataque

---

### Passo 3 — Modelagem de Ameaças

**Agente responsável:** threat-model-architect

**Ações:**
1. Aplicar framework STRIDE para cada ativo crítico identificado
2. Mapear táticas e técnicas relevantes do MITRE ATT&CK conforme perfil setorial
3. Construir cadeia de kill chain conceitual para as ameaças mais relevantes

**Output:** Relatório de Modelagem de Ameaças (STRIDE + MITRE ATT&CK)

---

### Passo 4 — HITL: Revisão Humana do Modelo de Ameaças

**Responsável:** Usuário/Profissional de Segurança

**O que revisar:**
- As ameaças mapeadas são plausíveis para o setor e porte da organização
- Não há lacunas óbvias de ameaças relevantes ao contexto

**Gate de qualidade:** gate `modelo_ameacas_revisado_por_humano`

---

### Passo 5 — Avaliação de Vulnerabilidades (Sem Exploração)

**Agente responsável:** vulnerability-assessor

**Ações:**
1. Avaliar vulnerabilidades conhecidas com base em informações já fornecidas (CVEs documentados, configurações relatadas)
2. Pontuar cada vulnerabilidade com CVSS
3. Priorizar por severidade e probabilidade de exploração

**Nota crítica:** Esta etapa NÃO executa scanners ativos ou exploits — trabalha exclusivamente com informações já fornecidas pela organização ou de fontes públicas de CVE.

**Output:** Scorecard de Postura de Segurança com prioridades CVSS

---

### Passo 6 — Perspectiva Adversarial Conceitual

**Agente responsável:** red-team-advisor

**Ações:**
1. Construir cadeias de ataque conceituais com base no inventário, modelo de ameaças e vulnerabilidades já documentados
2. Identificar pontos de maior lacuna de detecção
3. Priorizar recomendações defensivas por impacto de interrupção da cadeia

**Output:** Relatório de Perspectiva Adversarial para Fortalecimento Defensivo

---

## Critérios de Qualidade

| Critério | Padrão Mínimo |
|----------|---------------|
| Autorização | Documentada e verificada antes de qualquer atividade |
| Escopo defensivo | Nenhuma ação ofensiva real em qualquer etapa |
| Cobertura de ativos | Todos os ativos críticos informados estão no inventário |
| Priorização CVSS | 100% das vulnerabilidades com pontuação e priorização |
| Revisão humana | Modelo de ameaças validado por profissional de segurança |

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
