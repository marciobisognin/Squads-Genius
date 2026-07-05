# Quality Gates — Bifröst Forge Engine

A forja só avança quando cada gate passa. Gates reprovados acionam rollback ao último
ponto aprovado (registrado no Saga Ledger).

| Gate | O que verifica | Responsável |
|---|---|---|
| `briefing` | Campos obrigatórios, lacunas por severidade, sem bloqueadores | Mímir Briefing Oracle |
| `research` | Fontes presentes, separação observado/inferido | Huginn & Muninn |
| `design` | Paleta/tokens originais, sem ativos de marca | Eitri Design Forge |
| `squad_architecture` | Roster não-redundante, matriz sem sobreposição | Valkyrie Agent Marshal |
| `scripts` | Todo `.py` compila, teste mínimo presente | Brokkr Script Smith |
| `traceability` | Cada output esperado ↔ artefato produzido (≥ 80%) | Heimdall |
| `determinism` | Dois hashes de árvore idênticos + ledger íntegro | Heimdall |
| `publication` | Sem segredos, autorização humana registrada | Bifröst Release Herald |

## Rubrica de nota (Heimdall)
`score = média(structure, manifest, safety, traceability)`; veredito:
- `go` — sem problemas e `score ≥ 80`;
- `go-with-human-review` — sem problemas bloqueantes, revisão recomendada;
- `no-go` — problemas estruturais/segurança presentes.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
