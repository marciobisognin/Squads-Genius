# Universal Obsidian Knowledge Squad — PRD (versão revisada)

**Squad portátil para transformar qualquer vault Obsidian em uma base de conhecimento pesquisável, citável, auditável e adaptável ao usuário ou ao agente que o carregar.**

> **Versão deste PRD:** 2.0 (revisada) · **Status:** proposta técnica pronta para construção · **Modo padrão:** read-only
>
> **Changelog em relação à v1:** alinhamento com o `validate_squad.py` (pastas/arquivos obrigatórios), agentes como personas Markdown, manifesto `squad.yaml` com `file:` por item, remoção de caminhos hardcoded no adaptador Maeve, mapeamento explícito determinístico-vs-LLM, IDs/citações estáveis, conciliação da lista de testes e registro no `SQUAD_INDEX.md`.

---

## 1. Visão geral

O **Universal Obsidian Knowledge Squad** é um sistema multiagente e portável para usar um vault Obsidian como base de conhecimento operacional.

Ele não deve depender de uma pessoa, de uma assistente específica ou de um caminho fixo de arquivos. O mesmo squad deve funcionar para:

- Maeve, quando carregado por um usuário que utilize esse adaptador;
- qualquer outro agente Hermes;
- outro assistente compatível;
- outro usuário com seu próprio Obsidian;
- uso local via linha de comando, mesmo sem agente conversacional.

A arquitetura separa três camadas:

1. **Núcleo universal** — indexação, busca, citações, grafo e auditoria (determinístico).
2. **Perfil do usuário** — caminho do vault, preferências, idioma, privacidade e modo de escrita.
3. **Adaptador do agente** — regras específicas para Maeve, Hermes genérico ou outro assistente.

Assim, quando Maeve carregar o squad, ela o incorpora como uma extensão operacional. Quando outro usuário ou agente carregar, o squad se adapta ao vault e às preferências daquele ambiente.

---

## 2. Nome e identidade do squad

- **Nome público recomendado:** Universal Obsidian Knowledge Squad
- **Slug técnico:** `universal-obsidian-knowledge-squad`
- **Nomes alternativos:** `obsidian-knowledge-engine-squad`, `portable-obsidian-rag-squad`, `obsidian-vault-intelligence-squad`

### Regra de identidade

O núcleo do squad deve ser neutro. Ele **não** deve conter dependências fixas como: nome de usuário específico, caminho fixo de vault, persona obrigatória, instituição obrigatória, idioma obrigatório, modelo obrigatório, provedor obrigatório ou agente obrigatório.

A personalização deve ocorrer por **configuração** e **adaptadores**, nunca por hardcode. Isso inclui adaptadores: nenhum adaptador pode trazer caminho de entrega, nome de usuário ou pasta de dispositivo embutidos no manifesto (ver §16).

---

## 3. Objetivo

Permitir que qualquer pessoa use seu Obsidian como base de conhecimento estruturada, com capacidade de:

- varrer e indexar notas Markdown;
- extrair títulos, headings, tags, frontmatter, links e backlinks;
- pesquisar por palavra-chave, estrutura, pasta, tag e relações;
- gerar respostas com citações rastreáveis;
- produzir sínteses, relatórios, artigos, planos, PRDs, squads e materiais;
- mapear lacunas, duplicidades e notas órfãs;
- operar em modo seguro, inicialmente **read-only**;
- adaptar linguagem, estilo e critérios ao usuário que estiver usando.

---

## 4. Princípio de portabilidade

O squad opera a partir de um arquivo de configuração do usuário, sem caminhos fixos.

```yaml
user_profile:
  display_name: "Usuário"
  language: "pt-BR"
  timezone: "America/Sao_Paulo"
  preferred_style: "claro, técnico e objetivo"

vault:
  path: "/caminho/para/o/vault"
  name: "Meu Obsidian"
  default_scope: "all"

runtime:
  default_mode: "read_only"
  citation_required: true
  allow_write: false
  agent_adapter: "generic"
```

### Ordem de resolução do vault (nunca caminho fixo)

1. Configuração explícita passada por CLI (`--vault`).
2. `config/user.config.yaml` local.
3. Variável de ambiente `OBSIDIAN_VAULT_PATH`.
4. Busca assistida por diretórios comuns (com confirmação do usuário).
5. Solicitação de caminho ao usuário.

---

## 5. Como funciona quando Maeve carrega

Quando Maeve carrega o squad, o adaptador `maeve` pode ser ativado:

```yaml
runtime:
  agent_adapter: "maeve"
```

Maeve incorpora o squad como extensão da própria operação. Diante de pedidos como "use meu Obsidian", "consulte minhas notas", "o que eu já escrevi sobre isso?", "monte um PRD a partir do meu Obsidian", Maeve deve:

1. carregar a skill do squad;
2. localizar a configuração do vault;
3. operar em modo read-only por padrão;
4. consultar o índice;
5. buscar notas relevantes;
6. responder com citações;
7. pedir autorização antes de qualquer alteração.

**Regra:** Maeve pode usar a própria persona para entregar o resultado, mas o conhecimento citado deve vir do vault e ser rastreável.

---

## 6. Como funciona para qualquer outro usuário

Setup inicial genérico:

1. Informar o caminho do vault.
2. Escolher idioma padrão.
3. Escolher modo de operação (`read_only`, `suggest`, `draft_patch`, `write` apenas com autorização).
4. Definir pastas a incluir e a excluir.
5. Gerar índice inicial.
6. Executar teste de consulta.
7. Gerar `quality_report.json`.

```bash
python3 scripts/setup_user_profile.py \
  --vault "/home/user/Obsidian/MyVault" \
  --language "en-US" \
  --adapter "generic" \
  --mode "read_only"
```

---

## 7. Arquitetura geral (alinhada ao validador do repositório)

> O `validate_squad.py` exige os diretórios `agents/`, `tasks/`, `workflows/`, `scripts/`, `examples/`, `docs/` e os arquivos `squad.yaml`, `README.md`, `LICENSE`, `NOTICE.md`, `AUTHORS.md`. A estrutura abaixo já contempla todos.

```text
universal-obsidian-knowledge-squad/
├── squad.yaml                 # manifesto (obrigatório) — lista agentes/tasks/workflows com file:
├── README.md                  # (obrigatório)
├── LICENSE                    # (obrigatório) — MIT
├── NOTICE.md                  # (obrigatório)
├── AUTHORS.md                 # (obrigatório)
├── .gitignore                 # ignora índices gerados e qualquer conteúdo de vault
├── docs/                      # (obrigatório)
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   └── ADAPTERS.md
├── config/
│   ├── default.config.yaml
│   ├── user.config.example.yaml
│   └── adapters/
│       ├── generic.yaml
│       ├── maeve.yaml
│       └── hermes.yaml
├── skills/
│   ├── generic-obsidian-knowledge/SKILL.md
│   └── maeve-obsidian-adapter/SKILL.md
├── agents/                    # personas em Markdown (convenção do repo)
│   ├── vault-orchestrator.md
│   ├── user-profile-resolver.md
│   ├── note-indexer.md
│   ├── metadata-extractor.md
│   ├── lexical-retriever.md
│   ├── semantic-retriever.md
│   ├── citation-guardian.md
│   ├── knowledge-synthesizer.md
│   ├── graph-mapper.md
│   ├── note-curator.md
│   └── quality-auditor.md
├── tasks/
│   ├── t01_setup_profile.yaml
│   ├── t02_scan_vault.yaml
│   ├── t03_build_index.yaml
│   ├── t04_query_knowledge.yaml
│   ├── t05_generate_citations.yaml
│   ├── t06_synthesize_answer.yaml
│   ├── t07_map_backlinks.yaml
│   ├── t08_detect_duplicates.yaml
│   ├── t09_generate_digest.yaml
│   └── t10_quality_gate.yaml
├── workflows/
│   ├── setup_user.yaml
│   ├── build_index.yaml
│   ├── update_index.yaml
│   ├── ask_vault.yaml
│   ├── generate_knowledge_map.yaml
│   ├── vault_digest.yaml
│   ├── curate_notes.yaml
│   └── export_context.yaml
├── scripts/                   # núcleo determinístico (Python 3.11+, sem deps externas no mínimo viável)
│   ├── setup_user_profile.py
│   ├── obsidian_index.py
│   ├── obsidian_search.py
│   ├── obsidian_query.py
│   ├── obsidian_graph.py
│   ├── obsidian_digest.py
│   ├── obsidian_export_context.py
│   ├── obsidian_quality_audit.py
│   └── run_squad.py           # entrypoint que orquestra os workflows via CLI
├── schemas/
│   ├── user_profile.schema.json
│   ├── vault_config.schema.json
│   ├── note.schema.json
│   ├── chunk.schema.json
│   ├── citation.schema.json
│   ├── query_result.schema.json
│   └── vault_index.schema.json
├── templates/
│   ├── answer_with_citations.md
│   ├── knowledge_map.md
│   ├── gap_report.md
│   ├── weekly_digest.md
│   ├── restructuring_suggestion.md
│   └── user_config.yaml
├── examples/                  # (obrigatório)
│   ├── sample_vault/
│   ├── queries/
│   └── outputs/
└── tests/
    ├── test_setup_profile.py
    ├── test_index.py
    ├── test_frontmatter.py
    ├── test_links.py
    ├── test_search.py
    ├── test_citations.py
    ├── test_graph.py
    ├── test_permissions.py
    ├── test_adapters.py
    └── test_quality.py
```

> **Observação sobre índices:** o diretório de índice (`.obsidian_knowledge_index/`) e a pasta `indexes/` guardam dados gerados e **nunca** conteúdo de vault versionado. Apenas `indexes/.gitkeep` é commitado; o restante entra no `.gitignore`.

---

## 8. Manifesto `squad.yaml` (esboço normativo)

O `validate_squad.py` verifica que cada `file:` de agente, task e workflow exista. O manifesto deve seguir este formato:

```yaml
name: universal-obsidian-knowledge-squad
display_name: Universal Obsidian Knowledge Squad
version: 1.0.0
language: pt-BR
license: MIT
creator: Marcio Bisognin
instagram: "@marciobisognin"
required_footer: "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."
positioning: >
  Transforma qualquer vault Obsidian em base de conhecimento pesquisável,
  citável e auditável, portável entre usuários, agentes e CLI.
default_mode: read_only

agents:
  - id: vault-orchestrator
    file: agents/vault-orchestrator.md
    role: Coordena a execução do squad e escolhe workflows.
  - id: user-profile-resolver
    file: agents/user-profile-resolver.md
    role: Lê configuração do usuário, idioma, vault e modo.
  - id: note-indexer
    file: agents/note-indexer.md
    role: Varre o vault e cria índice de notas (via script determinístico).
  - id: metadata-extractor
    file: agents/metadata-extractor.md
    role: Extrai frontmatter, tags, headings e datas (determinístico).
  - id: lexical-retriever
    file: agents/lexical-retriever.md
    role: Busca por texto usando SQLite FTS5 (determinístico).
  - id: semantic-retriever
    file: agents/semantic-retriever.md
    role: Busca por embeddings quando disponível (opcional).
  - id: citation-guardian
    file: agents/citation-guardian.md
    role: Garante rastreabilidade das respostas.
  - id: knowledge-synthesizer
    file: agents/knowledge-synthesizer.md
    role: Produz sínteses, relatórios e materiais (LLM).
  - id: graph-mapper
    file: agents/graph-mapper.md
    role: Mapeia links, backlinks, clusters e lacunas (determinístico).
  - id: note-curator
    file: agents/note-curator.md
    role: Sugere curadoria; escrita só com autorização.
  - id: quality-auditor
    file: agents/quality-auditor.md
    role: Verifica integridade, citações e segurança.

tasks:
  - id: t01_setup_profile
    file: tasks/t01_setup_profile.yaml
    owner: user-profile-resolver
  - id: t02_scan_vault
    file: tasks/t02_scan_vault.yaml
    owner: note-indexer
  - id: t03_build_index
    file: tasks/t03_build_index.yaml
    owner: note-indexer
  - id: t04_query_knowledge
    file: tasks/t04_query_knowledge.yaml
    owner: lexical-retriever
  - id: t05_generate_citations
    file: tasks/t05_generate_citations.yaml
    owner: citation-guardian
  - id: t06_synthesize_answer
    file: tasks/t06_synthesize_answer.yaml
    owner: knowledge-synthesizer
  - id: t07_map_backlinks
    file: tasks/t07_map_backlinks.yaml
    owner: graph-mapper
  - id: t08_detect_duplicates
    file: tasks/t08_detect_duplicates.yaml
    owner: graph-mapper
  - id: t09_generate_digest
    file: tasks/t09_generate_digest.yaml
    owner: knowledge-synthesizer
  - id: t10_quality_gate
    file: tasks/t10_quality_gate.yaml
    owner: quality-auditor

workflows:
  - id: setup_user
    file: workflows/setup_user.yaml
  - id: build_index
    file: workflows/build_index.yaml
  - id: update_index
    file: workflows/update_index.yaml
  - id: ask_vault
    file: workflows/ask_vault.yaml
  - id: generate_knowledge_map
    file: workflows/generate_knowledge_map.yaml
  - id: vault_digest
    file: workflows/vault_digest.yaml
  - id: curate_notes
    file: workflows/curate_notes.yaml
  - id: export_context
    file: workflows/export_context.yaml

outputs:
  - quality_report.json
  - knowledge_map.md
  - gap_report.md
  - weekly_digest.md
  - answer_with_citations.md
```

---

## 9. Componentes principais

### 9.1 Núcleo universal (determinístico)

Leitura de Markdown, extração de frontmatter/tags/headings/wikilinks, detecção de backlinks, chunking por estrutura Markdown, indexação incremental, busca lexical, resposta com citações e auditoria de qualidade.

### 9.2 Perfil do usuário

```yaml
user_profile:
  display_name: "Nome do usuário"
  language: "pt-BR"
  preferred_style: "objetivo"
  domain_focus: ["pesquisa", "gestão", "educação"]
  private_mode: true
```

### 9.3 Configuração do vault

```yaml
vault:
  path: "/caminho/para/o/vault"          # nunca fixo no código; vem da resolução do §4
  include_patterns: ["**/*.md"]
  exclude_patterns:
    - ".obsidian/**"
    - "Templates/**"
    - "Private/**"
    - "Anexos/**"
  max_file_size_mb: 5
  parse_frontmatter: true
  parse_wikilinks: true
  parse_tags: true
```

### 9.4 Adaptador do agente

```yaml
# config/adapters/generic.yaml
agent_adapter:
  name: "generic"
  invoke_style: "neutral"
  answer_voice: "professional"
  require_citations: true
  allow_agent_memory_write: false
```

```yaml
# config/adapters/maeve.yaml — SEM caminhos de dispositivo embutidos
agent_adapter:
  name: "maeve"
  invoke_style: "executive_orchestrator"
  answer_voice: "Maeve, pt-BR, profissional e direta"
  require_citations: true
  default_language: "pt-BR"
  delivery_path_env: "MAEVE_DELIVERY_PATH"   # caminho resolvido por env/config do usuário
  allow_agent_memory_write: false
```

---

## 10. Agentes do squad

| Agente | Função | Portabilidade | Tipo |
|---|---|---|---|
| **Vault Orchestrator** | Coordena execução e escolhe workflows. | Universal | LLM (orquestração) |
| **User Profile Resolver** | Lê config, idioma, vault e modo. | Universal | Determinístico |
| **Note Indexer** | Varre o vault e cria índice. | Universal | Determinístico |
| **Metadata Extractor** | Extrai frontmatter, tags, headings, datas. | Universal | Determinístico |
| **Lexical Retriever** | Busca textual via SQLite FTS5. | Universal | Determinístico |
| **Semantic Retriever** | Busca por embeddings quando disponível. | Opcional | LLM/embeddings |
| **Citation Guardian** | Garante rastreabilidade das respostas. | Universal | Determinístico + verificação |
| **Knowledge Synthesizer** | Produz sínteses, relatórios e materiais. | Adaptável por idioma/estilo | LLM |
| **Graph Mapper** | Mapeia links, backlinks, clusters e lacunas. | Universal | Determinístico |
| **Note Curator** | Sugere curadoria; escrita só autorizada. | Escrita requer autorização | LLM + patch determinístico |
| **Quality Auditor** | Verifica integridade, citações e segurança. | Universal | Determinístico |

---

## 11. Mapa determinístico × LLM (controle de custo de token)

> Regra do repositório: priorizar scripts determinísticos quando a etapa não exigir LLM. Só há chamada de modelo onde há geração/julgamento de linguagem natural.

| Etapa | Script determinístico | Precisa LLM? |
|---|---|:--:|
| Scan e parsing de notas | `obsidian_index.py` | Não |
| Extração de metadados/backlinks | `obsidian_index.py` | Não |
| Indexação FTS5 | `obsidian_index.py` | Não |
| Busca lexical e ranking | `obsidian_search.py` | Não |
| Seleção de trechos candidatos | `obsidian_query.py` | Não |
| Verificação de citação (trecho existe na fonte) | `obsidian_query.py` | Não |
| Grafo, clusters, duplicidades, órfãs | `obsidian_graph.py` | Não |
| Auditoria de qualidade | `obsidian_quality_audit.py` | Não |
| **Síntese/redação da resposta final** | — | **Sim** |
| **Curadoria: justificativa das sugestões** | patch via script | **Sim (texto)** |

Implicação: a maior parte do pipeline roda sem token. O LLM só entra na **síntese** e na **redação de justificativas**, sempre sobre trechos já recuperados e citáveis.

---

## 12. Modos de operação

| Modo | Descrição | Escrita no vault | Requer autorização |
|---|---|:--:|:--:|
| `read_only` | Lê, busca e responde com citações. | Não | Não |
| `suggest` | Sugere melhorias, tags, reorganizações. | Não | Não |
| `draft_patch` | Gera proposta em formato diff/patch. | Não aplica automaticamente | Sim, para aplicar |
| `write` | Altera notas diretamente. | Sim | Sim, explícita |
| `curate` | Reorganiza estrutura/tags/duplicidades. | Sim | Sim, explícita |

**Padrão público:** `read_only`.

---

## 13. Regras de segurança

1. Nunca alterar notas sem autorização explícita.
2. Nunca indexar segredos (tokens, chaves, `.env`).
3. Permitir exclusão de pastas privadas via `exclude_patterns`.
4. Mecanismo de exclusão é próprio do squad (via `exclude_patterns`/`config`); **não** se pressupõe um `.obsidianignore` nativo do Obsidian (ele não existe).
5. Separar resposta citada de inferência do agente.
6. Toda afirmação atribuída ao vault deve conter fonte.
7. O índice deve ser local por padrão.
8. Não enviar conteúdo do vault para APIs externas sem consentimento explícito.
9. Embeddings externos são opcionais, documentados e gated por consentimento (rule 8).
10. O modo `write` é bloqueado por padrão.
11. Nenhum conteúdo de vault, índice gerado ou caminho pessoal é commitado no repositório (ver `.gitignore`).

---

## 14. Índice local e modelos de dados

```text
.obsidian_knowledge_index/
├── vault.sqlite
├── notes_index.json
├── chunks_index.json
├── tags_index.json
├── backlinks_index.json
├── headings_index.json
├── attachments_index.json
├── last_scan.json
└── quality_report.json
```

### Registro de nota (ID estável)

```json
{
  "note_id": "uuid-estável-independente-do-caminho",
  "current_path": "Projetos/Exemplo.md",
  "previous_paths": [],
  "title": "Exemplo",
  "frontmatter": { "type": "project", "status": "active" },
  "tags": ["projeto", "pesquisa"],
  "headings": ["Resumo", "Referências", "Próximas ações"],
  "links_out": ["[[Nota Relacionada]]"],
  "links_in": [],
  "modified_at": "2026-06-18T10:00:00",
  "content_sha256": "...",
  "word_count": 1200,
  "language": "pt-BR"
}
```

> **Por que ID estável:** ID derivado do caminho quebra ao renomear/mover a nota e perde o histórico de backlinks. Usa-se um `note_id` estável + `previous_paths` para preservar relações entre scans.

### Registro de chunk

```json
{
  "chunk_id": "sha256:chunk",
  "note_id": "uuid-estável",
  "path": "Projetos/Exemplo.md",
  "heading": "Resumo",
  "text": "Trecho da nota...",
  "anchor_quote": "primeiras palavras do trecho",
  "start_line": 12,
  "end_line": 34,
  "tags": ["projeto"],
  "score": null
}
```

---

## 15. Busca híbrida

### Fase inicial (obrigatória, determinística)

- SQLite FTS5 para busca lexical;
- filtros por pasta, tag, heading e data;
- ranking por frequência, proximidade e metadados.

### Fase avançada (opcional)

- embeddings locais ou remotos; vector store; reranking; similaridade semântica; clusterização temática.

| Camada | Tecnologia sugerida | Obrigatória |
|---|---|:--:|
| Lexical | SQLite FTS5 | Sim |
| Metadados | SQLite/JSON | Sim |
| Backlinks | parser de wikilinks | Sim |
| Semântica | Chroma, FAISS ou LanceDB | Não |
| Embeddings | local ou API | Não |
| Grafo | NetworkX/JSON | Opcional |

---

## 16. Citações

Toda resposta baseada no vault deve produzir citações ancoradas em **caminho + heading + trecho literal**, com linha apenas como dica (linhas mudam entre edições).

### Citação mínima

```text
Fonte: Pasta/Nota.md > Heading
```

### Citação ideal

```json
{
  "path": "Pasta/Nota.md",
  "heading": "Heading",
  "anchor_quote": "Trecho citado literal (âncora estável)",
  "start_line": 10,
  "end_line": 24
}
```

> A âncora primária é `path > heading > anchor_quote`. `start_line/end_line` são auxiliares e podem desatualizar entre scans; o verificador de citação confirma que `anchor_quote` ainda existe na fonte antes de citar.

### Regra de ausência de fonte

> Não encontrei fonte suficiente no vault para afirmar isso como conhecimento do Obsidian.

---

## 17. Skills

### Skill universal — `generic-obsidian-knowledge`

```yaml
name: generic-obsidian-knowledge
description: Use when the user asks an agent to consult, search, synthesize, cite, map, or curate an Obsidian vault as a knowledge base. Works with any user-configured vault and defaults to read-only mode.
```

Ensina o agente a: carregar config do usuário; localizar o vault; usar o índice; buscar notas; responder com citações; não inventar conteúdo; pedir autorização antes de escrita; respeitar idioma e estilo.

### Adaptador Maeve — `maeve-obsidian-adapter` (opcional)

Ajusta idioma padrão (pt-BR), tom executivo, entrega em caminho **resolvido por env/config** (`MAEVE_DELIVERY_PATH`), integração com rotinas da Maeve, regra de não alterar vault sem autorização e resposta com fontes + síntese executiva.

**Regra de portabilidade:** o adaptador Maeve fica isolado e **não** é dependência do núcleo. Nenhum caminho de dispositivo, nome de usuário ou pasta pessoal é embutido no manifesto.

---

## 18. Workflows

- **Setup inicial:** usuário informa vault → valida caminho → cria config → scan → índice → testa consulta → `quality_report`.
- **Consulta ao vault:** pergunta → resolver perfil → buscar índice → selecionar trechos → validar citações → sintetizar → entregar fontes.
- **Atualização incremental:** ler `last_scan` → verificar hashes → reindexar alterados → remover deletados → atualizar backlinks → `quality_report`.
- **Mapa de conhecimento:** tema → buscar notas → mapear backlinks/tags/headings → clusters → mapa em Markdown/HTML.
- **Curadoria segura:** auditar → detectar duplicidades/lacunas/órfãs → sugestões → aguardar autorização → aplicar patch se permitido.

---

## 19. Produtos geráveis

Resposta com citações, síntese temática, relatório executivo, artigo, PRD, README, squad, plano de aula, plano de pesquisa, roteiro de vídeo, mapa de conhecimento, matriz de conceitos, digest semanal, relatório de lacunas, relatório de duplicidades, proposta de reorganização e exportação de contexto para outro agente.

---

## 20. Comandos previstos (padronizados em `python3`)

```bash
# Setup
python3 scripts/setup_user_profile.py --vault "/path/to/vault" --language "pt-BR" --adapter "generic" --mode "read_only"

# Indexação
python3 scripts/obsidian_index.py --config config/user.config.yaml

# Busca
python3 scripts/obsidian_search.py --config config/user.config.yaml --query "tema" --top-k 20

# Consulta com citações
python3 scripts/obsidian_query.py --config config/user.config.yaml --query "O que minhas notas dizem sobre isto?" --with-citations

# Mapa de conhecimento
python3 scripts/obsidian_graph.py --config config/user.config.yaml --topic "tema" --output examples/outputs/knowledge_map.md

# Auditoria
python3 scripts/obsidian_quality_audit.py --config config/user.config.yaml --output examples/outputs/quality_report.json

# Orquestrador CLI (entrypoint único de workflows)
python3 scripts/run_squad.py --workflow ask_vault --config config/user.config.yaml --query "..."
```

---

## 21. Critérios de aceite

O squad só é considerado funcional quando:

- aceitar configuração de vault por usuário (sem caminho fixo);
- não depender de Maeve nem de usuário específico;
- operar com adaptador genérico e com adaptador Maeve quando configurado;
- indexar notas Markdown e extrair frontmatter, tags, headings, links e backlinks;
- criar índice persistente e executar busca textual;
- retornar resultados com caminho, heading e trecho;
- gerar resposta com citações verificadas;
- operar em `read_only` por padrão e bloquear escrita sem autorização;
- excluir pastas privadas configuradas;
- gerar `quality_report.json`;
- passar nos testes mínimos;
- **passar no `validate_squad.py` com `go_no_go: "go"`** (pastas/arquivos obrigatórios presentes, manifesto consistente, sem segredos);
- **estar registrado no `SQUAD_INDEX.md`.**

### Metas mensuráveis (opcionais, recomendadas)

| Métrica | Alvo |
|---|---|
| Reindex incremental | só arquivos alterados desde `last_scan` |
| Tempo de indexação | ≤ ~1 s por 100 notas em hardware modesto |
| Verificação de citação | 100% das citações com `anchor_quote` presente na fonte |
| Vazamento de segredos | 0 (validado por `validate_squad.py`) |

---

## 22. Testes obrigatórios

| Teste | Objetivo |
|---|---|
| `test_setup_profile.py` | Criação de perfil por usuário. |
| `test_index.py` | Indexação de notas Markdown. |
| `test_frontmatter.py` | Extração de YAML/frontmatter. |
| `test_links.py` | Wikilinks e backlinks. |
| `test_search.py` | Busca lexical (FTS5). |
| `test_citations.py` | Fontes e trechos citáveis verificáveis. |
| `test_graph.py` | Grafo, backlinks, clusters. |
| `test_permissions.py` | Bloqueio de escrita sem autorização. |
| `test_adapters.py` | Adaptador genérico e Maeve. |
| `test_quality.py` | Quality report. |

---

## 23. Publicação no repositório

- **Caminho:** `Squads-Genius/squads/universal-obsidian-knowledge-squad/`
- Publicado como ferramenta universal; o adaptador Maeve existe dentro dele, mas **não** é dependência obrigatória.
- Após criar: **registrar em `SQUAD_INDEX.md`**.
- Validar com `python3 squads/maeve-genius-forge-squad/scripts/validate_squad.py --root squads/universal-obsidian-knowledge-squad` antes de considerar concluído.
- **Não** criar pull request nem release sem autorização explícita do usuário.

---

## 24. Regra de incorporação por agentes

```text
Universal Obsidian Knowledge Squad + Maeve Adapter   = extensão operacional da Maeve
Universal Obsidian Knowledge Squad + Generic Adapter = assistente Obsidian neutro
Universal Obsidian Knowledge Squad (CLI)             = ferramenta local de indexação e consulta
```

---

## 25. Escopo da v1 e fora de escopo

**Na v1:** vault único; busca lexical determinística; citações verificadas; adaptadores generic/maeve; modos read_only/suggest/draft_patch.

**Fora de escopo da v1 (futuro):** multi-vault simultâneo; semântica/embeddings (opcional, desligado por padrão); aplicação automática de `write`/`curate` sem confirmação.

---

## 26. Conclusão

O squad nasce universal: núcleo neutro e determinístico, configuração por usuário, adaptador genérico, adaptador Maeve opcional e isolado, read-only por padrão, citações verificadas, escrita protegida, indexação local, busca lexical inicial e RAG semântico opcional. Funciona via agente ou via CLI, sem carregar identidade, caminhos ou preferências de qualquer usuário anterior.

---

**Tipo:** Squad universal / Obsidian knowledge harness
**Compatibilidade:** Hermes Agent, agentes compatíveis, CLI local
**Modo padrão:** read-only

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
