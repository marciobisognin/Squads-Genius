#!/usr/bin/env python3
"""Valida a matriz operacional de metas e aponta lacunas auditáveis.

Verifica campos obrigatórios, vocabulário controlado (status/risco/periodicidade),
duplicidade de código, metas sem indicador/fonte/responsável/evidência e próxima
revisão vencida. Gera um quality report JSON e retorna código de saída != 0 se
houver achados bloqueantes — pronto para uso em CI.

Uso:
    python3 validate_indicator_matrix.py --input matriz_metas.csv \
        --report output/quality_report.json
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdi_common import (  # noqa: E402
    CAMPOS_OBRIGATORIOS,
    NIVEIS_RISCO,
    PERIODICIDADES,
    STATUS_VALIDOS,
    is_overdue,
    norm,
    read_csv,
    write_json,
)

STATUS_NORM = {norm(s) for s in STATUS_VALIDOS}
RISCO_NORM = {norm(s) for s in NIVEIS_RISCO}
PERIOD_NORM = {norm(s) for s in PERIODICIDADES}


def validate(rows: list[dict]) -> dict:
    findings: list[dict] = []
    codigos: dict[str, int] = {}

    def add(severidade: str, codigo: str, categoria: str, msg: str) -> None:
        findings.append(
            {
                "severidade": severidade,
                "codigo_meta": codigo,
                "categoria": categoria,
                "mensagem": msg,
            }
        )

    for i, row in enumerate(rows, start=1):
        codigo = (row.get("codigo") or f"linha-{i}").strip()
        codigos[codigo] = codigos.get(codigo, 0) + 1

        for campo in CAMPOS_OBRIGATORIOS:
            if not str(row.get(campo) or "").strip():
                sev = "alto" if campo in {"indicador", "fonte_dados", "responsavel_nome"} else "médio"
                add(sev, codigo, "campo_obrigatorio", f"campo obrigatório vazio: {campo}")

        status = norm(row.get("status"))
        if status and status not in STATUS_NORM:
            add("médio", codigo, "vocabulario", f"status inválido: {row.get('status')}")

        risco = norm(row.get("risco"))
        if risco and risco not in RISCO_NORM:
            add("médio", codigo, "vocabulario", f"risco inválido: {row.get('risco')}")

        period = norm(row.get("periodicidade"))
        if period and period not in PERIOD_NORM:
            add("baixo", codigo, "vocabulario", f"periodicidade inválida: {row.get('periodicidade')}")

        if not str(row.get("evidencia_obrigatoria") or "").strip():
            add("alto", codigo, "evidencia", "meta sem evidência obrigatória definida")

        if is_overdue(row.get("proxima_revisao")):
            add("alto", codigo, "prazo", f"próxima revisão vencida: {row.get('proxima_revisao')}")

    for codigo, count in codigos.items():
        if count > 1:
            add("alto", codigo, "duplicidade", f"código repetido {count}x")

    contagem = {sev: sum(1 for f in findings if f["severidade"] == sev) for sev in ("alto", "médio", "baixo")}
    bloqueantes = contagem["alto"]
    report = {
        "total_metas": len(rows),
        "total_achados": len(findings),
        "por_severidade": contagem,
        "go_no_go": "no-go" if bloqueantes else "go",
        "achados": findings,
        "observacao": "Achados de severidade alta exigem saneamento/revisão humana antes da publicação.",
    }
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Valida matriz de metas/indicadores do PDI.")
    ap.add_argument("--input", required=True, help="Matriz de metas (CSV).")
    ap.add_argument("--report", default="output/quality_report.json", help="Relatório JSON.")
    ap.add_argument("--strict", action="store_true", help="Falha (exit!=0) se houver achados altos.")
    args = ap.parse_args(argv)

    rows = read_csv(args.input)
    report = validate(rows)
    write_json(args.report, report)

    print(f"Metas: {report['total_metas']} | Achados: {report['total_achados']} "
          f"(altos={report['por_severidade']['alto']}, médios={report['por_severidade']['médio']}, "
          f"baixos={report['por_severidade']['baixo']})")
    print(f"go_no_go: {report['go_no_go']} | relatório: {args.report}")

    if args.strict and report["go_no_go"] == "no-go":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
