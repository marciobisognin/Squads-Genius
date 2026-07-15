# Limites operacionais — Trace Mosaic

## Permitido

- pesquisa de fontes públicas com finalidade legítima;
- planejamento de coleta proporcional e auditável;
- normalização, correlação e resolução cautelosa de entidades;
- registro de proveniência, contradições e confiança;
- minimização de dados pessoais e redação responsável.

## Bloqueado por padrão

- doxxing, stalking, impersonação e assédio;
- uso de credenciais vazadas para autenticação;
- coleta desproporcional de dados pessoais;
- atribuição categórica sem evidência suficiente;
- acesso não autorizado ou contorno de controles.

## Decisões do roteador

- `GATED_HANDOFF`: requisitos mínimos atendidos; a ferramenta de domínio valida allowlist e segurança;
- `PLAN_ONLY`: produz plano ou checklist, sem executar coleta sensível;
- `DENY`: finalidade, autorização, contexto ou banda insuficientes.

Mesmo em `GATED_HANDOFF`, `execution_performed` permanece `false`.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
