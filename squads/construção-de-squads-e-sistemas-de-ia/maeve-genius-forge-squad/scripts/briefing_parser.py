"""Parsing, schema and validation for Maeve Genius Forge briefings."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

BRIEFING_SCHEMA: Dict[str, Dict[str, Any]] = {
    "project_name": {"type": "string", "required": True, "description": "Nome humano do projeto/squad."},
    "objective": {"type": "string", "required": True, "description": "Objetivo principal que o squad deve alcançar."},
    "problem": {"type": "string", "required": True, "description": "Problema real que justifica o squad."},
    "target_audience": {"type": "string", "required": True, "description": "Público-alvo ou usuários principais."},
    "expected_outputs": {"type": "list[string]", "required": True, "description": "Artefatos esperados do squad."},
    "constraints": {"type": "list[string] | object", "required": False, "description": "Limitações técnicas, legais, operacionais ou de linguagem."},
    "integrations": {"type": "list[string] | object", "required": False, "description": "Sistemas externos, APIs, repositórios ou canais de publicação."},
    "security_level": {"type": "string", "required": False, "description": "low, standard, elevated ou high."},
    "human_approval_requirements": {"type": "list[string]", "required": False, "description": "Etapas que exigem aprovação humana."},
    "success_metrics": {"type": "list[string]", "required": False, "description": "Métricas verificáveis de sucesso."},
    "budget_limit": {"type": "number | string | null", "required": False, "description": "Limite de orçamento/custo, quando informado."},
    "preferred_models": {"type": "list[string]", "required": False, "description": "Modelos de IA preferidos, quando houver fundamento."},
}

ALIASES = {
    "audience": "target_audience",
    "success_criteria": "success_metrics",
    "desired_asset": "expected_outputs",
    "budget": "budget_limit",
}
LIST_FIELDS = {"expected_outputs", "human_approval_requirements", "success_metrics", "preferred_models"}
DICT_OR_LIST_FIELDS = {"constraints", "integrations"}
SECURITY_LEVELS = {"low", "standard", "elevated", "high"}


class BriefingError(ValueError):
    """Raised when briefing parsing or validation fails with a human-readable message."""


@dataclass
class Briefing:
    project_name: str
    objective: str
    problem: str
    target_audience: str
    expected_outputs: List[str]
    constraints: Any = field(default_factory=list)
    integrations: Any = field(default_factory=list)
    security_level: str = "standard"
    human_approval_requirements: List[str] = field(default_factory=list)
    success_metrics: List[str] = field(default_factory=list)
    budget_limit: Any = None
    preferred_models: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "objective": self.objective,
            "problem": self.problem,
            "target_audience": self.target_audience,
            "expected_outputs": self.expected_outputs,
            "constraints": self.constraints,
            "integrations": self.integrations,
            "security_level": self.security_level,
            "human_approval_requirements": self.human_approval_requirements,
            "success_metrics": self.success_metrics,
            "budget_limit": self.budget_limit,
            "preferred_models": self.preferred_models,
            "warnings": self.warnings,
        }


def _detect_format(path: Path, forced_format: Optional[str]) -> str:
    if forced_format:
        return forced_format.lower()
    if path.suffix.lower() == ".json":
        return "json"
    if path.suffix.lower() in {".yaml", ".yml"}:
        return "yaml"
    return "auto"


def _load_yaml(text: str, path: Path) -> Dict[str, Any]:
    if yaml is None:
        raise BriefingError("Parser YAML real indisponível: instale PyYAML para ler briefings YAML.")
    try:
        data = yaml.safe_load(text)
    except Exception as exc:
        raise BriefingError(f"YAML inválido em {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise BriefingError(f"Briefing YAML deve ser um objeto/mapping na raiz: {path}")
    return data


def _load_json(text: str, path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(text)
    except Exception as exc:
        raise BriefingError(f"JSON inválido em {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise BriefingError(f"Briefing JSON deve ser um objeto na raiz: {path}")
    return data


def read_raw_briefing(path: str | Path, forced_format: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
    briefing_path = Path(path)
    if not briefing_path.is_file():
        raise BriefingError(f"Arquivo de briefing não encontrado: {briefing_path}")
    text = briefing_path.read_text(encoding="utf-8")
    fmt = _detect_format(briefing_path, forced_format)
    if fmt == "json":
        return _load_json(text, briefing_path), "json"
    if fmt == "yaml":
        return _load_yaml(text, briefing_path), "yaml"
    try:
        return _load_json(text, briefing_path), "json"
    except BriefingError:
        return _load_yaml(text, briefing_path), "yaml"


def _as_list(value: Any, field_name: str) -> List[str]:
    if value is None or value == "":
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (tuple, list)):
        return [str(item).strip() for item in value if str(item).strip()]
    raise BriefingError(f"Campo '{field_name}' deve ser texto ou lista de textos; recebido: {type(value).__name__}")


def _normalize(raw: Dict[str, Any], strict: bool) -> tuple[Dict[str, Any], List[str]]:
    data = dict(raw)
    warnings: List[str] = []
    for old, new in ALIASES.items():
        if old in data and new not in data:
            data[new] = data[old]
            warnings.append(f"Campo legado '{old}' normalizado para '{new}'.")
        elif old in data and new in data:
            warnings.append(f"Campo legado '{old}' ignorado porque '{new}' também foi informado.")
    if not data.get("problem") and not strict:
        objective = str(data.get("objective", "")).strip()
        data["problem"] = f"Problema a detalhar pelo responsável humano a partir do objetivo: {objective}" if objective else "Problema não informado."
        warnings.append("Campo obrigatório 'problem' não informado; criada lacuna explícita para revisão humana.")
    if not data.get("target_audience") and not strict:
        data["target_audience"] = "Público-alvo não informado"
        warnings.append("Campo obrigatório 'target_audience' não informado; marcado para revisão humana.")
    if not data.get("expected_outputs") and not strict:
        data["expected_outputs"] = ["squad.yaml", "README.md", "agents", "tasks", "workflows", "scripts", "tests", "docs"]
        warnings.append("Campo obrigatório 'expected_outputs' não informado; usados artefatos estruturais mínimos do squad.")
    for field_name in LIST_FIELDS:
        data[field_name] = _as_list(data.get(field_name), field_name)
    for field_name in DICT_OR_LIST_FIELDS:
        value = data.get(field_name, [])
        if value is None:
            value = []
        if not isinstance(value, (list, dict)):
            value = [value] if isinstance(value, str) else None
        if value is None:
            raise BriefingError(f"Campo '{field_name}' deve ser lista, objeto ou texto.")
        data[field_name] = value
    data["security_level"] = str(data.get("security_level") or "standard").strip().lower()
    if data["security_level"] not in SECURITY_LEVELS:
        raise BriefingError("Campo 'security_level' deve ser um de: low, standard, elevated, high.")
    return data, warnings


def validate_briefing(raw: Dict[str, Any], strict: bool = False) -> Briefing:
    data, warnings = _normalize(raw, strict=strict)
    missing = [name for name, spec in BRIEFING_SCHEMA.items() if spec.get("required") and not data.get(name)]
    if missing:
        raise BriefingError("Campos obrigatórios ausentes ou vazios: " + ", ".join(missing))
    if strict:
        unknown = sorted(set(data) - set(BRIEFING_SCHEMA) - set(ALIASES))
        if unknown:
            raise BriefingError("Campos não reconhecidos em modo --strict: " + ", ".join(unknown))
    for field_name in ["project_name", "objective", "problem", "target_audience"]:
        if not isinstance(data[field_name], str) or not data[field_name].strip():
            raise BriefingError(f"Campo '{field_name}' deve ser texto não vazio.")
    return Briefing(
        project_name=data["project_name"].strip(), objective=data["objective"].strip(),
        problem=data["problem"].strip(), target_audience=data["target_audience"].strip(),
        expected_outputs=data["expected_outputs"], constraints=data.get("constraints", []),
        integrations=data.get("integrations", []), security_level=data.get("security_level", "standard"),
        human_approval_requirements=data.get("human_approval_requirements", []),
        success_metrics=data.get("success_metrics", []), budget_limit=data.get("budget_limit"),
        preferred_models=data.get("preferred_models", []), warnings=warnings, raw=raw,
    )


def load_briefing(path: str | Path, strict: bool = False, forced_format: Optional[str] = None, budget_limit: Any = None) -> Briefing:
    raw, _ = read_raw_briefing(path, forced_format=forced_format)
    if budget_limit is not None:
        raw = dict(raw)
        raw["budget_limit"] = budget_limit
    return validate_briefing(raw, strict=strict)
