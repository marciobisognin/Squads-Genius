---
task: parseReadmeRequest()
responsavel: "Quill"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: projectPath
    tipo: string
    descricao: "Caminho do projeto alvo"
    obrigatorio: true
  - nome: projectType
    tipo: string
    descricao: "Tipo do projeto (opcional, auto-detect se omitido)"
    obrigatorio: false
  - nome: scope
    tipo: string
    descricao: "Escopo: full ou quick (default: full)"
    obrigatorio: false

Saida:
  - nome: parsedRequest
    tipo: file
    descricao: "Request parseado com projeto, tipo, escopo e caminho de saída (destino: scanProject() task)"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] Caminho do projeto é válido e acessível"
    - "[ ] Diretório contém ao menos 1 arquivo de código ou configuração"
  post-conditions:
    - "[ ] Tipo de projeto identificado (Library, CLI, Web App, API, Monorepo, Mobile, Squad AIOS)"
    - "[ ] Escopo definido (full/quick)"
    - "[ ] Caminho de output definido"

Performance:
  duration_expected: "1 minuto"
  cost_estimated: "~500 tokens"
  cacheable: false
  parallelizable: false
  skippable_when: "Nunca — é o ponto de entrada do pipeline"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 3
    delay: "5s"
  fallback: "Solicitar ao usuário tipo e escopo manualmente"
  notification: "orchestrator"

Metadata:
  story: "Como usuário, quero que o tipo de projeto seja detectado automaticamente para gerar o README adequado"
  version: "1.0.0"
  dependencies: []
---

# parseReadmeRequest() — Parse da Solicitação de README

## Pipeline Diagram

```
[user request]
    |
    | projectPath, projectType?, scope?
    v
+------------------------+
| parseReadmeRequest()   |  <-- Quill (Orchestrator)
|      (Organism)        |
+------------------------+
    |
    | parsedRequest (file)
    v
[scanProject()]
```

## Descrição

Analisar a solicitação do usuário para extrair: projeto alvo, tipo de projeto (detectar automaticamente se não fornecido), escopo desejado e caminho de saída do README.

## Detecção Automática de Tipo

1. Verificar `package.json` → campo `bin` presente? CLI Tool
2. Verificar `package.json` → campo `main`/`module`/`exports`? Library
3. Verificar presença de framework web (next.config, vite.config, nuxt.config)? Web App
4. Verificar rotas de API (routes/, controllers/, openapi.yaml)? API
5. Verificar workspaces (pnpm-workspace.yaml, lerna.json, turbo.json)? Monorepo
6. Verificar mobile (expo, react-native, android/, ios/)? Mobile
7. Verificar `squad.yaml`? Squad AIOS
8. Fallback: Library
