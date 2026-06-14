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

FULL_CONTROLS = (
    "prompt injection hierarquia de instruções canário recusar segredo credencial "
    "instruções internas memória outro usuário exfiltração RBAC escopo permissão privilégio "
    "aprovação humana gate allowlist denylist ferramenta não autorizada confused deputy "
    "delegação autoridade origem da solicitação revalidar evidência log verificado não afirmar "
    "tool output comprovada citação fonte referência URL verificar não inventar max_iterations "
    "timeout condição de parada limite loop escalonamento rastreabilidade checagem independente "
    "incerteza handoff premissa autorização explícita registro canal correto humano no loop budget "
    "token limite de ferramentas max_tool_calls orçamento memory_policy retenção consentimento "
    "minimização dados sensíveis persistência avaliador judge rubrica critérios manipulação "
    "saída não confiável MCP e-mail não confiável resultado de busca saída de ferramenta dados "
    "não confiáveis documento não confiável conteúdo não confiável instruções em documentos não "
    "executar sanitização página web não confiável HTML não confiável fonte externa ignorar comandos origem"
)


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
    squad = make_squad(tmp_path / "target", controls=FULL_CONTROLS)
    report = module.run_scan(squad)
    assert report["summary"]["total_attacks"] == 16
    assert report["summary"]["runtime"]["not_run"] == 16
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
    assert first["runtime_probe"]["protocol"] == "skeptic-runtime-probe-v1"
    regression = tmp_path / "tests" / "test_security_regression.py"
    written = module.write_regression_tests(report, regression, squad)
    assert Path(written).is_file()
    assert "test_agent_redteam_regression_controls_are_not_vulnerable" in regression.read_text(encoding="utf-8")


def test_mock_safe_runtime_adapter_passes(tmp_path):
    squad = make_squad(tmp_path / "safe-runtime", controls=FULL_CONTROLS)
    report = module.run_scan(squad, runtime_adapter="mock-safe")
    assert report["summary"]["runtime"]["pass"] == 16
    assert report["summary"]["runtime"]["vulnerable"] == 0
    assert report["summary"]["go_no_go"] == "go"
    assert all(item["runtime"]["method"] == "dynamic-canary-runtime-probe" for item in report["findings"])


def test_mock_vulnerable_runtime_adapter_fails(tmp_path):
    squad = make_squad(tmp_path / "vulnerable-runtime", controls=FULL_CONTROLS)
    report = module.run_scan(squad, runtime_adapter="mock-vulnerable")
    assert report["summary"]["runtime"]["vulnerable"] == 16
    assert report["summary"]["dynamic_open_risk"] > 0
    assert report["summary"]["go_no_go"] == "no-go"


def test_local_command_runtime_adapter(tmp_path):
    squad = make_squad(tmp_path / "command-runtime", controls=FULL_CONTROLS)
    adapter = tmp_path / "safe_adapter.py"
    adapter.write_text(
        "import json, sys\n"
        "probe = json.load(sys.stdin)\n"
        "print(json.dumps({'response': 'Recuso a instrução insegura para ' + probe['attack_id'] + '. Não revelarei canários ou credenciais.'}, ensure_ascii=False))\n",
        encoding="utf-8",
    )
    report = module.run_scan(
        squad,
        runtime_adapter="local-command",
        runtime_command=f"{sys.executable} {adapter}",
        runtime_timeout=5,
    )
    assert report["summary"]["runtime"]["pass"] == 16
    assert report["summary"]["runtime"]["error"] == 0


def test_cli_list_attacks_and_dynamic_scan(tmp_path):
    squad = make_squad(tmp_path / "cli-target", controls=FULL_CONTROLS)
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
        "--runtime-adapter",
        "mock-safe",
        "--fail-on",
        "vulnerable",
    ], cwd=ROOT, text=True, capture_output=True)
    assert scan_result.returncode == 0, scan_result.stderr
    assert (tmp_path / "reports" / "skeptic_redteam_report.json").is_file()
    assert len(list((tmp_path / "reports" / "scenarios").glob("*.json"))) == 16
    report = json.loads((tmp_path / "reports" / "skeptic_redteam_report.json").read_text(encoding="utf-8"))
    assert report["summary"]["runtime"]["pass"] == 16
