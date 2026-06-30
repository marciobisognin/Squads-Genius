#!/usr/bin/env python3
"""
Ensure all squad directories have required structure (agents/, tasks/, workflows/).
Creates empty .gitkeep files to preserve directory structure in git.
"""

import os
import sys
from pathlib import Path

REQUIRED_DIRS = ["agents", "tasks", "workflows"]


def fix_squad_structure(repo_root: str = None) -> dict:
    """
    Ensure all squads have required directory structure.

    Args:
        repo_root: Path to repository root. If None, uses current directory.

    Returns:
        dict with counts: fixed, already_ok, failed
    """
    if repo_root is None:
        repo_root = os.getcwd()

    repo_path = Path(repo_root)
    stats = {"fixed": 0, "already_ok": 0, "failed": 0}

    # Find all directories containing squad.yaml
    squad_dirs = []
    for squad_yaml in repo_path.rglob("squad.yaml"):
        squad_dirs.append(squad_yaml.parent)

    print(f"Found {len(squad_dirs)} squad directories.")
    print()

    for squad_dir in sorted(squad_dirs):
        squad_name = squad_dir.name
        missing_dirs = []

        # Check which required directories are missing
        for req_dir in REQUIRED_DIRS:
            dir_path = squad_dir / req_dir
            if not dir_path.exists():
                missing_dirs.append(dir_path)

        if not missing_dirs:
            print(f"✓ {squad_name} — all required directories exist")
            stats["already_ok"] += 1
        else:
            try:
                for dir_path in missing_dirs:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    gitkeep = dir_path / ".gitkeep"
                    gitkeep.touch()

                dir_names = ", ".join(d.name for d in missing_dirs)
                print(f"✅ {squad_name} — created: {dir_names}")
                stats["fixed"] += 1
            except Exception as e:
                print(f"❌ {squad_name} — FAILED: {e}")
                stats["failed"] += 1

    print()
    print("=" * 60)
    print(f"Summary: {stats['fixed']} fixed, {stats['already_ok']} already ok, {stats['failed']} failed")
    print("=" * 60)

    return stats


if __name__ == "__main__":
    repo_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    fix_squad_structure(repo_root)
