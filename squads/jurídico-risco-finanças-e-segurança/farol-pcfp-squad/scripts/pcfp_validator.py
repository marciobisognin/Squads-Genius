#!/usr/bin/env python3
"""Validador determinístico da PCFP — regras estruturais, de incidência,
exequibilidade e jurisprudência TCU embarcada.

Cada checagem retorna status OK | ALERTA | BLOQUEIO. BLOQUEIO aciona o
"Turing loop" (devolve ao Calculator/Rules); ALERTA segue com nota no relatório.

Sem dependências externas. Python 3.11+.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List

try:
    from .pcfp_rules import RuleSet, default_ruleset
    from .pcfp_engine import calcular_planilha, PostoInput
except ImportError:  # pragma: no cover
    from pcfp_rules import RuleSet, default_ruleset
    from pcfp_engine import calcular_planilha, PostoInput

OK, ALERTA, BLOQUEIO = "OK", "ALERTA", "BLOQUEIO"

# Jurisprudência TCU embarcada (referência citável nas checagens).
TCU = {
    "exequibilidade": "Ac. 1.214/2013-P; 839/2020-P (exequibilidade ≠ lucro zero)",
    "zerar_componente": "Ac. 2.186/2013-2ªC (vedado zerar/irrisorar componentes)",
    "todos_custos": "Ac. 2.823/2012-P (composição de todos os custos unitários)",
    "superdimensionado": "Ac. 117/2014-P (índices superdimensionados corrigidos para menos)",
    "irpj_csll": "Jurisprudência TCU — IRPJ/CSLL não compõem a planilha",
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


def validar(planilha: Dict[str, object], rules: RuleSet,
            piso_cct: float = 0.0, custo_minimo_in176: float = 0.0) -> Dict[str, object]:
    """Roda todas as checagens sobre o resultado da engine."""
    checks: List[Check] = []

    # 1) Estrutura — sem IRPJ/CSLL na planilha
    flat = " ".join(
        f"{r['codigo']} {r['descricao']}".lower()
        for posto in planilha["postos"] for r in posto["rubricas"])
    if "irpj" in flat or "csll" in flat:
        checks.append(Check("estrutura.sem_irpj_csll", BLOQUEIO,
                            "IRPJ/CSLL presentes na planilha", TCU["irpj_csll"]))
    else:
        checks.append(Check("estrutura.sem_irpj_csll", OK,
                            "Nenhuma rubrica de IRPJ/CSLL", TCU["irpj_csll"]))

    # 2) Incidência — Submódulo 2.2 sobre (Módulo 1 + Submódulo 2.1)
    for posto in planilha["postos"]:
        base = posto["modulo1"] + posto["submodulo_2_1"]
        esperado = round(rules.total_submodulo_2_2 * base, 2)
        obtido = posto["submodulo_2_2"]
        if abs(esperado - obtido) > 0.05:
            checks.append(Check("incidencia.sub_2_2", BLOQUEIO,
                                f"{posto['nome']}: 2.2 esperado {esperado}, obtido {obtido}",
                                "IN 07/2018"))
        else:
            checks.append(Check("incidencia.sub_2_2", OK,
                                f"{posto['nome']}: 2.2 incide corretamente sobre M1+2.1",
                                "IN 07/2018"))

    # 3) Pisos — salário ≥ piso CCT e ≥ custo mínimo IN 176/2024
    for posto in planilha["postos"]:
        salario = next((r["valor"] for r in posto["rubricas"] if r["codigo"] == "1.A"), 0.0)
        piso = max(piso_cct, custo_minimo_in176)
        if piso and salario + 0.01 < piso:
            checks.append(Check("pisos.salario_minimo", BLOQUEIO,
                                f"{posto['nome']}: salário {salario} < piso {piso}",
                                "IN 176/2024 / CCT"))
        elif not piso:
            checks.append(Check("pisos.salario_minimo", ALERTA,
                                f"{posto['nome']}: piso CCT/IN176 não informado — confirmar (HITL)",
                                "IN 176/2024 / CCT"))
        else:
            checks.append(Check("pisos.salario_minimo", OK,
                                f"{posto['nome']}: salário ≥ piso", "IN 176/2024 / CCT"))

    # 4) Exequibilidade — nenhum componente legal zerado/irrisório
    for posto in planilha["postos"]:
        for cod in ("2.1", "2.2", "3"):
            val = next((r["valor"] for r in posto["rubricas"] if r["codigo"] == cod), None)
            if val is not None and val <= 0:
                checks.append(Check("exequibilidade.componente_zerado", BLOQUEIO,
                                    f"{posto['nome']}: componente {cod} zerado/irrisório",
                                    TCU["zerar_componente"]))
        # lucro > 0 (exequibilidade não exige lucro zero)
        lucro = posto["lucro"]
        if lucro <= 0:
            checks.append(Check("exequibilidade.lucro", ALERTA,
                                f"{posto['nome']}: lucro zerado — avaliar risco de inexecução",
                                TCU["exequibilidade"]))

    # 5) Coerência de regime
    if rules.regime not in ("in05_8666", "lei14133_in98"):
        checks.append(Check("regime.coerencia", BLOQUEIO,
                            f"Regime inválido: {rules.regime}", "IN 05/2017 / IN 98/2022"))
    else:
        checks.append(Check("regime.coerencia", OK,
                            f"Regime: {rules.regime}", "IN 05/2017 / IN 98/2022"))

    # 6) Desoneração/reoneração coerente com o cronograma
    if rules.desoneracao_folha and rules.inss_patronal > 0:
        checks.append(Check("desoneracao.coerencia", ALERTA,
                            "Folha marcada como desonerada mas INSS patronal > 0 no 2.2 — "
                            "tratar CPRB no Módulo 6 (Lei 14.973/2024)",
                            "Lei 14.973/2024"))

    status_geral = _pior_status(checks)
    go = status_geral != BLOQUEIO
    return {
        "status_geral": status_geral,
        "go_no_go": "go" if go else "no-go (Turing loop)",
        "total": len(checks),
        "bloqueios": sum(1 for c in checks if c.status == BLOQUEIO),
        "alertas": sum(1 for c in checks if c.status == ALERTA),
        "checks": [c.to_dict() for c in checks],
    }


def relatorio_markdown(rel: Dict[str, object]) -> str:
    linhas = ["# Relatório de Validação — PCFP", "",
              f"- Status geral: **{rel['status_geral']}** ({rel['go_no_go']})",
              f"- Checagens: {rel['total']} | Bloqueios: {rel['bloqueios']} | Alertas: {rel['alertas']}",
              "", "| Regra | Status | Detalhe | Fundamento |", "|---|---|---|---|"]
    for c in rel["checks"]:
        linhas.append(f"| {c['regra']} | {c['status']} | {c['detalhe']} | {c['fundamento']} |")
    return "\n".join(linhas) + "\n"


if __name__ == "__main__":
    import json

    rs = default_ruleset(cct_id="EXEMPLO", municipio_uf="Frederico Westphalen/RS")
    planilha = calcular_planilha([
        PostoInput("Auxiliar de limpeza", "5143-20", 10, 1600.0,
                   vale_transporte_custo=220.0, auxilio_alimentacao=500.0)
    ], rs)
    rel = validar(planilha, rs, piso_cct=1550.0, custo_minimo_in176=1518.0)
    print(json.dumps(rel, ensure_ascii=False, indent=2))
