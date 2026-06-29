#!/usr/bin/env python3
"""Cria o perfil/configuração do usuário para o squad.

Gera config/user.config.yaml (ou .json se PyYAML ausente) a partir de flags,
sem assumir caminho fixo. Modo padrão read_only e escrita bloqueada.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import obsidian_core as core

VALID_MODES = {"read_only", "suggest", "draft_patch", "write", "curate"}


def build_profile(vault: str, language: str, adapter: str,
                  mode: str) -> dict:
    if mode not in VALID_MODES:
        raise ValueError(f"Modo inválido: {mode}. Use {sorted(VALID_MODES)}")
    return {
        "user_profile": {
            "display_name": "Usuário",
            "language": language,
            "preferred_style": "claro, técnico e objetivo",
            "private_mode": True,
        },
        "vault": {
            "path": vault,
            "include_patterns": ["**/*.md"],
            "exclude_patterns": [
                ".obsidian/**", "Templates/**", "Private/**", "Anexos/**",
            ],
            "max_file_size_mb": 5,
            "parse_frontmatter": True,
            "parse_wikilinks": True,
            "parse_tags": True,
        },
        "runtime": {
            "default_mode": mode,
            "citation_required": True,
            "allow_write": mode in {"write", "curate"},
            "agent_adapter": adapter,
        },
    }


def write_profile(profile: dict, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    if core.yaml is not None:
        target = out_dir / "user.config.yaml"
        target.write_text(
            core.yaml.safe_dump(profile, allow_unicode=True, sort_keys=False),
            encoding="utf-8")
    else:
        target = out_dir / "user.config.json"
        target.write_text(
            json.dumps(profile, ensure_ascii=False, indent=2),
            encoding="utf-8")
    return target


def main() -> int:
    ap = argparse.ArgumentParser(description="Cria perfil do usuário.")
    ap.add_argument("--vault", required=True)
    ap.add_argument("--language", default="pt-BR")
    ap.add_argument("--adapter", default="generic")
    ap.add_argument("--mode", default="read_only")
    ap.add_argument("--config-dir", default="config")
    args = ap.parse_args()
    try:
        profile = build_profile(args.vault, args.language, args.adapter,
                                args.mode)
        target = write_profile(profile, Path(args.config_dir))
    except Exception as exc:  # noqa: BLE001
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"config_written": str(target),
                      "mode": args.mode, "adapter": args.adapter},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
