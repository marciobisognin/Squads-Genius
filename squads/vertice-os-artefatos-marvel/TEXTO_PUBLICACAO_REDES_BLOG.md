# VÉRTICE-OS | Arquitetura interna temática

O VÉRTICE-OS é uma arquitetura interna de agentes que organiza orquestração, planejamento, roteamento, runtime durável, governança, evidência, observabilidade, segurança, políticas, adapters e meta-construção de squads.

A proposta central é simples: cada agente tem ID técnico estável, codinome, função explícita, entradas, saídas, permissões, gates de qualidade e regras de escalonamento.

O sistema não usa personagens como agentes ou identidades. A camada temática funciona como linguagem interna memorável para artefatos, materiais, locais e elementos, sem substituir contratos, schemas, testes ou observabilidade.

## Exemplos de uso

- Coordenar uma ordem complexa por DAG com checkpoints.
- Validar handoffs entre agentes por contrato.
- Exigir aprovação humana para ações irreversíveis.
- Isolar conteúdo suspeito antes de contaminar memória ou artefatos.
- Reconstruir a fonte de cada claim factual.
- Revogar runs e credenciais diante de incidente crítico.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
