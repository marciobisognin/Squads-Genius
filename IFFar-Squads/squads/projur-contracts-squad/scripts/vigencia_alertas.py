#!/usr/bin/env python3
"""Alertas de ciclo de vida: status de vigência e prazo de renovação.

Uso: python scripts/vigencia_alertas.py --metadados ./saida/metadados.json \
        --hoje 2026-06-17 --output ./saida
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path

from projur_common import read_json, write_json

LIMITE_ALERTA_DIAS = 90


def to_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadados", required=True)
    ap.add_argument("--hoje", default=date.today().isoformat())
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    out = Path(args.output) if args.output else Path(args.metadados).parent
    hoje = to_date(args.hoje) or date.today()
    itens = read_json(args.metadados, {"itens": []}).get("itens", [])

    alertas = []
    for md in itens:
        fim = to_date(md.get("vigencia_fim"))
        if not fim:
            alertas.append({"instrumento_id": md["id"], "status": "sem_vigencia",
                            "dias_para_vencimento": None, "percentual_aditivos": None,
                            "acao_recomendada": "Identificar data de vigência manualmente"})
            continue
        dias = (fim - hoje).days
        if dias < 0:
            status, acao = "vencido", "Verificar renovação/extinção e regularidade da execução"
        elif dias <= LIMITE_ALERTA_DIAS:
            status, acao = "a_vencer", f"Iniciar processo de renovação ({dias} dias restantes)"
        else:
            status, acao = "vigente", "Sem ação imediata"
        alertas.append({"instrumento_id": md["id"], "status": status,
                        "dias_para_vencimento": dias, "percentual_aditivos": None,
                        "acao_recomendada": acao})

    write_json(out / "alertas.json", {"total": len(alertas), "itens": alertas})
    venc = sum(1 for a in alertas if a["status"] in ("vencido", "a_vencer"))
    print(f"Alertas de vigência gerados: {len(alertas)} ({venc} requerem atenção).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
