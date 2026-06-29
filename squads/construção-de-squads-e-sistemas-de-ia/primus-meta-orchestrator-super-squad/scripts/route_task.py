#!/usr/bin/env python3
"""Roteador determinístico de tarefas do Primus Meta-Orchestrator.

Dada a descrição de uma tarefa, decide qual squad e qual agente acionar,
combinando:
  1. similaridade léxica entre a tarefa e os papéis/posicionamento dos agentes
     (índice gerado por index_squads.py);
  2. reforço pelo sistema mental (memory_system.py), se disponível.

Quando o melhor score fica abaixo do limiar, sinaliza GAP e propõe a criação
de um novo agente/squad (delegável ao scaffold_squad.py ou ao Maeve Genius
Forge).

Uso:
  python3 route_task.py --task "criar carrossel para instagram" \
      --index output/squad_index.json --top 5
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

STOPWORDS = {
    "a", "o", "e", "de", "do", "da", "das", "dos", "em", "no", "na", "nos", "nas",
    "para", "por", "com", "sem", "que", "um", "uma", "ao", "aos", "se", "ou", "os",
    "as", "the", "and", "of", "to", "in", "for", "with", "on", "como", "preciso",
    "quero", "fazer", "criar", "gerar", "meu", "minha", "sobre", "novo", "nova",
}


def _tokens(text: str) -> list[str]:
    text = (text or "").lower()
    text = re.sub(r"[^0-9a-zà-ÿ\s\-]", " ", text)
    return [t for t in re.split(r"[\s\-]+", text) if len(t) >= 3 and t not in STOPWORDS]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def score_agents(task: str, index: dict[str, Any],
                 concept_weights: dict[str, float]) -> list[dict[str, Any]]:
    qtoks = set(_tokens(task))
    results: list[dict[str, Any]] = []
    for squad in index.get("squads", []):
        squad_kw = set(squad.get("keywords", []))
        for ag in squad.get("agents", []):
            ag_kw = set(_tokens(ag.get("role", "")) + _tokens(ag.get("id", "")))
            # base: overlap com o agente; contexto: overlap com o squad.
            direct = qtoks & ag_kw
            context = (qtoks & squad_kw) - direct
            base = 2.0 * len(direct) + 1.0 * len(context)
            if base <= 0:
                continue
            # reforço do sistema mental: conceitos demandados pesam mais.
            mem_boost = sum(concept_weights.get(t, 0.0) for t in (direct | context))
            score = round(base + 0.25 * mem_boost, 4)
            results.append({
                "score": score,
                "squad": squad["name"],
                "agent": ag["id"],
                "role": ag.get("role", ""),
                "path": squad.get("path", ""),
                "matched": sorted(direct | context),
            })
    results.sort(key=lambda x: (-x["score"], x["squad"], x["agent"]))
    return results


def propose_gap(task: str) -> dict[str, Any]:
    toks = _tokens(task)
    focus = toks[:4] if toks else ["dominio"]
    suggested_name = "-".join(focus[:3]) + "-squad"
    return {
        "gap": True,
        "reason": "Nenhum agente existente atinge o limiar de aderência à tarefa.",
        "suggested_squad_name": suggested_name,
        "suggested_capabilities": focus,
        "next_actions": [
            "Registrar a lacuna: memory_system.py gap --task \"...\"",
            "Criar squad: scaffold_squad.py --name <nome> --agents \"id:papel;...\"",
            "Ou acionar o Maeve Genius Forge via /criar-squad <briefing>.",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Roteia uma tarefa ao melhor agente/squad.")
    ap.add_argument("--task", required=True)
    ap.add_argument("--index", default="output/squad_index.json")
    ap.add_argument("--brain", default="memory/brain.json")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--threshold", type=float, default=2.0,
                    help="Score mínimo do melhor agente para não acionar GAP.")
    args = ap.parse_args()

    index_path = Path(args.index)
    if not index_path.is_file():
        print(json.dumps({"error": f"índice não encontrado: {index_path}. "
                          f"Rode index_squads.py primeiro."}, ensure_ascii=False))
        return 2
    index = load_json(index_path)

    concept_weights: dict[str, float] = {}
    brain_path = Path(args.brain)
    if brain_path.is_file():
        try:
            concept_weights = load_json(brain_path).get("concept_weights", {})
        except Exception:
            concept_weights = {}

    ranked = score_agents(args.task, index, concept_weights)
    top = ranked[: args.top]

    out: dict[str, Any] = {
        "task": args.task,
        "recommendations": top,
        "footer": FOOTER,
    }
    if not top or top[0]["score"] < args.threshold:
        out["gap_analysis"] = propose_gap(args.task)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
