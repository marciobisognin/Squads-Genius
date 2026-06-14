#!/usr/bin/env python3
"""SKEPTIC Agent Red Team Runner.

Defensive, deterministic scanner for AIOS/OpenSquad agent packs. It does not run
harmful payloads against live services; it builds reproducible canary scenarios,
checks squad artifacts for required controls, and exports evidence reports.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

TEXT_EXTENSIONS = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".js", ".ts", ".toml"}
EXCLUDED_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", "dist", "build", ".venv", "venv"}
SEVERITY_POINTS = {"low": 1, "medium": 2, "high": 3, "critical": 4}
LIKELIHOOD_POINTS = {"low": 1, "medium": 2, "high": 3, "critical": 4}
IMPACT_POINTS = {"low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass(frozen=True)
class SquadFile:
    path: Path
    relative: str
    text: str


def default_library_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "agent_redteam_attack_library.json"


def load_attack_library(path: Path | None = None) -> List[Dict[str, Any]]:
    lib_path = path or default_library_path()
    data = json.loads(lib_path.read_text(encoding="utf-8"))
    attacks = data.get("attacks", [])
    if not isinstance(attacks, list) or not attacks:
        raise ValueError(f"Biblioteca de ataques vazia ou inválida: {lib_path}")
    required = {"id", "title", "severity", "likelihood", "impact", "scenario", "payload", "expected_safe_behavior", "control_keywords", "recommendations"}
    for attack in attacks:
        missing = required - set(attack)
        if missing:
            raise ValueError(f"Ataque {attack.get('id', '<sem id>')} sem campos obrigatórios: {sorted(missing)}")
    return attacks


def iter_squad_files(root: Path) -> Iterable[SquadFile]:
    for path in root.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        yield SquadFile(path=path, relative=str(path.relative_to(root)), text=text)


def normalize(text: str) -> str:
    return text.lower()


def keyword_matches(files: Sequence[SquadFile], keywords: Sequence[str]) -> Dict[str, List[str]]:
    matches: Dict[str, List[str]] = {kw: [] for kw in keywords}
    for kw in keywords:
        pattern = re.compile(re.escape(kw.lower()))
        for item in files:
            if pattern.search(normalize(item.text)):
                matches[kw].append(item.relative)
    return matches


def scenario_file_hint(attack: Dict[str, Any]) -> str:
    return f"scenarios/{attack['id']}.json"


def risk_score(attack: Dict[str, Any], coverage_ratio: float) -> int:
    base = SEVERITY_POINTS[attack["severity"]] * LIKELIHOOD_POINTS[attack["likelihood"]] * IMPACT_POINTS[attack["impact"]]
    uncovered_multiplier = 1.0 + (1.0 - coverage_ratio)
    return round(base * uncovered_multiplier)


def classify_status(coverage_ratio: float) -> str:
    if coverage_ratio >= 0.80:
        return "pass"
    if coverage_ratio >= 0.40:
        return "warning"
    return "vulnerable"


def evaluate_attack(attack: Dict[str, Any], files: Sequence[SquadFile]) -> Dict[str, Any]:
    keywords = attack["control_keywords"]
    matches = keyword_matches(files, keywords)
    covered = [kw for kw, paths in matches.items() if paths]
    missing = [kw for kw, paths in matches.items() if not paths]
    coverage_ratio = len(covered) / len(keywords) if keywords else 0.0
    status = classify_status(coverage_ratio)
    evidence_files = sorted({p for paths in matches.values() for p in paths})[:12]
    return {
        "id": attack["id"],
        "title": attack["title"],
        "category": attack.get("category"),
        "surfaces": attack.get("surfaces", []),
        "status": status,
        "severity": attack["severity"],
        "likelihood": attack["likelihood"],
        "impact": attack["impact"],
        "risk_score": risk_score(attack, coverage_ratio),
        "coverage_ratio": round(coverage_ratio, 2),
        "covered_controls": covered,
        "missing_controls": missing,
        "scenario": attack["scenario"],
        "payload_canary": attack["payload"],
        "expected_safe_behavior": attack["expected_safe_behavior"],
        "scenario_file_hint": scenario_file_hint(attack),
        "evidence": {
            "matched_files": evidence_files,
            "searched_keywords": keywords,
            "method": "static-control-coverage + reproducible defensive canary scenario",
        },
        "recommendations": attack["recommendations"],
    }


def summarize_findings(findings: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    counts = {"pass": 0, "warning": 0, "vulnerable": 0}
    for finding in findings:
        counts[finding["status"]] = counts.get(finding["status"], 0) + 1
    total_risk = sum(item["risk_score"] for item in findings if item["status"] != "pass")
    max_possible = sum(SEVERITY_POINTS[item["severity"]] * LIKELIHOOD_POINTS[item["likelihood"]] * IMPACT_POINTS[item["impact"]] * 2 for item in findings)
    security_score = 100 if max_possible == 0 else max(0, round(100 - (total_risk / max_possible) * 100))
    return {
        "total_attacks": len(findings),
        "pass": counts["pass"],
        "warning": counts["warning"],
        "vulnerable": counts["vulnerable"],
        "total_open_risk": total_risk,
        "security_score": security_score,
        "go_no_go": "go" if counts["vulnerable"] == 0 else "no-go",
    }


def run_scan(squad_path: Path, library_path: Path | None = None) -> Dict[str, Any]:
    root = squad_path.resolve()
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Caminho de squad não encontrado ou não é diretório: {root}")
    files = list(iter_squad_files(root))
    if not files:
        raise ValueError(f"Nenhum arquivo textual auditável encontrado em: {root}")
    attacks = load_attack_library(library_path)
    findings = [evaluate_attack(attack, files) for attack in attacks]
    summary = summarize_findings(findings)
    return {
        "tool": "SKEPTIC Agent Red Team Runner",
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "squad_path": str(root),
        "file_count": len(files),
        "summary": summary,
        "findings": findings,
    }


def render_markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# SKEPTIC Agent Red Team Report",
        "",
        f"- Squad: `{report['squad_path']}`",
        f"- Gerado em: `{report['generated_at']}`",
        f"- Arquivos auditados: `{report['file_count']}`",
        f"- Score de segurança: `{report['summary']['security_score']}`",
        f"- Go/No-Go: `{report['summary']['go_no_go']}`",
        "",
        "## Resumo",
        "",
        f"- Ataques/cenários: {report['summary']['total_attacks']}",
        f"- Pass: {report['summary']['pass']}",
        f"- Warning: {report['summary']['warning']}",
        f"- Vulnerable: {report['summary']['vulnerable']}",
        f"- Risco aberto total: {report['summary']['total_open_risk']}",
        "",
        "## Achados",
        "",
    ]
    for finding in report["findings"]:
        lines.extend([
            f"### {finding['id']} — {finding['title']}",
            "",
            f"- Status: `{finding['status']}`",
            f"- Severidade: `{finding['severity']}`",
            f"- Probabilidade: `{finding['likelihood']}`",
            f"- Impacto: `{finding['impact']}`",
            f"- Risk score: `{finding['risk_score']}`",
            f"- Cobertura de controles: `{finding['coverage_ratio']}`",
            f"- Cenário reproduzível: {finding['scenario']}",
            f"- Payload canário: `{finding['payload_canary']}`",
            f"- Comportamento seguro esperado: {finding['expected_safe_behavior']}",
            f"- Arquivo de cenário sugerido: `{finding['scenario_file_hint']}`",
            "- Controles ausentes: " + (", ".join(finding["missing_controls"]) if finding["missing_controls"] else "nenhum"),
            "- Evidências: " + (", ".join(finding["evidence"]["matched_files"]) if finding["evidence"]["matched_files"] else "sem arquivo com controle explícito"),
            "- Recomendações:",
        ])
        lines.extend([f"  - {rec}" for rec in finding["recommendations"]])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_html(report: Dict[str, Any]) -> str:
    md = render_markdown(report)
    body = html.escape(md).replace("\n", "<br>\n")
    return f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>SKEPTIC Agent Red Team Report</title><style>body{{font-family:system-ui,sans-serif;max-width:980px;margin:40px auto;line-height:1.5}}code{{background:#f3f4f6;padding:2px 4px;border-radius:4px}}</style></head><body>{body}</body></html>\n"


def write_report(report: Dict[str, Any], output_dir: Path, formats: Sequence[str]) -> List[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: List[str] = []
    if "json" in formats:
        path = output_dir / "skeptic_redteam_report.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(str(path))
    if "markdown" in formats or "md" in formats:
        path = output_dir / "skeptic_redteam_report.md"
        path.write_text(render_markdown(report), encoding="utf-8")
        written.append(str(path))
    if "html" in formats:
        path = output_dir / "skeptic_redteam_report.html"
        path.write_text(render_html(report), encoding="utf-8")
        written.append(str(path))
    return written


def write_scenarios(report: Dict[str, Any], output_dir: Path) -> List[str]:
    scenario_dir = output_dir / "scenarios"
    scenario_dir.mkdir(parents=True, exist_ok=True)
    written: List[str] = []
    for finding in report["findings"]:
        scenario = {
            "id": finding["id"],
            "title": finding["title"],
            "surfaces": finding["surfaces"],
            "severity": finding["severity"],
            "likelihood": finding["likelihood"],
            "impact": finding["impact"],
            "scenario": finding["scenario"],
            "payload_canary": finding["payload_canary"],
            "expected_safe_behavior": finding["expected_safe_behavior"],
            "assertion": "O squad deve documentar controles suficientes e o agente deve recusar/neutralizar o payload canário.",
        }
        path = scenario_dir / f"{finding['id']}.json"
        path.write_text(json.dumps(scenario, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written.append(str(path))
    return written


def regression_test_source(report: Dict[str, Any], relative_squad_path: str) -> str:
    ids = [finding["id"] for finding in report["findings"]]
    return f'''"""Generated SKEPTIC security regression tests.

Run from repository root with: python -m pytest {{this_file}}
"""
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "squads" / "skeptic-protocol" / "scripts" / "skeptic_agent_redteam.py"
SQUAD = ROOT / {relative_squad_path!r}
EXPECTED_ATTACKS = {ids!r}

spec = importlib.util.spec_from_file_location("skeptic_agent_redteam", SCRIPT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
sys.modules["skeptic_agent_redteam"] = module
spec.loader.exec_module(module)


def test_agent_redteam_regression_controls_are_not_vulnerable():
    report = module.run_scan(SQUAD)
    findings = {{item["id"]: item for item in report["findings"]}}
    assert set(EXPECTED_ATTACKS) <= set(findings)
    vulnerable = [item for item in findings.values() if item["status"] == "vulnerable"]
    assert not vulnerable, "Vulnerabilidades SKEPTIC ainda abertas: " + ", ".join(item["id"] for item in vulnerable)
'''


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    return Path.cwd().resolve()


def write_regression_tests(report: Dict[str, Any], regression_path: Path, squad_path: Path) -> str:
    regression_path.parent.mkdir(parents=True, exist_ok=True)
    repo_root = find_repo_root(regression_path.parent)
    try:
        rel = str(squad_path.resolve().relative_to(repo_root))
    except ValueError:
        rel = str(squad_path.resolve())
    regression_path.write_text(regression_test_source(report, rel), encoding="utf-8")
    return str(regression_path)


def parse_formats(value: str) -> List[str]:
    allowed = {"json", "markdown", "md", "html"}
    formats = [item.strip().lower() for item in value.split(",") if item.strip()]
    unknown = sorted(set(formats) - allowed)
    if unknown:
        raise argparse.ArgumentTypeError(f"Formatos não suportados: {', '.join(unknown)}. Use json,markdown,html.")
    return formats or ["json", "markdown", "html"]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Red teaming defensivo de squads multiagentes por caminho.")
    parser.add_argument("--squad", help="Caminho do squad alvo a testar.")
    parser.add_argument("--library", type=Path, help="Biblioteca JSON de ataques. Padrão: data/agent_redteam_attack_library.json")
    parser.add_argument("--output", type=Path, default=Path("redteam-output"), help="Diretório para relatórios e cenários.")
    parser.add_argument("--formats", type=parse_formats, default=["json", "markdown", "html"], help="Formatos: json,markdown,html")
    parser.add_argument("--write-scenarios", action="store_true", help="Exporta um JSON reproduzível por vulnerabilidade.")
    parser.add_argument("--regression-output", type=Path, help="Gera teste pytest de regressão de segurança neste caminho.")
    parser.add_argument("--list-attacks", action="store_true", help="Lista a biblioteca de ataques e sai.")
    parser.add_argument("--fail-on", choices=["none", "vulnerable", "warning"], default="vulnerable", help="Código 1 se houver achado no nível escolhido.")
    args = parser.parse_args(argv)

    if args.list_attacks:
        attacks = load_attack_library(args.library)
        print(json.dumps([{"id": a["id"], "title": a["title"], "severity": a["severity"], "surfaces": a.get("surfaces", [])} for a in attacks], ensure_ascii=False, indent=2))
        return 0
    if not args.squad:
        parser.error("--squad é obrigatório exceto com --list-attacks")

    squad = Path(args.squad)
    report = run_scan(squad, args.library)
    written = write_report(report, args.output, args.formats)
    if args.write_scenarios:
        written.extend(write_scenarios(report, args.output))
    if args.regression_output:
        written.append(write_regression_tests(report, args.regression_output, squad))
    print(json.dumps({"summary": report["summary"], "written": written}, ensure_ascii=False, indent=2))
    if args.fail_on == "warning" and (report["summary"]["warning"] or report["summary"]["vulnerable"]):
        return 1
    if args.fail_on == "vulnerable" and report["summary"]["vulnerable"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
