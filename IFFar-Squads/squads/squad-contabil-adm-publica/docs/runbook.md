# Runbook operacional

## 1. Preparar o caso

Crie um JSON conforme `schemas/case_input.schema.json`. Use somente exportações e relatórios já obtidos por meios institucionais autorizados.

## 2. Executar a engine

```bash
python3 scripts/contabil_core.py \
  --input examples/caso_com_inconsistencias.json \
  --output-dir generated/demo
```

## 3. Revisar as saídas

- `analysis.json` — estado estruturado, hash e achados;
- `matriz_achados.csv` — matriz filtrável;
- `plano_regularizacao.md` — proposta assistida, não executada;
- `relatorio_conformidade.md` — relatório para revisão do contador.

## 4. Gate do contador

O contador confirma ou rejeita:

1. enquadramento dos achados;
2. referência normativa vigente;
3. procedimento de regularização;
4. conclusão da conformidade.

## 5. Revalidar

Após as ações realizadas fora do squad, anexe novas evidências, gere novo caso e compare hashes/achados. Nunca altere manualmente a saída anterior para simular saneamento.

## Validação técnica

```bash
python3 -m py_compile scripts/*.py
python3 -m pytest -q tests
python3 scripts/validate_squad.py --root .
```

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
