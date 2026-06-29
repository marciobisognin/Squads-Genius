#!/usr/bin/env python3
"""Valida os exemplos de contrato (SACP-IN, Claim, VerifiedClaim, Dossier) do squad PALIMPSESTO contra seus schemas JSON.

Uso:
    python3 scripts/validate_contracts.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
FIXTURES = ROOT / "examples" / "fixtures"


def _check_required(name: str, schema: dict, payload: dict) -> list[str]:
    errors = []
    for field in schema.get("required", []):
        if field not in payload:
            errors.append(f"{name}: campo obrigatório ausente: {field}")
    for field, spec in schema.get("properties", {}).items():
        if field not in payload:
            continue
        enum = spec.get("enum")
        if enum and payload[field] not in enum:
            errors.append(f"{name}: valor inválido em '{field}': {payload[field]!r} (esperado um de {enum})")
    return errors


def main() -> int:
    pairs = [
        ("SACP-IN", "sacp-in.schema.json", "sacp-in.example.json"),
        ("Claim", "claim.schema.json", "claim.example.json"),
        ("VerifiedClaim", "verified-claim.schema.json", "verified-claim.example.json"),
        ("Dossier", "dossier.schema.json", "dossier.example.json"),
    ]
    all_errors: list[str] = []
    for name, schema_file, fixture_file in pairs:
        schema_path = TEMPLATES / schema_file
        fixture_path = FIXTURES / fixture_file
        if not schema_path.is_file():
            all_errors.append(f"{name}: schema ausente em {schema_path}")
            continue
        if not fixture_path.is_file():
            all_errors.append(f"{name}: fixture ausente em {fixture_path}")
            continue
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        all_errors.extend(_check_required(name, schema, payload))

    if all_errors:
        print("FALHA na validação dos contratos:")
        for err in all_errors:
            print(f"  - {err}")
        return 1
    print(f"OK: {len(pairs)} contratos validados com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
