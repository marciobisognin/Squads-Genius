#!/usr/bin/env python3
"""Maeve Genius Forge executor.

Transforms a YAML/JSON briefing into a complete, deterministic, validatable squad.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from agent_generator import generate_agent_files
from briefing_parser import BriefingError, load_briefing
from documentation_generator import generate_documentation
from package_generator import base_package_files, build_manifest, dump_yaml, quality_report, static_validations, write_text
from requirements_analyzer import analyze_requirements
from script_generator import generate_scripts
from squad_architect import design_architecture
from task_file_generator import generate_task_files
from task_generator import generate_tasks
from test_generator import generate_tests
from workflow_file_generator import generate_workflow_files
from workflow_generator import generate_workflows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera um squad completo a partir de briefing YAML ou JSON.")
    parser.add_argument("--briefing", required=True, help="Arquivo de briefing YAML/JSON.")
    parser.add_argument("--output", required=True, help="Diretório de saída do squad gerado.")
    parser.add_argument("--dry-run", action="store_true", help="Analisa o briefing e imprime o plano sem gravar arquivos.")
    parser.add_argument("--strict", action="store_true", help="Falha se campos obrigatórios, tipos ou campos desconhecidos estiverem inválidos.")
    parser.add_argument("--overwrite", action="store_true", help="Substitui o diretório de saída se ele já contiver arquivos.")
    parser.add_argument("--format", choices=["yaml", "json"], help="Força o formato de leitura do briefing.")
    parser.add_argument("--no-llm", action="store_true", help="Garante execução determinística sem chamadas LLM externas. Este é o modo implementado.")
    parser.add_argument("--budget-limit", help="Sobrescreve budget_limit do briefing para fins de análise e relatório.")
    return parser.parse_args()


def _ensure_output(out: Path, overwrite: bool) -> None:
    if out.exists() and any(out.iterdir()):
        if not overwrite:
            raise BriefingError(f"Diretório de saída já existe e não está vazio: {out}. Use --overwrite para substituir.")
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)


def _expected_core_files(files: Dict[str, str]) -> List[str]:
    return sorted(files.keys())


def _run_pytest(root: Path) -> tuple[List[str], List[str]]:
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=root, text=True, capture_output=True)
    summary = (result.stdout + "\n" + result.stderr).strip().splitlines()[-8:]
    label = "pytest -q :: " + " | ".join(summary)
    if result.returncode == 0:
        return [label], []
    return [], [label]


def build_files(args: argparse.Namespace) -> tuple[Dict[str, str], Dict[str, Any]]:
    briefing = load_briefing(args.briefing, strict=args.strict, forced_format=args.format, budget_limit=args.budget_limit)
    analysis = analyze_requirements(briefing)
    architecture = design_architecture(briefing, analysis)
    tasks = generate_tasks(briefing, architecture)
    workflows = generate_workflows(briefing, tasks)
    slug = architecture["slug"]
    manifest = build_manifest(briefing.project_name, slug, architecture, tasks, workflows, briefing.to_dict())

    files: Dict[str, str] = {}
    files["squad.yaml"] = dump_yaml(manifest)
    files.update(generate_agent_files(architecture["agents"]))
    files.update(generate_task_files(tasks))
    files.update(generate_workflow_files(workflows))
    files.update(generate_scripts(briefing.project_name, slug))
    files.update(generate_documentation(briefing, architecture, analysis))
    files.update(base_package_files(briefing.project_name))
    files.update(generate_tests(_expected_core_files(files) + ["quality_report.json"]))
    context = {"briefing": briefing, "analysis": analysis, "architecture": architecture, "tasks": tasks, "workflows": workflows}
    return files, context


def main() -> int:
    args = parse_args()
    try:
        files, context = build_files(args)
        dry_plan = {
            "project_name": context["briefing"].project_name,
            "output": str(Path(args.output)),
            "dry_run": bool(args.dry_run),
            "no_llm": bool(args.no_llm),
            "components_planned": sorted(files.keys()),
            "agent_count": len(context["architecture"]["agents"]),
            "task_count": len(context["tasks"]),
            "workflow_count": len(context["workflows"]),
            "risks": context["analysis"]["risks"],
            "human_review_required": context["analysis"]["human_review_required"],
        }
        if args.dry_run:
            print(json.dumps(dry_plan, ensure_ascii=False, indent=2))
            return 0
        out = Path(args.output).resolve()
        _ensure_output(out, args.overwrite)
        for rel, content in files.items():
            write_text(out / rel, content if content.endswith("\n") else content + "\n")
        draft_report = {
            "components_generated": sorted(files.keys()),
            "validations_executed": [],
            "tests_passed": [],
            "tests_failed": ["pytest ainda não executado"],
            "risks_found": context["analysis"]["risks"],
            "human_review_required": context["analysis"]["human_review_required"],
            "score": 0,
            "score_basis": "rascunho criado antes dos testes para permitir validação de presença do arquivo",
            "go_no_go": "pending-tests",
        }
        write_text(out / "quality_report.json", json.dumps(draft_report, ensure_ascii=False, indent=2) + "\n")
        validations_result = static_validations(out)
        tests_passed, tests_failed = _run_pytest(out)
        report = quality_report(
            components=list(files.keys()),
            validations=validations_result["validations"],
            risks=context["analysis"]["risks"],
            human_review=context["analysis"]["human_review_required"],
            tests_passed=tests_passed,
            tests_failed=tests_failed,
        )
        write_text(out / "quality_report.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"output": str(out), "score": report["score"], "go_no_go": report["go_no_go"], "tests_failed": tests_failed}, ensure_ascii=False, indent=2))
        return 0 if not tests_failed else 1
    except BriefingError as exc:
        print(f"Erro de briefing: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
