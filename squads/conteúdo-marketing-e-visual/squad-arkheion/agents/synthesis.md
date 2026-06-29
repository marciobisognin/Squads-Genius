# SÝNTHESIS — A Composição

> Étimo: σύνθεσις (*sýnthesis*), "composição". · Tier: **Python, não-LLM** · Guilda da Renderização · Implementação: `scripts/synthesis_plan.py`

## Missão
Montar o master a partir das N CENA-10 aprovadas: concatenação com corte seco + glitch de 1–2 frames, passe global de grão/scanline para continuidade temporal, mix de áudio com silêncios estratégicos, card de encerramento e exportação master 2160² + entrega 1080².

## Entrada — N× `Cena10` (aprovadas) + `AudioSpec` + `encerramento`
## Saída — `DossieMaster` (JSON) + arquivos `.mp4`
```json
{ "path_master_2160": "outputs/master_2160.mp4",
  "path_entrega_1080": "outputs/entrega_1080.mp4",
  "duracao_total_s": 60.0, "cenas": [ ... ],
  "encerramento": "escuro", "langfuse_trace_id": "..." }
```

## Responsabilidades (PRD §8.4)
- `concat` das cenas em ordem, com corte seco + transição glitch (1–2 frames).
- **Passe global** de grão/scanline sobre a timeline montada (continuidade do grão entre cortes).
- Áudio: bed de drone contínuo + SFX por cue + silêncios (AudioSpec) + locução opcional (TTS).
- Anexar card de encerramento (escuro/branco) com fade lento.
- Exportar master **2160²** e entrega **1080²**, 24fps, H.264/HEVC.

## Regras
- Determinístico: mesma entrada → mesmo master. Sem FFmpeg disponível, emite o **plano de montagem** + comandos (auditável).

## Comandos
- `*help` · `*assemble` · `*export <2160|1080>` · `*exit`

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
