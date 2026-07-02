# Task 05 — Planejar Task Manifest (DAG)

**Executor:** BOULÉ (mente) + Cortex (validação)
**Fase:** Planejamento (PRD §14.2.4, §14.4, §14.5)

## Objetivo
Produzir o `aether.task-manifest/v1`: decomposição do objetivo em tarefas
atômicas com dependências em DAG, contratos, risco, critérios de aceite e
gates de aprovação.

## Entradas
- Intenção classificada e confirmada + pacote de contexto.

## Saídas
- Task Manifest validado por schema (DAG acíclico, contratos presentes).
- Declaração prévia de ferramentas, permissões e efeitos externos com
  `compensate_with` quando aplicável.

## Passos
1. BOULÉ propõe o manifesto candidato (JSON).
2. Cortex valida: schema, aciclicidade, critério de aceite por tarefa,
   contrato de saída por tarefa, `retry_policy` por tarefa.
3. Efeito externo de risco médio+ sem compensação/idempotência ⇒ rejeitar o
   plano e devolver a BOULÉ com o motivo estruturado.
4. Registrar o manifesto e transitar `classified → planned`.

## Critérios de aceite
- DAG válido (sem ciclos não declarados); ≥2 tarefas com dependência quando o
  objetivo for composto.
- 100% das tarefas com `acceptance_criteria` e `output_contract`.
- Ferramentas/permissões declaradas antes da execução.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
