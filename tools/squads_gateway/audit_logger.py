"""Audit Logger — Fase 3 do Gateway.

Log estruturado em JSONL com rastreamento completo de decisões.
Cada entrada contém: timestamp, tipo de evento, request, resultado, feedback, hash.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from .schemas import AuditLogEntry


class AuditLogger:
    """Logger de auditoria para o Squads Gateway."""

    def __init__(self, log_path: Path = None):
        """Inicializa logger.

        Args:
            log_path: Caminho do arquivo JSONL (default: gateway_audit.log)
        """
        self.log_path = log_path or Path("gateway_audit.log")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_event(
        self,
        event_type: str,
        request_data: dict[str, Any],
        result_data: dict[str, Any],
        user_feedback: Optional[str] = None,
    ) -> str:
        """Registra um evento no log de auditoria.

        Args:
            event_type: Tipo de evento (index | search | route | activate | feedback)
            request_data: Dados da requisição
            result_data: Dados do resultado
            user_feedback: Feedback do usuário (success | failure | neutral)

        Returns:
            Hash único do evento para rastreamento
        """
        # Cria hash único da decisão
        decision_hash = self._compute_decision_hash(event_type, request_data, result_data)

        # Cria entrada de auditoria
        entry = AuditLogEntry(
            timestamp=datetime.utcnow().isoformat(),
            event_type=event_type,
            request_data=request_data,
            result_data=result_data,
            user_feedback=user_feedback,
            decision_hash=decision_hash,
        )

        # Escreve no arquivo JSONL
        with open(self.log_path, "a", encoding="utf-8") as f:
            line = json.dumps(entry.to_dict(), ensure_ascii=False)
            f.write(line + "\n")

        return decision_hash

    def log_index_event(self, squad_count: int, broken_links: int) -> str:
        """Registra evento de indexação."""
        request = {"repo_root": "."}
        result = {"total_squads": squad_count, "broken_links": broken_links}
        return self.log_event("index", request, result)

    def log_search_event(self, term: str, results_count: int, top_match: Optional[str] = None) -> str:
        """Registra evento de busca."""
        request = {"search_term": term}
        result = {"results_count": results_count, "top_match": top_match}
        return self.log_event("search", request, result)

    def log_route_event(
        self,
        task: str,
        top_match: Optional[str],
        score: float,
        matched_keywords: list[str],
    ) -> str:
        """Registra evento de roteamento."""
        request = {"task_description": task}
        result = {
            "top_match": top_match,
            "score": score,
            "matched_keywords": matched_keywords,
        }
        return self.log_event("route", request, result)

    def log_activate_event(self, squad_name: str, entry_agent: str) -> str:
        """Registra evento de ativação."""
        request = {"squad_name": squad_name}
        result = {"entry_point_agent": entry_agent}
        return self.log_event("activate", request, result)

    def log_feedback(self, decision_hash: str, feedback: str, notes: str = "") -> None:
        """Registra feedback sobre uma decisão anterior.

        Args:
            decision_hash: Hash do evento original
            feedback: success | failure | neutral
            notes: Notas adicionais do usuário
        """
        request = {"decision_hash": decision_hash}
        result = {"feedback_notes": notes}
        self.log_event("feedback", request, result, user_feedback=feedback)

    @staticmethod
    def _compute_decision_hash(event_type: str, request: dict, result: dict) -> str:
        """Computa hash SHA256 da decisão para rastreamento."""
        # Cria string determinística (ordenada)
        data = {
            "event_type": event_type,
            "request": json.dumps(request, sort_keys=True, ensure_ascii=False),
            "result": json.dumps(result, sort_keys=True, ensure_ascii=False),
        }
        signature = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(signature.encode()).hexdigest()[:16]

    def read_log(self, limit: int = None) -> list[dict[str, Any]]:
        """Lê todas as entradas do log.

        Args:
            limit: Máximo de entradas (default: todas)

        Returns:
            Lista de dicts com as entradas
        """
        entries = []
        if not self.log_path.exists():
            return entries

        with open(self.log_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if limit and i >= limit:
                    break
                try:
                    entry = json.loads(line)
                    entries.append(entry)
                except json.JSONDecodeError:
                    continue

        return entries

    def get_event_stats(self) -> dict[str, Any]:
        """Retorna estatísticas de eventos registrados."""
        entries = self.read_log()

        stats = {
            "total_events": len(entries),
            "events_by_type": {},
            "feedback_summary": {"success": 0, "failure": 0, "neutral": 0},
        }

        for entry in entries:
            event_type = entry.get("event_type", "unknown")
            stats["events_by_type"][event_type] = stats["events_by_type"].get(event_type, 0) + 1

            feedback = entry.get("user_feedback")
            if feedback in stats["feedback_summary"]:
                stats["feedback_summary"][feedback] += 1

        return stats

    def print_stats(self) -> None:
        """Imprime estatísticas do log."""
        stats = self.get_event_stats()

        print("\n" + "=" * 70)
        print("📊 AUDIT LOG STATISTICS")
        print("=" * 70)
        print(f"\n📈 Total de eventos: {stats['total_events']}")

        print(f"\n📋 Por tipo de evento:")
        for event_type in sorted(stats["events_by_type"].keys()):
            count = stats["events_by_type"][event_type]
            print(f"   {event_type:12s}: {count:4d}")

        print(f"\n💬 Feedback recebido:")
        for feedback_type in ["success", "failure", "neutral"]:
            count = stats["feedback_summary"][feedback_type]
            if count > 0:
                print(f"   {feedback_type:12s}: {count:4d}")

        print("\n" + "=" * 70 + "\n")
