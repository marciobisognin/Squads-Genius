import json
from pathlib import Path

from farol_30_contracts import build_price_evidence, evaluate_specification, extract_attributes, forecast_baseline, validate_contracts

ROOT = Path(__file__).resolve().parents[1]


def test_farol_30_contracts_are_valid():
    report = validate_contracts(ROOT)
    assert report["go_no_go"] == "go", report


def test_extract_attributes_does_not_match_bare_m_or_l_substring():
    # Regressão: "m" (metro) e "l" (litro) sem \b casavam com qualquer palavra
    # que contivesse essas letras (ex.: "plástico" virava capacidade: ["l"]).
    attrs = extract_attributes("Papel sulfite branco A4 75g/m2 resma com 500 folhas")
    assert "dimensao" not in attrs
    assert "capacidade" not in attrs
    attrs_com_medida = extract_attributes("Mangueira de 10mm de diâmetro, comprimento 5 metros")
    assert "10mm" in attrs_com_medida["dimensao"]
    assert "metros" in attrs_com_medida["dimensao"]


def test_specification_engine_separates_contextual_risks():
    result = evaluate_specification("PANELA MARCA EXEMPLO 7 LITROS EM ALUMÍNIO COM CABO REFORÇADO", "UNIDADE", "123")
    classes = {f["classification"] for f in result["findings"]}
    assert "depende_justificativa" in classes
    assert result["human_review_required"]


def test_specification_engine_allows_brand_used_only_as_reference():
    # Regressão: marca citada apenas como referência de qualidade, com similar/
    # equivalente admitido, é uso permitido pelo art. 41 da Lei nº 14.133/2021
    # e não deveria gerar achado de termo restritivo.
    result = evaluate_specification(
        "PANELA MARCA DE REFERÊNCIA TRAMONTINA, 7 LITROS, EM ALUMÍNIO, ADMITIDA SIMILAR DE QUALIDADE EQUIVALENTE",
        "UNIDADE",
    )
    mensagens = [f["message"] for f in result["findings"]]
    assert not any("restritivo" in m for m in mensagens)


def test_price_evidence_has_hash_and_quality_score():
    samples = [
        {"price": 10, "comparable": True, "source": "Compras.gov"},
        {"price": 11, "comparable": True, "source": "PNCP"},
        {"price": 12, "comparable": True, "source": "Ata"},
        {"price": 80, "comparable": False, "source": "não equivalente"},
    ]
    evidence = build_price_evidence(samples, {"source": "teste"})
    assert len(evidence["raw_hash"]) == 64
    assert evidence["stats"]["n"] == 3
    assert evidence["quality_score"] > 0


def test_forecast_baseline_returns_interval_and_human_gate():
    forecast = forecast_baseline([{"quantity": 10}, {"quantity": 12}, {"quantity": 11}, {"quantity": 50}])
    assert forecast["status"] == "baseline"
    assert forecast["probable_interval"][1] >= forecast["central_value"]
    assert forecast["human_review_required"]
