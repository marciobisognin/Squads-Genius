#!/usr/bin/env python3
"""Motor determinístico do Squad SCRIBA (§7 do PRD).

Implementa, em Python puro e sem LLM, os quatro cálculos do motor:
  7.1 Reajuste em sentido estrito (índice pré-pactuado).
  7.2 Repactuação DEMO (anualidade por componente + alerta de preclusão).
  7.3 Limites de aditivo (±25%/50%, vedada compensação — Ac. 749/2010-TCU).
  7.4 Conta-Depósito Vinculada × Pagamento pelo Fato Gerador (PFG).

Princípio reitor (anti-alucinação): nenhum valor monetário sai do LLM. Cada
resultado carrega memória de cálculo (fórmula + insumos + fundamento legal).

Sem dependências externas. Python 3.11+.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Dict, List, Optional

CENTAVOS = 2


def brl(value: float) -> float:
    """Arredonda para centavos (2 casas), padrão monetário."""
    return round(float(value) + 1e-9, CENTAVOS)


@dataclass
class MemoriaItem:
    """Uma linha da memória de cálculo, totalmente rastreável."""

    item: str
    valor: object
    formula: str
    fundamento: str

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


# ---------------------------------------------------------------------------
# 7.1 — Reajuste em sentido estrito (serviços sem MO / bens / locação)
# ---------------------------------------------------------------------------
def calcular_reajuste(valor_base: float, indice_inicial: float, indice_final: float,
                       indice_nome: str = "IPCA") -> Dict[str, object]:
    """fator = indice_final / indice_inicial; valor_reajustado = valor_base * fator.

    Marco inicial do índice = data da proposta (Lei 10.192/2001, art. 2º-3º).
    """
    if indice_inicial <= 0:
        raise ValueError("indice_inicial deve ser > 0")
    fator = indice_final / indice_inicial
    valor_base_r = brl(valor_base)
    valor_reajustado = brl(valor_base_r * fator)
    memoria = [
        MemoriaItem("fator_indice", round(fator, 6),
                    f"{indice_final} / {indice_inicial}",
                    f"nº-índice {indice_nome}; Lei 10.192/2001 art. 2º-3º"),
        MemoriaItem("valor_reajustado", valor_reajustado,
                    f"{valor_base_r} × {round(fator, 6)}",
                    "Marco inicial = data da proposta (não a da assinatura)"),
    ]
    return {
        "indice": indice_nome,
        "valor_base": valor_base_r,
        "fator_indice": round(fator, 6),
        "valor_reajustado": valor_reajustado,
        "memoria": [m.to_dict() for m in memoria],
        "fundamento": "Lei 14.133/2021 art. 6º, LVIII; Lei 10.192/2001 art. 2º-3º",
    }


# ---------------------------------------------------------------------------
# 7.3 — Limites de aditivo (art. 124–125)
# ---------------------------------------------------------------------------
def avaliar_limites_aditivo(valor_inicial_atualizado: float, acrescimo: float = 0.0,
                             supressao: float = 0.0,
                             reforma_edificio_equipamento: bool = False) -> Dict[str, object]:
    """limite = 50% (reforma de edifício/equipamento) ou 25% (regra geral).

    VEDADA a compensação entre acréscimos e supressões para o cômputo do limite
    (Ac. 749/2010-Plenário-TCU) — cada percentual é avaliado isoladamente.
    """
    if valor_inicial_atualizado <= 0:
        raise ValueError("valor_inicial_atualizado deve ser > 0")
    limite = 0.50 if reforma_edificio_equipamento else 0.25
    acrescimo_pct = round(acrescimo / valor_inicial_atualizado, 6)
    supressao_pct = round(supressao / valor_inicial_atualizado, 6)
    excede = acrescimo_pct > limite or supressao_pct > limite
    return {
        "valor_inicial_atualizado": brl(valor_inicial_atualizado),
        "acrescimo": brl(acrescimo),
        "supressao": brl(supressao),
        "limite_aplicavel": limite,
        "acrescimo_pct": acrescimo_pct,
        "supressao_pct": supressao_pct,
        "compensacao_vedada": True,
        "status": "EXCEDE_LIMITE" if excede else "OK",
        "fundamento": "Lei 14.133/2021 arts. 124-125; vedada compensação (Ac. 749/2010-Plenário-TCU)",
    }


# ---------------------------------------------------------------------------
# 7.2 — Repactuação (serviços com DEMO)
# ---------------------------------------------------------------------------
@dataclass
class ComponenteRepactuacao:
    """Um componente repactuável: 'mao_de_obra' (data-base da CCT) ou
    'insumos' (data da apresentação da proposta) — podem ter datas-base distintas
    (art. 135, §4º da Lei 14.133/2021)."""

    nome: str
    data_base_anterior: date
    valor_atual: float
    valor_negociado: Optional[float] = None


def avaliar_repactuacao(componentes: List[ComponenteRepactuacao], data_referencia: date,
                         data_fim_vigencia: Optional[date] = None,
                         solicitada: bool = False,
                         dias_alerta_preclusao: int = 60) -> Dict[str, object]:
    """Verifica anualidade por componente e emite alerta crítico de preclusão.

    Preclusão (IN 05/2017 art. 57, §7º): repactuações não solicitadas durante a
    vigência precluem com a assinatura da prorrogação ou o encerramento do
    contrato — por isso o alerta é emitido conforme a proximidade do fim de
    vigência quando a repactuação ainda não foi solicitada.
    """
    resultados = []
    for c in componentes:
        dias = (data_referencia - c.data_base_anterior).days
        diferenca = brl(c.valor_negociado - c.valor_atual) if c.valor_negociado is not None else None
        resultados.append({
            "componente": c.nome,
            "data_base_anterior": c.data_base_anterior.isoformat(),
            "dias_desde_data_base": dias,
            "anualidade_cumprida": dias >= 365,
            "valor_atual": brl(c.valor_atual),
            "valor_negociado": brl(c.valor_negociado) if c.valor_negociado is not None else None,
            "diferenca": diferenca,
            "fundamento": ("IN SEGES/MPDG 05/2017 arts. 54-61 (Subseção VI); "
                           "Lei 14.133/2021 art. 135, II e §4º"),
        })

    alerta_preclusao = False
    dias_para_fim = None
    if data_fim_vigencia is not None:
        dias_para_fim = (data_fim_vigencia - data_referencia).days
        if not solicitada and dias_para_fim <= dias_alerta_preclusao:
            alerta_preclusao = True

    return {
        "componentes": resultados,
        "data_fim_vigencia": data_fim_vigencia.isoformat() if data_fim_vigencia else None,
        "dias_para_fim_vigencia": dias_para_fim,
        "solicitada": solicitada,
        "alerta_preclusao": alerta_preclusao,
        "fundamento_preclusao": "IN SEGES/MPDG 05/2017 art. 57, §7º",
    }


# ---------------------------------------------------------------------------
# 7.4 — Conta-Depósito Vinculada × Pagamento pelo Fato Gerador (PFG)
# ---------------------------------------------------------------------------
def calcular_provisao_mensal(salario_base: float, modo: str = "conta_vinculada") -> Dict[str, object]:
    """Provisões mensais de férias+1/3, 13º e multa FGTS de rescisão (Módulos 3/4
    da planilha de custos). Em PFG essas parcelas só são pagas no fato gerador
    (não há depósito mensal bloqueado)."""
    if modo not in ("conta_vinculada", "pfg"):
        raise ValueError("modo deve ser 'conta_vinculada' ou 'pfg'")
    ferias_terco = brl(salario_base * (1 / 12 + 1 / 36))
    decimo = brl(salario_base / 12)
    multa_fgts = brl(salario_base * 0.08 * 0.40)
    total = brl(ferias_terco + decimo + multa_fgts)
    return {
        "modo": modo,
        "salario_base": brl(salario_base),
        "ferias_e_terco": ferias_terco,
        "decimo_terceiro": decimo,
        "multa_fgts_rescisao": multa_fgts,
        "provisao_mensal_total": total,
        "deposito_mensal_bloqueado": modo == "conta_vinculada",
        "pago_no_fato_gerador": modo == "pfg",
        "fundamento": ("IN SEGES/MPDG 05/2017, Anexos (Conta-Depósito Vinculada / PFG); "
                       "Súmula 331/TST; Lei 14.133/2021 art. 121"),
    }


# ---------------------------------------------------------------------------
# 7.5 — Prorrogação (vigência)
# ---------------------------------------------------------------------------
def avaliar_prorrogacao(meses_ja_executados: int, meses_prorrogacao: int,
                         limite_meses: int = 60) -> Dict[str, object]:
    """Serviço contínuo: até 60 meses (art. 107) — checagem do teto cumulativo."""
    total = meses_ja_executados + meses_prorrogacao
    return {
        "meses_ja_executados": meses_ja_executados,
        "meses_prorrogacao": meses_prorrogacao,
        "meses_totais": total,
        "limite_meses": limite_meses,
        "status": "OK" if total <= limite_meses else "EXCEDE_LIMITE",
        "fundamento": "Lei 14.133/2021 art. 107",
    }


if __name__ == "__main__":
    import json

    exemplo = {
        "reajuste": calcular_reajuste(1_200_000.00, 100.0, 104.5, "IPCA"),
        "limites_aditivo": avaliar_limites_aditivo(1_200_000.00, acrescimo=250_000.00),
        "conta_vinculada": calcular_provisao_mensal(1_600.00, "conta_vinculada"),
        "prorrogacao": avaliar_prorrogacao(24, 12),
    }
    print(json.dumps(exemplo, ensure_ascii=False, indent=2))
