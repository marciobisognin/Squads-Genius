"""Package assembly and quality report calculation for generated squads."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."
SECRET_MARKERS = ["github_pat_", "gho_", "sk-", "BEGIN PRIVATE KEY", "password=", "token="]


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def scan_generated_files(root: Path) -> List[str]:
    issues: List[str] = []
    for path in root.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in SECRET_MARKERS:
                if marker in text and path.name not in {"validate_generated_squad.py"}:
                    issues.append(f"possível segredo em {path.relative_to(root)}: {marker}")
            if not text.strip():
                issues.append(f"arquivo vazio: {path.relative_to(root)}")
    return issues


def build_manifest(project_name: str, slug: str, architecture: Dict[str, Any], tasks: List[Dict[str, Any]], workflows: List[Dict[str, Any]], briefing: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": slug,
        "commercial_name": project_name,
        "version": "0.1.0",
        "language": "pt-BR",
        "license": "MIT",
        "creator": "Marcio Bisognin",
        "required_footer": FOOTER,
        "briefing_trace": briefing,
        "agents": [{"id": agent["id"], "file": f"agents/{agent['id']}.yaml", "role": agent["role"]} for agent in architecture["agents"]],
        "tasks": [{"id": task["id"], "file": f"tasks/{task['id']}.yaml", "owner": task["assigned_agent"]} for task in tasks],
        "workflows": [{"id": wf["id"], "file": f"workflows/{wf['id']}.yaml"} for wf in workflows],
        "quality_gates": ["briefing", "contracts", "scripts", "tests", "human_approval"],
        "outputs": ["squad.yaml", "README.md", "agents", "tasks", "workflows", "scripts", "tests", "examples", "docs", "quality_report.json"],
    }


def static_validations(root: Path) -> Dict[str, Any]:
    required_files = ["squad.yaml", "README.md", "LICENSE", "NOTICE.md", "AUTHORS.md", "requirements.txt", "quality_report.json"]
    required_dirs = ["agents", "tasks", "workflows", "scripts", "tests", "examples", "docs"]
    issues: List[str] = []
    validations: List[Dict[str, Any]] = []
    for rel in required_dirs:
        ok = (root / rel).is_dir()
        validations.append({"name": f"diretório {rel}", "passed": ok})
        if not ok:
            issues.append(f"diretório ausente: {rel}")
    for rel in required_files:
        ok = (root / rel).is_file()
        validations.append({"name": f"arquivo {rel}", "passed": ok})
        if not ok:
            issues.append(f"arquivo ausente: {rel}")
    for rel in ["squad.yaml"]:
        try:
            yaml.safe_load((root / rel).read_text(encoding="utf-8"))
            validations.append({"name": f"YAML {rel}", "passed": True})
        except Exception as exc:
            validations.append({"name": f"YAML {rel}", "passed": False, "error": str(exc)})
            issues.append(f"YAML inválido: {rel}")
    for folder in ["agents", "tasks", "workflows"]:
        for path in (root / folder).glob("*.yaml"):
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
                validations.append({"name": f"YAML {path.relative_to(root)}", "passed": True})
            except Exception as exc:
                validations.append({"name": f"YAML {path.relative_to(root)}", "passed": False, "error": str(exc)})
                issues.append(f"YAML inválido: {path.relative_to(root)}")
    secret_issues = scan_generated_files(root)
    issues.extend(secret_issues)
    validations.append({"name": "scan de segredos", "passed": not secret_issues, "issues": secret_issues})
    return {"validations": validations, "issues": issues}


def calculate_quality_score(validations: List[Dict[str, Any]], risks: List[Dict[str, str]], human_review: List[str], tests_failed: List[str]) -> int:
    if not validations:
        return 0
    passed = sum(1 for item in validations if item.get("passed"))
    validation_score = 70 * passed / len(validations)
    high_risks = sum(1 for risk in risks if risk.get("severity") == "high")
    medium_risks = sum(1 for risk in risks if risk.get("severity") == "medium")
    risk_penalty = min(25, high_risks * 10 + medium_risks * 5 + len(tests_failed) * 8 + min(len(human_review), 5) * 2)
    completeness_bonus = 30 if passed == len(validations) else max(0, 20 - len(tests_failed) * 5)
    return max(0, min(100, round(validation_score + completeness_bonus - risk_penalty)))


def base_package_files(project_name: str) -> Dict[str, str]:
    return {
        "LICENSE": "MIT License\n\nCopyright (c) 2026 Marcio Bisognin\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the Software), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to preserving this notice and license.\n\nTHE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.\n",
        "NOTICE.md": f"# NOTICE\n\n{project_name} foi gerado pelo Maeve Genius Forge a partir de briefing fornecido pelo usuário.\n\n{FOOTER}\n",
        "AUTHORS.md": "# Autores\n\n- Marcio Bisognin — criação e curadoria do squad.\n- Maeve Genius Forge — geração determinística dos artefatos iniciais.\n",
        "requirements.txt": "PyYAML>=6.0\npytest>=8.0\n",
        ".ip/ownership.json": json.dumps({"owner": "Marcio Bisognin", "license": "MIT", "footer": FOOTER}, ensure_ascii=False, indent=2),
        ".ip/response-footer.md": FOOTER + "\n",
    }


def quality_report(components: List[str], validations: List[Dict[str, Any]], risks: List[Dict[str, str]], human_review: List[str], tests_passed: List[str], tests_failed: List[str]) -> Dict[str, Any]:
    score = calculate_quality_score(validations, risks, human_review, tests_failed)
    return {
        "components_generated": sorted(components),
        "validations_executed": validations,
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "risks_found": risks,
        "human_review_required": human_review,
        "score": score,
        "score_basis": "score calculado por proporção de validações aprovadas, penalidades por riscos, testes reprovados e revisões humanas pendentes",
        "go_no_go": "go" if score >= 80 and not tests_failed and not any(r.get("severity") == "high" for r in risks) else "go-with-human-review",
    }
