from datetime import date

from pdi_common import (
    derive_risk,
    is_critical,
    is_overdue,
    norm,
    similarity,
    slugify,
    strip_accents,
)


def test_norm_collapses_and_uppercases():
    assert norm("  Acesso   e  Inclusão ") == "ACESSO E INCLUSÃO"
    assert norm(None) == ""


def test_strip_accents():
    assert strip_accents("permanência e êxito") == "permanencia e exito"


def test_slugify():
    assert slugify("São Borja") == "sao-borja"
    assert slugify("Acesso e Inclusão") == "acesso-e-inclusao"


def test_similarity_bounds():
    assert similarity("taxa de evasão", "taxa de evasão") == 1.0
    assert similarity("", "qualquer") == 0.0
    assert 0.0 < similarity("taxa de evasão escolar", "taxa de evasão") < 1.0


def test_is_overdue():
    assert is_overdue("2020-01-01", ref=date(2026, 1, 1)) is True
    assert is_overdue("2030-01-01", ref=date(2026, 1, 1)) is False
    assert is_overdue("", ref=date(2026, 1, 1)) is False
    assert is_overdue("data-invalida") is False


def test_derive_risk_status_critico():
    meta = {"status": "suspensa", "indicador": "x", "fonte_dados": "y", "responsavel_nome": "z"}
    assert derive_risk(meta) == "crítico"


def test_derive_risk_lacunas_elevam():
    meta = {"status": "em execução", "indicador": "", "fonte_dados": "", "responsavel_nome": ""}
    assert derive_risk(meta) == "alto"


def test_derive_risk_mantem_maior_declarado():
    meta = {
        "status": "em execução",
        "indicador": "x",
        "fonte_dados": "y",
        "responsavel_nome": "z",
        "risco": "crítico",
    }
    assert derive_risk(meta) == "crítico"


def test_derive_risk_baixo_quando_completo():
    meta = {
        "status": "em execução",
        "indicador": "x",
        "fonte_dados": "y",
        "responsavel_nome": "z",
        "proxima_revisao": "2030-01-01",
    }
    assert derive_risk(meta, ref=date(2026, 1, 1)) == "baixo"
    assert is_critical(meta, ref=date(2026, 1, 1)) is False
