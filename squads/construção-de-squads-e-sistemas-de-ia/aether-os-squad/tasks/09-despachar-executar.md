# Task 09 — Despachar e Executar sob Quotas

**Executor:** dispatch_engine + quota_engine + budget_engine + executores
selecionados
**Fase:** Execução (PRD §14.6, §22, §26)

## Objetivo
Ordenar as tarefas prontas por despacho determinístico e executá-las sob
quotas, orçamento, sandbox e disjuntores — com toda falha tipada.

## Entradas
- Task Manifest aprovado + selection-decisions + quotas
  (`config/quotas.yaml`) + teto de orçamento do run.

## Saídas
- Decisões de despacho registradas (fatores + ordem), eventos de execução,
  artefatos com sha256, ledgers de orçamento/quota, `aether.error/v1` para
  cada falha.

## Passos
1. Elegibilidade: dependências satisfeitas, aprovação resolvida, quota
   disponível, disjuntor fechado.
2. Ordenação: prioridade do run → justiça entre tenants (round-robin
   ponderado) → caminho crítico (mais dependentes destravados) → desempate
   `(created_at, run_id, task_id)`.
3. Execução: scripts não confiáveis em sandbox (rede negada por padrão,
   limites de CPU/memória/tempo); segredos por alias via broker, nunca em log.
4. Orçamento: aviso soft a 80%, corte hard no teto (`budget_exceeded`).
5. Falha: classe canônica + ação da tabela (`error_policy.yaml`); retries com
   backoff até o limite; `dependency_failed` propaga `skipped` pelo DAG.
6. Efeitos externos executados gravam `CompensationEntry`; falha do run após
   efeitos ⇒ compensação em ordem inversa.

## Critérios de aceite
- Ordem de despacho reprodutível para o mesmo conjunto de tarefas prontas.
- Nenhuma tarefa executada sem quota/orçamento/aprovação resolvidos.
- Toda falha materializada como `aether.error/v1` — zero texto livre.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
