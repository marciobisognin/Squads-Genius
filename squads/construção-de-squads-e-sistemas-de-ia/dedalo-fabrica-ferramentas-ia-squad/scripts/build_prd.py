#!/usr/bin/env python3
"""Compositor determinístico do PRD da ferramenta (TÉLOS) do DÉDALO.

Recebe um objeto PRD estruturado (JSON) — produzido pelo LLM como JSON — e o renderiza
em Markdown com a matriz de rastreabilidade fonte->requisito->feature. Sem LLM aqui:
apenas formatação determinística e checagem de features órfãs.

Uso:
    python3 scripts/build_prd.py --input examples/tool_prd.json --output output/prd.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


def _section(title: str, items: list) -> str:
    if not items:
        return f"## {title}\n\n_(não informado)_\n"
    body = "\n".join(f"- {it}" for it in items)
    return f"## {title}\n\n{body}\n"


def find_orphan_features(prd: dict) -> list[str]:
    """Retorna features sem rastreabilidade (feature órfã = alucinação potencial)."""
    traced = set()
    for row in prd.get("traceability_matrix", []):
        if isinstance(row, dict) and row.get("feature"):
            traced.add(str(row["feature"]))
    return [f for f in prd.get("features", []) if str(f) not in traced]


def render_prd(prd: dict) -> str:
    lines = [f"# PRD — {prd.get('objective', 'Ferramenta')}", ""]
    lines.append(_section("Objetivo", [prd.get("objective", "")]))
    lines.append(_section("Personas", prd.get("personas", [])))
    lines.append(_section("Casos de uso", prd.get("use_cases", [])))
    lines.append(_section("Requisitos funcionais", prd.get("functional_reqs", [])))
    lines.append(_section("Requisitos não funcionais", prd.get("non_functional_reqs", [])))
    lines.append(_section("Features (MoSCoW)", prd.get("features", [])))
    lines.append(_section("Corte do MVP", prd.get("mvp_cut", [])))
    lines.append(_section("Critérios de aceite", prd.get("acceptance_criteria", [])))

    matrix = prd.get("traceability_matrix", [])
    lines.append("## Matriz de rastreabilidade (fonte → requisito → feature)\n")
    if matrix:
        lines.append("| Fonte | Requisito | Feature |")
        lines.append("|---|---|---|")
        for row in matrix:
            lines.append(f"| {row.get('source','')} | {row.get('requirement','')} | {row.get('feature','')} |")
        lines.append("")
    else:
        lines.append("_(matriz não informada)_\n")

    orphans = find_orphan_features(prd)
    if orphans:
        lines.append("> [!CAUTION]")
        lines.append("> Features órfãs (sem rastreabilidade) — ELENCHUS deve auditar:")
        for o in orphans:
            lines.append(f"> - {o}")
        lines.append("")
    lines.append(f"\n{FOOTER}\n")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Renderiza o PRD em Markdown com matriz de rastreabilidade.")
    ap.add_argument("--input", required=True, help="ToolPRD em JSON.")
    ap.add_argument("--output", help="Caminho de saída do Markdown (stdout se omitido).")
    args = ap.parse_args()
    prd = json.loads(Path(args.input).read_text(encoding="utf-8"))
    md = render_prd(prd)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(json.dumps({"output": str(out), "orphan_features": find_orphan_features(prd)}, ensure_ascii=False))
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
