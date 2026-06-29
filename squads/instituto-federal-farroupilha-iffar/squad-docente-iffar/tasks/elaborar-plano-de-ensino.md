# Task — Elaborar Plano de Ensino

## Objetivo
Montar o rascunho do Plano de Ensino do componente curricular, cruzado com o
calendário acadêmico, e validado contra o PPC/RDP.

## Agentes responsáveis
`planejador-de-ensino` (A2) com validação de `guardiao-curricular` (A1)

## Entradas
- Ementa do componente curricular.
- Calendário acadêmico do semestre/campus.
- Base normativa do PPC/RDP do curso.

## Passos
1. Estruturar o plano: ementa → objetivos → metodologia → conteúdo programático →
   avaliação → referências.
2. Executar `scripts/build_cronograma.py` para distribuir o conteúdo nas aulas do
   semestre, respeitando dias letivos e datas de conselho de classe.
3. Enviar o rascunho ao Guardião Curricular para veredito de aderência ao PPC/RDP.
4. Sanear apontamentos do veredito antes de enviar ao Gate Humano.
5. Validar o plano final contra `schemas/plano_ensino.schema.json`.

## Saídas
- Plano de Ensino em rascunho, estruturado.
- Cronograma de aulas distribuído no semestre.
- Veredito de aderência do Guardião Curricular.

## Regras
- Conflito entre carga horária e calendário disponível é sinalizado, nunca ajustado
  silenciosamente.
- Plano só segue para lançamento institucional após homologação no Gate Humano.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
