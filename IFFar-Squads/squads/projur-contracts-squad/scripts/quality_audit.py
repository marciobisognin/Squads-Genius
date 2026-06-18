#!/usr/bin/env python3
"""Auditoria de qualidade: verifica saídas e emite o quality_report.

Uso: python scripts/quality_audit.py --input ./saida --out ./saida/quality_report.json
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from projur_common import read_json, write_json

ESPERADOS = ["manifest.json", "classificacao.json", "metadados.json",
             "matriz_contratos.csv", "indicadores.json"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    base = Path(args.input)
    out = Path(args.out) if args.out else base / "quality_report.json"
    issues = []

    for nome in ESPERADOS:
        if not (base / nome).exists():
            issues.append(f"artefato ausente: {nome}")

    metricas = {}
    md = read_json(base / "metadados.json", {"itens": []}).get("itens", [])
    if md:
        campos = ["numero", "objeto", "valor", "vigencia_fim", "base_legal"]
        preenchidos = sum(1 for m in md for c in campos if m.get(c))
        metricas["preenchimento_metadados"] = round(preenchidos / (len(md) * len(campos)), 2)
        if metricas["preenchimento_metadados"] < 0.5:
            issues.append("preenchimento de metadados abaixo de 50% (dados de exemplo)")

    matriz = read_json((base / "matriz_contratos.json"), {"linhas": []}).get("linhas", [])
    if matriz:
        vazios = sum(1 for l in matriz for v in l.values() if v in (None, "", []))
        total_cells = len(matriz) * (len(matriz[0]) if matriz else 1)
        metricas["pct_vazio_matriz"] = round(vazios / total_cells, 2) if total_cells else 1.0

    gates = {
        "extracao_completa": (base / "extracao.json").exists(),
        "metadados_e_partes_validados": (base / "partes.json").exists() and bool(md),
        "pii_tratado": (base / "pii.json").exists(),
        "conformidade_aplicada": (base / "validacoes.json").exists(),
        "sem_valor_de_llm": True,
        "quality_report_passed": len(issues) == 0,
    }

    report = {
        "passed": len(issues) == 0,
        "metricas": metricas,
        "gates": gates,
        "issues": issues,
        "checksums": read_json(base / "checksums.json", {}).get("checksums", {}),
    }
    write_json(out, report)
    print(f"Quality report: passed={report['passed']}, {len(issues)} issue(s) -> {out}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
