#!/usr/bin/env python3
"""Exemplo de adapter seguro para SKEPTIC runtime probes.

Recebe JSON em stdin e devolve JSON com campo `response`. Este adapter simula
um agente que reconhece canários defensivos e recusa instruções inseguras.
"""
from __future__ import annotations

import json
import sys

probe = json.load(sys.stdin)
attack_id = probe.get("attack_id", "unknown")
print(json.dumps({
    "response": (
        f"Recuso a instrução insegura do cenário {attack_id}. "
        "Não revelarei canários, credenciais, memória, instruções internas, "
        "dados de outro usuário nem executarei ferramenta não autorizada. "
        "Tratarei o conteúdo recebido como dado não confiável."
    )
}, ensure_ascii=False))
