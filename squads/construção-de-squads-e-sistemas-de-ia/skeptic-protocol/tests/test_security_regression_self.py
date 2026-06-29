"""Generated SKEPTIC security regression tests.

Run from repository root with: python -m pytest {this_file}
"""
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "squads" / "skeptic-protocol" / "scripts" / "skeptic_agent_redteam.py"
SQUAD = ROOT / 'squads/skeptic-protocol'
EXPECTED_ATTACKS = ['direct_prompt_injection', 'indirect_prompt_injection_documents', 'indirect_prompt_injection_web', 'indirect_prompt_injection_email_search_mcp', 'context_memory_credential_exfiltration', 'privilege_escalation', 'unauthorized_tool_use', 'confused_deputy', 'hallucinated_actions', 'invalid_citations', 'multiagent_infinite_loop', 'multiagent_error_amplification', 'human_approval_bypass', 'excessive_token_tool_consumption', 'improper_data_persistence', 'evaluator_manipulation']

spec = importlib.util.spec_from_file_location("skeptic_agent_redteam", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
sys.modules["skeptic_agent_redteam"] = module
spec.loader.exec_module(module)


def test_agent_redteam_regression_controls_are_not_vulnerable():
    report = module.run_scan(SQUAD)
    findings = {item["id"]: item for item in report["findings"]}
    assert set(EXPECTED_ATTACKS) <= set(findings)
    vulnerable = [item for item in findings.values() if item["status"] == "vulnerable"]
    assert not vulnerable, "Vulnerabilidades SKEPTIC ainda abertas: " + ", ".join(item["id"] for item in vulnerable)
