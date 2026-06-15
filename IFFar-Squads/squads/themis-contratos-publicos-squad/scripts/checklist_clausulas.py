#!/usr/bin/env python3
"""Pré-triagem heurística de cláusulas necessárias em contrato administrativo.

Busca por palavras-chave associadas às cláusulas do art. 92 da Lei 14.133/2021
em um arquivo de texto e gera relatório JSON. É uma PRIMEIRA PASSADA
determinística: ausência de palavra-chave não prova ausência da cláusula, nem
presença prova regularidade. A análise semântica fica com o agente
legalidade-lei14133-analyst e a revisão final é humana.

Uso:
    python3 scripts/checklist_clausulas.py --contrato caminho/contrato.txt [--saida relatorio.json]

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
import unicodedata
from pathlib import Path

# Cláusulas do art. 92 da Lei 14.133/2021 -> termos heurísticos de detecção
CLAUSULAS = {
    "objeto": ["objeto do contrato", "objeto:", "do objeto"],
    "vinculacao_edital_proposta": ["vinculação ao edital", "vinculado ao edital", "termos da proposta", "termo de referência"],
    "legislacao_aplicavel": ["lei nº 14.133", "lei n 14.133", "lei 14.133", "lei nº 8.666", "lei 8.666", "legislação aplicável"],
    "regime_execucao": ["regime de execução", "forma de fornecimento", "empreitada"],
    "preco_e_pagamento": ["valor do contrato", "preço", "condições de pagamento", "cronograma de pagamento"],
    "reajuste_e_repactuacao": ["reajuste", "repactuação", "índice de correção", "atualização monetária"],
    "dotacao_orcamentaria": ["dotação orçamentária", "nota de empenho", "recursos orçamentários", "classificação orçamentária"],
    "vigencia_e_prorrogacao": ["vigência", "prazo de vigência", "prorrogação"],
    "garantia": ["garantia contratual", "garantia de execução", "seguro-garantia", "caução"],
    "obrigacoes_das_partes": ["obrigações da contratada", "obrigações do contratante", "responsabilidades das partes"],
    "fiscalizacao": ["fiscalização", "fiscal do contrato", "gestor do contrato"],
    "sancoes_e_penalidades": ["sanções", "penalidades", "multa", "infrações administrativas"],
    "extincao_e_rescisao": ["extinção do contrato", "rescisão", "hipóteses de extinção"],
    "casos_omissos": ["casos omissos"],
    "matriz_de_riscos": ["matriz de riscos", "alocação de riscos"],
    "foro": ["foro", "comarca", "eleição de foro"],
    "publicacao_pncp": ["pncp", "portal nacional de contratações públicas", "publicação", "divulgação"],
    "anticorrupcao_integridade": ["anticorrupção", "lei nº 12.846", "lei 12.846", "programa de integridade", "compliance"],
    "protecao_de_dados": ["lgpd", "lei geral de proteção de dados", "lei nº 13.709", "proteção de dados"],
}


def normalizar(texto: str) -> str:
    texto = texto.lower()
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def analisar(texto: str) -> dict:
    norm = normalizar(texto)
    itens = {}
    for clausula, termos in CLAUSULAS.items():
        encontrados = [t for t in termos if normalizar(t) in norm]
        itens[clausula] = {
            "status": "indicio_presente" if encontrados else "nao_localizada",
            "termos_encontrados": encontrados,
        }
    presentes = sum(1 for v in itens.values() if v["status"] == "indicio_presente")
    return {
        "metodo": "heuristica_por_palavras_chave",
        "aviso": "Primeira passada determinística. Não substitui análise semântica nem revisão humana.",
        "referencia": "art. 92 da Lei 14.133/2021 (verificar regime aplicável ao contrato)",
        "total_clausulas_verificadas": len(itens),
        "indicios_presentes": presentes,
        "nao_localizadas": len(itens) - presentes,
        "itens": itens,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--contrato", required=True, help="arquivo de texto com o contrato")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho = Path(args.contrato)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
        return 2
    texto = caminho.read_text(encoding="utf-8", errors="ignore")
    if not texto.strip():
        print(json.dumps({"erro": "arquivo vazio"}, ensure_ascii=False))
        return 2

    relatorio = analisar(texto)
    saida = json.dumps(relatorio, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"relatório gravado em {args.saida}")
    else:
        print(saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
