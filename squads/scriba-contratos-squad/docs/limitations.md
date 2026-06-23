# Limitações, premissas e riscos

## Separação epistêmica
- **Observado** (no PRD/Compêndio do usuário): os quatro instrumentos contratuais
  (minuta inicial, termo aditivo, apostilamento, repactuação/reajuste), a tabela-decisão
  do Instrument Router (§11), as fórmulas de reajuste/repactuação/limites de aditivo,
  o regime dual (Lei 14.133/2021 + IN 05/2017) e a jurisprudência TCU listada.
- **Inferido**: mapeamento da arquitetura do PRD para 11 agentes + 11 tasks + 4 workflows.
- **Hipótese**: estrutura do catálogo de minutas AGU/CNMLC referenciada pelo
  Template Selector — ainda não implementada nesta versão (placeholder de arquitetura).
- **Recomendação**: confirmar vigência da minuta selecionada e a fundamentação de
  cada cláusula via HITL Gate A/B antes de qualquer uso real.
- **Risco**: usar a tabela-decisão ou os cálculos sem revisão jurídica humana pode
  gerar instrumento incompatível com o caso concreto.

## Limitações conhecidas (v1)
- **Fora do escopo:** obras e serviços de engenharia, compras de bens, contratações
  sem dedicação exclusiva de mão de obra (quando aplicável à conta vinculada/PFG).
- O **Extractor (LLM)**, o **Normative RAG (LLM+RAG)**, o **Template Selector**, o
  **Drafter**, o **Doc Generator** e o **Explainer** ainda não estão automatizados
  neste repositório — são especificados como agentes; o núcleo determinístico
  (Router + Engine + Validator, F1) está entregue e testado (21 casos-ouro).
- A geração de DOCX depende de biblioteca externa (`python-docx`); sem ela, a
  saída cai para Markdown.
- O catálogo de minutas AGU/CNMLC vigentes não está embarcado nesta versão —
  é referenciado como integração futura com fonte oficial.

## Mitigações (do PRD)
| Risco | Mitigação |
|---|---|
| LLM "calcular" e errar | Matemática 100% em código (`scriba_engine.py`); LLM só extrai/redige |
| Instrumento errado (aditivo × apostila) | Tabela-decisão determinística + HITL Gate A |
| Cláusula sem fundamento | Validator bloqueia cláusula sem `fundamento` preenchido |
| Preclusão de repactuação não detectada | Alerta crítico embarcado na engine (art. 57, §7º IN 05/2017) |
| Loop infinito de bloqueio | `max_iterations` no Turing loop → escala ao HITL Gate B |
| Minuta desatualizada | Guarda de vigência no Template Selector (futuro) |

## Aviso
Este squad é uma ferramenta de apoio. **Não substitui o parecer jurídico da
procuradoria/CLCFW responsável.** Toda peça contratual exige homologação humana
(HITL Gate B) antes de uso oficial.
