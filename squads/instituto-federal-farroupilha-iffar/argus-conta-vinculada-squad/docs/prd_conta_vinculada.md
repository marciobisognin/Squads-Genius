# PRD — Squad Árgus (Conta Vinculada)

Implementação do PRD do dossiê "Conta-Depósito Vinculada na Administração Pública Federal"
(jun/2026). Documento-fonte resumido em `docs/base_normativa.md`.

## 1. Objetivo
Dado o tipo de contrato + contracheques + relatório FGTS, gerar automaticamente a planilha
de conta-vinculada em Excel, com os dados dos contratados e todos os campos calculados
(provisão mensal, saldo, liberações), aderente à IN 05/2017 / Lei 14.133.

## 2. Usuários
TAE/fiscal administrativo · gestor de contrato · setor financeiro/orçamento.

## 3. Entradas
Parâmetros do contrato (regime tributário, SAT/RAT/FAP, banco, vigência, jornada 40/44h,
multa 4/5%); contracheques (PDF/imagem); relatório FGTS (FGTS Digital — Relatório por
Trabalhador e/ou extrato para fins rescisórios; extrato SEFIP para competências < 03/2024).

## 4. Arquitetura (orquestrador + 5 agentes)
| Agente | Papel |
|---|---|
| A1 Orquestrador Árgus | controla o fluxo, valida pré-condições, consolida saída e inconsistências |
| A2 Extrator | OCR/parse de contracheque e FGTS → registros normalizados |
| A3 Regras & Parâmetros | percentuais por regime/SAT/jornada/multa; HITL Gate 1 |
| A4 Engine de Cálculo | provisão, saldo, liberações (Python puro determinístico) |
| A5 Validador | confere FGTS/INSS, regras de negócio, bloqueia liberação irregular |
| A6 Gerador de Excel | monta abas, fórmulas, memória e exporta .xlsx |

## 5. Regras de negócio chave
- total mensal = remuneração × (8,33% + 12,10% + [5%|4%] + incidência 2.2 por SAT);
- incidência 2.2 = (34,80%|35,80%|36,80%) × 21,19% (13º a 1/11 + férias+1/3);
- 13º e férias por 1/12 avos (fração ≥ 15 dias = mês cheio);
- multa rescisória 40% (sem justa causa) / 20% (acordo) sobre o saldo do extrato FGTS;
- liberação só com documentação completa e FGTS regular.

## 6. Validações
CPF válido; soma de avos ≤ 12; FGTS recolhido ≥ devido por competência; saldo nunca negativo;
alerta de divergência de remuneração entre contracheque e planilha de custos; consistência de
competências (SEFIP vs FGTS Digital antes/depois de 03/2024).

## 7. Saída
Arquivo .xlsx com as 5 abas + relatório de inconsistências (trabalhadores com FGTS irregular,
divergências de remuneração, pendências documentais que impedem liberação).

## 8. Riscos / observações de implementação
- divergência 5% vs 4% (parametrizar, default 4%);
- jornada e reembolso-creche (Decreto 12.174/2024 + IN 148/2026);
- Simples Nacional (zera encargos de terceiros do 2.2);
- reoneração (Lei 14.973/2024);
- migração SEFIP→FGTS Digital (formatos de extrato distintos).

## 9. Como o squad implementa o PRD
- **Engine** `scripts/conta_vinculada_core.py` cobre §5 com golden tests (`--self-test`).
- **Validador** `scripts/validar_conta_vinculada.py` cobre §6 e o fail-closed de liberação.
- **Gerador** `scripts/gerar_planilha_xlsx.py` cobre §7 (apenas stdlib, .xlsx válido + CSV).
- **Workflows** cobrem os 4 eventos (montagem completa, provisão mensal, liberação por evento).
- **HITL**: Gate 1 (parâmetros jurídicos) e Gate 2 (autorização de liberação).

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
