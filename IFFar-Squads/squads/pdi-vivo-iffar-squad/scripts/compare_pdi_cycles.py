#!/usr/bin/env python3
"""Compara dois ciclos do PDI por incidência de termos de gestão viva.

Reproduz, de forma determinística e auditável, a tabela comparativa do estudo
(ex.: indicadores, riscos, evidências, dashboard, painel, dados, territorial).
Recebe dois arquivos de texto extraídos e gera CSV/Markdown comparativos.

Uso:
    python3 compare_pdi_cycles.py --anterior extracoes/pdi_2019_2026.txt \
        --novo extracoes/pdi_vivo_2027_2034.txt --output-dir output/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdi_common import write_csv  # noqa: E402

TERMOS = [
    "monitoramento",
    "indicadores",
    "riscos",
    "evidências",
    "dashboard",
    "painel",
    "dados",
    "territorial",
    "permanência",
    "êxito",
    "orçamento",
    "transparência",
]


def count_terms(text: str) -> dict[str, int]:
    lower = text.lower()
    return {t: lower.count(t.lower()) for t in TERMOS}


def build_rows(anterior: dict[str, int], novo: dict[str, int],
               label_a: str, label_b: str) -> list[dict]:
    rows = []
    for termo in TERMOS:
        a, b = anterior[termo], novo[termo]
        rows.append(
            {
                "termo": termo,
                label_a: a,
                label_b: b,
                "delta": b - a,
                "tendencia": "↑" if b > a else ("↓" if b < a else "="),
            }
        )
    return rows


def to_markdown(rows: list[dict], label_a: str, label_b: str) -> str:
    out = ["# Comparativo de ciclos do PDI — incidência de termos de gestão viva", ""]
    out.append(f"| Termo | {label_a} | {label_b} | Δ | Tendência |")
    out.append("|---|---:|---:|---:|:---:|")
    for r in rows:
        out.append(f"| {r['termo']} | {r[label_a]} | {r[label_b]} | {r['delta']:+d} | {r['tendencia']} |")
    out.append("")
    out.append("> Contagem textual não substitui leitura qualitativa; serve para evidenciar "
               "onde o novo ciclo reforça monitoramento, evidências e dados.")
    out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Compara ciclos do PDI por incidência de termos.")
    ap.add_argument("--anterior", required=True, help="Texto extraído do ciclo anterior.")
    ap.add_argument("--novo", required=True, help="Texto extraído do novo ciclo.")
    ap.add_argument("--label-anterior", default="anterior")
    ap.add_argument("--label-novo", default="novo")
    ap.add_argument("--output-dir", default="output")
    args = ap.parse_args(argv)

    a_text = Path(args.anterior).read_text(encoding="utf-8", errors="ignore")
    b_text = Path(args.novo).read_text(encoding="utf-8", errors="ignore")
    rows = build_rows(count_terms(a_text), count_terms(b_text), args.label_anterior, args.label_novo)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "comparativo_ciclos.csv", rows,
              ["termo", args.label_anterior, args.label_novo, "delta", "tendencia"])
    (out_dir / "comparativo_ciclos.md").write_text(
        to_markdown(rows, args.label_anterior, args.label_novo), encoding="utf-8")

    print(f"OK: comparativo de {len(rows)} termos -> {out_dir}/comparativo_ciclos.[csv|md]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
