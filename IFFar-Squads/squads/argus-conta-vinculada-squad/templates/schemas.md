# Schemas dos contratos (handoffs entre agentes)

Os agentes trocam dados por JSON validado. Abaixo, a forma mínima de cada contrato.

## ContratoParams (A3 → A4)
```json
{
  "regime": "lucro_real_presumido | simples_nacional",
  "sat": "1 | 2 | 3",
  "fap": "1.0",
  "multa_modo": "atual | literal",
  "jornada": 40,
  "vigencia": "AAAA-MM-DD a AAAA-MM-DD",
  "fonte_percentuais": "Caderno de Logística 2018 / item 14 Anexo XII",
  "decidido_por": "responsável (HITL Gate 1)"
}
```

## TrabalhadorRecord (A2 → A4)
```json
{
  "nome": "string", "cpf": "000.000.000-00", "cbo": "0000-00",
  "admissao": "AAAA-MM-DD", "inicio_contrato": "AAAA-MM-DD",
  "salario_base": "0.00", "adicionais": "0.00", "remuneracao": "0.00",
  "competencia": "AAAA-MM", "jornada": 40,
  "confianca": "alta | media | baixa", "campos_ilegiveis": []
}
```

## FgtsRecord (A2 → A5)
```json
{
  "cpf": "000.000.000-00", "origem": "fgts_digital | sefip",
  "competencias": [{"competencia": "AAAA-MM", "deposito": "0.00", "status": "regular | irregular"}],
  "saldo": "0.00", "valor_base_rescisorio": "0.00"
}
```

## ProvisaoMensal (A4 → A6)
```json
{
  "remuneracao": "0.00", "regime": "...", "sat": "1", "fap": "1.0",
  "rubricas": [{"nome": "...", "valor": "0.00", "percentual": "0.0833", "formula": "...", "fundamento": "..."}],
  "total_mensal": "0.00", "percentual_total": "0.318035"
}
```

## LiberacaoEvento (A4 → A5/A6)
```json
{"evento": "13º | férias | rescisão | encerramento", "avos": 12,
 "principal": "0.00", "encargos": "0.00", "total": "0.00", "fonte_saldo": "extrato FGTS"}
```

## ConferenciaReport (A5 → A6)
```json
{"competencia": "AAAA-MM", "responsavel_validacao": "string",
 "por_trabalhador": [{"cpf": "...", "evento": "...", "libera": true, "bloqueios": []}],
 "go_no_go": "go | no-go", "total_bloqueados": 0}
```

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
