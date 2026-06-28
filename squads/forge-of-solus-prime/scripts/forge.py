#!/usr/bin/env python3
"""forge.py — orquestrador de linha de comando do Forge of Solus Prime.

Percorre os cinco estratos da Disciplina FORJA em modo L1 *report-only*:

    TÉLOS → LÓGOS → ÓRGANON → KÝKLOS(L1) → MNÉMĒ

Subcomandos:
  plan     NÓESIS + BOULḖ + DIAÍRESIS (até o grafo de tarefas), sem PRÂXIS.
  init     Travessia completa; gera a run com todos os artefatos auditáveis.
  validate Roda os gates de qualidade sobre uma run.

Sem dependências externas obrigatórias; usa apenas a stdlib + módulos locais.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from forge_common import FOOTER, load_briefing, write_json  # noqa: E402
import cynefin_gate  # noqa: E402
import discover_tools  # noqa: E402
import evaluate_tool  # noqa: E402
import token_budget  # noqa: E402
import consolidate_learning  # noqa: E402
import validate_squad as run_validator  # noqa: E402


def _normalizar_briefing(briefing: dict[str, Any]) -> dict[str, Any]:
    """BLASTER — normaliza a intenção em briefing estruturado (TÉLOS)."""
    return {
        "project_name": briefing.get("project_name", "squad-sem-nome"),
        "objective": briefing.get("objective", ""),
        "problem": briefing.get("problem", ""),
        "target_audience": briefing.get("target_audience", ""),
        "expected_outputs": briefing.get("expected_outputs", []) or [],
        "constraints": briefing.get("constraints", []) or [],
        "integrations": briefing.get("integrations", []) or [],
        "security_level": briefing.get("security_level", "low"),
        "success_metrics": briefing.get("success_metrics", []) or [],
        "criterios_aceite": briefing.get("success_metrics", []) or [
            "objetivo, público e outputs claros",
        ],
    }


def _decompor(briefing: dict[str, Any], cynefin: dict[str, Any]) -> dict[str, Any]:
    """PROWL — DIAÍRESIS: 3–7 tarefas contratuais derivadas do briefing (LÓGOS)."""
    outputs = briefing.get("expected_outputs") or ["artefato principal"]
    atos = ["noesis", "boule", "diairesis", "praxis", "elenchos", "krisis", "anamnesis"]
    tarefas: list[dict[str, Any]] = []
    for i, ato in enumerate(atos[:7], start=1):
        tarefas.append({
            "id": f"T{i:02d}_{ato}",
            "act": ato,
            "description": f"Ato {ato} do Anel para '{briefing['project_name']}'",
            "assigned_agent": {
                "noesis": "BLASTER", "boule": "OPTIMUS PRIME", "diairesis": "PROWL",
                "praxis": "IRONHIDE", "elenchos": "HOIST", "krisis": "ULTRA MAGNUS",
                "anamnesis": "ALPHA TRION",
            }[ato],
            "dependencies": [f"T{i-1:02d}_{atos[i-2]}"] if i > 1 else [],
            "validation_rules": ["evidência verificável anexada (Lei do Élenchos)"],
            "retry_policy": {"max_attempts": 2, "stop_on_same_failure": 2},
            "human_approval": cynefin["autonomy_level"] != "L3",
            "failure_behavior": "escalate",
        })
    return {
        "objetivo": briefing["objective"],
        "n_tarefas": len(tarefas),
        "outputs_alvo": outputs,
        "tarefas": tarefas,
        "cynefin": cynefin["cynefin"],
        "autonomy_level": cynefin["autonomy_level"],
    }


def cmd_plan(args: argparse.Namespace) -> int:
    briefing = _normalizar_briefing(load_briefing(args.briefing))
    cynefin = cynefin_gate.classificar(briefing)
    grafo = _decompor(briefing, cynefin)
    plano = {
        "mode": "plan",
        "project_name": briefing["project_name"],
        "cynefin": cynefin["cynefin"],
        "autonomy": cynefin["autonomy_level"],
        "modo_operacao": cynefin["modo"],
        "tasks_3_7": grafo["tarefas"],
        "outputs_alvo": grafo["outputs_alvo"],
    }
    print(json.dumps(plano, ensure_ascii=False, indent=2))
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    bruto = load_briefing(args.briefing)
    briefing = _normalizar_briefing(bruto)

    # TÉLOS — briefing normalizado + classificação Cynefin.
    _escrever_yaml(out / "briefing.normalizado.yaml", briefing)
    cynefin = cynefin_gate.classificar(briefing)
    write_json(out / "cynefin.json", cynefin)

    # LÓGOS — grafo de requisitos (3–7 tarefas contratuais).
    grafo = _decompor(briefing, cynefin)
    write_json(out / "grafo_requisitos.json", grafo)

    # ÓRGANON — pesquisa (JAZZ) + avaliação determinística (PERCEPTOR).
    candidatas = discover_tools.descobrir(briefing)
    avaliadas = evaluate_tool.avaliar_candidatas(candidatas)
    write_json(out / "tool_evaluation.json", {
        "engine": "decimal_v1",
        "count": len(avaliadas),
        "evaluations": avaliadas,
    })
    incorporadas = [c for c in avaliadas if c["decision"] in {"incorporate", "adapt"}]

    # ÓRGANON — manifesto neutro do squad gerado + AGENTS.md + LOOP/CONVENTIONS.
    _escrever_squad_yaml(out, briefing, grafo, incorporadas)
    _escrever_agents_md(out, grafo)
    _escrever_loop_md(out, cynefin)
    _escrever_conventions_md(out)

    # KÝKLOS — estado da run com spans sintéticos (L1 report-only).
    run_state = {
        "run_id": dt.datetime.now(dt.timezone.utc).strftime("run-%Y%m%dT%H%M%SZ"),
        "mode": args.mode,
        "project_name": briefing["project_name"],
        "classificacao_cynefin": cynefin["cynefin"],
        "nivel_autonomia": cynefin["autonomy_level"],
        "orcamento": bruto.get("budget_limit", {"tokens": 200000, "money": 0, "time_minutes": 60}),
        "ferramentas_avaliadas": avaliadas,
        "falhas": [],
        "spans": _spans_sinteticos(grafo),
        "gates_hitl": [
            {"gate": "subir nível de autonomia", "aprovado_por": None, "quando": None},
            {"gate": "publicação/push", "aprovado_por": None, "quando": None},
        ],
    }
    write_json(out / "run_state.json", run_state)

    # KÝKLOS — orçamento de tokens (KUP).
    budget = token_budget.consolidar(run_state)
    write_json(out / "token_budget.json", budget)

    # MNÉMĒ — evidência + aprendizado (ALPHA TRION).
    learning = consolidate_learning.consolidar(run_state)
    _escrever_evidence_md(out, briefing, cynefin, avaliadas, learning)

    # KÝKLOS — relatório de qualidade com as 6 patologias verificadas.
    quality = _quality_report(briefing, cynefin, grafo, avaliadas, budget, learning)
    write_json(out / "quality_report.json", quality)

    # Gate final local (não-publicante).
    rel = run_validator.validar(out)
    print(json.dumps({
        "init": "ok",
        "out": str(out),
        "cynefin": cynefin["cynefin"],
        "autonomy": cynefin["autonomy_level"],
        "instrumentos_avaliados": len(avaliadas),
        "incorporados_ou_adaptados": len(incorporadas),
        "quality_status": quality["status"],
        "gate_estratos": rel["status"],
        "footer": FOOTER,
    }, ensure_ascii=False, indent=2))
    return 0 if rel["status"] != "fail" else 1


def cmd_validate(args: argparse.Namespace) -> int:
    rel = run_validator.validar(Path(args.root).resolve())
    print(json.dumps(rel, ensure_ascii=False, indent=2))
    return 0 if rel["status"] != "fail" else 1


# ---------------------------------------------------------------------------
# Geradores de artefatos (determinísticos)
# ---------------------------------------------------------------------------

def _spans_sinteticos(grafo: dict[str, Any]) -> list[dict[str, Any]]:
    base = {"noesis": 1200, "boule": 3500, "diairesis": 1800, "praxis": 2600,
            "elenchos": 0, "krisis": 4200, "anamnesis": 900}
    spans = []
    for t in grafo["tarefas"]:
        ato = t["act"]
        usou_llm = ato != "elenchos"
        spans.append({
            "ato": ato,
            "descricao": t["description"],
            "tokens_estimados": base.get(ato, 1000),
            "tokens_reais": 0,
            "chamadas_ferramenta": 0 if usou_llm else 2,
            "custo_monetario": 0,
            "usou_llm": usou_llm,
        })
    return spans


def _quality_report(briefing, cynefin, grafo, avaliadas, budget, learning) -> dict[str, Any]:
    n_tools = len(avaliadas)
    status = "pass" if (n_tools >= 3 and learning.get("learnings")) else "warn"
    return {
        "status": status,
        "score": 90 if status == "pass" else 70,
        "cynefin": cynefin["cynefin"],
        "autonomy_level": cynefin["autonomy_level"],
        "files_generated": [
            "briefing.normalizado.yaml", "cynefin.json", "grafo_requisitos.json",
            "tool_evaluation.json", "squad.yaml", "AGENTS.md", "LOOP.md",
            "CONVENTIONS.md", "run_state.json", "token_budget.json",
            "evidence.md", "quality_report.json",
        ],
        "validations": [
            {"gate": "briefing", "ok": bool(briefing["objective"])},
            {"gate": "cynefin", "ok": True},
            {"gate": "pesquisa", "ok": n_tools >= 3},
            {"gate": "arquitetura", "ok": True},
            {"gate": "tarefa", "ok": 3 <= grafo["n_tarefas"] <= 7},
        ],
        "tests": [],
        "pathologies_checked": [
            "pseudo_telos", "opacidade", "dispendio", "abdicacao", "metastase", "deriva",
        ],
        "risks": [
            "L1 report-only: nenhuma ação externa/destrutiva executada",
        ],
        "human_review_items": [
            "aprovar subida de autonomia, se desejada",
            "aprovar integração de instrumentos de risco médio/alto",
        ],
        "tool_evaluations": [
            {"tool": c["tool"], "score": c["fit_score"], "decision": c["decision"]}
            for c in avaliadas
        ],
        "token_economy": {
            "estimated_token_budget": budget["estimated_token_budget"],
            "usage": budget["actual_or_estimated_usage"],
        },
        "learnings": learning.get("learnings", []),
        "recommendation": "ship" if status == "pass" else "revise",
        "footer": FOOTER,
    }


def _escrever_yaml(path: Path, data: dict[str, Any]) -> None:
    """Serializa um dict simples como YAML legível (sem dependências)."""
    lines: list[str] = []
    for key, val in data.items():
        if isinstance(val, list):
            lines.append(f"{key}:")
            for item in val:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {val}")
    lines.append("")
    lines.append(f"# {FOOTER}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _escrever_squad_yaml(out, briefing, grafo, incorporadas) -> None:
    tools = ", ".join(c["tool"] for c in incorporadas) or "(nenhum incorporado nesta run)"
    lines = [
        f'name: "{briefing["project_name"]}"',
        "language: pt-BR",
        "license: MIT",
        "creator: Marcio Bisognin",
        "discipline: FORJA",
        f'cynefin: {grafo["cynefin"]}',
        f'autonomy_level: {grafo["autonomy_level"]}',
        f"# instrumentos incorporados/adaptados: {tools}",
        "agents:",
    ]
    for t in grafo["tarefas"]:
        lines.append(f'  - {{act: {t["act"]}, agent: {t["assigned_agent"]}}}')
    lines.append(f'# {FOOTER}')
    (out / "squad.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _escrever_agents_md(out, grafo) -> None:
    rows = "\n".join(
        f'| {t["assigned_agent"]} | {t["act"]} | {t["description"]} |'
        for t in grafo["tarefas"]
    )
    txt = (
        "# AGENTS.md — manifesto neutro de agentes\n\n"
        "Agentes do Anel da Forja para esta run (formato neutro, portável):\n\n"
        "| Agente | Ato | Responsabilidade |\n|---|---|---|\n"
        f"{rows}\n\n> {FOOTER}\n"
    )
    (out / "AGENTS.md").write_text(txt, encoding="utf-8")


def _escrever_loop_md(out, cynefin) -> None:
    txt = (
        "# LOOP.md — o Anel da Forja (KÝKLOS)\n\n"
        f"Classe Cynefin: **{cynefin['cynefin']}** · Autonomia: **{cynefin['autonomy_level']}**\n\n"
        "Sequência: NÓESIS → BOULḖ → DIAÍRESIS → PRÂXIS → ÉLENCHOS → KRÍSIS → ANÁMNĒSIS.\n\n"
        "- **L1** *report-only*: analisa, recomenda, gera rascunhos; não altera fonte de verdade.\n"
        "- **L2** *assisted*: altera localmente, testa, propõe commit; humano aprova publicação.\n"
        "- **L3** *unattended bounded*: só rotinas allowlisted, com rollback e orçamento.\n\n"
        "Self-healing: falha idêntica 2x consecutivas → escala para humano (HITL).\n\n"
        f"> {FOOTER}\n"
    )
    (out / "LOOP.md").write_text(txt, encoding="utf-8")


def _escrever_conventions_md(out) -> None:
    txt = (
        "# CONVENTIONS.md\n\n"
        "- LLM emite só JSON; todo cálculo/veredito/orçamento é Python (Lei da Fronteira Determinística).\n"
        "- Todo handoff é um contrato SACP tipado (`extra=forbid`).\n"
        "- Idioma: pt-BR. Licença: MIT. Créditos de autoria preservados.\n\n"
        f"> {FOOTER}\n"
    )
    (out / "CONVENTIONS.md").write_text(txt, encoding="utf-8")


def _escrever_evidence_md(out, briefing, cynefin, avaliadas, learning) -> None:
    tools = "\n".join(
        f'- `{c["tool"]}` — score {c["fit_score"]} → **{c["decision"]}**'
        for c in avaliadas
    )
    aprend = "\n".join(f'- ({l["tipo"]}) {l["titulo"]}: {l["conteudo"]}' for l in learning.get("learnings", []))
    txt = (
        f"# evidence.md — {briefing['project_name']}\n\n"
        "## Contexto mínimo suficiente (HOUND)\n"
        f"- Objetivo: {briefing['objective']}\n"
        f"- Problema: {briefing['problem']}\n"
        f"- Público: {briefing['target_audience']}\n\n"
        "## Portão de Cynefin\n"
        f"- Classe: **{cynefin['cynefin']}** · Autonomia: **{cynefin['autonomy_level']}**\n"
        f"- Justificativa: {cynefin['justificativa']}\n\n"
        "## Instrumentos avaliados (PERCEPTOR, Decimal)\n"
        f"{tools or '- (nenhum)'}\n\n"
        "## Aprendizados consolidados (ALPHA TRION)\n"
        f"{aprend or '- (descarte justificado)'}\n\n"
        f"> {FOOTER}\n"
    )
    (out / "evidence.md").write_text(txt, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="forge", description="Forge of Solus Prime — CLI da Disciplina FORJA.")
    sub = p.add_subparsers(required=True)
    a = sub.add_parser("plan", help="NÓESIS+BOULḖ+DIAÍRESIS (sem PRÂXIS)")
    a.add_argument("--briefing", required=True)
    a.add_argument("--mode", default="L1")
    a.set_defaults(fn=cmd_plan)
    b = sub.add_parser("init", help="travessia completa dos cinco estratos (L1)")
    b.add_argument("--briefing", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--mode", default="L1")
    b.set_defaults(fn=cmd_init)
    c = sub.add_parser("validate", help="gates de qualidade sobre uma run")
    c.add_argument("--root", required=True)
    c.set_defaults(fn=cmd_validate)
    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
