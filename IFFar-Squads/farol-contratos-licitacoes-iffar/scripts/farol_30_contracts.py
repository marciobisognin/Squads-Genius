#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

ATTRIBUTE_PATTERNS = {
    "dimensao": ["mm", "cm", "m", "metro", "metros"],
    "capacidade": ["ml", "l", "litro", "litros"],
    "material": ["aço", "aco", "inox", "alumínio", "aluminio", "plástico", "plastico", "polipropileno", "vidro"],
    "embalagem": ["caixa", "pacote", "fardo", "frasco", "galão", "embalagem", "kit"],
    "garantia": ["garantia"],
    "norma_tecnica": ["abnt", "inmetro", "nbr"],
}
RESTRICTIVE_TERMS = ["marca", "modelo exclusivo", "fabricação nacional", "nacional"]


def normalize(text: Any) -> str:
    return " ".join(str(text or "").lower().split())


def sha256_obj(obj: Any) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_yaml(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if yaml:
        return yaml.safe_load(text)
    return json.loads(text)


def extract_attributes(description: str) -> dict[str, list[str]]:
    d = normalize(description)
    attrs: dict[str, list[str]] = {}
    for name, terms in ATTRIBUTE_PATTERNS.items():
        hits = [term for term in terms if term in d]
        if hits:
            attrs[name] = sorted(set(hits))
    numbers = [token for token in d.replace("x", " x ").split() if any(ch.isdigit() for ch in token)]
    if numbers:
        attrs["valores_numericos"] = numbers
    return attrs


def evaluate_specification(description: str, unidade: str = "", codigo: str = "") -> dict[str, Any]:
    d = normalize(description)
    attrs = extract_attributes(description)
    findings = []
    if len(d) < 45:
        findings.append({"classification": "suspeita", "risk_level": "alto", "category": "descrição", "message": "Descrição curta; verificar suficiência técnica no contexto do item."})
    if not attrs.get("valores_numericos"):
        findings.append({"classification": "depende_justificativa", "risk_level": "médio", "category": "descrição", "message": "Descrição sem medida, capacidade ou dimensão numérica; confirmar se o objeto exige atributo objetivo."})
    for term in RESTRICTIVE_TERMS:
        if term in d and "não será aceita indicação de marca" not in d:
            findings.append({"classification": "depende_justificativa", "risk_level": "alto", "category": "descrição", "message": f"Termo potencialmente restritivo: {term}."})
    u = normalize(unidade)
    if u in {"unidade", "und", "un"} and attrs.get("embalagem"):
        findings.append({"classification": "suspeita", "risk_level": "médio", "category": "unidade", "message": "Descrição menciona embalagem, mas unidade de fornecimento está como unidade."})
    return {"codigo": codigo, "attributes": attrs, "findings": findings, "human_review_required": any(f["risk_level"] in {"alto", "crítico"} for f in findings)}


def robust_stats(values: list[float]) -> dict[str, Any]:
    vals = sorted(v for v in values if v is not None and v > 0)
    if not vals:
        return {"n": 0, "quality_score": 0.0}
    med = statistics.median(vals)
    mean = statistics.fmean(vals)
    q1, q3 = (statistics.quantiles(vals, n=4, method="inclusive")[0], statistics.quantiles(vals, n=4, method="inclusive")[2]) if len(vals) >= 4 else (med, med)
    iqr = q3 - q1
    filtered = [v for v in vals if iqr == 0 or (q1 - 1.5 * iqr) <= v <= (q3 + 1.5 * iqr)]
    dispersion = (iqr / med) if med else 0
    quality = min(1.0, 0.25 + 0.1 * len(filtered) + max(0.0, 0.35 - min(dispersion, 0.35)))
    return {"n": len(vals), "n_valid": len(filtered), "min": min(vals), "max": max(vals), "mean": mean, "median": med, "q1": q1, "q3": q3, "iqr": iqr, "quality_score": round(quality, 3)}


def build_price_evidence(samples: list[dict[str, Any]], parameters: dict[str, Any] | None = None) -> dict[str, Any]:
    parameters = parameters or {}
    values = [float(s["price"]) for s in samples if s.get("comparable", True) and s.get("price") is not None]
    stats = robust_stats(values)
    raw_hash = sha256_obj({"samples": samples, "parameters": parameters})
    return {"evidence_id": raw_hash[:16], "source": parameters.get("source", "multiple_authorized_sources"), "collected_at": datetime.now(timezone.utc).isoformat(), "parameters": parameters, "raw_hash": raw_hash, "stats": stats, "quality_score": stats.get("quality_score", 0.0), "human_review_required": stats.get("quality_score", 0.0) < 0.75}


def forecast_baseline(history: list[dict[str, Any]]) -> dict[str, Any]:
    values = [float(row["quantity"]) for row in history if row.get("quantity") is not None]
    if not values:
        return {"status": "insufficient_history", "human_review_required": True}
    med = statistics.median(values)
    mad = statistics.median([abs(v - med) for v in values]) if len(values) > 1 else 0
    lower = max(0, med - 1.4826 * mad)
    upper = med + 1.4826 * mad
    return {"status": "baseline", "n": len(values), "central_value": med, "probable_interval": [round(lower, 3), round(upper, 3)], "model_quality": "baseline_only" if len(values) < 6 else "usable_baseline", "human_review_required": True}


def validate_contracts(root: Path) -> dict[str, Any]:
    issues = []
    agent_fields = {"id", "name", "role", "objective", "responsibilities", "non_responsibilities", "input_schema", "output_schema", "allowed_tools", "denied_tools", "autonomy_level", "trust_policy", "memory_policy", "escalation_policy", "quality_criteria", "handoff_contract"}
    for path in (root / "agents").glob("*.yaml"):
        data = load_yaml(path)
        missing = sorted(agent_fields - set(data or {}))
        if missing:
            issues.append(f"{path.relative_to(root)} sem campos: {', '.join(missing)}")
    workflow = load_yaml(root / "workflows" / "farol-30-procurement-intelligence.yaml")
    for step in workflow.get("steps", []):
        for field in ["id", "agent", "depends_on", "timeout", "retry_policy", "human_approval"]:
            if field not in step:
                issues.append(f"workflow step {step.get('id')} sem {field}")
    rules = load_yaml(root / "references" / "normative_rules.yaml")
    for rule in rules.get("rules", []):
        for field in ["id", "source", "article", "scope", "requirement", "official_source", "status", "validated_by"]:
            if field not in rule:
                issues.append(f"normative rule {rule.get('id')} sem {field}")
    for rel in ["schemas/finding.schema.json", "schemas/evidence.schema.json", "schemas/case.schema.json"]:
        if not (root / rel).is_file():
            issues.append(f"schema ausente: {rel}")
    return {"go_no_go": "go" if not issues else "no-go", "issues": issues}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Contratos e motores Farol 3.0")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("validate-contracts"); p.add_argument("--root", default=".")
    p = sub.add_parser("evaluate-spec"); p.add_argument("--descricao", required=True); p.add_argument("--unidade", default=""); p.add_argument("--codigo", default="")
    p = sub.add_parser("price-evidence"); p.add_argument("--samples", required=True); p.add_argument("--source", default="manual")
    p = sub.add_parser("forecast"); p.add_argument("--history", required=True)
    args = parser.parse_args(argv)
    if args.cmd == "validate-contracts":
        result = validate_contracts(Path(args.root).resolve())
    elif args.cmd == "evaluate-spec":
        result = evaluate_specification(args.descricao, args.unidade, args.codigo)
    elif args.cmd == "price-evidence":
        result = build_price_evidence(json.loads(Path(args.samples).read_text(encoding="utf-8")), {"source": args.source})
    else:
        result = forecast_baseline(json.loads(Path(args.history).read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("go_no_go", "go") == "go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
