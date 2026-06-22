# Maeve Athena-Mímir Venture Forge

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.1.0-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


## O que é este squad

O **Maeve Athena-Mímir Venture Forge** é um squad premium para transformar ideias de negócio ainda incertas em hipóteses claras, experimentos práticos, evidências interpretáveis e decisões executivas. Ele foi inspirado em princípios de validação rápida de ideias de negócio e reescrito com uma camada metodológica baseada em elementos das mitologias grega e nórdica.

A mitologia aqui não é apenas estética. Cada elemento funciona como metáfora operacional para uma etapa do processo: estratégia, navegação da incerteza, prototipagem, teste de mercado, interpretação de sinais e decisão.

## Para que serve

Este squad serve para validar uma ideia de negócio antes de investir tempo, dinheiro e energia em uma solução completa. Ele ajuda a responder perguntas como:

- Existe um problema real e relevante?
- O público reconhece esse problema?
- A proposta de valor faz sentido?
- Qual hipótese oferece maior risco para o projeto?
- Que experimento simples pode gerar evidência útil?
- A ideia deve avançar, pivotar, ser redesenhada ou abandonada?

## Estrutura dos agentes

### 1. Athena — Estrategista Métis

Define a tese estratégica da ideia, organiza o raciocínio inicial e separa intuição, hipótese e evidência. Atua para dar clareza antes da execução.

### 2. Ariadne — Cartógrafa do Labirinto de Hipóteses

Constrói o mapa de hipóteses e riscos. Usa o conceito do fio de Ariadne para manter rastreabilidade entre problema, cliente, proposta, teste, evidência e decisão.

### 3. Mímir — Guardião do Poço de Evidências

Avalia a profundidade das evidências coletadas. Ajuda a distinguir sinais fracos, opiniões superficiais, comportamento real, intenção de compra e validação consistente.

### 4. Hefesto & Brokkr — Forja de Protótipos

Transforma hipóteses em artefatos testáveis: MVPs, protótipos, simulações, landing pages, experimentos concierge, pilotos e pré-vendas.

### 5. Bifröst — Designer da Ponte de Experimentos

Cria a ponte entre a hipótese interna e o mercado real. Define experimentos proporcionais ao risco, com métrica, público, canal, prazo e critério de decisão.

### 6. Nornas — Orquestradoras da Sprint

Organizam a sequência temporal da validação: o que já foi aprendido, o que precisa ser testado agora e quais futuros possíveis se abrem após cada resultado.

### 7. Hermes — Mentor de Mensagem, Canal e Go-to-Market

Traduz a proposta em comunicação, abordagem de mercado, convites para teste, entrevistas, pilotos e primeiras ações de tração.

### 8. Têmis & Týr — Revisor Ético-Financeiro

Revisa ética, privacidade, viabilidade financeira, promessas feitas ao público, vieses de interpretação e limites da evidência antes da decisão final.

## O que o squad faz

O squad conduz uma ideia por um processo estruturado de experimentação:

1. Clarifica a ideia e o problema central.
2. Mapeia hipóteses críticas e riscos.
3. Organiza uma árvore de conexão do negócio inspirada em Yggdrasil.
4. Escolhe o teste mais adequado para a incerteza dominante.
5. Produz artefatos de teste e prototipagem.
6. Coleta e interpreta sinais de mercado como “runas” de evidência.
7. Compara expectativa, resultado e aprendizado.
8. Gera uma recomendação executiva baseada em evidências.

## O que o squad entrega no final

Ao final do processo, o squad pode entregar:

- mapa de hipóteses e riscos da ideia;
- árvore Yggdrasil do modelo de negócio;
- cartão-runa de experimento;
- plano Bifröst de teste com público, canal, métrica e prazo;
- roteiro de entrevista, landing page, piloto, concierge ou MVP;
- matriz de evidências do Poço de Mímir;
- síntese das Nornas com passado, presente e cenários futuros;
- recomendação final: avançar, pivotar, redesenhar, testar novamente ou abandonar.

## Licença e autoria

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/maeve-athena-mimir-venture-forge-squad/squad.yaml` e `squads/maeve-athena-mimir-venture-forge-squad/workflows/labirinto-hipoteses.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** (veja os agentes em `squads/maeve-athena-mimir-venture-forge-squad/agents/`).
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad (veja os agentes em `squads/maeve-athena-mimir-venture-forge-squad/agents/`)
> e conduza o fluxo definido em `squads/maeve-athena-mimir-venture-forge-squad/`. Siga `squads/maeve-athena-mimir-venture-forge-squad/workflows/labirinto-hipoteses.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/maeve-athena-mimir-venture-forge-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/maeve-athena-mimir-venture-forge-squad/workflows/labirinto-hipoteses.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/maeve-athena-mimir-venture-forge-squad/squad.yaml @squads/maeve-athena-mimir-venture-forge-squad/workflows/labirinto-hipoteses.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/maeve-athena-mimir-venture-forge-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/maeve-athena-mimir-venture-forge-squad/squad.yaml #file:squads/maeve-athena-mimir-venture-forge-squad/workflows/labirinto-hipoteses.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/maeve-athena-mimir-venture-forge-squad/squad.yaml @squads/maeve-athena-mimir-venture-forge-squad/workflows/labirinto-hipoteses.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/maeve-athena-mimir-venture-forge-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/maeve-athena-mimir-venture-forge-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/maeve-athena-mimir-venture-forge-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/maeve-athena-mimir-venture-forge-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/maeve-athena-mimir-venture-forge-squad/squad.yaml` e `squads/maeve-athena-mimir-venture-forge-squad/workflows/labirinto-hipoteses.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
