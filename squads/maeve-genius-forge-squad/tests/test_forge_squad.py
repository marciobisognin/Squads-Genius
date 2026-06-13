from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from briefing_parser import BriefingError, load_briefing, validate_briefing
from requirements_analyzer import analyze_requirements
from squad_architect import design_architecture
from task_generator import generate_tasks
from workflow_generator import generate_workflows


def test_yaml_briefing_parser_accepts_formal_schema():
    briefing = load_briefing(ROOT / "examples" / "briefing_atena_contratos_publicos.yaml", strict=True)
    assert briefing.project_name == "Atena Contratos Públicos"
    assert briefing.problem
    assert briefing.target_audience
    assert briefing.expected_outputs
    assert briefing.security_level == "elevated"


def test_briefing_errors_are_clear_in_strict_mode():
    with pytest.raises(BriefingError) as exc:
        validate_briefing({"project_name": "X"}, strict=True)
    assert "Campos obrigatórios" in str(exc.value)


def test_architecture_avoids_integration_agent_without_integrations():
    briefing = validate_briefing({
        "project_name": "Squad Simples",
        "objective": "Gerar relatório local",
        "problem": "Processo manual lento",
        "target_audience": "equipe interna",
        "expected_outputs": ["README.md", "scripts"],
        "security_level": "standard",
    })
    analysis = analyze_requirements(briefing)
    architecture = design_architecture(briefing, analysis)
    roles = {agent["role"] for agent in architecture["agents"]}
    assert "Integrações declaradas no briefing" not in roles
    assert len(roles) == len(architecture["agents"])


def test_generated_task_and_workflow_contracts_are_complete():
    briefing = load_briefing(ROOT / "examples" / "briefing_atena_contratos_publicos.yaml")
    analysis = analyze_requirements(briefing)
    architecture = design_architecture(briefing, analysis)
    tasks = generate_tasks(briefing, architecture)
    workflows = generate_workflows(briefing, tasks)
    for task in tasks:
        for field in ["id", "description", "assigned_agent", "dependencies", "input_schema", "output_schema", "validation_rules", "timeout", "retry_policy", "human_approval", "failure_behavior"]:
            assert field in task
    workflow = workflows[0]
    assert workflow["failure_paths"]
    assert all("gate" in step and "retry_policy" in step and "timeout" in step for step in workflow["steps"])


def test_cli_dry_run_lists_components(tmp_path):
    result = subprocess.run([
        sys.executable,
        str(ROOT / "scripts" / "forge_squad.py"),
        "--briefing",
        str(ROOT / "examples" / "briefing_atena_contratos_publicos.yaml"),
        "--output",
        str(tmp_path / "out"),
        "--dry-run",
        "--strict",
        "--no-llm",
    ], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    data = yaml.safe_load(result.stdout)
    assert data["dry_run"] is True
    assert any(path == "squad.yaml" for path in data["components_planned"])
