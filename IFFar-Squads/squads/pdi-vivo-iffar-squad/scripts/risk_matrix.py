#!/usr/bin/env python3
"""Constrói a matriz de riscos do PDI a partir da matriz operacional de metas.

Aplica a regra determinística de `derive_risk` (status, atraso e lacunas de
evidência elevam o risco), consolida por dimensão e por campus, e sugere ação
corretiva quando ausente. Saídas: CSV e Markdown.

Uso:
    python3 risk_matrix.py --input matriz_metas.csv --output-dir output/
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdi_common import derive_risk, is_overdue, norm, read_csv, write_csv  # noqa: E402

ACAO_PADRAO = {
    "crítico": "Levar à Câmara de Riscos; decisão corretiva imediata e repactuação se necessário.",
    "alto": "Definir responsável, indicador e fonte; reavaliar no próximo ciclo trimestral.",
    "médio": "Monitorar; confirmar dados e prazos na próxima atualização.",
    "baixo": "Acompanhamento de rotina.",
}


def build(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        risco = derive_risk(r)
        motivos = []
        if norm(r.get("status")) in {"ATRASADA"} or is_overdue(r.get("proxima_revisao")):
            motivos.append("prazo")
        if not str(r.get("indicador") or "").strip():
            motivos.append("sem indicador")
        if not str(r.get("fonte_dados") or "").strip():
            motivos.append("sem fonte")
        if not str(r.get("responsavel_nome") or "").strip():
            motivos.append("sem responsável")
        if norm(r.get("status")) in {"SUSPENSA", "REQUER DECISÃO", "REQUER REPACTUAÇÃO"}:
            motivos.append("status crítico")
        out.append(
            {
                "codigo": r.get("codigo", ""),
                "dimensao": r.get("dimensao", ""),
                "campus": r.get("campus", ""),
                "meta": (r.get("meta", "")[:90]),
                "status": r.get("status", ""),
                "risco": risco,
                "motivos": "; ".join(motivos) or "—",
                "restricao_principal": r.get("restricao_principal", ""),
                "acao_corretiva": r.get("acao_corretiva") or ACAO_PADRAO[risco],
            }
        )
    # Ordena por criticidade decrescente.
    ordem = {"crítico": 0, "alto": 1, "médio": 2, "baixo": 3}
    out.sort(key=lambda x: ordem[x["risco"]])
    return out


def to_markdown(rows: list[dict]) -> str:
    cont = Counter(r["risco"] for r in rows)
    out = ["# Matriz de Riscos do PDI", ""]
    out.append(f"- Crítico: **{cont.get('crítico', 0)}** | Alto: **{cont.get('alto', 0)}** | "
               f"Médio: **{cont.get('médio', 0)}** | Baixo: **{cont.get('baixo', 0)}**")
    out.append("")
    out.append("| Código | Dimensão | Campus | Risco | Motivos | Ação corretiva |")
    out.append("|---|---|---|:--:|---|---|")
    for r in rows:
        if r["risco"] in {"crítico", "alto"}:
            out.append(f"| {r['codigo']} | {r['dimensao']} | {r['campus']} | "
                       f"**{r['risco']}** | {r['motivos']} | {r['acao_corretiva']} |")
    out.append("")
    out.append("> Riscos médios e baixos detalhados no CSV. Regra conservadora: lacunas de "
               "indicador/fonte/responsável e prazos vencidos elevam o risco.")
    out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gera matriz de riscos do PDI.")
    ap.add_argument("--input", required=True, help="Matriz de metas (CSV).")
    ap.add_argument("--output-dir", default="output")
    args = ap.parse_args(argv)

    rows = build(read_csv(args.input))
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "matriz_riscos.csv", rows,
              ["codigo", "dimensao", "campus", "meta", "status", "risco",
               "motivos", "restricao_principal", "acao_corretiva"])
    (out_dir / "matriz_riscos.md").write_text(to_markdown(rows), encoding="utf-8")

    criticos = sum(1 for r in rows if r["risco"] in {"crítico", "alto"})
    print(f"OK: {len(rows)} metas avaliadas | {criticos} de atenção -> {out_dir}/matriz_riscos.[csv|md]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
