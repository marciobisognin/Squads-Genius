# ⚒️ Hefesto Forja Licitatória

**Nome técnico:** `hefesto-forja-licitatoria-squad`
**Versão:** `1.0.0` | **Tier:** Premium

Squad que transforma a **documentação inicial do órgão** em um **processo de licitação completo**, na modalidade solicitada (pregão, concorrência, diálogo competitivo, leilão, concurso, dispensa ou inexigibilidade), gerando todos os artefatos da fase preparatória e os instrumentos do certame — com base na **Lei 14.133/2021**, na estrutura dos **modelos oficiais da AGU/CNMLC** e nas **INs SEGES** e referenciais da **CGU**.

> ⚖️ **Ressalva obrigatória:** os artefatos são minutas de apoio técnico. Na esfera federal, os modelos AGU/CNMLC são de uso obrigatório ou exigem justificativa (art. 19, IV). O processo real exige parecer jurídico (art. 53) e autorização da autoridade competente. Revisão humana obrigatória.

## Diferencial premium: intake que pergunta

O agente **`intake-requisitos-clarifier`** é um gate bloqueante: ele inventaria o que você entregou, roda uma checagem determinística de campos por modalidade e — se faltar informação essencial — **devolve perguntas numeradas, com o motivo legal de cada uma, e pausa a forja até você responder**. Nada é inventado: lacuna vira pergunta ou premissa explícita confirmada por você.

## O que o squad gera (dossiê completo)

| # | Artefato | Base |
|---|---|---|
| 1 | Relatório de intake | suficiência documental |
| 2 | Nota de enquadramento | modalidade/rito — arts. 28-33, 74-75 |
| 3 | DFD | Decreto 10.947/2022 |
| 4 | ETP | art. 18, §1º + IN SEGES 58/2022 |
| 5 | Pesquisa de preços + planilha CSV | art. 23 + IN SEGES 65/2021, estatísticas por script |
| 6 | Matriz de riscos | art. 22 + IN Conjunta MP/CGU 01/2016 |
| 7 | Termo de referência | art. 6º, XXIII, estrutura AGU/CNMLC |
| 8 | Edital + anexos (ou aviso de contratação direta) | art. 25 (ou art. 72) |
| 9 | Minuta de contrato | art. 92, cláusula a cláusula com refs |
| 10 | Nota de conformidade + dossiê indexado | checklists e coerência cruzada |

## Agentes (9)

`hefesto-orchestrator` · `intake-requisitos-clarifier` · `enquadramento-modalidade-strategist` · `planejamento-dfd-etp-architect` · `termo-referencia-writer` · `pesquisa-precos-planilhista` · `matriz-riscos-engineer` · `edital-minutas-redator` · `conformidade-dossie-auditor`

## Workflows (3)

- `processo_licitacao_completo` — 11 etapas, 6 gates, handoff humano final.
- `contratacao_direta` — dispensa/inexigibilidade com a documentação do art. 72.
- `complementar_informacoes` — ciclo curto quando o usuário retorna com respostas.

## Scripts determinísticos (Python 3.11+, sem dependências)

```bash
python3 scripts/intake_suficiencia.py --solicitacao examples/exemplo_solicitacao_pregao.json
python3 scripts/analise_pesquisa_precos.py --planilha examples/exemplo_cotacoes.csv
python3 scripts/montar_dossie.py --pasta <pasta-do-processo> --fluxo licitacao
```

## Como ativar

1. Leia `squad.yaml` e assuma a persona `agents/hefesto-orchestrator.md`.
2. Preencha `templates/solicitacao_contratacao.yaml` (ou descreva livremente) e entregue os documentos que tiver.
3. Responda às perguntas do intake e aprove os gates.
4. Receba o dossiê e siga o handoff humano (modelos oficiais AGU → jurídico → autoridade).

Exemplos em [`examples/exemplo_uso.md`](examples/exemplo_uso.md). Fontes e normas em [`docs/base_normativa_e_modelos.md`](docs/base_normativa_e_modelos.md). Para revisão jurídica cruzada do resultado, use o squad irmão [`themis-contratos-publicos-squad`](../themis-contratos-publicos-squad/).

## Princípios

- Informação faltante NUNCA é inventada: o intake pergunta.
- Decisões do órgão são marcadas `[[DECISÃO DO ÓRGÃO]]`, nunca tomadas pela forja.
- Cálculos de preço sempre por script determinístico.
- Estrutura dos modelos oficiais, sem cópia literal; tudo `a confirmar` é listado na nota de conformidade.
- Consistência cruzada de objeto, valores e prazos em todos os artefatos.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
