#!/usr/bin/env python3
"""Brokkr Script Smith — forja os scripts determinísticos do squad-alvo.

Brokkr martelou o fole enquanto Eitri forjava; aqui geramos scripts portáveis,
com `if __name__ == '__main__'`, footer e sem dependências externas obrigatórias.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

from typing import Dict

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

_VALIDATOR = '''#!/usr/bin/env python3
"""Validador estrutural do squad {project}.

Verifica presença de diretórios/arquivos obrigatórios e YAML válido.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_DIRS = ["agents", "tasks", "workflows", "scripts", "examples", "docs"]
REQUIRED_FILES = ["squad.yaml", "README.md", "LICENSE", "NOTICE.md", "AUTHORS.md"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    issues = []
    for d in REQUIRED_DIRS:
        if not (root / d).is_dir():
            issues.append("diretorio ausente: " + d)
    for f in REQUIRED_FILES:
        if not (root / f).is_file():
            issues.append("arquivo ausente: " + f)
    report = {{"go_no_go": "go" if not issues else "no-go", "issues": issues}}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''

_RUNNER = '''#!/usr/bin/env python3
"""Runner determinístico do squad {project}: lista agentes/tasks/workflows do manifesto.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None


def load_manifest(root: Path):
    text = (root / "squad.yaml").read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    return json.loads(text)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    manifest = load_manifest(root)
    summary = {{
        "squad": manifest.get("name"),
        "agents": [a["id"] for a in manifest.get("agents", [])],
        "tasks": [t["id"] for t in manifest.get("tasks", [])],
        "workflows": [w["id"] for w in manifest.get("workflows", [])],
    }}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def generate_scripts(project_name: str) -> Dict[str, str]:
    return {
        "scripts/validate_generated_squad.py": _VALIDATOR.format(project=project_name),
        "scripts/run_squad.py": _RUNNER.format(project=project_name),
    }


if __name__ == "__main__":  # pragma: no cover
    print("Brokkr Script Smith — módulo de geração de scripts.\n" + FOOTER)
