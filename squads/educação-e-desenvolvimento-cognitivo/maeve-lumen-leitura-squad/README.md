# Maeve Lumen Leitura — Squad Premium de Alfabetização Fonológica

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-premium--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


## O que é este squad

O **Maeve Lumen Leitura** é um squad premium criado para transformar o conteúdo do livro *Método Prático de Alfabetização para Destravar a Leitura* em um sistema operacional de apoio à alfabetização fonológica.

Ele não é apenas um resumo do livro. O squad converte os princípios do material em agentes, tarefas, workflows, modelos e scripts que ajudam a identificar onde a leitura travou e a organizar intervenções pedagógicas curtas, lúdicas e progressivas.

## Para que serve

Serve para apoiar famílias, professores e tutores quando a criança apresenta dificuldades como:

- reconhecer letras, mas não conseguir juntar sílabas;
- adivinhar palavras pela primeira letra;
- ler com lentidão, insegurança ou pouca fluência;
- copiar textos, mas não conseguir ler o que escreveu;
- precisar reforçar a relação entre som, letra, sílaba, palavra e frase.

O objetivo é oferecer uma rotina prática de diagnóstico, planejamento, atividade e acompanhamento, sem substituir avaliação profissional quando houver sinais persistentes de dificuldades auditivas, visuais, neurológicas, emocionais, linguísticas ou de aprendizagem.

## Estrutura dos agentes

### 1. Alfabetização Strategist

Organiza a lógica pedagógica geral do squad. Interpreta o estágio da criança, define prioridades e transforma o conteúdo do livro em uma sequência de ação aplicável.

### 2. Diagnóstico Trava Leitura

Mapeia rapidamente o ponto provável de bloqueio na leitura. Observa se a dificuldade aparece em letras, sons, encontros vocálicos, sílabas, palavras ou fluência inicial.

### 3. Fonologia Sílabas Coach

Conduz a progressão fonológica. Trabalha consciência sonora, relação grafema-fonema, encontros vocálicos, sílabas simples e formação inicial de palavras.

### 4. Atividades Lúdicas Designer

Cria atividades simples, curtas e envolventes para a criança praticar sem pressão excessiva. Prioriza jogos, repetição leve, manipulação de sons e pequenas vitórias observáveis.

### 5. Rotina 15min Orchestrator

Monta sessões diárias de 10 a 15 minutos. Define começo, prática principal, reforço, leitura curta e fechamento, evitando excesso de carga cognitiva.

### 6. Família Professor Mentor

Traduz o plano em orientação clara para adultos. Gera recomendações, relatórios simples e formas de acompanhamento entre família, professor e tutor.

### 7. Segurança Pedagógica Reviewer

Revisa os planos e entregáveis para evitar promessas exageradas, rótulos indevidos, pressão emocional ou uso do squad como diagnóstico clínico. Recomenda avaliação especializada quando necessário.

## O que o squad faz na prática

- Aplica uma ficha de diagnóstico rápido de aproximadamente 3 minutos.
- Identifica a provável etapa de trava da leitura.
- Sugere uma sequência fonológica de intervenção.
- Gera plano de sessão curta de alfabetização.
- Cria atividades lúdicas com vogais, encontros vocálicos, sílabas, palavras e frases.
- Produz trilha semanal de acompanhamento.
- Gera relatório simples para família/professor.
- Inclui gate de segurança pedagógica.

## O que o squad entrega no final

Ao ser utilizado, o squad pode entregar:

- ficha de diagnóstico inicial;
- plano de sessão de 10–15 minutos;
- atividades fonológicas e lúdicas;
- banco inicial de palavras e frases;
- trilha semanal de prática;
- relatório de acompanhamento para família/professor;
- recomendações pedagógicas com cautelas de segurança.

## Principais pastas

- `agents/`: agentes especialistas do squad.
- `tasks/`: tarefas operacionais executadas pelos agentes.
- `workflows/`: fluxos principais de diagnóstico, atividades e acompanhamento.
- `templates/`: modelos reutilizáveis de ficha, plano, trilha e relatório.
- `references/`: princípios extraídos e transformados a partir do livro.
- `scripts/`: script local para gerar demonstrações e artefatos.
- `examples/`: caso de demonstração.
- `output/demo/`: exemplos de saída gerados pelo smoke test.
- `validation/`: relatórios de validação e qualidade.

## Licença e autoria

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/maeve-lumen-leitura-squad/squad.yaml` e `squads/maeve-lumen-leitura-squad/workflows/diagnostico-e-plano.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/maeve-lumen-leitura-squad/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/maeve-lumen-leitura-squad/agents/`)
> e conduza o fluxo definido em `squads/maeve-lumen-leitura-squad/`. Siga `squads/maeve-lumen-leitura-squad/workflows/diagnostico-e-plano.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/maeve-lumen-leitura-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/maeve-lumen-leitura-squad/workflows/diagnostico-e-plano.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/maeve-lumen-leitura-squad/squad.yaml @squads/maeve-lumen-leitura-squad/workflows/diagnostico-e-plano.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/maeve-lumen-leitura-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/maeve-lumen-leitura-squad/squad.yaml #file:squads/maeve-lumen-leitura-squad/workflows/diagnostico-e-plano.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/maeve-lumen-leitura-squad/squad.yaml @squads/maeve-lumen-leitura-squad/workflows/diagnostico-e-plano.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/maeve-lumen-leitura-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/maeve-lumen-leitura-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/maeve-lumen-leitura-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/maeve-lumen-leitura-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/maeve-lumen-leitura-squad/squad.yaml` e `squads/maeve-lumen-leitura-squad/workflows/diagnostico-e-plano.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
