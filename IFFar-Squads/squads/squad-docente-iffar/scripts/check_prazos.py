#!/usr/bin/env python3
"""Verifica prazos institucionais (PROEN/RDP) e emite alertas escalonados.

Regra determinística: compara cada prazo da agenda com a data de referência e
classifica em alerta_antecedencia_longa, alerta_antecedencia_curta ou vencido,
conforme limiares configuráveis.

Uso:
    python3 check_prazos.py --agenda agenda_prazos.json --hoje 2026-06-18 \
        --output alertas.json
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sacp_common import days_until, parse_date, read_json, write_json  # noqa: E402

LIMIAR_LONGA = 15
LIMIAR_CURTA = 5


def classify(dias_restantes: int) -> str:
    if dias_restantes < 0:
        return "vencido"
    if dias_restantes <= LIMIAR_CURTA:
        return "alerta_antecedencia_curta"
    if dias_restantes <= LIMIAR_LONGA:
        return "alerta_antecedencia_longa"
    return "sem_alerta"


def build(agenda: list[dict], hoje) -> dict:
    alertas = []
    checklist = {"total": len(agenda), "vencidos": 0, "em_alerta": 0, "ok": 0}
    for item in agenda:
        prazo = parse_date(item.get("data_limite", ""))
        if prazo is None:
            alertas.append({**item, "status": "data_invalida"})
            continue
        dias = days_until(prazo, hoje)
        status = classify(dias)
        alertas.append({**item, "dias_restantes": dias, "status": status})
        if status == "vencido":
            checklist["vencidos"] += 1
        elif status.startswith("alerta"):
            checklist["em_alerta"] += 1
        else:
            checklist["ok"] += 1
    return {"alertas": alertas, "checklist_conformidade": checklist}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agenda", required=True, help="JSON com lista de prazos (data_limite, descricao, dispositivo_rdp).")
    ap.add_argument("--hoje", help="Data de referência (YYYY-MM-DD); padrão é a data atual.")
    ap.add_argument("--output", required=True, help="Saída de alertas e checklist (JSON).")
    args = ap.parse_args()

    agenda = read_json(args.agenda)
    hoje = parse_date(args.hoje) if args.hoje else None
    resultado = build(agenda, hoje)
    write_json(args.output, resultado)

    print(
        f"Prazos verificados: {resultado['checklist_conformidade']['vencidos']} vencido(s), "
        f"{resultado['checklist_conformidade']['em_alerta']} em alerta."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
