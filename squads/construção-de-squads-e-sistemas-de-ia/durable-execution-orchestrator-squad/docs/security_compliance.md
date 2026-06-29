# Segurança, Compliance e Auditoria

## Diretrizes

- Não persistir credenciais em texto claro.
- Usar chaves de idempotência para chamadas externas.
- Registrar aprovação humana com ator, canal, horário e payload mínimo.
- Aplicar minimização de dados e retenção configurável conforme LGPD.
- Preparar alinhamento com ISO 42001 para governança de sistemas de IA.

## Controles implementados no protótipo

- Event log estruturado.
- Separação de sinais e eventos.
- Compensações auditáveis.
- Métricas de tokens, custo e retries.
- Validador local do pacote.

## Controles futuros

- Criptografia em repouso por backend.
- RBAC por squad e usuário.
- Exportador OpenTelemetry real.
- Integração com Aegis Security Gateway.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
