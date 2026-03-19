---
task: mapearCisnesNegros()
responsavel: "Cygnus Vidente"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: target
    tipo: string
    obrigatorio: true
    descricao: "Sistema, projeto ou decisão a analisar"
  - nome: domain
    tipo: string
    obrigatorio: false
    descricao: "Domínio (financeiro, tecnológico, organizacional)"
  - nome: variables
    tipo: array
    obrigatorio: false
    descricao: "Lista de variáveis-chave a classificar"
  - nome: context
    tipo: file
    obrigatorio: false
    descricao: "Contexto adicional sobre o sistema (ex: input.md)"

Saida:
  - nome: cisnesNegrosMapa
    tipo: file
    obrigatorio: true
    descricao: "Mapa completo de vulnerabilidades (destino: projetarAntifragilidade())"
  - nome: classificationRegistry
    tipo: file
    obrigatorio: true
    descricao: "Registro Mediocristão/Extremistão"
  - nome: biasReport
    tipo: file
    obrigatorio: true
    descricao: "Vieses detectados"

Checklist:
  pre-conditions:
    - "[ ] Target definido e compreensível"
    - "[ ] Domínio identificado ou inferível"
    - "[ ] Contexto suficiente para análise (mínimo 3 variáveis-chave)"
  post-conditions:
    - "[ ] Todas as variáveis-chave classificadas (Mediocristão/Extremistão)"
    - "[ ] Pelo menos 3 potenciais Cisnes Negros mapeados"
    - "[ ] Vieses verificados contra checklist de 5 falácias"
    - "[ ] Exposições identificadas (côncavas vs convexas)"
    - "[ ] Nenhuma previsão feita — apenas vulnerabilidades mapeadas"

Performance:
  duration_expected: "5-10 min"
  cacheable: false
  parallelizable: true
  skippable_when: "Nunca — base da análise"

Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: "5s"
  fallback: "Solicitar clarificação ao usuário"
  notification: "orchestrator"

Metadata:
  version: 1.0.0
  author: marciobisognin
  story: Genius Athena-Strange — Taleb Pipeline
---

# mapearCisnesNegros()

## Pipeline Diagram

```
[Input: target] ──→ [mapearCisnesNegros()] ──→ [cisnes-negros-mapa.md] ──→ [projetarAntifragilidade()]
```

## Descrição

Analisa um sistema/projeto e identifica todas as vulnerabilidades a Cisnes Negros, classificando variáveis entre Mediocristão e Extremistão. Esta é a fase de fundação, onde o "impensável" é trazido para o mapeamento técnico.

### Responsabilidades

1. **Classificação do Domínio** — Distinguir entre Mediocristão (eventos extremos irrelevantes) e Extremistão (eventos extremos dominam).
2. **Mapeamento de Vulnerabilidade** — Identificar onde o sistema é "côncavo" (downside ilimitado).
3. **Escaneamento de Vieses** — Desmontar a falácia narrativa e o platonismo que ocultam riscos reais.
