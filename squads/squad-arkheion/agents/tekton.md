# TÉKTŌN — O Artífice

> Étimo: τέκτων (*téktōn*), "artífice/construtor". · Tier: **Python, não-LLM** · Guilda da Renderização · Implementação: `scripts/hud_plan.py`, `scripts/grade.py`

## Missão
Renderizar cada CENA-10 de forma determinística: o HUD frame-a-frame (Trilho A) e o footage canônico (Trilho B), compondo A sobre B em um `.mp4` de 10s exatos. A identidade é **code-enforced** — o LLM nunca desenha.

## Entrada — `CardInterface` + `FootageSpec` (por cena)
## Saída — `Cena10` (JSON) + arquivo `.mp4`
```json
{ "idx": 1, "path_mp4": "outputs/cena01.mp4", "duracao_s": 10.0,
  "checksum": "sha256:...", "kanon_aprovado": true }
```

## Pipeline (PRD §8)
1. **Trilho A (HUD):** template HTML/CSS com moldura fixa (cantos "L", régua, contador, rodapé) + `@font-face` das fontes permitidas; variáveis CSS = tokens do Cânone. `hud_plan.py` calcula 240 frames @24fps: fade do preto, entrada do título (0,4–0,8s), glitch RGB (1–2 frames), digitação a 25 cps, cursor piscando (0,6–0,9s), e dataviz no beat de prova. Captura por **Playwright** → PNG com alfa.
2. **Trilho B (footage):** envia `FootageSpec` à API text-to-video (provider plugável), 1:1, 10s; aplica `grade.py` (cadeia FFmpeg canônica + scanlines).
3. **Composição:** overlay alfa de A sobre B, corte em 10s, `checksum`, submissão ao KÁNŌN.

## Regras
- Tudo parametrizado pelo Cânone; nenhum número mágico. Falha de API → escala ao TURING.
- Degradação graciosa: sem Playwright/FFmpeg, emite o **plano** + `render_hash` (determinístico/auditável).

## Comandos
- `*help` · `*render <cena_idx>` · `*hud <cena_idx>` · `*grade <footage>` · `*exit`

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
