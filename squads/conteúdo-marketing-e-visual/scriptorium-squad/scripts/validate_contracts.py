#!/usr/bin/env python3
"""Valida as fixtures de contrato do squad SCRIPTORIUM contra seus JSON Schemas.

Checa, sem dependências externas: campos obrigatórios (`required`) e valores de
`enum` declarados nos schemas. Determinístico e offline.

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

PAIRS = [
    ("BriefingDeQuestao", "briefing-de-questao.schema.json", "briefing-de-questao.example.json"),
    ("VerificacaoCitacao", "verificacao-citacao.schema.json", "verificacao-citacao.example.json"),
    ("RelatorioIntegridade", "relatorio-integridade.schema.json", "relatorio-integridade.example.json"),
    ("ContratoDeParecer", "contrato-de-parecer.schema.json", "contrato-de-parecer.example.json"),
    ("MatrizDeRastreabilidade", "matriz-de-rastreabilidade.schema.json", "matriz-de-rastreabilidade.example.json"),
    ("PassaporteDossie", "passaporte-dossie.schema.json", "passaporte-dossie.example.json"),
]


def _check(name: str, schema: dict, payload: dict) -> list[str]:
    errors: list[str] = []
    for field in schema.get("required", []):
        if field not in payload:
            errors.append(f"{name}: campo obrigatório ausente: {field}")
    for field, spec in schema.get("properties", {}).items():
        if field not in payload or not isinstance(spec, dict):
            continue
        enum = spec.get("enum")
        if enum and payload[field] not in enum:
            errors.append(
                f"{name}: valor inválido em '{field}': {payload[field]!r} (esperado um de {enum})"
            )
    return errors


def main() -> int:
    all_errors: list[str] = []
    for name, schema_file, fixture_file in PAIRS:
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
        all_errors.extend(_check(name, schema, payload))

    if all_errors:
        print("FALHA na validação dos contratos:")
        for err in all_errors:
            print(f"  - {err}")
        return 1
    print(f"OK: {len(PAIRS)} contratos validados com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
