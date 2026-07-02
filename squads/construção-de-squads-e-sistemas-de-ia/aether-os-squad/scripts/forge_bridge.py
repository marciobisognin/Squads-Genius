#!/usr/bin/env python3
"""Forja do AETHER OS: capability_gap -> briefing + scaffold de squad novo.

Gera, em workspace isolado, um squad candidato mínimo que passa na validação
estrutural do repositório (validate_squad.py): squad.yaml, README, LICENSE,
NOTICE, AUTHORS, agents/, tasks/, workflows/, scripts/, examples/, docs/.
Quando o construtor oficial (Maeve Genius Forge) estiver disponível, a
construção completa deve ser delegada a ele. PRD AETHER OS v1.2, Seção 20.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ENGINE_ID = "aether-forge-bridge@1.0.0"
FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "novo-squad"


def briefing_yaml(gap: dict, slug: str) -> str:
    capability = gap.get("capability", "capacidade não especificada")
    return f"""project_name: {gap.get('name', slug)}
objective: >
  Prover a capacidade '{capability}' identificada como capability_gap pelo
  Motor de Seleção do AETHER OS (run {gap.get('run_id', 'n/a')}).
problem: >
  {gap.get('problem', 'Nenhum squad existente passou nos gates para a tarefa.')}
target_audience: operadores do AETHER OS no Hermes Agent
expected_outputs:
  - squad candidato com contratos explícitos para '{capability}'
constraints:
  - workspace isolado; nunca o repositório produtivo
  - scripts primeiro em sandbox com dados sintéticos
  - revisão adversarial ELENCHUS antes de qualquer promoção
integrations: []
security_level: alto
human_approval_requirements: promoção e publicação exigem aprovação humana
success_metrics:
  - validate_squad.py retorna go
budget_limit: herdado do run pai (fração restritiva)
preferred_models: [local-first]
"""


def scaffold(gap: dict, workspace: Path) -> dict:
    slug = slugify(gap.get("name") or gap.get("capability", "novo-squad"))
    root = workspace / slug
    if root.exists():
        raise FileExistsError(f"workspace já contém {slug}")
    capability = gap.get("capability", "capability")
    for sub in ("agents", "tasks", "workflows", "scripts", "examples", "docs"):
        (root / sub).mkdir(parents=True)

    (root / "squad.yaml").write_text(f"""name: {gap.get('name', slug)}
code: {slug}
version: 0.1.0
language: pt-BR
license: MIT
creator: Marcio Bisognin
status: experimental
description: |
  Squad candidato forjado pelo AETHER OS para a capacidade '{capability}'
  (capability_gap). Uso controlado; promoção a trusted exige telemetria e gates.
capabilities:
- {capability}
agents:
- id: executor-principal
  file: agents/executor-principal.md
  role: Executa a capacidade '{capability}' sob contrato.
tasks:
- id: executar-capacidade
  file: tasks/executar-capacidade.md
  desc: Executa '{capability}' com critérios de aceite explícitos.
workflows:
- id: pipeline-principal
  file: workflows/pipeline-principal.yaml
  desc: Fluxo mínimo entrada -> execução -> validação -> entrega.
footer: '{FOOTER}'
""", encoding="utf-8")

    (root / "agents" / "executor-principal.md").write_text(
        f"""# Executor Principal — {capability}

## Missão
Executar a capacidade `{capability}` sob contrato explícito de entrada/saída,
com critérios de aceite verificáveis e falha tipada (aether.error/v1).

## Regras
1. Emitir somente JSON estruturado; números finais vêm de código determinístico.
2. Declarar permissões e efeitos externos antes de executar.
3. Falha segura: contrato inválido bloqueia a etapa.

---
{FOOTER}
""", encoding="utf-8")

    (root / "tasks" / "executar-capacidade.md").write_text(
        f"""# Task — Executar {capability}

## Objetivo
Executar `{capability}` e produzir artefato validável com hash.

## Critérios de aceite
- Saída valida no contrato declarado.
- Artefato registrado com sha256 e vínculo ao run.

---
{FOOTER}
""", encoding="utf-8")

    (root / "workflows" / "pipeline-principal.yaml").write_text(
        f"""schema_version: aether.workflow/v1
id: pipeline-principal
name: Pipeline Principal ({capability})
version: 0.1.0
stages:
  - id: s1
    task: tasks/executar-capacidade.md
    executor: executor-principal
exit_states: [completed, partial, failed]
# {FOOTER}
""", encoding="utf-8")

    (root / "scripts" / "validate_output.py").write_text(
        f'''#!/usr/bin/env python3
"""Validador determinístico de saída do squad {slug} (stdlib)."""
import json
import sys


def validate(payload: dict) -> dict:
    issues = []
    if "result" not in payload:
        issues.append("campo obrigatório ausente: result")
    return {{"valid": not issues, "issues": issues}}


if __name__ == "__main__":
    data = json.load(sys.stdin) if not sys.stdin.isatty() else {{}}
    print(json.dumps(validate(data), ensure_ascii=False))
    sys.exit(0)

# {FOOTER}
''', encoding="utf-8")

    (root / "examples" / "exemplo-entrada.json").write_text(
        canonical({"capability": capability, "input": "exemplo"}) + "\n",
        encoding="utf-8")
    (root / "docs" / "README-candidato.md").write_text(
        f"""# {gap.get('name', slug)} — candidato experimental

Forjado pelo AETHER OS a partir de capability_gap. Antes da promoção:
1. `validate_squad.py --root .` => go
2. Teste em sandbox com dados sintéticos
3. Revisão adversarial ELENCHUS
4. Aprovação humana (promotion-request.json)

---
{FOOTER}
""", encoding="utf-8")
    (root / "README.md").write_text(
        f"""# {gap.get('name', slug)}

Squad candidato (status: **experimental**) forjado pelo AETHER OS para a
capacidade `{capability}`. Ver `docs/README-candidato.md` para o fluxo de
promoção governada.

---
{FOOTER}
""", encoding="utf-8")
    (root / "LICENSE").write_text(
        "MIT License\n\nCopyright (c) 2026 Marcio Bisognin\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining "
        "a copy of this software and associated documentation files (the "
        "Software), to deal in the Software without restriction, subject to "
        "preserving this notice.\n\n" + FOOTER + "\n", encoding="utf-8")
    (root / "NOTICE.md").write_text(
        f"# NOTICE\n\nSquad candidato forjado pelo AETHER OS (capability_gap).\n\n{FOOTER}\n",
        encoding="utf-8")
    (root / "AUTHORS.md").write_text(
        f"# Autores\n\n- Marcio Bisognin — propriedade e curadoria.\n- AETHER OS — forja do candidato.\n\n{FOOTER}\n",
        encoding="utf-8")

    (root / "promotion-request.json").write_text(canonical({
        "schema_version": "aether.promotion-request/v1",
        "candidate": slug,
        "status": "experimental",
        "requires": ["validate_go", "sandbox_test", "adversarial_review",
                     "human_approval"],
        "forged_by": ENGINE_ID,
        "parent_run_id": gap.get("run_id", ""),
    }) + "\n", encoding="utf-8")

    return {"schema_version": "aether.forge-result/v1", "candidate": slug,
            "path": str(root), "status": "experimental",
            "next_steps": ["validate", "sandbox", "elenchus", "approval"],
            "forged_by": ENGINE_ID}


def main() -> int:
    ap = argparse.ArgumentParser(description="Forja AETHER (capability_gap)")
    ap.add_argument("--gap", required=True,
                    help="JSON com capability, name, problem, run_id")
    ap.add_argument("--workspace", required=True,
                    help="workspace isolado (nunca o repositório produtivo)")
    ap.add_argument("--briefing-only", action="store_true")
    args = ap.parse_args()
    gap = json.loads(Path(args.gap).read_text(encoding="utf-8"))
    workspace = Path(args.workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    slug = slugify(gap.get("name") or gap.get("capability", "novo-squad"))
    briefing_path = workspace / f"briefing_{slug}.yaml"
    briefing_path.write_text(briefing_yaml(gap, slug), encoding="utf-8")
    if args.briefing_only:
        print(canonical({"briefing": str(briefing_path)}))
        return 0
    result = scaffold(gap, workspace)
    result["briefing"] = str(briefing_path)
    print(canonical(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
