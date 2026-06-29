#!/usr/bin/env python3
"""THEORÍA — Biblioteca de primitivas Manim vetadas (DSL de cena).

A "voz visual" do padrão 3b1b é um vocabulário finito de movimentos. THEORÍA o
codifica como primitivas parametrizadas, testadas e versionadas. Cada primitiva
declara: parâmetros aceitos (com defaults), run_time default e um TEMPLATE de
código Manim determinístico.

SCENOGRAPHO só pode referenciar primitivas registradas aqui. Se precisar de algo
novo, abre ticket para HEFESTO (escape hatch sob sandbox), e a primitiva aprovada
é PROMOVIDA para este registro. Isso mantém a saída determinística e reprodutível.

Sem dependências externas — apenas stdlib. Compatível com o Motor MANIM
(manim_compiler.py), que consome este registro.
"""
from __future__ import annotations

from typing import Any, Dict, List

# Versão da DSL — fixar junto do manim_version_lock garante reprodutibilidade.
DSL_VERSION = "1.0.0"


# Cada entrada:
#   params: nome -> default (None = obrigatório)
#   run_time: default em segundos
#   template: código Manim (str.format com os params + run_time)
#   golden: nome do golden frame de regressão (referência de teste)
PRIMITIVES: Dict[str, Dict[str, Any]] = {
    "TitleReveal": {
        "params": {"texto": None, "subtitulo": ""},
        "run_time": 1.2,
        "template": (
            "titulo = Title({texto!r})\n"
            "self.play(Write(titulo), run_time={run_time})\n"
        ),
        "golden": "title_reveal.png",
    },
    "NumberLineReveal": {
        "params": {"x_min": -5, "x_max": 5, "step": 1},
        "run_time": 1.0,
        "template": (
            "reta = NumberLine(x_range=[{x_min}, {x_max}, {step}])\n"
            "self.play(Create(reta), run_time={run_time})\n"
        ),
        "golden": "number_line.png",
    },
    "NumberPlaneReveal": {
        "params": {"x_min": -6, "x_max": 6, "y_min": -4, "y_max": 4},
        "run_time": 1.2,
        "template": (
            "plano = NumberPlane(x_range=[{x_min}, {x_max}], y_range=[{y_min}, {y_max}])\n"
            "self.play(Create(plano), run_time={run_time})\n"
        ),
        "golden": "number_plane.png",
    },
    "FunctionGraphReveal": {
        "params": {"expr": "x**2", "x_min": -3, "x_max": 3, "cor": "BLUE"},
        "run_time": 1.5,
        "template": (
            "eixos = Axes(x_range=[{x_min}, {x_max}], y_range=[-1, 9])\n"
            "grafico = eixos.plot(lambda x: {expr}, color={cor})\n"
            "self.play(Create(eixos), run_time=0.8)\n"
            "self.play(Create(grafico), run_time={run_time})\n"
        ),
        "golden": "function_graph.png",
    },
    "TransformEquation": {
        "params": {"de": "a^2 + b^2", "para": "c^2"},
        "run_time": 1.4,
        "template": (
            "eq_de = MathTex({de!r})\n"
            "eq_para = MathTex({para!r})\n"
            "self.play(Write(eq_de), run_time=0.8)\n"
            "self.play(TransformMatchingTex(eq_de, eq_para), run_time={run_time})\n"
        ),
        "golden": "transform_equation.png",
    },
    "VectorTransform": {
        "params": {"vetor": [1, 1], "matriz": [[2, 0], [0, 1]]},
        "run_time": 1.6,
        "template": (
            "plano = NumberPlane()\n"
            "vetor = Vector({vetor})\n"
            "self.add(plano)\n"
            "self.play(GrowArrow(vetor), run_time=0.6)\n"
            "self.play(ApplyMatrix({matriz}, vetor), run_time={run_time})\n"
        ),
        "golden": "vector_transform.png",
    },
    "MatrixMultiplication": {
        "params": {"A": [[1, 2], [3, 4]], "B": [[0, 1], [1, 0]]},
        "run_time": 1.8,
        "template": (
            "ma = Matrix({A})\n"
            "mb = Matrix({B})\n"
            "grupo = VGroup(ma, mb).arrange(RIGHT, buff=0.6)\n"
            "self.play(Write(grupo), run_time={run_time})\n"
        ),
        "golden": "matrix_mult.png",
    },
    "GeometricProof": {
        "params": {"passos": []},
        "run_time": 2.0,
        "template": (
            "figura = VGroup()\n"
            "# passos geométricos encadeados: {passos}\n"
            "self.play(Create(figura), run_time={run_time})\n"
        ),
        "golden": "geometric_proof.png",
    },
    "HighlightFocus": {
        "params": {"ponto": [0, 0], "cor": "YELLOW"},
        "run_time": 0.8,
        "template": (
            "foco = Dot(point=[{ponto[0]}, {ponto[1]}, 0], color={cor})\n"
            "self.play(FadeIn(foco, scale=1.5), Flash(foco), run_time={run_time})\n"
        ),
        "golden": "highlight_focus.png",
    },
    "CameraMove": {
        "params": {"alvo": [0, 0], "zoom": 1.0},
        "run_time": 1.2,
        "template": (
            "self.play(self.camera.frame.animate.move_to([{alvo[0]}, {alvo[1]}, 0])"
            ".set(width=config.frame_width / {zoom}), run_time={run_time})\n"
        ),
        "golden": "camera_move.png",
    },
    "ComplexPlaneReveal": {
        "params": {"x_min": -3, "x_max": 3, "y_min": -3, "y_max": 3},
        "run_time": 1.2,
        "template": (
            "plano = ComplexPlane(x_range=[{x_min}, {x_max}], y_range=[{y_min}, {y_max}])\n"
            "self.play(Create(plano), run_time={run_time})\n"
        ),
        "golden": "complex_plane.png",
    },
    "ComplexPlaneSpiral": {
        "params": {"theta": 3.14159, "raio": 1.0, "cor": "YELLOW"},
        "run_time": 2.0,
        "template": (
            "plano = ComplexPlane()\n"
            "vetor = Vector([{raio}, 0])\n"
            "self.add(plano, vetor)\n"
            "self.play(Rotate(vetor, angle={theta}, about_point=ORIGIN), run_time={run_time})\n"
        ),
        "golden": "complex_spiral.png",
    },
}


def list_primitives() -> List[str]:
    """Nomes das primitivas registradas (catálogo fechado da v1.0)."""
    return sorted(PRIMITIVES.keys())


def exists(nome: str) -> bool:
    return nome in PRIMITIVES


def default_run_time(nome: str) -> float:
    return float(PRIMITIVES[nome]["run_time"])


def resolve_params(nome: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Aplica defaults da primitiva sobre os params informados.

    Levanta KeyError com mensagem clara se a primitiva não existir e ValueError
    se faltar parâmetro obrigatório (default None).
    """
    if nome not in PRIMITIVES:
        raise KeyError(f"primitiva inexistente: {nome!r} (abra ticket para HEFESTO)")
    schema = PRIMITIVES[nome]["params"]
    resolved: Dict[str, Any] = {}
    for key, default in schema.items():
        if key in params:
            resolved[key] = params[key]
        elif default is not None:
            resolved[key] = default
        else:
            raise ValueError(f"primitiva {nome!r}: parâmetro obrigatório ausente: {key!r}")
    return resolved


if __name__ == "__main__":
    import json

    print(json.dumps({
        "dsl_version": DSL_VERSION,
        "total": len(PRIMITIVES),
        "primitivas": list_primitives(),
    }, ensure_ascii=False, indent=2))

# Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
