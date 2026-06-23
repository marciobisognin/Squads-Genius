#!/usr/bin/env python3
"""RuleSet da PCFP — percentuais, bases de incidência e fundamentos legais.

Este módulo concentra os PARÂMETROS de cálculo (não calcula valores). Os defaults
abaixo refletem o modelo público da planilha (Anexo VII-D da IN SEGES/MP 05/2017,
regime NÃO desonerado) e servem como ponto de partida AUDITÁVEL.

IMPORTANTE (anti-alucinação):
- Nenhum percentual aqui é "verdade certificada": todo valor final deve ser
  confirmado contra a CCT/ACT vigente, os custos mínimos da IN 176/2024 e o
  enquadramento tributário do licitante (HITL Gate 1).
- O FAP, o RAT/SAT (CNAE) e o regime PIS/COFINS variam por empresa/atividade.
- IRPJ e CSLL NÃO entram na planilha (são tributos sobre o lucro — jurisprudência TCU).

Sem dependências externas. Python 3.11+.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict


# Fundamentos legais reutilizados (citados na memória de cálculo).
FUND = {
    "inss": "Art. 22, I, Lei 8.212/1991; IN RFB 2.110/2022",
    "rat": "Art. 22, II, Lei 8.212/1991 (SAT/RAT × FAP)",
    "terceiros": "Contribuições a terceiros (Sal.-Educação, INCRA, Sistema S, SEBRAE)",
    "fgts": "Art. 15, Lei 8.036/1990 (8%)",
    "13_ferias": "Submódulo 2.1 — IN 05/2017 Anexo VII-D; IN 07/2018",
    "incidencia_2_2": "Submódulo 2.2 incide sobre Módulo 1 + Submódulo 2.1 (IN 07/2018)",
    "vt": "Lei 7.418/1985 — vale-transporte por custo efetivo, descontados até 6% do salário",
    "rescisao": "Módulo 3 — provisão para rescisão; Lei 12.506/2011 (aviso prévio proporcional)",
    "multa_fgts": "Art. 18, §1º, Lei 8.036/1990 (multa de 40% do FGTS)",
    "substituicao": "Módulo 4 — custo de reposição do profissional ausente",
    "tributos": "PIS/COFINS (regime cumulativo/não-cumulativo) e ISS municipal sobre o faturamento",
    "veda_irpj_csll": "IRPJ/CSLL vedados na planilha — tributos sobre o lucro (jurisprudência TCU)",
    "desoneracao": "Lei 14.973/2024 — reoneração gradual da folha (cronograma)",
    "custos_minimos": "IN SEGES/MGI 176/2024 — custos mínimos de remuneração",
}


@dataclass
class RuleSet:
    """Conjunto de parâmetros que a engine aplica. Cada campo é auditável."""

    # ---- Submódulo 2.2 — encargos sociais (regime NÃO desonerado) ----
    inss_patronal: float = 0.20
    rat_sat: float = 0.03          # 1%, 2% ou 3% conforme grau de risco (CNAE)
    fap: float = 1.0               # multiplicador FAP (0,5 a 2,0)
    salario_educacao: float = 0.025
    incra: float = 0.002
    senai_senac: float = 0.010
    sesi_sesc: float = 0.015
    sebrae: float = 0.006
    fgts: float = 0.08
    desoneracao_folha: bool = False  # se True, INSS patronal sai e entra CPRB no M6

    # ---- Submódulo 2.1 — 13º, férias e 1/3 ----
    decimo_terceiro: float = 0.0833      # 1/12
    ferias_terco: float = 0.1111         # férias (1/12) + 1/3 constitucional

    # ---- Módulo 3 — provisão para rescisão (defaults do modelo público) ----
    aviso_previo_indenizado: float = 0.00417   # provisão APi
    multa_fgts_rescisao: float = 0.04          # 40% sobre FGTS provisionado
    aviso_previo_trabalhado: float = 0.00194   # provisão APt

    # ---- Módulo 4 — custo de reposição/substituição (defaults) ----
    substituicao_ferias: float = 0.00      # informar conforme cobertura efetiva
    substituicao_ausencias: float = 0.00

    # ---- Módulo 6 — custos indiretos, lucro e tributos ----
    custos_indiretos: float = 0.05
    lucro: float = 0.0678
    pis: float = 0.0165            # default regime não-cumulativo
    cofins: float = 0.076          # default regime não-cumulativo
    iss: float = 0.05              # alíquota municipal (2% a 5%) — confirmar no município

    # ---- Metadados de origem/vigência ----
    cct_id: str = "A_CONFIRMAR"
    regime: str = "lei14133_in98"   # ou "in05_8666"
    municipio_uf: str = "A_CONFIRMAR"
    fundamentos: Dict[str, str] = field(default_factory=lambda: dict(FUND))

    # ---------- derivados ----------
    @property
    def rat_fap(self) -> float:
        """RAT/SAT ajustado pelo FAP."""
        return round(self.rat_sat * self.fap, 6)

    @property
    def total_submodulo_2_2(self) -> float:
        """Soma dos encargos do Submódulo 2.2 (regime não desonerado)."""
        base = (
            self.rat_fap
            + self.salario_educacao
            + self.incra
            + self.senai_senac
            + self.sesi_sesc
            + self.sebrae
            + self.fgts
        )
        if not self.desoneracao_folha:
            base += self.inss_patronal
        return round(base, 6)

    @property
    def total_tributos(self) -> float:
        """Alíquota total de tributos sobre o faturamento (sem IRPJ/CSLL)."""
        return round(self.pis + self.cofins + self.iss, 6)

    def to_dict(self) -> Dict[str, object]:
        d = asdict(self)
        d["rat_fap"] = self.rat_fap
        d["total_submodulo_2_2"] = self.total_submodulo_2_2
        d["total_tributos"] = self.total_tributos
        return d


def default_ruleset(**overrides) -> RuleSet:
    """Cria um RuleSet com defaults públicos e aplica overrides do Rules Engine/HITL."""
    rs = RuleSet()
    for key, value in overrides.items():
        if not hasattr(rs, key):
            raise KeyError(f"Parâmetro desconhecido no RuleSet: {key}")
        setattr(rs, key, value)
    return rs


if __name__ == "__main__":
    import json

    rs = default_ruleset()
    print(json.dumps(rs.to_dict(), ensure_ascii=False, indent=2))
