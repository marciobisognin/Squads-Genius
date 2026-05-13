# instagram-carrossel-visual-pro

**Nome técnico:** `instagram-carrossel-visual-pro`
**Slug no repositório:** `instagram-carrossel-visual-pro`
**Versão:** `1.0.0`
**Número na seleção original:** 5

## Visão geral

Squad para criar carrosséis premium de Instagram com PPT e vídeo Manim.

## Para que serve

Produzir carrosséis visuais profissionais com estrutura narrativa, design de slides e apoio de geração/exportação visual para apresentações e redes sociais.

## Estrutura operacional

- **Agentes:** 8
- **Tasks:** 8
- **Workflows:** 2
- **Scripts:** 2
- **Arquivos totais publicados:** 40

## Agentes

- `agents/carousel-copywriter.md` — description: Escreve copy slide a slide para Instagram.
- `agents/carousel-orchestrator.md` — description: Orquestra o pipeline completo do carrossel ao vídeo.
- `agents/carousel-strategist.md` — description: Define objetivo editorial e narrativa do carrossel.
- `agents/instagram-publisher.md` — description: Prepara e publica pacote final no Instagram.
- `agents/manim-video-producer.md` — description: Cria vídeo explicativo em Manim.
- `agents/ppt-producer.md` — description: Monta a versão final em PPT.
- `agents/typography-color-engineer.md` — description: Seleciona tipografia e combinações de cor por tema.
- `agents/visual-director.md` — description: Define direção de arte e composição visual por slide.

## Tasks principais

- `tasks/assemble-publish-package.md` — Task: assemble-publish-package
- `tasks/build-manim-video.md` — Task: build-manim-video
- `tasks/build-ppt-deliverable.md` — Task: build-ppt-deliverable
- `tasks/build-visual-system.md` — Task: build-visual-system
- `tasks/collect-briefing.md` — Task: collect-briefing
- `tasks/design-narrative-arc.md` — Task: design-narrative-arc
- `tasks/produce-slide-assets.md` — Task: produce-slide-assets
- `tasks/write-carousel-copy.md` — Task: write-carousel-copy

## Workflows

- `workflows/carrossel_premium_pipeline.yaml`
- `workflows/rapid_restyle_pipeline.yaml`

## Scripts e automação

- `scripts/build-deliverables.cjs`
- `scripts/validate-package.cjs`

## Como usar

1. Abra o arquivo `squad.yaml` para identificar nome, versão, agentes, tasks e workflows.
2. Leia os arquivos em `agents/` para entender os papéis especializados.
3. Execute as tasks em `tasks/` conforme o fluxo indicado em `workflows/`.
4. Quando houver scripts em `scripts/`, use-os como automações auxiliares; revise dependências antes de executar.
5. Registre saídas, decisões e evidências nos diretórios de documentação ou geração previstos pelo próprio squad.

## Arquivos de referência

- `README.md`
- `squad.yaml`

## Propriedade intelectual e licença

- Licença padrão adotada para novos squads de Marcio: MIT.
- Criado por: Marcio Bisognin.
- Instagram: [@marciobisognin](https://instagram.com/marciobisognin).
- Observação: squads legados foram publicados preservando sua estrutura original; quando não houver arquivo de licença interno, considere a política do repositório e a documentação de cada pasta.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
