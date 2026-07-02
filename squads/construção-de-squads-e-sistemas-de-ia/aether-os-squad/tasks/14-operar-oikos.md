# Task 14 — Operar Oikos (Organização Persistente)

**Executor:** OIKONÓMOS (mente) + oikos_engine (motor) + pipeline mestre
**Fase:** Organizações persistentes (PRD v1.3, §17.5–17.9)

## Objetivo
Operar um oikos — pulso, inbox, cargos e memória — sob o invariante único:
**o oikos não executa nada**; todo trabalho vira run normal do AETHER.

## Entradas
- Manifesto `aether.oikos/v1` validado + relógio injetável + quotas do tenant.

## Saídas
- `PulseTick` por disparo (status: `run_opened | missed | skipped`).
- `InboxItem` roteado (cargo + rota) ou escalado à cadeia/gate humano.
- Runs de ciclo abertos no pipeline mestre com orçamento debitado do oikos.

## Passos
1. `python3 scripts/oikos_engine.py validate --manifest <oikos.yaml>` —
   schema, organograma consistente (reports_to existentes, sem ciclos),
   rotas, teto de autonomia e políticas.
2. `python3 scripts/oikos_engine.py pulse-due --manifest <oikos.yaml> --now
   <ISO>` — ticks devidos calculados deterministicamente; cada tick abre um
   **run de ciclo** via `workflows/oikos_pulso_ciclo.yaml`.
3. Briefing do inbox: classificação de intake normal (Task 02) → roteamento
   pelo organograma (`oikos_engine.py route`) → cargo responsável.
4. Risco acima do `autonomy_ceiling` do cargo escala pela cadeia de
   subordinação; alto/crítico segue as regras gerais de aprovação.
5. Modo não assistido: prosseguir apenas com o que não depende de aprovação;
   pedidos vão ao canal do host com prazo e `on_expire`.
6. Memória: camada de oikos (curadoria MNÉME), de cargo (TTL) e de run
   (isolada) via `memory_engine.py` com escopos `oikos:<id>` / `cargo:<id>`.

## Critérios de aceite
- Nenhum efeito produzido fora de um run — trilha completa por construção.
- Ciclo perdido gera `PulseTick` com status e alerta, nunca silêncio.
- Limites de oikoi/ciclos simultâneos respeitados (Motor de Quotas).
- Ciclo de vida (`draft→active→paused→archived`) só transita por comando
  auditado; arquivar congela pulso/inbox e preserva a trilha.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
