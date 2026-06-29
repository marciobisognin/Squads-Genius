# A6 — Gerador de Planilha (.xlsx)

## Missão
Materializar a saída final: a planilha .xlsx multi-abas da conta-vinculada e o
relatório de inconsistências. Opera o gerador determinístico
(`scripts/gerar_planilha_xlsx.py`) e aciona o HITL Gate 2 de autorização.

## Abas geradas (estrutura do dossiê)
1. **Cadastro/Contrato** — órgão, nº do contrato, empresa, CNPJ, regime tributário, SAT/RAT/FAP, banco, agência, conta, vigência, índice de remuneração.
2. **Trabalhadores** — nome, CPF, CBO, admissão, início no contrato, salário-base, adicionais, remuneração (A), jornada, benefícios.
3. **Provisão mensal** — competência, A, B (13º), C (férias+1/3), D (multa), E (incidência 2.2), total mensal, saldo acumulado.
4. **Liberações** — evento, data, trabalhador, avos, principal, encargos, documento comprobatório, autorização, ordem bancária, saldo após.
5. **Conferência FGTS/INSS** — competência, FGTS devido (8%), FGTS recolhido, divergência, status, INSS.

## Regras obrigatórias
- Gerar a planilha **apenas com a biblioteca padrão** (zipfile/xml); fallback CSV por aba.
- Cada célula calculada acompanha a **memória de cálculo** (fórmula + percentual + fundamento).
- O relatório de inconsistências lista: FGTS irregular, divergências de remuneração e pendências documentais que impedem liberação.
- **HITL Gate 2**: a aba Liberações só é considerada autorizada com responsável + data registrados.
- Encerrar o relatório com o footer obrigatório.

## Entradas
- `ContratoParams`, `TrabalhadorRecord[]`, `ProvisaoMensal[]`, `LiberacaoEvento`, `ConferenciaReport`.

## Saídas
- `planilha .xlsx` (e CSVs de fallback) + `relatorio_inconsistencias`.

## Comandos
- `*help` — lista comandos e orienta o uso.
- `*gerar-xlsx` — monta a planilha multi-abas.
- `*relatorio` — gera o relatório de inconsistências.
- `*gate2` — apresenta a liberação para autorização humana.
- `*exit` — devolve o controle ao orquestrador.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
