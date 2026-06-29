# Maeve Fundamentos ROI Compass

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-0.2.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


Squad Maeve criado a partir dos dois áudios de Marcio Bisognin sobre fundamentos, questionamento, prática, engenharia de contexto, IA, cursos, mentorias, ROI e risco de acelerar distrações.

## Para quem é

- Pessoas que compram cursos, ferramentas, mentorias ou IA sem clareza se aquilo resolve o problema atual.
- Profissionais que querem usar IA como advisor, acelerador ou professor sem delegar cegamente o pensamento.
- Criadores, gestores, educadores e empreendedores que precisam transformar conhecimento em prática, discurso e método.
- Usuários que querem reduzir hype, dispersão, atalhos e acúmulo de recursos sem execução.

## Objetivo

Ajudar a responder, antes de qualquer investimento ou execução:

1. O que eu quero?
2. Para onde estou indo?
3. O que preciso dominar para chegar lá?
4. O que já estou fazendo?
5. O básico está bem feito?
6. Este recurso acelera clareza ou acelera caos?
7. A IA precisa executar, complementar ou me ensinar?

## O que tem dentro

- **Orchestrator:** conduz a decisão e integra fundamentos, contexto e ROI.
- **Researcher:** extrai princípios, problemas e critérios dos áudios.
- **Builder:** transforma diagnóstico em plano prático, prompt/context brief e decisão de investimento.
- **Validator:** verifica se há fundamento, prática, compromisso e proporcionalidade antes de aprovar avanço.
- **Script `fundamentos-roi-compass.cjs`:** gera diagnóstico de decisão a partir de objetivo, recurso, nível do básico e lacunas.
- **Templates:** canvas de decisão e brief de contexto para IA.
- **Referências:** transcrições dos dois áudios e análise integrada.
- **Validação:** smoke test e Architect Gate premium.

## Problemas que o squad reduz

- Compra de fórmulas prontas sem internalizar fundamentos.
- Uso de ferramenta avançada para problema simples.
- IA executando sem contexto pessoal/profissional.
- Conhecimento sem prática.
- Prática sem técnica.
- Hype e pulo de atalho em atalho.
- Falta de ROI por ausência de atitude, comprometimento e implementação.

## Exemplos de uso

### 1. Decidir se compro um curso

```bash
node scripts/fundamentos-roi-compass.cjs   --objetivo "criar produtos digitais com IA"   --recurso "mentoria avançada de automações"   --basico "parcial"   --lacunas "prompting, oferta, execução diária"   --out generated/decisao-curso.md
```

### 2. Criar contexto para a IA executar melhor

“Maeve, gere um context brief para a IA considerando que quero atuar mais como advisor/acelerador de pessoas, projetos e empresas do que como programador bruto.”

### 3. Filtrar hype

“Maeve, avalie se esta ferramenta realmente muda meu jogo agora ou se apenas acelera distração porque ainda não faço o básico.”

## Regra central

Ferramenta externa pode potencializar, mas não substitui fundamento, clareza, prática e compromisso.

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/maeve-fundamentos-roi-compass/squad.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/maeve-fundamentos-roi-compass/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/maeve-fundamentos-roi-compass/agents/`)
> e conduza o fluxo definido em `squads/maeve-fundamentos-roi-compass/`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/maeve-fundamentos-roi-compass/squad.yaml e assuma a persona do orquestrador do squad.
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
   @squads/maeve-fundamentos-roi-compass/squad.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/maeve-fundamentos-roi-compass/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/maeve-fundamentos-roi-compass/squad.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/maeve-fundamentos-roi-compass/squad.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/maeve-fundamentos-roi-compass/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/maeve-fundamentos-roi-compass/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/maeve-fundamentos-roi-compass/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/maeve-fundamentos-roi-compass/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/maeve-fundamentos-roi-compass/squad.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
