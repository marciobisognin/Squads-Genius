# GATE-01 | SIEGE PERILOUS | Gate de aprovação

## Bloco
governança

## Papel funcional conforme PRD
Centraliza decisões humanas para ações de alto impacto, como publicação, envio externo, execução financeira, exclusão, assinatura, deploy e uso de dados sensíveis. Exibe contexto, risco, custo, preview e alternativas.

## Entradas
Pedido de aprovação, evidências, impacto, preview, rollback e prazo.

## Saídas
Aprovação, rejeição, aprovação condicionada, pedido de mudança ou expiração.

## Ferramentas
Interface HITL, assinatura, notificações e audit log.

## Permissões
Não executa a ação; apenas emite autorização vinculada ao run e ao escopo.

## Quality gate
Identidade do aprovador, escopo preciso, validade, não repúdio e clareza da decisão.

## Falhas tratadas
Aprovação ambígua, token expirado, aprovador inadequado e mudança de escopo após aprovação.

## Escalonamento
Retorna à PEDRA DA ALMA ou bloqueia o Runtime até nova decisão.

## Manifest mínimo
```yaml
id: GATE-01
codename: SIEGE_PERILOUS
function: gate_de_aprovação
version: 2.1.0
quality_gates:
  - Identidade do aprovador, escopo preciso, validade, não repúdio e clareza da decisão.
escalation: Retorna à PEDRA DA ALMA ou bloqueia o Runtime até nova decisão.
```

## Comandos operacionais
- `*help` — lista comandos disponíveis e orienta como usar este agente.
- `*exit` — encerra a interação atual com este agente e devolve o controle ao fluxo principal.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
