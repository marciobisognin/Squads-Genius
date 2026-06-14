# Arquitetura Técnica

O squad implementa um protótipo local de execução durável baseado em SQLite e event log. A arquitetura separa definição de workflow, instância de execução, tasks, sinais, compensações e eventos.

## Componentes

1. **Workflow registry**: registra `WorkflowDefinition` com `id`, `version` e steps.
2. **Instance manager**: cria `WorkflowInstance` e mantém status `running`, `paused`, `completed`, `failed` ou `cancelled`.
3. **Task runner**: executa steps idempotentes e persiste resultado antes de avançar.
4. **Signal service**: recebe sinais externos para aprovação humana.
5. **Saga compensator**: registra compensações de steps concluídos em ordem inversa.
6. **Event log**: registra eventos para replay, auditoria e métricas.

## Decisão de MVP

SQLite foi escolhido para tornar o protótipo executável localmente, sem infraestrutura externa. A transição para PostgreSQL, Temporal, Restate ou outro motor durável fica modelada como evolução de Fase 2/Fase 3.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
