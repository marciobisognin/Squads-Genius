---
task: mapearCisnesNegros()
responsavel: cygnus-vidente
responsavel_type: agent
atomic_layer: Organism
---

# mapearCisnesNegros()

> Analisa um sistema/projeto e identifica todas as vulnerabilidades a Cisnes Negros, classificando variáveis entre Mediocristão e Extremistão.

## Pipeline

```
[Input: sistema/projeto] → [Classificar variáveis] → [Mapear exposições] → [Detectar vieses] → [Output: cisnes-negros-mapa.md]
```

## Entrada

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| `target` | `string` | Sistema, projeto ou decisão a analisar | ✅ |
| `domain` | `string` | Domínio (financeiro, tecnológico, organizacional) | ❌ |
| `variables` | `string[]` | Lista de variáveis-chave a classificar | ❌ |
| `context` | `markdown` | Contexto adicional sobre o sistema | ❌ |

## Saída

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| `cisnes-negros-mapa.md` | `markdown` | Mapa completo de vulnerabilidades | ✅ |
| `classification-registry.md` | `markdown` | Registro Mediocristão/Extremistão | ✅ |
| `bias-report.md` | `markdown` | Vieses detectados | ✅ |

## Checklist

### Pré-condições
- [ ] Target definido e compreensível
- [ ] Domínio identificado ou inferível
- [ ] Contexto suficiente para análise (mínimo 3 variáveis-chave)

### Pós-condições
- [ ] Todas as variáveis-chave classificadas (Mediocristão/Extremistão)
- [ ] Pelo menos 3 potenciais Cisnes Negros mapeados
- [ ] Vieses verificados contra checklist de 5 falácias
- [ ] Exposições identificadas (côncavas vs convexas)
- [ ] Nenhuma previsão feita — apenas vulnerabilidades mapeadas

## Performance

| Métrica | Valor |
|---------|-------|
| Duração estimada | 5-10 min |
| Cacheable | Não (depende do contexto) |
| Idempotente | Sim |

## Error Handling

| Erro | Ação |
|------|------|
| Input insuficiente | Solicitar clarificação (máx 3 perguntas) |
| Domínio desconhecido | Pedir exemplos concretos ao usuário |
| Sem variáveis no Extremistão | Documentar como "sistema predominantemente Mediocristão" |

## Metadata

| Campo | Valor |
|-------|-------|
| version | 1.0.0 |
| author | marciobisognin |
| story | Genius Athena-Strange — Taleb Pipeline |
