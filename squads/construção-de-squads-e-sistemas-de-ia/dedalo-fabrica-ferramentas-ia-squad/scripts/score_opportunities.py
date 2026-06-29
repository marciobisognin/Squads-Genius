#!/usr/bin/env python3
"""CLI determinística de priorização de oportunidades do DÉDALO.

Lê um opportunity_map (JSON/YAML) com premissas 1-5 e imprime o ranking calculado
em Python puro. O LLM nunca calcula — esta é a fronteira determinística do squad.

Uso:
    python3 scripts/score_opportunities.py --input examples/opportunity_map.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Torna o pacote engine/ importável independentemente do diretório de execução.
ENGINE_DIR = Path(__file__).resolve().parent.parent / "engine"
sys.path.insert(0, str(ENGINE_DIR))

from scoring import OppScoringAssumptions, rank_opportunities  # noqa: E402

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


def _load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"} and yaml is not None:
        return yaml.safe_load(text)
    return json.loads(text)


def _to_pairs(data: dict) -> list[tuple[str, OppScoringAssumptions]]:
    pairs: list[tuple[str, OppScoringAssumptions]] = []
    for opp in data.get("opportunities", []):
        a = opp["scoring_assumptions"]
        pairs.append(
            (
                opp["name"],
                OppScoringAssumptions(
                    impact_value_1to5=int(a["impact_value_1to5"]),
                    effort_1to5=int(a["effort_1to5"]),
                    risk_1to5=int(a["risk_1to5"]),
                    data_availability_1to5=int(a["data_availability_1to5"]),
                    repetition_1to5=int(a["repetition_1to5"]),
                ),
            )
        )
    return pairs


def main() -> int:
    ap = argparse.ArgumentParser(description="Prioriza oportunidades (motor Python determinístico).")
    ap.add_argument("--input", required=True, help="opportunity_map em JSON ou YAML.")
    args = ap.parse_args()
    data = _load(Path(args.input))
    ranked = rank_opportunities(_to_pairs(data))
    out = [
        {"rank": i + 1, "name": s.name, "score": s.score, "below_threshold": s.below_threshold}
        for i, s in enumerate(ranked)
    ]
    print(json.dumps({"ranking": out}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
