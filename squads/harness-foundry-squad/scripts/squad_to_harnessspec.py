#!/usr/bin/env python3
"""Converte um squad.yaml do Squads-Genius em um HarnessSpec portável.

O HarnessSpec é o único contrato de troca deste squad com motores externos
de empacotamento (ex.: agent-harness-generator/metaharness). Nada do código
desses motores é importado ou copiado aqui.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def build_harnessspec(root: Path) -> dict:
    squad_yaml = root / "squad.yaml"
    if not squad_yaml.exists():
        raise FileNotFoundError(f"squad.yaml não encontrado em {root}")

    with squad_yaml.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    gaps: list[str] = []

    capabilities = []
    for agent in data.get("agents", []):
        persona_path = root / agent.get("file", "")
        if not persona_path.exists():
            gaps.append(f"persona ausente para agente '{agent.get('id')}'")
        capabilities.append(
            {
                "id": agent.get("id"),
                "description": agent.get("role", ""),
                "persona_file": agent.get("file"),
            }
        )

    commands = []
    for task in data.get("tasks", []):
        task_path = root / task.get("file", "")
        task_data = {}
        if task_path.exists():
            with task_path.open(encoding="utf-8") as fh:
                task_data = yaml.safe_load(fh) or {}
        else:
            gaps.append(f"arquivo de task ausente: '{task.get('file')}'")
        commands.append(
            {
                "id": task.get("id"),
                "owner": task.get("owner"),
                "inputs": task_data.get("inputs", []),
                "outputs": task_data.get("outputs", []),
            }
        )

    pipelines = []
    for workflow in data.get("workflows", []):
        pipelines.append({"id": workflow.get("id"), "file": workflow.get("file")})

    harnessspec = {
        "name": data.get("name", root.name),
        "commercial_name": data.get("commercial_name", data.get("name", root.name)),
        "version": data.get("version", "0.0.0"),
        "license": data.get("license", "MIT"),
        "required_footer": data.get("required_footer", ""),
        "capabilities": capabilities,
        "commands": commands,
        "pipelines": pipelines,
        "policy": {"default": "deny", "exceptions": []},
        "gaps": gaps,
        "source_squad_path": str(root),
    }
    return harnessspec


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--squad", required=True, help="Diretório do squad de origem")
    parser.add_argument("--out", required=True, help="Caminho do harnessspec.json de saída")
    args = parser.parse_args()

    spec = build_harnessspec(Path(args.squad))
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(spec, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
