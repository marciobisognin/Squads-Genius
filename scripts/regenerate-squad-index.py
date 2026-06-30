#!/usr/bin/env python3
"""
Regenerate SQUAD_INDEX.md with conformance status and all squad metadata.
Reads squad.yaml, checks compliance, and generates index with badges.
"""

import sys
from pathlib import Path
import yaml


def load_squad_yaml(filepath):
    """Load squad.yaml file."""
    try:
        return yaml.safe_load(filepath.read_text(encoding="utf-8"))
    except Exception:
        return None


def check_squad_compliance(squad_dir):
    """Check if squad passes 6-point compliance checklist."""
    checks = {
        "squad_yaml": (squad_dir / "squad.yaml").exists(),
        "readme": (squad_dir / "README.md").exists(),
        "license": (squad_dir / "LICENSE").exists(),
        "agents": (squad_dir / "agents").is_dir(),
        "tasks": (squad_dir / "tasks").is_dir(),
        "workflows": (squad_dir / "workflows").is_dir(),
    }

    passed = sum(1 for v in checks.values() if v)
    return passed, checks


def get_status_badge(passed):
    """Return status badge based on compliance score."""
    if passed == 6:
        return "✅"
    elif passed >= 4:
        return "⚠️"
    else:
        return "❌"


def generate_squad_index(repo_root=None):
    """Generate SQUAD_INDEX.md with compliance badges."""
    if repo_root is None:
        repo_root = Path.cwd()
    else:
        repo_root = Path(repo_root)

    # Find all squad directories
    squads = []
    for squad_yaml in sorted(repo_root.rglob("squad.yaml")):
        squad_dir = squad_yaml.parent
        data = load_squad_yaml(squad_yaml)

        if data:
            passed, checks = check_squad_compliance(squad_dir)
            badge = get_status_badge(passed)

            # Determine README path (relative to repo root)
            readme_path = squad_dir / "README.md"
            if readme_path.exists():
                readme_rel = str(readme_path.relative_to(repo_root))
            else:
                readme_rel = None

            squads.append(
                {
                    "id": data.get("name", squad_dir.name),
                    "display_name": data.get("commercial_name", data.get("name", squad_dir.name)),
                    "version": data.get("version", "não informada"),
                    "positioning": data.get("positioning", ""),
                    "readme": readme_rel,
                    "squad_dir": str(squad_dir.relative_to(repo_root)),
                    "compliance_passed": passed,
                    "compliance_total": 6,
                    "badge": badge,
                    "checks": checks,
                }
            )

    # Sort by ID
    squads.sort(key=lambda x: x["id"])

    # Generate index content
    lines = [
        "# Índice de Squads",
        "",
        "Squads publicados no repositório `Squads-Genius`.",
        "",
        "**Legenda de conformidade**:",
        "- ✅ Completo (6/6 requisitos)",
        "- ⚠️ Parcial (4-5/6 requisitos)",
        "- ❌ Incompleto (<4/6 requisitos)",
        "",
        "---",
        "",
    ]

    for squad in squads:
        # Format badge and compliance info
        status = f"{squad['badge']} `{squad['compliance_passed']}/{squad['compliance_total']}`"

        # Build entry
        if squad["readme"]:
            entry = f"- {status} [{squad['display_name']}]({squad['readme']}) — `{squad['id']}` — v`{squad['version']}`"
        else:
            entry = f"- {status} {squad['display_name']} — `{squad['id']}` — v`{squad['version']}` ⚠️ sem README"

        # Add positioning if available
        if squad["positioning"]:
            positioning = squad["positioning"][:100].rstrip() + ("..." if len(squad["positioning"]) > 100 else "")
            entry += f"\n  - {positioning}"

        lines.append(entry)
        lines.append("")

    # Add summary section
    total = len(squads)
    complete = sum(1 for s in squads if s["compliance_passed"] == 6)
    partial = sum(1 for s in squads if 4 <= s["compliance_passed"] < 6)
    incomplete = sum(1 for s in squads if s["compliance_passed"] < 4)

    lines.extend(
        [
            "",
            "---",
            "",
            "## Resumo de Conformidade",
            "",
            f"| Status | Quantidade | Percentual |",
            f"|--------|-----------|-----------|",
            f"| ✅ Completo | {complete} | {100*complete//total}% |",
            f"| ⚠️ Parcial | {partial} | {100*partial//total}% |",
            f"| ❌ Incompleto | {incomplete} | {100*incomplete//total}% |",
            f"| **Total** | **{total}** | **100%** |",
            "",
        ]
    )

    content = "\n".join(lines)

    # Write to file
    index_path = repo_root / "SQUAD_INDEX.md"
    index_path.write_text(content, encoding="utf-8")

    print(f"✅ Generated SQUAD_INDEX.md ({total} squads, {complete} complete)")
    print(f"   ✅ {complete} complete | ⚠️ {partial} partial | ❌ {incomplete} incomplete")

    return squads


if __name__ == "__main__":
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML not found. Installing...")
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
        import yaml

    repo_root = sys.argv[1] if len(sys.argv) > 1 else None
    generate_squad_index(repo_root)
