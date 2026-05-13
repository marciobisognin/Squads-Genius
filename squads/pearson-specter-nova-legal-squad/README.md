# pearson-specter-nova-legal-squad

**Nome técnico:** `pearson-specter-nova-legal-squad`
**Slug no repositório:** `pearson-specter-nova-legal-squad`
**Versão:** `1.0.0`
**Número na seleção original:** 14

## Visão geral

Squad legal inteligente para orquestrar pipeline adversarial de argumentação e estratégia jurídica usando LLMs especializados em direito brasileiro e common law.

## Para que serve

Organizar análise jurídica/estratégica inspirada em uma firma de alta performance, com agentes para triagem, argumentação, auditoria e estruturação de peças ou pareceres.

## Estrutura operacional

- **Agentes:** 6
- **Tasks:** 7
- **Workflows:** 1
- **Scripts:** 0
- **Arquivos totais publicados:** 20

## Agentes

- `agents/donna.md` — title: Analista de Jurimetria e Legal Ops
- `agents/harvey.md` — title: Especialista em M&A e Litígio Estratégico
- `agents/jessica.md` — title: Especialista em Governança, Antitruste e Relações Governamentais
- `agents/legal-orchestrator.md` — title: Orquestrador do Pipeline Jurídico
- `agents/louis.md` — title: Especialista Tributário e Financeiro
- `agents/mike.md` — title: Pesquisador Constitucional e Penal

## Tasks principais

- `tasks/compile-case-report.md` — task: compileCaseReport()
- `tasks/craft-strategy.md` — task: craftStrategy()
- `tasks/deep-research.md` — responsavel_type: Agente
- `tasks/define-case.md` — responsavel: "Legal Orchestrator
- `tasks/financial-audit.md` — task: financialAudit()
- `tasks/intake-oracle.md` — responsavel_type: Agente
- `tasks/macro-alignment.md` — task: macroAlignment()

## Workflows

- `workflows/litigation-pipeline-loop.yaml`

## Como usar

1. Abra o arquivo `squad.yaml` para identificar nome, versão, agentes, tasks e workflows.
2. Leia os arquivos em `agents/` para entender os papéis especializados.
3. Execute as tasks em `tasks/` conforme o fluxo indicado em `workflows/`.
4. Quando houver scripts em `scripts/`, use-os como automações auxiliares; revise dependências antes de executar.
5. Registre saídas, decisões e evidências nos diretórios de documentação ou geração previstos pelo próprio squad.

## Arquivos de referência

- `README.md`
- `squad.yaml`
- `config/coding-standards.md`
- `config/source-tree.md`
- `config/tech-stack.md`

## Propriedade intelectual e licença

- Licença padrão adotada para novos squads de Marcio: MIT.
- Criado por: Marcio Bisognin.
- Instagram: [@marciobisognin](https://instagram.com/marciobisognin).
- Observação: squads legados foram publicados preservando sua estrutura original; quando não houver arquivo de licença interno, considere a política do repositório e a documentação de cada pasta.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
