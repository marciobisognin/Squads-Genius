# Task 01 — Triagem e roteamento

**Owner:** `triador`
**Camada:** 0

## Objetivo
Classificar o objeto de conhecimento recebido e emitir o contrato `SACP-IN`, definindo trilhas ativadas (das 7 da Camada 1), nível de profundidade (1/2/3) e o recorte espaço-temporal tentativo.

## Passos
1. Ler o objeto bruto enviado pelo usuário.
2. Classificar em `object_type` (texto sagrado/literário, evento, personalidade, conceito/ideia, lugar, objeto material, processo de longa duração).
3. Identificar os três tempos prováveis (evento/registro/recepção).
4. Selecionar as trilhas pertinentes entre CHRONOS, TERRA, VERBUM, ETHOS, KRATOS, NUMEN, NOÛS — na dúvida, incluir.
5. Marcar `sensitivity_flag` quando o tema tocar religião viva, genocídio, disputa identitária ou política contemporânea.
6. Emitir `SACP-IN` (`templates/sacp-in.schema.json`).

## Critério de aceite
- `SACP-IN` válido contra o schema.
- Toda trilha excluída tem justificativa explícita.
