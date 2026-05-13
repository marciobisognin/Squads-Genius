# Criar Video Francisca Manim

## Objetivo
Criar, ao final do carrossel, um vídeo vertical em português brasileiro com voz Francisca, visual lúdico premium para Instagram e texto altamente visível.

## Entrada
- `roteiro.md`
- `legenda.txt`
- `manifest.json`
- imagens PNG dos slides em `slides/`
- solicitação original do usuário, quando disponível

## Processo
1. Escrever plano audiovisual em `video/plan.md`.
2. Escrever narração em `video/narracao.txt` em pt-BR.
3. Tentar usar Manim para gerar animação vertical 1080x1920.
4. Se Manim falhar no Termux, usar fallback Pillow + ffmpeg sem interromper a entrega.
5. Gerar voz com `edge-tts` usando `pt-BR-FranciscaNeural`.
6. Muxar vídeo e áudio com ffmpeg.
7. Exportar `video/final_francisca.mp4`.
8. Exportar `video/preview.png` para conferência visual.

## Saídas esperadas
- `video/plan.md`
- `video/narracao.txt`
- `video/video_base.mp4`
- `video/narracao_francisca.mp3` quando TTS estiver disponível
- `video/final_francisca.mp4`
- `video/preview.png`
- `video/video_manifest.json`

## Critérios de qualidade
- Conteúdo integralmente em pt-BR.
- Voz Francisca quando o TTS estiver disponível.
- Texto grande e visível em tela de celular.
- Design lúdico, premium e coerente com o carrossel.
- Nenhum bloqueio caso Manim não funcione no Termux: usar fallback.
