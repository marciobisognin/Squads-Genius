#!/usr/bin/env python3
"""Motor de Oikos do AETHER OS (aether.oikos/v1) — PRD v1.3, §17.5-17.9.

Organizações persistentes sob o invariante único: o oikos NÃO executa nada;
agenda, contextualiza e enfileira runs normais. Este motor valida manifesto,
calcula ticks devidos do pulso (relógio injetável, NFR-25), roteia inbox pelo
organograma com escalada e governa o ciclo de vida. Stdlib puro.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ENGINE_ID = "aether-oikos-engine@1.0.0"

LIFECYCLE = {"draft": {"active"}, "active": {"paused", "archived"},
             "paused": {"active", "archived"}, "archived": set()}
RISK_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def load_manifest(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("manifesto deve ser um mapping")
    return data


def _cron_field_matches(field: str, value: int, lo: int, hi: int) -> bool:
    """Matcher mínimo de campo cron: *, n, a-b, a,b,c e */step."""
    for part in field.split(","):
        part = part.strip()
        step = 1
        if "/" in part:
            part, step_s = part.split("/", 1)
            step = int(step_s)
        if part in ("*", ""):
            candidates = range(lo, hi + 1, step)
        elif "-" in part:
            a, b = part.split("-", 1)
            candidates = range(int(a), int(b) + 1, step)
        else:
            candidates = [int(part)] if step == 1 else \
                range(int(part), hi + 1, step)
        if value in candidates:
            return True
    return False


def cron_matches(expr: str, moment: datetime) -> bool:
    fields = expr.split()
    if len(fields) != 5:
        raise ValueError(f"cron inválido: {expr!r}")
    minute, hour, dom, month, dow = fields
    return (_cron_field_matches(minute, moment.minute, 0, 59)
            and _cron_field_matches(hour, moment.hour, 0, 23)
            and _cron_field_matches(dom, moment.day, 1, 31)
            and _cron_field_matches(month, moment.month, 1, 12)
            and _cron_field_matches(dow, moment.isoweekday() % 7, 0, 6))


def validate(manifest: dict) -> dict:
    """Valida o manifesto aether.oikos/v1 — falha bloqueia (falha segura)."""
    issues: list[str] = []
    for field in ("schema_version", "id", "name", "version", "mission",
                  "org_chart", "positions"):
        if field not in manifest:
            issues.append(f"campo obrigatório ausente: {field}")
    if manifest.get("schema_version") not in (None, "aether.oikos/v1"):
        issues.append("schema_version deve ser aether.oikos/v1")

    chart = manifest.get("org_chart", []) or []
    names = {entry.get("position") for entry in chart}
    roots = [e for e in chart if e.get("reports_to") is None]
    if chart and not roots:
        issues.append("organograma sem raiz (reports_to: null)")
    for entry in chart:
        boss = entry.get("reports_to")
        if boss is not None and boss not in names:
            issues.append(f"reports_to inexistente: {boss}")
    # aciclicidade da cadeia de subordinação
    for entry in chart:
        seen, current = set(), entry.get("position")
        chain = {e.get("position"): e.get("reports_to") for e in chart}
        while current is not None:
            if current in seen:
                issues.append(f"ciclo no organograma envolvendo: {current}")
                break
            seen.add(current)
            current = chain.get(current)

    for pos in manifest.get("positions", []) or []:
        ceiling = pos.get("autonomy_ceiling", "medium")
        if ceiling not in RISK_RANK:
            issues.append(f"autonomy_ceiling inválido em {pos.get('id')}: {ceiling}")
        if not pos.get("mandate"):
            issues.append(f"cargo sem mandato: {pos.get('id')}")

    process_ids = {p.get("id") for p in manifest.get("processes", []) or []}
    for entry in manifest.get("pulse", []) or []:
        try:
            cron_matches(entry.get("cron", ""), datetime(2026, 1, 5, 7, 0))
        except Exception as exc:
            issues.append(f"cron inválido no pulso: {exc}")
        if entry.get("process") not in process_ids:
            issues.append(f"pulso aponta processo inexistente: {entry.get('process')}")

    for level in manifest.get("policies", {}).get("unattended_allowed", []) or []:
        if level not in RISK_RANK:
            issues.append(f"unattended_allowed com nível inválido: {level}")

    return {"schema_version": "aether.oikos-validation/v1",
            "oikos": manifest.get("id", ""), "valid": not issues,
            "issues": issues, "validated_by": ENGINE_ID}


def pulse_due(manifest: dict, now_iso: str) -> dict:
    """Ticks devidos no minuto de referência — determinístico, relógio injetado."""
    moment = datetime.fromisoformat(now_iso)
    ticks = []
    for entry in manifest.get("pulse", []) or []:
        due = cron_matches(entry["cron"], moment)
        ticks.append({"cron": entry["cron"], "process": entry["process"],
                      "due": due,
                      "tick": {"schema_version": "aether.pulse-tick/v1",
                               "oikos": manifest.get("id", ""),
                               "process": entry["process"],
                               "at": now_iso,
                               "status": "run_opened" if due else "not_due"}
                      if True else None})
    return {"schema_version": "aether.pulse-report/v1",
            "oikos": manifest.get("id", ""), "now": now_iso,
            "ticks": ticks, "decided_by": ENGINE_ID}


def route(manifest: dict, item: dict) -> dict:
    """Roteia um InboxItem ao cargo pelo organograma; sem rota, escala."""
    label = item.get("route", "")
    chart = manifest.get("org_chart", []) or []
    matches = [e["position"] for e in chart if label in (e.get("routes") or [])]
    if len(matches) == 1:
        return {"schema_version": "aether.inbox-routing/v1",
                "item": item.get("id", ""), "route": label,
                "position": matches[0], "escalated": False,
                "decided_by": ENGINE_ID}
    roots = [e["position"] for e in chart if e.get("reports_to") is None]
    return {"schema_version": "aether.inbox-routing/v1",
            "item": item.get("id", ""), "route": label,
            "position": roots[0] if roots else None,
            "escalated": True,
            "reason": "rota ausente" if not matches else "rota em conflito",
            "next": "gate humano se a cadeia não resolver",
            "decided_by": ENGINE_ID}


def autonomy_check(manifest: dict, position_id: str, risk_tier: str) -> dict:
    """Teto de autonomia do cargo: risco acima do teto escala pela cadeia."""
    positions = {p["id"]: p for p in manifest.get("positions", []) or []}
    pos = positions.get(position_id)
    if pos is None:
        return {"allowed": False, "reason": f"cargo inexistente: {position_id}",
                "decided_by": ENGINE_ID}
    ceiling = pos.get("autonomy_ceiling", "medium")
    allowed = RISK_RANK[risk_tier] <= RISK_RANK[ceiling]
    return {"schema_version": "aether.autonomy-check/v1",
            "position": position_id, "risk_tier": risk_tier,
            "autonomy_ceiling": ceiling, "allowed": allowed,
            "action": None if allowed else "escalate_chain_then_human_gate",
            "decided_by": ENGINE_ID}


def transition(state: str, to: str) -> dict:
    ok = to in LIFECYCLE.get(state, set())
    return {"schema_version": "aether.oikos-lifecycle/v1",
            "from": state, "to": to, "valid": ok,
            "note": ("arquivar congela pulso/inbox e preserva a trilha"
                     if ok and to == "archived" else
                     None if ok else f"transição inválida: {state} -> {to}"),
            "decided_by": ENGINE_ID}


def main() -> int:
    ap = argparse.ArgumentParser(description="Motor de Oikos AETHER")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("--manifest", required=True)
    p = sub.add_parser("pulse-due"); p.add_argument("--manifest", required=True)
    p.add_argument("--now", required=True, help="ISO-8601 (relógio injetável)")
    r = sub.add_parser("route"); r.add_argument("--manifest", required=True)
    r.add_argument("--item", required=True)
    a = sub.add_parser("autonomy"); a.add_argument("--manifest", required=True)
    a.add_argument("--position", required=True); a.add_argument("--tier", required=True)
    t = sub.add_parser("transition"); t.add_argument("--state", required=True)
    t.add_argument("--to", required=True)
    args = ap.parse_args()
    if args.cmd == "transition":
        result = transition(args.state, args.to)
        print(canonical(result))
        return 0 if result["valid"] else 1
    manifest = load_manifest(Path(args.manifest))
    if args.cmd == "validate":
        result = validate(manifest)
        print(canonical(result))
        return 0 if result["valid"] else 1
    if args.cmd == "pulse-due":
        print(canonical(pulse_due(manifest, args.now)))
        return 0
    if args.cmd == "route":
        item = json.loads(Path(args.item).read_text(encoding="utf-8"))
        print(canonical(route(manifest, item)))
        return 0
    result = autonomy_check(manifest, args.position, args.tier)
    print(canonical(result))
    return 0 if result["allowed"] else 1


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
