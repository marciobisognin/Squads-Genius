"""Task generation for generated squads."""
from __future__ import annotations

from typing import Any, Dict, List

from briefing_parser import Briefing


def _schema(fields: List[str]) -> Dict[str, Any]:
    return {"type": "object", "required": fields, "properties": {field: {"type": "string"} for field in fields}}


def _task(task_id: str, description: str, assigned_agent: str, dependencies: List[str], human_approval: bool, timeout: int = 600) -> Dict[str, Any]:
    return {
        "id": task_id,
        "description": description,
        "assigned_agent": assigned_agent,
        "dependencies": dependencies,
        "input_schema": _schema(["briefing", "previous_outputs"]),
        "output_schema": _schema(["status", "artifact_paths", "validation_notes"]),
        "validation_rules": ["arquivo de saída existe e não está vazio", "campos obrigatórios do schema presentes", "conteúdo rastreável ao briefing", "sem credenciais ou segredos persistidos"],
        "timeout": timeout,
        "retry_policy": {"max_attempts": 2, "backoff_seconds": 30, "retry_on": ["erro transitório", "arquivo temporariamente indisponível"]},
        "human_approval": human_approval,
        "failure_behavior": "registrar falha, preservar artefatos parciais e acionar caminho de revisão humana",
    }


def generate_tasks(briefing: Briefing, architecture: Dict[str, Any]) -> List[Dict[str, Any]]:
    agents = {agent["role"]: agent["id"] for agent in architecture["agents"]}
    tasks = [
        _task("01_validate_briefing", "Validar briefing formal, lacunas e premissas antes da execução.", agents["Coordenação e validação de briefing"], [], bool(briefing.human_approval_requirements), 300),
        _task("02_build_expected_outputs", "Gerar os artefatos esperados declarados no briefing sem extrapolar conteúdo sem fundamento.", agents["Produção dos artefatos esperados"], ["01_validate_briefing"], False, 900),
    ]
    if "Integrações declaradas no briefing" in agents:
        tasks.append(_task("03_prepare_integrations", "Preparar contratos e validações para integrações explicitamente informadas.", agents["Integrações declaradas no briefing"], ["01_validate_briefing"], True, 600))
    if "Aprovação humana, segurança e conformidade" in agents:
        deps = ["02_build_expected_outputs"] + (["03_prepare_integrations"] if any(t["id"] == "03_prepare_integrations" for t in tasks) else [])
        tasks.append(_task("04_security_and_human_gate", "Executar gate de segurança e aprovação humana antes de uso externo.", agents["Aprovação humana, segurança e conformidade"], deps, True, 600))
    tasks.append(_task("05_quality_validation", "Validar estrutura, scripts, testes e relatório de qualidade calculado.", agents["Validação, testes e relatório de qualidade"], [task["id"] for task in tasks], False, 600))
    return tasks
