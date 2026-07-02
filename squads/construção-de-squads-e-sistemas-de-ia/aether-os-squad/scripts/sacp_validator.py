#!/usr/bin/env python3
"""Validador de handoffs SACP do AETHER OS (aether.handoff/v1).

Toda passagem de trabalho é tipada, rastreável e verificável: schema,
integridade SHA-256, classe de dado e sanitização anti-injeção. Handoff
reprovado vai a dead-letter, nunca desaparece. PRD v1.2, Seção 15.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ENGINE_ID = "sacp-validator@1.0.0"

REQUIRED_FIELDS = ("schema_version", "handoff_id", "run_id", "from", "to",
                   "contract", "payload_ref", "data_classification",
                   "provenance", "integrity")
DATA_CLASSES = ("public", "internal", "confidential", "restricted")

# Padrões conhecidos de injeção: tentativa de sobrescrever papel, revelar
# prompt de sistema ou disparar ferramenta a partir de payload (dado).
INJECTION_PATTERNS = [
    re.compile(r"(?i)ignore (all )?(previous|prior) instructions"),
    re.compile(r"(?i)you are now (the )?(system|admin|root)"),
    re.compile(r"(?i)reveal (your )?(system )?prompt"),
    re.compile(r"(?i)disregard (your )?(rules|policies|guardrails)"),
    re.compile(r"(?i)execute (this|the following) (tool|command) without"),
]


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def sanitize_scan(text: str) -> list[str]:
    return [p.pattern for p in INJECTION_PATTERNS if p.search(text)]


def validate(envelope: dict, payload_text: str | None = None) -> dict:
    """Valida um envelope de handoff; falha bloqueia a etapa (falha segura)."""
    issues: list[dict] = []

    for field in REQUIRED_FIELDS:
        if field not in envelope:
            issues.append({"class": "contract_violation",
                           "detail": f"campo obrigatório ausente: {field}"})
    contract = envelope.get("contract", {})
    if contract and not (contract.get("input_schema") and contract.get("output_schema")):
        issues.append({"class": "contract_violation",
                       "detail": "contrato sem input_schema/output_schema"})
    if envelope.get("data_classification") not in DATA_CLASSES:
        issues.append({"class": "contract_violation",
                       "detail": "data_classification inválida"})
    if payload_text is not None:
        declared = (envelope.get("integrity") or {}).get("sha256")
        actual = hashlib.sha256(payload_text.encode("utf-8")).hexdigest()
        if declared and declared != actual:
            issues.append({"class": "integrity_error",
                           "detail": f"sha256 divergente: {declared[:12]}… != {actual[:12]}…"})
        hits = sanitize_scan(payload_text)
        if hits:
            issues.append({"class": "injection_suspected",
                           "detail": f"padrões: {hits}"})
    unverified = [a for a in envelope.get("assertions", [])
                  if not a.get("verified", False)]
    verdict = "accepted" if not issues else "dead_letter"
    return {
        "schema_version": "aether.handoff-validation/v1",
        "handoff_id": envelope.get("handoff_id", ""),
        "run_id": envelope.get("run_id", ""),
        "verdict": verdict,
        "issues": issues,
        "unverified_assertions": len(unverified),
        "note": ("asserções não verificadas não podem virar premissa automática"
                 if unverified else ""),
        "validated_by": ENGINE_ID,
    }


def to_dead_letter(envelope: dict, validation: dict, dl_path: Path,
                   ttl_hours: int = 24) -> None:
    """Handoff reprovado vai à fila de dead-letter com envelope e motivo."""
    record = {"envelope": envelope, "validation": validation,
              "ttl_hours": ttl_hours, "status": "quarantined"}
    with dl_path.open("a", encoding="utf-8") as fh:
        fh.write(canonical(record) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validador SACP AETHER")
    ap.add_argument("--envelope", required=True, help="JSON do handoff")
    ap.add_argument("--payload", help="arquivo do payload para hash/sanitização")
    ap.add_argument("--dead-letter", default="dead_letter.jsonl")
    args = ap.parse_args()
    envelope = json.loads(Path(args.envelope).read_text(encoding="utf-8"))
    payload_text = (Path(args.payload).read_text(encoding="utf-8", errors="ignore")
                    if args.payload else None)
    result = validate(envelope, payload_text)
    if result["verdict"] == "dead_letter":
        to_dead_letter(envelope, result, Path(args.dead_letter))
    print(canonical(result))
    return 0 if result["verdict"] == "accepted" else 7  # 7 = handoff rejeitado


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
