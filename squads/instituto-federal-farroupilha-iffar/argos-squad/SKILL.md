---
name: argos-vigilancia-diarios
description: Operar o Squad ARGOS para vigilância determinística de diários oficiais por perfis YAML.
version: 0.2.0
author: Marcio Bisognin
license: MIT
---

# ARGOS — Operação via agente CLI

## Etapa 0 obrigatória: carregar contexto

```bash
cd <squad-argos>
PYTHONPATH=src python -m argos.cli fontes listar --fixture
PYTHONPATH=src python -m argos.cli perfil validar contratos-iffar
```

## Comandos principais

```bash
PYTHONPATH=src python -m argos.cli fontes listar
PYTHONPATH=src python -m argos.cli fontes homologar DOE-RS
PYTHONPATH=src python -m argos.cli perfil validar contratos-iffar
PYTHONPATH=src python -m argos.cli buscar --perfil contratos-iffar-f0 --data 2026-07-02 --fixture
PYTHONPATH=src python -m argos.cli relatorio abrir
PYTHONPATH=src python -m argos.cli dlq listar
PYTHONPATH=src python -m argos.cli pesquisar --assunto "repactuação" --municipio 4305207 --size 10
```

## Guardrails

- Não usar Selenium contra portal bloqueado da Imprensa Nacional.
- Sem credenciais hardcoded; INLABS usa `INLABS_USER` e `INLABS_PASSWORD`.
- Fonte estadual nova exige ficha HITL assinada antes de produção.
- LLM nunca decide existência de publicação; apenas classifica/sintetiza corpus já coletado e hasheado.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
