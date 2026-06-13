"""Deterministic requirements analysis for generated squads."""
from __future__ import annotations

from typing import Any, Dict, List

from briefing_parser import BRIEFING_SCHEMA, Briefing


def _flatten_items(value: Any) -> List[str]:
    if isinstance(value, dict):
        return [f"{k}: {v}" for k, v in value.items()]
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def analyze_requirements(briefing: Briefing) -> Dict[str, Any]:
    warnings = list(briefing.warnings)
    human_review: List[str] = []
    risks: List[Dict[str, str]] = []
    constraints = _flatten_items(briefing.constraints)
    integrations = _flatten_items(briefing.integrations)
    if not briefing.success_metrics:
        human_review.append("Definir métricas de sucesso mensuráveis antes de publicação operacional.")
        risks.append({"id": "missing-success-metrics", "severity": "medium", "description": "Métricas de sucesso não foram fornecidas no briefing."})
    if not briefing.human_approval_requirements:
        human_review.append("Confirmar pontos de aprovação humana obrigatórios.")
    if briefing.budget_limit in (None, ""):
        risks.append({"id": "missing-budget-limit", "severity": "low", "description": "Limite de orçamento não informado; scripts não estimam preços fixos."})
    if briefing.security_level in {"elevated", "high"} and not briefing.human_approval_requirements:
        risks.append({"id": "security-without-approval", "severity": "high", "description": "Nível de segurança elevado sem aprovações humanas explícitas."})
    for integration in integrations:
        text = integration.lower()
        if any(marker in text for marker in ["token", "senha", "password", "api key", "secret"]):
            risks.append({"id": "credential-risk", "severity": "high", "description": "Integração menciona credenciais; usar variáveis de ambiente e nunca persistir segredos."})
    return {
        "schema": BRIEFING_SCHEMA,
        "observed": {
            "project_name": briefing.project_name,
            "objective": briefing.objective,
            "problem": briefing.problem,
            "target_audience": briefing.target_audience,
            "expected_outputs": briefing.expected_outputs,
            "constraints": constraints,
            "integrations": integrations,
            "security_level": briefing.security_level,
            "budget_limit": briefing.budget_limit,
            "preferred_models": briefing.preferred_models,
        },
        "warnings": warnings,
        "risks": risks,
        "human_review_required": human_review + briefing.human_approval_requirements,
        "determinism": "A geração local é determinística quando executada com --no-llm; nenhum conteúdo é produzido por chamada externa.",
    }
