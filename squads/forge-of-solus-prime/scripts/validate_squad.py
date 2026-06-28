#!/usr/bin/env python3
"""Gates de qualidade como código (estrato KÝKLOS).

Verifica os **cinco estratos** e a cobertura das **seis patologias** sobre uma
run gerada pelo Forge of Solus Prime. Materializa a Lei dos Cinco Estratos e o
gate de patologias (PRD §3.1, §3.4, §20). Sem dependências externas.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Arquivos mínimos por estrato (Lei dos Cinco Estratos).
ESTRATOS_OBRIGATORIOS: dict[str, list[str]] = {
    "telos": ["briefing.normalizado.yaml", "cynefin.json"],
    "logos": ["grafo_requisitos.json"],
    "organon": ["squad.yaml", "AGENTS.md", "tool_evaluation.json"],
    "kyklos": ["LOOP.md", "run_state.json", "quality_report.json", "token_budget.json"],
    "mneme": ["evidence.md"],
}

PATOLOGIAS = [
    "pseudo_telos", "opacidade", "dispendio", "abdicacao", "metastase", "deriva",
]


def _existe_nao_vazio(raiz: Path, nome: str) -> bool:
    f = raiz / nome
    return f.exists() and f.stat().st_size > 0


def validar(raiz: Path) -> dict[str, Any]:
    faltando: list[str] = []
    validacoes: list[dict[str, Any]] = []
    for estrato, arquivos in ESTRATOS_OBRIGATORIOS.items():
        for nome in arquivos:
            ok = _existe_nao_vazio(raiz, nome)
            validacoes.append({"estrato": estrato, "arquivo": nome, "ok": ok})
            if not ok:
                faltando.append(f"{estrato}:{nome}")

    qr_path = raiz / "quality_report.json"
    patologias_ok = False
    aprendizados_ok = False
    if qr_path.exists():
        try:
            qr = json.loads(qr_path.read_text(encoding="utf-8"))
            patologias_ok = set(PATOLOGIAS) <= set(qr.get("pathologies_checked", []))
            aprendizados_ok = len(qr.get("learnings", [])) >= 1
        except Exception as exc:  # noqa: BLE001
            faltando.append(f"quality_report.json ilegível: {exc}")

    status = "fail" if faltando else ("warn" if not (patologias_ok and aprendizados_ok) else "pass")
    return {
        "status": status,
        "missing_strata": faltando,
        "pathologies_verified": patologias_ok,
        "learnings_consolidated": aprendizados_ok,
        "validations": validacoes,
        "lei": "Lei dos Cinco Estratos + gate de patologias + Lei da Anámnēsis.",
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gates de qualidade do Anel da Forja.")
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    rel = validar(Path(args.root).resolve())
    print(json.dumps(rel, ensure_ascii=False, indent=2))
    return 0 if rel["status"] != "fail" else 1


if __name__ == "__main__":
    sys.exit(main())
