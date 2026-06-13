"""Generate pytest tests for produced squads."""
from __future__ import annotations

from typing import Dict, List


def generate_tests(expected_files: List[str]) -> Dict[str, str]:
    expected_repr = repr(sorted(expected_files))
    structure_test = f'''from pathlib import Path
import json
import py_compile

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FILES = {expected_repr}


def test_all_expected_files_exist_and_are_not_empty():
    for rel in EXPECTED_FILES:
        path = ROOT / rel
        assert path.is_file(), f"arquivo esperado ausente: {{rel}}"
        assert path.read_text(encoding="utf-8").strip(), f"arquivo vazio: {{rel}}"


def test_yaml_and_json_files_parse():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix in {{".yaml", ".yml"}}:
            assert yaml.safe_load(path.read_text(encoding="utf-8")) is not None, path
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))


def test_python_scripts_compile():
    for path in (ROOT / "scripts").glob("*.py"):
        py_compile.compile(str(path), doraise=True)
'''
    contract_test = '''from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_agent_contract_fields():
    required = {
        "id", "name", "role", "objective", "responsibilities", "non_responsibilities",
        "input_schema", "output_schema", "allowed_tools", "denied_tools", "memory_policy",
        "escalation_policy", "quality_criteria"
    }
    for path in (ROOT / "agents").glob("*.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert required <= set(data), f"campos ausentes em {path.name}: {required - set(data)}"


def test_task_contract_fields():
    required = {
        "id", "description", "assigned_agent", "dependencies", "input_schema", "output_schema",
        "validation_rules", "timeout", "retry_policy", "human_approval", "failure_behavior"
    }
    for path in (ROOT / "tasks").glob("*.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert required <= set(data), f"campos ausentes em {path.name}: {required - set(data)}"


def test_workflow_has_gates_and_failure_paths():
    for path in (ROOT / "workflows").glob("*.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert data.get("steps"), path.name
        assert data.get("failure_paths"), path.name
        for step in data["steps"]:
            assert "gate" in step
            assert "retry_policy" in step
            assert "timeout" in step
'''
    return {"tests/test_generated_files.py": structure_test, "tests/test_contracts.py": contract_test}
