# Relatório de atualização — Farol 3.0

## Fonte

Documento recebido: `Atualização SQUAD farol _260614_183438.docx`.

## Componentes atualizados

- Manifesto `squad.yaml` atualizado para 3.0.0.
- 12 agentes YAML adicionados.
- Workflow institucional Farol 3.0 criado.
- Base normativa versionada criada.
- Schemas de achados, evidências e casos criados.
- Script `farol_30_contracts.py` criado.
- Testes `test_farol_30_contracts.py` criados.
- README, CHANGELOG, smoke test e relatório de validação atualizados.

## Validações executadas

- `python -m py_compile scripts/*.py`: aprovado.
- `python -m pytest tests -q`: 27 testes aprovados.
- `python scripts/smoke_test.py`: aprovado, incluindo estrutura, compilação e auditoria offline na planilha de exemplo.
- `python scripts/farol_30_contracts.py validate-contracts --root .`: `go_no_go: go`, sem issues.

## Limitações mantidas

- O Farol 3.0 ainda não implementa API FastAPI, PostgreSQL, SSO/RBAC ou painel web institucional.
- A integração semântica por embeddings e a equivalência CATMAT/CATSER completa permanecem como próximas fases.
- Normas foram versionadas como registro operacional inicial; validação jurídica final exige responsável humano.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
