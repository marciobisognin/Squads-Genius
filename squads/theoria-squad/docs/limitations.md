# THEORÍA — Limitações Conhecidas (v1.0)

## Não-objetivos da v1.0
- **3D complexo:** fora do escopo além do `ThreeDScene` básico.
- **Trilha musical:** apenas narração TTS + silêncios calculados; trilha é *post-hook* opcional.
- **Multilíngue:** v1.0 é pt-BR nativo.

## Ambiente
- **Scripts determinísticos:** rodam só com stdlib (Python 3.11+) — sem render real.
- **Render real exige binários externos:** Manim Community (pinned), FFmpeg e um
  provedor de TTS pt-BR. Sem eles, os módulos `manim_compiler.py`, `render_config.py`
  e `assemble_av.py` **emitem o plano/código determinístico** (auditável), mas **não
  executam** o render — o vídeo final é produzido no ambiente com os binários.
- **Sandbox HEFESTO:** a codegen custom assume Docker disponível para isolamento (RNF5).
  Sem Docker, mantenha HEFESTO desligado e use apenas o catálogo vetado.

## Reprodutibilidade
- **Sem TTS:** output idêntico bit-a-bit (frames) dado Manim pinado + DSL + seed.
- **Com TTS:** perceptualmente idêntico — a síntese de voz pode variar por provedor;
  por isso a reconciliação de duração (S5↔S9) é determinística sobre as durações medidas.

## Custos
- Render full 1080p é caro: o QA usa **preview em baixa qualidade** e só promove a
  full após convergência. Guardrails de custo por estágio e circuit breaker no
  self-healing (RNF4) limitam loops.

## Métricas são alvos, não garantias
Os KPIs (≥70% QA na 1ª tentativa, ≥85% self-healing, etc.) são **metas de calibração**
da v1.0 e dependem de domínio, complexidade e do provedor de TTS.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
