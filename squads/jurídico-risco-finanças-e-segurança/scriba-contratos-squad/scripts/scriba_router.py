#!/usr/bin/env python3
"""Instrument Router do Squad SCRIBA — tabela-decisão §11 do Compêndio.

Regras puras (sem LLM): dado o conjunto de fatos da situação (`ContractFacts`),
decide qual instrumento gerar — minuta inicial, termo aditivo, apostilamento ou
repactuação — com `rationale` e `legal_refs` anexados, replicando o Anexo B do
PRD (Tabela-decisão do Instrument Router).

A ordem de avaliação importa: situações que exigem termo aditivo (inovam a
base contratual) são checadas antes das que admitem apostilamento (apenas
registram efeito de cláusula já existente).

Sem dependências externas. Python 3.11+.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import List, Optional

INSTRUMENTOS = ("minuta_inicial", "termo_aditivo", "apostilamento", "repactuacao")


@dataclass
class ContractFacts:
    """Situação detectada (entrada do Router). Cada campo corresponde a uma
    linha da tabela-decisão do compêndio (§11)."""

    nova_contratacao: bool = False
    prorrogar_prazo: bool = False
    acrescimo_supressao_quantitativo: bool = False
    alteracao_qualitativa_objeto: bool = False
    reajuste_indice_ja_previsto: bool = False
    repactuacao_prevista_sem_renegociacao: bool = False
    repactuacao_com_demonstracao_analitica: bool = False
    reequilibrio_economico_financeiro: bool = False
    mudanca_dados_cadastrais_ou_empenho: bool = False


@dataclass
class RouterDecision:
    instrument_type: str
    rationale: str
    legal_refs: List[str]
    needs_hitl: bool
    hitl_gate: Optional[str]

    def to_dict(self) -> dict:
        return asdict(self)


def rotear_instrumento(facts: ContractFacts) -> RouterDecision:
    """Aplica a tabela-decisão. Lança ValueError se nenhuma situação reconhecida
    (caso Cynefin Complex — deve subir para HITL antes do roteamento)."""

    if facts.nova_contratacao:
        return RouterDecision(
            "minuta_inicial",
            "Formalização de contratação nova após licitação/contratação direta.",
            ["L14133:arts.89-95"], False, None)

    if facts.prorrogar_prazo:
        return RouterDecision(
            "termo_aditivo",
            "Prorrogação de prazo de serviço contínuo (até 60 meses, art. 107).",
            ["L14133:art.107"], True, "A")

    if facts.acrescimo_supressao_quantitativo:
        return RouterDecision(
            "termo_aditivo",
            "Acréscimo/supressão de quantitativo (±25% ou 50% em reforma).",
            ["L14133:arts.124-125", "TCU:Ac.749/2010"], True, "A")

    if facts.alteracao_qualitativa_objeto:
        return RouterDecision(
            "termo_aditivo",
            "Alteração qualitativa do objeto.",
            ["L14133:art.124,I"], True, "A")

    if facts.repactuacao_com_demonstracao_analitica:
        return RouterDecision(
            "termo_aditivo",
            "Repactuação com demonstração analítica de custos / negociação relevante "
            "— natureza declaratória recomenda termo aditivo (entendimento TCU).",
            ["L14133:art.135", "IN05/2017:arts.54-61", "TCU:Ac.1827/2008"], True, "A")

    if facts.reequilibrio_economico_financeiro:
        return RouterDecision(
            "termo_aditivo",
            "Reequilíbrio econômico-financeiro (caso fortuito, força maior ou fato do príncipe).",
            ["L14133:art.124,II", "L14133:art.130"], True, "A")

    if facts.reajuste_indice_ja_previsto:
        return RouterDecision(
            "apostilamento",
            "Reajuste por índice já previsto em cláusula contratual (IPCA/INCC/etc.).",
            ["L14133:art.136,I"], False, None)

    if facts.repactuacao_prevista_sem_renegociacao:
        return RouterDecision(
            "apostilamento",
            "Repactuação prevista no contrato, mero cálculo de variação, sem "
            "renegociação ou demonstração analítica relevante.",
            ["L14133:art.136,I"], True, "A")

    if facts.mudanca_dados_cadastrais_ou_empenho:
        return RouterDecision(
            "apostilamento",
            "Mudança de razão/denominação social, empenho ou atualização de dado cadastral.",
            ["L14133:art.136,II-IV"], False, None)

    raise ValueError(
        "Nenhuma situação reconhecida em ContractFacts — Cynefin Complex: "
        "encaminhar para HITL antes do roteamento.")


if __name__ == "__main__":
    import json

    exemplo = ContractFacts(repactuacao_com_demonstracao_analitica=True)
    decisao = rotear_instrumento(exemplo)
    print(json.dumps(decisao.to_dict(), ensure_ascii=False, indent=2))
