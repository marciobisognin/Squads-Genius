#!/usr/bin/env python3
"""THEORÍA — Testes de determinismo do núcleo auditável.

Garante o invariante RNF1: o mesmo input sempre produz o mesmo output. Roda com
pytest OU standalone (`python3 tests/test_determinism.py`) — sem dependências
externas além da stdlib.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import chronos_timing  # noqa: E402
import manim_compiler  # noqa: E402
import primitive_library  # noqa: E402
import qa_frame_checks  # noqa: E402
import validate_scene_graph  # noqa: E402

EX = ROOT / "examples"


def _load(name):
    return json.loads((EX / name).read_text(encoding="utf-8"))


def test_primitives_registered():
    prims = primitive_library.list_primitives()
    assert "ComplexPlaneSpiral" in prims
    assert len(prims) >= 10  # MVP de ~10 primitivas (PRD Fase 0)


def test_chronos_is_deterministic():
    beats = _load("beats_euler.json")
    a = chronos_timing.build_timeline(beats["beats"], tuple(beats["banda_duracao_s"]))
    b = chronos_timing.build_timeline(beats["beats"], tuple(beats["banda_duracao_s"]))
    assert a == b
    assert a["n_beats"] == 4
    assert a["duracao_total_s"] > 0


def test_scene_graph_valid():
    scenes = _load("scene_graph_euler.json")
    report = validate_scene_graph.validate_payload(scenes)
    assert report["valid"], report["issues"]
    assert report["primitivas_existentes"]


def test_compiler_is_deterministic():
    scenes = _load("scene_graph_euler.json")["scenes"]
    code_a = manim_compiler.compile_scenes(scenes, "EulerIdentity")
    code_b = manim_compiler.compile_scenes(scenes, "EulerIdentity")
    assert code_a == code_b
    assert "class EulerIdentity(Scene)" in code_a
    assert "ComplexPlane" in code_a


def test_compiler_rejects_unknown_primitive():
    bad = [{"beat_id": "x", "primitivas": [{"primitiva": "NaoExiste", "params": {}, "run_time_s": 1.0}]}]
    try:
        manim_compiler.compile_scenes(bad, "Bad")
    except ValueError as exc:
        assert "inválido" in str(exc) or "inexistente" in str(exc)
    else:
        raise AssertionError("deveria recusar primitiva inexistente")


def test_qa_flags_contrast_and_sync():
    frames = _load("qa_frames_euler.json")
    report = qa_frame_checks.run_qa(frames)
    assert not report["aprovado"]
    tipos = {d["tipo"] for d in report["defeitos"]}
    assert "contraste" in tipos
    assert "sync" in tipos


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}")
    print(f"\n{len(fns) - failed}/{len(fns)} testes passaram")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_run_all())

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
