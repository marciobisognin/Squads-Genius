# Task — Consolidar dossiê de conselho de classe

## Objetivo
Consolidar conteúdos lançados e frequência em um dossiê fiel aos dados de origem,
sem qualquer decisão pedagógica automatizada.

## Agente responsável
`registros-conselho-classe` (A6) — agente sensível, dados tratados em ambiente
controlado

## Entradas
- Conteúdos lançados por componente/turma.
- Frequência registrada.
- Histórico da turma.

## Passos
1. Agregar conteúdos e frequência por estudante/turma.
2. Gerar resumo estritamente descritivo por estudante (sem juízo de mérito).
3. Sinalizar lacunas ou inconsistências de dados sem corrigir automaticamente.
4. Montar o dossiê no formato esperado pelo conselho de classe.
5. Enviar ao Gate Humano antes de qualquer uso no conselho.

## Saídas
- Dossiê de conselho de classe.
- Resumo por estudante (somente consolidação).
- Lista de inconsistências detectadas.

## Regras
- O agente não decide aprovação, reprovação ou encaminhamento — apenas consolida.
- Toda lacuna de dado é explicitada no dossiê, nunca preenchida por inferência.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
