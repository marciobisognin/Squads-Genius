"""Testes do módulo comum (validação CNPJ/CPF, parsing, similaridade)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import projur_common as pc  # noqa: E402


def test_valid_cnpj():
    assert pc.valid_cnpj("11.222.333/0001-81") is True
    assert pc.valid_cnpj("11.111.111/1111-11") is False


def test_valid_cpf():
    assert pc.valid_cpf("529.982.247-25") is True
    assert pc.valid_cpf("111.111.111-11") is False


def test_classify_document():
    assert pc.classify_document("11.222.333/0001-81") == ("CNPJ", True)
    assert pc.classify_document("529.982.247-25") == ("CPF", True)
    assert pc.classify_document("abc")[0] == "desconhecido"


def test_parse_money_br():
    assert pc.parse_money_br("R$ 1.200.000,00") == 1200000.0
    assert pc.parse_money_br("R$ 350.000,00") == 350000.0
    assert pc.parse_money_br("sem valor") is None


def test_parse_date_br():
    assert pc.parse_date_br("01/03/2025") == "2025-03-01"
    assert pc.parse_date_br("nada") is None


def test_similarity():
    assert pc.similarity("Contrato Administrativo", "contrato administrativo") > 0.95
