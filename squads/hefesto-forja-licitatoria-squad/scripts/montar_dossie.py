#!/usr/bin/env python3
"""Montagem determinística do índice do dossiê do processo.

Varre a pasta do processo e confere os artefatos obrigatórios conforme o
fluxo (licitacao ou direta), gerando o índice do dossiê em Markdown com
presentes/ausentes — insumo do gate dossie_conforme_e_revisao_humana.

Uso:
    python3 scripts/montar_dossie.py --pasta processos/meu-processo --fluxo licitacao

Sem dependências externas (Python 3.11+).
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path

ARTEFATOS = {
    "licitacao": [
        ("relatorio_intake", "Relatório de intake e suficiência"),
        ("nota_enquadramento", "Nota de enquadramento de modalidade"),
        ("dfd", "Documento de Formalização da Demanda"),
        ("etp", "Estudo Técnico Preliminar"),
        ("pesquisa_precos", "Planilha da pesquisa de preços (CSV)"),
        ("relatorio_pesquisa_precos", "Relatório da pesquisa de preços"),
        ("matriz_riscos", "Matriz de riscos da contratação"),
        ("termo_referencia", "Termo de referência / projeto básico"),
        ("edital", "Edital e anexos"),
        ("minuta_contrato", "Minuta de contrato"),
        ("nota_conformidade", "Nota de conformidade"),
    ],
    "direta": [
        ("relatorio_intake", "Relatório de intake e suficiência"),
        ("nota_enquadramento", "Nota de enquadramento (hipótese arts. 74/75)"),
        ("dfd", "Documento de Formalização da Demanda"),
        ("etp", "Estudo Técnico Preliminar (quando exigível)"),
        ("pesquisa_precos", "Planilha/justificativa de preço (CSV)"),
        ("relatorio_pesquisa_precos", "Relatório da pesquisa/justificativa de preço"),
        ("termo_referencia", "Termo de referência"),
        ("aviso_contratacao_direta", "Aviso de contratação direta + razão da escolha"),
        ("minuta_contrato", "Minuta de contrato ou instrumento equivalente"),
        ("nota_conformidade", "Nota de conformidade"),
    ],
}


def localizar(pasta: Path, chave: str):
    achados = sorted(p for p in pasta.rglob(f"*{chave}*") if p.is_file())
    return achados[0] if achados else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pasta", required=True, help="pasta do processo forjado")
    ap.add_argument("--fluxo", choices=["licitacao", "direta"], default="licitacao")
    ap.add_argument("--saida", default=None, help="arquivo do índice (padrão: <pasta>/00_indice_dossie.md)")
    args = ap.parse_args()

    pasta = Path(args.pasta)
    if not pasta.is_dir():
        print(json.dumps({"erro": f"pasta não encontrada: {pasta}"}, ensure_ascii=False))
        return 2

    linhas = [
        f"# Índice do Dossiê — {pasta.name}",
        "",
        f"- **Fluxo:** {args.fluxo}",
        f"- **Gerado em:** {date.today().isoformat()} (montar_dossie.py — verificação de PRESENÇA de arquivos; conteúdo é auditado pelo conformidade-dossie-auditor)",
        "",
        "| # | Artefato | Arquivo | Status |",
        "|---|---|---|---|",
    ]
    ausentes = []
    for i, (chave, nome) in enumerate(ARTEFATOS[args.fluxo], start=1):
        arq = localizar(pasta, chave)
        if arq:
            linhas.append(f"| {i} | {nome} | `{arq.relative_to(pasta)}` | presente |")
        else:
            linhas.append(f"| {i} | {nome} | — | **AUSENTE** |")
            ausentes.append(nome)

    linhas += [
        "",
        f"**Resultado:** {'COMPLETO (presença de arquivos)' if not ausentes else f'PENDENTE — {len(ausentes)} artefato(s) ausente(s)'}",
        "",
        "> Handoff humano obrigatório: adaptação aos modelos oficiais AGU/CNMLC, análise jurídica (art. 53 da Lei 14.133/2021) e autorização da autoridade competente.",
        "",
        "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.",
    ]

    destino = Path(args.saida) if args.saida else pasta / "00_indice_dossie.md"
    destino.write_text("\n".join(linhas), encoding="utf-8")
    print(json.dumps({"indice": str(destino), "ausentes": ausentes, "completo": not ausentes}, ensure_ascii=False, indent=2))
    return 0 if not ausentes else 1


if __name__ == "__main__":
    sys.exit(main())
