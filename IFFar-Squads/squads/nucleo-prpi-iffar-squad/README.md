# 🔬 Núcleo PRPI IFFar

**Nome técnico:** `nucleo-prpi-iffar-squad`
**Versão:** `1.0.0`

Squad institucional de apoio à **Pró-Reitoria/Diretoria de Pesquisa, Pós-Graduação e Extensão (PRPI)** do Instituto Federal Farroupilha (IFFar): elaboração de editais internos de fomento (PIBIC, PIBITI, PIBID, extensão), triagem formal de propostas submetidas, acompanhamento do cronograma de bolsas concedidas, consolidação de relatórios de produção científica/técnica e apoio à prestação de contas de bolsas e de convênios/parcerias de extensão.

> ⚖️ **Ressalva obrigatória:** os artefatos gerados são minutas e relatórios de apoio técnico-administrativo. Mérito científico/técnico de propostas, aprovação de edital e decisões de concessão ou corte de bolsa são exclusivos dos comitês de avaliação e da Pró-Reitoria. Revisão humana é obrigatória em todos os artefatos.

## Problema que resolve

A elaboração de editais de fomento e a triagem de propostas hoje dependem de verificação manual de documentação, enquadramento e limite de bolsas por orientador — processo sujeito a inconsistências e retrabalho. O acompanhamento do cronograma de bolsas (mensalidades, relatórios, TCR) e a prestação de contas de bolsas e convênios são feitos sem alerta sistemático de prazos, gerando descumprimentos que só aparecem tarde. A consolidação da produção científica/técnica para Lattes, SUAP, relatório de gestão e Plataforma Nilo Peçanha é manual e propensa a duplicidades. Este squad automatiza a parte determinística desse trabalho (checklists, triagem documental, monitoramento de prazos, deduplicação) e organiza a parte textual (editais, relatórios, dossiês), preservando toda decisão de mérito e toda decisão administrativa sensível como humana.

## O que o squad gera

| # | Artefato | Base |
|---|---|---|
| 1 | Relatório de intake da demanda PRPI | tipo de demanda, documentos disponíveis, lacunas |
| 2 | Minuta de edital interno de fomento | checklist de campos obrigatórios por script determinístico |
| 3 | Relatório de triagem de propostas submetidas | documentação, enquadramento e limite de bolsas por script determinístico |
| 4 | Relatório de cronograma de bolsas | mensalidades, relatórios e TCR comparados à data de referência |
| 5 | Relatório de produção científica/técnica consolidado | produção declarada (Lattes/SUAP), deduplicada por script determinístico |
| 6 | Dossiê de prestação de contas de convênio/parceria de extensão | plano de aplicação aprovado x comprovantes declarados |
| 7 | Relatório de auditoria de prestação de contas de bolsas | documentos exigidos x entregues, vigência x período coberto |

## Agentes (5)

`prpi-orchestrator` · `triagem-propostas-fomento` · `cronograma-bolsas-acompanhador` · `producao-cientifica-redator` · `prestacao-contas-fomento-auditor`

## Workflows (3)

- `ciclo_edital_fomento` — intake → elaboração do edital → aprovação humana → triagem das propostas → avaliação de mérito pelo comitê.
- `acompanhamento_bolsas` — intake → cronograma de bolsas → auditoria de prestação de contas → decisão humana da coordenação.
- `producao_e_prestacao_contas` — intake → consolidação da produção científica → dossiê de prestação de contas de convênio/parceria → validação humana final.

## Scripts determinísticos (Python 3.11+, sem dependências)

```bash
python3 scripts/checklist_edital_fomento.py --edital examples/exemplo_edital.json
python3 scripts/triagem_propostas.py --edital examples/exemplo_edital.json --propostas examples/exemplo_propostas.json
python3 scripts/cronograma_bolsas.py --bolsas examples/exemplo_bolsas_cronograma.json --data-referencia 2026-06-17
python3 scripts/consolidador_producao.py --producao examples/exemplo_producao.json
python3 scripts/auditoria_prestacao_contas_bolsas.py --bolsas examples/exemplo_bolsas_prestacao_contas.json
```

## Como ativar

1. Leia `squad.yaml` e assuma a persona `agents/prpi-orchestrator.md`.
2. Descreva a demanda ou preencha `templates/solicitacao_demanda_prpi.yaml`.
3. Acompanhe o roteamento para o workflow correspondente e responda às perguntas de intake.
4. Aprove os gates humanos quando solicitado — o squad nunca decide em lugar do comitê de avaliação ou da Pró-Reitoria.
5. Receba os artefatos consolidados.

Exemplos em [`examples/exemplo_uso.md`](examples/exemplo_uso.md). Fontes e normas em [`docs/base_normativa_prpi.md`](docs/base_normativa_prpi.md). Para conformidade e prazos institucionais cruzados, ver o squad irmão [`compliance-ia-iffar-squad`](../compliance-ia-iffar-squad/).

## Princípios

- Nenhuma decisão de mérito científico, aprovação de edital ou concessão/corte de bolsa é tomada pelo squad: ele prepara, audita e sinaliza — a decisão é sempre humana.
- Triagem de propostas é estritamente formal (documentação, enquadramento, conflitos) e checada por script determinístico, nunca por inferência do agente.
- Dados pessoais de bolsistas, orientadores e pesquisadores tratados com minimização (LGPD): apenas os campos necessários à tarefa.
- Toda fonte normativa citada com versão/data; o que não foi verificado na fonte oficial é marcado `a confirmar`.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
