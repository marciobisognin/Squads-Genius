#!/usr/bin/env python3
"""Gera um texto de PDI sintético para demonstrar a extração de metas.

Cria um .txt com dimensões, objetivos e metas numeradas, útil para rodar
build_goal_matrix.py em ambiente offline (sem expor documento institucional real).

Uso:
    python3 gerar_exemplo.py --output pdi_sintetico.txt
"""
from __future__ import annotations

import argparse
from pathlib import Path

TEXTO = """\
PLANO DE DESENVOLVIMENTO INSTITUCIONAL — CICLO 2027-2034 (EXEMPLO SINTÉTICO)

Dimensão: Acesso e Inclusão
Objetivo: Ampliar o acesso com equidade e permanência.
Meta 1.1 Elevar a taxa de ocupação de vagas para 95% até 2034.
Meta 1.2 Ampliar o número de ingressantes por ações afirmativas.

Dimensão: Permanência e Êxito
Objetivo: Reduzir a evasão e ampliar a conclusão.
Meta 2.1 Reduzir a taxa de evasão para abaixo de 12%.
Meta 2.2 Elevar a taxa de conclusão dos cursos técnicos.

Dimensão: Pesquisa e Inovação
Objetivo: Fortalecer a pesquisa aplicada e a inovação.
Meta 3.1 Dobrar o número de projetos de pesquisa com fomento.

Dimensão: Extensão
Objetivo: Ampliar o impacto territorial.
Meta 4.1 Atingir 30 mil pessoas em ações de extensão por ano.

Dimensão: Gestão de Pessoas
Objetivo: Qualificar o quadro de servidores.
Meta 5.1 Atingir 70% de docentes com doutorado.
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gera PDI sintético de exemplo.")
    ap.add_argument("--output", default="pdi_sintetico.txt")
    args = ap.parse_args(argv)
    Path(args.output).write_text(TEXTO, encoding="utf-8")
    print(f"OK: PDI sintético -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
