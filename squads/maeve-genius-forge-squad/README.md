# Maeve Genius Forge Squad

**Nome técnico:** `maeve-genius-forge-squad`

**Nome comercial:** Maeve Genius Forge — fábrica funcional de squads

O Maeve Genius Forge transforma um briefing YAML ou JSON em um squad completo, consistente, validável, testável e executável. A implementação atual é determinística no modo `--no-llm` e gera artefatos reais em disco, não apenas documentos estáticos.

## O que está implementado

O executor `scripts/forge_squad.py` foi refatorado em módulos especializados:

- `briefing_parser.py` — leitura YAML/JSON com parser YAML real e schema formal.
- `requirements_analyzer.py` — análise de lacunas, riscos e revisões humanas.
- `squad_architect.py` — arquitetura de agentes sem redundância de responsabilidades.
- `agent_generator.py` — geração de `agents/*.yaml` com contrato completo.
- `task_generator.py` — geração de tasks com schema, timeout, retry e falha.
- `workflow_generator.py` — workflows com condições, dependências, gates e caminhos de falha.
- `script_generator.py` — scripts Python do squad gerado.
- `documentation_generator.py` — README, docs e exemplos.
- `test_generator.py` — testes automatizados dos arquivos gerados.
- `package_generator.py` — LICENSE, NOTICE, AUTHORS, requirements e relatório de qualidade calculado.

## Schema formal do briefing

Campos suportados:

- `project_name`
- `objective`
- `problem`
- `target_audience`
- `expected_outputs`
- `constraints`
- `integrations`
- `security_level`
- `human_approval_requirements`
- `success_metrics`
- `budget_limit`
- `preferred_models`

Em `--strict`, campos obrigatórios ausentes, tipos inválidos ou campos desconhecidos produzem erro claro. Sem `--strict`, aliases legados como `audience` e `success_criteria` são normalizados com aviso.

## Uso rápido

```bash
python scripts/forge_squad.py \
  --briefing examples/briefing_atena_contratos_publicos.yaml \
  --output output/atena-contratos-publicos \
  --overwrite \
  --strict \
  --no-llm

python scripts/validate_squad.py --root output/atena-contratos-publicos
pytest -q
```

## Modos do executor

- `--dry-run`: analisa o briefing e mostra componentes planejados sem gravar arquivos.
- `--strict`: valida o briefing com rigidez de schema.
- `--overwrite`: substitui o diretório de saída quando já existe.
- `--format yaml|json`: força o formato de leitura.
- `--no-llm`: executa em modo determinístico, sem chamadas externas.
- `--budget-limit`: sobrescreve o limite de orçamento informado no briefing.

## Artefatos obrigatórios gerados

Cada execução completa gera:

- `squad.yaml`
- `README.md`
- `agents/*.yaml`
- `tasks/*.yaml`
- `workflows/*.yaml`
- `scripts/*.py`
- `tests/`
- `examples/`
- `docs/`
- `LICENSE`
- `NOTICE.md`
- `AUTHORS.md`
- `requirements.txt`
- `quality_report.json`

## Critérios de qualidade

O `quality_report.json` registra componentes gerados, validações executadas, testes aprovados, testes reprovados, riscos, itens de revisão humana e nota calculada. A nota não é fixa: deriva da proporção de validações aprovadas, penalidades por risco, testes reprovados e revisões pendentes.

## Limitações conhecidas

- O modo atual é determinístico e não executa pesquisa web nem chamadas LLM.
- Integrações declaradas viram contratos e gates; chamadas externas reais exigem implementação específica e aprovação humana.
- O Forge não cria preços, paletas ou recomendações comerciais quando o briefing não fornece base verificável.
- Publicação GitHub permanece bloqueada até autorização humana explícita.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
