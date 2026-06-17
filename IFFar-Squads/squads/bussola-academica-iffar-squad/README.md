# 🧭 Bússola Acadêmica IFFar

**Nome técnico:** `bussola-academica-iffar-squad`
**Versão:** `1.0.0`

Squad institucional de apoio ao **ciclo acadêmico** de secretarias e coordenações do Instituto Federal Farroupilha (IFFar): revisão de PPC e matriz curricular, calendário e editais de matrícula/rematrícula, auditoria de integralização curricular, atas de conselho de classe, relatórios de aproveitamento/evasão e consistência dos dados enviados ao **SISTEC** e à **Plataforma Nilo Peçanha**.

> ⚖️ **Ressalva obrigatória:** os artefatos gerados são minutas e relatórios de apoio técnico-administrativo. Toda decisão pedagógica — aprovação de PPC, deferimento de matrícula, fechamento de ata de conselho de classe, envio oficial a SISTEC/PNP — é exclusiva da coordenação, do colegiado e da secretaria acadêmica. Revisão humana é obrigatória em todos os artefatos.

## Problema que resolve

O ciclo acadêmico é hoje conduzido manualmente a cada período letivo, com retrabalho, risco de erro na integralização curricular (pré-requisitos e equivalências verificados "de memória") e respostas lentas a estudantes e famílias. O envio de dados a sistemas federais (SISTEC, Plataforma Nilo Peçanha) é manual e sujeito a inconsistências que só aparecem depois do envio. Este squad automatiza a parte determinística desse trabalho (checagem de regras, detecção de conflitos) e organiza a parte textual (relatórios, minutas), preservando toda decisão pedagógica como humana.

## O que o squad gera

| # | Artefato | Base |
|---|---|---|
| 1 | Relatório de aderência PPC/DCN | DCN aplicável + Catálogo Nacional de Cursos Técnicos |
| 2 | Relatório de integralização curricular | matriz curricular x histórico escolar, por script determinístico |
| 3 | Calendário acadêmico validado | checagem de conflitos de data por script determinístico |
| 4 | Edital de matrícula/rematrícula | Regulamento Didático-Pedagógico vigente |
| 5 | Minuta de ata de conselho de classe | dados de desempenho da turma, deliberação do colegiado |
| 6 | Relatório de aproveitamento/retenção/evasão | indicadores agregados por turma/curso |
| 7 | Checklist de consistência SISTEC/PNP | checagem de campos obrigatórios por script determinístico |

## Agentes (5)

`bussola-orchestrator` · `ppc-dcn-analyst` · `curriculo-integralizacao-auditor` · `atas-editais-redator` · `sistec-pnp-validador`

## Workflows (3)

- `revisao_ppc` — análise de aderência às DCN/catálogo de cursos + aprovação do NDE/colegiado.
- `ciclo_matricula` — calendário → edital → auditoria de integralização → checklist SISTEC/PNP → deferimento humano.
- `fechamento_periodo_letivo` — ata de conselho de classe → relatório de aproveitamento/evasão → checklist SISTEC/PNP → envio humano.

## Scripts determinísticos (Python 3.11+, sem dependências)

```bash
python3 scripts/auditor_integralizacao.py --matriz examples/exemplo_matriz_curricular.json --historico examples/exemplo_historico_aluno.json
python3 scripts/conflito_calendario.py --calendario examples/exemplo_calendario.json
python3 scripts/checklist_sistec_pnp.py --registro examples/exemplo_registro_sistec.json
```

## Como ativar

1. Leia `squad.yaml` e assuma a persona `agents/bussola-orchestrator.md`.
2. Descreva a demanda ou preencha `templates/solicitacao_ciclo_academico.yaml`.
3. Acompanhe o roteamento para o workflow correspondente e responda às perguntas de intake.
4. Aprove os gates humanos quando solicitado — o squad nunca decide em lugar da coordenação, do colegiado ou da secretaria acadêmica.
5. Receba os artefatos consolidados.

Exemplos em [`examples/exemplo_uso.md`](examples/exemplo_uso.md). Fontes e normas em [`docs/base_normativa_academica.md`](docs/base_normativa_academica.md). Para conformidade e prazos institucionais cruzados, ver o squad irmão [`compliance-ia-iffar-squad`](../compliance-ia-iffar-squad/).

## Princípios

- Nenhuma decisão pedagógica é tomada pelo squad: ele prepara, audita e sinaliza — a decisão é sempre humana.
- Regras curriculares (pré-requisito, equivalência, carga horária, conflito de data) são checadas por script determinístico, nunca por inferência do agente.
- Dados pessoais de estudantes tratados com minimização (LGPD): apenas os campos necessários à tarefa.
- Toda fonte normativa citada com versão/data; o que não foi verificado na fonte oficial é marcado `a confirmar`.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
