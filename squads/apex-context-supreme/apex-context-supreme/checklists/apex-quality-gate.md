# Quality Gate: apex-context-supreme

Este checklist deve ser validado pela **Vigil** (Validadora) antes da entrega final dos artefatos de contexto.

## Validação de Formato

- [ ] Todos os arquivos `.md` gerados possuem syntax Markdown válida.
- [ ] Arquivos `blueprint.yaml` e `inventory.json` em `.apex-context/` estão bem formados.
- [ ] O manifesto `squad.yaml` está atualizado na versão corrente.

## Validação Semântica

- [ ] As regras geradas pelo Spark são acionáveis (contêm verbos imperativos).
- [ ] O Trim removeu redundâncias entre arquivos de plataformas diferentes (cross-platform check).
- [ ] O inventário técnico lista corretamente as tecnologias detectadas no projeto.

## Validação de Infraestrutura AIOS

- [ ] Slash commands (`*iniciar-pipeline`, `*status-apex`) devidamente descritos nos agentes.
- [ ] Todos os agentes possuem o frontmatter YAML obrigatório.
- [ ] Todas as tasks possuem contratos de Entrada/Saída definidos.

## Critérios de ACEITAÇÃO (Blockers)

| Critério | Descrição | Status |
|----------|-----------|--------|
| Sem Erros de Syntax | Block se houver Markdown quebrado | [ ] |
| Sem Regras Órfãs | Block se Spark gerou regras sem blueprint | [ ] |
| Cross-platform OK | Block se `CLAUDE.md` e `GEMINI.md` são idênticos | [ ] |
