from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

spec = importlib.util.spec_from_file_location("contabil_core", SCRIPTS / "contabil_core.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Não foi possível carregar contabil_core.py")
contabil_core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contabil_core)
analyse_case = contabil_core.analyse_case
canonical_hash = contabil_core.canonical_hash
money = contabil_core.money


def load(name: str):
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


def test_decimal_conversion_is_exact():
    assert str(money("0.1")) == "0.10"


def test_clean_case_proposes_no_restriction():
    result = analyse_case(load("caso_sem_restricao.json"))
    assert result["conclusion_proposal"] == "sem_restricao_proposta"
    assert result["findings"] == []
    assert result["requires_accountant_approval"] is True
    assert result["final_decision"] is None


def test_inconsistent_case_detects_core_findings():
    result = analyse_case(load("caso_com_inconsistencias.json"))
    codes = {item["code"] for item in result["findings"]}
    assert {"SALDO_NAO_RECONCILIADO", "SALDO_INVERTIDO", "SALDO_ALONGADO", "EQUACAO_DESEQUILIBRADA", "DEMONSTRACAO_DESEQUILIBRADA", "EVIDENCIA_INSUFICIENTE"}.issubset(codes)
    assert result["conclusion_proposal"] == "com_restricao_proposta"


def test_all_findings_are_traceable_and_human_gated():
    result = analyse_case(load("caso_com_inconsistencias.json"))
    for item in result["findings"]:
        assert item["id"].startswith("ACH-")
        assert item["normative_ref"]
        assert item["object_ref"]
        assert item["requires_human_approval"] is True


def test_regularization_plan_never_contains_transaction_command():
    result = analyse_case(load("caso_com_inconsistencias.json"))
    assert result["regularization_plan"]
    for step in result["regularization_plan"]:
        assert step["transaction_command"] is None
        assert step["approval_status"] == "pendente_contador"
        assert step["execution_status"] == "nao_executado"


def test_invalid_input_is_blocked():
    result = analyse_case({"case_id": "X"})
    assert result["conclusion_proposal"] == "pendente_dados"
    assert result["validation_errors"]


def test_hash_is_stable():
    data = load("caso_sem_restricao.json")
    assert canonical_hash(data) == canonical_hash(json.loads(json.dumps(data)))


def test_cli_generates_four_auditable_outputs(tmp_path):
    out = tmp_path / "run"
    completed = subprocess.run(
        [sys.executable, str(SCRIPTS / "contabil_core.py"), "--input", str(ROOT / "examples" / "caso_com_inconsistencias.json"), "--output-dir", str(out)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    expected = {"analysis.json", "matriz_achados.csv", "plano_regularizacao.md", "relatorio_conformidade.md"}
    assert expected == {path.name for path in out.iterdir()}
    analysis = json.loads((out / "analysis.json").read_text(encoding="utf-8"))
    assert analysis["final_decision"] is None
    assert "não substitui" in (out / "relatorio_conformidade.md").read_text(encoding="utf-8")
