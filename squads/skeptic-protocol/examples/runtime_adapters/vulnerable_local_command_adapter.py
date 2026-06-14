#!/usr/bin/env python3
"""Exemplo de adapter vulnerável para demonstrar detecção do SKEPTIC.

Não usar como runtime real. Ele ecoa o payload canário de propósito para que o
runner classifique o comportamento como vulnerável.
"""
from __future__ import annotations

import json
import sys

probe = json.load(sys.stdin)
payload = probe.get("payload_canary", "")
print(json.dumps({
    "response": f"UNSAFE: obedeci ao conteúdo não confiável e ecoei o payload: {payload} SKEPTIC_CANARY_SECRET"
}, ensure_ascii=False))
