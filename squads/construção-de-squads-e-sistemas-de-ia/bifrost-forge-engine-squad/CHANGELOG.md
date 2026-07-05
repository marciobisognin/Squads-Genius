# Changelog — Bifröst Forge Engine

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [1.0.0] — 2026-07-05
### Adicionado
- Engine determinístico completo: `bifrost_forge.py` + `bifrost_orchestrator.py`.
- **Saga Ledger** — trilha de auditoria JSONL com hash SHA256 encadeado (`saga_ledger.py`).
- **Heimdall** — validador com matriz de rastreabilidade, verificação de determinismo e
  rubrica pontuada por gate (`heimdall_validate.py`).
- **Yggdrasil** — registro vivo com roteamento léxico e detecção de duplicatas
  (`yggdrasil_registry.py`).
- **Mímir DNA Distiller** — perfil de estilo em 5 camadas com salvaguardas de PI (`mimir_dna.py`).
- 11 agentes temáticos, 14 tasks, 5 workflows (incl. `campaign_dispatch` multi-squad).
- Geradores determinísticos: `saga_briefing`, `runic_architect`, `norn_workflows`,
  `valkyrie_agents`, `eitri_design`, `brokkr_scripts`, `package_saga`.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
