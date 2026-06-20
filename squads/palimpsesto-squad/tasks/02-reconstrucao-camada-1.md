# Task 02 — Reconstrução (Camada 1)

**Owners:** `chronos`, `terra`, `verbum`, `ethos`, `kratos`, `numen`, `nous` (execução em paralelo)
**Camada:** 1

## Objetivo
Cada agente especialista ativado pelo `SACP-IN` reconstrói sua trilha disciplinar e emite `claims[]` com certeza preliminar.

## Passos
1. Receber `SACP-IN` do Triador.
2. Cada trilha ativada produz seus `claims[]` (ver `templates/claim.schema.json`), seguindo sua regra de ouro e semente de prompt (`agents/<trilha>.md`).
3. Aplicar a regra dos três tempos quando o objeto exigir (evento ≠ registro ≠ recepção).
4. Encaminhar todos os `claims[]` consolidados para ÁGON.

## Critério de aceite
- Cada claim tem `preliminary_certainty` e `risk` explícitos.
- Nenhuma trilha ativada deixa de entregar ao menos um claim.
