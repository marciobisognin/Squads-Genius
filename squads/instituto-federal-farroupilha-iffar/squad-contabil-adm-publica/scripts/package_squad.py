#!/usr/bin/env python3
"""Empacota o squad em ZIP reprodutível e verifica a integridade."""
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

EXCLUDE_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv"}


def build(root: Path, output: Path) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    files = [p for p in root.rglob("*") if p.is_file() and not any(part in EXCLUDE_PARTS for part in p.parts)]
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, Path(root.name) / path.relative_to(root))
    with zipfile.ZipFile(output) as archive:
        bad = archive.testzip()
        names = set(archive.namelist())
    required = {f"{root.name}/README.md", f"{root.name}/PRD.md", f"{root.name}/squad.yaml"}
    return {"zip": str(output.resolve()), "files": len(files), "bad_member": bad, "required_present": required.issubset(names)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = build(Path(args.root).resolve(), Path(args.output).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["bad_member"] is None and result["required_present"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
