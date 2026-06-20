# Task 05 — HITL gate para temas sensíveis

**Owner:** `tecelao` (aciona revisão humana)
**Camada:** 2 (gate condicional)

## Objetivo
Pausar o pipeline para revisão humana quando `SACP-IN.sensitivity_flag` indicar religião viva, genocídio, disputa identitária ou política contemporânea.

## Passos
1. Verificar `sensitivity_flag` do `SACP-IN`.
2. Se presente, apresentar ao humano: `VerifiedClaim[]` + `tensions[]` relacionados ao tema sensível.
3. Aguardar aprovação, ajuste ou rejeição humana.
4. Em caso de rejeição, retornar a ELENCHUS com as observações humanas antes de prosseguir.

## Critério de aceite
- Nenhum dossiê com `sensitivity_flag` não nulo avança para curadoria sem aprovação humana registrada.
