# Manual operacional — Forge of Solus Prime

## Pré-requisitos
- Python **3.11+**. Em modo L1 *report-only*, **nenhuma dependência externa** é
  obrigatória (a stdlib basta). Para o conjunto completo: `pip install -r requirements.txt`.

## Travessia completa (Definition of Done)
A partir de `squads/forge-of-solus-prime/`:

```bash
python3 scripts/forge.py plan     --briefing examples/briefing_exemplo.yaml
python3 scripts/forge.py init     --briefing examples/briefing_exemplo.yaml --out runs/demo --mode L1
python3 scripts/cynefin_gate.py   --briefing examples/briefing_exemplo.yaml --out runs/demo/cynefin.json
python3 scripts/discover_tools.py --briefing examples/briefing_exemplo.yaml --out runs/demo/tool_candidates.json
python3 scripts/evaluate_tool.py  --candidates runs/demo/tool_candidates.json --out runs/demo/tool_evaluation.json
python3 scripts/token_budget.py   --run runs/demo/run_state.json --out runs/demo/token_budget.json
python3 scripts/validate_squad.py --root runs/demo
python3 scripts/build_pack.py     --root runs/demo --output runs/demo/pack.zip
python3 -m pytest -q
```

Artefatos exigidos (não vazios) em `runs/demo/`: `briefing.normalizado.yaml`,
`cynefin.json`, `grafo_requisitos.json`, `squad.yaml`, `AGENTS.md`, `LOOP.md`,
`CONVENTIONS.md`, `run_state.json`, `token_budget.json`, `evidence.md`,
`tool_evaluation.json`, `quality_report.json`.

## Subcomandos do `forge.py`
| Comando | Atos cobertos | O que faz |
|---|---|---|
| `plan` | NÓESIS + BOULḖ + DIAÍRESIS | Deriva rota e grafo de 3–7 tarefas, sem PRÂXIS |
| `init` | Cinco estratos (L1) | Gera a run completa e auditável |
| `validate` | KÝKLOS | Roda os gates dos 5 estratos + 6 patologias |

## Modos de operação
- **Modo 0 — Blueprint** (`apenas_pesquisa.yaml`): só pesquisa + arquitetura.
- **Modo 1 — Forja determinística** (`forja_deterministica.yaml`): templates, sem LLM.
- **Modo 2 — Forja assistida por pesquisa**: descobre e avalia instrumentos.
- **Modo 3 — Anel assistido (L2)** (`execucao_assistida.yaml`): commit local, sem push.
- **Modo 4 — Multiagente controlado**: agentes paralelos + juízo adversarial.
- **Modo 5 — Unattended limitado (L3)**: só baixo risco, allowlist, rollback.

## Regras de segurança (inegociáveis)
- L1 é o padrão; subir de nível exige aprovação humana registrada.
- Sem rede/credenciais sem gate HITL; risco alto nunca incorpora automaticamente.
- Nenhuma publicação/push sem autorização explícita.

> Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
