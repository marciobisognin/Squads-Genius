"""Architecture rules for avoiding redundant agents."""
from __future__ import annotations

import re
from typing import Any, Dict, List

from briefing_parser import Briefing


def slugify(text: str) -> str:
    text = text.lower().strip()
    replacements = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e", "í": "i", "ó": "o", "ô": "o", "õ": "o", "ú": "u", "ü": "u", "ç": "c"}
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "generated-squad"


def _schema(fields: List[str]) -> Dict[str, Any]:
    return {"type": "object", "required": fields, "properties": {field: {"type": "string"} for field in fields}}


def _agent(agent_id: str, name: str, role: str, objective: str, responsibilities: List[str], non_responsibilities: List[str], allowed_tools: List[str], denied_tools: List[str], security_level: str) -> Dict[str, Any]:
    return {
        "id": agent_id,
        "name": name,
        "role": role,
        "objective": objective,
        "responsibilities": responsibilities,
        "non_responsibilities": non_responsibilities,
        "input_schema": _schema(["briefing", "context"]),
        "output_schema": _schema(["status", "artifacts", "validation_notes"]),
        "allowed_tools": allowed_tools,
        "denied_tools": denied_tools,
        "memory_policy": "Não persistir dados sensíveis; registrar apenas decisões e premissas necessárias ao projeto.",
        "escalation_policy": "Escalar ao humano quando faltar informação obrigatória, houver risco legal/segurança ou aprovação prevista no briefing.",
        "quality_criteria": ["entrega rastreável ao briefing", "sem conteúdo sem fundamento no briefing", "saída validável por schema e testes", "separação entre observado, inferido, risco e recomendação"],
        "security_level": security_level,
    }


def design_architecture(briefing: Briefing, analysis: Dict[str, Any]) -> Dict[str, Any]:
    slug = slugify(briefing.project_name)
    agents: List[Dict[str, Any]] = []
    agents.append(_agent(f"{slug}-intake-orchestrator", "Intake Orchestrator", "Coordenação e validação de briefing", "Garantir que entradas, lacunas e aprovações humanas estejam explícitas antes da execução.", ["validar briefing", "bloquear execução em lacunas críticas", "rotear tarefas conforme dependências"], ["produzir artefatos finais sem validação", "publicar externamente"], ["read_file", "write_file", "yaml_parser"], ["external_publish", "credential_access"], briefing.security_level))
    agents.append(_agent(f"{slug}-delivery-builder", "Delivery Builder", "Produção dos artefatos esperados", "Construir os outputs solicitados com base apenas no briefing validado e nos dados aprovados.", ["gerar artefatos esperados", "produzir documentação operacional", "manter rastreabilidade com objetivo e problema"], ["definir preços sem base", "assumir integrações inexistentes", "aprovar juridicamente conteúdo"], ["read_file", "write_file", "python"], ["network_without_approval", "external_publish"], briefing.security_level))
    if analysis.get("observed", {}).get("integrations", []):
        agents.append(_agent(f"{slug}-integration-engineer", "Integration Engineer", "Integrações declaradas no briefing", "Desenhar contratos técnicos e verificações para integrações explicitamente informadas.", ["mapear integrações declaradas", "gerar contratos de entrada/saída", "definir validações de falha e timeout"], ["criar integração não solicitada", "armazenar token", "executar chamada externa sem aprovação"], ["python", "schema_validator"], ["secret_storage", "external_write_without_approval"], briefing.security_level))
    if briefing.security_level in {"elevated", "high"} or briefing.human_approval_requirements:
        agents.append(_agent(f"{slug}-security-gatekeeper", "Security Gatekeeper", "Aprovação humana, segurança e conformidade", "Aplicar gates de segurança e aprovação humana nas etapas sensíveis.", ["verificar riscos", "aplicar aprovações humanas", "bloquear publicação insegura"], ["substituir decisão humana", "expor segredos", "reduzir critérios de segurança"], ["schema_validator", "secret_scanner"], ["credential_access", "external_publish"], briefing.security_level))
    agents.append(_agent(f"{slug}-quality-sentinel", "Quality Sentinel", "Validação, testes e relatório de qualidade", "Validar completude, consistência, testes e riscos antes de considerar o squad pronto.", ["executar validações", "registrar testes aprovados e reprovados", "calcular nota por critérios reais"], ["maquiar nota fixa", "ignorar falhas", "aprovar arquivo não testado"], ["pytest", "python", "yaml_parser"], ["external_publish"], briefing.security_level))
    return {"slug": slug, "agents": agents, "agent_count_reasoning": "Agentes criados somente para responsabilidades exclusivas: intake, entrega, integração quando declarada, segurança quando exigida e qualidade independente."}
