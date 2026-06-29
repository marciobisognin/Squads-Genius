#!/usr/bin/env python3
"""KUP — economia de tokens e orçamento por run (estrato KÝKLOS).

Consolida o orçamento de uma run a partir do `run_state.json` (spans de
observabilidade quando presentes). Os números são derivados deterministicamente
dos eventos registrados — nunca estimados por um modelo de linguagem
(Lei da Fronteira Determinística).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forge_common import write_json  # noqa: E402

# Roteamento canônico de modelos por tipo de ato (barato vs. forte).
ROTA_MODELOS = {
    "noesis": "barato (classificação/normalização)",
    "boule": "forte (estratégia/topologia)",
    "diairesis": "barato (decomposição estruturada)",
    "praxis": "barato→forte (depende da microtarefa)",
    "elenchos": "determinístico (scripts, sem LLM)",
    "krisis": "forte (juízo adversarial)",
    "anamnesis": "barato (consolidação)",
}

# Passos cobertos por script puro (custo de LLM = 0).
PASSOS_SCRIPTADOS = [
    "validação de schema (sacp.py)",
    "pontuação de instrumentos (evaluate_tool.py — Decimal)",
    "classificação de roteamento (cynefin_gate.py)",
    "empacotamento e contagem (build_pack.py)",
    "gates de qualidade (validate_squad.py)",
]


def consolidar(run_state: dict[str, Any]) -> dict[str, Any]:
    """Deriva o orçamento de tokens a partir do estado da run."""
    spans = run_state.get("spans", [])
    orcamento = run_state.get("orcamento", {}) or {}
    teto_tokens = int(orcamento.get("tokens", 0) or 0)

    tokens_reais = 0
    tokens_estimados = 0
    chamadas = 0
    custo = Decimal("0")
    por_ato: dict[str, int] = {}
    passos_llm: list[str] = []

    for span in spans:
        ato = str(span.get("ato", "desconhecido"))
        tr = int(span.get("tokens_reais", 0) or 0)
        te = int(span.get("tokens_estimados", 0) or 0)
        tokens_reais += tr
        tokens_estimados += te
        chamadas += int(span.get("chamadas_ferramenta", 0) or 0)
        custo += Decimal(str(span.get("custo_monetario", 0) or 0))
        por_ato[ato] = por_ato.get(ato, 0) + (tr or te)
        if span.get("usou_llm"):
            passos_llm.append(f"{ato}: {span.get('descricao', 'passo LLM')}")

    uso = tokens_reais or tokens_estimados
    estouro = teto_tokens > 0 and uso > teto_tokens

    oportunidades: list[str] = []
    for ato, total in sorted(por_ato.items(), key=lambda x: -x[1]):
        if total > 0 and ROTA_MODELOS.get(ato, "").startswith("forte"):
            oportunidades.append(
                f"{ato}: avaliar cache/resumo incremental antes do modelo forte"
            )
    if not spans:
        oportunidades.append(
            "run sem spans registrados — orçamento estimado pela tabela de roteamento"
        )

    return {
        "estimated_token_budget": teto_tokens,
        "actual_or_estimated_usage": uso,
        "tokens_reais": tokens_reais,
        "tokens_estimados": tokens_estimados,
        "tool_calls": chamadas,
        "custo_monetario": str(custo),
        "orcamento_estourado": estouro,
        "model_routing": [{"ato": a, "rota": r} for a, r in ROTA_MODELOS.items()],
        "scripted_steps": PASSOS_SCRIPTADOS,
        "llm_steps": passos_llm,
        "usage_by_act": por_ato,
        "savings_opportunities": oportunidades,
        "lei": "Lei da Fronteira Determinística — números derivados de spans, não de LLM.",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="KUP — orçamento de tokens por run.")
    ap.add_argument("--run", required=True, help="caminho do run_state.json")
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    run_state = json.loads(Path(args.run).read_text(encoding="utf-8"))
    resultado = consolidar(run_state)
    if args.out:
        write_json(args.out, resultado)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
