# Forja de Empresas — Asgard Company Forge

Se o Bifröst forja **squads**, a Asgard Company Forge forja **organizações**.

## O que gera
De um briefing de negócio (`company_name`, `mission`, `market`, `offer`, `size`,
`departments?`), deriva deterministicamente:
- **Organograma**: direção (Allfather) → chefias de departamento → especialistas.
- **Funcionários como agentes**: cada um com cargo, `reports_to` e contrato I/O.
- **Departamentos**: um YAML por departamento.
- **Governança**: cadeia de comando e gates (missão, contratos, segurança, aprovação humana).

## Porte (`size`) → estrutura
| size | departamentos | pessoas por depto |
|---|---|---|
| small | 3 | 1 |
| medium | 4 | 2 |
| large | 5 | 3 |

## Uso
```bash
python3 scripts/asgard_company_forge.py --briefing examples/company_briefing_valhalla_ventures.yaml --output ./empresa --overwrite --verify-determinism
# injetando uma mente da biblioteca
python3 scripts/asgard_company_forge.py --briefing empresa.yaml --output ./empresa --overwrite --mind dna/voz-institucional.yaml
```

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
