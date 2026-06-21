# Task 05 — Finalizar (G2)

**Owner:** `G2` (formatação/divulgação)
**Estágio:** 5

## Objetivo
Gerar o artefato publicável e a Declaração de Uso de IA, com gate terminal de recusa.

## Passos
1. (opt-in) Se `SCR_CLAIM_AUDIT=1`: auditoria de fidelidade por citação (LLM-como-juiz).
2. `conformador-de-citacoes`: bibliografia final no estilo do venue.
3. Exportar: Markdown; DOCX (Pandoc); LaTeX/Typst; PDF (Tectonic).
4. `sentinela-de-conformidade`: Declaração de Uso de IA conforme o venue.

## Gate terminal
- O formatador **recusa** qualquer saída com alegação não-sustentada pendente.

## Critério de aceite
- Artefato gerado no(s) formato(s) escolhido(s) pelo humano.
- Nenhuma alegação não-sustentada pendente; Declaração de IA presente.
