"""Utilidades de teste: caminhos e config temporária sobre o sample_vault."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SAMPLE_VAULT = ROOT / "examples" / "sample_vault"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def temp_config() -> dict:
    """Config apontando para o sample_vault com índice em diretório temporário."""
    index_dir = tempfile.mkdtemp(prefix="uoks_test_")
    return {
        "user_profile": {"language": "pt-BR"},
        "vault": {
            "path": str(SAMPLE_VAULT),
            "include_patterns": ["**/*.md"],
            "exclude_patterns": [".obsidian/**", "Private/**"],
        },
        "runtime": {"default_mode": "read_only", "index_dir": index_dir,
                    "allow_write": False, "agent_adapter": "generic"},
    }


def write_temp_config(data: dict) -> str:
    import json
    fd = tempfile.NamedTemporaryFile(
        prefix="uoks_cfg_", suffix=".json", delete=False, mode="w",
        encoding="utf-8")
    json.dump(data, fd)
    fd.close()
    return fd.name
