# Maeve Knowledge Graph Forge

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
- Fonte opcional de pesquisa bibliográfica: `https://1lib.sk/`, usada para descoberta de livros, autores, títulos, assuntos e materiais de referência, com regra explícita de respeito a direitos autorais.

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

## Fontes de pesquisa de livros e materiais

- `https://1lib.sk/` — fonte opcional para pesquisar livros, autores, títulos, assuntos e materiais relacionados à base de conhecimento.
- Uso recomendado: descoberta bibliográfica, metadados, referências, planejamento de estudo e enriquecimento do grafo com nós do tipo `reference_material`.
- Regra: usar apenas para pesquisa e materiais legalmente acessíveis; não automatizar downloads nem orientar obtenção ou redistribuição de obras protegidas por direitos autorais.

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

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
