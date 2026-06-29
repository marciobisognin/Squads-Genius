#!/usr/bin/env python3
"""Testes do núcleo executável do Forge of Solus Prime (Lei do Élenchos).

Cobrem: pontuação determinística (Decimal), Portão de Cynefin, contrato SACP
(anti-DERIVA), travessia completa `forge init` e gates de qualidade. Usam apenas
a stdlib + pytest.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import cynefin_gate  # noqa: E402
import evaluate_tool  # noqa: E402
import forge  # noqa: E402
import sacp  # noqa: E402
import validate_squad as run_validator  # noqa: E402

BRIEFING = str(ROOT / "examples" / "briefing_exemplo.yaml")


def test_pontuar_deterministico():
    metricas = {"fit": 1, "licenca": 1, "manutencao": 1, "seguranca": 1,
                "instalacao": 1, "testabilidade": 1, "interop_agente": 1}
    assert evaluate_tool.pontuar(metricas) == Decimal("1.0000")
    # reprodutível
    assert evaluate_tool.pontuar(metricas) == evaluate_tool.pontuar(metricas)


def test_pontuar_rejeita_metricas_invalidas():
    import pytest

    with pytest.raises(ValueError):
        evaluate_tool.pontuar({"fit": 2})


def test_decisao_risco_alto_nunca_incorpora():
    assert evaluate_tool.decidir(Decimal("0.99"), "high") == "reject"
    assert evaluate_tool.decidir(Decimal("0.75"), "low") == "incorporate"
    assert evaluate_tool.decidir(Decimal("0.55"), "low") == "adapt"
    assert evaluate_tool.decidir(Decimal("0.10"), "low") == "watch"


def test_cynefin_classifica_e_roteia():
    from forge_common import load_briefing

    res = cynefin_gate.classificar(load_briefing(BRIEFING))
    assert res["cynefin"] in {"clear", "complicated", "complex", "chaotic"}
    assert res["autonomy_level"] in {"L1", "L2", "L3"}


def test_chaotic_nunca_passa_de_l1():
    res = cynefin_gate.classificar({
        "objective": "responder a uma crise urgente e instável sem padrão",
        "problem": "incidente em produção", "autonomy_level": "L3",
        "cynefin_hint": "chaotic",
    })
    assert res["cynefin"] == "chaotic"
    assert res["autonomy_level"] == "L1"


def test_sacp_rejeita_ato_invalido():
    import pytest

    with pytest.raises(ValueError):
        sacp.novo_contrato("A", "B", sacp.Estrato.LOGOS, "ato_inexistente", {})


def test_sacp_contrato_serializa():
    c = sacp.novo_contrato("BLASTER", "PROWL", sacp.Estrato.LOGOS, "diairesis", {"n": 1})
    d = sacp.dump(c)
    assert d["emissor"] == "BLASTER"
    assert d["ato"] == "diairesis"


def test_forge_init_gera_todos_estratos(tmp_path):
    out = tmp_path / "run"
    rc = forge.main(["init", "--briefing", BRIEFING, "--out", str(out), "--mode", "L1"])
    assert rc == 0
    obrigatorios = [
        "briefing.normalizado.yaml", "cynefin.json", "grafo_requisitos.json",
        "squad.yaml", "AGENTS.md", "LOOP.md", "CONVENTIONS.md",
        "run_state.json", "token_budget.json", "evidence.md", "quality_report.json",
        "tool_evaluation.json",
    ]
    for nome in obrigatorios:
        f = out / nome
        assert f.exists() and f.stat().st_size > 0, nome
    rel = run_validator.validar(out)
    assert rel["status"] == "pass"
    assert rel["pathologies_verified"] is True


def test_quality_report_verifica_seis_patologias(tmp_path):
    out = tmp_path / "run"
    forge.main(["init", "--briefing", BRIEFING, "--out", str(out), "--mode", "L1"])
    qr = json.loads((out / "quality_report.json").read_text(encoding="utf-8"))
    assert set(qr["pathologies_checked"]) == {
        "pseudo_telos", "opacidade", "dispendio", "abdicacao", "metastase", "deriva",
    }


def test_decompoe_em_3_a_7_tarefas(tmp_path):
    out = tmp_path / "run"
    forge.main(["init", "--briefing", BRIEFING, "--out", str(out), "--mode", "L1"])
    grafo = json.loads((out / "grafo_requisitos.json").read_text(encoding="utf-8"))
    assert 3 <= grafo["n_tarefas"] <= 7
