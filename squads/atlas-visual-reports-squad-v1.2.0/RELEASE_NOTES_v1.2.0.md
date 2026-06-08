# Release Notes — Atlas Visual Reports Squad v1.2.0

## Base
Evolução operacional do BRD `BRD_squad_design_relatorios_premium.md`.

## Principais melhorias
- Contratos JSON entre agentes.
- Templates separados em três camadas: executive, analytical e appendix.
- Scripts separados para HTML, PDF e validação.
- CSS premium print-safe com `@page`, grids adaptativos e prevenção de estouro.
- Smoke test v1.2 com geração real de HTML + PDF.
- BRD preservado em `references/prd/` e como `BRD.md`.

## Critério de aceite
A versão só é considerada pronta quando `validate_squad.py`, `smoke_test.py`, `qpdf --check` e renderização `mutool` passam.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
