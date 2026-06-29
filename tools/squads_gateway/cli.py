#!/usr/bin/env python3
"""CLI do Squads Gateway — Fase 1 & 2.

Uso:
  python3 -m tools.squads_gateway.cli index --repo <path> --output <path>
  python3 -m tools.squads_gateway.cli search --index <path> --term "conteúdo"
  python3 -m tools.squads_gateway.cli route --index <path> --task "criar..."
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from .indexer import (
    create_index,
    save_index,
    generate_audit_report,
)
from .ranker import rank_squads


def cmd_index(args) -> int:
    """Comando: index — Cria índice canônico."""
    repo_root = Path(args.repo).resolve()
    output_path = Path(args.output).resolve() if args.output else repo_root / "squads_index.json"
    audit_path = output_path.parent / "gateway_audit.json"

    if not repo_root.exists():
        print(f"❌ Repo não encontrado: {repo_root}", file=sys.stderr)
        return 2

    print(f"📚 Indexando squads em {repo_root}...", flush=True)

    index = create_index(repo_root)

    print(f"✅ {index.total_count} squads indexados", flush=True)

    save_index(index, output_path)
    print(f"📄 Índice salvo: {output_path}", flush=True)

    generate_audit_report(index, audit_path)
    print(f"📊 Auditoria gerada: {audit_path}", flush=True)

    # Resumo
    print(f"\n📈 Resumo:")
    print(f"  - Total: {index.total_count}")
    print(f"  - Com agentes: {sum(1 for s in index.squads if s.agents)}")
    print(f"  - Com tarefas: {sum(1 for s in index.squads if s.tasks)}")
    print(f"  - Com workflows: {sum(1 for s in index.squads if s.workflows)}")

    return 0


def cmd_search(args) -> int:
    """Comando: search — Busca por termo."""
    index_path = Path(args.index)

    if not index_path.exists():
        print(f"❌ Índice não encontrado: {index_path}", file=sys.stderr)
        return 2

    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    term = args.term.lower()
    results = rank_squads(term, index_data, top_n=args.top)

    output = {
        "search_term": args.term,
        "results_count": len(results),
        "results": results,
        "generated_at": datetime.utcnow().isoformat(),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


def cmd_route(args) -> int:
    """Comando: route — Roteia tarefa ao melhor squad."""
    index_path = Path(args.index)

    if not index_path.exists():
        print(f"❌ Índice não encontrado: {index_path}", file=sys.stderr)
        return 2

    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    results = rank_squads(args.task, index_data, top_n=args.top)

    output = {
        "task": args.task,
        "recommendations": results[:args.top],
        "generated_at": datetime.utcnow().isoformat(),
    }

    # Se score muito baixo, sugere GAP
    if results and results[0]["score"] < args.threshold:
        top_keywords = [r["matched_keywords"][0] for r in results[:3] if r.get("matched_keywords")]
        output["gap_analysis"] = {
            "has_gap": True,
            "reason": "Score insuficiente para roteamento confiável",
            "suggested_squad_name": "-".join(top_keywords[:2] or ["novo"]) + "-squad",
            "suggested_capabilities": top_keywords[:4],
            "next_steps": [
                f"Criar novo squad com /criar-squad",
                f"Ou registrar essa demanda para aprendizagem",
            ],
        }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


def main():
    """Entry point da CLI."""
    parser = argparse.ArgumentParser(
        description="Squads Gateway — catálogo vivo e roteamento",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s index --repo /home/user/Squads-Genius
  %(prog)s search --index squads_index.json --term "conteúdo"
  %(prog)s route --index squads_index.json --task "criar carrossel para instagram"
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Comando")

    # Comando: index
    index_parser = subparsers.add_parser("index", help="Cria índice canônico")
    index_parser.add_argument("--repo", default=".", help="Raiz do repositório (default: .)")
    index_parser.add_argument("--output", help="Caminho de saída (default: {repo}/squads_index.json)")
    index_parser.set_defaults(func=cmd_index)

    # Comando: search
    search_parser = subparsers.add_parser("search", help="Busca por termo")
    search_parser.add_argument("--index", required=True, help="Caminho do índice JSON")
    search_parser.add_argument("--term", required=True, help="Termo de busca")
    search_parser.add_argument("--top", type=int, default=5, help="Top-N resultados (default: 5)")
    search_parser.set_defaults(func=cmd_search)

    # Comando: route
    route_parser = subparsers.add_parser("route", help="Roteia tarefa ao melhor squad")
    route_parser.add_argument("--index", required=True, help="Caminho do índice JSON")
    route_parser.add_argument("--task", required=True, help="Descrição da tarefa")
    route_parser.add_argument("--top", type=int, default=3, help="Top-N recomendações (default: 3)")
    route_parser.add_argument("--threshold", type=float, default=2.0, help="Score mínimo (default: 2.0)")
    route_parser.set_defaults(func=cmd_route)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
