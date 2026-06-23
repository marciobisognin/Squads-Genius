#!/usr/bin/env python3
"""Engine determinística da Planilha de Custos e Formação de Preços (PCFP).

Implementa os Módulos 1–6 do Anexo VII-D da IN SEGES/MP 05/2017, por posto,
sobre o valor mensal por empregado, com a ORDEM DE INCIDÊNCIA correta:

  - Submódulo 2.2 incide sobre o Módulo 1 E o Submódulo 2.1 (IN 07/2018).
  - A provisão de rescisão (Módulo 3) recebe a incidência do Submódulo 2.2.
  - Vale-transporte: custo efetivo (descontados até 6% do salário) — sem piso arbitrário.
  - Tributos do Módulo 6 por "gross-up" sobre o faturamento; IRPJ/CSLL NÃO entram.

Princípio reitor (anti-alucinação): toda a matemática é código puro, determinística
e auditável. O LLM nunca produz valores monetários. Cada rubrica carrega
{valor, formula, fundamento}.

Sem dependências externas. Python 3.11+.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

try:  # execução como módulo do pacote ou direto
    from .pcfp_rules import RuleSet, default_ruleset, FUND
except ImportError:  # pragma: no cover
    from pcfp_rules import RuleSet, default_ruleset, FUND


CENTAVOS = 2


def brl(value: float) -> float:
    """Arredonda para centavos (2 casas), padrão monetário."""
    return round(float(value) + 1e-9, CENTAVOS)


@dataclass
class Rubrica:
    """Uma linha da planilha, totalmente rastreável."""

    codigo: str
    descricao: str
    valor: float
    formula: str
    fundamento: str
    flags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        d = asdict(self)
        d["valor"] = brl(self.valor)
        return d


@dataclass
class PostoInput:
    """Entrada de um posto/categoria profissional."""

    nome: str
    cbo: str
    quantidade: int
    salario_base: float
    meses_execucao: int = 12

    # adicionais (Módulo 1)
    periculosidade: bool = False                 # 30% sobre o salário-base
    insalubridade_grau: float = 0.0              # 0.10 / 0.20 / 0.40
    salario_minimo: float = 1518.0               # base da insalubridade (parametrizável)
    adicional_noturno: float = 0.0               # valor mensal já apurado, se houver
    outros_modulo1: float = 0.0

    # benefícios (Submódulo 2.3)
    vale_transporte_custo: float = 0.0           # custo efetivo mensal do VT (bruto)
    desconto_vt_sobre_salario: float = 0.06      # até 6% do salário-base
    auxilio_alimentacao: float = 0.0
    assistencia_medica: float = 0.0
    outros_beneficios: float = 0.0

    # insumos (Módulo 5)
    uniformes: float = 0.0
    materiais: float = 0.0
    equipamentos: float = 0.0
    epis: float = 0.0


@dataclass
class PostoResult:
    nome: str
    cbo: str
    quantidade: int
    meses_execucao: int
    rubricas: List[Rubrica]
    modulo1: float
    submodulo_2_1: float
    submodulo_2_2: float
    submodulo_2_3: float
    modulo2: float
    modulo3: float
    modulo4: float
    modulo5: float
    custo_sem_lucro_tributos: float
    custos_indiretos: float
    lucro: float
    tributos: float
    preco_mensal_unitario: float
    preco_mensal_total: float
    preco_global: float

    def to_dict(self) -> Dict[str, object]:
        d = asdict(self)
        d["rubricas"] = [r.to_dict() for r in self.rubricas]
        return d


def calcular_posto(posto: PostoInput, rules: Optional[RuleSet] = None) -> PostoResult:
    """Calcula a planilha de um posto, com memória de cálculo rubrica a rubrica."""
    rs = rules or default_ruleset()
    rubricas: List[Rubrica] = []

    # ---------------- Módulo 1 — Composição da Remuneração ----------------
    salario = brl(posto.salario_base)
    rubricas.append(Rubrica(
        "1.A", "Salário-base", salario,
        "piso CCT/ACT (≥ custos mínimos IN 176/2024)", FUND["custos_minimos"]))

    peric = brl(0.30 * salario) if posto.periculosidade else 0.0
    if posto.periculosidade:
        rubricas.append(Rubrica(
            "1.B", "Adicional de periculosidade", peric,
            "30% × salário-base", "Art. 193, §1º, CLT"))

    insal = brl(posto.insalubridade_grau * posto.salario_minimo) if posto.insalubridade_grau else 0.0
    if posto.insalubridade_grau:
        rubricas.append(Rubrica(
            "1.C", "Adicional de insalubridade", insal,
            f"{posto.insalubridade_grau:.0%} × salário-mínimo", "Art. 192, CLT"))

    noturno = brl(posto.adicional_noturno)
    if noturno:
        rubricas.append(Rubrica(
            "1.D", "Adicional noturno", noturno,
            "adicional + hora noturna reduzida (apurado)", "Art. 73, CLT"))

    outros1 = brl(posto.outros_modulo1)
    if outros1:
        rubricas.append(Rubrica(
            "1.E", "Outros (Módulo 1)", outros1, "informado", "CCT/ACT"))

    modulo1 = brl(salario + peric + insal + noturno + outros1)
    rubricas.append(Rubrica(
        "1", "TOTAL Módulo 1 — Remuneração", modulo1,
        "1.A + 1.B + 1.C + 1.D + 1.E", "IN 05/2017 Anexo VII-D"))

    # ---------------- Submódulo 2.1 — 13º, férias e 1/3 ----------------
    decimo = brl(rs.decimo_terceiro * modulo1)
    ferias = brl(rs.ferias_terco * modulo1)
    sub_2_1 = brl(decimo + ferias)
    rubricas.append(Rubrica(
        "2.1.A", "13º salário", decimo,
        f"{rs.decimo_terceiro:.4%} × Módulo 1", FUND["13_ferias"]))
    rubricas.append(Rubrica(
        "2.1.B", "Férias + 1/3 constitucional", ferias,
        f"{rs.ferias_terco:.4%} × Módulo 1", FUND["13_ferias"]))
    rubricas.append(Rubrica(
        "2.1", "SUBTOTAL Submódulo 2.1", sub_2_1, "2.1.A + 2.1.B", FUND["13_ferias"]))

    # ---------------- Submódulo 2.2 — GPS, FGTS e contribuições ----------------
    # INCIDÊNCIA-CHAVE: sobre Módulo 1 + Submódulo 2.1 (somente parcelas salariais).
    base_2_2 = brl(modulo1 + sub_2_1)
    sub_2_2 = brl(rs.total_submodulo_2_2 * base_2_2)
    rubricas.append(Rubrica(
        "2.2", "SUBTOTAL Submódulo 2.2 (encargos sociais)", sub_2_2,
        f"{rs.total_submodulo_2_2:.4%} × (Módulo 1 + Submódulo 2.1)",
        FUND["incidencia_2_2"],
        flags=["desonerado"] if rs.desoneracao_folha else []))

    # ---------------- Submódulo 2.3 — benefícios mensais/diários ----------------
    desconto_vt = brl(posto.desconto_vt_sobre_salario * salario)
    vt_efetivo = brl(max(0.0, posto.vale_transporte_custo - desconto_vt))
    if posto.vale_transporte_custo:
        rubricas.append(Rubrica(
            "2.3.A", "Vale-transporte (custo efetivo)", vt_efetivo,
            f"max(0; custo {brl(posto.vale_transporte_custo)} − "
            f"{posto.desconto_vt_sobre_salario:.0%}×salário {desconto_vt})",
            FUND["vt"], flags=["custo_efetivo"]))
    va = brl(posto.auxilio_alimentacao)
    am = brl(posto.assistencia_medica)
    ob = brl(posto.outros_beneficios)
    for cod, desc, val in (("2.3.B", "Auxílio-alimentação/refeição", va),
                           ("2.3.C", "Assistência médica/familiar", am),
                           ("2.3.D", "Outros benefícios (CCT)", ob)):
        if val:
            rubricas.append(Rubrica(cod, desc, val, "valor CCT/custo efetivo", "CCT/ACT"))
    sub_2_3 = brl(vt_efetivo + va + am + ob)
    rubricas.append(Rubrica(
        "2.3", "SUBTOTAL Submódulo 2.3 (benefícios)", sub_2_3,
        "2.3.A + 2.3.B + 2.3.C + 2.3.D", "IN 05/2017 Anexo VII-D"))

    modulo2 = brl(sub_2_1 + sub_2_2 + sub_2_3)
    rubricas.append(Rubrica(
        "2", "TOTAL Módulo 2 — Encargos e Benefícios", modulo2,
        "2.1 + 2.2 + 2.3", "IN 05/2017 Anexo VII-D"))

    # ---------------- Módulo 3 — Provisão para Rescisão ----------------
    # Base de encargos da rescisão recebe a incidência do Submódulo 2.2.
    api = brl(rs.aviso_previo_indenizado * modulo1)
    apt = brl(rs.aviso_previo_trabalhado * modulo1)
    multa = brl(rs.multa_fgts_rescisao * (rs.fgts * base_2_2))
    incid_resc = brl(rs.total_submodulo_2_2 * (api + apt))
    modulo3 = brl(api + apt + multa + incid_resc)
    rubricas.append(Rubrica(
        "3.A", "Aviso prévio indenizado + proporcional", api,
        f"{rs.aviso_previo_indenizado:.4%} × Módulo 1", FUND["rescisao"]))
    rubricas.append(Rubrica(
        "3.B", "Aviso prévio trabalhado", apt,
        f"{rs.aviso_previo_trabalhado:.4%} × Módulo 1", FUND["rescisao"]))
    rubricas.append(Rubrica(
        "3.C", "Multa FGTS (40%)", multa,
        f"{rs.multa_fgts_rescisao:.0%} × (FGTS {rs.fgts:.0%} × base 2.2)", FUND["multa_fgts"]))
    rubricas.append(Rubrica(
        "3.D", "Incidência Submódulo 2.2 sobre rescisão", incid_resc,
        f"{rs.total_submodulo_2_2:.4%} × (3.A + 3.B)", FUND["incidencia_2_2"]))
    rubricas.append(Rubrica(
        "3", "TOTAL Módulo 3 — Provisão para Rescisão", modulo3,
        "3.A + 3.B + 3.C + 3.D", FUND["rescisao"]))

    # ---------------- Módulo 4 — Custo de reposição/substituição ----------------
    sub_fer = brl(rs.substituicao_ferias * modulo1)
    sub_aus = brl(rs.substituicao_ausencias * modulo1)
    modulo4 = brl(sub_fer + sub_aus)
    rubricas.append(Rubrica(
        "4", "TOTAL Módulo 4 — Reposição do profissional ausente", modulo4,
        f"({rs.substituicao_ferias:.4%}+{rs.substituicao_ausencias:.4%}) × Módulo 1",
        FUND["substituicao"]))

    # ---------------- Módulo 5 — Insumos diversos ----------------
    modulo5 = brl(posto.uniformes + posto.materiais + posto.equipamentos + posto.epis)
    rubricas.append(Rubrica(
        "5", "TOTAL Módulo 5 — Insumos diversos", modulo5,
        "uniformes + materiais + equipamentos + EPIs", "IN 05/2017 Anexo VII-D"))

    # ---------------- Módulo 6 — Custos indiretos, tributos e lucro ----------------
    custo_base = brl(modulo1 + modulo2 + modulo3 + modulo4 + modulo5)
    ci = brl(rs.custos_indiretos * custo_base)
    base_lucro = brl(custo_base + ci)
    lucro = brl(rs.lucro * base_lucro)
    base_tributos = brl(custo_base + ci + lucro)
    aliq = rs.total_tributos
    # Gross-up: tributos incidem sobre o faturamento (preço final).
    preco_unitario = brl(base_tributos / (1.0 - aliq)) if aliq < 1 else base_tributos
    tributos = brl(preco_unitario - base_tributos)

    rubricas.append(Rubrica(
        "6.A", "Custos indiretos", ci,
        f"{rs.custos_indiretos:.4%} × (M1..M5)", "IN 05/2017 Anexo VII-D"))
    rubricas.append(Rubrica(
        "6.B", "Lucro", lucro,
        f"{rs.lucro:.4%} × (M1..M5 + custos indiretos)", "IN 05/2017 Anexo VII-D"))
    rubricas.append(Rubrica(
        "6.C", "Tributos (PIS+COFINS+ISS) por gross-up", tributos,
        f"preço × {aliq:.4%}; preço = base/(1−{aliq:.4%})", FUND["tributos"],
        flags=["sem_irpj_csll"]))
    rubricas.append(Rubrica(
        "VII", "PREÇO MENSAL POR EMPREGADO", preco_unitario,
        "M1 + M2 + M3 + M4 + M5 + custos indiretos + lucro + tributos",
        "IN 05/2017 Anexo VII-D — Quadro-Resumo"))

    preco_total = brl(preco_unitario * posto.quantidade)
    preco_global = brl(preco_total * posto.meses_execucao)
    rubricas.append(Rubrica(
        "RESUMO", "Valor global do posto", preco_global,
        f"{preco_unitario} × {posto.quantidade} postos × {posto.meses_execucao} meses",
        "IN 05/2017 Anexo VII-D — Quadro-Resumo"))

    return PostoResult(
        nome=posto.nome, cbo=posto.cbo, quantidade=posto.quantidade,
        meses_execucao=posto.meses_execucao, rubricas=rubricas,
        modulo1=modulo1, submodulo_2_1=sub_2_1, submodulo_2_2=sub_2_2,
        submodulo_2_3=sub_2_3, modulo2=modulo2, modulo3=modulo3, modulo4=modulo4,
        modulo5=modulo5, custo_sem_lucro_tributos=custo_base, custos_indiretos=ci,
        lucro=lucro, tributos=tributos, preco_mensal_unitario=preco_unitario,
        preco_mensal_total=preco_total, preco_global=preco_global)


def calcular_planilha(postos: List[PostoInput], rules: Optional[RuleSet] = None) -> Dict[str, object]:
    """Calcula todos os postos e o quadro-resumo global."""
    rs = rules or default_ruleset()
    resultados = [calcular_posto(p, rs) for p in postos]
    valor_global = brl(sum(r.preco_global for r in resultados))
    return {
        "ruleset": rs.to_dict(),
        "postos": [r.to_dict() for r in resultados],
        "valor_global_contrato": valor_global,
    }


if __name__ == "__main__":
    import json

    exemplo = PostoInput(
        nome="Auxiliar de limpeza (diurno 44h)", cbo="5143-20", quantidade=10,
        salario_base=1600.00, vale_transporte_custo=220.00, auxilio_alimentacao=500.00,
        uniformes=30.00, epis=15.00, meses_execucao=12)
    print(json.dumps(calcular_planilha([exemplo]), ensure_ascii=False, indent=2))
