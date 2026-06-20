#!/usr/bin/env python3
"""Calcula um fit score determinístico para transformar um squad em harness.

Equivalente leve ao `metaharness score/analyze`, sem depender do motor
externo agent-harness-generator. Não inventa métricas: tudo que falta no
squad é registrado em `gaps` e penaliza o score correspondente.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

CREDENTIAL_HINTS = ("api_key", "apikey", "secret", "token", "password", "senha")


def _load_squad_yaml(root: Path) -> dict:
    squad_yaml = root / "squad.yaml"
    if not squad_yaml.exists():
        return {}
    with squad_yaml.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _scan_for_credentials(root: Path) -> list[str]:
    hits = []
    for path in root.rglob("*"):
        if path.is_dir() or path.name == "score_squad_fit.py":
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".zip"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        for hint in CREDENTIAL_HINTS:
            if f"{hint}=" in text or f'"{hint}"' in text or f"{hint}:" in text and "your-" not in text:
                hits.append(str(path.relative_to(root)))
                break
    return hits


def score_squad(root: Path) -> dict:
    data = _load_squad_yaml(root)
    gaps: list[str] = []
    constraints: list[str] = []

    agents = data.get("agents") or []
    tasks = data.get("tasks") or []
    workflows = data.get("workflows") or []

    if not data:
        constraints.append("squad.yaml ausente ou ilegível")

    # harness_fit: presença e completude de agentes/tasks/workflows
    harness_fit = 0
    if agents:
        harness_fit += 35
    else:
        gaps.append("nenhum agente declarado em squad.yaml")
    if tasks:
        harness_fit += 35
    else:
        gaps.append("nenhuma task declarada em squad.yaml")
    if workflows:
        harness_fit += 30
    else:
        gaps.append("nenhum workflow declarado em squad.yaml")

    # compile_confidence: scripts determinísticos vs. apenas prompts
    scripts_dir = root / "scripts"
    py_scripts = list(scripts_dir.glob("*.py")) if scripts_dir.exists() else []
    compile_confidence = min(100, 20 + 20 * len(py_scripts))
    if not py_scripts:
        gaps.append("sem scripts determinísticos em scripts/")

    # task_coverage: tasks com inputs/outputs/acceptance_criteria
    tasks_dir = root / "tasks"
    covered = 0
    total = 0
    if tasks_dir.exists():
        task_files = list(tasks_dir.glob("*.yaml"))
        total = len(task_files)
        for task_file in task_files:
            with task_file.open(encoding="utf-8") as fh:
                task_data = yaml.safe_load(fh) or {}
            if task_data.get("inputs") and task_data.get("outputs") and task_data.get("acceptance_criteria"):
                covered += 1
    task_coverage = round(100 * covered / total) if total else 0
    if total and covered < total:
        gaps.append(f"{total - covered} task(s) sem inputs/outputs/acceptance_criteria completos")

    # tool_safety: ausência de credenciais + footer obrigatório
    credential_hits = _scan_for_credentials(root)
    tool_safety = 100
    if credential_hits:
        tool_safety -= 60
        constraints.append(f"possíveis credenciais em: {', '.join(credential_hits)}")
    if not data.get("required_footer"):
        tool_safety -= 20
        gaps.append("required_footer ausente em squad.yaml")

    # memory_usefulness: outputs declarados reaproveitáveis
    outputs = data.get("outputs") or []
    memory_usefulness = min(100, 20 * len(outputs)) if outputs else 0
    if not outputs:
        gaps.append("squad.yaml não declara outputs reaproveitáveis")

    # custo estimado: heurística simples por nº de agentes/tasks (não é preço real)
    est_cost_per_run = round(0.01 * len(agents) + 0.005 * len(tasks), 4)

    harness_fit_total = round(
        0.35 * harness_fit
        + 0.20 * compile_confidence
        + 0.20 * task_coverage
        + 0.15 * tool_safety
        + 0.10 * memory_usefulness
    )

    if not (root / "LICENSE").exists():
        constraints.append("LICENSE ausente")
    if not (root / "README.md").exists():
        constraints.append("README.md ausente")

    if constraints:
        go_no_go = "no-go"
    elif harness_fit_total < 40:
        go_no_go = "no-go"
    elif harness_fit_total < 70:
        go_no_go = "go-with-human-review"
    else:
        go_no_go = "go"

    recommended_mode = "CLI local"
    if py_scripts and outputs:
        recommended_mode = "CLI + MCP"
    if (root / "package.json").exists():
        recommended_mode = "pacote npm"

    return {
        "squad": data.get("name", root.name),
        "harness_fit": harness_fit_total,
        "breakdown": {
            "harness_fit": harness_fit,
            "compile_confidence": compile_confidence,
            "task_coverage": task_coverage,
            "tool_safety": tool_safety,
            "memory_usefulness": memory_usefulness,
        },
        "est_cost_per_run_usd": est_cost_per_run,
        "recommended_mode": recommended_mode,
        "constraints": constraints,
        "gaps": gaps,
        "go_no_go": go_no_go,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Diretório do squad a avaliar")
    parser.add_argument("--out", help="Arquivo JSON de saída (default: stdout)")
    args = parser.parse_args()

    report = score_squad(Path(args.root))
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
