#!/usr/bin/env python3
"""Distribui o conteúdo programático de um componente nas aulas do semestre.

Cruza a lista de tópicos com o calendário (dias letivos, feriados e dias sem
aula), produzindo um cronograma data-a-data. Não decide conteúdo nem datas de
prova — apenas distribui o que foi informado e sinaliza se o número de aulas
disponíveis é insuficiente para o conteúdo programado.

Uso:
    python3 build_cronograma.py --topicos topicos.json --inicio 2026-08-03 \
        --fim 2026-12-18 --feriados feriados.json --dias-sem-aula 5,6 \
        --output cronograma.json
"""
from __future__ import annotations

import argparse
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sacp_common import is_dia_letivo, parse_date, read_json, write_json  # noqa: E402


def build(topicos: list[str], inicio, fim, feriados: set, dias_sem_aula: set[int]) -> dict:
    aulas = []
    d = inicio
    while d <= fim:
        if is_dia_letivo(d, feriados, dias_sem_aula):
            aulas.append(d)
        d += timedelta(days=1)

    cronograma = []
    conflito = len(topicos) > len(aulas)
    n = min(len(topicos), len(aulas))
    for i in range(n):
        cronograma.append({"data_aula": aulas[i].isoformat(), "topico": topicos[i]})

    topicos_sem_aula = topicos[n:] if conflito else []

    return {
        "cronograma": cronograma,
        "total_aulas_disponiveis": len(aulas),
        "total_topicos": len(topicos),
        "conflito_carga_horaria": conflito,
        "topicos_sem_aula_alocada": topicos_sem_aula,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--topicos", required=True, help="JSON com lista de tópicos (array de strings).")
    ap.add_argument("--inicio", required=True, help="Data de início do semestre (YYYY-MM-DD).")
    ap.add_argument("--fim", required=True, help="Data de término do semestre (YYYY-MM-DD).")
    ap.add_argument("--feriados", help="JSON com lista de datas de feriado (YYYY-MM-DD).")
    ap.add_argument("--dias-sem-aula", default="5,6", help="Weekdays sem aula, separados por vírgula (0=seg).")
    ap.add_argument("--output", required=True, help="Caminho do cronograma de saída (JSON).")
    args = ap.parse_args()

    topicos = read_json(args.topicos)
    inicio = parse_date(args.inicio)
    fim = parse_date(args.fim)
    feriados = set()
    if args.feriados:
        feriados = {parse_date(x) for x in read_json(args.feriados)}
    dias_sem_aula = {int(x) for x in args.dias_sem_aula.split(",") if x.strip()}

    resultado = build(topicos, inicio, fim, feriados, dias_sem_aula)
    write_json(args.output, resultado)

    if resultado["conflito_carga_horaria"]:
        print(
            f"[ALERTA] {len(resultado['topicos_sem_aula_alocada'])} tópico(s) sem aula "
            f"disponível no período informado. Revisão humana necessária.",
            file=sys.stderr,
        )
    print(f"Cronograma gerado em {args.output} ({len(resultado['cronograma'])} aulas alocadas).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
