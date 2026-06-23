# Limitações, premissas e riscos

## Separação epistêmica
- **Observado** (no PRD/Dossiê do usuário): estrutura da planilha (Anexo VII-D),
  ordem de incidência (IN 07/2018), vedação a IRPJ/CSLL, jurisprudência TCU listada,
  variantes CV/PFG, regime dual.
- **Inferido**: mapeamento da arquitetura do PRD para 8 agentes + 8 tasks + 3 workflows.
- **Hipótese**: percentuais default do `RuleSet` (modelo público, regime não desonerado)
  — ilustrativos, não certificados.
- **Recomendação**: confirmar CCT, custos mínimos (IN 176/2024) e enquadramento
  tributário via HITL antes de qualquer uso real.
- **Risco**: usar os defaults sem confirmação CCT/tributária produz planilha incorreta.

## Limitações conhecidas (v1)
- **Fora do escopo:** obras e serviços de engenharia (SINAPI/SICRO), compras de bens,
  serviços sem dedicação exclusiva.
- Os percentuais de **rescisão (Módulo 3)** e **substituição (Módulo 4)** são defaults
  parametrizáveis; o cálculo fino depende de cobertura efetiva e da CCT.
- O **Extractor (LLM)** e o **Classifier (CBO/CCT)** ainda não estão automatizados neste
  repositório — são especificados como agentes; a engine determinística (F1) e o
  esqueleto executável estão entregues e testados.
- A geração de XLSX requer `openpyxl`; sem ele há fallback CSV (sem fórmulas vivas).

## Mitigações (do PRD)
| Risco | Mitigação |
|---|---|
| LLM "calcular" e errar | Matemática 100% em código; LLM só extrai/classifica/redige |
| CCT errada → planilha errada | HITL #1 obrigatório + custos mínimos IN 176/2024 como piso |
| Norma muda (alta cadência) | RAG versionado + flag de vigência + revisão trimestral |
| Desoneração mal aplicada | Cronograma da Lei 14.973/2024 parametrizado e testado |
| Loop infinito de bloqueio | `max_iterations` no Turing loop → escala a HITL |

## Aviso
Este squad é uma ferramenta de apoio. **Não substitui o parecer técnico/jurídico do
servidor responsável.** Toda saída exige homologação humana antes de uso oficial.
