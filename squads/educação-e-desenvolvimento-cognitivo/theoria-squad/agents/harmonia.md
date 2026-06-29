# HARMONIA — Assembly Final (Mux + 1080p + Formato)

> Étimo: ἁρμονία (*harmonía*), "ajuste, junção em proporção".
> Tier: **Determinístico (sem LLM)** · Implementação: `scripts/assemble_av.py`

## Missão
**Juntar em proporção** o que as guildas produziram: faz o **mux** determinístico do
vídeo (Manim) com o áudio (EChÓ) via FFmpeg, alinha pelos *timestamps* da linha do
tempo mestra, normaliza o áudio, aplica **formato/aspecto e 1080p**, e exporta o
contêiner final. Gera também o **manifesto de artefatos** para auditoria.

## Entradas — vídeo Manim + áudio EChÓ + `Timeline` + `formato`
## Saída — plano de mux + manifesto
```json
{ "mux": { "formato": "9:16", "resolucao": [1080, 1920],
           "comando_ffmpeg": "ffmpeg -y -i ... -crf 18 -r 60 ...", "saida": "outputs/final.mp4" },
  "manifesto": { "job_id": "...", "duracao_total_s": 230.4, "manifest_hash": "..." } }
```

## Render config (PRD §9.3)
| Formato | Resolução 1080p | FPS |
|---|---|---|
| 16:9 | 1920 × 1080 | 60 |
| 9:16 | 1080 × 1920 | 60 |
| 1:1 | 1080 × 1080 | 60 |

Encode H.264 / `yuv420p` / CRF configurável — reproduzível.

## Responsabilidades
- Alinhar áudio↔vídeo pelos timestamps; normalizar nível de áudio.
- Aplicar pad/scale para o aspecto alvo sem distorcer.
- Emitir manifesto com hashes (timeline, mux) para auditoria/RNF2.

## Não-responsabilidades
- Não corrige defeitos visuais (ÁRGOS) nem reajusta tempo (CHRONOS).

## Comandos (CLI)
- `python3 scripts/assemble_av.py --timeline timeline.json --formato 9:16 --out outputs/final.mp4`

## Critérios de qualidade
- Saída sempre 1080p no formato escolhido; manifesto completo e hasheado.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
