# Nirvana README Architect — Tech Stack

## Core
| Tecnologia | Propósito | Versão |
|-----------|---------|---------|
| GitHub Flavored Markdown | Linguagem de markup do README | Latest |
| Mermaid | Diagramas no GitHub | 10.x+ |
| Shields.io | Badges dinâmicos | API v1 |

## Features do GitHub Suportadas
| Feature | Sintaxe | Uso no NRA |
|---------|---------|-----------|
| Headings (H1-H6) | `# Heading` | Estrutura do README |
| Bold/Italic | `**bold**` `*italic*` | Ênfase em texto |
| Code blocks | ` ```lang ` | Exemplos de código |
| Tables | `\| col \|` | Referências tabulares |
| Task lists | `- [ ] item` | Checklists de setup |
| Alerts | `> [!TYPE]` | Destaques importantes |
| Footnotes | `[^1]` | Referências externas |
| Mermaid diagrams | ` ```mermaid ` | Arquitetura e fluxos |
| Math/LaTeX | `$formula$` | Fórmulas (se necessário) |
| Collapsed sections | `<details>` | Conteúdo extenso |
| Badges | `![alt](url)` | Status do projeto |
| Emojis | `:emoji:` | Scanning visual |
| kbd tags | `<kbd>key</kbd>` | Atalhos de teclado |
| Sub/superscript | `<sub>` `<sup>` | Notações |
| Diff blocks | ` ```diff ` | Changelogs |
| Relative links | `[text](./path)` | Navegação interna |
| Reference links | `[text][ref]` | Links organizados |

## Ferramentas Claude Code
| Ferramenta | Propósito |
|-----------|---------|
| Read | Leitura de arquivos do projeto |
| Write | Escrita do README final |
| Edit | Edição incremental do README |
| Glob | Descoberta de arquivos e estrutura |
| Grep | Busca de padrões (env vars, imports, configs) |
| Bash | Directory tree, contagem de arquivos |
| lsp_document_symbols | Análise de símbolos em arquivos |
