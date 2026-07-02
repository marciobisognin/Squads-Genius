# Demo — Run guiado de ponta a ponta (offline, local-first)

Executa descoberta → seleção → risco → despacho → decision-replay, narrando
cada decisão determinística. Nenhuma chamada a modelo; nenhum acesso a rede.

## 1. Diagnóstico e workspace

```bash
cd squads/construção-de-squads-e-sistemas-de-ia/aether-os-squad
python3 scripts/aether_cli.py doctor
python3 scripts/aether_cli.py init --workspace workspace
```

## 2. Run guiado

```bash
python3 scripts/aether_cli.py demo
```

Saída esperada (resumo): seleção escolhe `squad:beta@1.0.0/task:analisar`
(o candidato `discovered` é eliminado no gate `trust_state`); risco `low`
com política `auto`; despacho enfileira `t1` e bloqueia `t2`
(`approval_pending`); decision-replay `pass` — byte a byte.

## 3. Descoberta real de squads do repositório

```bash
python3 scripts/registry_indexer.py discover --root ../../../squads --output workspace/registry.json
python3 scripts/registry_indexer.py search --registry workspace/registry.json --query "construcao_de_squads"
```

## 4. Seleção determinística com breakdown auditável

```bash
python3 scripts/selection_engine.py --request examples/selection_request.json
```

## 5. capability_gap → Forja de um squad novo

```bash
echo '{"capability": "video-subtitle-sync", "name": "Squad Legendas", "run_id": "run_x"}' > /tmp/gap.json
python3 scripts/forge_bridge.py --gap /tmp/gap.json --workspace workspace/forge
python3 ../maeve-genius-forge-squad/scripts/validate_squad.py --root workspace/forge/squad-legendas
```

## 6. Autoaprendizado (lições com proveniência e TTL)

```bash
python3 scripts/memory_engine.py --store workspace/memory/lessons.jsonl extract --run examples/run_aprovado.json > /tmp/lesson.json
python3 scripts/memory_engine.py --store workspace/memory/lessons.jsonl add --lesson /tmp/lesson.json
python3 scripts/memory_engine.py --store workspace/memory/lessons.jsonl query --scope pdf-ocr-analysis
```

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
