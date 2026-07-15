# Limites operacionais — Scope Sentinel

## Permitido

- planejamento e documentação de testes autorizados;
- coleta pública ou de baixo impacto dentro do escopo declarado;
- análise de versões e advisories;
- validação de evidências, priorização de remediação e reteste;
- laboratórios sintéticos ou explicitamente autorizados.

## Bloqueado por padrão

- força bruta, captura de credenciais, phishing real e engenharia social ofensiva;
- exploração destrutiva, persistência, exfiltração e negação de serviço;
- ações fora do escopo, sem autorização verificável ou acima da banda aprovada;
- mudanças de estado sem aprovação humana.

## Decisões do roteador

- `GATED_HANDOFF`: requisitos mínimos atendidos; uma ferramenta de domínio ainda deve validar allowlist e segurança;
- `PLAN_ONLY`: produz plano, laboratório ou checklist, sem executar a técnica;
- `DENY`: autorização, contexto, banda ou ambiente insuficientes.

Mesmo em `GATED_HANDOFF`, `execution_performed` permanece `false`.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
