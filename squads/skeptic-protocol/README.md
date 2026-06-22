# SKEPTIC Protocol

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-2.1.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


O **SKEPTIC Protocol** evoluiu de uma metodologia de testes adversariais de software para uma plataforma defensiva de **red teaming de agentes e squads multiagentes**.

A versão atual testa qualquer squad por caminho, usando biblioteca de ataques canários, 16 cenários reproduzíveis cobrindo as 14 classes solicitadas, classificação por severidade/probabilidade/impacto, relatório de evidências, recomendações, execução dinâmica opcional via runtime adapters, geração de testes de regressão e integração com CI.

## O que faz

O SKEPTIC executa uma bateria determinística contra artefatos de squads AIOS/OpenSquad para verificar se existem controles explícitos contra falhas típicas de agentes e sistemas multiagentes:

1. Prompt injection direta.
2. Prompt injection indireta em documentos, páginas web, e-mails, resultados de busca e ferramentas MCP.
3. Exfiltração de contexto, memória, credenciais, instruções internas e dados de outro usuário.
4. Escalada de privilégio.
5. Uso de ferramenta não autorizada.
6. Confused deputy.
7. Alucinação de ações executadas.
8. Citações inexistentes ou incompatíveis.
9. Loop infinito entre agentes.
10. Amplificação de erro entre agentes.
11. Aprovação humana simulada ou ignorada.
12. Consumo excessivo de tokens e ferramentas.
13. Persistência indevida de dados.
14. Manipulação do agente avaliador.

## Uso rápido

```bash
cd squads/skeptic-protocol

python scripts/skeptic_agent_redteam.py \
  --squad ../maeve-genius-forge-squad \
  --output redteam-output/maeve-genius-forge \
  --formats json,markdown,html \
  --write-scenarios \
  --regression-output tests/test_security_regression_maeve_genius_forge.py \
  --fail-on none
```

Para testar o próprio SKEPTIC:

```bash
python scripts/skeptic_agent_redteam.py \
  --squad . \
  --output redteam-output/self \
  --formats json,markdown,html \
  --write-scenarios \
  --fail-on vulnerable
```

## Saídas

- `skeptic_redteam_report.json` — relatório estruturado para automação e CI.
- `skeptic_redteam_report.md` — relatório legível para revisão humana.
- `skeptic_redteam_report.html` — relatório portável para compartilhamento.
- `scenarios/*.json` — um cenário reproduzível por vulnerabilidade.
- teste pytest de regressão quando `--regression-output` é informado.

## Biblioteca de ataques

A biblioteca fica em:

`data/agent_redteam_attack_library.json`

Cada entrada contém:

- `id`
- `title`
- `category`
- `surfaces`
- `severity`
- `likelihood`
- `impact`
- `scenario`
- `payload`
- `expected_safe_behavior`
- `control_keywords`
- `recommendations`

Os payloads são **canários defensivos**. Eles simulam tentativas de ataque sem usar credenciais reais, dados reais de usuários ou exploração de sistemas externos.

## Runtime adapters

Além do modo estático, o SKEPTIC agora executa probes dinâmicos canários contra um runtime explicitamente informado.

### Adapter seguro simulado

```bash
python scripts/skeptic_agent_redteam.py \
  --squad . \
  --output redteam-output/mock-safe \
  --runtime-adapter mock-safe \
  --formats json,markdown,html \
  --write-scenarios
```

### Adapter vulnerável simulado

```bash
python scripts/skeptic_agent_redteam.py \
  --squad . \
  --output redteam-output/mock-vulnerable \
  --runtime-adapter mock-vulnerable \
  --fail-on none
```

### Adapter por comando local

```bash
python scripts/skeptic_agent_redteam.py \
  --squad . \
  --output redteam-output/local-command \
  --runtime-adapter local-command \
  --runtime-command "python examples/runtime_adapters/safe_local_command_adapter.py" \
  --runtime-timeout 5 \
  --formats json,markdown,html \
  --write-scenarios
```

O comando recebe o probe JSON via `stdin` e devolve texto ou JSON com `response`, `content`, `message` ou `output`.

## Regressão de segurança

Quando uma correção for aplicada, gere um teste de regressão:

```bash
python scripts/skeptic_agent_redteam.py \
  --squad /caminho/do/squad \
  --output redteam-output/squad-corrigido \
  --regression-output tests/test_security_regression_squad_corrigido.py \
  --fail-on none

python -m pytest tests/test_security_regression_squad_corrigido.py
```

O teste falha se qualquer vulnerabilidade voltar ao estado `vulnerable`.

## CI

A workflow `.github/workflows/skeptic-agent-redteam.yml` executa:

```bash
python -m pytest -q
python scripts/skeptic_agent_redteam.py --squad . --output redteam-output --formats json,markdown,html --write-scenarios --fail-on vulnerable
```

## Pipeline atualizado

| Fase | Agente | Papel |
|------|--------|-------|
| 1 | `failure-predictor` | Identifica classes de falha e lacunas de controle. |
| 2 | `test-engineer` | Transforma achados em testes e regressões. |
| 3 | `solution-implementer` | Corrige controles, contratos e documentação. |
| 4 | `red-teamer` | Executa a biblioteca de ataques canários contra o squad alvo. |
| 5 | `skeptic-orchestrator` | Consolida evidências, go/no-go e recomendações. |

## Documentação técnica

- `docs/runtime-adapters.md`
- `docs/agent-red-team-platform.md`
- `tasks/run-agent-red-team.md`
- `workflows/agent-squad-red-team-platform.yaml`
- `scripts/skeptic_agent_redteam.py`

## Limitações

- A execução padrão continua estática e determinística: verifica controles documentados e cenários reproduzíveis.
- A execução dinâmica agora existe por runtime adapters (`mock-safe`, `mock-vulnerable` e `local-command`), mas runtimes produtivos devem ser conectados por wrappers isolados e com dados sintéticos.
- Resultado `pass` indica cobertura mínima nos artefatos e/ou resposta segura ao canário; ambientes produtivos ainda exigem validação em sandbox antes de uso operacional.

## Autor

Marcio Bisognin

[Squads Platform](https://squads.sh/pt)

[Instagram @marciobisognin](https://www.instagram.com/marciobisognin/)

## Licença

MIT

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/skeptic-protocol/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/skeptic-protocol/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/skeptic-protocol/agents/`)
> e conduza o fluxo definido em `squads/skeptic-protocol/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/skeptic-protocol/squad.yaml e assuma a persona do orquestrador do squad.
  Conduza o fluxo para o briefing: <...>
```
- Use **`@caminho/arquivo`** para dar contexto preciso (autocompleta no prompt).
- Disponível em **CLI, app desktop/web (claude.ai/code) e extensões VS Code / JetBrains**.

</details>

<details>
<summary><b>🟦 Cursor</b></summary>

<br>

1. Abra a pasta do repositório no Cursor.
2. No **Chat / Composer (⌘/Ctrl + I)**, referencie os arquivos com `@`:
   ```text
   @squads/skeptic-protocol/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/skeptic-protocol/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/skeptic-protocol/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/skeptic-protocol/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/skeptic-protocol/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/skeptic-protocol/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/skeptic-protocol/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/skeptic-protocol/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/skeptic-protocol/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>


---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
