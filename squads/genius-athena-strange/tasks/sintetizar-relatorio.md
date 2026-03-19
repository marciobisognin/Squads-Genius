---
task: sintetizarRelatorio()
responsavel: hermes-orquestrador
responsavel_type: agent
atomic_layer: Organism
---

# sintetizarRelatorio()

> Consolida todos os artefatos em um relatório executivo acionável que classifica o sistema como Frágil, Robusto ou Antifrágil.

## Pipeline

```
[Todos os artefatos] → [Sintetizar insights] → [Gerar TL;DR] → [Plano de Ação] → [Output: relatorio-executivo-antifragil.md]
```

## Entrada

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| `cisnes-negros-mapa.md` | `markdown` | Mapa de Cygnus | ✅ |
| `antifragile-blueprint.md` | `markdown` | Blueprint de Hydra | ✅ |
| `barbell-strategy.md` | `markdown` | Estratégia de Sêneca | ✅ |
| `validation-report.md` | `markdown` | Relatório de Medusa | ✅ |
| `fragility-scorecard.md` | `markdown` | Scorecard de Medusa | ✅ |

## Saída

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| `relatorio-executivo-antifragil.md` | `markdown` | Relatório executivo final | ✅ |

## Checklist

### Pré-condições
- [ ] Todos os 5 artefatos de entrada recebidos
- [ ] `validation-report.md` contém status final (PASSED/FAILED)

### Pós-condições
- [ ] TL;DR de 3 bullets no topo
- [ ] Status global declarado (ANTIFRÁGIL / ROBUSTO / FRÁGIL)
- [ ] Seções de cada agente presentes
- [ ] Plano de ação com 3 horizontes (24h, 1 semana, 1 mês)
- [ ] Anexos referenciados

## Metadata

| Campo | Valor |
|-------|-------|
| version | 1.0.0 |
| author | marciobisognin |
| story | Genius Athena-Strange — Taleb Pipeline |
