# Arquitetura da Ferramenta — `<nome>`

> Template do DÉMIOURGÓS. Boring-but-reliable; comprar o que não é diferencial; preferir local-first.

## Stack
- Linguagem/runtime, framework, banco (`SQLite`/`CSV` no local-first).

## Modelo de dados
- Entidades, relações, chaves.

## APIs / Integrações
- `<endpoint>` — método, contrato, auth (comprar auth/billing quando não for diferencial).

## Fluxos de automação
- `<gatilho> -> <ação> -> <resultado>`

## Camada de IA
- Onde o LLM emite JSON; onde o Python calcula (invariante aplicado dentro da ferramenta-cliente).

## RAG / Recuperação
- Estratégia (`rag`/`rules`/`hybrid`), índice, fonte.

## Deployment
- `local_first | web_saas | hybrid` (justificar a escolha).

## Build vs Buy
| Componente | Decisão | Justificativa |
|---|---|---|
| Auth | Buy | não é diferencial |

## Backlog inicial
- [ ] `<item implementável>`

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
