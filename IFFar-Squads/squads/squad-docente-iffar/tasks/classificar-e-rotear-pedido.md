# Task — Classificar e rotear pedido

## Objetivo
Receber o pedido do docente em linguagem natural e classificá-lo (planejar, gerar
material, avaliar, adaptar, registrar) para roteamento ao(s) agente(s) correto(s).

## Agente responsável
`maestro-pedagogico` (A0)

## Entradas
- Pedido em linguagem natural.
- Contexto de curso, turma e componente curricular.

## Passos
1. Classificar a intenção do pedido (classificador estilo Cynefin).
2. Montar o payload SACP inicial conforme `schemas/sacp_handoff.schema.json`.
3. Definir a rota de agentes a acionar e a ordem de dependência.
4. Encaminhar ao `guardiao-curricular` sempre que houver geração de conteúdo.

## Saídas
- Intenção classificada com justificativa.
- Rota de execução.
- Payload SACP validado por schema.

## Regras
- Pedido ambíguo é sinalizado para esclarecimento — nunca assumido por adivinhação.
- Nenhuma rota pula o Guardião Curricular quando há geração de conteúdo pedagógico.
- Nenhuma rota pula o Gate Humano antes de qualquer saída oficial.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
