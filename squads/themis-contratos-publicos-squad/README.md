# Themis Contratos Públicos

**Nome técnico:** `themis-contratos-publicos-squad`
**Versão:** `1.0.0`

Equipe jurídica de IA para **análise de documentos de contratos administrativos da administração pública brasileira**, com verificação de conformidade fundamentada nas normas e entendimentos usados pela **CGU** (controle interno, integridade e transparência) e pelos **Tribunais de Contas** (TCU e TCEs — legalidade, jurisprudência e riscos ao erário).

> ⚖️ **Ressalva obrigatória:** o squad produz apoio técnico automatizado. Não substitui parecer de advogado, procurador ou órgão de assessoramento jurídico (art. 53 da Lei 14.133/2021). Toda saída exige revisão humana qualificada.

## O que o squad analisa

- Contratos, termos aditivos, apostilamentos e atas de registro de preços.
- Peças de planejamento (ETP, termo de referência, pesquisa de preços) e de seleção (edital, julgamento).
- Justificativas de dispensa e inexigibilidade (arts. 74 e 75 da Lei 14.133/2021).
- Execução e gestão: fiscalização, medições, garantias, sanções e extinção.

## O que ele entrega

| Artefato | Conteúdo |
|---|---|
| Ficha de triagem | tipo de peça, regime legal, metadados, lacunas |
| Checklist de conformidade | cláusulas necessárias (art. 92, Lei 14.133/2021) item a item |
| Relatório de legalidade | apontamentos com lei, artigo e parágrafo |
| Nota de jurisprudência | súmulas/acórdãos TCU aplicáveis, com grau de confiança |
| Relatório de integridade | transparência, CEIS/CNEP, nepotismo, conflito de interesses |
| Matriz de riscos | sobrepreço, jogo de planilha, aditivos, direcionamento — com severidade |
| Parecer consolidado | relatório, fundamentação, quadro de apontamentos, recomendações e conclusão |

## Agentes

- `themis-orchestrator` — coordena o pipeline, consolida achados e aciona quality gates.
- `intake-document-triager` — triagem documental e identificação do regime legal.
- `legalidade-lei14133-analyst` — legalidade formal e material (Lei 14.133/2021 e regimes legados).
- `jurisprudencia-tcu-researcher` — confronto com súmulas e acórdãos do TCU/TCEs.
- `cgu-integridade-compliance-analyst` — integridade, transparência e controle interno (referenciais CGU).
- `riscos-sobrepreco-auditor` — matriz de riscos, sobrepreço e análise de aditivos.
- `parecer-relator-juridico` — parecer técnico-jurídico consolidado.

## Workflows

- `analise_completa_contrato.yaml` — pipeline completo em 9 etapas, 6 quality gates, revisão humana final obrigatória.
- `triagem_rapida_red_flags.yaml` — triagem expressa para priorizar carteiras de contratos.

## Scripts determinísticos (Python 3.11+, sem dependências)

```bash
# pré-triagem heurística de cláusulas necessárias
python3 scripts/checklist_clausulas.py --contrato examples/exemplo_contrato_trecho.txt

# limites legais de termos aditivos (25% / 50%)
python3 scripts/validar_limites_aditivos.py --valor-inicial 480000 --aditivos 90000 40000 --regime 14133
```

## Como ativar

1. Leia `squad.yaml` e assuma a persona `agents/themis-orchestrator.md`.
2. Rode o workflow `analise_completa_contrato` fornecendo os documentos do processo.
3. Aprove cada quality gate e faça a revisão humana final.

Exemplos completos em [`examples/exemplo_uso.md`](examples/exemplo_uso.md). Base normativa em [`docs/base_normativa.md`](docs/base_normativa.md).

## Princípios de qualidade

- Todo apontamento cita norma, súmula ou acórdão; citações de memória são marcadas `a confirmar`.
- Separação explícita entre observado, inferido, hipótese, recomendação e risco.
- Cálculos (percentuais de aditivo) sempre por script determinístico.
- Indício nunca é afirmado como irregularidade consumada.
- Nenhum dado pessoal sensível ou segredo nos artefatos.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
