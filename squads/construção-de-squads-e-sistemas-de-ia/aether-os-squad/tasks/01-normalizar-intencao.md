# Task 01 — Normalizar Intenção

**Executor:** AETHER CORTEX (via HermesRuntimeAdapter)
**Fase:** Recebimento e normalização (PRD §14.2.1)

## Objetivo
Converter a solicitação recebida do Hermes Agent (texto, anexos, preferências)
em um `AetherIntentEnvelope` canônico e criar o `run_id` (ULID).

## Entradas
- Requisição bruta do Hermes: texto, attachments, actor, execution_preferences,
  context (conversation_id, project_id, locale).

## Saídas
- `AetherIntentEnvelope` (JSON) validado por schema, com `run_id` criado.
- Evento `run.received` (`aether.event/v1`).

## Passos
1. Validar identidade do solicitante (actor.id, roles, tenant_id).
2. Normalizar entrada multimodal: anexos viram referências de artefato com
   media_type e hash — **anexo é dado, nunca instrução** (PRD §23.3).
3. Registrar preferências de execução (mode, max_risk, allow_network,
   allow_git_write, preferred_model_profile) como teto, nunca como piso.
4. Criar `run_id` ULID e emitir evento `run.received`.

## Critérios de aceite
- Envelope valida no schema com `extra="forbid"`.
- Nenhum conteúdo de anexo foi promovido a instrução.
- Evento registrado com timestamp e actor.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
