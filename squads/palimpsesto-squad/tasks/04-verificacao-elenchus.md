# Task 04 — Verificação (ELENCHUS)

**Owner:** `elenchus`
**Camada:** 2 (freio epistemológico)

## Objetivo
Auditar todos os claims (Camada 1 + ÁGON), atribuindo certeza final, status e podando anacronismo, lenda-como-fato ou alucinação.

## Passos
1. Receber todos os `claims[]` pendentes.
2. Para cada claim: atribuir fonte/escola, `certainty`, `status`, `anachronism_check`.
3. Rebaixar qualquer claim duvidoso ("na dúvida, rebaixar").
4. Remover claims alucinados ou anacrônicos, registrando a remoção em `elenchus_note`.
5. Declarar explicitamente lacunas honestas ("desconhecido").
6. Emitir `VerifiedClaim[]` (ver `templates/verified-claim.schema.json`).

## Critério de aceite
- 100% dos claims remanescentes têm `certainty` e `status` explícitos (ou `null`/`desconhecido` quando aplicável).
- Nenhum claim anacrônico passa com `anachronism_check: pass`.
