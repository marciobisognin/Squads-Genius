# Task 07 — Seleção Determinística (Matchmaking)

**Executor:** EKLOGÉ (mente, sinal) + selection_engine (motor, decisão)
**Fase:** Matchmaking (PRD §12, §14.2.5)

## Objetivo
Para cada tarefa do Task Manifest, escolher o squad/agente/ferramenta executor
por **decisão reproduzível**: gates rígidos eliminatórios + score ponderado —
ou emitir `capability_gap` legítimo.

## Entradas
- Task Manifest + Registry indexado + propostas `semantic_fit` de EKLOGÉ +
  pesos de `config/selection_weights.yaml`.

## Saídas
- `aether.selection-decision/v1` por tarefa: candidatos, gates aplicados,
  sub-scores, pesos, score final (Decimal), escolhido e justificativa — ou
  `capability_gap: true`.

## Passos
1. Gates binários por candidato: compatibilidade de contrato, estado de
   confiança, permissões ⊆ autorizadas, residência de dados, saúde.
2. EKLOGÉ propõe `semantic_fit` (0–1) **somente** para quem passou nos gates.
3. `python3 scripts/selection_engine.py --request <sel_request.json>` calcula
   `score = w_fit*fit + w_quality*quality + w_freshness*freshness -
   w_risk*risk - w_cost*cost - w_latency*latency` em Decimal.
4. Empate: confiança desc → custo asc → latência asc → id lexicográfico.
5. Nenhum candidato elegível ⇒ `capability_gap` ⇒ Task 12 (Forja).

## Critérios de aceite
- Decisão reproduz byte a byte no decision-replay (Task de auditoria).
- Nenhum candidato reprovado em gate foi promovido "pela nota semântica".
- Breakdown completo persistido como `SelectionDecision`.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
