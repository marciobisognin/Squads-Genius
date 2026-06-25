# NOTICE

THEORÍA — squad multiagente para geração cinematográfica de vídeos educacionais em Manim
(padrão estético 3Blue1Brown), criado a partir do PRD v1.0 fornecido pelo usuário.

## Propriedade intelectual e originalidade
- THEORÍA implementa uma **gramática visual** (vocabulário finito de movimentos) **inspirada** no estilo
  educacional consagrado por 3Blue1Brown. Não copia marca, logotipo, código proprietário, áudio, roteiro
  ou qualquer ativo de terceiros.
- As **primitivas da DSL** (`scripts/primitive_library.py`) são reimplementações **originais** sobre
  **Manim Community** (licença MIT). Manim e FFmpeg são software de terceiros, usados conforme suas
  respectivas licenças.
- Provedores de TTS (ElevenLabs / Azure Neural / Coqui) são integrações plugáveis; nenhuma credencial,
  token ou chave é incluída neste repositório.

## Determinismo e auditoria
- Os scripts determinísticos rodam apenas com a stdlib do Python 3.11+.
- Todos os artefatos intermediários são persistíveis para auditoria; o manifesto liga input→output por
  hashes (timeline, mux).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
