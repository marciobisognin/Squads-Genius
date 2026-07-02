#!/usr/bin/env python3
"""Registry & Discovery do AETHER OS (aether.squad/v1).

Varre roots de squads, interpreta squad.yaml (adaptador squad-yaml) e converte
para o manifesto canônico interno com estado de confiança — sem executar
nenhum script dos squads descobertos. PRD AETHER OS v1.2, Seções 10 e 11.

Parser YAML mínimo embutido (stdlib-first): cobre o subconjunto usado pelos
manifestos (mapeamentos, listas, escalares); se PyYAML existir, é usado.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ENGINE_ID = "aether-registry-indexer@1.0.0"

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), default=str)


def _parse_yaml(text: str) -> dict:
    if yaml is not None:
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    # Fallback mínimo: só chaves de topo escalares e listas simples de mapas
    # com chave 'file' — suficiente para indexar id/nome/versão/componentes.
    result: dict = {}
    current_list_key = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 0 and ":" in stripped:
            key, _, value = stripped.partition(":")
            key, value = key.strip(), value.strip()
            if value in ("", "|", ">", "|-", ">-"):
                result[key] = []
                current_list_key = key
            else:
                result[key] = value.strip("'\"")
                current_list_key = None
        elif stripped.startswith("- ") and current_list_key:
            item = stripped[2:].strip()
            if ":" in item:
                k, _, v = item.partition(":")
                result[current_list_key].append({k.strip(): v.strip().strip("'\"")})
            else:
                result[current_list_key].append(item.strip("'\""))
        elif indent >= 2 and ":" in stripped and current_list_key:
            lst = result.get(current_list_key)
            if isinstance(lst, list) and lst and isinstance(lst[-1], dict):
                k, _, v = stripped.partition(":")
                lst[-1][k.strip()] = v.strip().strip("'\"")
    return result


def _component_refs(manifest: dict, key: str) -> list[dict]:
    items = manifest.get(key) or []
    refs = []
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and item.get("file"):
                refs.append({"id": item.get("id", Path(item["file"]).stem),
                             "path": item["file"]})
    return refs


def index_squad(squad_dir: Path) -> dict:
    """Converte um diretório de squad em manifesto canônico aether.squad/v1."""
    manifest_path = squad_dir / "squad.yaml"
    text = manifest_path.read_text(encoding="utf-8", errors="ignore")
    sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    entry = {
        "schema_version": "aether.squad/v1",
        "id": squad_dir.name,
        "name": squad_dir.name,
        "version": "0.0.0",
        "source": {"type": "local", "uri": str(squad_dir), "commit_sha": None,
                   "trusted": False},
        "adapter": {"type": "squad-yaml", "version": 1},
        "capabilities": [],
        "components": {"agents": [], "tasks": [], "workflows": []},
        "trust_state": "discovered",
        "issues": [],
        "integrity": {"manifest_sha256": sha256,
                      "indexed_at": datetime.now(timezone.utc).isoformat()},
    }
    try:
        manifest = _parse_yaml(text)
    except Exception as exc:
        entry["trust_state"] = "quarantined"
        entry["issues"].append(f"parse_error: {exc}")
        return entry
    entry["trust_state"] = "parsed"
    entry["name"] = str(manifest.get("name", squad_dir.name))
    entry["id"] = str(manifest.get("code", squad_dir.name))
    entry["version"] = str(manifest.get("version", "0.0.0"))
    domains = manifest.get("domains") or []
    if isinstance(domains, list):
        entry["capabilities"] = [str(d) for d in domains if isinstance(d, str)]
    for key in ("agents", "tasks", "workflows"):
        entry["components"][key] = _component_refs(manifest, key)
    # Validação estrutural: referências devem existir (nunca executa scripts).
    missing = [ref["path"] for key in ("agents", "tasks", "workflows")
               for ref in entry["components"][key]
               if not (squad_dir / ref["path"]).is_file()]
    if missing:
        entry["trust_state"] = "quarantined"
        entry["issues"] = [f"missing_reference: {m}" for m in missing]
    else:
        entry["trust_state"] = "validated"
    return entry


def discover(root: Path) -> dict:
    squads = []
    for manifest in sorted(root.rglob("squad.yaml")):
        if "__pycache__" in manifest.parts:
            continue
        squads.append(index_squad(manifest.parent))
    return {
        "schema_version": "aether.registry/v1",
        "root": str(root),
        "squads": squads,
        "counts": {
            "total": len(squads),
            "validated": sum(1 for s in squads if s["trust_state"] == "validated"),
            "quarantined": sum(1 for s in squads if s["trust_state"] == "quarantined"),
        },
        "indexed_by": ENGINE_ID,
    }


def search(registry: dict, query: str) -> list[dict]:
    q = query.lower()
    hits = []
    for squad in registry.get("squads", []):
        haystack = " ".join([squad["id"], squad["name"],
                             " ".join(squad.get("capabilities", []))]).lower()
        if q in haystack:
            hits.append({"id": squad["id"], "name": squad["name"],
                         "version": squad["version"],
                         "trust_state": squad["trust_state"]})
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="Registry/Discovery AETHER")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("discover")
    d.add_argument("--root", required=True)
    d.add_argument("--output", help="arquivo de saída do registry.json")
    s = sub.add_parser("search")
    s.add_argument("--registry", required=True)
    s.add_argument("--query", required=True)
    args = ap.parse_args()
    if args.cmd == "discover":
        registry = discover(Path(args.root).resolve())
        out = canonical(registry)
        if args.output:
            Path(args.output).write_text(out, encoding="utf-8")
        print(out if not args.output else
              canonical(registry["counts"]))
        return 0
    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    print(canonical(search(registry, args.query)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
