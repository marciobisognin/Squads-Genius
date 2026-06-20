# Template `vertical:iffar`

Ponto de partida para empacotar squads institucionais brasileiros (jurídico/educacional, especialmente IFFar) como harness. Não é um squad funcional por si só — é o conjunto de personas e convenções que o `harness-doctor-curator` injeta quando o squad de origem é institucional.

## Agentes de referência

| Agente | Função |
|---|---|
| `analista-normativo` | Confere base normativa (leis, instruções normativas, resoluções) citada nos artefatos. |
| `gestor-contratual` | Acompanha cláusulas, prazos e obrigações contratuais. |
| `auditor-evidencias` | Garante que toda afirmação tenha evidência rastreável (documento, página, hash). |
| `redator-institucional` | Padroniza linguagem institucional em português formal. |
| `revisor-lgpd` | Verifica minimização de dados pessoais e retenção conforme LGPD. |

## Como usar

1. Rode `scripts/score_squad_fit.py` no squad institucional de origem.
2. Se o squad for jurídico/educacional, copie os agentes deste template para `output/<squad>/hermes/vertical-iffar/` como complemento — nunca como substituto dos agentes originais do squad.
3. Documente no `SKILL.md` do harness que o template `vertical:iffar` foi aplicado.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
