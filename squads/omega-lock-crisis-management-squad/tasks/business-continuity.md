---
task: business_continuity
display_name: "Continuidade de Negócios e Pós-Mortem"
owner: operational-continuity-planner
atomic_layer: Organism
license: MIT
creator: "Marcio Bisognin"
instagram: "@marciobisognin"
---

# Task: Continuidade de Negócios e Pós-Mortem

## Objetivo
Garantir a continuidade das operações críticas durante a crise e, após a contenção, conduzir a análise pós-mortem completa que transforme o evento em aprendizado organizacional duradouro.

## Entradas Obrigatórias

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|------------|-----------|
| `crisis_response_playbook` | arquivo | sim | Playbook gerado pela task de resposta à crise |
| `affected_processes` | lista | sim | Lista de processos impactados pela crise |
| `organizational_structure` | string | não | Estrutura de equipes e responsáveis por área |
| `existing_bcp` | arquivo | não | BCP pré-existente para referência e atualização |
| `crisis_decision_log` | arquivo | sim | Log de decisões da fase de resposta |

## Saídas Esperadas

| Artefato | Proprietário | Formato |
|---------|-------------|--------|
| Business Impact Analysis (BIA) | operational-continuity-planner | Markdown |
| Plano de Continuidade de Negócios (BCP) | operational-continuity-planner | Markdown |
| Matriz de RTO/RPO | operational-continuity-planner | Markdown/Tabela |
| Diagnóstico Reputacional Pós-Crise | reputation-recovery-designer | Markdown |
| Roadmap de Recuperação Reputacional | reputation-recovery-designer | Markdown |
| Relatório de Pós-Mortem | post-mortem-analyst | Markdown |
| Plano de Ação Preventiva | post-mortem-analyst | Markdown |

## Checklist de Pré-Condições

- [ ] Crise em fase de contenção (sinais em queda por pelo menos 24h)
- [ ] Crisis Response Playbook da fase ativa disponível
- [ ] Decision log da fase de resposta completo
- [ ] Equipe de continuidade identificada e disponível
- [ ] Responsável pelo pós-mortem definido (pode ser externo/facilitador neutro)

## Checklist de Pós-Condições

- [ ] Todos os processos críticos com rota alternativa documentada
- [ ] BIA completo com criticidade, RTO e RPO por processo
- [ ] Diagnóstico reputacional conduzido com indicadores medidos
- [ ] Roadmap de recuperação aprovado com KRIs e metas
- [ ] Pós-mortem com causa-raiz identificada (5 Porquês e Fishbone)
- [ ] Plano de ação com 100% dos itens com proprietário e prazo
- [ ] Playbook de crise atualizado com lições aprendidas
- [ ] Aprovação formal do pós-mortem pela liderança

## Sequência de Execução

```
FASE A — CONTINUIDADE (executar durante e após a crise ativa):
1. [operational-continuity-planner] → Business Impact Analysis
2. [operational-continuity-planner] → Ativação do BCP
3. [operational-continuity-planner] → Monitoramento de recuperação operacional

FASE B — RECUPERAÇÃO REPUTACIONAL (iniciar após contenção):
4. [reputation-recovery-designer] → Diagnóstico reputacional pós-crise
5. [reputation-recovery-designer] → Roadmap de recuperação em 4 fases
6. [reputation-recovery-designer] → Dashboard de KRIs reputacionais

FASE C — PÓS-MORTEM (conduzir após estabilização):
7. [post-mortem-analyst] → Coleta e organização de evidências
8. [post-mortem-analyst] → Análise de causa-raiz (5 Porquês + Fishbone)
9. [post-mortem-analyst] → After Action Review por frente
10. [post-mortem-analyst] → Relatório de Pós-Mortem + Plano de Ação
    ↳ HITL obrigatório — aprovação da liderança antes de publicar
11. [omega-lock-orchestrator] → Encerramento formal do ciclo de crise
```

## Framework de Análise Pós-Mortem (Referência)

### 5 Porquês — Template
```
EVENTO CENTRAL: [o que aconteceu]
Por quê 1: [primeira causa]
Por quê 2: [causa da causa 1]
Por quê 3: [causa da causa 2]
Por quê 4: [causa da causa 3]
Por quê 5: [causa-raiz final]
AÇÃO CORRETIVA: [o que deve mudar]
```

### After Action Review — Template
```
O QUE FOI PLANEJADO: [intenção original]
O QUE ACONTECEU: [realidade observada]
POR QUE DIFERIU: [análise do gap]
O QUE APRENDER: [lição extraída]
AÇÃO RESULTANTE: [mudança concreta com proprietário e prazo]
```

## Critérios de Aceite

- BIA completo com 100% dos processos críticos mapeados
- Pós-mortem com pelo menos uma causa-raiz identificada por via do 5 Porquês
- Plano de ação com proprietário, prazo e indicador para cada item
- Recomendações de atualização do playbook documentadas e aceitas
- Ciclo de crise encerrado formalmente pelo orchestrator

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
