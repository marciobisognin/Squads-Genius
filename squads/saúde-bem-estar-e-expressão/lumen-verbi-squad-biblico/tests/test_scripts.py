"""Testes minimos dos scripts deterministicos do Lumen Verbi.

Executar a partir da raiz do squad: python3 -m pytest -q
"""
from __future__ import annotations

import sys
from pathlib import Path

SQUAD_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = SQUAD_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import montar_prompt_persona as mp  # noqa: E402
import parse_referencia_biblica as prb  # noqa: E402
import selecionar_agentes as sa  # noqa: E402
import validar_fidelidade as vf  # noqa: E402

DATA = SCRIPTS / "data"


def test_selecionar_sermao_da_montanha():
    dados = sa.carregar_dados(DATA)
    res = sa.selecionar("Qual o significado do Sermao da Montanha e quem o proferiu?", dados)
    ids = [p["id"] for p in res["personas_primarias"]]
    assert "persona-jesus" in ids
    hist_ids = [h["id"] for h in res["historiadores_complementares"]]
    assert "historiador-novo-testamento" in hist_ids


def test_selecionar_lei_aciona_moises():
    dados = sa.carregar_dados(DATA)
    res = sa.selecionar("Explique a Lei Mosaica e os Dez Mandamentos no Exodo", dados)
    assert res["personas_primarias"][0]["id"] == "persona-moises"


def test_selecionar_fallback_sem_match():
    dados = sa.carregar_dados(DATA)
    res = sa.selecionar("xyzzy plugh fnord", dados)
    assert res["fallback"] is True


def test_parse_referencia_simples():
    indice = prb.carregar_livros(DATA)
    refs = prb.extrair("Como entender Joao 3:16 e Mateus 5:1-12?", indice)
    normalizadas = [r["referencia_normalizada"] for r in refs]
    assert "Joao 3:16" in normalizadas
    assert "Mateus 5:1-12" in normalizadas


def test_parse_abreviacao_e_capitulo():
    indice = prb.carregar_livros(DATA)
    refs = prb.extrair("Leia Sl 23 com atencao", indice)
    assert refs and refs[0]["livro"] == "Salmos" and refs[0]["capitulo"] == 23


def test_montar_prompt_inclui_guardrails():
    perfis = mp.carregar_perfis(DATA)
    perfil = mp.buscar_perfil(perfis, "persona-paulo")
    prompt = mp.montar(perfil, "Fale sobre a graca", ["Romanos 3 trata da justificacao."])
    assert "Guardrails" in prompt
    assert "Paulo" in prompt
    assert "Marcio Bisognin" in prompt


def test_validar_fidelidade_reprova_sem_referencia():
    rel = vf.validar("Deus e amor.", DATA)
    assert rel["aprovado"] is False
    assert any("referencia" in p for p in rel["problemas"])


def test_validar_fidelidade_aprova_completa():
    resposta = (
        "Esta e uma representacao didatica de IA. Em Joao 3:16 vemos o amor de Deus. "
        "Licenca: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."
    )
    rel = vf.validar(resposta, DATA)
    assert rel["aprovado"] is True
