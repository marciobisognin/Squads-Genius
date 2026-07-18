#!/usr/bin/env python3
"""Validador estrutural e de segurança do Squad Contábil Adm Pública."""
from __future__ import annotations

import argparse
import json
import py_compile
import re
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REQUIRED_FILES = [
    "squad.yaml", "README.md", "PRD.md", "LICENSE", "NOTICE.md", "AUTHORS.md",
    "TEXTO_PUBLICACAO_REDES_BLOG.md", ".ip/ownership.json", ".ip/response-footer.md",
    "scripts/contabil_core.py", "scripts/validate_squad.py",
    "examples/caso_sem_restricao.json", "examples/caso_com_inconsistencias.json",
    "docs/base_normativa.md", "docs/limites_operacionais.md",
]
REQUIRED_DIRS = ["agents", "tasks", "workflows", "scripts", "tests", "examples", "docs", "schemas", "templates"]
SECRET_PATTERNS = [
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"gho_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
]


def validate(root: Path) -> dict:
    issues = []
    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.is_file() or path.stat().st_size == 0:
            issues.append(f"arquivo ausente ou vazio: {rel}")
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            issues.append(f"diretório ausente: {rel}")
    manifest_path = root / "squad.yaml"
    manifest = None
    if manifest_path.is_file():
        if yaml is None:
            issues.append("PyYAML indisponível para validar squad.yaml")
        else:
            try:
                manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            except Exception as exc:
                issues.append(f"squad.yaml inválido: {exc}")
    if isinstance(manifest, dict):
        for section in ("agents", "tasks", "workflows", "scripts"):
            items = manifest.get(section)
            if not isinstance(items, list) or not items:
                issues.append(f"manifesto sem lista não vazia: {section}")
                continue
            for item in items:
                rel = item.get("file") if isinstance(item, dict) else None
                if not rel or not (root / rel).is_file():
                    issues.append(f"referência inexistente em {section}: {rel}")
    for script in sorted((root / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(script), doraise=True)
        except Exception as exc:
            issues.append(f"Python inválido em {script.name}: {exc}")
    for path in root.rglob("*"):
        if not path.is_file() or any(part in {"__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".py", ".txt", ".csv"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                issues.append(f"possível segredo em {path.relative_to(root)}")
        if re.search(r"%[0-9A-Fa-f]{2}", text) or re.search(r"\\u[0-9A-Fa-f]{4}", text):
            issues.append(f"texto codificado indevidamente em {path.relative_to(root)}")
    return {
        "go_no_go": "go" if not issues else "no_go",
        "issues": issues,
        "required_files_checked": len(REQUIRED_FILES),
        "manifest_sections_checked": ["agents", "tasks", "workflows", "scripts"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    result = validate(Path(args.root).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["go_no_go"] == "go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
