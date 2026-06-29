# Task 01 — Investigar (G1)

**Owner:** `G1` (Investigação) · acesso a dados: `bruto`
**Estágio:** 1

## Objetivo
Da pergunta ao Relatório de Síntese verificado, com bibliografia checada e contraditório anti-bajulação.

## Passos
1. `arquiteto-da-questao`: refinar a pergunta → `BriefingDeQuestao`.
2. `cartografo-metodologico`: blueprint metodológico + hierarquia de evidência.
3. `curador-bibliografico`: corpus-primeiro; listar lacunas; buscar o que falta.
4. `verificador-de-fontes`: verificação determinística 4-índices (`scripts/verify_citations.py`).
5. `sintetizador`: Relatório de Síntese anti-vazamento (`[LACUNA DE MATERIAL]` onde faltar).
6. `meta-analista`: agregação quando aplicável.
7. `critico-adversarial`: contraditório pontuado (`scripts/concession_audit.py`).
8. `auditor-de-vieses`: matriz de risco de viés.

## Gates
- 🤖 Verificação 4-índices; hierarquia de evidência; anti-bajulação no contraditório.
- 🧑 Humano confirma pergunta + método.

## Critério de aceite
- Nenhuma fonte `inexistente` usada na síntese (sem override humano registrado).
- Toda afirmação não-fundamentada etiquetada como `[LACUNA DE MATERIAL]`.
- Log de contraditório sem concessão com pontuação < 4.
