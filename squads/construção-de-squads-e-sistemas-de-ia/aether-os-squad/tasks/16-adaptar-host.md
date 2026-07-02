# Task 16 — Adaptar Host e Economizar Tokens

**Executor:** host_adapter + token_economy (motores) + Cortex
**Fase:** Contrato de host e economia (PRD v1.3, §9.4/9.5 e §26.5)

## Objetivo
Tratar qualquer host de agente como driver atrás de contrato formal
(`aether.host-adapter/v1`) e reduzir o gasto de tokens por alavancas
determinísticas **neutras em relação às decisões**.

## Entradas
- Contrato do host (capacidades declaradas: `subagent_fork`, `prompt_caching`,
  `native_sandbox`, `notification_channels`, `approval_ui`, `streaming`) +
  `config/token_economy.yaml`.

## Saídas
- Vetor de capacidades consultável (`host_adapter.py capabilities`).
- Decisão de derivação por sub-tarefa (`token_economy.py derive`):
  herança de contexto vs. instanciação limpa, registrada como evento.
- Telemetria de economia por alavanca.

## Passos
1. `python3 scripts/host_adapter.py validate --adapter <host.json>` — o
   núcleo nunca depende de capacidade não declarada.
2. Capacidade ausente ⇒ **degradação determinística da tabela** (nunca
   improviso): sem `subagent_fork` → instanciação limpa; sem `native_sandbox`
   → sandbox do AETHER; sem `approval_ui` → fila da CLI com os mesmos prazos.
3. Decisão de derivação — regras em ordem:
   (1) host sem `subagent_fork` → limpa;
   (2) conteúdo não confiável no pai ou classe de dado do filho inferior →
   **limpa, sempre** (segurança precede economia);
   (3) contexto herdado acima do limiar → limpa;
   (4) caso contrário → herança, registrada como evento.
4. Handoff por referência: envelopes SACP transportam `artifact://` e
   asserções, nunca conteúdo bruto extenso (teto de tokens por envelope).
5. Layout cacheável: estável no início (manifesto, sistema, prósopon),
   variável no fim (briefing, memória, handoff).
6. **Neutralidade verificada**: decision-replay compara pares com/sem
   cache/herança; divergência é quebra de invariante (alerta crítico).

## Critérios de aceite
- Nenhuma alavanca altera o resultado de qualquer decisão (replay `pass`).
- Toda degradação segue a tabela declarada; paridade entre hosts é verificada,
  não presumida.
- Derivação com herança nunca ocorre com conteúdo não confiável ou
  rebaixamento de classe de dado.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
