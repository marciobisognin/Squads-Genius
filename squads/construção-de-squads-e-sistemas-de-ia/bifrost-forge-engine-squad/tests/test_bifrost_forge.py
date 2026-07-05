"""Testes end-to-end do Bifröst Forge Engine.

Cobrem: forja completa, presença de artefatos, verificação de determinismo
(mesma entrada ⇒ mesma árvore SHA256), integridade do Saga Ledger e veredito
'go' do validador Heimdall.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from saga_briefing import load_briefing  # noqa: E402
from bifrost_orchestrator import BifrostOrchestrator, tree_hash  # noqa: E402
from saga_ledger import SagaLedger  # noqa: E402
import heimdall_validate  # noqa: E402

BRIEFING = ROOT / "examples" / "briefing_valhalla_knowledge.yaml"


@pytest.fixture(scope="module")
def forged(tmp_path_factory):
    out = tmp_path_factory.mktemp("bifrost")
    briefing = load_briefing(BRIEFING)
    report = BifrostOrchestrator(briefing, out).forge()
    return out, report


def test_core_artifacts_present(forged):
    out, _ = forged
    for rel in ["squad.yaml", "README.md", "LICENSE", "NOTICE.md", "AUTHORS.md"]:
        assert (out / rel).is_file(), f"faltou {rel}"
    for d in ["agents", "tasks", "workflows", "scripts", "examples", "docs", "tests"]:
        assert (out / d).is_dir(), f"faltou dir {d}"


def test_report_go(forged):
    _, report = forged
    assert report["go_no_go"] in {"go", "go-with-human-review"}
    assert report["score"] >= 70
    assert not report["tests_failed"]


def test_determinism_same_hash():
    briefing = load_briefing(BRIEFING)
    hashes = []
    for _ in range(2):
        d = Path(tempfile.mkdtemp(prefix="det-"))
        BifrostOrchestrator(briefing, d).forge()
        hashes.append(tree_hash(d)[0])
    assert hashes[0] == hashes[1], "determinismo quebrado: hashes diferentes"


def test_ledger_integrity(forged):
    out, _ = forged
    ok, issues = SagaLedger.verify(out / ".saga" / "saga_ledger.jsonl")
    assert ok, f"ledger corrompido: {issues}"


def test_heimdall_go(forged):
    out, _ = forged
    report = heimdall_validate.validate(out, str(BRIEFING))
    assert report["go_no_go"] != "no-go", report.get("issues")
    assert report["traceability"]["coverage_pct"] >= 60
