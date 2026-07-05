#!/usr/bin/env python3
"""Runic Architect — análise de requisitos e desenho de arquitetura não-redundante.

Deriva, de forma determinística, o conjunto mínimo de agentes necessários (um por
responsabilidade exclusiva) e uma matriz de capacidade que prova a ausência de
sobreposição — evitando o inchaço de squads com agentes redundantes.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

from saga_briefing import BRIEFING_SCHEMA, Briefing

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

_ACCENTS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e", "í": "i",
            "ó": "o", "ô": "o", "õ": "o", "ú": "u", "ü": "u", "ç": "c", "ñ": "n"}


def slugify(text: str) -> str:
    text = text.lower().strip()
    for src, dst in _ACCENTS.items():
        text = text.replace(src, dst)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "generated-squad"


def _flatten(value: Any) -> List[str]:
    if isinstance(value, dict):
        return [f"{k}: {v}" for k, v in value.items()]
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def analyze_requirements(briefing: Briefing) -> Dict[str, Any]:
    human_review: List[str] = list(briefing.human_approval_requirements)
    risks: List[Dict[str, str]] = []
    constraints = _flatten(briefing.constraints)
    integrations = _flatten(briefing.integrations)

    for gap in briefing.gaps:
        sev = gap.get("severity", "low")
        if sev in {"blocker", "high"}:
            risks.append({"id": f"gap-{gap['field']}", "severity": "high" if sev == "high" else "high", "description": gap["note"]})
            human_review.append(gap["note"])
        elif sev == "medium":
            risks.append({"id": f"gap-{gap['field']}", "severity": "medium", "description": gap["note"]})
    if briefing.budget_limit in (None, ""):
        risks.append({"id": "missing-budget-limit", "severity": "low", "description": "Limite de orçamento não informado; scripts não fixam preços."})
    for integration in integrations:
        low = integration.lower()
        if any(marker in low for marker in ["credencial", "senha", "secret", "api key", "chave"]):
            risks.append({"id": "credential-risk", "severity": "high", "description": "Integração cita credenciais; usar variáveis de ambiente e nunca persistir segredos."})

    return {
        "schema": BRIEFING_SCHEMA,
        "observed": {
            "project_name": briefing.project_name, "objective": briefing.objective,
            "problem": briefing.problem, "target_audience": briefing.target_audience,
            "expected_outputs": briefing.expected_outputs, "constraints": constraints,
            "integrations": integrations, "security_level": briefing.security_level,
            "budget_limit": briefing.budget_limit, "preferred_models": briefing.preferred_models,
        },
        "warnings": briefing.warnings,
        "gaps": briefing.gaps,
        "risks": risks,
        "human_review_required": human_review,
        "determinism": "Geração local determinística com --no-llm; nenhum conteúdo vem de chamada externa.",
    }


def _schema(fields: List[str]) -> Dict[str, Any]:
    return {"type": "object", "required": fields, "properties": {f: {"type": "string"} for f in fields}}


def _agent(agent_id: str, name: str, role: str, objective: str, capabilities: List[str],
           responsibilities: List[str], non_responsibilities: List[str],
           allowed_tools: List[str], denied_tools: List[str], security_level: str) -> Dict[str, Any]:
    return {
        "id": agent_id, "name": name, "role": role, "objective": objective,
        "capabilities": capabilities, "responsibilities": responsibilities,
        "non_responsibilities": non_responsibilities,
        "input_schema": _schema(["briefing", "context"]),
        "output_schema": _schema(["status", "artifacts", "validation_notes"]),
        "allowed_tools": allowed_tools, "denied_tools": denied_tools,
        "memory_policy": "Não persistir dados sensíveis; registrar apenas decisões e premissas necessárias.",
        "escalation_policy": "Escalar ao humano em lacuna obrigatória, risco legal/segurança ou aprovação prevista.",
        "quality_criteria": [
            "entrega rastreável ao briefing", "sem conteúdo sem fundamento",
            "saída validável por schema e testes", "separação entre observado, inferido, risco e recomendação",
        ],
        "security_level": security_level,
    }


def design_architecture(briefing: Briefing, analysis: Dict[str, Any]) -> Dict[str, Any]:
    slug = slugify(briefing.project_name)
    sec = briefing.security_level
    agents: List[Dict[str, Any]] = []
    agents.append(_agent(
        f"{slug}-intake-orchestrator", "Intake Orchestrator", "Coordenação e validação de briefing",
        "Garantir entradas, lacunas e aprovações humanas explícitas antes da execução.",
        ["intake", "gating", "routing"],
        ["validar briefing", "bloquear execução em lacunas críticas", "rotear tarefas por dependência"],
        ["produzir artefatos finais", "publicar externamente"],
        ["read_file", "write_file", "yaml_parser"], ["external_publish", "credential_access"], sec))
    agents.append(_agent(
        f"{slug}-delivery-builder", "Delivery Builder", "Produção dos artefatos esperados",
        "Construir os outputs solicitados com base apenas no briefing validado.",
        ["authoring", "assembly"],
        ["gerar artefatos esperados", "produzir documentação operacional", "manter rastreabilidade"],
        ["definir preços sem base", "assumir integrações inexistentes", "aprovar juridicamente"],
        ["read_file", "write_file", "python"], ["network_without_approval", "external_publish"], sec))
    if analysis.get("observed", {}).get("integrations"):
        agents.append(_agent(
            f"{slug}-integration-engineer", "Integration Engineer", "Integrações declaradas",
            "Desenhar contratos e verificações para integrações explicitamente informadas.",
            ["integration_contracts"],
            ["mapear integrações declaradas", "gerar contratos I/O", "definir timeout e falha"],
            ["criar integração não solicitada", "armazenar credencial", "chamar externo sem aprovação"],
            ["python", "schema_validator"], ["secret_storage", "external_write_without_approval"], sec))
    if sec in {"elevated", "high"} or briefing.human_approval_requirements:
        agents.append(_agent(
            f"{slug}-security-gatekeeper", "Security Gatekeeper", "Segurança e aprovação humana",
            "Aplicar gates de segurança e aprovação humana em etapas sensíveis.",
            ["security_gating", "compliance"],
            ["verificar riscos", "aplicar aprovações humanas", "bloquear publicação insegura"],
            ["substituir decisão humana", "expor segredos", "reduzir critérios de segurança"],
            ["schema_validator", "secret_scanner"], ["credential_access", "external_publish"], sec))
    agents.append(_agent(
        f"{slug}-quality-sentinel", "Quality Sentinel", "Validação, testes e relatório",
        "Validar completude, consistência, testes e riscos antes de considerar o squad pronto.",
        ["validation", "reporting"],
        ["executar validações", "registrar testes aprovados/reprovados", "calcular nota por critérios reais"],
        ["maquiar nota fixa", "ignorar falhas", "aprovar arquivo não testado"],
        ["pytest", "python", "yaml_parser"], ["external_publish"], sec))

    capability_matrix = {agent["id"]: agent["capabilities"] for agent in agents}
    all_caps = [c for caps in capability_matrix.values() for c in caps]
    overlaps = sorted({c for c in all_caps if all_caps.count(c) > 1})
    return {
        "slug": slug,
        "agents": agents,
        "capability_matrix": capability_matrix,
        "capability_overlaps": overlaps,
        "non_redundant": not overlaps,
        "reasoning": "Um agente por responsabilidade exclusiva: intake, entrega, integração (se declarada), "
                     "segurança (se exigida) e qualidade independente. Matriz de capacidade sem sobreposição.",
    }


if __name__ == "__main__":  # pragma: no cover - demonstração rápida
    import json
    from saga_briefing import load_briefing
    import sys
    b = load_briefing(sys.argv[1])
    a = analyze_requirements(b)
    print(json.dumps(design_architecture(b, a), ensure_ascii=False, indent=2))
