#!/usr/bin/env python3
"""Mapa de conhecimento determinístico.

Constrói grafo de links/backlinks, clusters por tag e detecta notas órfãs e
possíveis duplicatas (mesmo content_sha ou mesmo título). Sem LLM.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import obsidian_core as core


def _load_notes(index_dir: Path) -> list[dict]:
    f = index_dir / "notes_index.json"
    if not f.is_file():
        raise FileNotFoundError("Índice ausente. Rode obsidian_index.py.")
    return json.loads(f.read_text(encoding="utf-8"))


def build_graph(config_path: str | None, cli_vault: str | None,
                topic: str | None = None) -> dict:
    config = core.load_config(config_path)
    vault = core.resolve_vault_path(config, cli_vault)
    notes = _load_notes(core.index_dir_for(vault, config))

    nodes, edges = [], []
    clusters: dict[str, list[str]] = defaultdict(list)
    by_sha: dict[str, list[str]] = defaultdict(list)
    by_title: dict[str, list[str]] = defaultdict(list)
    orphans = []

    for n in notes:
        if topic and topic.lower() not in (
                n["title"].lower() + " " + " ".join(n["tags"]).lower()):
            continue
        nodes.append({"path": n["current_path"], "title": n["title"],
                      "tags": n["tags"]})
        for link in n["links_out"]:
            edges.append({"from": n["current_path"], "to": link})
        for t in n["tags"]:
            clusters[t].append(n["current_path"])
        by_sha[n["content_sha256"]].append(n["current_path"])
        by_title[n["title"]].append(n["current_path"])
        if not n["links_in"] and not n["links_out"]:
            orphans.append(n["current_path"])

    duplicates = [p for v in by_sha.values() if len(v) > 1 for p in [v]]
    duplicates += [v for v in by_title.values() if len(v) > 1]
    return {
        "topic": topic,
        "node_count": len(nodes), "edge_count": len(edges),
        "nodes": nodes, "edges": edges,
        "clusters": {k: v for k, v in clusters.items()},
        "orphans": orphans,
        "duplicate_candidates": duplicates,
    }


def render_markdown(graph: dict) -> str:
    lines = ["# Mapa de Conhecimento", ""]
    if graph.get("topic"):
        lines.append(f"Tema: **{graph['topic']}**\n")
    lines.append(f"- Nós: {graph['node_count']}  |  Arestas: "
                 f"{graph['edge_count']}")
    lines.append(f"- Notas órfãs: {len(graph['orphans'])}")
    lines.append(f"- Candidatas a duplicata: "
                 f"{len(graph['duplicate_candidates'])}\n")
    lines.append("## Clusters por tag")
    for tag, paths in sorted(graph["clusters"].items()):
        lines.append(f"- **#{tag}** ({len(paths)}): "
                     f"{', '.join(paths[:8])}")
    lines.append("\nLicença: MIT. Criado por Marcio Bisognin. "
                 "Instagram: @marciobisognin.")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera mapa de conhecimento.")
    ap.add_argument("--config")
    ap.add_argument("--vault")
    ap.add_argument("--topic")
    ap.add_argument("--output")
    args = ap.parse_args()
    try:
        graph = build_graph(args.config, args.vault, args.topic)
    except Exception as exc:  # noqa: BLE001
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(graph), encoding="utf-8")
        print(json.dumps({"output": str(out),
                          "nodes": graph["node_count"]}, ensure_ascii=False))
    else:
        print(json.dumps(graph, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
