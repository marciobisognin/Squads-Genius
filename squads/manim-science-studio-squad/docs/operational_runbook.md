# Runbook Operacional

## Execução local

```bash
python scripts/manim_studio_pipeline.py --briefing examples/briefing_heisenberg.json --output output/heisenberg --package
```

## Validação

```bash
python -m pytest -q
python scripts/validate_squad.py --root .
```

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
