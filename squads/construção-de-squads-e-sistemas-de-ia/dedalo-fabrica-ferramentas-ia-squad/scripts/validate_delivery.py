#!/usr/bin/env python3
"""Validador determinístico de entrega (NÓMOS/SYNTHÉTES) do DÉDALO.

Checa a presença e a consistência mínima dos artefatos finais antes do export, espelhando
os critérios de aceite do PRD. Sem LLM: apenas verificações de arquivo e sanidade.

Uso:
    python3 scripts/validate_delivery.py --root output
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_PRD_ARTIFACTS = ["sources.md", "opportunity_map.yaml", "prd.md", "validation_report.md"]
EXPECTED_MVP_ARTIFACTS = ["architecture.md", "backlog.md", "squad.yaml"]


def validate(root: Path, require_mvp: bool) -> dict:
    issues: list[str] = []
    expected = list(EXPECTED_PRD_ARTIFACTS)
    if require_mvp:
        expected += EXPECTED_MVP_ARTIFACTS
    for name in expected:
        path = root / name
        if not path.is_file():
            issues.append(f"artefato ausente: {name}")
        elif path.stat().st_size == 0:
            issues.append(f"artefato vazio: {name}")
    go_no_go = "go" if not issues else "no_go"
    return {
        "root": str(root),
        "require_mvp": require_mvp,
        "expected": expected,
        "issues": issues,
        "go_no_go": go_no_go,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Valida a presença/consistência dos artefatos de entrega.")
    ap.add_argument("--root", default="output", help="Diretório com os artefatos de entrega.")
    ap.add_argument("--require-mvp", action="store_true", help="Exige também os artefatos do MVP (fase 2/3).")
    args = ap.parse_args()
    report = validate(Path(args.root), args.require_mvp)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["go_no_go"] == "go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
