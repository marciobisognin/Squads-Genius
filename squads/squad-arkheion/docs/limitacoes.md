# Limitações conhecidas — ARKHEION

- **Render real exige stack pesado.** A renderização frame-a-frame (Playwright) e a grade
  (FFmpeg) precisam estar instalados. Sem eles, os scripts degradam para **plano +
  comandos** (determinístico e auditável), mas não produzem o `.mp4`.
- **API de vídeo plugável.** A geração de footage depende de um provider externo
  (Kling/Runway/Veo/Luma). A variância entre providers é neutralizada pela grade canônica,
  mas a disponibilidade/custo do provider está fora do controle do squad.
- **Custo de créditos de vídeo.** Mitigado pelo Gate 2 (aprova roteiro antes de gerar) e
  pela regeneração por-cena (não por-vídeo).
- **Tamanhos suportados.** 3 a 9 CENA-10 (30s a 90s, múltiplos de 10s). Tamanhos fora
  dessa faixa são rejeitados por `canon.resolver_duracao()` — a CENA-10 é atômica.
- **Fontes não redistribuídas.** As famílias recomendadas (OFL) precisam ser instaladas
  localmente (`@font-face`); seus arquivos não acompanham o repositório.
- **Áudio.** Bed/SFX dependem de biblioteca licenciada/loops versionados; TTS é opcional
  e, por default, ausente (o silêncio é parte da estética).
- **Pydantic opcional.** Sem Pydantic v2, os contratos usam dataclasses com validação
  equivalente — cobertura de validação ligeiramente mais simples, mas funcional.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
