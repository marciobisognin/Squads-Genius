# EChÓ — Síntese de Voz pt-BR (Orquestra TTS)

> Étimo: Ἠχώ (*Ēchṓ*), a ninfa cuja voz repete e devolve o som.
> Tier: **Determinístico (orquestra TTS plugável, sem LLM de conteúdo)** · Modelo: sem LLM

## Missão
Dar **voz** à narração: sintetizar o texto pt-BR de cada beat e — crucialmente —
**devolver as durações reais** para reconciliar com CHRONOS (loop S5↔S9). EChÓ é uma
**interface abstrata**: o provedor (ElevenLabs / Azure Neural / Coqui) é plugável; a
orquestração (segmentação, retries, normalização) é determinística.

## Entradas — `Beat[]` (com `narracao`) + `TTSConfig`
```json
{ "provider": "azure_neural", "voz": "pt-BR-AntonioNeural", "rate": "0%", "seed": 42 }
```
## Saída — `VoiceAssets` + durações reais
```json
{ "assets": [ { "beat_id": "b1", "wav": "media/audio/b1.wav", "duracao_real_s": 6.2 } ],
  "duracoes_para_chronos": { "b1": 6.2, "b2": 12.4 } }
```

## Responsabilidades
- Sintetizar por beat com voz/seed fixos (perceptualmente reproduzível).
- Medir a duração real de cada áudio e devolvê-la a CHRONOS.
- *Fallback* para legendas/cartelas se TTS off ou provedor indisponível (RF6).

## Não-responsabilidades
- Não escreve narração (RAPSODO) nem decide pausas (CHRONOS).
- Não mistura áudio+vídeo (HARMONIA).

## Comandos (orquestração)
- `*help` · `*synthesize` · `*durations` · `*exit`

## Critérios de qualidade
- Durações reais entregues para 100% dos beats.
- Provedor trocável sem mudar o contrato de saída.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
