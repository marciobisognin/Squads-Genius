#!/usr/bin/env python3
"""Gera o pacote de instalação Hermes (cli-config.yaml, optional-mcps, SKILL.md)
a partir de um harnessspec.json produzido por squad_to_harnessspec.py.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def generate(harnessspec_path: Path, out_dir: Path, exposure_level: str) -> None:
    spec = json.loads(harnessspec_path.read_text(encoding="utf-8"))
    name = spec["name"]

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "optional-mcps").mkdir(exist_ok=True)

    personalities = {
        cap["id"]: cap.get("description") or "Agente do harness"
        for cap in spec.get("capabilities", [])
    }
    cli_config = {
        "model": {"provider": "auto"},
        "agent": {"personalities": personalities},
    }
    (out_dir / "cli-config.yaml").write_text(
        yaml.safe_dump(cli_config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    if exposure_level == "npm":
        mcp_entry = {name: {"command": "npx", "args": ["-y", f"{name}@latest", "mcp", "start"]}}
    else:
        mcp_entry = {
            name: {
                "command": "python3",
                "args": ["scripts/run_squad.py"],
                "note": "Execução local; publique como pacote npm para habilitar 'npx'.",
            }
        }
    (out_dir / "optional-mcps" / f"{name}.json").write_text(
        json.dumps(mcp_entry, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    commands_md = "\n".join(
        f"- `{cmd['id']}` (owner: `{cmd['owner']}`) — inputs: {cmd['inputs']}, outputs: {cmd['outputs']}"
        for cmd in spec.get("commands", [])
    )
    skill_md = f"""# {spec.get("commercial_name", name)} (skill Hermes)

Harness gerado pelo Harness Foundry Squad a partir de `{spec.get("source_squad_path")}`.

## Instalação

```bash
cp -r {name} ~/.hermes/skills/{name}
```

## Comandos disponíveis

{commands_md or "Nenhum comando mapeado — revisar harnessspec.json."}

## Policy

Default-deny. Exceções: {spec.get("policy", {}).get("exceptions") or "nenhuma"}.

{spec.get("required_footer", "")}
"""
    (out_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harnessspec", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--exposure-level", choices=["local", "npm"], default="local")
    args = parser.parse_args()
    generate(Path(args.harnessspec), Path(args.out), args.exposure_level)
    print(f"Pacote Hermes gerado em {args.out}")


if __name__ == "__main__":
    main()
