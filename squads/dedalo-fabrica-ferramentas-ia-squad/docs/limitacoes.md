# Limitações Conhecidas — DÉDALO

> Separando observado, hipótese e risco (regra do construtor).

## Dependências externas (degradação graciosa)
- **Pydantic ausente:** schemas degradam para dataclasses (stdlib). A forma é preservada;
  a validação estrita de tipos fica reduzida.
- **Langfuse ausente:** `observability/langfuse_hooks.py` usa um sink local determinístico;
  nenhuma credencial é lida ou exigida.
- **Ferramentas de extração** (yt-dlp, ffprobe, whisper, OCR) não acompanham o squad: o
  `extract_sources.py` entrega o ESQUELETO e marca fontes inacessíveis.

## Fronteiras de produto
- **Construção (F3):** HÉPHAISTOS só age após HITL#2; protótipo é o MENOR artefato que prova
  a dor #1 — não um SaaS completo.
- **Setores regulados:** saúde/jurídico/financeiro entregam apoio, nunca decisão final
  (humano no loop obrigatório via NÓMOS).
- **Fontes protegidas por login:** marcadas como inacessíveis; conteúdo não verificado não é usado.

## Riscos residuais
- Otimismo sistêmico (sycophancy) no scoring — mitigado por notas auditadas + cálculo em Python
  + cenário pessimista em domínio complexo.
- Automação sobre processo ruim — mitigado pelo gate de diagnóstico de TÉCHNE.

## Ambiente (publicação)
- `git push` de **tags** pode retornar 403 (credenciais com escopo de branch); release formal
  fica para a UI do GitHub. PR/merge na `main` seguem o playbook do repositório quando autorizado.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
