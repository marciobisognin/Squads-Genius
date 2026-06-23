# Árgus — Conta Vinculada

> Squad multiagente que automatiza a **Conta-Depósito Vinculada** (Anexo XII da IN SEGES/MPDG
> 05/2017; art. 121 da Lei 14.133/2021) em contratos com dedicação exclusiva de mão de obra
> na administração pública federal. Do contracheque + FGTS Digital à planilha `.xlsx` auditável.

Árgus Panoptes era o gigante de cem olhos que nunca dormia. Aqui, ele vigia cada depósito,
cada provisão e cada liberação da conta bloqueada — com cálculo determinístico e gates humanos.

## O que faz
1. **Parametriza** o contrato (regime tributário, SAT/RAT/FAP, jornada 40/44h, multa 4/5%) — HITL Gate 1.
2. **Extrai** contracheques e o relatório do FGTS Digital (e SEFIP para competências < 03/2024).
3. **Calcula** a provisão mensal (13º 8,33% · férias+1/3 12,10% · multa · incidência 2.2), o saldo
   e as liberações (13º por avos, férias proporcional+1/3, rescisão com multa FGTS 40%/20%).
4. **Confere** o FGTS 8% devido vs recolhido e aplica as regras de negócio (fail-closed).
5. **Gera** a planilha `.xlsx` (5 abas) + relatório de inconsistências — HITL Gate 2.

## Princípios
- **Cálculo determinístico, raciocínio por LLM:** nenhum valor monetário vem de LLM — só da engine Python testável.
- **Rastreabilidade total:** cada rubrica carrega valor, fórmula, percentual, fundamento e fonte.
- **Fail-closed na liberação:** FGTS irregular, documentação incompleta ou justa causa BLOQUEIAM.
- **HITL nos pontos críticos:** parâmetros jurídicos e autorização de liberação são decisões humanas.

## Estrutura
```
argus-conta-vinculada-squad/
├── squad.yaml                 # manifesto (6 agentes, 8 tasks, 3 workflows, 3 scripts)
├── agents/                    # a1..a6 (orquestrador + extrator, regras, engine, validador, gerador)
├── tasks/                     # 01..08 (com HITL Gate 1 e Gate 2)
├── workflows/                 # montagem completa · provisão mensal · liberação por evento
├── scripts/                   # engine + validador + gerador .xlsx (apenas stdlib)
├── templates/                 # schemas dos contratos · estrutura da planilha
├── examples/                  # contrato de exemplo + conferência + planilha .xlsx gerada
└── docs/                      # base normativa · PRD · artefatos da forja
```

## Uso rápido
```bash
# provisão mensal (engine determinística)
python3 scripts/conta_vinculada_core.py --provisao --remuneracao 1620 --regime lucro_real_presumido --sat 1 --multa 4

# do contrato completo à planilha .xlsx
python3 scripts/conta_vinculada_core.py --input examples/exemplo_contrato_limpeza.json > /tmp/consolidado.json
python3 scripts/gerar_planilha_xlsx.py --input /tmp/consolidado.json --output minha_planilha.xlsx --csv

# conferência + regras de liberação (fail-closed)
python3 scripts/validar_conta_vinculada.py --input examples/exemplo_conferencia.json

# testes (golden checks do dossiê)
python3 scripts/conta_vinculada_core.py --self-test
python3 scripts/validar_conta_vinculada.py --self-test
python3 scripts/gerar_planilha_xlsx.py --self-test
```

## Percentuais de referência (item 14 do Anexo XII)
| Rubrica | % | Fonte |
|---|---|---|
| 13º | 8,33% | Anexo XII, item 14 |
| Férias + 1/3 | 12,10% | 9,075% + 3,025% |
| Multa FGTS s/ aviso | **4% (default)** / 5% (literal) | Lei 13.932/2019; Orientação nº 26 |
| Incidência 2.2 | 7,39 / 7,60 / 7,82% | SAT 1/2/3% (= 2.2 × 21,19%) |
| **Total mensal** | **31,82–32,25%** (4%) | Lucro Real/Presumido |

> Simples Nacional: Submódulo 2.2 = só FGTS 8%. Valores são de **partida** — conferir a redação
> vigente e os Cadernos de Logística da SEGES.

## Avisos
Automação **não é parecer jurídico nem contábil**. A multa (4% atual / 5% literal) deve ser
confirmada com a Procuradoria/AGU local. Toda liberação exige conferência sem bloqueios e
autorização humana registrada (responsável + data).

## Integrações
Recebe a remuneração-base e o Submódulo 2.2 do **Squad PCFP**; convive com PROJUR/Farol/Themis
no ciclo de vida do contrato.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
