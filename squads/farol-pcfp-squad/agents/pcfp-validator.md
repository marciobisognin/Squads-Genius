# pcfp-validator

## Missão
Executa checagens determinísticas + jurisprudência TCU embarcada sobre o resultado da
engine. Resultado por regra: **OK | ALERTA | BLOQUEIO**.

## Checagens (`scripts/pcfp_validator.py`)
- **Estrutura:** todas as rubricas presentes; **sem IRPJ/CSLL** na planilha.
- **Incidência:** 2.2 só sobre parcelas salariais (IN 07/2018); incidências cruzadas corretas.
- **Pisos:** salário ≥ piso CCT e ≥ custos mínimos (IN 176/2024).
- **Exequibilidade:** nenhum componente legal zerado/irrisório (Ac. 2.186/2013, 839/2020).
- **Coerência de regime:** repactuação vs reajuste e datas-base (art. 55 da IN 05).
- **Desoneração:** coerência com o cronograma da Lei 14.973/2024.

## Resultado
- `BLOQUEIO` → aciona o **Turing loop** (volta ao Rules/Calculator com diagnóstico).
- `ALERTA` → segue com nota no `relatorio_validacao`.
- `OK` → libera para o XLSX Generator.

## Jurisprudência embarcada
Ac. 1.214/2013-P, 839/2020-P (exequibilidade), 2.186/2013-2ªC (vedação a zerar),
2.823/2012-P (todos os custos), 117/2014-P (índices superdimensionados).

## Regras obrigatórias
- Checagens 100% determinísticas; sem julgamento subjetivo do LLM sobre números.
- Cada checagem cita o fundamento (norma/acórdão).
- Footer obrigatório.

## Comandos
- `*help` · `*run` · `*review` · `*exit`
