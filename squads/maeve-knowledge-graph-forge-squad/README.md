# Maeve Knowledge Graph Forge

<div align="center">

![version](https://img.shields.io/badge/vers%C3%A3o-1.0.2-2b6cb0?style=for-the-badge) ![status](https://img.shields.io/badge/status-production--ready-2f855a?style=for-the-badge) ![license](https://img.shields.io/badge/licen%C3%A7a-MIT-805ad5?style=for-the-badge) ![lang](https://img.shields.io/badge/idioma-pt--BR-dd6b20?style=for-the-badge)

</div>


## Resumo enxuto

Este squad transforma uma **base de conhecimento** — PDFs, livros, pastas, documentos, anotações e textos — em um **mapa inteligente de conexões**, semelhante à lógica visual de grafos usada em ferramentas de conhecimento.

Ele vasculha o material, extrai conceitos, identifica relações, organiza clusters temáticos e mostra o que se conecta com o quê. Depois pergunta ao usuário o que ele quer fazer com aquela base: estudar, aprender, criar um sistema, desenvolver uma aplicação, montar um curso, gerar conteúdo, criar um squad derivado ou cruzar aquele material com outras áreas.

## Para quem é

- Pessoas que têm muitos PDFs, livros ou documentos e não sabem por onde começar.
- Estudantes e pesquisadores que precisam entender conexões entre temas.
- Criadores que querem transformar documentos em cursos, artigos, roteiros ou produtos.
- Desenvolvedores que querem criar sistemas a partir de uma base documental.
- Consultores que desejam converter conhecimento acumulado em oferta, workflow ou aplicação.

## Objetivo

Transformar documentos dispersos em um **sistema de conhecimento acionável**. O squad não apenas resume arquivos: ele cria um grafo com conceitos, documentos, entidades e conexões; explica centros de gravidade; mostra lacunas; sugere trilhas de aprendizagem; e conduz o usuário para uma próxima ação prática.

## O que tem dentro

- 10 agentes especializados.
- 12 tasks operacionais.
- 4 workflows: pipeline completo, grafo visual, modo estudo e modo construção.
- Scripts Python para inventariar arquivos, extrair texto simples, gerar conceitos, criar grafo JSON/HTML, validar e empacotar.
- Templates, exemplo prático, documentação e quality gates.

## Agentes

- `knowledge-intake-orchestrator` — Recebe pastas, PDFs, livros e documentos; define escopo e objetivo.
- `document-ingestion-specialist` — Inventaria arquivos, formatos e metadados.
- `ocr-and-text-extraction-agent` — Extrai texto e aponta necessidade de OCR externo.
- `concept-entity-miner` — Identifica conceitos, entidades, termos, autores e problemas.
- `semantic-link-architect` — Cria relações de causa, dependência, oposição, exemplo e aplicação.
- `knowledge-graph-visualizer` — Gera grafo visual navegável em JSON/HTML.
- `learning-path-designer` — Transforma o grafo em trilhas de estudo.
- `application-opportunity-analyst` — Detecta possibilidades de sistemas, apps, cursos, squads e workflows.
- `cross-domain-synthesizer` — Cruza o conteúdo com outras áreas.
- `action-output-generator` — Pergunta a próxima ação e gera o artefato escolhido.

## Exemplos

### Exemplo 1 — Estudar uma pasta de PDFs
O usuário entrega PDFs sobre IA, educação e avaliação. O squad extrai conteúdo, cria grafo, mostra temas centrais e gera trilha de estudo.

### Exemplo 2 — Criar sistema a partir de documentos
O usuário entrega manuais e normas. O squad identifica entidades, fluxos, regras e dependências; depois sugere arquitetura de sistema.

### Exemplo 3 — Criar curso ou produto
O usuário entrega livros e materiais próprios. O squad organiza os temas, detecta sequência pedagógica e sugere módulos.

## Uso rápido

```bash
python scripts/run_demo.py
python scripts/build_knowledge_graph.py --input examples/sample_knowledge_base --output output/demo_graph
python scripts/validate_squad.py --root .
python scripts/package_squad.py --root . --output ../../exports/maeve-knowledge-graph-forge-squad-v1.0.0.zip
```

---

## 🤝 Como usar nos principais LLMs de codificação

> [!NOTE]
> **O padrão de ativação é o mesmo em qualquer ferramenta:**
> 1. **Dê contexto** ao assistente apontando os arquivos do squad (especialmente `squads/maeve-knowledge-graph-forge-squad/squad.yaml` e `squads/maeve-knowledge-graph-forge-squad/workflows/full_knowledge_graph_pipeline.yaml`).
> 2. **Peça que ele assuma a persona do orquestrador** definido em `squads/maeve-knowledge-graph-forge-squad/agents/knowledge-intake-orchestrator.md`.
> 3. **Conduza o fluxo** respeitando os checkpoints humanos e validando cada handoff/contrato.
>
> **Prompt de ativação** (copie, cole e ajuste o briefing):
> ```text
> Assuma a persona do orquestrador do squad definido em `squads/maeve-knowledge-graph-forge-squad/agents/knowledge-intake-orchestrator.md`
> e conduza o fluxo definido em `squads/maeve-knowledge-graph-forge-squad/`. Siga `squads/maeve-knowledge-graph-forge-squad/workflows/full_knowledge_graph_pipeline.yaml`.
> Valide cada handoff/contrato e respeite os checkpoints humanos.
> Meu briefing é: <descreva seu objetivo, materiais e formato de saída>.
> ```

<details open>
<summary><b>🟣 Claude Code (CLI / Web / IDE) — recomendado</b></summary>

<br>

```bash
# No terminal, dentro do repositório
claude

> Leia @squads/maeve-knowledge-graph-forge-squad/squad.yaml e assuma a persona do orquestrador do squad.
  Siga @squads/maeve-knowledge-graph-forge-squad/workflows/full_knowledge_graph_pipeline.yaml. Conduza o fluxo para o briefing: <...>
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
   @squads/maeve-knowledge-graph-forge-squad/squad.yaml @squads/maeve-knowledge-graph-forge-squad/workflows/full_knowledge_graph_pipeline.yaml
   Assuma a persona do orquestrador e conduza o fluxo para o briefing: <...>
   ```
3. **Persistente:** crie um `.cursorrules` na raiz apontando para `squads/maeve-knowledge-graph-forge-squad/` como squad ativo.

</details>

<details>
<summary><b>⬛ GitHub Copilot (VS Code Chat)</b></summary>

<br>

```text
@workspace #file:squads/maeve-knowledge-graph-forge-squad/squad.yaml #file:squads/maeve-knowledge-graph-forge-squad/workflows/full_knowledge_graph_pipeline.yaml
Assuma a persona do orquestrador deste squad e conduza o fluxo para: <...>
```
Para regras persistentes, crie **`.github/copilot-instructions.md`** com o prompt de ativação.

</details>

<details>
<summary><b>🟩 Windsurf (Cascade)</b></summary>

<br>

```text
@squads/maeve-knowledge-graph-forge-squad/squad.yaml @squads/maeve-knowledge-graph-forge-squad/workflows/full_knowledge_graph_pipeline.yaml
Atue como o orquestrador deste squad e execute o fluxo para: <briefing>.
```
Fixe as regras em **`.windsurfrules`** (raiz do projeto).

</details>

<details>
<summary><b>🟧 Cline / Roo Code (VS Code)</b></summary>

<br>

```text
Leia squads/maeve-knowledge-graph-forge-squad/squad.yaml e assuma a persona do orquestrador.
Conduza o fluxo do squad e execute os scripts em squads/maeve-knowledge-graph-forge-squad/scripts/ quando o passo pedir.
Briefing: <...>
```
O Cline/Roo pode **executar os scripts** do squad e ler a saída — aprove a execução quando solicitado.

</details>

<details>
<summary><b>🟨 Continue.dev / Aider / Zed AI / chats web</b></summary>

<br>

- **Continue.dev:** use `@file` para `squads/maeve-knowledge-graph-forge-squad/squad.yaml`; cole o prompt de ativação.
- **Aider:** `aider squads/maeve-knowledge-graph-forge-squad/squad.yaml` e instrua o orquestrador.
- **ChatGPT / Gemini (sem acesso a arquivos):** copie o conteúdo de `squads/maeve-knowledge-graph-forge-squad/squad.yaml` e `squads/maeve-knowledge-graph-forge-squad/workflows/full_knowledge_graph_pipeline.yaml` para o chat, cole o prompt de ativação e rode eventuais scripts localmente, colando a saída de volta.

</details>



Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
