# NOTICE

ARKHEION — squad multiagente para produção de dossiês visuais em vídeo com estética
analógica investigativa ("arquivo confidencial"), criado a partir do PRD v1.0
fornecido pelo usuário (Marcio Bisognin).

## Propriedade intelectual e originalidade
- ARKHEION codifica uma **identidade visual original** (paleta, geometria, tipografia,
  timing, grade) como constantes em `arkheion/canon.py`. Não copia marca, logotipo,
  prompt, áudio, roteiro ou qualquer ativo proprietário de terceiros.
- A "estética arquivo confidencial" referida no PRD é uma **direção de arte** (sensação
  investigativa), reimplementada de forma autoral em código — não é a cópia de nenhuma
  identidade alheia. Logos de parceiros no card de encerramento, quando usados, são
  ativos fornecidos pelo próprio usuário no Gate 1; apenas a *lógica* de composição é
  do squad.
- As fontes recomendadas (Oxanium, Chakra Petch, Tektur, Orbitron, Share Tech Mono,
  Space Mono, IBM Plex Mono) são famílias de licença aberta (OFL); seus arquivos não
  são redistribuídos aqui.

## Software de terceiros
- LangGraph, Pydantic, Playwright, FFmpeg e MoviePy são software de terceiros, usados
  conforme suas respectivas licenças. APIs de text-to-video (Kling/Runway/Veo/Luma) e
  de TTS são integrações plugáveis; nenhuma credencial, token ou chave é incluída.

## Determinismo e auditoria
- Os scripts determinísticos e o núcleo (`arkheion/`) rodam com a stdlib do Python 3.11+;
  dependências pesadas (Pydantic/Playwright/FFmpeg) são opcionais com fallback.
- Cada `Cena10.checksum` é linkado à sua spec → reconstrução completa do "porquê" de
  cada cena (auditoria TCU-grade).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
