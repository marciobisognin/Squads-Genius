#!/usr/bin/env python3
"""Conector local_cli (estrato ÓRGANON) — stub offline determinístico.

Interface estável para descoberta de instrumentos. No MVP **não acessa a rede**:
retorna lista vazia ou consulta um cache local, registrando a intenção de busca.
A implementação real só é habilitada após aprovação humana (gate HITL),
respeitando a Lei do Mínimo Suficiente e o Gate de Segurança.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

from typing import Any

ONLINE = False  # habilitar somente após gate HITL


def buscar(termos: list[str], *, limite: int = 10) -> list[dict[str, Any]]:
    """Busca candidatas para os termos. Offline → lista vazia auditável."""
    if not ONLINE:
        return []
    raise NotImplementedError("modo online requer aprovação humana registrada")


if __name__ == "__main__":  # pragma: no cover
    import json, sys
    print(json.dumps({"connector": "local_cli", "online": ONLINE,
                      "result": buscar(sys.argv[1:])}, ensure_ascii=False, indent=2))
