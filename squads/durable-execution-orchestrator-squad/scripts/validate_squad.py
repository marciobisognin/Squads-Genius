#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, py_compile
from pathlib import Path
try:
    import yaml
except Exception:
    yaml = None
REQUIRED_DIRS = ["agents","tasks","workflows","scripts","tests","examples","docs"]
REQUIRED_FILES = ["README.md","PRD.md","squad.yaml","LICENSE","NOTICE.md","AUTHORS.md","requirements.txt","pyproject.toml","quality_report.json"]
def load_yaml(path: Path):
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) if yaml else json.loads(text)
def validate(root: Path) -> dict:
    issues = []
    for d in REQUIRED_DIRS:
        if not (root / d).is_dir(): issues.append(f"diretório ausente: {d}")
    for f in REQUIRED_FILES:
        if not (root / f).is_file(): issues.append(f"arquivo ausente: {f}")
    try: manifest = load_yaml(root / "squad.yaml")
    except Exception as exc: issues.append(f"squad.yaml inválido: {exc}"); manifest = {}
    for section in ["agents","tasks","workflows"]:
        for item in manifest.get(section, []) if isinstance(manifest, dict) else []:
            rel = item.get("file")
            if not rel or not (root / rel).is_file(): issues.append(f"{section} referenciado ausente: {rel}")
    for path in root.rglob("*.yaml"):
        try: load_yaml(path)
        except Exception as exc: issues.append(f"YAML inválido em {path.relative_to(root)}: {exc}")
    for path in root.rglob("*.py"):
        if "__pycache__" in path.parts: continue
        try: py_compile.compile(str(path), doraise=True)
        except Exception as exc: issues.append(f"Python inválido em {path.relative_to(root)}: {exc}")
    return {"go_no_go":"go" if not issues else "no-go","issues":issues,"checked_files":len([p for p in root.rglob('*') if p.is_file()])}
def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--root", default="."); args = parser.parse_args(); report = validate(Path(args.root).resolve()); print(json.dumps(report, ensure_ascii=False, indent=2)); return 0 if report["go_no_go"] == "go" else 1
if __name__ == "__main__": raise SystemExit(main())
