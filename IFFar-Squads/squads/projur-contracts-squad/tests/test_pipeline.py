"""Teste de integração leve: classificação e checagem de cláusulas essenciais."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import classify_instrument as ci  # noqa: E402
import check_essential_clauses as ce  # noqa: E402


def test_classify_contrato():
    texto = (ROOT / "examples" / "lote" / "contrato_001.txt").read_text(encoding="utf-8")
    tipo, conf, _ = ci.classify(texto)
    assert tipo == "contrato"
    assert conf > 0


def test_classify_convenio():
    texto = (ROOT / "examples" / "lote" / "convenio_002.txt").read_text(encoding="utf-8")
    tipo, _, _ = ci.classify(texto)
    assert tipo in ("convenio", "contrato_fundacao_apoio")


def test_essenciais_constantes():
    # o contrato de exemplo cobre as principais cláusulas essenciais
    assert "objeto" in ce.ESSENCIAIS
    assert "foro" in ce.ESSENCIAIS
    assert len(ce.ESSENCIAIS) >= 8
