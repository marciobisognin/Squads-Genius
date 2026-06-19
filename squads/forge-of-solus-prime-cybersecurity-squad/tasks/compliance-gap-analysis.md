---
task:
  name: compliance-gap-analysis
  id: compliance-gap-analysis
  title: "Análise de Lacunas de Conformidade e Fortalecimento Defensivo"
  icon: "📋"
  description: >
    Tarefa de análise de lacunas de conformidade (LGPD, ISO 27001, SOC 2, NIST CSF),
    geração de políticas de segurança, playbooks de resposta a incidentes, programa de
    conscientização e avaliação de risco de cadeia de suprimentos.
  estimated_duration: "3 a 4 dias úteis"
  squad: forge-of-solus-prime-cybersecurity-squad
  workflow: cybersecurity-pipeline.yaml
  output_format: Relatório de Lacunas de Conformidade + Pack de Políticas + Playbooks
  prerequisite_task: security-posture-assessment.md

inputs:
  required:
    - escopo_conformidade: "LGPD, ISO 27001, SOC 2, NIST CSF (um ou mais)"
    - documentos_existentes: "Políticas e controles já documentados pela organização"
  optional:
    - historico_incidentes: "Relatos de incidentes anteriores"
    - lista_fornecedores: "Fornecedores e parceiros críticos"

outputs:
  primary:
    - name: "Relatório de Análise de Lacunas de Conformidade"
      description: "Gaps priorizados por risco e esforço de correção"
    - name: "Pack de Políticas de Segurança"
      description: "PSI, BYOD, nuvem, trabalho remoto, classificação de dados"
  secondary:
    - "Playbook de Resposta a Incidentes por tipo de ataque"
    - "Plano de Treinamento e Conscientização em Segurança"
    - "Relatório de Risco de Cadeia de Suprimentos Digitais"

hitl_checkpoints:
  - id: policies_approved_by_client
    description: "Aprovação das políticas de segurança pelo cliente"
    required: true
    blocker: true
  - id: final_human_review
    description: "Revisão final por profissional de segurança qualificado"
    required: true
    blocker: true
---

# Tarefa: Análise de Lacunas de Conformidade e Fortalecimento Defensivo

## Visão Geral

Com a postura de segurança já avaliada na task `security-posture-assessment.md`, esta
tarefa foca em conformidade regulatória, políticas formais, prontidão para incidentes e
conscientização — os pilares de governança da segurança defensiva.

**Pré-requisito:** modelo de ameaças e scorecard de vulnerabilidades já aprovados.

## Passo a Passo

### Passo 1 — Análise de Lacunas de Conformidade

**Agente responsável:** lgpd-iso27001-auditor

**Ações:**
1. Avaliar conformidade atual frente aos frameworks selecionados (LGPD, ISO 27001 Anexo A, SOC 2, NIST CSF)
2. Identificar lacunas específicas por controle/requisito
3. Priorizar lacunas por risco regulatório e esforço de correção

**Output:** Relatório de Análise de Lacunas de Conformidade

---

### Passo 2 — Geração do Pack de Políticas de Segurança

**Agente responsável:** security-policy-writer

**Ações:**
1. Gerar Política de Segurança da Informação (PSI) alinhada às lacunas identificadas
2. Gerar políticas complementares: BYOD, uso de nuvem, trabalho remoto, classificação de dados
3. Garantir que as políticas são realistas para a operação da organização

**Output:** Pack de Políticas de Segurança

---

### Passo 3 — HITL: Aprovação das Políticas pelo Cliente

**Responsável:** Usuário/Cliente

**O que revisar:**
- As políticas são compatíveis com a realidade operacional da organização
- Não criam atrito operacional desproporcional ao risco mitigado

**Gate de qualidade:** gate `politicas_aprovadas_pelo_cliente`

---

### Passo 4 — Playbooks de Resposta a Incidentes

**Agente responsável:** incident-response-planner

**Ações:**
1. Criar playbook de resposta para cada tipo de incidente relevante ao perfil de ameaças (ransomware, vazamento de dados, comprometimento de credenciais, DDoS)
2. Definir papéis, responsabilidades e cadeia de comunicação por playbook
3. Conduzir exercício tabletop conceitual de validação (não simulação real)

**Output:** Playbook de Resposta a Incidentes por tipo de ataque

---

### Passo 5 — Conscientização e Risco de Cadeia de Suprimentos

**Agentes responsáveis:** security-awareness-designer, supply-chain-risk-analyst

**Ações:**
1. Projetar programa de conscientização em segurança com trilhas por função (security-awareness-designer)
2. Desenhar simulações conceituais de phishing para treinamento (sem execução de phishing real sem autorização específica)
3. Avaliar risco de fornecedores e parceiros críticos da cadeia de suprimentos digital (supply-chain-risk-analyst)

**Output:** Plano de Treinamento e Conscientização + Relatório de Risco de Cadeia de Suprimentos

---

### Passo 6 — HITL: Revisão Final por Profissional Qualificado

**Responsável:** Usuário/Profissional de Segurança Qualificado

**O que revisar:**
- Todos os gates anteriores foram aprovados
- O pacote final não contém recomendações que exigem execução ofensiva real
- Disclaimer de escopo defensivo presente em toda a entrega

**Gate de qualidade:** gate `entrega_final_revisada_por_humano`

---

## Critérios de Qualidade

| Critério | Padrão Mínimo |
|----------|---------------|
| Cobertura de frameworks | Todos os frameworks selecionados pelo cliente avaliados |
| Priorização de lacunas | 100% das lacunas com nível de risco e esforço estimado |
| Playbooks completos | Cada tipo de incidente relevante tem playbook com papéis definidos |
| Revisão humana final | Profissional de segurança qualificado revisa antes da entrega |

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
