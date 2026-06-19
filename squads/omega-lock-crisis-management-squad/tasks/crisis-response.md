---
task: crisis_response
display_name: "Resposta a Crise Corporativa"
owner: omega-lock-orchestrator
atomic_layer: System
license: MIT
creator: "Marcio Bisognin"
instagram: "@marciobisognin"
---

# Task: Resposta a Crise Corporativa

## Objetivo
Conduzir o pipeline completo de resposta a uma crise corporativa desde a detecção até a contenção, mobilizando todos os agentes do squad na sequência e intensidade corretas para o nível de severidade identificado.

## Entradas Obrigatórias

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|------------|-----------|
| `crisis_briefing` | string | sim | Descrição do evento ou sinal de crise detectado |
| `organization_context` | string | sim | Setor, porte, stakeholders principais, histórico relevante |
| `affected_channels` | lista | não | Canais já afetados (mídia, reguladores, operação) |
| `existing_bcp` | arquivo | não | Plano de Continuidade de Negócios pré-existente |
| `legal_context` | string | não | Contexto jurídico preliminar (advogado interno ou externo) |

## Saídas Esperadas

| Artefato | Proprietário | Formato |
|---------|-------------|--------|
| Boletim de Alerta Antecipado | crisis-early-warning-sentinel | Markdown |
| Relatório de Classificação | crisis-classifier | Markdown |
| Kit de Comunicação por Stakeholder | stakeholder-comm-architect | Markdown |
| Parecer Jurídico de Comunicados | legal-risk-interface | Markdown |
| Plano de Continuidade (BCP) | operational-continuity-planner | Markdown |
| Key Messages e Statement Inicial | media-response-strategist | Markdown |
| Crisis Response Playbook | omega-lock-orchestrator | Markdown |

## Checklist de Pré-Condições

- [ ] Briefing inicial da crise disponível
- [ ] Contexto organizacional fornecido
- [ ] Responsável humano identificado (HITL)
- [ ] Canal de comunicação seguro para equipe de crise estabelecido
- [ ] Acesso a sistemas de monitoramento de mídia disponível

## Checklist de Pós-Condições

- [ ] Nível de severidade definido e aprovado (com HITL se >= 3)
- [ ] Todos os comunicados externos revisados pelo jurídico antes de publicação
- [ ] Crisis Response Playbook completo e aprovado
- [ ] BCP ativo para processos críticos afetados
- [ ] Stakeholders críticos comunicados na sequência e canal corretos
- [ ] Decision log completo com todas as decisões e justificativas

## Sequência de Execução

```
1. [crisis-early-warning-sentinel] → Detecção e Boletim de Alerta
2. [crisis-classifier] → Tipificação e Nível de Severidade
   ↳ SE nível >= 3: HITL obrigatório — aguardar aprovação humana
3. [omega-lock-orchestrator] → Abertura do Ciclo e Decision Log
4. [PARALELO]:
   - [stakeholder-comm-architect] → Kit de Comunicação
   - [legal-risk-interface] → Mapa de Riscos Jurídicos
   - [operational-continuity-planner] → BCP
   - [media-response-strategist] → Key Messages + Statement
5. [legal-risk-interface] → Revisão dos comunicados externos
6. [omega-lock-orchestrator] → Consolidação do Crisis Response Playbook
   ↳ HITL obrigatório — aprovação humana antes de execução
7. [crisis-early-warning-sentinel] → Monitoramento de contenção
```

## Critérios de Aceite

- Playbook completo com planos de todas as frentes
- Zero comunicados externos publicados sem revisão jurídica
- Decision log auditável com timestamps e responsáveis
- Nenhum quality gate pulado sem justificativa documentada

## Observações

- Esta task pode ser encerrada antes do pós-mortem se houver urgência operacional
- O pós-mortem deve ser executado como task separada (`business-continuity.md`) após a contenção
- Em crises de Nível 5, toda comunicação deve ser aprovada pelo CEO ou equivalente

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
