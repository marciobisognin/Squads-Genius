#!/usr/bin/env python3
"""Estatísticas determinísticas da cesta de preços (método IN SEGES 65/2021).

Lê o CSV da pesquisa de preços (colunas: item;fonte;identificacao_fonte;data;
valor_unitario;quantidade) e calcula por item: média, mediana, menor preço,
coeficiente de variação e sinalização de possíveis outliers (preços que se
desviam da mediana além do limiar).

A escolha do critério do valor estimado (média, mediana ou menor preço) e o
descarte de cotações são DECISÕES registradas pelo agente, não do script.

Uso:
    python3 scripts/analise_pesquisa_precos.py --planilha cotacoes.csv [--limiar-outlier 0.25]

Sem dependências externas (Python 3.11+).
"""
import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path


def carregar(caminho: Path) -> dict[str, list[dict]]:
    itens: dict[str, list[dict]] = defaultdict(list)
    with caminho.open(encoding="utf-8") as f:
        leitor = csv.DictReader(f, delimiter=";")
        obrigatorias = {"item", "fonte", "identificacao_fonte", "data", "valor_unitario"}
        faltam = obrigatorias - set(leitor.fieldnames or [])
        if faltam:
            raise ValueError(f"colunas ausentes no CSV: {sorted(faltam)} (separador esperado: ';')")
        for n, linha in enumerate(leitor, start=2):
            try:
                valor = float(str(linha["valor_unitario"]).replace("R$", "").replace(".", "").replace(",", ".").strip()
                              if "," in str(linha["valor_unitario"]) else str(linha["valor_unitario"]).replace("R$", "").strip())
            except ValueError:
                raise ValueError(f"linha {n}: valor_unitario inválido: {linha['valor_unitario']!r}")
            if valor <= 0:
                raise ValueError(f"linha {n}: valor_unitario deve ser positivo")
            if not str(linha["fonte"]).strip() or not str(linha["data"]).strip():
                raise ValueError(f"linha {n}: cotação sem fonte ou sem data não entra na cesta (IN 65/2021)")
            itens[str(linha["item"]).strip()].append({
                "fonte": linha["fonte"].strip(),
                "identificacao_fonte": linha["identificacao_fonte"].strip(),
                "data": linha["data"].strip(),
                "valor_unitario": valor,
            })
    return itens


def analisar_item(cotacoes: list[dict], limiar: float) -> dict:
    valores = [c["valor_unitario"] for c in cotacoes]
    media = statistics.mean(valores)
    mediana = statistics.median(valores)
    menor = min(valores)
    desvio = statistics.stdev(valores) if len(valores) > 1 else 0.0
    cv = (desvio / media) if media else 0.0
    outliers = [
        {**c, "desvio_relativo_mediana": round(abs(c["valor_unitario"] - mediana) / mediana, 4)}
        for c in cotacoes
        if mediana and abs(c["valor_unitario"] - mediana) / mediana > limiar
    ]
    alertas = []
    if len(valores) < 3:
        alertas.append("menos de 3 cotações: justificar formalmente (IN 65/2021)")
    if len({c["fonte"] for c in cotacoes}) < 2:
        alertas.append("fonte única: diversificar fontes ou justificar")
    if cv > limiar:
        alertas.append(f"coeficiente de variação {cv:.2%} acima do limiar {limiar:.0%}: avaliar consistência da cesta")
    return {
        "n_cotacoes": len(valores),
        "media": round(media, 2),
        "mediana": round(mediana, 2),
        "menor_preco": round(menor, 2),
        "coeficiente_variacao": round(cv, 4),
        "possiveis_outliers": outliers,
        "alertas": alertas,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--planilha", required=True, help="CSV da cesta de preços (separador ';')")
    ap.add_argument("--limiar-outlier", type=float, default=0.25, help="desvio relativo à mediana para sinalizar outlier (padrão 0.25)")
    ap.add_argument("--saida", default=None, help="arquivo JSON de saída (padrão: stdout)")
    args = ap.parse_args()

    caminho = Path(args.planilha)
    if not caminho.is_file():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
        return 2
    try:
        itens = carregar(caminho)
    except ValueError as e:
        print(json.dumps({"erro": str(e)}, ensure_ascii=False))
        return 2
    if not itens:
        print(json.dumps({"erro": "planilha sem cotações"}, ensure_ascii=False))
        return 2

    resultado = {
        "metodo": "estatísticas da cesta de preços (IN SEGES 65/2021)",
        "limiar_outlier": args.limiar_outlier,
        "itens": {item: analisar_item(cots, args.limiar_outlier) for item, cots in itens.items()},
        "observacao": "Critério do valor estimado (média/mediana/menor) e descarte de outliers são decisões do agente, registradas no relatório, com revisão humana.",
    }
    saida = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(saida, encoding="utf-8")
        print(f"resultado gravado em {args.saida}")
    else:
        print(saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
