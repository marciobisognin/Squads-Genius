#!/usr/bin/env python3
"""Sistema mental evolutivo do Primus Meta-Orchestrator.

Mantém um "cérebro" persistente em JSON que evolui a cada interação:
registra tarefas roteadas, reforça pesos de conceitos, acompanha desempenho
de cada agente, deriva aprendizados e acumula lacunas (gaps) que podem virar
novos squads.

Estrutura de memory/brain.json:
  version, created_at, updated_at
  interactions[]   -> histórico de roteamentos e resultados
  concept_weights  -> palavra-chave -> peso (reforço + decaimento)
  agent_performance-> "squad/agent" -> {uses, success, fail, score_sum}
  learnings[]      -> insights derivados deterministicamente
  gaps[]           -> necessidades não atendidas (candidatas a novo squad)

Comandos:
  record   --task ... --squad ... --agent ... [--score N] [--outcome success|fail] [--feedback ...]
  gap      --task ... [--note ...]
  recall   --task ...
  evolve   [--decay 0.98]
  stats

Sem dependências externas. Determinístico (exceto timestamps).
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."
DEFAULT_BRAIN = Path("memory/brain.json")

STOPWORDS = {
    "a", "o", "e", "de", "do", "da", "das", "dos", "em", "no", "na", "nos", "nas",
    "para", "por", "com", "sem", "que", "um", "uma", "ao", "aos", "se", "ou", "os",
    "as", "the", "and", "of", "to", "in", "for", "with", "on", "como", "preciso",
    "quero", "fazer", "criar", "gerar", "uma", "meu", "minha", "sobre",
}


def _tokens(text: str) -> list[str]:
    text = (text or "").lower()
    text = re.sub(r"[^0-9a-zà-ÿ\s\-]", " ", text)
    return [t for t in re.split(r"[\s\-]+", text) if len(t) >= 3 and t not in STOPWORDS]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_brain(path: Path) -> dict[str, Any]:
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("interactions", [])
                data.setdefault("concept_weights", {})
                data.setdefault("agent_performance", {})
                data.setdefault("learnings", [])
                data.setdefault("gaps", [])
                return data
        except Exception:
            pass
    return {
        "version": 1,
        "created_at": _now(),
        "updated_at": _now(),
        "interactions": [],
        "concept_weights": {},
        "agent_performance": {},
        "learnings": [],
        "gaps": [],
        "footer": FOOTER,
    }


def save_brain(path: Path, brain: dict[str, Any]) -> None:
    brain["updated_at"] = _now()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(brain, ensure_ascii=False, indent=2), encoding="utf-8")


def derive_learnings(brain: dict[str, Any]) -> list[str]:
    learnings: list[str] = []
    perf = brain["agent_performance"]
    # Agentes mais confiáveis (>=3 usos, alta taxa de sucesso).
    reliable = [
        (k, v) for k, v in perf.items()
        if v["uses"] >= 3 and v["success"] / max(1, v["uses"]) >= 0.7
    ]
    reliable.sort(key=lambda x: (-x[1]["success"], x[0]))
    for k, v in reliable[:5]:
        rate = round(100 * v["success"] / max(1, v["uses"]))
        learnings.append(f"Agente confiável: {k} ({rate}% de sucesso em {v['uses']} usos).")
    # Agentes com baixo desempenho.
    weak = [
        (k, v) for k, v in perf.items()
        if v["uses"] >= 3 and v["success"] / max(1, v["uses"]) < 0.4
    ]
    for k, v in weak[:3]:
        rate = round(100 * v["success"] / max(1, v["uses"]))
        learnings.append(f"Revisar agente: {k} (apenas {rate}% de sucesso em {v['uses']} usos).")
    # Conceitos dominantes na demanda.
    cw = sorted(brain["concept_weights"].items(), key=lambda x: -x[1])[:5]
    if cw:
        top = ", ".join(f"{k}" for k, _ in cw)
        learnings.append(f"Temas mais demandados: {top}.")
    # Lacunas acumuladas.
    open_gaps = [g for g in brain["gaps"] if not g.get("resolved")]
    if open_gaps:
        learnings.append(f"{len(open_gaps)} lacuna(s) aberta(s) sugerem novo agente/squad.")
    return learnings


def cmd_record(brain: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    key = f"{args.squad}/{args.agent}"
    toks = _tokens(args.task)
    for t in set(toks):
        brain["concept_weights"][t] = round(brain["concept_weights"].get(t, 0.0) + 1.0, 4)
    perf = brain["agent_performance"].setdefault(
        key, {"uses": 0, "success": 0, "fail": 0, "score_sum": 0.0})
    perf["uses"] += 1
    perf["score_sum"] = round(perf["score_sum"] + float(args.score or 0.0), 4)
    if args.outcome == "success":
        perf["success"] += 1
    elif args.outcome == "fail":
        perf["fail"] += 1
    brain["interactions"].append({
        "ts": _now(),
        "task": args.task,
        "squad": args.squad,
        "agent": args.agent,
        "score": float(args.score or 0.0),
        "outcome": args.outcome,
        "feedback": args.feedback or "",
        "tokens": toks,
    })
    brain["learnings"] = derive_learnings(brain)
    return {"recorded": key, "interactions": len(brain["interactions"])}


def cmd_gap(brain: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    gap = {
        "ts": _now(),
        "task": args.task,
        "note": args.note or "",
        "tokens": _tokens(args.task),
        "resolved": False,
    }
    brain["gaps"].append(gap)
    brain["learnings"] = derive_learnings(brain)
    return {"gap_recorded": gap["task"], "open_gaps": sum(1 for g in brain["gaps"] if not g.get("resolved"))}


def cmd_recall(brain: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    qtoks = set(_tokens(args.task))
    scored = []
    for it in brain["interactions"]:
        overlap = qtoks & set(it.get("tokens", []))
        if not overlap:
            continue
        boost = sum(brain["concept_weights"].get(t, 0.0) for t in overlap)
        scored.append((round(len(overlap) + 0.1 * boost, 4), it))
    scored.sort(key=lambda x: -x[0])
    # Sugestões agregadas por agente, ponderadas por desempenho.
    agent_votes: dict[str, float] = {}
    for sc, it in scored:
        key = f"{it['squad']}/{it['agent']}"
        perf = brain["agent_performance"].get(key, {})
        rate = perf.get("success", 0) / max(1, perf.get("uses", 1))
        agent_votes[key] = round(agent_votes.get(key, 0.0) + sc * (0.5 + rate), 4)
    suggestions = sorted(agent_votes.items(), key=lambda x: -x[1])[:5]
    return {
        "matches": [
            {"score": sc, "task": it["task"], "agent": f"{it['squad']}/{it['agent']}",
             "outcome": it["outcome"]}
            for sc, it in scored[:5]
        ],
        "suggested_agents": [{"agent": k, "weight": w} for k, w in suggestions],
    }


def cmd_evolve(brain: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    decay = float(args.decay)
    removed = 0
    for k in list(brain["concept_weights"].keys()):
        brain["concept_weights"][k] = round(brain["concept_weights"][k] * decay, 4)
        if brain["concept_weights"][k] < 0.05:
            del brain["concept_weights"][k]
            removed += 1
    brain["version"] = int(brain.get("version", 1)) + 1
    brain["learnings"] = derive_learnings(brain)
    return {"version": brain["version"], "concepts_pruned": removed,
            "learnings": brain["learnings"]}


def cmd_stats(brain: dict[str, Any], _args: argparse.Namespace) -> dict[str, Any]:
    perf = brain["agent_performance"]
    return {
        "version": brain.get("version"),
        "interactions": len(brain["interactions"]),
        "agents_tracked": len(perf),
        "concepts": len(brain["concept_weights"]),
        "open_gaps": sum(1 for g in brain["gaps"] if not g.get("resolved")),
        "learnings": brain["learnings"],
        "top_concepts": sorted(brain["concept_weights"].items(), key=lambda x: -x[1])[:10],
    }


COMMANDS = {
    "record": cmd_record,
    "gap": cmd_gap,
    "recall": cmd_recall,
    "evolve": cmd_evolve,
    "stats": cmd_stats,
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Sistema mental evolutivo do Primus.")
    ap.add_argument("command", choices=sorted(COMMANDS.keys()))
    ap.add_argument("--brain", default=str(DEFAULT_BRAIN))
    ap.add_argument("--task", default="")
    ap.add_argument("--squad", default="")
    ap.add_argument("--agent", default="")
    ap.add_argument("--score", default="0")
    ap.add_argument("--outcome", choices=["success", "fail", "unknown"], default="unknown")
    ap.add_argument("--feedback", default="")
    ap.add_argument("--note", default="")
    ap.add_argument("--decay", default="0.98")
    args = ap.parse_args()

    brain_path = Path(args.brain)
    brain = load_brain(brain_path)
    result = COMMANDS[args.command](brain, args)
    if args.command != "recall" and args.command != "stats":
        save_brain(brain_path, brain)
    elif args.command == "stats":
        # stats e recall não alteram, mas garantimos persistência de learnings em stats
        save_brain(brain_path, brain)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
