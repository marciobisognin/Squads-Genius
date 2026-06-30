"""Squads Gateway — Catálogo vivo e roteador de execução.

PRD: Indexar, buscar, rotear e executar squads com auditoria completa.
Componentes: indexer, ranker, router, contract_builder, audit_logger.
"""

__version__ = "0.1.0"
__author__ = "Marcio Bisognin"

from .schemas import IndexEntry, RouteRequest, RouteDecision, ActivationContract

__all__ = [
    "IndexEntry",
    "RouteRequest",
    "RouteDecision",
    "ActivationContract",
]
