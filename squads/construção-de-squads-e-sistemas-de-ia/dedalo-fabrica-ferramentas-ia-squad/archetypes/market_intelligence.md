# Arquétipo A — Inteligência de Mercado (`market_intel`)

> Família A · Inteligência de mercado. Cada arquétipo é um molde reutilizável de ferramenta.

## Dor canônica
Decisões comerciais por feeling; concorrência e preço mudam sem que a empresa perceba a tempo.

## Dados necessários
- Catálogo/preços de concorrentes, conteúdo publicado, ofertas, sazonalidade.

## Agentes sugeridos (na ferramenta-cliente)
- Coletor (scraping/API), normalizador (Python), analisador (LLM-JSON), alerta (regras Python).

## Integrações
- Fontes públicas, planilhas, e-mail/Slack para alertas, banco local (SQLite).

## Esqueleto de MVP
- Monitor de concorrentes + radar de preço/oferta + relatório vivo semanal (HTML/SQLite).

## Riscos
- Termos de uso de fontes; dados desatualizados; ruído sem priorização.

## Gancho de monetização
- Assinatura de "radar de mercado" por nicho; relatórios premium.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
