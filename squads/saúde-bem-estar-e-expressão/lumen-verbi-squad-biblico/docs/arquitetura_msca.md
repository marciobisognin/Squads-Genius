# Arquitetura — MSCA (Mecanismo de Seleção e Combinação de Agentes)

O MSCA é o cérebro do squad. Ele transforma uma consulta em linguagem natural em
um plano de orquestração e em uma resposta composta. Combina etapas
**determinísticas** (scripts, reproduzíveis e baratas) com etapas que exigem
**LLM** (redação no estilo de cada persona).

## Fluxo

```
Usuário
  │  consulta em linguagem natural
  ▼
[1] Intake (01)  ──► normaliza, confirma escopo bíblico
  ▼
[2] PLN/Intenção (02)  ──► parse_referencia_biblica.py
        • entidades (personagens, livros, cap:vers)
        • intenção (teológica | histórica | interpretativa | combinada)
        • temas/doutrinas
  ▼
[3] Recuperação BDC (03)  ──► curador-bdc
        • versículos, contexto histórico, definições, fontes
  ▼
[4] Seleção/Combinação (04)  ──► selecionar_agentes.py
        • personas primárias (1–2)
        • historiadores complementares (se houver gatilho)
        • múltiplas perspectivas (scores próximos)
        • fallback (sem match → curador esclarece)
  ▼
[5] Resposta da persona (05)  ──► montar_prompt_persona.py + LLM
  ▼
[6] Contexto histórico (06)  ──► historiador (condicional)
  ▼
[7] Composição (07)  ──► ordem lógica: teológico → histórico, com atribuição
  ▼
[8] Guardrails (08)  ──► validar_fidelidade.py + guardiao-teologico  [GATE]
  ▼
[9] Refinamento (09)  ──► follow-ups reabrem o ciclo
  ▼
[10] Registro (10)  ──► histórico + métricas
```

## Determinístico vs. LLM

| Etapa | Determinístico | LLM |
|-------|----------------|-----|
| Parse de referências | `parse_referencia_biblica.py` | — |
| Seleção/ranqueamento de agentes | `selecionar_agentes.py` | — |
| Montagem do prompt | `montar_prompt_persona.py` | — |
| Validação de guardrails | `validar_fidelidade.py` | revisão final do guardião |
| Redação no estilo da persona | — | sim |
| Composição narrativa | — | sim |

Princípio: **só usar LLM onde há ambiguidade ou geração de texto**; a seleção e a
validação são reproduzíveis e auditáveis.

## Lógica de combinação

- **Seleção primária:** 1–2 personas de maior score (conhecimento + nome citado + mapa semântico).
- **Seleção secundária:** historiador(es) quando há gatilho histórico/cultural/textual ou quando um evento mapeado os indica.
- **Múltiplas perspectivas:** quando os scores das primeiras personas estão próximos (`sugere_multiplas_perspectivas`).
- **Fallback:** sem persona pontuada, o `curador-bdc` pede esclarecimento.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
