#!/usr/bin/env python3
"""THEORÍA — Motor MANIM: compilador determinístico scene-graph JSON → código Manim.

Núcleo auditável/reproduzível (sem LLM). Recebe uma lista de scene-graphs (um por
beat) e emite um arquivo .py de cena Manim renderizável, montado exclusivamente a
partir das primitivas vetadas (primitive_library.py).

O mesmo scene-graph JSON SEMPRE produz o mesmo código — base do RNF1
(reprodutibilidade). Antes de compilar, valida via validate_scene_graph.

Uso:
    python3 scripts/manim_compiler.py --scenes scenes.json --out outputs/theoria_scene.py
    python3 scripts/manim_compiler.py --scenes scenes.json --class-name EulerIdentity
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List

from primitive_library import DSL_VERSION, PRIMITIVES, resolve_params
from validate_scene_graph import validate_payload

HEADER = '''"""Cena gerada deterministicamente pelo Motor MANIM (THEORÍA).
DSL_VERSION={dsl} | beats={n} | NÃO EDITAR À MÃO — regenere a partir do scene-graph.
"""
from manim import *


class {cls}(Scene):
    def construct(self):
'''

INDENT = " " * 8


def _emit_call(nome: str, params: Dict[str, Any], run_time: float) -> str:
    """Renderiza o template da primitiva com params resolvidos."""
    spec = PRIMITIVES[nome]
    resolved = resolve_params(nome, params)
    body = spec["template"].format(run_time=run_time, **resolved)
    return "".join(INDENT + line + "\n" for line in body.rstrip("\n").split("\n"))


def compile_scenes(scenes: List[Dict[str, Any]], class_name: str = "TheoriaScene") -> str:
    """Gera o código-fonte Manim a partir dos scene-graphs."""
    report = validate_payload(scenes)
    if not report["valid"]:
        raise ValueError("scene-graph inválido: " + "; ".join(report["issues"]))

    out = [HEADER.format(dsl=DSL_VERSION, n=len(scenes), cls=class_name)]
    for scene in scenes:
        out.append(f"{INDENT}# --- beat {scene.get('beat_id')} ---\n")
        for call in scene.get("primitivas", []):
            nome = call["primitiva"]
            run_time = float(call.get("run_time_s", PRIMITIVES[nome]["run_time"]))
            out.append(_emit_call(nome, call.get("params", {}), run_time))
        camera = scene.get("camera") or {}
        if camera.get("movimento", "static") != "static":
            alvo = camera.get("alvo", [0, 0])
            zoom = 1.6 if camera.get("movimento") == "zoom_in" else 0.7 if camera.get("movimento") == "zoom_out" else 1.0
            rt = float(camera.get("run_time_s", 1.2))
            out.append(
                f"{INDENT}self.play(self.camera.frame.animate.move_to("
                f"[{alvo[0]}, {alvo[1]}, 0]).set(width=config.frame_width / {zoom}), run_time={rt})\n"
            )
        out.append(f"{INDENT}self.wait(0.2)\n")
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Motor MANIM — compila scene-graph em código.")
    ap.add_argument("--scenes", help="JSON com lista de scene-graphs. Se ausente, lê stdin.")
    ap.add_argument("--class-name", default="TheoriaScene")
    ap.add_argument("--out", help="Arquivo .py de saída. Se ausente, imprime no stdout.")
    args = ap.parse_args()

    raw = open(args.scenes, encoding="utf-8").read() if args.scenes else sys.stdin.read()
    scenes = json.loads(raw)
    if isinstance(scenes, dict):
        scenes = scenes.get("scenes", [scenes])
    try:
        code = compile_scenes(scenes, args.class_name)
    except ValueError as exc:
        print(f"Erro de compilação: {exc}", file=sys.stderr)
        return 2

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(code)
        print(json.dumps({"out": args.out, "beats": len(scenes), "class": args.class_name}, ensure_ascii=False))
    else:
        print(code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
