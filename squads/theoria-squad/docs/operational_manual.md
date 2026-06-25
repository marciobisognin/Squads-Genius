# THEORÍA — Manual Operacional

## Pré-requisitos
- **Scripts determinísticos:** Python 3.11+ (stdlib apenas — rodam em qualquer lugar).
- **Render real (opcional):** Manim Community (pinned), FFmpeg, e — para TTS — um
  provedor pt-BR (ElevenLabs / Azure Neural / Coqui). Render isolado em Docker.

## Fluxo determinístico (sem render real)
O núcleo auditável roda sem Manim/FFmpeg instalados — útil para validar a lógica,
o timing e a compilação antes de gastar GPU.

```bash
cd squads/theoria-squad

# 1) Inspecionar o catálogo de primitivas
python3 scripts/primitive_library.py

# 2) Timing determinístico (linha do tempo mestra)
python3 scripts/chronos_timing.py --beats examples/beats_euler.json

# 3) Reconciliar com durações reais do TTS (loop S5<->S9)
python3 scripts/chronos_timing.py --beats examples/beats_euler.json \
    --reconcile examples/tts_durations_euler.json

# 4) Validar o scene-graph contra a DSL vetada
python3 scripts/validate_scene_graph.py --scene examples/scene_graph_euler.json

# 5) Compilar scene-graph -> código Manim (Motor MANIM)
python3 scripts/manim_compiler.py --scenes examples/scene_graph_euler.json \
    --class-name EulerIdentity --out outputs/euler_scene.py

# 6) Gerar comandos de render (formato/1080p)
python3 scripts/render_config.py --formato 9:16 \
    --scene-file outputs/euler_scene.py --class EulerIdentity

# 7) QA por frame (ÁRGOS) + roteamento de self-healing
python3 scripts/qa_frame_checks.py --frames examples/qa_frames_euler.json

# 8) Plano de mux + manifesto (HARMONIA)
python3 scripts/chronos_timing.py --beats examples/beats_euler.json > /tmp/tl.json
python3 scripts/assemble_av.py --timeline /tmp/tl.json --formato 9:16 \
    --out outputs/euler_final.mp4
```

## Render real (com Manim/FFmpeg)
1. Gere o `euler_scene.py` (passo 5).
2. Rode o comando `render_full` emitido pelo `render_config.py` (passo 6).
3. Sintetize a narração via EChÓ (provedor TTS) → `narracao.wav`.
4. Rode o `comando_ffmpeg` emitido pelo `assemble_av.py` (passo 8) para o mux 1080p.

## Gates humanos
- **Gate A (S1):** confirme domínio, profundidade e banda antes de gastar tokens/render.
- **Gate B (S7, opcional):** preview do storyboard (default ligado para alta complexidade).
- **Gate C (S12):** AISTHÉSIS apresenta vídeo + rubrica; aprove / reprove / aprove com ressalvas.

## Testes
```bash
python3 tests/test_determinism.py     # standalone, sem dependências
# ou: python3 -m pytest -q            # se pytest estiver instalado
```

## Validação do squad
```bash
python3 scripts/validate_squad.py --root .
# ou, a partir da raiz do repositório:
python3 squads/maeve-genius-forge-squad/scripts/validate_squad.py --root squads/theoria-squad
```

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
