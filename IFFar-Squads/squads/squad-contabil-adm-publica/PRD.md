# PRD — Squad Contábil Adm Pública

**Versão:** 1.0.0<br/>
**Autor:** Marcio Bisognin<br/>
**Data:** 16/07/2026<br/>
**Status:** Implementado e validado

## 1. Visão geral

### 1.1 Problema

A conformidade contábil federal depende da análise tempestiva de múltiplas evidências: balancete, razão, demonstrativos, equações e relatórios de inconsistência. O trabalho é altamente sensível à competência, à UG, à vigência normativa e à rastreabilidade. Planilhas desconectadas e análises sem trilha de evidência aumentam o risco de restrições indevidas, regularizações tardias e demonstrações inconsistentes.

### 1.2 Solução

Um squad multiagente com engine Python determinística que:

1. recebe somente dados fornecidos pelo usuário;
2. normaliza e cataloga evidências;
3. detecta inconsistências aritméticas e estruturais;
4. aplica lentes separadas para conformidade e demonstrações;
5. propõe regularização assistida;
6. exige gates do contador;
7. materializa um dossiê auditável.

### 1.3 Não objetivos

- operar o SIAFI;
- produzir lançamento ou comando transacional;
- decidir restrição sem contador;
- certificar demonstrações;
- armazenar documentos reais no GitHub.

## 2. Arquitetura

| ID | Agente | Entrada | Saída |
|---|---|---|---|
| A1 | Orquestrador Contábil | briefing, UG, competência | WorkflowPlan |
| A2 | Curador de Dados SIAFI | exportações e relatórios | CaseInput, EvidenceCatalog |
| A3 | Analista de Conformidade | caso e evidências | ConformityAssessment |
| A4 | Analista de Demonstrações | balancete e demonstrativos | StatementReview |
| A5 | Regularizador Contábil | achados aprovados | RegularizationPlan |
| A6 | Auditor de Evidências | achados e handoffs | EvidenceAudit |
| A7 | Relator para o Contador | estado consolidado | dossiê final |

## 3. Base normativa

- Macrofunção 02.03.15 — Conformidade Contábil;
- Macrofunção 02.03.19 — Demonstrações Contábeis;
- Macrofunção 02.10.06 — Manual de Regularizações Contábeis;
- IN STN nº 6/2007;
- Decreto nº 6.976/2009;
- MCASP vigente.

O squad guarda referências, não procedimentos transacionais congelados. A redação oficial vigente deve ser consultada no caso real.

## 4. Workflows

### 4.1 Conformidade mensal

Intake → evidências → conformidade → demonstrações → triagem → auditoria → relatório → gate do contador.

### 4.2 Regularização assistida

Achado → evidência → classificação → consulta à 02.10.06 → plano proposto → gate do contador → revalidação → relatório.

### 4.3 Encerramento e demonstrações

Intake → demonstrativos → equilíbrio e correlações → conformidade → relatório → gate do contador.

## 5. Modelo de dados

### CaseInput

- `case_id`, `ug`, `competencia`;
- `sources[]` com IDs e origem;
- `accounts[]` com natureza, movimentação, saldo e evidências;
- `equations[]` com dois lados e tolerância;
- `statements` com relações patrimoniais;
- `external_findings[]` importados de relatórios fornecidos;
- `rules` com parâmetros explícitos.

### Finding

- ID, código, severidade e objeto;
- evidências vinculadas;
- referência normativa;
- classe de ação;
- gate humano obrigatório.

### AnalysisOutput

- hash do input;
- erros de validação;
- conclusão proposta;
- decisão final nula;
- achados e contagens;
- plano de regularização não executado.

## 6. Engine determinística

A engine usa `Decimal` para valores monetários e aplica apenas regras declaradas:

- reconciliação do saldo por natureza débito/crédito;
- identificação de saldo negativo/invertido;
- aging quando o caso fornece `max_age_days`;
- diferença entre lados de equações;
- equilíbrio Ativo = Passivo + Patrimônio Líquido;
- importação rastreável de achados externos;
- hash SHA-256 canônico do caso.

Nenhum achado aritmético depende de LLM.

## 7. Stack técnico

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Engine | Python 3.11+ stdlib | determinismo e portabilidade |
| Valores | `decimal.Decimal` | evitar erros binários em moeda |
| Contratos | JSON Schema | handoffs verificáveis |
| Manifesto | YAML | compatibilidade AIOS/OpenSquad |
| Testes | pytest | casos-ouro e regressão |
| Artefatos | JSON, CSV, Markdown | auditoria e interoperabilidade |

## 8. Segurança e governança

- fail-closed;
- zero credenciais;
- minimização de dados pessoais;
- todo achado com evidência;
- máximo de três ciclos de correção;
- gates humanos para regularização e conclusão;
- nenhum campo `transaction_command` preenchido.

## 9. Critérios de aceitação

1. caso limpo produz `sem_restricao_proposta` e zero achados;
2. caso inconsistente detecta reconciliação, saldo invertido, aging, equação, demonstrativo e evidência ausente;
3. todo achado possui referência e gate humano;
4. plano nunca marca ação como executada;
5. CLI gera quatro artefatos válidos;
6. Python compila, pytest passa e validador retorna `go`;
7. ZIP é íntegro e contém README, PRD e manifesto.

## 10. Roadmap

- **F1:** engine e casos-ouro — entregue;
- **F2:** parser CSV parametrizável para layouts institucionais;
- **F3:** catálogo versionado de equações e restrições, alimentado por fonte oficial;
- **F4:** comparação entre competências e aging longitudinal;
- **F5:** painel local e integração controlada com repositório de evidências institucional.

## 11. Riscos e mitigações

| Risco | Impacto | Mitigação |
|---|---|---|
| norma desatualizada | orientação incorreta | consultar fonte oficial e registrar versão |
| evidência incompleta | falso achado | gate fail-closed |
| interpretação automática | invasão de competência | decisão final sempre nula |
| dado pessoal | exposição | minimização e não versionamento |
| regra genérica tratada como norma | falsa precisão | parâmetros explícitos do caso |
| automação transacional | risco institucional | sem credenciais, sem comandos, sem acesso SIAFI |

## 12. Execução

```bash
python3 scripts/contabil_core.py --input examples/caso_com_inconsistencias.json --output-dir generated/demo
python3 -m pytest -q tests
python3 scripts/validate_squad.py --root .
```

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
