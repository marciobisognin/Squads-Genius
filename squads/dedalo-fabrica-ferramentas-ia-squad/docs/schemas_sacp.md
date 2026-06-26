# Contratos SACP — DÉDALO

> SACP = Structured Agent Communication Protocol. Todo handoff é um envelope tipado,
> versionado, com `provenance` e `confidence`. Implementação: `schemas/sacp_envelope.py`.

## Envelope
```json
{
  "sacp_version": "1.0",
  "run_id": "forge-2026-06-26-a1b2",
  "from_agent": "KAIROS",
  "to_agent": "LOGISTES",
  "payload_type": "OpportunityMap",
  "payload": { "opportunities": [] },
  "provenance": {
    "agent": "KAIROS", "evidence_type": "hipotese",
    "source_refs": ["IG:DZ82MqEMUA8@01:12"],
    "timestamp": "2026-06-26T14:40:00Z", "confidence": 0.68
  },
  "schema_valid": true
}
```

## Regras SACP
1. `schema_valid` é setado pela Guilda de Turing.
2. `confidence < 0.6` aciona auditoria de ELENCHUS (`needs_redteam_audit`).
3. Todo payload de domínio carrega `maps_to_evidence` ou marca explícita de hipótese.
4. Nenhuma nota numérica trafega sem origem.

## Payloads de domínio (`schemas/agent_payloads.py`)
- `SourcePackage` (SKOPÓS) · `OpportunityMap`/`Opportunity`/`OppScoringAssumptions` (KAIRÓS)
- `RedTeamReport` (ELENCHUS) · `ValidationReport` (NÓMOS)

## Estado global (`schemas/global_state.py`)
- `GlobalState` com fatias por agente, `hitl_gates`, `healing_log`, `langfuse_trace_id`.
- Pydantic quando disponível; fallback dataclasses (stdlib) sem perder a forma.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
