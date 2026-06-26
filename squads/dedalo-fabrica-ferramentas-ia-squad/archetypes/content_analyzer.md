# Arquétipo A — Analisador de Conteúdo (`content_analyzer`)

> Família A · Inteligência de mercado.

## Dor canônica
Volume de conteúdo (vídeos, posts, reviews) que ninguém consegue ler/estruturar para decidir.

## Dados necessários
- Transcrições, legendas, comentários, métricas de engajamento.

## Agentes sugeridos
- Extrator (yt-dlp/whisper), classificador (LLM-JSON), agregador de métricas (Python).

## Integrações
- APIs de mídia, planilhas, dashboard local.

## Esqueleto de MVP
- Pipeline vídeo→transcrição→temas→relatório com timestamps e confiança.

## Riscos
- Fontes protegidas por login; alucinação de tema sem evidência.

## Gancho de monetização
- Relatórios de tendência; curadoria de conteúdo como serviço.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
