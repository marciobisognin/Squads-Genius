#!/usr/bin/env python3
"""Bifröst Forge — executor de topo do engine (da ideia ao squad completo).

Transforma um briefing YAML/JSON em um squad completo, determinístico e validável,
com trilha de auditoria encadeada (Saga Ledger) e verificação de determinismo.

Exemplos:
    python3 bifrost_forge.py --briefing b.yaml --output out --overwrite
    python3 bifrost_forge.py --briefing b.yaml --output out --dry-run
    python3 bifrost_forge.py --briefing b.yaml --output out --verify-determinism

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

from saga_briefing import BriefingError, load_briefing
from bifrost_orchestrator import BifrostOrchestrator, tree_hash

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Forja um squad completo a partir de um briefing YAML/JSON.")
    ap.add_argument("--briefing", required=True, help="Arquivo de briefing YAML/JSON.")
    ap.add_argument("--output", required=True, help="Diretório de saída do squad forjado.")
    ap.add_argument("--dry-run", action="store_true", help="Planeja sem gravar arquivos.")
    ap.add_argument("--strict", action="store_true", help="Falha em campos ausentes/desconhecidos.")
    ap.add_argument("--overwrite", action="store_true", help="Substitui a saída se já existir.")
    ap.add_argument("--format", choices=["yaml", "json"], help="Força o formato de leitura.")
    ap.add_argument("--no-llm", action="store_true", help="Execução determinística sem LLM (modo implementado).")
    ap.add_argument("--budget-limit", help="Sobrescreve budget_limit do briefing.")
    ap.add_argument("--resume", action="store_true", help="Retoma de um checkpoint anterior.")
    ap.add_argument("--verify-determinism", action="store_true", help="Forja duas vezes e compara o hash da árvore.")
    return ap.parse_args()


def _ensure_output(out: Path, overwrite: bool) -> None:
    if out.exists() and any(out.iterdir()):
        if not overwrite:
            raise BriefingError(f"Saída já existe e não está vazia: {out}. Use --overwrite.")
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)


def _verify_determinism(briefing) -> str:
    digests = []
    for _ in range(2):
        tmp = Path(tempfile.mkdtemp(prefix="bifrost-det-"))
        try:
            BifrostOrchestrator(briefing, tmp).forge()
            digests.append(tree_hash(tmp)[0])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    if digests[0] != digests[1]:
        raise BriefingError(f"determinismo quebrado: {digests[0]} != {digests[1]}")
    return digests[0]


def main() -> int:
    args = parse_args()
    try:
        briefing = load_briefing(args.briefing, strict=args.strict, forced_format=args.format, budget_limit=args.budget_limit)
        orch = BifrostOrchestrator(briefing, Path(args.output))
        if args.dry_run:
            plan = orch.plan()
            plan["dry_run"] = True
            plan["no_llm"] = bool(args.no_llm)
            print(json.dumps(plan, ensure_ascii=False, indent=2))
            return 0

        det_hash = _verify_determinism(briefing) if args.verify_determinism else None

        out = Path(args.output).resolve()
        _ensure_output(out, args.overwrite)
        report = BifrostOrchestrator(briefing, out).forge(resume=args.resume)

        if det_hash and det_hash != report.get("determinism_hash"):
            print(f"Aviso: hash de verificação difere da saída ({det_hash} != {report.get('determinism_hash')}).", file=sys.stderr)

        print(json.dumps({
            "output": str(out),
            "score": report["score"],
            "go_no_go": report["go_no_go"],
            "determinism_hash": report.get("determinism_hash"),
            "determinism_verified": bool(args.verify_determinism),
            "ledger_head": report.get("ledger_head"),
            "tests_failed": report["tests_failed"],
        }, ensure_ascii=False, indent=2))
        return 0 if not report["tests_failed"] else 1
    except BriefingError as exc:
        print(f"Erro de briefing: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
