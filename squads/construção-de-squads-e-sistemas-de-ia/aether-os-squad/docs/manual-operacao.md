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

# Oikos — organizações persistentes (PRD v1.3)
python3 scripts/oikos_engine.py validate --manifest <oikos.yaml>
python3 scripts/oikos_engine.py pulse-due --manifest <oikos.yaml> --now <ISO>
python3 scripts/oikos_engine.py route --manifest <oikos.yaml> --item <inbox_item.json>
python3 scripts/oikos_engine.py autonomy --manifest <oikos.yaml> --position <cargo> --tier <tier>
python3 scripts/oikos_engine.py transition --state active --to paused

# Prósopon — personas com salvaguardas (PRD v1.3)
python3 scripts/persona_engine.py validate --prosopon <prosopon.json>
python3 scripts/persona_engine.py label-check --artifact <arquivo> --persona <id>
python3 scripts/persona_engine.py gallery-add --prosopon <prosopon.json>
python3 scripts/persona_engine.py gallery-retire --persona <id> --reason "<motivo>"

# Host e economia de tokens (PRD v1.3)
python3 scripts/host_adapter.py validate --adapter <host.json>
python3 scripts/host_adapter.py capabilities --adapter <host.json>
python3 scripts/token_economy.py derive --request <derivation_request.json>
python3 scripts/token_economy.py envelope-check --payload <arquivo>
python3 scripts/replay_engine.py --engine derivation --input <req.json> --output <decisao.json>
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
| Ciclo de oikos perdido (`PulseTick: missed`) | Verificar host/quota/disjuntor; ciclo perdido nunca se acumula em silêncio |
| Egressão de persona bloqueada (exit 10) | Rótulo ausente ou personificação: corrigir artefato; personificação é evento de segurança |
| Divergência de neutralidade (economia) | Alavanca alterou decisão: quebra de invariante; desligar alavanca e auditar |

## O que este squad NÃO faz sem gate humano

- Efeito externo de risco alto/crítico (aprovação com prazo e quórum).
- Promoção de lição a `approved_rule`.
- Promoção de squad forjado a `trusted` e publicação.
- Planejamento sob regime caótico/indefinido.
- Publicação de prósopon na Galeria (revisão humana obrigatória).
- Risco acima do teto de autonomia de um cargo de oikos (escala a cadeia).
- Modo não assistido fora dos níveis declarados em `unattended_allowed`.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
