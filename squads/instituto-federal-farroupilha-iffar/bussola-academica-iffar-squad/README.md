# 🧭 Bússola Acadêmica IFFar

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


**Nome técnico:** `bussola-academica-iffar-squad`
**Versão:** `1.0.0`

Squad institucional de apoio ao **ciclo acadêmico** de secretarias e coordenações do Instituto Federal Farroupilha (IFFar): revisão de PPC e matriz curricular, calendário e editais de matrícula/rematrícula, auditoria de integralização curricular, atas de conselho de classe, relatórios de aproveitamento/evasão e consistência dos dados enviados ao **SISTEC** e à **Plataforma Nilo Peçanha**.

> ⚖️ **Ressalva obrigatória:** os artefatos gerados são minutas e relatórios de apoio técnico-administrativo. Toda decisão pedagógica — aprovação de PPC, deferimento de matrícula, fechamento de ata de conselho de classe, envio oficial a SISTEC/PNP — é exclusiva da coordenação, do colegiado e da secretaria acadêmica. Revisão humana é obrigatória em todos os artefatos.

## Problema que resolve

O ciclo acadêmico é hoje conduzido manualmente a cada período letivo, com retrabalho, risco de erro na integralização curricular (pré-requisitos e equivalências verificados "de memória") e respostas lentas a estudantes e famílias. O envio de dados a sistemas federais (SISTEC, Plataforma Nilo Peçanha) é manual e sujeito a inconsistências que só aparecem depois do envio. Este squad automatiza a parte determinística desse trabalho (checagem de regras, detecção de conflitos) e organiza a parte textual (relatórios, minutas), preservando toda decisão pedagógica como humana.

## O que o squad gera

| # | Artefato | Base |
|---|---|---|
| 1 | Relatório de aderência PPC/DCN | DCN aplicável + Catálogo Nacional de Cursos Técnicos |
| 2 | Relatório de integralização curricular | matriz curricular x histórico escolar, por script determinístico |
| 3 | Calendário acadêmico validado | checagem de conflitos de data por script determinístico |
| 4 | Edital de matrícula/rematrícula | Regulamento Didático-Pedagógico vigente |
| 5 | Minuta de ata de conselho de classe | dados de desempenho da turma, deliberação do colegiado |
| 6 | Relatório de aproveitamento/retenção/evasão | indicadores agregados por turma/curso |
| 7 | Checklist de consistência SISTEC/PNP | checagem de campos obrigatórios por script determinístico |

## Agentes (5)

`bussola-orchestrator` · `ppc-dcn-analyst` · `curriculo-integralizacao-auditor` · `atas-editais-redator` · `sistec-pnp-validador`

## Workflows (3)

- `revisao_ppc` — análise de aderência às DCN/catálogo de cursos + aprovação do NDE/colegiado.
- `ciclo_matricula` — calendário → edital → auditoria de integralização → checklist SISTEC/PNP → deferimento humano.
- `fechamento_periodo_letivo` — ata de conselho de classe → relatório de aproveitamento/evasão → checklist SISTEC/PNP → envio humano.

## Scripts determinísticos (Python 3.11+, sem dependências)

```bash
python3 scripts/auditor_integralizacao.py --matriz examples/exemplo_matriz_curricular.json --historico examples/exemplo_historico_aluno.json
python3 scripts/conflito_calendario.py --calendario examples/exemplo_calendario.json
python3 scripts/checklist_sistec_pnp.py --registro examples/exemplo_registro_sistec.json
```

## Como ativar

1. Leia `squad.yaml` e assuma a persona `agents/bussola-orchestrator.md`.
2. Descreva a demanda ou preencha `templates/solicitacao_ciclo_academico.yaml`.
3. Acompanhe o roteamento para o workflow correspondente e responda às perguntas de intake.
4. Aprove os gates humanos quando solicitado — o squad nunca decide em lugar da coordenação, do colegiado ou da secretaria acadêmica.
5. Receba os artefatos consolidados.

Exemplos em [`examples/exemplo_uso.md`](examples/exemplo_uso.md). Fontes e normas em [`docs/base_normativa_academica.md`](docs/base_normativa_academica.md). Para conformidade e prazos institucionais cruzados, ver o squad irmão [`compliance-ia-iffar-squad`](../compliance-ia-iffar-squad/).

## Princípios

- Nenhuma decisão pedagógica é tomada pelo squad: ele prepara, audita e sinaliza — a decisão é sempre humana.
- Regras curriculares (pré-requisito, equivalência, carga horária, conflito de data) são checadas por script determinístico, nunca por inferência do agente.
- Dados pessoais de estudantes tratados com minimização (LGPD): apenas os campos necessários à tarefa.
- Toda fonte normativa citada com versão/data; o que não foi verificado na fonte oficial é marcado `a confirmar`.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `IFFar-Squads/squads/bussola-academica-iffar-squad/squad.yaml` e `IFFar-Squads/squads/bussola-academica-iffar-squad/workflows/revisao_ppc.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `IFFar-Squads/squads/bussola-academica-iffar-squad/agents/bussola-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `IFFar-Squads/squads/bussola-academica-iffar-squad/agents/bussola-orchestrator.md`
> e conduza o fluxo definido em `IFFar-Squads/squads/bussola-academica-iffar-squad/`. Siga `IFFar-Squads/squads/bussola-academica-iffar-squad/workflows/revisao_ppc.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @IFFar-Squads/squads/bussola-academica-iffar-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @IFFar-Squads/squads/bussola-academica-iffar-squad/workflows/revisao_ppc.yaml. Conduza o fluxo para o briefing: <...>
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
   @IFFar-Squads/squads/bussola-academica-iffar-squad/squad.yaml @IFFar-Squads/squads/bussola-academica-iffar-squad/workflows/revisao_ppc.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `IFFar-Squads/squads/bussola-academica-iffar-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:IFFar-Squads/squads/bussola-academica-iffar-squad/squad.yaml #file:IFFar-Squads/squads/bussola-academica-iffar-squad/workflows/revisao_ppc.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@IFFar-Squads/squads/bussola-academica-iffar-squad/squad.yaml @IFFar-Squads/squads/bussola-academica-iffar-squad/workflows/revisao_ppc.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia IFFar-Squads/squads/bussola-academica-iffar-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em IFFar-Squads/squads/bussola-academica-iffar-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `IFFar-Squads/squads/bussola-academica-iffar-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider IFFar-Squads/squads/bussola-academica-iffar-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `IFFar-Squads/squads/bussola-academica-iffar-squad/squad.yaml` e `IFFar-Squads/squads/bussola-academica-iffar-squad/workflows/revisao_ppc.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
