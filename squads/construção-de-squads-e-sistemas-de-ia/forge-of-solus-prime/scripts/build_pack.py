#!/usr/bin/env python3
"""BUMBLEBEE — empacotamento portável (estrato KÝKLOS → entrega).

Empacota uma run validada em um ZIP com manifesto neutro (RF-13/RF-14). O
manifesto descreve agentes, contratos SACP e LOOP de forma agnóstica a runtime:
qualquer runtime de agente compatível que leia o manifesto instala o squad.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forge_common import FOOTER, write_json  # noqa: E402


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def manifesto_neutro(raiz: Path) -> dict[str, Any]:
    """Gera um manifesto neutro a partir do conteúdo da run."""
    arquivos = sorted(
        p for p in raiz.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".zip"
    )
    return {
        "manifest_version": "neutral-1.0",
        "produced_by": "Forge of Solus Prime",
        "discipline": "FORJA",
        "estratos": ["telos", "logos", "organon", "kyklos", "mneme"],
        "files": [
            {"path": str(p.relative_to(raiz)), "sha256": _sha256(p), "bytes": p.stat().st_size}
            for p in arquivos
        ],
        "footer": FOOTER,
    }


def empacotar(raiz: Path, saida: Path) -> dict[str, Any]:
    """Escreve o manifesto e gera o ZIP da run."""
    raiz = raiz.resolve()
    manifesto = manifesto_neutro(raiz)
    write_json(raiz / "manifest.neutral.json", manifesto)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as zf:
        for entry in manifesto["files"] + [{"path": "manifest.neutral.json"}]:
            p = raiz / entry["path"]
            if p.exists():
                zf.write(p, arcname=entry["path"])
    return {
        "zip": str(saida),
        "files": len(manifesto["files"]),
        "manifest": "manifest.neutral.json",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="BUMBLEBEE — empacota a run em ZIP portável.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args(argv)
    resultado = empacotar(Path(args.root), Path(args.output))
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
