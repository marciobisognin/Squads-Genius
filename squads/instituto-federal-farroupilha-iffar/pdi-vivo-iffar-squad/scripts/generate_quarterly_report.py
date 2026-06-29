#!/usr/bin/env python3
"""Gera o relatório executivo trimestral do PDI a partir da matriz de metas.

Resumo de duas páginas: status consolidado, metas críticas, riscos, lacunas de
evidência e pendências de decisão. Saída em Markdown (conversível a PDF/DOCX por
ferramenta externa). Determinístico e auditável.

Uso:
    python3 generate_quarterly_report.py --input matriz_metas.csv \
        --ciclo 2027-2034 --trimestre 2026Q2 --output output/relatorio_trimestral.md
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdi_common import FOOTER, derive_risk, is_overdue, norm, read_csv  # noqa: E402


def build_report(rows: list[dict], ciclo: str, trimestre: str) -> str:
    total = len(rows)
    status_cont = Counter(norm(r.get("status")) or "SEM STATUS" for r in rows)
    risco_cont = Counter(derive_risk(r) for r in rows)
    criticas = [r for r in rows if derive_risk(r) in {"alto", "crítico"}]
    sem_indicador = [r for r in rows if not str(r.get("indicador") or "").strip()]
    sem_evidencia = [r for r in rows if not str(r.get("evidencia_obrigatoria") or "").strip()]
    vencidas = [r for r in rows if is_overdue(r.get("proxima_revisao"))]
    decisao = [r for r in rows if norm(r.get("status")) in {"REQUER DECISÃO", "REQUER REPACTUAÇÃO", "SUSPENSA"}]

    concluidas = status_cont.get("CONCLUÍDA", 0) + status_cont.get("PARCIALMENTE CONCLUÍDA", 0)
    pct = round(100 * concluidas / total, 1) if total else 0.0

    L = []
    L.append(f"# Relatório Executivo Trimestral — PDI {ciclo}")
    L.append(f"**Trimestre:** {trimestre}  |  **Gerado em:** {date.today().isoformat()}")
    L.append("")
    L.append("## 1. Panorama")
    L.append(f"- Metas acompanhadas: **{total}**")
    L.append(f"- Progresso (concluídas/parciais): **{concluidas}** ({pct}%)")
    L.append(f"- Risco — crítico: **{risco_cont.get('crítico', 0)}**, "
             f"alto: **{risco_cont.get('alto', 0)}**, médio: **{risco_cont.get('médio', 0)}**, "
             f"baixo: **{risco_cont.get('baixo', 0)}**")
    L.append("")
    L.append("### Status")
    for status, n in sorted(status_cont.items(), key=lambda x: -x[1]):
        L.append(f"- {status.capitalize()}: {n}")
    L.append("")

    L.append("## 2. Metas que exigem atenção (risco alto/crítico)")
    if criticas:
        L.append("| Código | Dimensão | Campus | Meta | Risco | Ação corretiva |")
        L.append("|---|---|---|---|:--:|---|")
        for r in criticas[:40]:
            L.append(f"| {r.get('codigo','')} | {r.get('dimensao','')} | {r.get('campus','')} | "
                     f"{r.get('meta','')[:70]} | **{derive_risk(r)}** | "
                     f"{(r.get('acao_corretiva') or '—')[:60]} |")
    else:
        L.append("_Nenhuma meta de risco alto/crítico neste ciclo._")
    L.append("")

    L.append("## 3. Pendências de decisão")
    if decisao:
        for r in decisao:
            L.append(f"- **{r.get('codigo','')}** ({r.get('campus','')}): {r.get('meta','')[:90]} "
                     f"— status: {r.get('status','')}")
    else:
        L.append("_Sem pendências de decisão registradas._")
    L.append("")

    L.append("## 4. Qualidade de dados")
    L.append(f"- Metas sem indicador: **{len(sem_indicador)}**")
    L.append(f"- Metas sem evidência obrigatória: **{len(sem_evidencia)}**")
    L.append(f"- Próximas revisões vencidas: **{len(vencidas)}**")
    L.append("")

    L.append("## 5. Recomendações")
    L.append("- Sanear lacunas de indicador/fonte/evidência antes da próxima conferência.")
    L.append("- Registrar ata de decisão corretiva para cada meta crítica.")
    L.append("- Revisão humana institucional obrigatória antes de publicação.")
    L.append("")
    L.append("---")
    L.append("> Relatório determinístico gerado a partir da matriz operacional. "
             "Não substitui leitura qualitativa nem deliberação colegiada.")
    L.append("")
    L.append(FOOTER)
    L.append("")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gera relatório executivo trimestral do PDI.")
    ap.add_argument("--input", required=True, help="Matriz de metas (CSV).")
    ap.add_argument("--ciclo", default="2027-2034")
    ap.add_argument("--trimestre", default="")
    ap.add_argument("--output", default="output/relatorio_trimestral.md")
    args = ap.parse_args(argv)

    rows = read_csv(args.input)
    report = build_report(rows, args.ciclo, args.trimestre or date.today().strftime("%YQ%m"))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"OK: relatório trimestral -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
