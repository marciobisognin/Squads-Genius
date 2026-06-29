# scriba-instrument-router

## Missão
Decide o `instrument_type` (minuta_inicial · termo_aditivo · apostilamento ·
repactuacao) pela tabela-decisão determinística do compêndio (§11). **Regras
puras — sem LLM, sem julgamento subjetivo.**

## Implementação
- Código: `scripts/scriba_router.py` (`rotear_instrumento(facts)`).
- Ordem de avaliação respeita a "regra de ouro" (compêndio §3.1): situações que
  **inovam** a base contratual (termo aditivo) são avaliadas antes das que
  apenas **registram** efeito de cláusula preexistente (apostilamento).
- Cada decisão carrega `rationale` + `legal_refs` + flags de HITL
  (`needs_hitl`, `hitl_gate`).

## Saída
- `instrument_decision.json` — `{instrument_type, rationale, legal_refs,
  needs_hitl, hitl_gate}`.

## Casos sem correspondência
Se nenhuma situação de `contract_facts` casar com a tabela, levanta erro e
sinaliza Cynefin `Complex`/`Chaotic` ao Orchestrator — nunca decide por
aproximação.

## Regras obrigatórias
- Determinismo: mesma entrada → mesma decisão.
- Toda decisão cita o dispositivo que a fundamenta.
- Footer obrigatório na entrega documental.

## Comandos
- `*help` · `*run` · `*review` · `*exit`
