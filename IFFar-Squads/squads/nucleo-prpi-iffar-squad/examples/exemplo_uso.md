# Exemplos de uso

## 1. Checklist de campos obrigatórios do edital (sem LLM)

```bash
cd IFFar-Squads/squads/nucleo-prpi-iffar-squad
python3 scripts/checklist_edital_fomento.py --edital examples/exemplo_edital.json
```

Saída: o edital do exemplo (PIBIC) não declara o campo específico `exige_plano_trabalho` — o script deve listar o campo ausente e retornar o gate `edital_aderente_normas` como `bloqueado`.

## 2. Triagem formal de propostas submetidas (sem LLM)

```bash
python3 scripts/triagem_propostas.py \
  --edital examples/exemplo_edital.json \
  --propostas examples/exemplo_propostas.json
```

Saída: a orientadora do exemplo tem 3 propostas, acima do limite de 2 do edital — propostas dela são classificadas como `conflito a resolver`, e uma delas também está `inapta por documentação` por faltar a carta de anuência. O gate `triagem_documental_completa` retorna `bloqueado`.

## 3. Acompanhamento do cronograma de bolsas (sem LLM)

```bash
python3 scripts/cronograma_bolsas.py \
  --bolsas examples/exemplo_bolsas_cronograma.json \
  --data-referencia 2026-06-17
```

Saída: a `BOLSA-2026-002` está com relatório parcial em atraso e a `BOLSA-2026-003` tem relatório próximo do vencimento — o gate `cronograma_bolsas_monitorado` retorna `bloqueado`.

## 4. Consolidação de produção científica (sem LLM)

```bash
python3 scripts/consolidador_producao.py --producao examples/exemplo_producao.json
```

Saída: o artigo do exemplo foi declarado duas vezes com o mesmo DOI (duplicidade) e a patente não tem identificador — o gate `producao_consolidada` retorna `bloqueado`.

## 5. Auditoria de prestação de contas de bolsas (sem LLM)

```bash
python3 scripts/auditoria_prestacao_contas_bolsas.py --bolsas examples/exemplo_bolsas_prestacao_contas.json
```

Saída: uma bolsa tem período coberto pelo relatório divergente da vigência e outra está sem o TCR assinado — o gate `prestacao_contas_auditada` retorna `bloqueado`.

## 6. Ciclo completo com a equipe de agentes (com LLM)

Em uma sessão do Claude Code (ou runtime AIOS compatível):

1. Leia `squad.yaml` e assuma a persona `agents/prpi-orchestrator.md`.
2. Descreva a demanda (edital de fomento, acompanhamento de bolsas ou produção científica/prestação de contas) ou preencha `templates/solicitacao_demanda_prpi.yaml`.
3. O orquestrador roteia para o workflow correspondente (`ciclo_edital_fomento`, `acompanhamento_bolsas` ou `producao_e_prestacao_contas`).
4. Acompanhe os gates — sempre que um gate exigir aprovação humana, a decisão é do comitê de avaliação ou da Pró-Reitoria, nunca do squad.
5. Receba os artefatos: minuta de edital, relatório de triagem de propostas, relatório de cronograma de bolsas, relatório de produção científica, dossiê de prestação de contas de convênio/parceria e/ou relatório de auditoria de prestação de contas de bolsas.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
