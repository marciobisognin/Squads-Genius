# Arquitetura do AETHER OS Squad

Implementação em formato de squad da arquitetura de referência do PRD AETHER
OS v1.2. O princípio que atravessa tudo: **modelos raciocinam e propõem; código
determinístico calcula e decide** (Seção 7 do PRD).

## Camadas

| Camada | Implementação neste squad |
|---|---|
| Host Runtime | Hermes Agent (ver `docs/integracao-hermes.md`) |
| Cortex | `agents/aether-cortex.md` + `workflows/aether_master_pipeline.yaml` |
| Cognition Layer (mentes) | `agents/` — KRITÉS, MAIEUTIKÉ, BOULÉ, EKLOGÉ, THÉMIS, ELENCHUS, TEKMÉRION, SÝNTHESIS, MNÉME, AITÍA, HÉPHAISTOS |
| Deterministic Layer (motores) | `scripts/` — selection, risk, budget, quota, dispatch, error-policy, replay |
| Registry & Discovery | `scripts/registry_indexer.py` (aether.squad/v1, estados de confiança) |
| Execution Plane | `scripts/dispatch_engine.py` + `scripts/run_loop.py` (loop de revisão) |
| Memory Plane | `scripts/memory_engine.py` (lições com proveniência/TTL) |
| Governance Plane | `config/risk_policy.yaml` + `scripts/risk_engine.py` + gates |
| Observability Plane | eventos `aether.event/v1` + `scripts/replay_engine.py` |
| Forge Plane | `scripts/forge_bridge.py` + `workflows/capability_gap_forge.yaml` |
| Organization Plane (v1.3) | `agents/oikonomos.md` + `scripts/oikos_engine.py` + `workflows/oikos_pulso_ciclo.yaml` — oikos agenda, nunca executa |
| Persona Plane (v1.3) | `agents/retratista.md` + `scripts/persona_engine.py` + `workflows/retratista_galeria.yaml` — máscara, não juízo |
| Host Plane (v1.3) | `scripts/host_adapter.py` + `config/host_adapters.yaml` — host é driver, degradação determinística |
| Economy Plane (v1.3) | `scripts/token_economy.py` + `config/token_economy.yaml` — neutra, verificada por replay |

## Reprodutibilidade em dois níveis (PRD §7.6)

- **Exata (motores):** mesma entrada ⇒ mesma saída byte a byte, verificada por
  `replay_engine.py` (serialização canônica: `sort_keys`, Decimal textual).
- **Registrada (mentes):** cada chamada grava perfil de modelo pinado, versão
  de prompt, parâmetros e saída bruta; o run-replay reutiliza a saída gravada.

## Códigos de saída dos motores (contrato operacional)

| Código | Significado |
|---|---|
| 0 | sucesso / admit / pass |
| 1 | não retryable / atenção |
| 3 | `capability_gap` (selection) |
| 4 | `budget_exceeded` |
| 5 | `enqueue_soft` (quota) |
| 6 | `refuse_hard` (quota) |
| 7 | handoff rejeitado → dead-letter |
| 8 | divergência de replay (incidente crítico) |
| 9 | loop de revisão não convergiu (partial/failed) |
| 10 | egressão de persona bloqueada (rótulo ausente / personificação) |
| 11 | envelope SACP excede teto de tokens (usar referência) |

## Defesa em profundidade (PRD §23)

1. Separação dado/instrução em todos os handoffs (SACP).
2. Sanitização de padrões de injeção (`sacp_validator.py`).
3. Determinismo como blindagem: motores não são persuadidos por texto.
4. Integridade SHA-256 por handoff; falha ⇒ `integrity_error` + dead-letter.
5. Quarentena de squads inválidos no discovery (nunca executa scripts).
6. ELENCHUS inspeciona conclusões e artefatos forjados.

## Fluxo de dados (resumo)

```text
Hermes -> IntentEnvelope -> KRITÉS (classificação) -> [gate humano/MAIEUTIKÉ]
  -> BOULÉ (Task Manifest DAG) -> registry_indexer (descoberta)
  -> EKLOGÉ (fit) -> selection_engine (decisão | capability_gap -> Forja)
  -> risk_engine (tier -> política -> aprovação) -> dispatch_engine (ordem)
  -> execução (sandbox) -> run_loop (loop de revisão até critérios)
  -> ELENCHUS/TEKMÉRION (contraditório) -> SÝNTHESIS (entrega)
  -> memory_engine + MNÉME (autoaprendizado) -> resposta ao Hermes
```

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
