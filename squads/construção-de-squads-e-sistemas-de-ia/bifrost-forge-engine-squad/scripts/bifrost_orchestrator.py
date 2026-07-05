#!/usr/bin/env python3
"""Allfather Orchestrator — máquina de estados da forja, com Saga Ledger e checkpoints.

Este é o coração do engine. Ao contrário de uma persona apenas descritiva, aqui a
orquestração é código real:

  * fases explícitas com gates;
  * checkpoints resumíveis (`--resume`);
  * trilha de auditoria encadeada por hash (Saga Ledger, JSONL + SHA256);
  * hash de determinismo da árvore de saída (mesma entrada ⇒ mesma árvore).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from saga_briefing import Briefing, load_briefing
from saga_ledger import SagaLedger
from runic_architect import analyze_requirements, design_architecture
from norn_workflows import generate_tasks, generate_workflows, generate_task_files, generate_workflow_files
from valkyrie_agents import generate_agent_files
from eitri_design import generate_design_system
from brokkr_scripts import generate_scripts
from package_saga import (
    base_package_files, build_manifest, dump_yaml, generate_documentation, generate_tests,
    quality_report, static_validations, write_text,
)

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

# Arquivos/pastas ignorados no hash de determinismo (metadados de build, não artefatos).
_DETERMINISM_EXCLUDE_PREFIXES = (".saga/",)
_DETERMINISM_EXCLUDE_NAMES = {"quality_report.json", "quality_report.md"}


def tree_hash(root: Path) -> Tuple[str, Dict[str, str]]:
    """Hash SHA256 estável da árvore de artefatos (exclui metadados de build)."""
    per_file: Dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if rel in _DETERMINISM_EXCLUDE_NAMES or any(rel.startswith(p) for p in _DETERMINISM_EXCLUDE_PREFIXES):
            continue
        per_file[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    material = "\n".join(f"{rel}:{digest}" for rel, digest in sorted(per_file.items()))
    return hashlib.sha256(material.encode("utf-8")).hexdigest(), per_file


class BifrostOrchestrator:
    """Orquestra a forja por fases, com auditoria e checkpoints."""

    def __init__(self, briefing: Briefing, output: Path, deterministic: bool = True) -> None:
        self.briefing = briefing
        self.output = Path(output)
        self.deterministic = deterministic
        self.context: Dict[str, Any] = {"briefing": briefing}
        self.files: Dict[str, str] = {}
        self._ledger: Optional[SagaLedger] = None

    # ---- fases ---------------------------------------------------------
    def _phase_intake(self) -> None:
        self.context["analysis"] = analyze_requirements(self.briefing)

    def _phase_architecture(self) -> None:
        self.context["architecture"] = design_architecture(self.briefing, self.context["analysis"])

    def _phase_flows(self) -> None:
        arch = self.context["architecture"]
        tasks = generate_tasks(self.briefing, arch)
        workflows = generate_workflows(self.briefing, tasks)
        self.context["tasks"] = tasks
        self.context["workflows"] = workflows

    def _phase_assemble(self) -> None:
        b, arch = self.briefing, self.context["architecture"]
        tasks, workflows = self.context["tasks"], self.context["workflows"]
        manifest = build_manifest(b.project_name, arch["slug"], arch, tasks, workflows, b.to_dict())
        self.files["squad.yaml"] = dump_yaml(manifest)
        self.files.update(generate_agent_files(arch["agents"]))
        self.files.update(generate_task_files(tasks))
        self.files.update(generate_workflow_files(workflows))
        self.files.update(generate_design_system(b.project_name))
        self.files.update(generate_scripts(b.project_name))
        self.files.update(generate_documentation(b, arch, self.context["analysis"]))
        self.files.update(base_package_files(b.project_name))
        self.files["examples/briefing.sample.yaml"] = dump_yaml(b.to_dict())
        self.files["examples/README.md"] = (
            f"# Exemplos — {b.project_name}\n\n"
            "`briefing.sample.yaml` contém o briefing normalizado que originou este squad.\n\n"
            f"{FOOTER}\n"
        )
        self.files.update(generate_tests(sorted(self.files.keys()) + ["quality_report.json"]))

    PHASES: List[Tuple[str, str, bool]] = [
        ("intake", "_phase_intake", True),
        ("architecture", "_phase_architecture", False),
        ("flows", "_phase_flows", False),
        ("assemble", "_phase_assemble", True),
    ]

    # ---- execução ------------------------------------------------------
    def plan(self) -> Dict[str, Any]:
        """Executa as fases em memória (sem gravar) e devolve o plano."""
        self._run_phases(ledger=None)
        arch, analysis = self.context["architecture"], self.context["analysis"]
        return {
            "project_name": self.briefing.project_name,
            "slug": arch["slug"],
            "components_planned": sorted(self.files.keys()),
            "agent_count": len(arch["agents"]),
            "task_count": len(self.context["tasks"]),
            "workflow_count": len(self.context["workflows"]),
            "non_redundant": arch["non_redundant"],
            "risks": analysis["risks"],
            "human_review_required": analysis["human_review_required"],
        }

    def _run_phases(self, ledger: Optional[SagaLedger], completed: Optional[set] = None) -> None:
        completed = completed or set()
        for name, handler, gate in self.PHASES:
            if name in completed:
                continue
            if ledger:
                ledger.record(name, "phase_start", {"gate": gate})
            getattr(self, handler)()
            if ledger:
                payload = {"artifacts": sorted(self.files.keys())} if name == "assemble" else {}
                ledger.record(name, "phase_end", payload)

    def forge(self, resume: bool = False) -> Dict[str, Any]:
        self.output.mkdir(parents=True, exist_ok=True)
        saga_dir = self.output / ".saga"
        saga_dir.mkdir(exist_ok=True)
        checkpoint_path = saga_dir / "checkpoint.json"
        completed: set = set()
        if resume and checkpoint_path.exists():
            completed = set(json.loads(checkpoint_path.read_text(encoding="utf-8")).get("completed", []))

        self._ledger = SagaLedger(saga_dir / "saga_ledger.jsonl", deterministic=self.deterministic)
        self._ledger.record("forge", "run_start", {"project": self.briefing.project_name, "resume": resume})
        self._run_phases(self._ledger, completed)
        checkpoint_path.write_text(json.dumps({"completed": [p[0] for p in self.PHASES]}, ensure_ascii=False, indent=2), encoding="utf-8")

        for rel, content in self.files.items():
            write_text(self.output / rel, content if content.endswith("\n") else content + "\n")

        # relatório rascunho (permite validar presença antes dos testes)
        analysis = self.context["analysis"]
        draft = {"go_no_go": "pending-tests", "score": 0, "risks_found": analysis["risks"]}
        write_text(self.output / "quality_report.json", json.dumps(draft, ensure_ascii=False, indent=2) + "\n")

        validations = static_validations(self.output)
        tests_passed, tests_failed = self._run_pytest(self.output)
        report = quality_report(
            components=list(self.files.keys()), validations=validations["validations"],
            risks=analysis["risks"], human_review=analysis["human_review_required"],
            tests_passed=tests_passed, tests_failed=tests_failed,
        )
        digest, per_file = tree_hash(self.output)
        report["determinism_hash"] = digest
        report["files_hashed"] = len(per_file)
        write_text(self.output / "quality_report.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")

        self._ledger.record("forge", "run_end", {"determinism_hash": digest, "go_no_go": report["go_no_go"], "score": report["score"]})
        report["ledger_head"] = self._ledger.head
        return report

    @staticmethod
    def _run_pytest(root: Path) -> Tuple[List[str], List[str]]:
        try:
            result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=root, text=True, capture_output=True)
        except Exception as exc:  # pragma: no cover
            return [], [f"pytest não executado: {exc}"]
        tail = (result.stdout + "\n" + result.stderr).strip().splitlines()[-6:]
        label = "pytest -q :: " + " | ".join(tail)
        return ([label], []) if result.returncode == 0 else ([], [label])


if __name__ == "__main__":  # pragma: no cover
    import argparse
    ap = argparse.ArgumentParser(description="Executa a forja orquestrada (uso avançado; prefira bifrost_forge.py).")
    ap.add_argument("--briefing", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()
    briefing = load_briefing(args.briefing)
    orch = BifrostOrchestrator(briefing, Path(args.output))
    print(json.dumps(orch.forge(resume=args.resume), ensure_ascii=False, indent=2))
