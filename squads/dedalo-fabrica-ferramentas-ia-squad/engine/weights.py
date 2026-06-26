#!/usr/bin/env python3
"""Pesos versionados (semver) do motor determinístico de priorização do DÉDALO.

Mantidos isolados para auditoria: qualquer mudança de peso é uma mudança de versão
explícita e rastreável. O LLM nunca toca nestes valores — apenas o Python os usa.
"""
from __future__ import annotations

# Versão dos pesos. Mudou o peso? Mude a versão (semver).
WEIGHTS_VERSION = "1.0.0"

# Pesos da função de score de oportunidade (ver engine/scoring.py).
# Soma dos termos positivos = 0.70; penalidades = 0.30.
WEIGHTS_V1 = {
    "impact": 0.35,
    "repetition": 0.20,
    "data_availability": 0.15,
    "effort_penalty": 0.15,
    "risk_penalty": 0.15,
}

# Limiar abaixo do qual uma oportunidade exige justificativa explícita para prosseguir.
SCORE_THRESHOLD = 0.45


def weights_fingerprint(weights: dict[str, float] = WEIGHTS_V1) -> str:
    """Assinatura estável dos pesos, para registrar em provenance/observabilidade."""
    items = ",".join(f"{k}={weights[k]}" for k in sorted(weights))
    return f"weights_v{WEIGHTS_VERSION}:{items}"


if __name__ == "__main__":
    print(weights_fingerprint())
