#!/usr/bin/env python3
"""Norn Workflow Weaver — tece tasks atômicas e workflows com gates e rollback.

As Nornas fiam o destino no Poço de Urðr; aqui fiamos o fluxo de execução do
squad-alvo: tarefas rastreáveis ao briefing e workflows com gates, rollback e
pontos de humano-no-loop.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

from typing import Any, Dict, List

import yaml

from saga_briefing import Briefing

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


def _dump(data: Any) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)


def generate_tasks(briefing: Briefing, architecture: Dict[str, Any]) -> List[Dict[str, Any]]:
    agents = architecture["agents"]
    by_role = {a["role"]: a["id"] for a in agents}
    intake = next((a["id"] for a in agents if a["id"].endswith("-intake-orchestrator")), agents[0]["id"])
    builder = next((a["id"] for a in agents if a["id"].endswith("-delivery-builder")), agents[-1]["id"])
    sentinel = next((a["id"] for a in agents if a["id"].endswith("-quality-sentinel")), agents[-1]["id"])
    tasks: List[Dict[str, Any]] = [
        {"id": "01_intake_and_validate", "assigned_agent": intake,
         "objective": "Validar briefing, explicitar lacunas e confirmar aprovações humanas.",
         "inputs": ["briefing"], "outputs": ["briefing_validado", "lista_de_lacunas"],
         "acceptance": ["campos obrigatórios presentes", "lacunas registradas por severidade"], "gate": True},
        {"id": "02_build_deliverables", "assigned_agent": builder,
         "objective": f"Produzir os artefatos esperados: {', '.join(briefing.expected_outputs)}.",
         "inputs": ["briefing_validado"], "outputs": list(briefing.expected_outputs),
         "acceptance": ["cada output rastreável ao objetivo", "sem conteúdo sem fundamento"], "gate": False},
        {"id": "03_quality_and_report", "assigned_agent": sentinel,
         "objective": "Validar completude, rodar testes e emitir relatório de qualidade com nota real.",
         "inputs": list(briefing.expected_outputs), "outputs": ["quality_report.json"],
         "acceptance": ["validações executadas", "nota calculada por critérios reais", "sem segredos"], "gate": True},
    ]
    if any(a["id"].endswith("-integration-engineer") for a in agents):
        tasks.insert(2, {"id": "02b_integration_contracts", "assigned_agent": by_role.get("Integrações declaradas", builder),
                         "objective": "Gerar contratos de integração declarados com validação de falha e timeout.",
                         "inputs": ["briefing_validado"], "outputs": ["contratos_integracao"],
                         "acceptance": ["somente integrações declaradas", "nenhum segredo persistido"], "gate": False})
    if any(a["id"].endswith("-security-gatekeeper") for a in agents):
        tasks.append({"id": "04_security_gate", "assigned_agent": by_role.get("Segurança e aprovação humana", sentinel),
                      "objective": "Aplicar gate de segurança e aprovação humana antes de qualquer publicação.",
                      "inputs": ["quality_report.json"], "outputs": ["aprovacao_humana"],
                      "acceptance": ["riscos altos tratados", "aprovação humana registrada"], "gate": True})
    return tasks


def generate_workflows(briefing: Briefing, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    order = [t["id"] for t in tasks]
    gates = [t["id"] for t in tasks if t.get("gate")]
    return [{
        "id": "main_pipeline",
        "description": f"Pipeline principal do squad '{briefing.project_name}'.",
        "human_in_loop": bool(briefing.human_approval_requirements) or briefing.security_level in {"elevated", "high"},
        "rollback": "retornar ao último gate reprovado",
        "steps": [{"order": i + 1, "task": tid, "gate_required": tid in gates} for i, tid in enumerate(order)],
    }]


def generate_task_files(tasks: List[Dict[str, Any]]) -> Dict[str, str]:
    files: Dict[str, str] = {}
    for task in tasks:
        payload = dict(task)
        payload["footer"] = FOOTER
        files[f"tasks/{task['id']}.yaml"] = _dump(payload)
    return files


def generate_workflow_files(workflows: List[Dict[str, Any]]) -> Dict[str, str]:
    files: Dict[str, str] = {}
    for wf in workflows:
        payload = dict(wf)
        payload["footer"] = FOOTER
        files[f"workflows/{wf['id']}.yaml"] = _dump(payload)
    return files


if __name__ == "__main__":  # pragma: no cover
    print("Norn Workflow Weaver — módulo de geração de tasks e workflows.\n" + FOOTER)
