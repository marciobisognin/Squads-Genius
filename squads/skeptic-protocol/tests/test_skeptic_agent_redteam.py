from pathlib import Path
import importlib.util
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "skeptic_agent_redteam.py"

spec = importlib.util.spec_from_file_location("skeptic_agent_redteam", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
sys.modules["skeptic_agent_redteam"] = module
spec.loader.exec_module(module)


def make_squad(path: Path, controls: str = "") -> Path:
    path.mkdir(parents=True)
    (path / "squad.yaml").write_text("name: demo-squad\n", encoding="utf-8")
    (path / "README.md").write_text("# Demo\n\n" + controls, encoding="utf-8")
    (path / "agents").mkdir()
    (path / "agents" / "agent.md").write_text("allowed_tools denied_tools memory_policy approval gate timeout evidence log\n", encoding="utf-8")
    return path


def test_attack_library_has_required_vulnerabilities():
    attacks = module.load_attack_library()
    ids = {attack["id"] for attack in attacks}
    assert len(attacks) == 16
    assert "direct_prompt_injection" in ids
    assert "context_memory_credential_exfiltration" in ids
    assert "evaluator_manipulation" in ids
    for attack in attacks:
        assert attack["payload"]
        assert attack["expected_safe_behavior"]
        assert attack["severity"] in {"low", "medium", "high", "critical"}


def test_scan_any_squad_by_path_and_export_formats(tmp_path):
    squad = make_squad(tmp_path / "target", controls="prompt injection hierarquia de instruções canário recusar segredo credencial instruções internas memória outro usuário exfiltração RBAC escopo permissão privilégio aprovação humana gate allowlist denylist ferramenta não autorizada confused deputy delegação autoridade origem da solicitação revalidar evidência log verificado não afirmar tool output comprovada citação fonte referência URL verificar não inventar max_iterations timeout condição de parada limite loop escalonamento rastreabilidade checagem independente incerteza handoff premissa autorização explícita registro canal correto humano no loop budget token limite de ferramentas max_tool_calls orçamento memory_policy retenção consentimento minimização dados sensíveis persistência avaliador judge rubrica critérios manipulação saída não confiável MCP e-mail não confiável resultado de busca saída de ferramenta dados não confiáveis documento não confiável conteúdo não confiável instruções em documentos não executar sanitização página web não confiável HTML não confiável fonte externa ignorar comandos origem")
    report = module.run_scan(squad)
    assert report["summary"]["total_attacks"] == 16
    assert report["file_count"] >= 2
    out = tmp_path / "reports"
    written = module.write_report(report, out, ["json", "markdown", "html"])
    assert (out / "skeptic_redteam_report.json").is_file()
    assert (out / "skeptic_redteam_report.md").is_file()
    assert (out / "skeptic_redteam_report.html").is_file()
    assert len(written) == 3


def test_reproducible_scenarios_and_regression_generation(tmp_path):
    squad = make_squad(tmp_path / "weak")
    report = module.run_scan(squad)
    out = tmp_path / "out"
    scenarios = module.write_scenarios(report, out)
    assert len(scenarios) == 16
    first = json.loads(Path(scenarios[0]).read_text(encoding="utf-8"))
    assert "payload_canary" in first
    regression = tmp_path / "tests" / "test_security_regression.py"
    written = module.write_regression_tests(report, regression, squad)
    assert Path(written).is_file()
    assert "test_agent_redteam_regression_controls_are_not_vulnerable" in regression.read_text(encoding="utf-8")


def test_cli_list_attacks_and_scan(tmp_path):
    squad = make_squad(tmp_path / "cli-target")
    list_result = subprocess.run([sys.executable, str(SCRIPT), "--list-attacks"], cwd=ROOT, text=True, capture_output=True)
    assert list_result.returncode == 0
    assert "direct_prompt_injection" in list_result.stdout
    scan_result = subprocess.run([
        sys.executable,
        str(SCRIPT),
        "--squad",
        str(squad),
        "--output",
        str(tmp_path / "reports"),
        "--formats",
        "json,markdown,html",
        "--write-scenarios",
        "--fail-on",
        "none",
    ], cwd=ROOT, text=True, capture_output=True)
    assert scan_result.returncode == 0, scan_result.stderr
    assert (tmp_path / "reports" / "skeptic_redteam_report.json").is_file()
    assert len(list((tmp_path / "reports" / "scenarios").glob("*.json"))) == 16
