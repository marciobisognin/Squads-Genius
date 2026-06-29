#!/usr/bin/env python3
"""Validador determinístico do SCRIBA — checklist AGU (cláusulas obrigatórias do
art. 92) + quadro de riscos TCU (índice mal justificado, compensação indevida de
limites, repactuação por instrumento errado, ausência de data-base, preclusão).

Cada checagem retorna OK | ALERTA | BLOQUEIO. BLOQUEIO aciona o Turing Guild
(devolve ao Drafter/Engine); ALERTA segue com nota no relatório.

Sem dependências externas. Python 3.11+.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List, Optional

try:
    from .scriba_engine import avaliar_limites_aditivo
    from .scriba_router import ContractFacts, RouterDecision
except ImportError:  # pragma: no cover
    from scriba_engine import avaliar_limites_aditivo
    from scriba_router import ContractFacts, RouterDecision

OK, ALERTA, BLOQUEIO = "OK", "ALERTA", "BLOQUEIO"

# Cláusulas obrigatórias do contrato administrativo (art. 92, Lei 14.133/2021).
CLAUSULAS_OBRIGATORIAS = (
    "partes_e_representantes",
    "objeto",
    "vinculo_edital_proposta",
    "preco_criterios_data_base_periodicidade_reajuste",
    "prazos",
    "garantias",
    "obrigacoes",
    "sancoes",
    "casos_de_extincao",
    "foro",
)

TCU = {
    "compensacao_limites": "Ac. 749/2010-Plenário (veda compensação entre acréscimos e supressões)",
    "repactuacao_instrumento": "Ac. 1.827/2008-Plenário (repactuação preferencialmente por termo aditivo)",
    "apostila_quantitativo": "Ac. 1.643/2024-Plenário (apostila para pequenos ajustes de quantitativo, excepcional)",
}


@dataclass
class Check:
    regra: str
    status: str
    detalhe: str
    fundamento: str = ""

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def _pior_status(checks: List[Check]) -> str:
    if any(c.status == BLOQUEIO for c in checks):
        return BLOQUEIO
    if any(c.status == ALERTA for c in checks):
        return ALERTA
    return OK


def validar_clausulas_obrigatorias(draft_clauses: Dict[str, object]) -> List[Check]:
    """Checa presença das cláusulas obrigatórias do art. 92 e da citação (`source`)
    de fundamento por cláusula (anti-alucinação)."""
    checks: List[Check] = []
    for clausula in CLAUSULAS_OBRIGATORIAS:
        bloco = draft_clauses.get(clausula)
        if bloco is None:
            checks.append(Check(f"art92.{clausula}", BLOQUEIO,
                                 "Cláusula obrigatória ausente", "Lei 14.133/2021 art. 92"))
            continue
        tem_fonte = isinstance(bloco, dict) and bool(bloco.get("source"))
        checks.append(Check(
            f"art92.{clausula}", OK if tem_fonte else BLOQUEIO,
            "Cláusula presente e com fundamento citado" if tem_fonte
            else "Cláusula presente, mas sem citação de fundamento (source)",
            "Lei 14.133/2021 art. 92"))
    return checks


def validar_limites_aditivo(limites_result: Dict[str, object]) -> Check:
    if limites_result.get("status") == "EXCEDE_LIMITE":
        return Check("aditivo.limites", BLOQUEIO,
                     f"Acréscimo {limites_result['acrescimo_pct']:.2%} ou supressão "
                     f"{limites_result['supressao_pct']:.2%} excede o limite "
                     f"{limites_result['limite_aplicavel']:.0%}",
                     TCU["compensacao_limites"])
    return Check("aditivo.limites", OK, "Dentro do limite aplicável, sem compensação",
                 TCU["compensacao_limites"])


def validar_repactuacao_por_instrumento(facts: ContractFacts, decisao: RouterDecision) -> Check:
    """BLOQUEIO se houver demonstração analítica relevante e o instrumento
    escolhido for apostilamento (entendimento doutrinário/TCU: Ac. 1.827/2008)."""
    if facts.repactuacao_com_demonstracao_analitica and decisao.instrument_type == "apostilamento":
        return Check("repactuacao.instrumento_correto", BLOQUEIO,
                     "Repactuação com demonstração analítica não pode ir por apostilamento",
                     TCU["repactuacao_instrumento"])
    return Check("repactuacao.instrumento_correto", OK,
                 "Instrumento coerente com a natureza da repactuação",
                 TCU["repactuacao_instrumento"])


def validar_indice_reajuste(reajuste_result: Optional[Dict[str, object]],
                             justificativa_indice: Optional[str]) -> Optional[Check]:
    if reajuste_result is None:
        return None
    if not justificativa_indice:
        return Check("reajuste.indice_justificado", ALERTA,
                     "Índice de reajuste sem justificativa registrada nos autos — "
                     "risco de glosa/TCU se não retratar a efetiva variação de custos",
                     "Lei 14.133/2021 art. 6º, LVIII")
    return Check("reajuste.indice_justificado", OK,
                 f"Índice {reajuste_result.get('indice')} justificado", "Lei 14.133/2021 art. 6º, LVIII")


def validar_preclusao_repactuacao(repactuacao_result: Optional[Dict[str, object]]) -> Optional[Check]:
    if repactuacao_result is None:
        return None
    if repactuacao_result.get("alerta_preclusao"):
        return Check("repactuacao.preclusao", ALERTA,
                     "Repactuação não solicitada e vigência próxima do fim/prorrogação — "
                     "risco de preclusão do direito",
                     repactuacao_result.get("fundamento_preclusao", "IN 05/2017 art. 57, §7º"))
    return Check("repactuacao.preclusao", OK, "Sem risco iminente de preclusão",
                 "IN 05/2017 art. 57, §7º")


def validar(*, draft_clauses: Optional[Dict[str, object]] = None,
            limites_result: Optional[Dict[str, object]] = None,
            facts: Optional[ContractFacts] = None,
            decisao: Optional[RouterDecision] = None,
            reajuste_result: Optional[Dict[str, object]] = None,
            justificativa_indice: Optional[str] = None,
            repactuacao_result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
    """Roda todas as checagens aplicáveis ao estado disponível e consolida o
    `validation_report`."""
    checks: List[Check] = []

    if draft_clauses is not None:
        checks.extend(validar_clausulas_obrigatorias(draft_clauses))
    if limites_result is not None:
        checks.append(validar_limites_aditivo(limites_result))
    if facts is not None and decisao is not None:
        checks.append(validar_repactuacao_por_instrumento(facts, decisao))
    c = validar_indice_reajuste(reajuste_result, justificativa_indice)
    if c is not None:
        checks.append(c)
    c = validar_preclusao_repactuacao(repactuacao_result)
    if c is not None:
        checks.append(c)

    status_geral = _pior_status(checks)
    return {
        "status_geral": status_geral,
        "go_no_go": "go" if status_geral != BLOQUEIO else "no-go (Turing Guild)",
        "total": len(checks),
        "bloqueios": sum(1 for c in checks if c.status == BLOQUEIO),
        "alertas": sum(1 for c in checks if c.status == ALERTA),
        "checks": [c.to_dict() for c in checks],
    }


def relatorio_markdown(rel: Dict[str, object]) -> str:
    linhas = ["# Relatório de Validação — SCRIBA", "",
              f"- Status geral: **{rel['status_geral']}** ({rel['go_no_go']})",
              f"- Checagens: {rel['total']} | Bloqueios: {rel['bloqueios']} | Alertas: {rel['alertas']}",
              "", "| Regra | Status | Detalhe | Fundamento |", "|---|---|---|---|"]
    for c in rel["checks"]:
        linhas.append(f"| {c['regra']} | {c['status']} | {c['detalhe']} | {c['fundamento']} |")
    return "\n".join(linhas) + "\n"


if __name__ == "__main__":
    import json

    limites = avaliar_limites_aditivo(1_200_000.00, acrescimo=250_000.00)
    rel = validar(limites_result=limites)
    print(json.dumps(rel, ensure_ascii=False, indent=2))
