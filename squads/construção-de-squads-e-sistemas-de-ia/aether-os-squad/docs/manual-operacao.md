# Manual de Operação

## Primeiros dez minutos (PRD §27.5)

```bash
cd squads/construção-de-squads-e-sistemas-de-ia/aether-os-squad
python3 scripts/aether_cli.py doctor        # diagnóstico com correções acionáveis
python3 scripts/aether_cli.py init          # workspace idempotente, offline
python3 scripts/aether_cli.py demo          # run guiado narrando cada decisão
```

## Operação por motor

```bash
# Descoberta e busca de capacidades
python3 scripts/registry_indexer.py discover --root <roots> --output registry.json
python3 scripts/registry_indexer.py search --registry registry.json --query "<termo>"

# Seleção determinística (breakdown auditável)
python3 scripts/selection_engine.py --request <selection_request.json>

# Risco e política de aprovação
python3 scripts/risk_engine.py --action <action.json>

# Despacho de tarefas prontas
python3 scripts/dispatch_engine.py --tasks <tasks.json>

# Orçamento e quotas
python3 scripts/budget_engine.py --ledger <ledger.json> [--charge 0.35]
python3 scripts/quota_engine.py --resource concurrent_tasks --current 3

# Falhas tipadas
python3 scripts/error_policy_engine.py --failure <failure.json>

# Handoffs SACP (+ dead-letter)
python3 scripts/sacp_validator.py --envelope <handoff.json> --payload <arquivo>

# Loop de revisão até a entrega
python3 scripts/run_loop.py review --task <task.json> [--max-attempts 3]

# Replay determinístico (auditoria)
python3 scripts/replay_engine.py --engine selection --input <req.json> --output <decisao.json>

# Autoaprendizado
python3 scripts/memory_engine.py --store memory/lessons.jsonl extract --run <run.json>
python3 scripts/memory_engine.py --store memory/lessons.jsonl add --lesson <lesson.json>
python3 scripts/memory_engine.py --store memory/lessons.jsonl promote --lesson-id <id> --approver <quem>
python3 scripts/memory_engine.py --store memory/lessons.jsonl expire
python3 scripts/memory_engine.py --store memory/lessons.jsonl query --scope <capability>

# Forja (capability_gap -> squad novo)
python3 scripts/forge_bridge.py --gap <gap.json> --workspace <workspace-isolado>
```

## Runbooks mínimos

| Alerta | Reação |
|---|---|
| `compensation_failed` | Incidente: intervenção humana imediata; nunca fingir que reverteu |
| Divergência de replay (exit 8) | Incidente crítico: código/config/dado adulterado; congelar motor e auditar |
| Dead-letter crescendo | Contrato quebrado ou ataque: triar itens, corrigir causa, reprocessar auditado |
| `injection_suspected` | Quarentena do conteúdo + revisão humana; nunca reprocessar sem correção |
| `budget_exceeded` | Pausar tarefas custosas; decisão humana para elevar teto |
| Aprovações expirando | Executar `on_expire` declarado; revisar telemetria antifadiga |

## O que este squad NÃO faz sem gate humano

- Efeito externo de risco alto/crítico (aprovação com prazo e quórum).
- Promoção de lição a `approved_rule`.
- Promoção de squad forjado a `trusted` e publicação.
- Planejamento sob regime caótico/indefinido.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
