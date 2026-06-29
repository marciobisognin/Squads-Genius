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
from .contract_builder import build_activation_contract, print_activation_contract, export_activation_contract
from .audit_logger import AuditLogger
from .memory_store import MemoryStore
from .hitl_gate import HITLGate
from .router import OrchestrationRouter


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


def cmd_activate(args) -> int:
    """Comando: activate — Gera contrato de ativação para um squad."""
    index_path = Path(args.index)

    if not index_path.exists():
        print(f"❌ Índice não encontrado: {index_path}", file=sys.stderr)
        return 2

    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    # Encontra o squad pelo nome
    target_squad = None
    for squad in index_data.get("squads", []):
        if squad.get("name") == args.squad or squad.get("display_name") == args.squad:
            target_squad = squad
            break

    if not target_squad:
        print(f"❌ Squad não encontrado: {args.squad}", file=sys.stderr)
        print(f"\n💡 Use 'search' para encontrar o squad correto:")
        print(f"   python3 -m tools.squads_gateway search --index {index_path} --term '{args.squad}'")
        return 2

    # Constrói contrato
    contract = build_activation_contract(target_squad)

    # Output: visualmente no console ou JSON
    if args.output_json:
        print(json.dumps(export_activation_contract(contract), ensure_ascii=False, indent=2))
    else:
        print_activation_contract(contract)

    # Salva em arquivo se solicitado
    if args.save:
        save_path = Path(args.save)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(export_activation_contract(contract), f, ensure_ascii=False, indent=2)
        print(f"📄 Contrato salvo: {save_path}")

    return 0


def cmd_orchestrate(args) -> int:
    """Comando: orchestrate — Pipeline completo com HITL e memória."""
    index_path = Path(args.index)

    if not index_path.exists():
        print(f"❌ Índice não encontrado: {index_path}", file=sys.stderr)
        return 2

    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    # Inicializa componentes da Fase 3
    audit_logger = AuditLogger()
    memory_store = MemoryStore()
    hitl_gate = HITLGate()
    router = OrchestrationRouter(index_data, audit_logger, memory_store, hitl_gate)

    # Executa pipeline
    decision = router.route(
        task_description=args.task,
        context=args.context,
        preferred_domain=args.domain,
        require_hitl_approval=args.require_approval,
    )

    # Output
    output = {
        "task": decision.task_description,
        "recommendations": [r.to_dict() for r in decision.recommendations],
        "top_match": decision.top_match.to_dict() if decision.top_match else None,
        "gap_analysis": decision.gap_analysis.to_dict() if decision.gap_analysis else None,
        "generated_at": decision.decision_timestamp,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


def cmd_logs(args) -> int:
    """Comando: logs — Gerencia logs de auditoria."""
    audit_logger = AuditLogger()

    if args.show_stats:
        audit_logger.print_stats()
        return 0

    if args.export:
        export_path = Path(args.export)
        entries = audit_logger.read_log()
        export_path.parent.mkdir(parents=True, exist_ok=True)

        with open(export_path, "w", encoding="utf-8") as f:
            for entry in entries:
                json.dump(entry, f, ensure_ascii=False)
                f.write("\n")

        print(f"📄 Logs exportados: {export_path} ({len(entries)} entradas)")
        return 0

    # Default: mostra últimas entradas
    entries = audit_logger.read_log(limit=10)
    print("\n" + "=" * 70)
    print("📊 ÚLTIMAS 10 ENTRADAS DE AUDITORIA")
    print("=" * 70)

    for entry in reversed(entries):
        print(f"\n⏱️  {entry['timestamp']}")
        print(f"   📋 Evento: {entry['event_type']}")
        if entry.get("user_feedback"):
            print(f"   💬 Feedback: {entry['user_feedback']}")

    print("\n" + "=" * 70 + "\n")
    return 0


def cmd_memory(args) -> int:
    """Comando: memory — Gerencia sistema de memória."""
    memory_store = MemoryStore()

    if args.show_stats:
        memory_store.print_memory_stats()
        return 0

    if args.record_feedback:
        # Formato: "tarefa|squad|feedback|notas"
        parts = args.record_feedback.split("|")
        if len(parts) < 3:
            print("❌ Formato inválido. Use: tarefa|squad|feedback[|notas]")
            return 2

        task, squad, feedback = parts[0], parts[1], parts[2]
        notes = parts[3] if len(parts) > 3 else ""

        memory_store.record_feedback(task, squad, feedback, notes)
        print(f"✅ Feedback registrado: {squad} ({feedback})")
        return 0

    if args.export_report:
        export_path = Path(args.export_report)
        report = memory_store.export_learning_report(export_path)
        print(f"📄 Relatório de aprendizagem: {export_path}")
        print(f"\n📊 {report['total_feedback_entries']} feedbacks registrados")
        print(f"🧠 {report['concepts_learned']} conceitos aprendidos")
        return 0

    # Default: mostra estatísticas
    memory_store.print_memory_stats()
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

    # Comando: activate
    activate_parser = subparsers.add_parser("activate", help="Gera contrato de ativação para um squad")
    activate_parser.add_argument("--index", required=True, help="Caminho do índice JSON")
    activate_parser.add_argument("--squad", required=True, help="Nome do squad a ativar")
    activate_parser.add_argument("--output-json", action="store_true", help="Saída em JSON (default: texto)")
    activate_parser.add_argument("--save", help="Salvar contrato em arquivo JSON")
    activate_parser.set_defaults(func=cmd_activate)

    # Comando: orchestrate (Fase 3)
    orch_parser = subparsers.add_parser("orchestrate", help="Pipeline completo com HITL, auditoria e memória")
    orch_parser.add_argument("--index", required=True, help="Caminho do índice JSON")
    orch_parser.add_argument("--task", required=True, help="Descrição da tarefa")
    orch_parser.add_argument("--context", help="Contexto adicional (optional)")
    orch_parser.add_argument("--domain", help="Domínio preferido (optional)")
    orch_parser.add_argument("--require-approval", action="store_true", help="Requer aprovação HITL")
    orch_parser.set_defaults(func=cmd_orchestrate)

    # Comando: logs (Fase 3)
    logs_parser = subparsers.add_parser("logs", help="Gerencia logs de auditoria")
    logs_parser.add_argument("--show-stats", action="store_true", help="Mostra estatísticas")
    logs_parser.add_argument("--export", help="Exporta logs para arquivo")
    logs_parser.set_defaults(func=cmd_logs)

    # Comando: memory (Fase 3)
    mem_parser = subparsers.add_parser("memory", help="Gerencia sistema de memória")
    mem_parser.add_argument("--show-stats", action="store_true", help="Mostra estatísticas de memória")
    mem_parser.add_argument("--record-feedback", help="Registra feedback: tarefa|squad|feedback[|notas]")
    mem_parser.add_argument("--export-report", help="Exporta relatório de aprendizagem")
    mem_parser.set_defaults(func=cmd_memory)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
