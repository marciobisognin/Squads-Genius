# OPS-03 | BIFROST BRIDGE | Mensageria e handoffs

## Bloco
infraestrutura

## Papel funcional conforme PRD
Transporta eventos e ordens entre agentes, squads e serviços. Preserva correlação, causação, prioridade, prazo e delivery semantics. Não interpreta o conteúdo da tarefa.

## Entradas
Eventos validados, filas, prioridade, deadline e destino.

## Saídas
Entrega confirmada, retry, dead-letter ou evento de falha.

## Ferramentas
Redis Streams, Kafka, NATS ou broker equivalente.

## Permissões
Somente entrega mensagens com selo ADAMANTIUM válido.

## Quality gate
Ordem causal, baixa perda, latência, backpressure e dead-letter observável.

## Falhas tratadas
Mensagem duplicada, congestionamento, destino indisponível e ordem causal quebrada.

## Escalonamento
Aciona PEDRA DO TEMPO para retry, M'KRAAN CRYSTAL para diagnóstico e NEGATIVE ZONE para tráfego anômalo.

## Manifest mínimo
```yaml
id: OPS-03
codename: BIFROST_BRIDGE
function: mensageria_e_handoffs
version: 2.1.0
quality_gates:
  - Ordem causal, baixa perda, latência, backpressure e dead-letter observável.
escalation: Aciona PEDRA DO TEMPO para retry, M'KRAAN CRYSTAL para diagnóstico e NEGATIVE ZONE para tráfego anômalo.
```

## Comandos operacionais
- `*help` — lista comandos disponíveis e orienta como usar este agente.
- `*exit` — encerra a interação atual com este agente e devolve o controle ao fluxo principal.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
