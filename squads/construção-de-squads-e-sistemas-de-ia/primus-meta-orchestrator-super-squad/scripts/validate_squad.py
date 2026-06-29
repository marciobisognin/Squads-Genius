#!/usr/bin/env python3
"""Validador / quality gate do squad (go-no-go).

Verifica estrutura mínima, manifesto, integridade de YAML/Python e ausência de
segredos. Compatível com o padrão do repositório Squads-Genius.
"""
from __future__ import annotations

import argparse
import json
import py_compile
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

REQUIRED_DIRS = ['agents', 'tasks', 'workflows', 'scripts', 'examples', 'docs']
REQUIRED_FILES = ['squad.yaml', 'README.md', 'LICENSE', 'NOTICE.md', 'AUTHORS.md']
SECRET_PATTERNS = [
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'gho_[A-Za-z0-9_]{20,}'),
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
    re.compile(r'BEGIN PRIVATE KEY'),
    re.compile(r'(?i)(password|token)\s*=\s*[^\s\]})]+'),
]


def load_manifest(root: Path) -> dict[str, Any]:
    text = (root / 'squad.yaml').read_text(encoding='utf-8')
    if yaml is not None:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError('squad.yaml deve conter objeto/mapping na raiz')
    return data


def _scan_yaml(path: Path, root: Path, issues: list[str]) -> None:
    if path.suffix not in {'.yaml', '.yml'} or yaml is None:
        return
    try:
        yaml.safe_load(path.read_text(encoding='utf-8'))
    except Exception as exc:
        issues.append(f'YAML inválido em {path.relative_to(root)}: {exc}')


def _scan_python(path: Path, root: Path, issues: list[str]) -> None:
    if path.suffix != '.py':
        return
    try:
        py_compile.compile(str(path), doraise=True)
    except Exception as exc:
        issues.append(f'Python inválido em {path.relative_to(root)}: {exc}')


def _scan_secrets(path: Path, root: Path, issues: list[str]) -> None:
    if '__pycache__' in path.parts or path.name in {'validate_squad.py', 'scaffold_squad.py'}:
        return
    try:
        txt = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return
    for pattern in SECRET_PATTERNS:
        if pattern.search(txt):
            issues.append(f'possível segredo em {path.relative_to(root)}: {pattern.pattern}')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    args = ap.parse_args()
    root = Path(args.root).resolve()
    issues: list[str] = []
    for d in REQUIRED_DIRS:
        if not (root / d).is_dir():
            issues.append(f'diretório ausente: {d}')
    for f in REQUIRED_FILES:
        if not (root / f).is_file():
            issues.append(f'arquivo ausente: {f}')
    try:
        manifest = load_manifest(root)
    except Exception as exc:
        print(json.dumps({'go_no_go': 'no-go', 'issues': [f'squad.yaml inválido: {exc}']},
                         ensure_ascii=False, indent=2))
        return 2
    for item in manifest.get('agents', []):
        if isinstance(item, dict) and not (root / item['file']).is_file():
            issues.append('agente ausente: ' + item['file'])
    for item in manifest.get('tasks', []):
        if isinstance(item, dict) and not (root / item['file']).is_file():
            issues.append('task ausente: ' + item['file'])
    for item in manifest.get('workflows', []):
        if isinstance(item, dict) and not (root / item['file']).is_file():
            issues.append('workflow ausente: ' + item['file'])
    for path in root.rglob('*'):
        if path.is_file():
            _scan_yaml(path, root, issues)
            _scan_python(path, root, issues)
            _scan_secrets(path, root, issues)
    completeness = 100 if not issues else max(0, 100 - len(issues) * 5)
    report = {
        'completeness': completeness,
        'traceability': 90 if manifest.get('agents') and manifest.get('tasks') else 60,
        'originality': 90,
        'execution_readiness': 95 if not issues else 60,
        'safety': 95 if not issues else 50,
        'go_no_go': 'go' if not issues else 'no-go',
        'issues': issues,
        'recommendations': ['Publicar no GitHub somente após autorização humana.'],
    }
    (root / 'output').mkdir(exist_ok=True)
    (root / 'output' / 'quality_report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == '__main__':
    sys.exit(main())
