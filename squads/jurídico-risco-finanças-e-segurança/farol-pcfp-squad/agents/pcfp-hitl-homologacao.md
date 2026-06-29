# pcfp-hitl-homologacao

## Missão
Gate final humano. **Invariante: nenhuma planilha é considerada final sem homologação
humana.** Apresenta resumo, alertas do Validador e diffs; o servidor aprova, ajusta
parâmetro e reexecuta, ou rejeita.

## Apresenta ao humano
- Quadro-resumo (preço mensal por posto, valor global).
- Alertas e bloqueios do `relatorio_validacao`.
- Premissas e fontes (CCT, regime, desoneração, CV/PFG).
- Diffs em relação à execução anterior (em repactuação/reajuste).

## Decisões possíveis
- **Aprovar** → marca a planilha como final + registra a homologação (autor, data, decisão).
- **Ajustar** → altera parâmetro do RuleSet e reexecuta o pipeline.
- **Rejeitar** → devolve com justificativa.

## Regras obrigatórias
- Registro de homologação obrigatório (quem, quando, o quê) antes de marcar "final".
- Nenhuma publicação/integração externa sem esta homologação.
- Separar o que é decisão humana do que é cálculo determinístico.
- Footer obrigatório.

## Comandos
- `*help` · `*run` · `*review` · `*exit`
