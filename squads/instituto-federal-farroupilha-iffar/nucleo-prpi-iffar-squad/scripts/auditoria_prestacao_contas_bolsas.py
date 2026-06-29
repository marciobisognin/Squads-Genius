#!/usr/bin/env python3
"""Auditoria determinística da prestação de contas de bolsas individuais.

Lê os dados de bolsas (vigência e documentos exigidos) e os documentos
declarados como entregues (JSON), conferindo se a documentação obrigatória
de prestação de contas (relatório final, TCR, comprovantes quando aplicável)
foi entregue e se o período coberto corresponde à vigência da bolsa.

Uso:
    python3 scripts/auditoria_prestacao_contas_bolsas.py --bolsas caminho/bolsas.json

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from pathlib import Path


def auditar_bolsa(bolsa: dict) -> dict:
    bolsa_id = bolsa.get("bolsa_id")
    documentos_exigidos = set(bolsa.get("documentos_exigidos", []))
    documentos_entregues = set(bolsa.get("documentos_entregues", []))
    documentos_ausentes = sorted(documentos_exigidos - documentos_entregues)

    periodo_coberto = bolsa.get("periodo_coberto_relatorio")
    vigencia = bolsa.get("vigencia")
    divergencias = []
    if periodo_coberto and vigencia and periodo_coberto != vigencia:
        divergencias.append({
            "motivo": "periodo_coberto_diferente_da_vigencia",
            "periodo_coberto_relatorio": periodo_coberto,
            "vigencia": vigencia,
        })

    if documentos_ausentes:
        classificacao = "pendência documental"
    elif divergencias:
        classificacao = "divergência a esclarecer"
    else:
        classificacao = "prestação de contas completa"

    return {
        "bolsa_id": bolsa_id,
        "documentos_ausentes": documentos_ausentes,
        "divergencias": divergencias,
        "classificacao": classificacao,
    }


def auditar(dados: dict) -> dict:
    bolsas = dados.get("bolsas", [])
    resultados = [auditar_bolsa(b) for b in bolsas]
    bloqueante = any(r["classificacao"] != "prestação de contas completa" for r in resultados)

    return {
        "total_bolsas": len(bolsas),
        "resultados": resultados,
        "gate_prestacao_contas_auditada": "liberado" if not bloqueante else "bloqueado",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bolsas", required=True, help="arquivo JSON com bolsas, documentos exigidos e entregues")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho = Path(args.bolsas)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
        return 2
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(json.dumps({"erro": f"JSON inválido: {e}"}, ensure_ascii=False))
        return 2

    resultado = auditar(dados)
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"resultado gravado em {args.saida}")
    else:
        print(saida)
    return 0 if resultado["gate_prestacao_contas_auditada"] == "liberado" else 1


if __name__ == "__main__":
    sys.exit(main())
