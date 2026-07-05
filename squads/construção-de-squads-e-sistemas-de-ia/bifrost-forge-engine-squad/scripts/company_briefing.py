#!/usr/bin/env python3
"""Frigg Company Briefing — schema e validação de briefings de EMPRESA.

Frigg, rainha de Asgard, governa a casa dos deuses. Este módulo lê o briefing de
uma empresa/organização e normaliza os campos que alimentam a forja de organograma,
cargos e governança.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

SIZES = {"small", "medium", "large"}
SECURITY_LEVELS = {"low", "standard", "elevated", "high"}

COMPANY_SCHEMA: Dict[str, Dict[str, Any]] = {
    "company_name": {"required": True, "description": "Nome da empresa/organização."},
    "mission": {"required": True, "description": "Missão em uma frase."},
    "market": {"required": True, "description": "Mercado/segmento de atuação."},
    "offer": {"required": True, "description": "Oferta/produto principal."},
    "departments": {"required": False, "description": "Lista de departamentos (opcional)."},
    "size": {"required": False, "description": "small | medium | large."},
    "constraints": {"required": False, "description": "Limitações."},
    "integrations": {"required": False, "description": "Integrações externas."},
    "security_level": {"required": False, "description": "low | standard | elevated | high."},
    "human_approval_requirements": {"required": False, "description": "Aprovações humanas."},
    "budget_limit": {"required": False, "description": "Limite de orçamento."},
    "category": {"required": False, "description": "Categoria da galeria."},
}

ALIASES = {"name": "company_name", "produto": "offer", "product": "offer", "mercado": "market", "missao": "mission"}
LIST_FIELDS = {"departments", "human_approval_requirements"}
DICT_OR_LIST_FIELDS = {"constraints", "integrations"}


class CompanyBriefingError(ValueError):
    """Erro legível de briefing de empresa."""


@dataclass
class CompanyBriefing:
    company_name: str
    mission: str
    market: str
    offer: str
    departments: List[str] = field(default_factory=list)
    size: str = "medium"
    constraints: Any = field(default_factory=list)
    integrations: Any = field(default_factory=list)
    security_level: str = "standard"
    human_approval_requirements: List[str] = field(default_factory=list)
    budget_limit: Any = None
    category: str = "Construção de Squads & Sistemas de IA"
    gaps: List[Dict[str, str]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "company_name": self.company_name, "mission": self.mission, "market": self.market,
            "offer": self.offer, "departments": self.departments, "size": self.size,
            "constraints": self.constraints, "integrations": self.integrations,
            "security_level": self.security_level,
            "human_approval_requirements": self.human_approval_requirements,
            "budget_limit": self.budget_limit, "category": self.category, "gaps": self.gaps,
        }


def _as_list(value: Any, name: str) -> List[str]:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        return [str(i).strip() for i in value if str(i).strip()]
    raise CompanyBriefingError(f"Campo '{name}' deve ser texto ou lista.")


def _read(path: Path, forced: Optional[str]) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    suffix = (forced or path.suffix.lstrip(".")).lower()
    if suffix == "json":
        return json.loads(text)
    if yaml is None:
        return json.loads(text)
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise CompanyBriefingError("Briefing de empresa deve ser um mapping na raiz.")
    return data


def validate_company_briefing(raw: Dict[str, Any], strict: bool = False) -> CompanyBriefing:
    data = dict(raw)
    for old, new in ALIASES.items():
        if old in data and new not in data:
            data[new] = data.pop(old)
    gaps: List[Dict[str, str]] = []
    missing = [k for k, s in COMPANY_SCHEMA.items() if s.get("required") and not data.get(k)]
    if missing:
        raise CompanyBriefingError("Campos obrigatórios ausentes: " + ", ".join(missing))
    for name in LIST_FIELDS:
        data[name] = _as_list(data.get(name), name)
    for name in DICT_OR_LIST_FIELDS:
        v = data.get(name, [])
        if v is None:
            v = []
        if not isinstance(v, (list, dict)):
            v = [v] if isinstance(v, str) else None
        if v is None:
            raise CompanyBriefingError(f"Campo '{name}' deve ser lista, objeto ou texto.")
        data[name] = v
    data["size"] = str(data.get("size") or "medium").strip().lower()
    if data["size"] not in SIZES:
        raise CompanyBriefingError("Campo 'size' deve ser small, medium ou large.")
    data["security_level"] = str(data.get("security_level") or "standard").strip().lower()
    if data["security_level"] not in SECURITY_LEVELS:
        raise CompanyBriefingError("Campo 'security_level' deve ser low, standard, elevated ou high.")
    if not data.get("departments"):
        gaps.append({"field": "departments", "severity": "medium", "note": "Departamentos não informados; derivados por padrão."})
    if not data.get("human_approval_requirements"):
        gaps.append({"field": "human_approval_requirements", "severity": "low", "note": "Sem aprovações humanas explícitas."})
    data.setdefault("category", "Construção de Squads & Sistemas de IA")
    return CompanyBriefing(
        company_name=str(data["company_name"]).strip(), mission=str(data["mission"]).strip(),
        market=str(data["market"]).strip(), offer=str(data["offer"]).strip(),
        departments=data["departments"], size=data["size"], constraints=data.get("constraints", []),
        integrations=data.get("integrations", []), security_level=data["security_level"],
        human_approval_requirements=data.get("human_approval_requirements", []),
        budget_limit=data.get("budget_limit"), category=str(data.get("category")).strip(),
        gaps=gaps, raw=raw,
    )


def load_company_briefing(path: str | Path, strict: bool = False, forced_format: Optional[str] = None) -> CompanyBriefing:
    p = Path(path)
    if not p.is_file():
        raise CompanyBriefingError(f"Briefing não encontrado: {p}")
    return validate_company_briefing(_read(p, forced_format), strict=strict)


def main() -> int:
    ap = argparse.ArgumentParser(description="Valida um briefing de empresa.")
    ap.add_argument("--briefing", required=True)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    try:
        b = load_company_briefing(args.briefing, strict=args.strict)
    except CompanyBriefingError as exc:
        print(f"Erro: {exc}")
        return 2
    print(json.dumps({"ok": True, "company": b.company_name, "size": b.size, "gaps": b.gaps}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
