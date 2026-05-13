# ISO 42001 AIMS Implementation Squad

**Nome técnico:** `iso-42001-aims-implementation`
**Slug no repositório:** `iso-42001-aims-implementation`
**Versão:** `5.0.0`
**Número na seleção original:** 1

## Visão geral

ISO 42001 AIMS Implementation Squad — Protocol v5.0

## Para que serve

Implementar, diagnosticar e preparar evidências de um Sistema de Gestão de Inteligência Artificial alinhado à ISO/IEC 42001, com pipeline de governança, riscos, impacto, controles e prontidão de auditoria.

## Estrutura operacional

- **Agentes:** 8
- **Tasks:** 8
- **Workflows:** 3
- **Scripts:** 2
- **Arquivos totais publicados:** 66

## Agentes

- `agents/ai-inventory-mapper.md` — Mapeador de Inventário de IA — `ai-inventory-mapper`
- `agents/aiia-executor.md` — Executor de AIIA — `aiia-executor`
- `agents/audit-evidence-collector.md` — Coletor de Evidências de Auditoria — `audit-evidence-collector`
- `agents/certification-readiness-checker.md` — Verificador de Prontidão de Certificação — `certification-readiness-checker`
- `agents/gap-analyzer.md` — Analisador de Lacunas ISO 42001 — `gap-analyzer`
- `agents/policy-template-writer.md` — Redator de Políticas e Templates — `policy-template-writer`
- `agents/risk-register-builder.md` — Construtor de Registro de Riscos — `risk-register-builder`
- `agents/soa-architect.md` — Arquiteto de SoA — `soa-architect`

## Tasks principais

- `tasks/01_map_ai_inventory.yaml` — title: "Mapear inventário de IA
- `tasks/02_analyze_iso42001_gaps.yaml` — title: "Analisar gaps ISO/IEC 42001
- `tasks/03_execute_aiia.yaml` — title: "Executar AIIA
- `tasks/04_build_risk_register.yaml` — title: "Construir registro de riscos
- `tasks/05_architect_soa.yaml` — title: "Arquitetar SoA
- `tasks/06_write_policy_templates.yaml` — title: "Escrever políticas e templates
- `tasks/07_collect_audit_evidence.yaml` — title: "Coletar evidências auditáveis
- `tasks/08_check_certification_readiness.yaml` — title: "Checar prontidão de certificação

## Workflows

- `workflows/audit_readiness_4_6_weeks.yaml`
- `workflows/full_implementation_9_12_months.yaml`
- `workflows/gap_analysis_2_4_weeks.yaml`

## Scripts e automação

- `scripts/build_visual_summary_pdf.py`
- `scripts/generate_aims_pack.py`

## Como usar

1. Abra o arquivo `squad.yaml` para identificar nome, versão, agentes, tasks e workflows.
2. Leia os arquivos em `agents/` para entender os papéis especializados.
3. Execute as tasks em `tasks/` conforme o fluxo indicado em `workflows/`.
4. Quando houver scripts em `scripts/`, use-os como automações auxiliares; revise dependências antes de executar.
5. Registre saídas, decisões e evidências nos diretórios de documentação ou geração previstos pelo próprio squad.

## Arquivos de referência

- `README.md`
- `TUTORIAL_DIDATICO.md`
- `squad.yaml`
- `docs/RESUMO_VISUAL_DETALHADO.md`
- `docs/estrutura_solicitada_mapeamento.md`
- `docs/pipeline_16_fases.md`

## Propriedade intelectual e licença

- Licença padrão adotada para novos squads de Marcio: MIT.
- Criado por: Marcio Bisognin.
- Instagram: [@marciobisognin](https://instagram.com/marciobisognin).
- Observação: squads legados foram publicados preservando sua estrutura original; quando não houver arquivo de licença interno, considere a política do repositório e a documentação de cada pasta.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
