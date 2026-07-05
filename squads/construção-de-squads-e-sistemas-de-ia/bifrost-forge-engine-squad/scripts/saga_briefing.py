#!/usr/bin/env python3
"""Mímir Briefing Oracle — parsing, schema e validação de briefings.

Evolui o parser de referência com:
  * lacunas graduadas por severidade (blocker / high / medium / low);
  * aliases ampliados e normalização determinística;
  * export de JSON Schema (`--schema`) para integração externa.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:  # PyYAML é opcional; JSON sempre funciona.
    import yaml
except Exception:  # pragma: no cover
    yaml = None

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

BRIEFING_SCHEMA: Dict[str, Dict[str, Any]] = {
    "project_name": {"type": "string", "required": True, "description": "Nome humano do projeto/squad."},
    "objective": {"type": "string", "required": True, "description": "Objetivo principal do squad."},
    "problem": {"type": "string", "required": True, "description": "Problema real que justifica o squad."},
    "target_audience": {"type": "string", "required": True, "description": "Público-alvo/usuários principais."},
    "expected_outputs": {"type": "list[string]", "required": True, "description": "Artefatos esperados."},
    "constraints": {"type": "list[string] | object", "required": False, "description": "Limitações."},
    "integrations": {"type": "list[string] | object", "required": False, "description": "Integrações externas."},
    "security_level": {"type": "string", "required": False, "description": "low, standard, elevated ou high."},
    "human_approval_requirements": {"type": "list[string]", "required": False, "description": "Aprovações humanas."},
    "success_metrics": {"type": "list[string]", "required": False, "description": "Métricas verificáveis."},
    "budget_limit": {"type": "number | string | null", "required": False, "description": "Limite de custo."},
    "preferred_models": {"type": "list[string]", "required": False, "description": "Modelos de IA preferidos."},
    "category": {"type": "string", "required": False, "description": "Categoria da galeria."},
}

ALIASES = {
    "audience": "target_audience",
    "publico": "target_audience",
    "public_target": "target_audience",
    "success_criteria": "success_metrics",
    "metrics": "success_metrics",
    "desired_asset": "expected_outputs",
    "outputs": "expected_outputs",
    "budget": "budget_limit",
    "goal": "objective",
    "models": "preferred_models",
}
LIST_FIELDS = {"expected_outputs", "human_approval_requirements", "success_metrics", "preferred_models"}
DICT_OR_LIST_FIELDS = {"constraints", "integrations"}
SECURITY_LEVELS = {"low", "standard", "elevated", "high"}


class BriefingError(ValueError):
    """Erro legível de parsing/validação de briefing."""


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
    category: str = "Construção de Squads & Sistemas de IA"
    gaps: List[Dict[str, str]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name, "objective": self.objective, "problem": self.problem,
            "target_audience": self.target_audience, "expected_outputs": self.expected_outputs,
            "constraints": self.constraints, "integrations": self.integrations,
            "security_level": self.security_level,
            "human_approval_requirements": self.human_approval_requirements,
            "success_metrics": self.success_metrics, "budget_limit": self.budget_limit,
            "preferred_models": self.preferred_models, "category": self.category,
            "gaps": self.gaps, "warnings": self.warnings,
        }


def _detect_format(path: Path, forced: Optional[str]) -> str:
    if forced:
        return forced.lower()
    if path.suffix.lower() == ".json":
        return "json"
    if path.suffix.lower() in {".yaml", ".yml"}:
        return "yaml"
    return "auto"


def _load_yaml(text: str, path: Path) -> Dict[str, Any]:
    if yaml is None:
        raise BriefingError("PyYAML indisponível: instale PyYAML para ler briefings YAML.")
    try:
        data = yaml.safe_load(text)
    except Exception as exc:  # pragma: no cover
        raise BriefingError(f"YAML inválido em {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise BriefingError(f"Briefing YAML deve ser um mapping na raiz: {path}")
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
    p = Path(path)
    if not p.is_file():
        raise BriefingError(f"Arquivo de briefing não encontrado: {p}")
    text = p.read_text(encoding="utf-8")
    fmt = _detect_format(p, forced_format)
    if fmt == "json":
        return _load_json(text, p), "json"
    if fmt == "yaml":
        return _load_yaml(text, p), "yaml"
    try:
        return _load_json(text, p), "json"
    except BriefingError:
        return _load_yaml(text, p), "yaml"


def _as_list(value: Any, field_name: str) -> List[str]:
    if value is None or value == "":
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (tuple, list)):
        return [str(item).strip() for item in value if str(item).strip()]
    raise BriefingError(f"Campo '{field_name}' deve ser texto ou lista de textos; recebido: {type(value).__name__}")


def _normalize(raw: Dict[str, Any], strict: bool) -> Tuple[Dict[str, Any], List[str], List[Dict[str, str]]]:
    data = dict(raw)
    warnings: List[str] = []
    gaps: List[Dict[str, str]] = []
    for old, new in ALIASES.items():
        if old in data and new not in data:
            data[new] = data.pop(old)
            warnings.append(f"Campo legado '{old}' normalizado para '{new}'.")
        elif old in data and new in data:
            data.pop(old)
            warnings.append(f"Campo legado '{old}' ignorado porque '{new}' já foi informado.")

    if not data.get("problem"):
        if strict:
            raise BriefingError("Campo obrigatório 'problem' ausente em modo --strict.")
        objective = str(data.get("objective", "")).strip()
        data["problem"] = f"Problema a detalhar pelo responsável humano a partir do objetivo: {objective}" if objective else "Problema não informado."
        gaps.append({"field": "problem", "severity": "high", "note": "Problema não informado; lacuna explícita para revisão humana."})
    if not data.get("target_audience"):
        if strict:
            raise BriefingError("Campo obrigatório 'target_audience' ausente em modo --strict.")
        data["target_audience"] = "Público-alvo não informado"
        gaps.append({"field": "target_audience", "severity": "high", "note": "Público-alvo não informado."})
    if not data.get("expected_outputs"):
        if strict:
            raise BriefingError("Campo obrigatório 'expected_outputs' ausente em modo --strict.")
        data["expected_outputs"] = ["squad.yaml", "README.md", "agents", "tasks", "workflows", "scripts", "tests", "docs"]
        gaps.append({"field": "expected_outputs", "severity": "medium", "note": "Outputs não informados; usados artefatos estruturais mínimos."})

    for name in LIST_FIELDS:
        data[name] = _as_list(data.get(name), name)
    for name in DICT_OR_LIST_FIELDS:
        value = data.get(name, [])
        if value is None:
            value = []
        if not isinstance(value, (list, dict)):
            value = [value] if isinstance(value, str) else None
        if value is None:
            raise BriefingError(f"Campo '{name}' deve ser lista, objeto ou texto.")
        data[name] = value

    data["security_level"] = str(data.get("security_level") or "standard").strip().lower()
    if data["security_level"] not in SECURITY_LEVELS:
        raise BriefingError("Campo 'security_level' deve ser um de: low, standard, elevated, high.")

    if not data.get("success_metrics"):
        gaps.append({"field": "success_metrics", "severity": "medium", "note": "Sem métricas de sucesso mensuráveis."})
    if not data.get("human_approval_requirements"):
        gaps.append({"field": "human_approval_requirements", "severity": "low", "note": "Sem pontos de aprovação humana explícitos."})
    if data["security_level"] in {"elevated", "high"} and not data.get("human_approval_requirements"):
        gaps.append({"field": "human_approval_requirements", "severity": "blocker", "note": "Segurança elevada sem aprovação humana explícita."})
    data.setdefault("category", "Construção de Squads & Sistemas de IA")
    return data, warnings, gaps


def validate_briefing(raw: Dict[str, Any], strict: bool = False) -> Briefing:
    data, warnings, gaps = _normalize(raw, strict=strict)
    missing = [name for name, spec in BRIEFING_SCHEMA.items() if spec.get("required") and not data.get(name)]
    if missing:
        raise BriefingError("Campos obrigatórios ausentes ou vazios: " + ", ".join(missing))
    if strict:
        unknown = sorted(set(data) - set(BRIEFING_SCHEMA) - set(ALIASES) - {"gaps", "warnings"})
        if unknown:
            raise BriefingError("Campos não reconhecidos em modo --strict: " + ", ".join(unknown))
    for name in ("project_name", "objective", "problem", "target_audience"):
        if not isinstance(data[name], str) or not data[name].strip():
            raise BriefingError(f"Campo '{name}' deve ser texto não vazio.")
    return Briefing(
        project_name=data["project_name"].strip(), objective=data["objective"].strip(),
        problem=data["problem"].strip(), target_audience=data["target_audience"].strip(),
        expected_outputs=data["expected_outputs"], constraints=data.get("constraints", []),
        integrations=data.get("integrations", []), security_level=data.get("security_level", "standard"),
        human_approval_requirements=data.get("human_approval_requirements", []),
        success_metrics=data.get("success_metrics", []), budget_limit=data.get("budget_limit"),
        preferred_models=data.get("preferred_models", []), category=str(data.get("category")).strip(),
        gaps=gaps, warnings=warnings, raw=raw,
    )


def load_briefing(path: str | Path, strict: bool = False, forced_format: Optional[str] = None, budget_limit: Any = None) -> Briefing:
    raw, _ = read_raw_briefing(path, forced_format=forced_format)
    if budget_limit is not None:
        raw = dict(raw)
        raw["budget_limit"] = budget_limit
    return validate_briefing(raw, strict=strict)


def export_json_schema() -> Dict[str, Any]:
    props = {name: {"type": "string", "description": spec["description"]} for name, spec in BRIEFING_SCHEMA.items()}
    required = [name for name, spec in BRIEFING_SCHEMA.items() if spec.get("required")]
    return {"$schema": "http://json-schema.org/draft-07/schema#", "title": "Bifröst Briefing", "type": "object", "required": required, "properties": props}


def main() -> int:
    ap = argparse.ArgumentParser(description="Valida ou inspeciona um briefing do Bifröst Forge.")
    ap.add_argument("--briefing", help="Arquivo de briefing YAML/JSON a validar.")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--schema", action="store_true", help="Imprime o JSON Schema do briefing.")
    args = ap.parse_args()
    if args.schema:
        print(json.dumps(export_json_schema(), ensure_ascii=False, indent=2))
        return 0
    if not args.briefing:
        ap.error("informe --briefing ou --schema")
    try:
        briefing = load_briefing(args.briefing, strict=args.strict)
    except BriefingError as exc:
        print(f"Erro de briefing: {exc}")
        return 2
    print(json.dumps({"ok": True, "project": briefing.project_name, "gaps": briefing.gaps, "warnings": briefing.warnings}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
