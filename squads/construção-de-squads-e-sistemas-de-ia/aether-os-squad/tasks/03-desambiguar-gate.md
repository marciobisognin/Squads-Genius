# Task 03 — Desambiguar no Gate de Classificação

**Executor:** MAIEUTIKÉ (mente) + operador humano
**Fase:** Gate HITL de classificação (PRD §13.3)

## Objetivo
Preparar a decisão humana quando o gate é acionado por ambiguidade: menor
conjunto de perguntas + interpretações candidatas com consequências.

## Entradas
- `aether.intake-classification/v1` com `requires_classification_gate: true`.

## Saídas
- `aether.disambiguation/v1` (perguntas + interpretações).
- Confirmação/ajuste humano registrado: objetivo primário, escopo, classe de
  dado, modo de execução e teto de risco.

## Passos
1. MAIEUTIKÉ gera perguntas mínimas (cada uma elimina ≥1 interpretação).
2. Apresentar interpretações lado a lado com consequências (escopo, risco,
   custo, efeitos externos).
3. Operador confirma ou ajusta; o run transita `awaiting_classification →
   classified` ou `→ aborted` (negado/expirado).

## Critérios de aceite
- Nenhuma pergunta genérica ("esclareça") — todas resolvem algo específico.
- A escolha humana referencia uma interpretação identificada (`i1`, `i2`…).
- Evento de gate registrado com identidade, decisão e timestamp.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
