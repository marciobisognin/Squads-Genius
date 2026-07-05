# Changelog — Bifröst Forge Engine

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
versionamento [SemVer](https://semver.org/lang/pt-BR/).

## [1.1.0] — 2026-07-05
### Adicionado
- **Pilar Empresas** — `asgard_company_forge.py` + `company_briefing.py`: forja de
  organograma (direção → chefias → funcionários como agentes com contrato), governança e
  gates, determinística e auditável (Saga Ledger próprio).
- **Pilar Mentes** — `mind_clone_library.py`: Biblioteca de Mentes que evolui o Mímir DNA
  para perfis de voz **injetáveis** em agentes/funcionários, com salvaguardas de PI
  (sem n-grama verbatim; só descritores abstratos).
- Agentes `frigg-company-architect` e `saga-mind-keeper`; tasks `15_forge_company_org` e
  `16_curate_mind_clones`; workflow `company_forge_pipeline.yaml`.
- Docs `company_forge.md` e `mind_clone_library.md`; exemplos de empresa e de voz; testes
  `test_company_and_minds.py`.
- Injeção de mente na forja de empresa via `--mind`.

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
