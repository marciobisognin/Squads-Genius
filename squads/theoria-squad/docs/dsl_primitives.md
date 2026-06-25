# THEORÍA — DSL de Cena (Biblioteca de Primitivas Vetadas)

A "voz visual" do padrão 3b1b é um **vocabulário finito de movimentos**. THEORÍA o
codifica como **primitivas parametrizadas, testadas e versionadas** em
`scripts/primitive_library.py`. Cada primitiva declara: parâmetros (com defaults),
`run_time` default, um **template de código Manim** determinístico e um **golden frame**
de regressão.

## Contrato
> SCENOGRAPHO **só** referencia primitivas existentes. Se precisar de algo novo, abre
> ticket para **HEFESTO** (escape hatch sob sandbox). A primitiva aprovada é
> **promovida** a este registro. Isso mantém a saída **determinística e reprodutível**.

## Catálogo MVP (v1.0)
| Primitiva | Uso |
|---|---|
| `TitleReveal` | abertura/legenda com fade + underline |
| `NumberLineReveal` | introdução de reta numérica |
| `NumberPlaneReveal` | introdução de plano cartesiano |
| `FunctionGraphReveal` | desenho progressivo de curva |
| `TransformEquation` | morfismo entre fórmulas (LaTeX) |
| `VectorTransform` | transformação linear de vetor |
| `MatrixMultiplication` | operação matricial passo a passo |
| `GeometricProof` | construção geométrica encadeada |
| `HighlightFocus` | foco semântico (amarelo) sobre objeto |
| `CameraMove` | pan/zoom intencional |
| `ComplexPlaneReveal` | introdução do plano complexo |
| `ComplexPlaneSpiral` | rotação no plano complexo (ex.: e^{iπ}) |

## Anatomia de uma primitiva
```python
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
}
```

## Ciclo de promoção (HEFESTO)
1. SCENOGRAPHO abre `PrimitiveTicket`.
2. HEFESTO forja a menor primitiva possível (lint → sandbox Docker → render-validate-heal).
3. Gera `golden_frame` de regressão.
4. Aprovada → **promovida** ao registro; vira determinística para sempre.

## Como inspecionar
```bash
python3 scripts/primitive_library.py        # lista o catálogo + DSL_VERSION
python3 scripts/validate_scene_graph.py --scene examples/scene_graph_euler.json
```

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
