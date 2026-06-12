# Exemplos de uso

## 1. Verificar suficiência da solicitação (sem LLM)

```bash
cd squads/hefesto-forja-licitatoria-squad
python3 scripts/intake_suficiencia.py --solicitacao examples/exemplo_solicitacao_pregao.json
```

Saída: gate `liberado`/`bloqueado` com a lista de perguntas pendentes que o agente de intake faria ao usuário.

## 2. Estatísticas da pesquisa de preços (sem LLM)

```bash
python3 scripts/analise_pesquisa_precos.py --planilha examples/exemplo_cotacoes.csv
```

Saída: média, mediana, menor preço, coeficiente de variação e outliers por item (a cotação de R$ 4.980,00 do exemplo deve ser sinalizada).

## 3. Índice do dossiê (sem LLM)

```bash
python3 scripts/montar_dossie.py --pasta <pasta-do-processo> --fluxo licitacao
```

## 4. Forja completa com a equipe de agentes (com LLM)

Em uma sessão do Claude Code (ou runtime AIOS compatível):

1. Leia `squad.yaml` e assuma a persona `agents/hefesto-orchestrator.md`.
2. Entregue a solicitação preenchida (`templates/solicitacao_contratacao.yaml`) e os documentos disponíveis.
3. O `intake-requisitos-clarifier` fará as perguntas sobre o que faltar — responda para liberar a forja.
4. Acompanhe os gates do workflow `processo_licitacao_completo` (ou `contratacao_direta`).
5. Receba o dossiê: DFD, ETP, pesquisa de preços com planilha, matriz de riscos, TR, edital + anexos, minuta de contrato e nota de conformidade.
6. Handoff humano: adapte aos modelos oficiais AGU/CNMLC vigentes, envie à assessoria jurídica e à autoridade competente.

## 5. Voltando com mais informações

Se a forja pausou por falta de dados, use o workflow `complementar_informacoes` entregando as respostas — o squad atualiza só os artefatos impactados.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
