#!/usr/bin/env python3
"""Motor de memória e autoaprendizado do AETHER OS (PRD §21).

Lições com proveniência, escopo, TTL e status governado:
observation -> candidate_rule -> approved_rule (promoção só por fluxo
humano/política). Dedupe determinístico; expiração por TTL; consulta por
escopo. Acervo em JSONL local (local-first).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ENGINE_ID = "aether-memory-engine@1.0.0"
VALID_TYPES = ("observation", "candidate_rule", "approved_rule")
VALID_STATUS = ("pending_review", "approved", "rejected", "revoked", "expired")


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def now_iso(now: str | None = None) -> str:
    """Relógio injetável (NFR-25): passe --now para replay determinístico."""
    return now or datetime.now(timezone.utc).isoformat()


def lesson_fingerprint(lesson: dict) -> str:
    basis = canonical({"scope": lesson.get("scope", ""),
                       "statement": lesson.get("statement", "").strip().lower()})
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def load(store: Path) -> list[dict]:
    if not store.exists():
        return []
    return [json.loads(line) for line in
            store.read_text(encoding="utf-8").splitlines() if line.strip()]


def save(store: Path, lessons: list[dict]) -> None:
    store.parent.mkdir(parents=True, exist_ok=True)
    store.write_text("".join(canonical(l) + "\n" for l in lessons),
                     encoding="utf-8")


def extract(run: dict, now: str | None = None) -> dict:
    """Extrai uma lição candidata estruturada de um run concluído."""
    if run.get("status") not in ("completed", "partial", "failed"):
        raise ValueError("lição só nasce de run finalizado")
    statement = run.get("lesson_statement", "").strip()
    if not statement:
        raise ValueError("run sem lesson_statement: registre descarte explícito")
    lesson = {
        "lesson_id": f"lesson_{lesson_fingerprint({'scope': run.get('scope', ''), 'statement': statement})}",
        "type": "candidate_rule" if run.get("status") == "completed" else "observation",
        "scope": run.get("scope", "general"),
        "statement": statement,
        "evidence": run.get("evidence", [run.get("run_id", "")]),
        "confidence": float(run.get("confidence", 0.5)),
        "status": "pending_review",
        "created_at": now_iso(now),
        "expires_at": run.get("expires_at"),
        "provenance": {"run_id": run.get("run_id", ""),
                       "extracted_by": ENGINE_ID},
    }
    return lesson


def add(store: Path, lesson: dict, now: str | None = None) -> dict:
    """Adiciona com dedupe determinístico (parecer MNÉME é etapa anterior)."""
    lessons = load(store)
    fp = lesson_fingerprint(lesson)
    for existing in lessons:
        if lesson_fingerprint(existing) == fp:
            return {"action": "duplicate", "duplicate_of": existing["lesson_id"],
                    "stored": False}
    lessons.append(lesson)
    save(store, lessons)
    return {"action": "stored", "lesson_id": lesson["lesson_id"], "stored": True}


def promote(store: Path, lesson_id: str, approver: str) -> dict:
    """Promoção a approved_rule — decisão humana/política registrada."""
    lessons = load(store)
    for lesson in lessons:
        if lesson["lesson_id"] == lesson_id:
            lesson["type"] = "approved_rule"
            lesson["status"] = "approved"
            lesson["approved_by"] = approver
            save(store, lessons)
            return {"action": "promoted", "lesson_id": lesson_id,
                    "approved_by": approver}
    return {"action": "not_found", "lesson_id": lesson_id}


def expire(store: Path, now: str | None = None) -> dict:
    """Expira lições vencidas (TTL) — regra vencida não influencia decisão."""
    reference = now_iso(now)
    lessons, expired = load(store), []
    for lesson in lessons:
        exp = lesson.get("expires_at")
        if exp and lesson["status"] != "expired" and exp <= reference:
            lesson["status"] = "expired"
            expired.append(lesson["lesson_id"])
    save(store, lessons)
    return {"action": "expired", "count": len(expired), "lessons": expired}


def query(store: Path, scope: str, now: str | None = None) -> dict:
    """Consulta por escopo — só approved_rule vale para decisão automática."""
    reference = now_iso(now)
    binding, informative = [], []
    for lesson in load(store):
        if lesson.get("status") in ("rejected", "revoked", "expired"):
            continue
        exp = lesson.get("expires_at")
        if exp and exp <= reference:
            continue
        if scope not in (lesson.get("scope", ""), "all"):
            if lesson.get("scope") != "general":
                continue
        target = binding if (lesson["type"] == "approved_rule"
                             and lesson["status"] == "approved") else informative
        target.append(lesson)
    return {"scope": scope, "binding_rules": binding,
            "informative": informative,
            "note": "informative nunca influencia decisão automática de alto impacto"}


def main() -> int:
    ap = argparse.ArgumentParser(description="Memória/Autoaprendizado AETHER")
    ap.add_argument("--store", default="memory/lessons.jsonl")
    ap.add_argument("--now", help="relógio injetável (ISO-8601) para replay")
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract"); e.add_argument("--run", required=True)
    a = sub.add_parser("add"); a.add_argument("--lesson", required=True)
    p = sub.add_parser("promote"); p.add_argument("--lesson-id", required=True)
    p.add_argument("--approver", required=True)
    sub.add_parser("expire")
    q = sub.add_parser("query"); q.add_argument("--scope", required=True)
    args = ap.parse_args()
    store = Path(args.store)
    if args.cmd == "extract":
        run = json.loads(Path(args.run).read_text(encoding="utf-8"))
        print(canonical(extract(run, args.now)))
    elif args.cmd == "add":
        lesson = json.loads(Path(args.lesson).read_text(encoding="utf-8"))
        print(canonical(add(store, lesson, args.now)))
    elif args.cmd == "promote":
        print(canonical(promote(store, args.lesson_id, args.approver)))
    elif args.cmd == "expire":
        print(canonical(expire(store, args.now)))
    else:
        print(canonical(query(store, args.scope, args.now)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
