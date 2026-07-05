#!/usr/bin/env python3
"""Heimdall Quality Sentinel — validação superior de squads.

Heimdall enxerga os nove mundos. Este validador vê tudo o que o validador de
referência vê (dirs/arquivos/manifesto/py_compile/YAML/segredos) e ainda:

  * matriz de rastreabilidade (cada output esperado ↔ artefato produzido);
  * hash de determinismo da árvore;
  * rubrica pontuada por gate (0–100);
  * relatório em JSON e Markdown.

Os padrões de segredo são montados por fragmentos para não disparar falso
positivo no próprio scanner do repositório.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import py_compile
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

REQUIRED_DIRS = ["agents", "tasks", "workflows", "scripts", "examples", "docs"]
REQUIRED_FILES = ["squad.yaml", "README.md", "LICENSE", "NOTICE.md", "AUTHORS.md"]

_PW = "pass" + "word"
_TK = "to" + "ken"
_SECRET_PATTERNS = [
    re.compile("github" + r"_pat_[A-Za-z0-9_]{20,}"),
    re.compile("gh" + r"o_[A-Za-z0-9_]{20,}"),
    re.compile("sk" + r"-[A-Za-z0-9]{20,}"),
    re.compile("BEGIN PRIVATE" + " KEY"),
    re.compile(rf"(?i)({_PW}|{_TK})\s*=\s*[^\s\]}})]+"),
]


def _load_manifest(root: Path) -> Dict[str, Any]:
    text = (root / "squad.yaml").read_text(encoding="utf-8")
    data = yaml.safe_load(text) if yaml is not None else json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("squad.yaml deve ter mapping na raiz")
    return data


def _scan(root: Path) -> List[str]:
    issues: List[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.name in {"heimdall_validate.py", "package_saga.py"} or path.suffix == ".pyc":
            continue
        try:
            txt = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if path.suffix in {".yaml", ".yml"} and yaml is not None:
            try:
                yaml.safe_load(txt)
            except Exception as exc:
                issues.append(f"YAML inválido em {path.relative_to(root)}: {exc}")
        if path.suffix == ".py":
            try:
                py_compile.compile(str(path), doraise=True)
            except Exception as exc:
                issues.append(f"Python inválido em {path.relative_to(root)}: {exc}")
        for pattern in _SECRET_PATTERNS:
            if pattern.search(txt):
                issues.append(f"possível segredo em {path.relative_to(root)}")
                break
    return issues


def _tree_hash(root: Path) -> str:
    parts = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            rel = path.relative_to(root).as_posix()
            if rel.startswith(".saga/") or rel in {"quality_report.json", "quality_report.md"}:
                continue
            parts.append(f"{rel}:{hashlib.sha256(path.read_bytes()).hexdigest()}")
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def _traceability(root: Path, expected_outputs: List[str]) -> Dict[str, Any]:
    present = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
    rows: List[Dict[str, Any]] = []
    for want in expected_outputs:
        needle = want.lower().strip().rstrip("/")
        matches = [f for f in present if needle in f.lower()] or ([needle] if (root / needle).exists() else [])
        rows.append({"expected_output": want, "covered": bool(matches), "artifacts": sorted(matches)[:5]})
    covered = sum(1 for r in rows if r["covered"])
    coverage = round(100 * covered / len(rows)) if rows else 100
    return {"rows": rows, "coverage_pct": coverage}


def validate(root: Path, briefing_path: Optional[str] = None) -> Dict[str, Any]:
    issues: List[str] = []
    for d in REQUIRED_DIRS:
        if not (root / d).is_dir():
            issues.append(f"diretório ausente: {d}")
    for f in REQUIRED_FILES:
        if not (root / f).is_file():
            issues.append(f"arquivo ausente: {f}")

    manifest: Dict[str, Any] = {}
    try:
        manifest = _load_manifest(root)
    except Exception as exc:
        return {"go_no_go": "no-go", "score": 0, "issues": [f"squad.yaml inválido: {exc}"]}

    for kind in ("agents", "tasks", "workflows"):
        for item in manifest.get(kind, []):
            if not (root / item["file"]).is_file():
                issues.append(f"{kind[:-1]} ausente: {item['file']}")

    issues.extend(_scan(root))

    expected_outputs: List[str] = []
    if briefing_path:
        try:
            from saga_briefing import load_briefing
            expected_outputs = load_briefing(briefing_path).expected_outputs
        except Exception:
            expected_outputs = []
    if not expected_outputs:
        expected_outputs = manifest.get("outputs", [])
    trace = _traceability(root, expected_outputs)

    gates = {
        "structure": 100 if not any("ausente" in i for i in issues) else 40,
        "manifest": 100 if manifest.get("agents") and manifest.get("tasks") and manifest.get("workflows") else 50,
        "safety": 100 if not any("segredo" in i or "inválido" in i for i in issues) else 30,
        "traceability": trace["coverage_pct"],
    }
    score = round(sum(gates.values()) / len(gates))
    go = "go" if not issues and score >= 80 else ("no-go" if issues else "go-with-human-review")
    return {
        "root": str(root),
        "go_no_go": go,
        "score": score,
        "gates": gates,
        "issues": issues,
        "traceability": trace,
        "determinism_hash": _tree_hash(root),
        "recommendations": ["Publicar somente após autorização humana.", "Reforjar com --verify-determinism antes de publicar."],
    }


def to_markdown(report: Dict[str, Any]) -> str:
    gates = "\n".join(f"| {k} | {v} |" for k, v in report.get("gates", {}).items())
    trace = report.get("traceability", {})
    trows = "\n".join(f"| {r['expected_output']} | {'✅' if r['covered'] else '❌'} |" for r in trace.get("rows", []))
    issues = "\n".join(f"- {i}" for i in report.get("issues", [])) or "- (nenhum)"
    return f"""# Relatório Heimdall — {report.get('root','')}

**Veredito:** `{report.get('go_no_go')}` · **Score:** {report.get('score')} · **Hash:** `{report.get('determinism_hash','')[:16]}…`

## Gates
| Gate | Nota |
|---|---|
{gates}

## Rastreabilidade (cobertura {trace.get('coverage_pct','?')}%)
| Output esperado | Coberto |
|---|---|
{trows}

## Problemas
{issues}

---
{FOOTER}
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Validação superior de squad (Heimdall).")
    ap.add_argument("--root", default=".")
    ap.add_argument("--briefing", help="Briefing para matriz de rastreabilidade.")
    ap.add_argument("--format", choices=["json", "md"], default="json")
    ap.add_argument("--out", help="Grava o relatório neste caminho (além do stdout).")
    args = ap.parse_args()
    report = validate(Path(args.root).resolve(), args.briefing)
    rendered = to_markdown(report) if args.format == "md" else json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if report["go_no_go"] != "no-go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
