#!/usr/bin/env python3
"""Diagnóstico final de um harness gerado: HEALTHY, WARN ou BLOCKED."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_FILES = ["cli-config.yaml", "optional-mcps", "SKILL.md"]


def run_doctor(hermes_dir: Path) -> dict:
    warnings = []
    blockers = []

    for required in REQUIRED_FILES:
        if not (hermes_dir / required).exists():
            blockers.append(f"arquivo/diretório obrigatório ausente: {required}")

    plugin_manifest = hermes_dir.parent / ".claude-plugin" / "plugin.json"
    if not plugin_manifest.exists():
        warnings.append("WARN .claude-plugin/plugin.json absent")

    mcp_dir = hermes_dir / "optional-mcps"
    if mcp_dir.exists() and not list(mcp_dir.glob("*.json")):
        warnings.append("WARN optional-mcps/ existe mas está vazio")

    if blockers:
        status = "BLOCKED"
    elif warnings:
        status = "WARN"
    else:
        status = "HEALTHY"

    return {"status": status, "blockers": blockers, "warnings": warnings}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hermes-dir", required=True, help="Diretório do pacote Hermes gerado")
    parser.add_argument("--out", help="Arquivo JSON de saída (default: stdout)")
    args = parser.parse_args()

    report = run_doctor(Path(args.hermes_dir))
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
