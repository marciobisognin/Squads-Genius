# Task — Adaptar para AEE / inclusão

## Objetivo
Adaptar material ou avaliação conforme a Resolução CONSUP 52/2019, preservando o
objetivo de aprendizagem original.

## Agente responsável
`agente-inclusao-aee` (A5) — agente sensível, dados tratados em ambiente controlado

## Entradas
- Material ou avaliação base.
- Perfil de necessidade educacional específica (sem laudo/diagnóstico).
- Parecer do NAPNE/CAI, quando exigido pela norma.

## Passos
1. Analisar o material base frente ao perfil informado.
2. Classificar a necessidade como adaptação de pequeno ou grande porte, citando o
   dispositivo da Res. CONSUP 52/2019.
3. Articular com NAPNE/CAI quando a norma exigir parecer especializado.
4. Produzir a versão adaptada e o registro de flexibilização para o Plano de Ensino.
5. Validar contra `schemas/adaptacao_aee.schema.json`.

## Saídas
- Versão adaptada do material/avaliação.
- Registro de flexibilização.
- Sinalização de parecer pendente, se aplicável.

## Regras
- O agente nunca infere diagnóstico — trabalha apenas com o perfil de necessidade
  informado.
- Toda adaptação de grande porte sem parecer NAPNE/CAI fica pendente de
  homologação especializada antes do Gate Humano.
- Dado de saúde/laudo não é persistido pelo agente.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
