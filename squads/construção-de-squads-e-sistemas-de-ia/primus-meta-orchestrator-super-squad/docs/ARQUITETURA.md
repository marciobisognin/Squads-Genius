# Arquitetura — Primus Meta-Orchestrator

O Primus é um **super agente acima dos squads**. Ele não executa o trabalho de
domínio; ele decide **quem** deve executar, **cria** o que falta e **aprende**
com cada decisão.

## Visão geral

```
              ┌───────────────────────────────────────────────┐
   pedido ──▶ │            primus-prime-orchestrator           │
              │   (decide reusar × combinar × criar; governa)  │
              └───┬───────────┬───────────┬───────────┬────────┘
                  │           │           │           │
            cartographer   router      gap-detector  memory-keeper
                  │           │           │           │
        index_squads.py  route_task.py scaffold_squad memory_system.py
                  │           │           │           │
            squad_index   recomendação  novo squad   brain.json (evolui)
            + WIKI.md                                  │
                  └───────────── governance ──────────┘
                              validate_squad.py (go/no-go)
```

## Componentes determinísticos (sem custo de LLM)

| Script | Papel |
| --- | --- |
| `index_squads.py` | Varre a pasta, indexa squads/agentes e gera o wiki de acesso rápido. |
| `route_task.py` | Recomenda o agente ideal por similaridade + memória; sinaliza GAP. |
| `memory_system.py` | Sistema mental evolutivo (record/recall/evolve/stats/gap). |
| `scaffold_squad.py` | Cria o esqueleto válido de um squad novo. |
| `validate_squad.py` | Quality gate go/no-go. |

A camada de LLM (os agentes `.md`) entra apenas para julgamento, justificativa e
refino — o trabalho mecânico é determinístico, portável e barato.

## O sistema mental que evolui

O cérebro (`memory/brain.json`) acumula:

- **interactions** — histórico de roteamentos e resultados;
- **concept_weights** — peso de cada conceito, reforçado pelo uso e reduzido por
  decaimento (`evolve`);
- **agent_performance** — usos, sucessos e falhas por agente, ajustando a
  confiança nas recomendações;
- **learnings** — insights derivados deterministicamente (agentes confiáveis,
  temas dominantes, lacunas abertas);
- **gaps** — necessidades não atendidas que, ao se repetirem, viram propostas de
  novos squads.

Quanto mais o Primus é usado, mais o roteamento acerta: `route_task.py` lê os
`concept_weights` e pondera o ranking pela memória.

## Fluxo recomendado

1. `index_refresh` — (re)gerar índice + wiki quando squads mudam.
2. `quick_routing` — rotear uma tarefa e registrar a decisão.
3. `full_meta_orchestration` — ciclo completo com criação e governança.
4. `memory_evolution_cycle` — manutenção periódica do cérebro.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
