"""Esquemas para Squads Gateway — usando dataclasses (stdlib, sem dependências).

Contratos estruturados para indexação, roteamento, handoff e auditoria.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any


@dataclass
class AgentEntry:
    """Agente extraído do squad.yaml."""

    id: str
    role: str = ""
    file: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "file": self.file,
        }


@dataclass
class TaskEntry:
    """Tarefa extraída do squad.yaml."""

    id: str
    file: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "file": self.file,
        }


@dataclass
class WorkflowEntry:
    """Workflow extraído do squad.yaml."""

    id: str
    file: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "file": self.file,
        }


@dataclass
class IndexEntry:
    """Entrada canônica do índice de squads."""

    name: str
    path: str
    display_name: str = ""
    version: str = "1.0.0"
    status: str = "operational-prototype"
    purpose: str = ""
    domain: str = ""
    language: str = "pt-BR"
    creator: str = ""
    license: str = "MIT"
    agents: list[AgentEntry] = field(default_factory=list)
    tasks: list[TaskEntry] = field(default_factory=list)
    workflows: list[WorkflowEntry] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    indexed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def __post_init__(self):
        if not self.name or len(self.name) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        if not self.path:
            raise ValueError("Caminho não pode ser vazio")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "display_name": self.display_name,
            "version": self.version,
            "status": self.status,
            "path": self.path,
            "purpose": self.purpose,
            "domain": self.domain,
            "language": self.language,
            "creator": self.creator,
            "license": self.license,
            "agents": [a.to_dict() for a in self.agents],
            "tasks": [t.to_dict() for t in self.tasks],
            "workflows": [w.to_dict() for w in self.workflows],
            "keywords": self.keywords,
            "tags": self.tags,
            "indexed_at": self.indexed_at,
        }


@dataclass
class Index:
    """Índice completo de squads."""

    version: str = "1.0.0"
    squads: list[IndexEntry] = field(default_factory=list)
    total_count: int = 0
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "squads": [s.to_dict() for s in self.squads],
            "total_count": self.total_count,
            "generated_at": self.generated_at,
            "metadata": self.metadata,
        }


@dataclass
class MatchedEntry:
    """Entrada casada em busca/roteamento."""

    squad: str
    path: str
    score: float
    agent: Optional[str] = None
    role: str = ""
    matched_keywords: list[str] = field(default_factory=list)
    evidence: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "squad": self.squad,
            "path": self.path,
            "score": self.score,
            "agent": self.agent,
            "role": self.role,
            "matched_keywords": self.matched_keywords,
            "evidence": self.evidence,
        }


@dataclass
class RouteRequest:
    """Pedido de roteamento de tarefa."""

    task_description: str
    context: Optional[str] = None
    preferred_domain: Optional[str] = None
    min_score_threshold: float = 2.0
    top_n: int = 3

    def __post_init__(self):
        if not self.task_description or len(self.task_description) < 5:
            raise ValueError("task_description deve ter pelo menos 5 caracteres")
        if self.min_score_threshold < 0:
            raise ValueError("min_score_threshold não pode ser negativo")
        if not (1 <= self.top_n <= 10):
            raise ValueError("top_n deve estar entre 1 e 10")


@dataclass
class GapAnalysis:
    """Análise de lacuna quando nenhum squad atende."""

    reason: str
    suggested_squad_name: str
    has_gap: bool = True
    suggested_capabilities: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "has_gap": self.has_gap,
            "reason": self.reason,
            "suggested_squad_name": self.suggested_squad_name,
            "suggested_capabilities": self.suggested_capabilities,
            "next_steps": self.next_steps,
        }


@dataclass
class RouteDecision:
    """Decisão estruturada de roteamento."""

    task_description: str
    recommendations: list[MatchedEntry] = field(default_factory=list)
    top_match: Optional[MatchedEntry] = None
    gap_analysis: Optional[GapAnalysis] = None
    routing_index_version: str = ""
    decision_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_description": self.task_description,
            "recommendations": [r.to_dict() for r in self.recommendations],
            "top_match": self.top_match.to_dict() if self.top_match else None,
            "gap_analysis": self.gap_analysis.to_dict() if self.gap_analysis else None,
            "routing_index_version": self.routing_index_version,
            "decision_timestamp": self.decision_timestamp,
        }


@dataclass
class ActivationChecklistItem:
    """Item de checklist para ativação."""

    category: str
    item: str
    required: bool = False
    example: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "item": self.item,
            "required": self.required,
            "example": self.example,
        }


@dataclass
class ActivationContract:
    """Contrato de ativação de um squad."""

    squad_name: str
    squad_path: str
    entry_point_agent: str
    activation_prompt: str
    checklist: list[ActivationChecklistItem] = field(default_factory=list)
    available_agents: list[str] = field(default_factory=list)
    available_tasks: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "squad_name": self.squad_name,
            "squad_path": self.squad_path,
            "entry_point_agent": self.entry_point_agent,
            "activation_prompt": self.activation_prompt,
            "checklist": [c.to_dict() for c in self.checklist],
            "available_agents": self.available_agents,
            "available_tasks": self.available_tasks,
            "generated_at": self.generated_at,
        }


@dataclass
class AuditLogEntry:
    """Entrada no log de auditoria (JSONL)."""

    event_type: str
    request_data: dict[str, Any] = field(default_factory=dict)
    result_data: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    user_feedback: Optional[str] = None
    decision_hash: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "request_data": self.request_data,
            "result_data": self.result_data,
            "user_feedback": self.user_feedback,
            "decision_hash": self.decision_hash,
        }
