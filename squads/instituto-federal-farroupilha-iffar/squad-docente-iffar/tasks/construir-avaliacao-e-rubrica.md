# Task — Construir avaliação e rubrica

## Objetivo
Elaborar instrumentos de avaliação e rubricas mapeados às competências do
componente, atualizando o banco de itens do curso.

## Agentes responsáveis
`avaliador-rubricas` (A4) com validação de `guardiao-curricular` (A1)

## Entradas
- Objetivos de aprendizagem do Plano de Ensino.
- Conteúdo efetivamente trabalhado.
- Banco de itens existente do curso.

## Passos
1. Mapear cada item de avaliação a um objetivo de aprendizagem específico.
2. Construir a rubrica com critérios observáveis e níveis de desempenho.
3. Gerar roteiro de feedback formativo associado.
4. Atualizar o banco de itens versionado por curso, evitando duplicidade.
5. Validar contra `schemas/avaliacao_rubrica.schema.json`.

## Saídas
- Instrumento de avaliação.
- Rubrica com critérios e níveis.
- Banco de itens atualizado.

## Regras
- Item sem objetivo de aprendizagem mapeado é sinalizado, não incluído no banco.
- Avaliação não inclui critério de aprovação/reprovação institucional — isso é
  decisão humana.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
