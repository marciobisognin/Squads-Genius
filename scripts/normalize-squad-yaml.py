#!/usr/bin/env python3
"""
Convert all squad.yaml from JSON to YAML format and harmonize versions.
Uses json and yaml (PyYAML) or falls back to manual parsing if needed.
"""

import json
import sys
from pathlib import Path


def load_squad_file(filepath):
    """Load squad file (JSON or YAML)."""
    content = filepath.read_text(encoding="utf-8")
    content = content.strip()

    if content.startswith("{"):
        return json.loads(content)
    elif content.startswith("name:") or content.startswith("---"):
        import yaml

        return yaml.safe_load(content)
    else:
        raise ValueError(f"Unknown format for {filepath}")


def save_as_yaml(data, filepath):
    """Save data as YAML format with safe serialization."""
    import yaml

    class CustomDumper(yaml.SafeDumper):
        pass

    def str_presenter(dumper, data):
        if "\n" in data or len(data) > 80:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    CustomDumper.add_representer(str, str_presenter)

    yaml_str = yaml.dump(
        data, Dumper=CustomDumper, default_flow_style=False, allow_unicode=True, sort_keys=False
    )

    filepath.write_text(yaml_str, encoding="utf-8")


def harmonize_version(version_str):
    """Convert version to semver X.Y.Z format."""
    if not version_str or version_str == "não informada" or version_str.lower() == "unknown":
        return "0.1.0"

    version_str = str(version_str).strip()

    # Try to parse existing version
    parts = version_str.split(".")
    if len(parts) >= 3:
        try:
            return f"{int(parts[0])}.{int(parts[1])}.{int(parts[2])}"
        except ValueError:
            pass

    # Fallback: 0.1.0
    return "0.1.0"


def normalize_squad_yaml(repo_root=None):
    """Normalize all squad.yaml files."""
    if repo_root is None:
        repo_root = Path.cwd()
    else:
        repo_root = Path(repo_root)

    stats = {"converted": 0, "already_yaml": 0, "harmonized": 0, "failed": 0}

    # Find all squad.yaml files
    squad_files = list(repo_root.rglob("squad.yaml"))
    print(f"Found {len(squad_files)} squad.yaml files.")
    print()

    for squad_file in sorted(squad_files):
        squad_name = squad_file.parent.name

        try:
            content = squad_file.read_text(encoding="utf-8").strip()

            is_json = content.startswith("{")
            is_yaml = content.startswith("name:") or content.startswith("---")

            if not is_json and not is_yaml:
                print(f"⚠️  {squad_name} — Unknown format, skipping")
                stats["failed"] += 1
                continue

            # Load the file
            data = load_squad_file(squad_file)

            # Harmonize version
            if isinstance(data, dict) and "version" in data:
                old_version = data["version"]
                data["version"] = harmonize_version(old_version)
                if data["version"] != old_version:
                    stats["harmonized"] += 1

            # Save as YAML
            save_as_yaml(data, squad_file)

            if is_json:
                print(f"✅ {squad_name} — JSON → YAML converted")
                stats["converted"] += 1
            else:
                print(f"✓ {squad_name} — Already YAML (version harmonized)")
                stats["already_yaml"] += 1

        except Exception as e:
            print(f"❌ {squad_name} — FAILED: {e}")
            stats["failed"] += 1

    print()
    print("=" * 60)
    print(
        f"Summary: {stats['converted']} JSON→YAML, {stats['already_yaml']} already YAML, "
        f"{stats['harmonized']} versions harmonized, {stats['failed']} failed"
    )
    print("=" * 60)

    return stats


if __name__ == "__main__":
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML not found. Installing...")
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
        import yaml

    repo_root = sys.argv[1] if len(sys.argv) > 1 else None
    normalize_squad_yaml(repo_root)
