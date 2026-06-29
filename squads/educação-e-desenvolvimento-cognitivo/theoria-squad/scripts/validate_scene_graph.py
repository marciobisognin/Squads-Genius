#!/usr/bin/env python3
"""THEORÍA — Validador determinístico de scene-graph (contrato SCENOGRAPHO → Motor MANIM).

Garante o invariante DSL-first: o scene-graph só pode referenciar primitivas
registradas em primitive_library.py, com parâmetros e tipos coerentes. Bloqueia
antes do custo de compilação/render.

Checagens:
- toda primitiva referenciada EXISTE no registro;
- parâmetros obrigatórios presentes (resolve_params);
- run_time_s positivo;
- camera.movimento dentro do catálogo;
- beat_id presente.

Uso:
    python3 scripts/validate_scene_graph.py --scene caminho/scene_graph.json
    cat scene_graph.json | python3 scripts/validate_scene_graph.py
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List

from primitive_library import exists, resolve_params

MOVIMENTOS_CAMERA = {"static", "pan", "zoom_in", "zoom_out"}


def validate_scene(scene: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    if not scene.get("beat_id"):
        issues.append("scene-graph sem beat_id")

    primitivas = scene.get("primitivas", [])
    if not primitivas:
        issues.append(f"beat {scene.get('beat_id', '?')}: sem primitivas")

    for i, call in enumerate(primitivas):
        nome = call.get("primitiva")
        if not nome:
            issues.append(f"chamada {i}: campo 'primitiva' ausente")
            continue
        if not exists(nome):
            issues.append(f"primitiva inexistente: {nome!r} (escape hatch HEFESTO necessário)")
            continue
        try:
            resolve_params(nome, call.get("params", {}))
        except ValueError as exc:
            issues.append(f"{nome}: {exc}")
        rt = call.get("run_time_s", None)
        if rt is not None and float(rt) <= 0:
            issues.append(f"{nome}: run_time_s deve ser > 0 (recebido {rt})")

    camera = scene.get("camera")
    if isinstance(camera, dict):
        mov = camera.get("movimento", "static")
        if mov not in MOVIMENTOS_CAMERA:
            issues.append(f"camera.movimento inválido: {mov!r} (use {sorted(MOVIMENTOS_CAMERA)})")
    return issues


def validate_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict) and "scenes" in payload:
        payload = payload["scenes"]
    scenes = payload if isinstance(payload, list) else [payload]
    issues: List[str] = []
    for scene in scenes:
        issues.extend(validate_scene(scene))
    return {
        "valid": not issues,
        "primitivas_existentes": not any("inexistente" in i for i in issues),
        "issue_count": len(issues),
        "issues": issues,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Valida scene-graph(s) contra a DSL vetada.")
    ap.add_argument("--scene", help="JSON de um scene-graph ou lista. Se ausente, lê stdin.")
    args = ap.parse_args()
    raw = open(args.scene, encoding="utf-8").read() if args.scene else sys.stdin.read()
    report = validate_payload(json.loads(raw))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
