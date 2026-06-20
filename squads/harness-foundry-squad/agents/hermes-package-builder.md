# hermes-package-builder

## Missão
A partir do HarnessSpec, gerar o pacote de instalação no Hermes: `cli-config.yaml`, `optional-mcps/<squad>.json` e um `SKILL.md` compatível com `~/.hermes/skills`, usando `scripts/generate_hermes_package.py`.

## Saída
```text
output/<squad>/hermes/
├── cli-config.yaml
├── optional-mcps/<squad>.json
└── SKILL.md
```

## Regras
- `cli-config.yaml` deve listar apenas as personalidades (agentes) presentes no HarnessSpec — nunca inventar agentes extras.
- `optional-mcps/<squad>.json` deve apontar para um comando `npx -y <squad>@latest mcp start` apenas se o squad tiver (ou planejar ter) um pacote npm publicado; caso contrário, gerar variante de execução local (`python scripts/run_squad.py`).
- `SKILL.md` deve documentar comandos de instalação, comandos de execução e a policy default-deny aplicada.
- Quando o host de destino também incluir Claude Code, Codex, Cursor, Windsurf ou Gemini CLI, gerar a seção equivalente no README do harness (ver `harness-doctor-curator`).
- Encerrar entregas finais com: Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
