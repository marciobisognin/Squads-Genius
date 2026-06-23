#!/usr/bin/env python3
"""Suíte de casos-ouro do motor determinístico do SCRIBA.

Os testes verificam INVARIANTES de correção (fator de reajuste, vedação de
compensação nos limites de aditivo, anualidade/preclusão da repactuação,
roteamento do instrumento correto) em entradas fixas — não substituem a
conferência manual contra o processo administrativo concreto.

Rodar:  python3 -m pytest -q   (ou)  python3 tests/test_golden_cases.py
"""
from __future__ import annotations

import datetime as dt
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from scriba_engine import (  # noqa: E402
    ComponenteRepactuacao,
    avaliar_limites_aditivo,
    avaliar_prorrogacao,
    avaliar_repactuacao,
    brl,
    calcular_provisao_mensal,
    calcular_reajuste,
)
from scriba_router import ContractFacts, rotear_instrumento  # noqa: E402
from scriba_validator import validar, BLOQUEIO, OK  # noqa: E402


# ---------- 7.1 Reajuste ----------
def test_reajuste_fator_e_valor():
    r = calcular_reajuste(1_200_000.00, 100.0, 104.5, "IPCA")
    assert r["fator_indice"] == round(104.5 / 100.0, 6)
    assert r["valor_reajustado"] == brl(1_200_000.00 * (104.5 / 100.0))


def test_reajuste_indice_zero_levanta_erro():
    try:
        calcular_reajuste(1000.0, 0.0, 100.0)
        assert False, "deveria levantar ValueError"
    except ValueError:
        pass


# ---------- 7.3 Limites de aditivo ----------
def test_limites_aditivo_dentro_do_limite_25pct():
    r = avaliar_limites_aditivo(1_000_000.00, acrescimo=200_000.00)
    assert r["status"] == OK
    assert r["acrescimo_pct"] == 0.2


def test_limites_aditivo_excede_25pct():
    r = avaliar_limites_aditivo(1_000_000.00, acrescimo=300_000.00)
    assert r["status"] == "EXCEDE_LIMITE"


def test_limites_aditivo_reforma_50pct():
    r = avaliar_limites_aditivo(1_000_000.00, acrescimo=400_000.00,
                                 reforma_edificio_equipamento=True)
    assert r["limite_aplicavel"] == 0.50
    assert r["status"] == OK


def test_limites_aditivo_compensacao_vedada_flag():
    r = avaliar_limites_aditivo(1_000_000.00, acrescimo=200_000.00, supressao=200_000.00)
    assert r["compensacao_vedada"] is True
    # cada percentual avaliado isoladamente -- não há média/compensação
    assert r["acrescimo_pct"] == 0.2 and r["supressao_pct"] == 0.2


# ---------- 7.2 Repactuação ----------
def test_repactuacao_anualidade_cumprida():
    comp = ComponenteRepactuacao("mao_de_obra", dt.date(2025, 1, 1), 100_000.00, 108_000.00)
    rel = avaliar_repactuacao([comp], dt.date(2026, 2, 1))
    assert rel["componentes"][0]["anualidade_cumprida"] is True
    assert rel["componentes"][0]["diferenca"] == brl(8_000.00)


def test_repactuacao_anualidade_nao_cumprida():
    comp = ComponenteRepactuacao("insumos", dt.date(2026, 1, 1), 50_000.00)
    rel = avaliar_repactuacao([comp], dt.date(2026, 6, 1))
    assert rel["componentes"][0]["anualidade_cumprida"] is False


def test_repactuacao_alerta_preclusao():
    comp = ComponenteRepactuacao("mao_de_obra", dt.date(2025, 1, 1), 100_000.00)
    rel = avaliar_repactuacao([comp], dt.date(2026, 6, 1),
                               data_fim_vigencia=dt.date(2026, 6, 20), solicitada=False)
    assert rel["alerta_preclusao"] is True


def test_repactuacao_sem_alerta_quando_solicitada():
    comp = ComponenteRepactuacao("mao_de_obra", dt.date(2025, 1, 1), 100_000.00)
    rel = avaliar_repactuacao([comp], dt.date(2026, 6, 1),
                               data_fim_vigencia=dt.date(2026, 6, 20), solicitada=True)
    assert rel["alerta_preclusao"] is False


# ---------- 7.4 Conta vinculada × PFG ----------
def test_conta_vinculada_vs_pfg_mesma_provisao_total():
    cv = calcular_provisao_mensal(1600.0, "conta_vinculada")
    pfg = calcular_provisao_mensal(1600.0, "pfg")
    assert cv["provisao_mensal_total"] == pfg["provisao_mensal_total"]
    assert cv["deposito_mensal_bloqueado"] is True
    assert pfg["pago_no_fato_gerador"] is True


# ---------- 7.5 Prorrogação ----------
def test_prorrogacao_dentro_do_teto():
    r = avaliar_prorrogacao(36, 12)
    assert r["status"] == OK


def test_prorrogacao_excede_teto():
    r = avaliar_prorrogacao(54, 12)
    assert r["status"] == "EXCEDE_LIMITE"


# ---------- Instrument Router (tabela-decisão §11) ----------
def test_router_nova_contratacao_gera_minuta():
    d = rotear_instrumento(ContractFacts(nova_contratacao=True))
    assert d.instrument_type == "minuta_inicial"
    assert d.needs_hitl is False


def test_router_prorrogacao_gera_aditivo():
    d = rotear_instrumento(ContractFacts(prorrogar_prazo=True))
    assert d.instrument_type == "termo_aditivo"
    assert d.hitl_gate == "A"


def test_router_reajuste_previsto_gera_apostilamento():
    d = rotear_instrumento(ContractFacts(reajuste_indice_ja_previsto=True))
    assert d.instrument_type == "apostilamento"
    assert d.needs_hitl is False


def test_router_repactuacao_analitica_gera_aditivo():
    d = rotear_instrumento(ContractFacts(repactuacao_com_demonstracao_analitica=True))
    assert d.instrument_type == "termo_aditivo"


def test_router_sem_situacao_levanta_erro():
    try:
        rotear_instrumento(ContractFacts())
        assert False, "deveria levantar ValueError (Cynefin Complex)"
    except ValueError:
        pass


# ---------- Validator ----------
def test_validador_bloqueia_excede_limite():
    limites = avaliar_limites_aditivo(1_000_000.00, acrescimo=300_000.00)
    rel = validar(limites_result=limites)
    assert rel["status_geral"] == BLOQUEIO


def test_validador_bloqueia_repactuacao_por_instrumento_errado():
    facts = ContractFacts(repactuacao_com_demonstracao_analitica=True)
    # decisão "errada" forçada para simular violação da regra de instrumento
    from scriba_router import RouterDecision
    decisao_errada = RouterDecision("apostilamento", "teste", [], True, "A")
    rel = validar(facts=facts, decisao=decisao_errada)
    assert rel["status_geral"] == BLOQUEIO


def test_validador_ok_caso_valido():
    limites = avaliar_limites_aditivo(1_000_000.00, acrescimo=200_000.00)
    rel = validar(limites_result=limites, reajuste_result={"indice": "IPCA"},
                  justificativa_indice="IPCA retrata a variação de custos do objeto")
    assert rel["bloqueios"] == 0


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    falhas = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            falhas += 1
            print(f"FAIL {fn.__name__}: {e}")
    print(f"\n{len(fns) - falhas}/{len(fns)} testes passaram")
    return 1 if falhas else 0


if __name__ == "__main__":
    raise SystemExit(_run_all())
