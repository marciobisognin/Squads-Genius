#!/usr/bin/env python3
"""Auditoria do Protocolo de Limiar de Concessão (primitiva 6.3 — anti-bajulação).

Recebe o log do contraditório (cada réplica do autor pontuada de 1 a 5 ANTES da
resposta) e verifica as regras anti-bajulação de forma determinística:

  1. Concessão só é permitida com pontuação >= 4.
  2. Sem concessões consecutivas.
  3. Reporta a taxa de concessão (não a suaviza).

Cada entrada do log:
  { "rodada": 1, "ataque": "...", "replica_autor": "...",
    "pontuacao": 4, "acao": "concede" | "mantem" }

Uso:
    python3 scripts/concession_audit.py --log examples/fixtures/contraditorio_log.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LIMIAR = 4


def audit(log: list[dict]) -> dict:
    violacoes: list[str] = []
    concessoes = 0
    prev_concedeu = False

    for e in log:
        rodada = e.get("rodada")
        acao = e.get("acao")
        pont = e.get("pontuacao")
        if acao == "concede":
            concessoes += 1
            if pont is None or pont < LIMIAR:
                violacoes.append(
                    f"rodada {rodada}: concessão com pontuação {pont} < {LIMIAR} (proibida)."
                )
            if prev_concedeu:
                violacoes.append(
                    f"rodada {rodada}: concessão consecutiva (proibida)."
                )
            prev_concedeu = True
        else:
            prev_concedeu = False

    total = len(log)
    return {
        "total_replicas": total,
        "concessoes": concessoes,
        "taxa_de_concessao": round(concessoes / total, 3) if total else 0.0,
        "violacoes": violacoes,
        "anti_bajulacao_ok": not violacoes,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    args = ap.parse_args()
    log = json.loads(Path(args.log).read_text(encoding="utf-8"))
    report = audit(log)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["anti_bajulacao_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
