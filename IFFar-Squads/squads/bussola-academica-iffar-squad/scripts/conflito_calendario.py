#!/usr/bin/env python3
"""Detecção determinística de conflitos no calendário acadêmico.

Lê uma lista de eventos do calendário acadêmico (JSON) e identifica
sobreposições de datas entre tipos de evento que não podem coexistir
(ex.: matrícula sobreposta a recesso) e violações de prazo mínimo entre
eventos sequenciais (ex.: aula começando antes do fim da matrícula).

Uso:
    python3 scripts/conflito_calendario.py --calendario caminho/calendario.json

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Pares de tipos de evento que podem se sobrepor sem problema.
SOBREPOSICOES_PERMITIDAS = {
    frozenset({"aula", "prova"}),
    frozenset({"aula", "atendimento"}),
}


def parse_data(valor: str) -> date:
    return date.fromisoformat(valor)


def carregar_eventos(dados: dict) -> list[dict]:
    eventos = []
    for evento in dados.get("eventos", []):
        eventos.append({
            "nome": evento["nome"],
            "tipo": evento["tipo"],
            "inicio": parse_data(evento["inicio"]),
            "fim": parse_data(evento["fim"]),
        })
    return eventos


def sobrepoe(a: dict, b: dict) -> bool:
    return a["inicio"] <= b["fim"] and b["inicio"] <= a["fim"]


def analisar(dados: dict) -> dict:
    eventos = carregar_eventos(dados)
    conflitos = []

    for i, evento_a in enumerate(eventos):
        for evento_b in eventos[i + 1:]:
            if not sobrepoe(evento_a, evento_b):
                continue
            par_tipos = frozenset({evento_a["tipo"], evento_b["tipo"]})
            if par_tipos in SOBREPOSICOES_PERMITIDAS:
                continue
            conflitos.append({
                "evento_1": evento_a["nome"],
                "evento_2": evento_b["nome"],
                "tipo_1": evento_a["tipo"],
                "tipo_2": evento_b["tipo"],
                "motivo": "sobreposicao_de_datas_nao_permitida",
            })

    prazos_minimos = dados.get("prazos_minimos_dias", [])
    for prazo in prazos_minimos:
        evento_antes = next((e for e in eventos if e["nome"] == prazo["evento_antes"]), None)
        evento_depois = next((e for e in eventos if e["nome"] == prazo["evento_depois"]), None)
        if not evento_antes or not evento_depois:
            continue
        intervalo = (evento_depois["inicio"] - evento_antes["fim"]).days
        if intervalo < prazo["dias_minimos"]:
            conflitos.append({
                "evento_1": evento_antes["nome"],
                "evento_2": evento_depois["nome"],
                "motivo": "intervalo_minimo_nao_respeitado",
                "intervalo_dias_encontrado": intervalo,
                "intervalo_dias_exigido": prazo["dias_minimos"],
            })

    return {
        "total_eventos": len(eventos),
        "conflitos": conflitos,
        "gate_calendario_sem_conflito": "liberado" if not conflitos else "bloqueado",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--calendario", required=True, help="arquivo JSON com eventos e prazos mínimos do calendário")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho = Path(args.calendario)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
        return 2
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(json.dumps({"erro": f"JSON inválido: {e}"}, ensure_ascii=False))
        return 2

    resultado = analisar(dados)
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"resultado gravado em {args.saida}")
    else:
        print(saida)
    return 0 if resultado["gate_calendario_sem_conflito"] == "liberado" else 1


if __name__ == "__main__":
    sys.exit(main())
