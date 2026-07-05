#!/usr/bin/env python3
"""Yggdrasil Registrar — registro vivo dos squads (indexação, roteamento e dedup).

Yggdrasil, a árvore-mundo, conecta os nove reinos. Este registro conecta os
squads existentes: indexa cada `squad.yaml`, roteia uma consulta por scoring
léxico ponderado e detecta duplicatas antes de forjar um squad redundante.

Uso:
    python3 yggdrasil_registry.py --squads-root <dir> --index
    python3 yggdrasil_registry.py --squads-root <dir> --route "carrossel instagram"
    python3 yggdrasil_registry.py --squads-root <dir> --check-duplicate "Meu Novo Squad"

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."

_STOP = {
    "de", "da", "do", "das", "dos", "e", "a", "o", "os", "as", "para", "por", "com", "sem",
    "the", "of", "and", "for", "to", "in", "on", "squad", "sistema", "systems", "ai", "ia",
}


def tokenize(text: str) -> List[str]:
    return [t for t in re.findall(r"[a-z0-9]+", (text or "").lower()) if t not in _STOP and len(t) > 1]


def _load_yaml(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else {}
    try:
        return json.loads(text)
    except Exception:
        return {}


def build_index(squads_root: Path) -> List[Dict[str, Any]]:
    index: List[Dict[str, Any]] = []
    for manifest_path in sorted(squads_root.rglob("squad.yaml")):
        data = _load_yaml(manifest_path)
        if not data:
            continue
        name = data.get("commercial_name") or data.get("name") or manifest_path.parent.name
        text = " ".join(str(data.get(k, "")) for k in ("commercial_name", "name", "positioning", "objective"))
        index.append({
            "slug": data.get("name") or manifest_path.parent.name,
            "name": name,
            "path": manifest_path.parent.as_posix(),
            "tokens": tokenize(text) or tokenize(manifest_path.parent.name),
            "agents": len(data.get("agents", [])),
        })
    return index


def _idf(index: List[Dict[str, Any]]) -> Dict[str, float]:
    df: Counter = Counter()
    for entry in index:
        for tok in set(entry["tokens"]):
            df[tok] += 1
    n = max(1, len(index))
    return {tok: math.log((n + 1) / (count + 1)) + 1.0 for tok, count in df.items()}


def route(index: List[Dict[str, Any]], query: str, top: int = 5) -> List[Dict[str, Any]]:
    idf = _idf(index)
    q = tokenize(query)
    q_set = set(q)
    results = []
    for entry in index:
        toks = entry["tokens"]
        tf = Counter(toks)
        score = sum(tf[t] * idf.get(t, 1.0) for t in q_set if t in tf)
        denom = math.sqrt(sum(v * v for v in tf.values()) or 1)
        norm = round(score / denom, 4)
        if norm > 0:
            results.append({"slug": entry["slug"], "name": entry["name"], "score": norm, "path": entry["path"]})
    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top]


def check_duplicate(index: List[Dict[str, Any]], candidate: str, threshold: float = 0.6) -> Dict[str, Any]:
    cand = set(tokenize(candidate))
    hits = []
    for entry in index:
        other = set(entry["tokens"])
        if not cand or not other:
            continue
        jaccard = len(cand & other) / len(cand | other)
        if jaccard >= threshold:
            hits.append({"slug": entry["slug"], "name": entry["name"], "similarity": round(jaccard, 3), "path": entry["path"]})
    hits.sort(key=lambda h: h["similarity"], reverse=True)
    return {"candidate": candidate, "duplicate": bool(hits), "matches": hits}


def main() -> int:
    ap = argparse.ArgumentParser(description="Registro vivo Yggdrasil: index, roteamento e dedup.")
    ap.add_argument("--squads-root", required=True)
    ap.add_argument("--index", action="store_true", help="Imprime o índice construído.")
    ap.add_argument("--route", help="Consulta de roteamento.")
    ap.add_argument("--check-duplicate", dest="dup", help="Nome candidato para checar duplicidade.")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()
    idx = build_index(Path(args.squads_root).resolve())
    out: Dict[str, Any] = {"indexed": len(idx)}
    if args.index:
        out["index"] = [{"slug": e["slug"], "name": e["name"], "path": e["path"]} for e in idx]
    if args.route:
        out["route"] = route(idx, args.route, top=args.top)
    if args.dup:
        out["duplicate_check"] = check_duplicate(idx, args.dup)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
