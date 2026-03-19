---
task: enriquecerContexto()
responsavel: "Spark"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: contextBlueprint
    tipo: file
    descricao: "blueprint.yaml definindo os arquivos de regras"
    obrigatorio: true
  - nome: techInventory
    tipo: file
    descricao: "inventory.json mapeando a stack tecnológica"
    obrigatorio: true

Saida:
  - nome: rawRuleFiles
    tipo: array
    descricao: "Lista de caminhos para os arquivos de regras (.md) criados/enriquecidos"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] blueprint.yaml lido e válido"
    - "[ ] Acesso de escrita aos locais de regras (raiz, .aiox-core, .codex)"
    - "[ ] Template context-rule.template.md disponível"
  post-conditions:
    - "[ ] Arquivos de regras criados com conteúdo denso (não apenas boilerplate)"
    - "[ ] Todos os subdomínios técnicos do inventory.json estão cobertos em pelo menos uma regra"
    - "[ ] Instruções acionáveis presentes em cada arquivo"

Performance:
  duration_expected: "3-7 minutos"
  cost_estimated: "~3000 tokens (Opus/Flash)"
  cacheable: false
  parallelizable: true
  skippable_when: "Nunca — conteúdo semântico deve ser gerado pelo menos uma vez"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: "5s"
  fallback: "Se a geração de uma regra falhar, mover para a próxima e reportar no log final"
  notification: "apex-orquestrista"

Metadata:
  story: "Como especialista em enriquecimento, preciso converter dados técnicos em instruções semânticas para IAs"
  version: "1.0.0"
  author: "Nirvana Squad Creator (Refined)"
---

# enriquecerContexto()

## Pipeline Diagram
```
┌───────────────┐     ┌───────────────┐     ┌───────────────────────┐
│ blueprint.yaml│────▶│    Spark      │────▶│  Regras Brutas (.md)   │
│ inventory.json│     │ (spark-alquim)│     │  (CLAUDE, GEMINI, etc) │
└───────────────┘     └───────────────┘     └───────────────────────┘
                               │                      │
                               │ Phase 2              │ Alimenta Trim
                               ▼                      ▼
                        ┌───────────┐          ┌──────────────┐
                        │ Context   │          │ Rules        │
                        │ Dense Info│          │ Knowledge    │
                        └───────────┘          └──────────────┘
```

## Descrição
A task `enriquecerContexto()` é onde a 'alquimia semântica' ocorre. Ela pega o blueprint estrutural de Maven e preenche cada arquivo de regra com conhecimento útil sobre o projeto, padrões de implementação e instruções específicas para agentes IA.
