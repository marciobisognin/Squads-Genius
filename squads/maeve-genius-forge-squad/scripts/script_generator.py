"""Generate deterministic Python scripts for the produced squad."""
from __future__ import annotations

from typing import Dict


def generate_scripts(project_name: str, slug: str) -> Dict[str, str]:
    run_script = f'''#!/usr/bin/env python3
"""Executor determinístico do squad {project_name}."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Executa o squad gerado em modo determinístico.")
    parser.add_argument("--input", required=True, help="Arquivo JSON de entrada operacional.")
    parser.add_argument("--output", required=True, help="Arquivo JSON de saída.")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.is_file():
        raise SystemExit(f"Entrada não encontrada: {{input_path}}")
    data = json.loads(input_path.read_text(encoding="utf-8"))
    result = {{
        "project": {project_name!r},
        "status": "processed",
        "observed_input_keys": sorted(data.keys()),
        "requires_human_review": data.get("requires_human_review", False),
    }}
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
    validate_script = '''#!/usr/bin/env python3
"""Valida a estrutura mínima do squad gerado."""
from __future__ import annotations

import argparse
import json
import py_compile
from pathlib import Path

import yaml

REQUIRED_FILES = ["squad.yaml", "README.md", "LICENSE", "NOTICE.md", "AUTHORS.md", "requirements.txt", "quality_report.json"]
REQUIRED_DIRS = ["agents", "tasks", "workflows", "scripts", "tests", "examples", "docs"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida arquivos, YAML e scripts Python do squad gerado.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    issues = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            issues.append(f"arquivo ausente: {rel}")
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            issues.append(f"diretório ausente: {rel}")
    for rel in ["squad.yaml"]:
        try:
            yaml.safe_load((root / rel).read_text(encoding="utf-8"))
        except Exception as exc:
            issues.append(f"YAML inválido em {rel}: {exc}")
    for folder in ["agents", "tasks", "workflows"]:
        for path in (root / folder).glob("*.yaml"):
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception as exc:
                issues.append(f"YAML inválido em {path.relative_to(root)}: {exc}")
    for path in (root / "scripts").glob("*.py"):
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            issues.append(f"script inválido em {path.relative_to(root)}: {exc}")
    print(json.dumps({"ok": not issues, "issues": issues}, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''
    return {"scripts/run_squad.py": run_script, "scripts/validate_generated_squad.py": validate_script}
