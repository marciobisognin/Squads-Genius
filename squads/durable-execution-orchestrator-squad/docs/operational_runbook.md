# Runbook Operacional

## Execução local

```bash
python scripts/durable_orchestrator.py run-example --workdir output/demo
```

## Recuperação após interrupção

1. Reutilize o mesmo arquivo SQLite.
2. Consulte o status da instância.
3. Execute novamente `run` para retomar do último checkpoint persistido.

## Aprovação humana

```bash
python scripts/durable_orchestrator.py signal --db output/demo/orchestrator.db --instance <INSTANCE_ID> --type approval --payload '{"approved": true}'
```

## Cancelamento com compensação

```bash
python scripts/durable_orchestrator.py cancel --db output/demo/orchestrator.db --instance <INSTANCE_ID>
```

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
