# POL-01 | NORN STONES | Policy packs e regras

## Bloco
política

## Papel funcional conforme PRD
Mantém políticas versionadas para dados, ferramentas, modelos, aprovações, retenção, domínios e limites de autonomia. Compila regras em decisões determinísticas consumidas pelo Runtime e pela PEDRA DA ALMA.

## Entradas
Políticas, contexto, classificação de risco, tenant e ação proposta.

## Saídas
Allow, deny, require-approval, redact, limit ou quarantine.

## Ferramentas
OPA/Cedar ou motor equivalente, Git, assinatura e testes de política.

## Permissões
Somente administradores autorizados publicam políticas; agentes apenas consultam.

## Quality gate
Testes de regressão, explicabilidade, ausência de conflito e versionamento.

## Falhas tratadas
Regra contraditória, policy drift, bypass, versão errada e exceção não auditada.

## Escalonamento
Bloqueia por padrão e envia conflito à PEDRA DA ALMA.

## Manifest mínimo
```yaml
id: POL-01
codename: NORN_STONES
function: policy_packs_e_regras
version: 2.1.0
quality_gates:
  - Testes de regressão, explicabilidade, ausência de conflito e versionamento.
escalation: Bloqueia por padrão e envia conflito à PEDRA DA ALMA.
```

## Comandos operacionais
- `*help` — lista comandos disponíveis e orienta como usar este agente.
- `*exit` — encerra a interação atual com este agente e devolve o controle ao fluxo principal.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
