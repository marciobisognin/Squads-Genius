#!/usr/bin/env python3
"""Indexador determinístico de squads do Primus Meta-Orchestrator.

Varre uma pasta com vários squads (cada um com `squad.yaml`), extrai squads,
agentes, papéis e capacidades e gera:

  - output/squad_index.json  -> índice estruturado (máquina)
  - output/SQUAD_WIKI.md     -> wiki de acesso rápido (humano)

Sem dependências externas obrigatórias (PyYAML é usado se disponível; caso
contrário recai para JSON quando o manifesto for JSON válido).

Uso:
  python3 index_squads.py --squads-root ../../ --output-dir output
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover - fallback quando PyYAML não existe
    yaml = None

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

# Stopwords pt-BR/en para extração de palavras-chave de capacidade.
STOPWORDS = {
    "a", "o", "e", "de", "do", "da", "das", "dos", "em", "no", "na", "nos", "nas",
    "para", "por", "com", "sem", "que", "um", "uma", "uns", "umas", "ao", "aos",
    "se", "ou", "os", "as", "the", "and", "of", "to", "in", "for", "with", "on",
    "como", "sua", "seu", "suas", "seus", "ele", "ela", "este", "esta", "esse",
    "essa", "isso", "etc", "sobre", "entre", "cada", "quando", "qual", "quais",
    "pelo", "pela", "mais", "menos", "muito", "ja", "já", "ser", "sao", "são",
    "tem", "ter", "fazer", "feito", "via", "partir", "todo", "toda", "todos",
    "todas", "squad", "agente", "agentes", "from", "this", "that", "are", "is",
}


def _slug_tokens(text: str) -> list[str]:
    text = (text or "").lower()
    text = re.sub(r"[^0-9a-zà-ÿ\s\-]", " ", text)
    tokens = re.split(r"[\s\-]+", text)
    out: list[str] = []
    for tok in tokens:
        tok = tok.strip()
        if len(tok) < 3 or tok in STOPWORDS:
            continue
        out.append(tok)
    return out


def load_manifest(path: Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    data: Any = None
    if yaml is not None:
        try:
            data = yaml.safe_load(text)
        except Exception:
            data = None
    if data is None:
        try:
            data = json.loads(text)
        except Exception:
            return None
    return data if isinstance(data, dict) else None


def _agent_entries(manifest: dict[str, Any]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    agents = manifest.get("agents") or []
    if isinstance(agents, list):
        for a in agents:
            if isinstance(a, dict):
                entries.append({
                    "id": str(a.get("id") or a.get("name") or "?"),
                    "role": str(a.get("role") or a.get("description") or ""),
                    "file": str(a.get("file") or ""),
                })
            elif isinstance(a, str):
                entries.append({"id": a, "role": "", "file": ""})
    return entries


def scan(squads_root: Path, self_name: str | None) -> dict[str, Any]:
    squads: list[dict[str, Any]] = []
    capability_map: dict[str, list[dict[str, str]]] = {}

    for manifest_path in sorted(squads_root.rglob("squad.yaml")):
        squad_dir = manifest_path.parent
        manifest = load_manifest(manifest_path)
        if not manifest:
            continue
        name = str(manifest.get("name") or squad_dir.name)
        if self_name and name == self_name:
            continue
        agents = _agent_entries(manifest)
        positioning = str(manifest.get("positioning") or manifest.get("commercial_name") or "")
        rel = str(squad_dir.relative_to(squads_root)) if squad_dir != squads_root else squad_dir.name

        # Palavras-chave do squad = posicionamento + nome + papéis dos agentes.
        squad_keywords = set(_slug_tokens(positioning) + _slug_tokens(name))
        for ag in agents:
            kws = _slug_tokens(ag["role"]) + _slug_tokens(ag["id"])
            squad_keywords.update(kws)
            for kw in set(kws):
                capability_map.setdefault(kw, []).append({
                    "squad": name,
                    "agent": ag["id"],
                    "role": ag["role"],
                })

        squads.append({
            "name": name,
            "commercial_name": str(manifest.get("commercial_name") or ""),
            "version": str(manifest.get("version") or "não informada"),
            "positioning": positioning,
            "path": rel,
            "agents": agents,
            "agent_count": len(agents),
            "keywords": sorted(squad_keywords),
        })

    squads.sort(key=lambda s: s["name"])
    index = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "squads_root": str(squads_root),
        "squad_count": len(squads),
        "agent_count": sum(s["agent_count"] for s in squads),
        "squads": squads,
        "capability_map": {k: v for k, v in sorted(capability_map.items())},
        "footer": FOOTER,
    }
    return index


def _top_capabilities(index: dict[str, Any], limit: int = 40) -> list[tuple[str, int]]:
    counts = [(kw, len(v)) for kw, v in index["capability_map"].items()]
    counts.sort(key=lambda x: (-x[1], x[0]))
    return counts[:limit]


def render_wiki(index: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Wiki de Squads — Primus Meta-Orchestrator")
    lines.append("")
    lines.append(f"> Gerado automaticamente em {index['generated_at']}.")
    lines.append(f"> {index['squad_count']} squads · {index['agent_count']} agentes mapeados.")
    lines.append("")
    lines.append("Use este mapa para escolher rapidamente **qual squad e qual agente** acionar "
                 "para cada tipo de tarefa. Para roteamento automático use `route_task.py`.")
    lines.append("")

    # Mapa de capacidades de acesso rápido.
    lines.append("## Acesso rápido por capacidade")
    lines.append("")
    lines.append("| Capacidade (palavra-chave) | Squads/agentes disponíveis |")
    lines.append("| --- | --- |")
    for kw, count in _top_capabilities(index):
        refs = index["capability_map"][kw]
        sample = ", ".join(sorted({f"{r['squad']}/{r['agent']}" for r in refs})[:4])
        more = f" (+{count - 4})" if count > 4 else ""
        lines.append(f"| `{kw}` | {sample}{more} |")
    lines.append("")

    # Catálogo de squads.
    lines.append("## Catálogo de squads")
    lines.append("")
    for s in index["squads"]:
        title = s["commercial_name"] or s["name"]
        lines.append(f"### {title} (`{s['name']}`) — v{s['version']}")
        if s["positioning"]:
            lines.append("")
            lines.append(f"{s['positioning']}")
        lines.append("")
        lines.append(f"- Caminho: `{s['path']}`")
        if s["agents"]:
            lines.append("- Agentes:")
            for ag in s["agents"]:
                role = f" — {ag['role']}" if ag["role"] else ""
                lines.append(f"  - `{ag['id']}`{role}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(FOOTER)
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Indexa squads e gera wiki de acesso rápido.")
    ap.add_argument("--squads-root", default="../..",
                    help="Pasta que contém os squads (cada um com squad.yaml).")
    ap.add_argument("--output-dir", default="output")
    ap.add_argument("--self-name", default="primus-meta-orchestrator-super-squad",
                    help="Nome do próprio squad orquestrador, excluído do índice.")
    args = ap.parse_args()

    root = Path(args.squads_root).resolve()
    if not root.is_dir():
        print(json.dumps({"error": f"pasta inexistente: {root}"}, ensure_ascii=False))
        return 2

    index = scan(root, args.self_name)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "squad_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "SQUAD_WIKI.md").write_text(render_wiki(index), encoding="utf-8")

    print(json.dumps({
        "squad_count": index["squad_count"],
        "agent_count": index["agent_count"],
        "capabilities": len(index["capability_map"]),
        "index": str(out / "squad_index.json"),
        "wiki": str(out / "SQUAD_WIKI.md"),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
