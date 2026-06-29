# MOTOR MANIM — Compilador Determinístico (Núcleo Auditável)

> Tier: **Determinístico (sem LLM)** · Implementação: `scripts/manim_compiler.py`

## Missão
Ser o **coração reproduzível** de THEORÍA: traduzir o **scene-graph JSON** em **código
Manim renderizável**, usando exclusivamente a **biblioteca de primitivas vetadas**
(`primitive_library.py`). O mesmo scene-graph **sempre** produz o mesmo código — base
do RNF1 (reprodutibilidade). Nenhum LLM participa desta etapa.

## Entradas — `SceneGraph[]` (validado) + registro de primitivas
## Saída — arquivo `.py` de cena Manim + relatório de compilação
```json
{ "out": "outputs/theoria_scene.py", "beats": 4, "class": "EulerIdentity" }
```

## Pipeline determinístico
1. Valida o scene-graph (`validate_scene_graph.py`): toda primitiva existe, params ok.
2. Para cada beat, resolve params (defaults da primitiva) e renderiza o `template`.
3. Emite a classe `Scene` com os beats em ordem, pausas e movimentos de câmera.
4. Falha **explicitamente** (sem improviso) se houver primitiva inexistente → HEFESTO.

## Responsabilidades
- Garantir saída idêntica para entrada idêntica (auditável, versionável).
- Recusar primitivas fora do registro (encaminha ticket ao escape hatch HEFESTO).

## Não-responsabilidades
- Não inventa código novo (isso é HEFESTO, sob sandbox) nem renderiza (ÁRGOS/Manim CLI).

## Comandos (CLI)
- `python3 scripts/manim_compiler.py --scenes scenes.json --class-name <Nome> --out <arquivo.py>`

## Critérios de qualidade
- 100% determinístico: `hash(código)` estável para o mesmo input.
- Zero código fora do catálogo de primitivas.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
