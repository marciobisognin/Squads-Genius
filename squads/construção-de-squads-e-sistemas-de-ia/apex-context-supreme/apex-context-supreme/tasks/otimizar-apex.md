---
task: otimizarContexto()
responsavel: "Trim"
responsavel_type: Agente
atomic_layer: Molecule

Entrada:
  - nome: rawRuleFiles
    tipo: array
    descricao: "Arquivos de regras brutos gerados por Spark"
    obrigatorio: true
  - nome: optimizationTargets
    tipo: array
    descricao: "Plataformas específicas para otimização cross-platform (do squad.yaml)"
    obrigatorio: true

Saida:
  - nome: optimizedRuleFiles
    tipo: array
    descricao: "Arquivos de regras com redução de ruído e densidade otimizada"
    obrigatorio: true

Checklist:
  pre-conditions:
    - "[ ] Arquivos brutos acessíveis para edição"
    - "[ ] Limites de tokens identificados para cada plataforma-alvo"
  post-conditions:
    - "[ ] Redundâncias cross-platform removidas via referências cruzadas"
    - "[ ] Redução de verbosidade mantendo a semântica em pelo menos 90%"
    - "[ ] Nenhuma regra crítica foi deletada durante a 'escultura'"

Performance:
  duration_expected: "2-4 minutos"
  cost_estimated: "~1500 tokens (Opus/Sonnet)"
  cacheable: true
  parallelizable: false
  skippable_when: "Tamanho total dos arquivos brutos está abaixo do threshold crítico (ex: 2000 tokens)"

Error Handling:
  strategy: abort
  fallback: "Manter arquivos brutos se a otimização falhar e reportar log"
  notification: "apex-orquestrista"

Metadata:
  story: "Como otimizador de janela, preciso garantir que o contexto seja eficiente e caiba nos limites das IAs"
  version: "1.0.0"
  author: "Nirvana Squad Creator (Refined)"
---

# otimizarContexto()

## Pipeline Diagram
```
┌───────────────┐     ┌───────────────┐     ┌───────────────────────┐
│ Regras Brutas │────▶│    Trim       │────▶│  Regras Otimizadas    │
│ (.md Files)   │     │ (trim-escultor)│     │  (High Density)       │
└───────────────┘     └───────────────┘     └───────────────────────┘
                               │                      │
                               │ Phase 3              │ Alimenta Vigil
                               ▼                      ▼
                        ┌────────────┐         ┌───────────────┐
                        │ Token Poda │         │ Slim Context  │
                        │ Deduplicat │         │ Cross-links   │
                        └────────────┘         └───────────────┘
```

## Descrição
A task `otimizarContexto()` atua como um 'escultor de sabedoria'. Ela revisa as regras geradas por Spark, remove redundâncias desnecessárias entre diferentes plataformas e otimiza o uso de tokens para que o contexto caiba confortavelmente na janela de atenção da IA sem perda de qualidade.
