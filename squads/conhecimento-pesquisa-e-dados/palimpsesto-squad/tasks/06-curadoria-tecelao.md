# Task 06 — Curadoria (O Tecelão)

**Owner:** `tecelao`
**Camada:** 2 → 3

## Objetivo
Fundir os `VerifiedClaim[]` e `tensions[]` num dossiê coerente, calibrado ao nível de profundidade solicitado, preservando divergências legítimas.

## Passos
1. Receber `VerifiedClaim[]` (pós-gate HITL, quando aplicável) e `tensions[]`.
2. Agrupar por camada disciplinar.
3. Eliminar redundância entre claims equivalentes.
4. Preservar divergências de escola como tal — nunca achatar em falso consenso.
5. Calibrar a seleção/extensão conforme `depth` (1/2/3).
6. Emitir `Dossier` (ver `templates/dossier.schema.json`).

## Critério de aceite
- `Dossier` válido contra o schema.
- Toda divergência de escola identificada por ELENCHUS aparece em `tensions[]`.
