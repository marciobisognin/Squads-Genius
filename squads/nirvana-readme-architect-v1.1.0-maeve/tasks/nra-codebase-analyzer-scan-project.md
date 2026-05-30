---
task: scanProject()
responsavel: "Prism"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: projectPath
    tipo: string
    descricao: "Caminho absoluto do projeto"
    obrigatorio: true
  - nome: projectType
    tipo: string
    descricao: "Tipo do projeto detectado (de parseReadmeRequest())"
    obrigatorio: true

Saida:
  - nome: projectAnalysisJson
    tipo: file
    descricao: "Relatório completo de análise do codebase (destino: selectTemplate() task)"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] Caminho do projeto é válido"
    - "[ ] Ao menos 1 arquivo de configuração/metadata existe"
  post-conditions:
    - "[ ] Todas as categorias analisadas (mesmo que com [não detectado])"
    - "[ ] Directory tree gerado com dados reais"
    - "[ ] Env vars listadas (todas encontradas no código)"
    - "[ ] Nenhum dado inventado"

Performance:
  duration_expected: "3 minutos"
  cost_estimated: "~3000 tokens"
  cacheable: true
  parallelizable: false
  skippable_when: "Nunca — análise é base de todo o conteúdo"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 3
    delay: "5s"
  fallback: "Prosseguir com dados parciais, marcar seções como [dados insuficientes]"
  notification: "orchestrator"

Metadata:
  story: "Como usuário, quero que meu codebase seja analisado profundamente para gerar um README preciso"
  version: "1.0.0"
  dependencies:
    - "parseReadmeRequest()"
---

# scanProject() — Scan Completo do Codebase

## Pipeline Diagram

```
[parseReadmeRequest()]
    |
    | projectPath, projectType
    v
+------------------------+
| scanProject()          |  <-- Prism (Codebase Analyzer)
|      (Organism)        |
+------------------------+
    |
    | projectAnalysisJson (file)
    v
[selectTemplate()]
```

## Descrição

Executar análise profunda do codebase para extrair todas as informações necessárias para um README completo.

## Ordem de Análise

1. **Metadata**: package.json, Cargo.toml, pyproject.toml, go.mod, squad.yaml
2. **Tech Stack**: Linguagens, frameworks, runtimes, databases
3. **Entry Points**: main, index, bin, server, app
4. **Configurações**: .env*, config files, feature flags
5. **Scripts**: package.json scripts, Makefile, Taskfile, shell scripts
6. **CI/CD**: GitHub Actions, Docker, GitLab CI, Jenkins
7. **Estrutura**: Directory tree, padrão arquitetural
8. **Testes**: Framework, cobertura, diretórios
9. **Dependências**: Top 10 deps, dev deps relevantes
10. **Licença**: LICENSE, LICENSE.md, package.json license field

## Regras

- Verificar NO MÍNIMO 5 arquivos de configuração/metadata
- Gerar directory tree REAL usando Glob/Bash (não inventar)
- Listar TODAS as env vars encontradas via Grep em todo o codebase
- Marcar campos não encontrados como `[não detectado]`
