"""Testes dos pilares Empresas (Asgard Company Forge) e Mentes (Sága Mind-Keeper).

Cobrem: forja de empresa determinística, presença de organograma, integridade do
ledger da empresa, salvaguarda de PI da biblioteca de mentes e injeção de perfil.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from company_briefing import load_company_briefing  # noqa: E402
from asgard_company_forge import CompanyForge, design_org  # noqa: E402
from bifrost_orchestrator import tree_hash  # noqa: E402
from saga_ledger import SagaLedger  # noqa: E402
from mind_clone_library import MindCloneLibrary, inject  # noqa: E402

COMPANY = ROOT / "examples" / "company_briefing_valhalla_ventures.yaml"
VOICE = ROOT / "examples" / "voice_sample_institucional.txt"


def _forge(tmp):
    briefing = load_company_briefing(COMPANY)
    return briefing, CompanyForge(briefing, tmp).forge()


def test_company_org_present(tmp_path):
    briefing, report = _forge(tmp_path)
    assert report["go_no_go"] == "go"
    for rel in ["company.yaml", "README.md", "governance.md", "LICENSE", "NOTICE.md", "AUTHORS.md"]:
        assert (tmp_path / rel).is_file(), rel
    assert (tmp_path / "employees").is_dir()
    assert (tmp_path / "departments").is_dir()
    assert report["employees"] >= 4


def test_company_determinism():
    briefing = load_company_briefing(COMPANY)
    hashes = []
    for _ in range(2):
        d = Path(tempfile.mkdtemp(prefix="co-det-"))
        CompanyForge(briefing, d).forge()
        hashes.append(tree_hash(d)[0])
    assert hashes[0] == hashes[1]


def test_company_ledger_integrity(tmp_path):
    _forge(tmp_path)
    ok, issues = SagaLedger.verify(tmp_path / ".saga" / "company_ledger.jsonl")
    assert ok, issues


def test_mind_library_add_and_inject(tmp_path):
    lib = MindCloneLibrary(tmp_path / "dna")
    profile = lib.add("Voz Institucional", VOICE)
    assert profile["id"] == "voz-institucional"
    assert set(profile["layers"].keys()) >= {"1_voice_cadence", "5_tone_markers"}
    enriched = lib.inject_into("Voz Institucional", {"name": "Delivery Builder"})
    assert "voice_profile" in enriched
    assert enriched["voice_profile"]["mind_id"] == "voz-institucional"


def test_mind_safeguard_no_verbatim(tmp_path):
    """A biblioteca não pode emitir n-gramas verbatim de 4+ palavras da fonte."""
    lib = MindCloneLibrary(tmp_path / "dna")
    profile = lib.add("Voz Institucional", VOICE)
    src = VOICE.read_text(encoding="utf-8").lower()
    # nenhum termo temático deve ser uma sequência longa da fonte
    for item in profile["layers"]["4_thematic_vectors"]["top_content_terms"]:
        assert len(item["term"].split()) == 1


def test_inject_pure_function():
    agent = {"name": "X"}
    out = inject({"id": "m1", "layers": {"5_tone_markers": {"register": "formal"}}}, agent)
    assert out["voice_profile"]["register"] == "formal"
    assert agent == {"name": "X"}  # não muta o original
