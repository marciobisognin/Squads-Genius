#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import py_compile
import re
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None

REQUIRED_DIRS = ['agents', 'tasks', 'workflows', 'scripts', 'tests', 'examples', 'docs', 'schemas', 'templates']
REQUIRED_FILES = ['squad.yaml', 'README.md', 'PRD.md', 'guardrails.md', 'LICENSE', 'NOTICE.md', 'AUTHORS.md', 'requirements.txt', 'quality_report.json']
AGENT_FIELDS = ['id', 'name', 'role', 'objective', 'responsibilities', 'non_responsibilities', 'input_schema', 'output_schema', 'allowed_tools', 'denied_tools', 'memory_policy', 'escalation_policy', 'quality_criteria']
TASK_FIELDS = ['id', 'description', 'assigned_agent', 'dependencies', 'input_schema', 'output_schema', 'validation_rules', 'timeout', 'retry_policy', 'human_approval', 'failure_behavior']
SECRET_PATTERNS = [re.compile(r'github_pat_[A-Za-z0-9_]{20,}'), re.compile(r'gho_[A-Za-z0-9_]{20,}'), re.compile(r'sk-[A-Za-z0-9]{20,}'), re.compile(r'BEGIN PRIVATE KEY')]


def load_yaml(path: Path):
    text = path.read_text(encoding='utf-8')
    if yaml is None:
        raise RuntimeError('PyYAML não disponível')
    return yaml.safe_load(text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    args = ap.parse_args()
    root = Path(args.root).resolve()
    issues = []
    for d in REQUIRED_DIRS:
        if not (root / d).is_dir():
            issues.append(f'diretório ausente: {d}')
    for f in REQUIRED_FILES:
        if not (root / f).is_file():
            issues.append(f'arquivo ausente: {f}')
    try:
        manifest = load_yaml(root / 'squad.yaml')
    except Exception as exc:
        print(json.dumps({'go_no_go': 'no-go', 'issues': [f'squad.yaml inválido: {exc}']}, ensure_ascii=False, indent=2))
        return 2
    for item in manifest.get('agents', []):
        p = root / item['file']
        if not p.is_file():
            issues.append(f'agente ausente: {item.get("file")}')
            continue
        data = load_yaml(p)
        missing = [f for f in AGENT_FIELDS if f not in data]
        if missing:
            issues.append(f'{p.relative_to(root)} sem campos: {missing}')
    for item in manifest.get('tasks', []):
        p = root / item['file']
        if not p.is_file():
            issues.append(f'task ausente: {item.get("file")}')
            continue
        data = load_yaml(p)
        missing = [f for f in TASK_FIELDS if f not in data]
        if missing:
            issues.append(f'{p.relative_to(root)} sem campos: {missing}')
    for item in manifest.get('workflows', []):
        p = root / item['file']
        if not p.is_file():
            issues.append(f'workflow ausente: {item.get("file")}')
    for path in root.rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts or '.pytest_cache' in path.parts:
            continue
        if path.suffix in {'.yaml', '.yml'}:
            try:
                load_yaml(path)
            except Exception as exc:
                issues.append(f'YAML inválido em {path.relative_to(root)}: {exc}')
        if path.suffix == '.py':
            try:
                py_compile.compile(str(path), doraise=True)
            except Exception as exc:
                issues.append(f'Python inválido em {path.relative_to(root)}: {exc}')
        if path.name == 'validate_squad.py':
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                issues.append(f'possível segredo em {path.relative_to(root)}')
    report = {'go_no_go': 'go' if not issues else 'no-go', 'issues': issues, 'checked_files': sum(1 for p in root.rglob('*') if p.is_file())}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == '__main__':
    raise SystemExit(main())
