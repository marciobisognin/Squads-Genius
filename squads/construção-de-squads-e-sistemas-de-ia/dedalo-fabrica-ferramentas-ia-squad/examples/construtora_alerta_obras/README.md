# Exemplo — Construtora · Alerta de Obras (`construction_control`)

> Cenário de demonstração do DÉDALO (Família D · operacional de nicho).

## Intake
- **Fonte:** processo de acompanhamento de obra (prazo/orçamento/clima/material).
- **Dor:** estouros de prazo e orçamento descobertos tarde.
- **output_mode:** `prd_plus_mvp`.

## Caminho esperado no pipeline
1. HÓROS classifica como **complexo** ⇒ 2 ciclos de ELENCHUS + data discovery.
2. TÉCHNE mapeia o processo de medição; marca anti_automation_flags se o processo for ruim.
3. LOGISTÉS aponta data_gaps (diário de obra incompleto).
4. Após HITL#2, HÉPHAISTOS gera dashboard local (HTML/SQLite) + smoke test.

## Saídas
- `output/prd.md`, `output/architecture.md`, `output/backlog.md`, `output/prototype/`.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
