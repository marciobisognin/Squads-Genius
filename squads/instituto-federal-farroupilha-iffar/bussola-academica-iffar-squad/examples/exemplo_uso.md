# Exemplos de uso

## 1. Auditoria de integralização curricular (sem LLM)

```bash
cd IFFar-Squads/squads/bussola-academica-iffar-squad
python3 scripts/auditor_integralizacao.py \
  --matriz examples/exemplo_matriz_curricular.json \
  --historico examples/exemplo_historico_aluno.json
```

Saída: o aluno do exemplo está cursando `PROG2` sem ter `PROG1` aprovado — o script deve sinalizar `pre_requisitos_nao_satisfeitos` e o gate `pendencia_bloqueante`.

## 2. Conflito de calendário acadêmico (sem LLM)

```bash
python3 scripts/conflito_calendario.py --calendario examples/exemplo_calendario.json
```

Saída: o período de matrícula do exemplo se sobrepõe ao recesso de janeiro — o script deve listar o conflito e retornar o gate `calendario_sem_conflito` como `bloqueado`.

## 3. Checklist de consistência SISTEC/PNP (sem LLM)

```bash
python3 scripts/checklist_sistec_pnp.py --registro examples/exemplo_registro_sistec.json
```

Saída: o registro do exemplo está marcado como `concluinte` sem `data_conclusao` e com carga horária cursada (240h) menor que a da matriz de referência (320h) — ambas as divergências devem ser listadas.

## 4. Ciclo completo com a equipe de agentes (com LLM)

Em uma sessão do Claude Code (ou runtime AIOS compatível):

1. Leia `squad.yaml` e assuma a persona `agents/bussola-orchestrator.md`.
2. Descreva a demanda (revisão de PPC, ciclo de matrícula ou fechamento de período letivo) ou preencha `templates/solicitacao_ciclo_academico.yaml`.
3. O orquestrador roteia para o workflow correspondente (`revisao_ppc`, `ciclo_matricula` ou `fechamento_periodo_letivo`).
4. Acompanhe os gates — sempre que um gate exigir aprovação humana, a decisão é da coordenação, do colegiado ou da secretaria acadêmica, nunca do squad.
5. Receba os artefatos: relatório de aderência PPC/DCN, relatório de integralização, calendário e edital de matrícula, minuta de ata de conselho de classe, relatório de aproveitamento/evasão e/ou checklist SISTEC/PNP.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
