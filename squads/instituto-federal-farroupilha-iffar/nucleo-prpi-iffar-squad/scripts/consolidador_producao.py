#!/usr/bin/env python3
"""Consolidação determinística de produção científica/técnica declarada.

Lê a produção declarada por pesquisador (JSON) em um período de referência e
agrega por tipo de produção, detectando duplicidades (mesmo título/DOI
declarado mais de uma vez) e itens sem identificador mínimo (DOI/ISBN/registro)
quando exigido pelo tipo de produção.

Uso:
    python3 scripts/consolidador_producao.py --producao caminho/producao.json

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

TIPOS_QUE_EXIGEM_IDENTIFICADOR = {"artigo", "livro", "capitulo_livro", "patente", "registro_software"}


def chave_identificacao(item: dict) -> str:
    identificador = item.get("identificador")
    if identificador:
        return identificador
    return item.get("titulo", "").strip().lower()


def consolidar(dados: dict) -> dict:
    itens = dados.get("producao", [])

    por_tipo = defaultdict(int)
    sem_identificador = []
    chaves = Counter()
    duplicidades = []

    for item in itens:
        tipo = item.get("tipo")
        por_tipo[tipo] += 1

        if tipo in TIPOS_QUE_EXIGEM_IDENTIFICADOR and not item.get("identificador"):
            sem_identificador.append({"titulo": item.get("titulo"), "tipo": tipo, "pesquisador": item.get("pesquisador")})

        chave = chave_identificacao(item)
        chaves[chave] += 1

    for chave, qtd in chaves.items():
        if qtd > 1:
            duplicidades.append({"chave": chave, "ocorrencias": qtd})

    bloqueante = bool(sem_identificador) or bool(duplicidades)

    return {
        "total_itens": len(itens),
        "por_tipo": dict(por_tipo),
        "itens_sem_identificador": sem_identificador,
        "duplicidades": duplicidades,
        "gate_producao_consolidada": "liberado" if not bloqueante else "bloqueado",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--producao", required=True, help="arquivo JSON com a produção declarada por pesquisador")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho = Path(args.producao)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
        return 2
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(json.dumps({"erro": f"JSON inválido: {e}"}, ensure_ascii=False))
        return 2

    resultado = consolidar(dados)
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"resultado gravado em {args.saida}")
    else:
        print(saida)
    return 0 if resultado["gate_producao_consolidada"] == "liberado" else 1


if __name__ == "__main__":
    sys.exit(main())
