#!/usr/bin/env python3
"""
Batch-fill LICENSE files in all squads that lack them.
Deterministic script with no external dependencies (stdlib only).
"""

import os
import sys
from pathlib import Path

LICENSE_CONTENT = """MIT License

Copyright (c) 2026 Marcio Bisognin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def fix_squad_licenses(repo_root: str = None) -> dict:
    """
    Add LICENSE file to all squads that lack it.

    Args:
        repo_root: Path to repository root. If None, uses current directory.

    Returns:
        dict with counts: added, skipped, failed
    """
    if repo_root is None:
        repo_root = os.getcwd()

    repo_path = Path(repo_root)
    stats = {"added": 0, "skipped": 0, "failed": 0}

    # Find all directories containing squad.yaml
    squad_dirs = []
    for squad_yaml in repo_path.rglob("squad.yaml"):
        squad_dirs.append(squad_yaml.parent)

    print(f"Found {len(squad_dirs)} squad directories (containing squad.yaml).")
    print()

    for squad_dir in sorted(squad_dirs):
        license_path = squad_dir / "LICENSE"
        squad_name = squad_dir.name

        if license_path.exists():
            print(f"✓ {squad_name} — LICENSE already exists")
            stats["skipped"] += 1
        else:
            try:
                license_path.write_text(LICENSE_CONTENT, encoding="utf-8")
                print(f"✅ {squad_name} — LICENSE added")
                stats["added"] += 1
            except Exception as e:
                print(f"❌ {squad_name} — FAILED: {e}")
                stats["failed"] += 1

    print()
    print("=" * 60)
    print(f"Summary: {stats['added']} added, {stats['skipped']} skipped, {stats['failed']} failed")
    print("=" * 60)

    return stats


if __name__ == "__main__":
    repo_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    fix_squad_licenses(repo_root)
