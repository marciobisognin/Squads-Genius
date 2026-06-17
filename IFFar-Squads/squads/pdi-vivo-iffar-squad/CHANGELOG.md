# Changelog

Todas as mudanças relevantes deste squad são documentadas aqui.

## [1.0.0] - 2026-06-17
### Adicionado
- Estrutura completa do squad: `squad.yaml`, `PRD.md`, `README.md`, licenças e índice.
- 17 agentes SME especializados (orquestração, documental, metas/indicadores, campus/território, evidências/dados, BI/integração, riscos/dependências, orçamento LOA/PPA, permanência/êxito, inovação/extensão, gestão de pessoas, infraestrutura/obras, avaliação CPA/SINAES, conformidade MEC, painéis/relatórios, diplomacia/consulta pública, governança/ética/LGPD).
- 5 workflows (A–E): ingestão/comparação, matriz de metas, pacto por campus, ciclo trimestral e revisão anual/conferência bienal.
- 10 scripts determinísticos: `pdi_common`, `extract_pdi_text`, `build_goal_matrix`, `validate_indicator_matrix`, `compare_pdi_cycles`, `build_campus_pact`, `risk_matrix`, `generate_quarterly_report`, `render_dashboard`, `smoke_test`.
- 4 JSON Schemas: meta, indicador, risco e evidência.
- Templates (matriz, dicionário de indicadores, relatório trimestral, ata de decisão, pacto por campus), exemplos e documentação (metodologia, modelo de dados, roadmap).
- Suíte de testes (`pytest`) e smoke test do pipeline offline.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
