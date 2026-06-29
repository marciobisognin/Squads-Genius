# Primus — Super Agente Meta-Orquestrador de Squads

> O agente acima de todos os squads. Ele não substitui os squads — ele os
> **governa**: indexa, cria o wiki de acesso rápido, roteia tarefas para o
> agente certo, cria agentes e squads novos quando há lacunas e mantém um
> **sistema mental que evolui a cada interação**.

- Nome técnico: `primus-meta-orchestrator-super-squad`
- Versão: 1.0.0 · Licença: MIT · Idioma: pt-BR

## O que ele faz

1. **Mapeia** qualquer pasta de squads e gera um índice estruturado.
2. **Cria um wiki de acesso rápido** que mostra, por capacidade, qual squad e
   qual agente usar para cada tipo de tarefa.
3. **Roteia** uma tarefa em linguagem livre para o melhor agente disponível,
   com justificativa e alternativas.
4. **Detecta lacunas** e, quando falta cobertura, **cria agentes e squads novos**
   (esqueleto válido) encaminhando o refino ao Maeve Genius Forge.
5. **Aprende continuamente**: um cérebro persistente reforça conceitos,
   acompanha o desempenho dos agentes e melhora as recomendações a cada uso.

## Agentes

| Agente | Papel |
| --- | --- |
| `primus-prime-orchestrator` | Super agente: decide reusar × combinar × criar; governa o ciclo. |
| `squad-cartographer` | Varre a pasta e gera índice + wiki de acesso rápido. |
| `task-router-oracle` | Recomenda o squad/agente ideal para a tarefa. |
| `gap-detector-architect` | Detecta lacunas e cria agentes/squads novos. |
| `mnemosyne-memory-keeper` | Sistema mental evolutivo (memória que aprende). |
| `aegis-governance-sentinel` | Qualidade, segurança, autoria e go/no-go. |

## Como ativar

- **Ativação manual:** leia `squad.yaml` e assuma a persona de
  `agents/primus-prime-orchestrator.md`, seguindo
  `workflows/full_meta_orchestration.yaml`.
- **Determinístico (recomendado para as etapas mecânicas):** use os scripts
  abaixo (Python 3.11+, sem dependências externas obrigatórias).

## Uso rápido (scripts determinísticos)

Basta apontar para a pasta que contém todos os squads (cada um com `squad.yaml`).

```bash
cd squads/primus-meta-orchestrator-super-squad

# 1. Indexar todos os squads e gerar o wiki de acesso rápido
python3 scripts/index_squads.py --squads-root ../.. --output-dir output
#   -> output/squad_index.json  (máquina)
#   -> output/SQUAD_WIKI.md      (humano: qual agente para cada tarefa)

# 2. Descobrir qual agente usar para uma tarefa
python3 scripts/route_task.py --task "criar carrossel premium para Instagram" \
    --index output/squad_index.json --top 5

# 3. Aprender com a decisão (o sistema mental evolui)
python3 scripts/memory_system.py record \
    --task "criar carrossel premium para Instagram" \
    --squad copo-de-cafe-academico-squad --agent gerador-carrossel \
    --outcome success
python3 scripts/memory_system.py stats

# 4. Quando faltar cobertura: criar um squad novo
python3 scripts/scaffold_squad.py --name meu-novo-squad \
    --commercial-name "Meu Novo Squad" --positioning "Resolve X para Y" \
    --agents "orquestrador:Coordena;executor:Executa" \
    --output ../meu-novo-squad

# 5. Validar (quality gate go/no-go)
python3 scripts/validate_squad.py --root .
```

## O sistema mental que evolui

O cérebro vive em `memory/brain.json` e evolui a cada interação: reforça os
conceitos mais demandados, acompanha sucesso/falha por agente, deriva
aprendizados e acumula lacunas recorrentes que viram propostas de novos squads.
O `evolve` aplica decaimento (esquecimento saudável) e recomputa os
aprendizados. O roteador (`route_task.py`) lê esses pesos e melhora o ranking.

Veja `docs/ARQUITETURA.md` para o desenho completo.

## Workflows

- `full_meta_orchestration` — ciclo completo (índice → wiki → rota → lacuna → criação → memória → governança).
- `quick_routing` — atalho: rotear uma tarefa e registrar a decisão.
- `index_refresh` — reindexar e regenerar o wiki quando squads mudam.
- `memory_evolution_cycle` — manutenção periódica do cérebro.

## Princípios

- Reutilizar agentes existentes antes de criar novos.
- Priorizar scripts determinísticos quando não houver necessidade de LLM.
- Separar observado, inferido, hipótese, recomendação e risco.
- Não copiar marcas, prompts ou ativos proprietários de terceiros.
- Nunca publicar segredos; publicar no GitHub apenas com autorização humana.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
