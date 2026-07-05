# Manual de operação — Bifröst Forge Engine

## Pré-requisitos
- Python 3.11+
- `pip install -r requirements.txt` (PyYAML, pytest) — opcionais, mas recomendados.

## Fluxo básico: forjar um squad
```bash
cd squads/construção-de-squads-e-sistemas-de-ia/bifrost-forge-engine-squad

# 1) planejar (sem gravar)
python3 scripts/bifrost_forge.py --briefing examples/briefing_valhalla_knowledge.yaml --output /tmp/out --dry-run

# 2) forjar de verdade, provando determinismo
python3 scripts/bifrost_forge.py --briefing examples/briefing_valhalla_knowledge.yaml --output /tmp/out --overwrite --verify-determinism

# 3) validar com Heimdall (rastreabilidade + gates)
python3 scripts/heimdall_validate.py --root /tmp/out --briefing examples/briefing_valhalla_knowledge.yaml --format md
```

## Auditoria (Saga Ledger)
Cada forja grava `/<output>/.saga/saga_ledger.jsonl`. Verifique a integridade:
```bash
python3 scripts/saga_ledger.py --verify /tmp/out/.saga/saga_ledger.jsonl
```

## Registro vivo (Yggdrasil)
```bash
# rotear uma necessidade para squads existentes
python3 scripts/yggdrasil_registry.py --squads-root ../.. --route "carrossel instagram"
# checar duplicidade antes de forjar
python3 scripts/yggdrasil_registry.py --squads-root ../.. --check-duplicate "Meu Novo Squad"
```

## DNA de persona (opcional, com salvaguardas de PI)
```bash
python3 scripts/mimir_dna.py --input material_publico.txt --output dna.yaml
```

## Flags úteis do `bifrost_forge.py`
| Flag | Efeito |
|---|---|
| `--dry-run` | Planeja sem gravar. |
| `--strict` | Falha em campos ausentes/desconhecidos. |
| `--overwrite` | Substitui a saída existente. |
| `--no-llm` | Execução determinística (modo implementado). |
| `--resume` | Retoma de checkpoint. |
| `--verify-determinism` | Forja 2× e compara o hash da árvore. |

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
