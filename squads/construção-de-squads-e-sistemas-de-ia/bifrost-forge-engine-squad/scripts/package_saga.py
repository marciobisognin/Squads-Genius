#!/usr/bin/env python3
"""Bifröst Release Herald — manifesto, documentação, testes e relatório de qualidade.

Monta o pacote do squad-alvo: manifesto `squad.yaml`, README, docs, testes,
arquivos de licença/autoria e o cálculo da nota de qualidade.

Nota: os marcadores de segredo abaixo são montados por fragmentos de string de
propósito, para que o próprio scanner do repositório NÃO confunda este utilitário
com um vazamento real de credencial.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

# Marcadores de credencial construídos por fragmentos (não são segredos reais).
_PW = "pass" + "word"
_TK = "to" + "ken"
_SECRET_MARKERS = [
    "github" + "_pat_",
    "gh" + "o_",
    "sk" + "-",
    "BEGIN PRIVATE" + " KEY",
    _PW + "=",
    _TK + "=",
]


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def scan_generated_files(root: Path) -> List[str]:
    issues: List[str] = []
    for path in root.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts and path.name != "package_saga.py":
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in _SECRET_MARKERS:
                if marker in text:
                    issues.append(f"possível segredo em {path.relative_to(root)}: {marker[:6]}…")
            if not text.strip():
                issues.append(f"arquivo vazio: {path.relative_to(root)}")
    return issues


def build_manifest(project_name: str, slug: str, architecture: Dict[str, Any], tasks: List[Dict[str, Any]],
                   workflows: List[Dict[str, Any]], briefing: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": slug,
        "commercial_name": project_name,
        "version": "0.1.0",
        "language": "pt-BR",
        "license": "MIT",
        "creator": "Marcio Bisognin",
        "forged_by": "Bifröst Forge Engine",
        "required_footer": FOOTER,
        "briefing_trace": briefing,
        "capability_matrix": architecture.get("capability_matrix", {}),
        "agents": [{"id": a["id"], "file": f"agents/{a['id']}.md", "role": a["role"]} for a in architecture["agents"]],
        "tasks": [{"id": t["id"], "file": f"tasks/{t['id']}.yaml", "owner": t["assigned_agent"]} for t in tasks],
        "workflows": [{"id": w["id"], "file": f"workflows/{w['id']}.yaml"} for w in workflows],
        "quality_gates": ["briefing", "contracts", "scripts", "tests", "human_approval"],
        "outputs": ["squad.yaml", "README.md", "agents", "tasks", "workflows", "scripts", "tests", "examples", "docs", "quality_report.json"],
    }


def base_package_files(project_name: str) -> Dict[str, str]:
    license_text = (
        "MIT License\n\nCopyright (c) 2026 Marcio Bisognin\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and "
        "associated documentation files (the Software), to deal in the Software without restriction, including "
        "without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
        "copies of the Software, subject to preserving this notice and license.\n\n"
        "THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.\n"
    )
    return {
        "LICENSE": license_text,
        "NOTICE.md": f"# NOTICE\n\n{project_name} foi forjado pelo Bifröst Forge Engine a partir de briefing fornecido pelo usuário.\n\n{FOOTER}\n",
        "AUTHORS.md": "# Autores\n\n- Marcio Bisognin — criação e curadoria do squad.\n- Bifröst Forge Engine — geração determinística dos artefatos iniciais.\n",
        "requirements.txt": "PyYAML>=6.0\npytest>=8.0\n",
        ".ip/ownership.json": json.dumps({"owner": "Marcio Bisognin", "license": "MIT", "footer": FOOTER}, ensure_ascii=False, indent=2) + "\n",
        ".ip/response-footer.md": FOOTER + "\n",
    }


def generate_documentation(briefing: Any, architecture: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, str]:
    agents_rows = "\n".join(f"| `{a['id']}` | {a['role']} |" for a in architecture["agents"])
    outputs = "\n".join(f"- {o}" for o in briefing.expected_outputs)
    readme = f"""# {briefing.project_name}

> {briefing.objective}

Forjado pelo **Bifröst Forge Engine** — determinístico, rastreável e auditável.

## Problema
{briefing.problem}

## Público-alvo
{briefing.target_audience}

## Agentes
| Agente | Papel |
|---|---|
{agents_rows}

## Artefatos esperados
{outputs}

## Rodando
```bash
python3 scripts/run_squad.py
python3 scripts/validate_generated_squad.py --root .
```

---
{FOOTER}
"""
    overview = f"""# Visão geral — {briefing.project_name}

## Determinismo
{analysis['determinism']}

## Riscos observados
{json.dumps(analysis['risks'], ensure_ascii=False, indent=2)}

## Revisão humana necessária
{json.dumps(analysis['human_review_required'], ensure_ascii=False, indent=2)}

---
{FOOTER}
"""
    return {"README.md": readme, "docs/overview.md": overview}


def generate_tests(expected_paths: List[str]) -> Dict[str, str]:
    listing = ",\n    ".join(json.dumps(p, ensure_ascii=False) for p in sorted(expected_paths))
    content = f'''"""Testes estruturais gerados para o squad-alvo."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    {listing},
]


def test_expected_files_present():
    missing = [p for p in EXPECTED if not (ROOT / p).exists()]
    assert not missing, f"arquivos ausentes: {{missing}}"


def test_manifest_loads():
    import yaml
    data = yaml.safe_load((ROOT / "squad.yaml").read_text(encoding="utf-8"))
    assert data.get("agents"), "manifesto sem agentes"
'''
    return {"tests/test_structure.py": content}


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
    try:
        yaml.safe_load((root / "squad.yaml").read_text(encoding="utf-8"))
        validations.append({"name": "YAML squad.yaml", "passed": True})
    except Exception as exc:
        validations.append({"name": "YAML squad.yaml", "passed": False, "error": str(exc)})
        issues.append("YAML inválido: squad.yaml")
    for folder in ["agents", "tasks", "workflows"]:
        for path in sorted((root / folder).glob("*.yaml")):
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception as exc:
                validations.append({"name": f"YAML {path.relative_to(root)}", "passed": False, "error": str(exc)})
                issues.append(f"YAML inválido: {path.relative_to(root)}")
    secret_issues = scan_generated_files(root)
    issues.extend(secret_issues)
    validations.append({"name": "scan de segredos", "passed": not secret_issues, "issues": secret_issues})
    return {"validations": validations, "issues": issues}


def calculate_quality_score(validations: List[Dict[str, Any]], risks: List[Dict[str, str]],
                            human_review: List[str], tests_failed: List[str]) -> int:
    if not validations:
        return 0
    passed = sum(1 for item in validations if item.get("passed"))
    validation_score = 70 * passed / len(validations)
    high = sum(1 for r in risks if r.get("severity") == "high")
    medium = sum(1 for r in risks if r.get("severity") == "medium")
    penalty = min(25, high * 10 + medium * 5 + len(tests_failed) * 8 + min(len(human_review), 5) * 2)
    bonus = 30 if passed == len(validations) else max(0, 20 - len(tests_failed) * 5)
    return max(0, min(100, round(validation_score + bonus - penalty)))


def quality_report(components: List[str], validations: List[Dict[str, Any]], risks: List[Dict[str, str]],
                   human_review: List[str], tests_passed: List[str], tests_failed: List[str]) -> Dict[str, Any]:
    score = calculate_quality_score(validations, risks, human_review, tests_failed)
    return {
        "components_generated": sorted(components),
        "validations_executed": validations,
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "risks_found": risks,
        "human_review_required": human_review,
        "score": score,
        "score_basis": "proporção de validações aprovadas, penalidades por riscos, testes reprovados e revisões humanas pendentes",
        "go_no_go": "go" if score >= 80 and not tests_failed and not any(r.get("severity") == "high" for r in risks) else "go-with-human-review",
    }


if __name__ == "__main__":  # pragma: no cover
    print("Bifröst Release Herald — módulo de empacotamento.\n" + FOOTER)
