import json
from pathlib import Path

from farol_30_contracts import build_price_evidence, evaluate_specification, forecast_baseline, validate_contracts

ROOT = Path(__file__).resolve().parents[1]


def test_farol_30_contracts_are_valid():
    report = validate_contracts(ROOT)
    assert report["go_no_go"] == "go", report


def test_specification_engine_separates_contextual_risks():
    result = evaluate_specification("PANELA MARCA EXEMPLO 7 LITROS EM ALUMÍNIO COM CABO REFORÇADO", "UNIDADE", "123")
    classes = {f["classification"] for f in result["findings"]}
    assert "depende_justificativa" in classes
    assert result["human_review_required"]


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
