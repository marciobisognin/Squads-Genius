# Prisma Psíquico Integrativo

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-ready__for__prompting-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


## O que é este squad

O **Prisma Psíquico Integrativo** é um squad premium Maeve/AIOS para análise psicológica assistiva, educacional e organizacional. Ele usa uma arquitetura multiagente do tipo **Orquestrador → Especialistas → Síntese**, na qual diferentes lentes psicológicas analisam o mesmo relato e o orquestrador produz uma formulação integrativa.

O squad trabalha com hipóteses, não com diagnóstico final. Ele não substitui psicólogo, psiquiatra, médico, avaliação profissional, psicoterapia, laudo ou serviço de emergência.

## Para que serve

Serve para transformar relatos humanos complexos em uma leitura estruturada, segura e multilente. Pode apoiar estudos, gestão, educação, liderança, desenvolvimento humano, análise institucional e criação de intervenções não clínicas.

É útil para casos envolvendo comportamento, motivação, procrastinação, conflitos, dinâmica familiar ou organizacional, perda de sentido, hábitos, sinais de sofrimento e necessidade de organizar hipóteses com responsabilidade.

## Estrutura dos agentes e o que fazem

- **Diretor Integrativo:** recebe o relato, faz triagem inicial, classifica a complexidade, seleciona os especialistas necessários e sintetiza as perspectivas.
- **Engenheiro Comportamental:** analisa hábitos, contingências, gatilhos, reforços, esquivas, padrões A-B-C e possibilidades pragmáticas de mudança.
- **Arqueólogo Dinâmico:** observa hipóteses psicodinâmicas, mecanismos de defesa, padrões repetitivos, conflitos latentes, trauma e significados não explícitos.
- **Arquiteto Neurobiológico:** considera sono, fadiga, fisiologia, substâncias, medicação, saúde geral, função executiva e fatores orgânicos que podem exigir avaliação profissional.
- **Dinamista Sistêmico:** desloca o foco do indivíduo para família, grupos, equipe, cultura, papéis, comunicação, poder e incentivos do sistema.
- **Fenomenologista Existencial:** analisa sentido, valores, angústia, vazio, liberdade, responsabilidade, propósito e autorrealização.
- **Analista Psicométrico:** organiza indicadores observáveis, validade, confiabilidade, limites de inferência e necessidade de instrumentos formais quando aplicável.
- **Guardião Ético-Crise:** bloqueia diagnóstico indevido, checa risco, aplica guardrails e aciona protocolo de crise quando há risco iminente.

## O que o squad entrega no final

Ao final de uma análise, o squad entrega:

- triagem de risco e complexidade;
- agentes/lentes acionados;
- hipóteses por perspectiva;
- lacunas de informação;
- síntese integrativa;
- plano de ação seguro e não clínico;
- avisos éticos e limites da análise;
- protocolo de crise quando houver risco iminente;
- arquivos estruturados como `formulation_report.md` e `formulation.json` quando usado pelos scripts.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/prisma-psiquico-integrativo/squad.yaml` e `squads/prisma-psiquico-integrativo/workflows/formulacao-integrativa.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/prisma-psiquico-integrativo/agents/diretor-integrativo.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/prisma-psiquico-integrativo/agents/diretor-integrativo.md`
> e conduza o fluxo definido em `squads/prisma-psiquico-integrativo/`. Siga `squads/prisma-psiquico-integrativo/workflows/formulacao-integrativa.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/prisma-psiquico-integrativo/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/prisma-psiquico-integrativo/workflows/formulacao-integrativa.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/prisma-psiquico-integrativo/squad.yaml @squads/prisma-psiquico-integrativo/workflows/formulacao-integrativa.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/prisma-psiquico-integrativo/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/prisma-psiquico-integrativo/squad.yaml #file:squads/prisma-psiquico-integrativo/workflows/formulacao-integrativa.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/prisma-psiquico-integrativo/squad.yaml @squads/prisma-psiquico-integrativo/workflows/formulacao-integrativa.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/prisma-psiquico-integrativo/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/prisma-psiquico-integrativo/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/prisma-psiquico-integrativo/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/prisma-psiquico-integrativo/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/prisma-psiquico-integrativo/squad.yaml` e `squads/prisma-psiquico-integrativo/workflows/formulacao-integrativa.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
