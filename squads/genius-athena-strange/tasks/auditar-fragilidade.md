---
task: auditarFragilidade()
responsavel: medusa-auditora
responsavel_type: agent
atomic_layer: Organism
---

# auditarFragilidade()

> Audita todos os artefatos contra 6 critérios de fragilidade, verificando skin in the game, Efeito Lindy e risco de ruína.

## Pipeline

```
[Todos os artefatos] → [6 Critérios] → [Skin in the Game] → [Efeito Lindy] → [Scorecard] → [Output: validation-report.md]
```

## Entrada

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| `cisnes-negros-mapa.md` | `markdown` | Mapa de Cygnus | ✅ |
| `antifragile-blueprint.md` | `markdown` | Blueprint de Hydra | ✅ |
| `barbell-strategy.md` | `markdown` | Estratégia de Sêneca | ✅ |
| `exposure-map.md` | `markdown` | Exposições de Sêneca | ✅ |

## Saída

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| `validation-report.md` | `markdown` | Relatório de auditoria com PASSED/FAILED | ✅ |
| `fragility-scorecard.md` | `markdown` | Scorecard por componente | ✅ |
| `acceptanceStatus` | `boolean` | `true` se todos os 6 critérios PASSED | ✅ |

## Checklist

### Pré-condições
- [ ] Todos os 4 artefatos de entrada recebidos
- [ ] Nenhum artefato com erros estruturais

### Pós-condições
- [ ] 6 critérios avaliados (Tríade, Barbell, Skin in the Game, Via Negativa, Lindy, Ruína)
- [ ] Scorecard gerado com pontuação por componente
- [ ] Fragilistas identificados (se houver)
- [ ] Status final declarado: PASSED ou FAILED
- [ ] Para cada FAIL: remediação documentada

## Performance

| Métrica | Valor |
|---------|-------|
| Duração estimada | 5-8 min |
| Cacheable | Não |
| Idempotente | Sim |

## Error Handling

| Erro | Ação |
|------|------|
| Artefato ausente | Bloquear validação, solicitar fase anterior |
| Critério ambíguo | Classificar como WARN e documentar |
| Risco de ruína não resolvido | FAIL automático + alerta urgente |

## Metadata

| Campo | Valor |
|-------|-------|
| version | 1.0.0 |
| author | marciobisognin |
| story | Genius Athena-Strange — Taleb Pipeline |
