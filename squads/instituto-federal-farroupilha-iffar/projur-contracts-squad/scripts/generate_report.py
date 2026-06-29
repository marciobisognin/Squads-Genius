#!/usr/bin/env python3
"""Relatório executivo em Markdown (PDF quando um conversor estiver disponível).

Uso: python scripts/generate_report.py --indicadores ./saida/indicadores.json \
        --alertas ./saida/alertas.json --validacoes ./saida/validacoes.json \
        --out ./saida/relatorio_executivo.md
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from projur_common import read_json

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--indicadores", required=True)
    ap.add_argument("--alertas", default=None)
    ap.add_argument("--validacoes", default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    ind = read_json(args.indicadores, {})
    alertas = read_json(args.alertas, {"itens": []}).get("itens", []) if args.alertas else []
    val = read_json(args.validacoes, {"itens": []}).get("itens", []) if args.validacoes else []

    a_vencer = [a for a in alertas if a.get("status") in ("a_vencer", "vencido")]
    L = []
    L.append("# Relatório Executivo — PROJUR Contracts Squad\n")
    L.append(f"_Gerado em {date.today().isoformat()}_\n")
    L.append("## 1. Panorama\n")
    L.append(f"- Total de instrumentos: **{ind.get('total_instrumentos', 0)}**")
    L.append(f"- Valor total: **R$ {ind.get('valor_total', 0):,.2f}**")
    L.append(f"- Taxa de renovação (aditivos/contratos): **{ind.get('taxa_renovacao', 0)}**")
    L.append(f"- % de instrumentos com cláusulas fora do padrão: **{ind.get('pct_clausulas_fora_padrao', 0) * 100:.0f}%**\n")
    L.append("## 2. Distribuição por tipo\n")
    for tipo, n in sorted(ind.get("por_tipo", {}).items(), key=lambda x: -x[1]):
        L.append(f"- {tipo}: {n}")
    L.append("\n## 3. Alertas de vigência\n")
    if a_vencer:
        for a in a_vencer[:30]:
            L.append(f"- {a['instrumento_id']}: **{a['status']}** — {a['acao_recomendada']}")
    else:
        L.append("- Nenhum instrumento vencido ou a vencer no horizonte monitorado.")
    L.append(f"\n## 4. Apontamentos de conformidade ({len(val)})\n")
    for v in val[:30]:
        L.append(f"- {v['instrumento_id']} — regra `{v['regra_id']}` ({v['classificacao']}): {v['fundamento']}")
    L.append("\n## 5. Ressalva\n")
    L.append("Apoio técnico automatizado. Não substitui parecer da Procuradoria competente "
             "(art. 53 da Lei 14.133/2021). Os dispositivos citados são referenciais e exigem "
             "verificação de vigência. Casos críticos devem ser encaminhados ao squad Themis.\n")
    L.append(f"\n---\n\n{FOOTER}\n")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"Relatório executivo gerado -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
