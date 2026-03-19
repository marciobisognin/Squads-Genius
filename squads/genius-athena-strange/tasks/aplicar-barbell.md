---
task: aplicarBarbell()
responsavel: "Sêneca Estrategista"
responsavel_type: Agente
atomic_layer: Organism

Entrada:
  - nome: antifragileBlueprint
    tipo: file
    obrigatorio: true
    descricao: "Blueprint antifrágil de Hydra"
  - nome: optionalityMap
    tipo: file
    obrigatorio: true
    descricao: "Opcionalidades mapeadas por Hydra"

Saida:
  - nome: barbellStrategy
    tipo: file
    obrigatorio: true
    descricao: "Estratégia barbell aplicada (destino: auditarFragilidade())"
  - nome: exposureMap
    tipo: file
    obrigatorio: true
    descricao: "Mapa de exposições côncavas vs convexas"
  - nome: ruinThresholds
    tipo: file
    obrigatorio: true
    descricao: "Limiares de ruína definidos"

Checklist:
  pre-conditions:
    - "[ ] antifragileBlueprint recebido e validado"
    - "[ ] Opcionalidades listadas"
  post-conditions:
    - "[ ] Polo seguro definido (85-90% dos recursos)"
    - "[ ] Polo agressivo definido (10-15% dos recursos)"
    - "[ ] Zero alocação na 'zona intermediária'"
    - "[ ] Todas as exposições classificadas (côncava/convexa/linear)"
    - "[ ] Limiar de ruína definido para cada cenário crítico"

Performance:
  duration_expected: "5-10 min"
  cacheable: false
  parallelizable: false
  skippable_when: "Nunca — define exposição financeira ou técnica final"

Error Handling:
  strategy: abort
  retry:
    max_attempts: 1
    delay: "0s"
  fallback: "FAIL automático — bloquear pipeline se risco de ruína for inaceitável"
  notification: "orchestrator"

Metadata:
  version: 1.0.0
  author: marciobisognin
  story: Genius Athena-Strange — Taleb Pipeline
---

# aplicarBarbell()

## Pipeline Diagram

```
[antifragileBlueprint] ──→ [aplicarBarbell()] ──→ [barbell-strategy.md] ──→ [auditarFragilidade()]
```

## Descrição

Recebe o blueprint antifrágil e aplica a Estratégia Barbell, mapeando exposições assimétricas e definindo limiares de ruína. É a fase de definição estratégica, equilibrando a fome de ganho (polo agressivo) com a paranoia de sobrevivência (polo seguro).
