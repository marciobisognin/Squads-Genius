# Limites operacionais — Breach Compass

## Permitido

- triagem, preservação e construção de timeline;
- extração e organização de IOCs a partir de dados autorizados ou sanitizados;
- análise estática e planejamento de análise dinâmica em laboratório isolado;
- planejamento reversível de contenção, erradicação e recuperação;
- mapeamento de detecções, lições aprendidas e testes de regressão.

## Bloqueado por padrão

- execução de malware no host ou em produção;
- contenção automática sem aprovação e rollback;
- persistência, evasão, exfiltração e negação de serviço;
- coleta de credenciais ou phishing real;
- divulgação indevida de dados pessoais, segredos ou evidências sensíveis.

## Decisões do roteador

- `GATED_HANDOFF`: requisitos mínimos atendidos; a ferramenta de domínio valida allowlist e segurança;
- `PLAN_ONLY`: produz plano, laboratório ou checklist, sem executar a técnica;
- `DENY`: autorização, isolamento, contexto ou banda insuficientes.

Mesmo em `GATED_HANDOFF`, `execution_performed` permanece `false`.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
