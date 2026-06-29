#!/usr/bin/env python3
"""Entrypoint único de orquestração via CLI.

Despacha workflows do squad para os scripts determinísticos. A síntese
textual (quando aplicável) fica a cargo do agente LLM que consome a saída.

Exemplos:
  python3 run_squad.py --workflow build_index --config config/user.config.yaml
  python3 run_squad.py --workflow ask_vault --query "tema" --config ...

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys

import obsidian_digest as digest_mod
import obsidian_graph as graph_mod
import obsidian_index as index_mod
import obsidian_quality_audit as audit_mod
import obsidian_query as query_mod

WORKFLOWS = {
    "build_index", "update_index", "ask_vault", "generate_knowledge_map",
    "vault_digest", "quality_gate", "export_context",
}


def dispatch(args: argparse.Namespace) -> dict:
    wf = args.workflow
    if wf in {"build_index", "update_index"}:
        return index_mod.build_index(args.config, args.vault)
    if wf == "ask_vault":
        if not args.query:
            raise ValueError("--query é obrigatório para ask_vault")
        return query_mod.query(args.config, args.vault, args.query)
    if wf == "generate_knowledge_map":
        return graph_mod.build_graph(args.config, args.vault, args.topic)
    if wf == "vault_digest":
        return digest_mod.digest(args.config, args.vault, args.days)
    if wf == "quality_gate":
        return audit_mod.audit(args.config, args.vault)
    if wf == "export_context":
        if not args.query:
            raise ValueError("--query é obrigatório para export_context")
        import obsidian_export_context as exp
        return exp.export_context(args.config, args.vault, args.query)
    raise ValueError(f"Workflow desconhecido: {wf}. Use {sorted(WORKFLOWS)}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Orquestrador CLI do squad.")
    ap.add_argument("--workflow", required=True, choices=sorted(WORKFLOWS))
    ap.add_argument("--config")
    ap.add_argument("--vault")
    ap.add_argument("--query")
    ap.add_argument("--topic")
    ap.add_argument("--days", type=int, default=7)
    args = ap.parse_args()
    try:
        result = dispatch(args)
    except Exception as exc:  # noqa: BLE001
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
