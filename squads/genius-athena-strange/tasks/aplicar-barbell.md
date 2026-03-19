---
task: aplicarBarbell()
responsavel: seneca-estrategista
responsavel_type: agent
atomic_layer: Organism
---

# aplicarBarbell()

> Recebe o blueprint antifrágil e aplica a Estratégia Barbell, mapeando exposições assimétricas e definindo limiares de ruína.

## Pipeline

```
[antifragile-blueprint.md] → [Definir Polos Barbell] → [Mapear Assimetrias] → [Definir Ruína] → [Pré-mortem Estoico] → [Output: barbell-strategy.md]
```

## Entrada

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| `antifragile-blueprint.md` | `markdown` | Blueprint antifrágil de Hydra | ✅ |
| `optionality-map.md` | `markdown` | Opcionalidades mapeadas por Hydra | ✅ |

## Saída

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| `barbell-strategy.md` | `markdown` | Estratégia barbell aplicada | ✅ |
| `exposure-map.md` | `markdown` | Mapa de exposições côncavas vs convexas | ✅ |
| `ruin-thresholds.md` | `markdown` | Limiares de ruína definidos | ✅ |

## Checklist

### Pré-condições
- [ ] `antifragile-blueprint.md` recebido e validado
- [ ] Opcionalidades listadas

### Pós-condições
- [ ] Polo seguro definido (85-90% dos recursos)
- [ ] Polo agressivo definido (10-15% dos recursos)
- [ ] Zero alocação na "zona intermediária"
- [ ] Todas as exposições classificadas (côncava/convexa/linear)
- [ ] Limiar de ruína definido para cada cenário crítico
- [ ] Pré-mortem estoico executado para top 3 riscos

## Performance

| Métrica | Valor |
|---------|-------|
| Duração estimada | 5-10 min |
| Cacheable | Não |
| Idempotente | Sim |

## Error Handling

| Erro | Ação |
|------|------|
| Blueprint incompleto | Solicitar revisão a Hydra |
| Impossível definir polo seguro | Escalar como "sistema originalmente frágil" |
| Risco de ruína identificado sem mitigação | FAIL automático — bloquear pipeline |

## Metadata

| Campo | Valor |
|-------|-------|
| version | 1.0.0 |
| author | marciobisognin |
| story | Genius Athena-Strange — Taleb Pipeline |
