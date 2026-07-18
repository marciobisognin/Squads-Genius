# Relatório de Conformidade Contábil — proposta para revisão

- **Caso:** DEMO-COM-INCONSISTENCIAS-001
- **UG:** 158000
- **Competência:** 06/2026
- **Conclusão proposta:** `com_restricao_proposta`
- **Hash do input:** `8ecd0b65cf9fe9fa2fe1dd77747377e8c49f522a315d7d6d4ffdf8a25a178734`

> Este relatório não substitui a certificação do contador responsável e não registra conformidade no SIAFI.

## Achados

### ACH-0001 — Demonstração contábil desequilibrada
- Severidade: `critical`
- Objeto: `demonstracoes:balanco_patrimonial`
- Evidências: DEM-ERR
- Descrição: Ativo difere de passivo mais patrimônio líquido em 100.00.
- Referência: Macrofunção 02.03.19 — Demonstrações Contábeis

### ACH-0002 — Equação contábil desequilibrada
- Severidade: `high`
- Objeto: `equacao:EQ-0042`
- Evidências: CONCONTIR-01
- Descrição: Diferença 50.00 entre os lados da equação EQ-0042.
- Referência: Macrofunção 02.03.15 e regra/equação fornecida pelo caso

### ACH-0003 — Evidência insuficiente
- Severidade: `high`
- Objeto: `CONINCONS:INCONS-001`
- Evidências: CONINCONS-NAO-ANEXADO
- Descrição: Evidências não localizadas: CONINCONS-NAO-ANEXADO
- Referência: Macrofunção 02.03.15 — evidência e qualidade do registro

### ACH-0004 — Evidência insuficiente
- Severidade: `high`
- Objeto: `conta:1.2.3.0.0.00.00`
- Evidências: não vinculadas
- Descrição: Objeto sem evidência vinculada.
- Referência: Macrofunção 02.03.15 — evidência e qualidade do registro

### ACH-0005 — Saldo com sinal incompatível
- Severidade: `high`
- Objeto: `conta:1.1.3.8.1.00.00`
- Evidências: BAL-ERR
- Descrição: A conta de natureza debit apresenta saldo -900.00.
- Referência: Macrofunção 02.10.06 — regularizações contábeis

### ACH-0006 — Saldo não reconciliado
- Severidade: `high`
- Objeto: `conta:1.1.3.8.1.00.00`
- Evidências: BAL-ERR
- Descrição: Saldo informado -900.00 difere do saldo calculado 1100.00.
- Referência: Macrofunção 02.03.15 — qualidade dos registros contábeis

### ACH-0007 — Inconsistência externa
- Severidade: `medium`
- Objeto: `CONINCONS:INCONS-001`
- Evidências: CONINCONS-NAO-ANEXADO
- Descrição: Registro importado de relatório fornecido pelo usuário.
- Referência: Macrofunção 02.03.15 — item a confirmar na redação vigente

### ACH-0008 — Saldo acima do prazo de análise informado
- Severidade: `medium`
- Objeto: `conta:1.1.3.8.1.00.00`
- Evidências: BAL-ERR
- Descrição: Permanência de 120 dias supera o limite parametrizado de 30 dias.
- Referência: Macrofunção 02.10.06 — regularizações contábeis; parâmetro do caso

## Aprovação

**Contador responsável:** ____________________

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
