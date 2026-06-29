"""Workflow generation with gates, retries, timeouts and failure paths."""
from __future__ import annotations

from typing import Any, Dict, List

from briefing_parser import Briefing


def generate_workflows(briefing: Briefing, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    steps = []
    for task in tasks:
        steps.append({
            "task": task["id"],
            "assigned_agent": task["assigned_agent"],
            "depends_on": task["dependencies"],
            "condition": "sempre" if not task["human_approval"] else "prosseguir somente após aprovação humana registrada",
            "timeout": task["timeout"],
            "retry_policy": task["retry_policy"],
            "gate": {"type": "approval" if task["human_approval"] else "validation", "pass_when": task["validation_rules"], "fail_when": ["schema inválido", "arquivo ausente", "risco alto sem aprovação"]},
            "on_failure": "failure_review_path",
        })
    workflow = {
        "id": "full_generation_workflow",
        "name": f"Workflow completo — {briefing.project_name}",
        "description": "Workflow determinístico gerado a partir do briefing, com condições, dependências, retries, timeouts, gates e caminho de falha.",
        "entrypoint": tasks[0]["id"] if tasks else None,
        "steps": steps,
        "failure_paths": {"failure_review_path": {"description": "Interromper execução, consolidar evidências, registrar artefatos parciais e solicitar revisão humana.", "notify": "human_owner", "resume_condition": "lacuna corrigida ou aprovação registrada"}},
        "success_conditions": briefing.success_metrics or ["todos os arquivos obrigatórios existem", "todos os testes automatizados passam"],
    }
    return [workflow]
