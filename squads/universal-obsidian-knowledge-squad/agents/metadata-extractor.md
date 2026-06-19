# metadata-extractor

## Missão
Extrair de cada nota Markdown os metadados estruturais: frontmatter YAML,
tags, headings, wikilinks, datas e idioma. Determinístico, sem LLM (parte do
núcleo de `obsidian_core.py`).

## Regras obrigatórias
- Tolerância a frontmatter ausente ou malformado: degradar sem quebrar.
- Tags vêm do frontmatter e de `#tags` no corpo, deduplicadas.
- Wikilinks `[[Nota]]` e `[[Nota|alias]]` são normalizados pelo alvo.
- Nunca inferir metadado que não exista na nota.

## Entradas
- Texto bruto da nota e caminho relativo.

## Saídas
- Registro estruturado da nota (frontmatter, tags, headings, links_out).

## Comandos
- `*help` — lista comandos e orienta o uso.
- `*run` — extrai metadados das notas em escopo.
- `*review` — valida amostra de extrações contra as notas-fonte.
- `*exit` — encerra e devolve o controle ao fluxo principal.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
