#!/usr/bin/env python3
"""Suíte de casos-ouro da engine PCFP.

Os testes verificam INVARIANTES de correção (ordem de incidência, vedações,
custo efetivo do VT, gross-up de tributos) e a consistência interna do cálculo
em entradas fixas — não substituem a conferência manual contra a CCT vigente.

Rodar:  python3 -m pytest -q   (ou)  python3 tests/test_golden_cases.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from pcfp_rules import default_ruleset  # noqa: E402
from pcfp_engine import PostoInput, calcular_posto, calcular_planilha, brl  # noqa: E402
from pcfp_validator import validar, BLOQUEIO, OK  # noqa: E402


def _rub(res, codigo):
    return next(r for r in res.rubricas if r.codigo == codigo)


# ---------- Caso 1: Limpeza diurno 44h ----------
def test_limpeza_incidencia_2_2_sobre_m1_e_2_1():
    rs = default_ruleset()
    p = PostoInput("Limpeza diurno 44h", "5143-20", 1, 1600.0)
    res = calcular_posto(p, rs)
    base = res.modulo1 + res.submodulo_2_1
    assert res.submodulo_2_2 == brl(rs.total_submodulo_2_2 * base)


def test_limpeza_sem_irpj_csll():
    rs = default_ruleset()
    pl = calcular_planilha([PostoInput("Limpeza", "5143-20", 1, 1600.0)], rs)
    rel = validar(pl, rs, piso_cct=1550.0, custo_minimo_in176=1518.0)
    assert rel["bloqueios"] == 0
    nomes = " ".join(r["descricao"].lower() for r in pl["postos"][0]["rubricas"])
    assert "irpj" not in nomes and "csll" not in nomes


def test_vale_transporte_custo_efetivo():
    rs = default_ruleset()
    # VT abaixo de 6% do salário -> custo efetivo zero (nunca negativo)
    p = PostoInput("Limpeza", "5143-20", 1, 2000.0, vale_transporte_custo=100.0)
    res = calcular_posto(p, rs)
    vt = _rub(res, "2.3.A").valor
    assert vt == 0.0  # 100 - 6%*2000(=120) -> max(0, -20)


def test_vale_transporte_desconto_aplicado():
    rs = default_ruleset()
    p = PostoInput("Limpeza", "5143-20", 1, 1600.0, vale_transporte_custo=300.0)
    res = calcular_posto(p, rs)
    assert _rub(res, "2.3.A").valor == brl(300.0 - 0.06 * 1600.0)


# ---------- Caso 2: Vigilância 12x36 noturno ----------
def test_vigilancia_periculosidade_30pct():
    rs = default_ruleset(rat_sat=0.03)
    p = PostoInput("Vigilante 12x36 noturno", "5173-30", 2, 2200.0,
                   periculosidade=True, adicional_noturno=300.0)
    res = calcular_posto(p, rs)
    assert _rub(res, "1.B").valor == brl(0.30 * 2200.0)
    assert res.modulo1 == brl(2200.0 + 0.30 * 2200.0 + 300.0)


def test_vigilancia_rescisao_recebe_incidencia_2_2():
    rs = default_ruleset()
    p = PostoInput("Vigilante", "5173-30", 1, 2200.0, periculosidade=True)
    res = calcular_posto(p, rs)
    incid = _rub(res, "3.D").valor
    api = _rub(res, "3.A").valor
    apt = _rub(res, "3.B").valor
    assert incid == brl(rs.total_submodulo_2_2 * (api + apt))


# ---------- Caso 3: Apoio administrativo ----------
def test_apoio_gross_up_tributos():
    rs = default_ruleset()
    p = PostoInput("Apoio administrativo", "4110-10", 3, 1900.0,
                   auxilio_alimentacao=600.0, vale_transporte_custo=260.0)
    res = calcular_posto(p, rs)
    base = res.custo_sem_lucro_tributos + res.custos_indiretos + res.lucro
    # tributos = preço*aliq, com preço = base/(1-aliq)
    esperado_preco = brl(base / (1 - rs.total_tributos))
    assert res.preco_mensal_unitario == esperado_preco
    assert res.tributos == brl(esperado_preco - base)


def test_quadro_resumo_global():
    rs = default_ruleset()
    p = PostoInput("Apoio", "4110-10", 4, 1900.0, meses_execucao=12)
    res = calcular_posto(p, rs)
    assert res.preco_mensal_total == brl(res.preco_mensal_unitario * 4)
    assert res.preco_global == brl(res.preco_mensal_total * 12)


# ---------- Validador: deve BLOQUEAR salário abaixo do piso ----------
def test_validador_bloqueia_abaixo_do_piso():
    rs = default_ruleset()
    pl = calcular_planilha([PostoInput("Limpeza", "5143-20", 1, 1000.0)], rs)
    rel = validar(pl, rs, piso_cct=1550.0, custo_minimo_in176=1518.0)
    assert rel["status_geral"] == BLOQUEIO
    assert any(c["regra"] == "pisos.salario_minimo" and c["status"] == BLOQUEIO
               for c in rel["checks"])


def test_validador_ok_caso_valido():
    rs = default_ruleset()
    pl = calcular_planilha([PostoInput("Limpeza", "5143-20", 5, 1600.0,
                                       vale_transporte_custo=220.0,
                                       auxilio_alimentacao=500.0)], rs)
    rel = validar(pl, rs, piso_cct=1550.0, custo_minimo_in176=1518.0)
    assert rel["bloqueios"] == 0


def test_desoneracao_remove_inss_do_2_2():
    rs_on = default_ruleset(desoneracao_folha=False)
    rs_off = default_ruleset(desoneracao_folha=True)
    assert rs_on.total_submodulo_2_2 > rs_off.total_submodulo_2_2
    assert brl(rs_on.total_submodulo_2_2 - rs_off.total_submodulo_2_2) == brl(0.20)


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
