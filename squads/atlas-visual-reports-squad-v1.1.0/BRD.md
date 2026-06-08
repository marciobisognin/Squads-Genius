# BRD — Squad de Design para Relatórios Premium de Grandes Empresas

**Nome provisório do squad:** `premium-report-design-squad`
**Versão do BRD:** 1.0
**Status:** proposta para validação antes da criação do squad
**Objetivo:** especificar um squad multiagente capaz de transformar relatórios pré-preenchidos em experiências visuais premium, entregues em **site HTML** e **PDF executivo**, com forte uso de infográficos, gráficos, mapas mentais, fluxogramas, storytelling visual e apêndice técnico organizado.

---

## 1. Visão executiva

O objetivo do `premium-report-design-squad` é criar relatórios com padrão visual compatível com grandes empresas, consultorias e relatórios anuais corporativos. O squad não deve apenas “formatar” um Markdown ou documento textual. Ele deve reconstruir a informação em uma experiência de comunicação executiva.

O resultado final deve ter três camadas:

1. **Camada executiva visual**
   Uma abertura altamente visual, destinada a diretores, conselheiros e gestores que precisam entender rapidamente o tema, os números, os riscos, as decisões e o caminho recomendado.

2. **Camada analítica visual detalhada**
   Uma seção intermediária com mais profundidade, ainda baseada em gráficos, mapas, fluxos, painéis, matrizes, comparações e storyboards visuais.

3. **Camada técnica / apêndice**
   Conteúdo detalhado, tabelas, metodologia, premissas, evidências, dados brutos, referências e textos longos. Essa camada preserva rigor técnico sem prejudicar a leitura executiva.

O squad deve gerar:

- **site HTML premium**, responsivo e navegável;
- **PDF A4 retrato ou paisagem**, conforme escolha do usuário, sem cortes, sem estouro de bordas e com qualidade de impressão;
- opcionalmente, imagens/figuras em SVG/PNG para reaproveitamento em apresentações.

---

## 2. Contexto e problema

Relatórios corporativos frequentemente partem de documentos longos, densos e técnicos. Quando simplesmente convertidos para PDF, tornam-se cansativos, pouco executivos e visualmente fracos. O problema central não é falta de conteúdo, mas falta de arquitetura visual.

O usuário deseja um sistema capaz de receber:

- relatório pré-preenchido em Markdown, DOCX, PDF, HTML, planilha ou texto estruturado;
- material de pesquisa;
- dados quantitativos;
- informações da empresa, nicho ou setor;
- preferências visuais;
- exigências de saída em HTML e PDF.

A partir disso, o squad deve:

- diagnosticar o tipo de relatório;
- selecionar linguagem visual adequada ao setor;
- definir paleta de cores e tipografia;
- criar narrativa executiva;
- transformar texto em diagramas, mapas e infográficos;
- criar site HTML premium;
- gerar PDF final validado.

---

## 3. Pesquisa de referências e padrões observados

A pesquisa considerou referências de templates premium, relatórios anuais, consultorias, dashboards executivos, design systems e visualização de dados.

### 3.1 Fontes e benchmarks verificados

#### Templates e repertório visual

- **Envato Elements — Annual Report Graphic Templates**
  Referência para relatórios anuais, layouts editoriais, capas, grids, infográficos, páginas de KPIs e relatórios corporativos com aparência premium.

- **Behance — Annual Report Projects**
  Benchmark visual para relatórios institucionais, ESG, branding, relatórios de impacto, apresentações editoriais e peças com forte direção de arte.

- **Dribbble — Annual Report / Report Design**
  Referência para micro-layouts, cards, dashboards, componentes modernos, capas e padrões visuais contemporâneos.

- **Microsoft Create — Report Templates**
  Templates corporativos mais acessíveis e aplicáveis a documentos, relatórios e apresentações executivas.

- **Canva, Adobe Stock, Adobe Express, Figma Community e Piktochart**
  Referências complementares de templates para relatórios, dashboards e infográficos. Algumas páginas podem bloquear acesso automatizado, mas são úteis para curadoria visual manual.

#### Relatórios corporativos reais

- **AnnualReports.com**
  Base ampla para benchmarking de relatórios anuais reais de empresas listadas.

- **LSEG Annual Reports**
  Exemplo de relatório corporativo de investor relations, com narrativa estratégica, governança e performance.

- **Unilever Annual Report and Accounts**
  Referência de relatório global com estratégia, desempenho, accountability, governança e clareza institucional.

#### Consultorias e comunicação executiva

- **Deloitte Insights**
  Referência para relatórios de mercado, linguagem executiva, storytelling de insights e estrutura de decisão.

- **PwC C-suite Insights**
  Referência para comunicação C-level, relatórios orientados a decisão e design sóbrio.

#### Visualização de dados e dashboards

- **Microsoft Power BI Design Tips**
  Boas práticas de dashboards: hierarquia, escolha de visuais, clareza, foco em informação acionável e composição visual.

- **Power BI Samples / Visualizations Overview**
  Catálogo útil para exemplos de gráficos, KPIs, segmentações, painéis e relatórios analíticos.

- **Storytelling with Data**
  Referência para redução de ruído, títulos acionáveis, clareza narrativa e visualização orientada à mensagem.

- **IBCS Standards**
  Padrões de comunicação executiva para relatórios de negócios: consistência visual, comparabilidade, semântica, notação e qualidade analítica.

- **From Data to Viz**
  Referência para seleção adequada do tipo de gráfico conforme a natureza dos dados e a pergunta analítica.

#### Design, acessibilidade e experiência

- **W3C / WCAG**
  Contraste, legibilidade, semântica e acessibilidade.

- **Material Design**
  Fundamentos de cor, tipografia, hierarquia, componentes e sistema visual.

- **GOV.UK Service Manual**
  Clareza textual, escrita objetiva, estrutura orientada ao usuário e acessibilidade.

---

## 4. Padrões visuais recorrentes nos melhores relatórios

### 4.1 Estrutura editorial premium

Os melhores relatórios não começam com texto longo. Eles começam com uma tese visual.

Padrões observados:

- capa forte, com título claro e identidade visual consistente;
- abertura executiva com KPIs principais;
- seções com respiro visual;
- páginas com uma ideia principal por tela/página;
- grids rigorosos;
- hierarquia tipográfica clara;
- alternância entre páginas de impacto, páginas analíticas e páginas técnicas.

### 4.2 Storytelling executivo

Relatórios premium geralmente seguem a lógica:

1. O que está acontecendo?
2. Por que importa?
3. Quais dados sustentam?
4. Qual risco ou oportunidade existe?
5. Qual decisão deve ser tomada?
6. Qual plano operacional viabiliza a decisão?

Em vez de títulos neutros como “Resultados”, usam títulos interpretativos, por exemplo:

- “Margem melhora, mas depende da redução de CAC”;
- “Risco regulatório é o principal bloqueador de escala”;
- “Três mercados concentram 78% da oportunidade”.

### 4.3 Visual-first

Os relatórios mais fortes usam a primeira camada como painel visual:

- mapas mentais;
- infográficos de tese;
- dashboards;
- funis;
- roadmaps;
- matrizes de risco;
- organogramas;
- mapas de stakeholders;
- cards de decisão;
- diagramas de causa e efeito.

Texto longo entra como suporte, não como eixo principal.

### 4.4 Sistemas visuais, não páginas isoladas

Os melhores templates são sistemas:

- paleta fixa;
- tipografia consistente;
- grid recorrente;
- componentes reutilizáveis;
- padrões de gráficos;
- ícones coerentes;
- linguagem visual adequada ao setor.

---

## 5. Objetivos de negócio do squad

### 5.1 Objetivo principal

Criar um squad multiagente que transforme relatórios densos em produtos visuais premium, com padrão de grandes empresas, entregues em HTML e PDF.

### 5.2 Objetivos específicos

- Reduzir densidade textual da camada principal.
- Aumentar compreensão executiva imediata.
- Escolher paleta de cores conforme empresa, setor ou tema.
- Escolher tipografia conforme tom: institucional, técnico, acadêmico, comercial, financeiro, ESG, educacional ou estratégico.
- Selecionar gráficos adequados ao tipo de dado.
- Criar infográficos e diagramas para explicar conceitos complexos.
- Criar PDF sem cortes, sem bordas estouradas e com layout A4 validado.
- Criar HTML responsivo, navegável e visualmente atrativo.
- Preservar conteúdo técnico em apêndice organizado.
- Garantir consistência visual entre HTML e PDF.

---

## 6. Escopo funcional

### 6.1 Entradas aceitas

O squad deve aceitar:

- Markdown `.md`;
- texto colado pelo usuário;
- DOCX;
- PDF textual;
- planilhas CSV/XLSX;
- JSON;
- imagens de referência visual;
- links de sites ou relatórios de referência;
- logotipo e brand kit da empresa;
- briefing textual do usuário;
- dados de pesquisa;
- fontes bibliográficas;
- relatórios pré-preenchidos.

### 6.2 Saídas obrigatórias

- `index.html` ou site estático equivalente;
- `styles.css` ou sistema de estilos embutido/organizado;
- assets em `assets/` quando necessário;
- PDF final em A4 retrato ou paisagem;
- arquivo de especificação visual do relatório;
- relatório de QA visual e técnico.

### 6.3 Saídas opcionais

- slides executivos;
- imagens PNG/SVG de gráficos;
- versão one-page executive brief;
- versão board deck;
- pacote de templates reutilizáveis;
- README do relatório;
- versão dark mode para HTML.

---

## 7. Estrutura recomendada do relatório produzido

### 7.1 Parte 1 — Executive Visual Layer

Finalidade: permitir que um executivo entenda o relatório em poucos minutos.

Componentes:

- capa premium;
- tese central visual;
- KPIs hero;
- mapa mental principal;
- dashboard executivo;
- matriz de riscos/oportunidades;
- roadmap ou fluxo de decisão;
- resumo visual de recomendações.

Características:

- pouco texto;
- frases curtas;
- números grandes;
- gráficos claros;
- visual de alta percepção de valor.

### 7.2 Parte 2 — Analytical Visual Layer

Finalidade: explicar as evidências e análises com profundidade moderada.

Componentes:

- seções analíticas por tema;
- gráficos comparativos;
- séries temporais;
- heatmaps;
- funis;
- mapas de stakeholders;
- organogramas;
- fluxos operacionais;
- diagramas de causa e efeito;
- cards de interpretação.

Características:

- densidade média;
- visual ainda predominante;
- texto explicativo curto;
- foco em evidência e implicação.

### 7.3 Parte 3 — Technical Appendix

Finalidade: preservar rigor e auditabilidade.

Componentes:

- texto completo do relatório original;
- metodologia;
- premissas;
- tabelas completas;
- dados detalhados;
- referências;
- notas técnicas;
- limitações;
- anexos.

Características:

- pode ser mais textual;
- deve ser bem paginado;
- tabelas devem quebrar corretamente;
- não deve prejudicar a leitura executiva.

---

## 8. Agentes do squad

### 8.1 Maestro de Relatório Premium

**Função:** coordenar o squad inteiro.
**Responsabilidades:**

- interpretar o pedido do usuário;
- confirmar tipo de relatório, público e formato;
- distribuir tarefas para agentes especialistas;
- garantir coerência entre conteúdo, design, HTML e PDF;
- aprovar a versão final antes da entrega.

**Entradas:** briefing do usuário, relatório pré-preenchido, dados e referências.
**Saídas:** plano de produção, checklist de aprovação e decisão final de release.

---

### 8.2 Agente de Intake e Diagnóstico

**Função:** entender o material recebido.
**Responsabilidades:**

- classificar tipo de relatório;
- identificar público-alvo;
- detectar setor/nicho;
- mapear objetivos do documento;
- identificar se o material é estratégico, financeiro, ESG, acadêmico, operacional, comercial, técnico ou institucional;
- identificar restrições de marca, compliance e linguagem.

**Saídas:** `project_brief.json` e diagnóstico textual.

---

### 8.3 Agente de Pesquisa e Benchmark Visual

**Função:** buscar referências de design aplicáveis ao tipo de relatório.
**Responsabilidades:**

- pesquisar templates e relatórios de grandes empresas;
- identificar padrões de layout aplicáveis;
- propor moodboard visual;
- classificar referências por tipo: annual report, ESG, dashboard, board deck, consulting report, institutional report;
- recomendar estilos visuais compatíveis com o nicho.

**Saídas:** `research_benchmark.md`, lista de referências, moodboard conceitual.

---

### 8.4 Agente de Estratégia Narrativa

**Função:** transformar conteúdo bruto em narrativa executiva.
**Responsabilidades:**

- definir tese central do relatório;
- criar estrutura de leitura;
- separar conteúdo em camadas: executivo, analítico e técnico;
- transformar títulos descritivos em títulos interpretativos;
- definir mensagens-chave por página;
- reduzir excesso de texto na camada principal.

**Saídas:** `editorial_plan.md`, mapa de seções, títulos executivos.

---

### 8.5 Agente de Dados e Evidências

**Função:** validar e estruturar dados.
**Responsabilidades:**

- identificar KPIs, métricas, percentuais e tendências;
- separar dados confiáveis, ausentes ou inconsistentes;
- mapear tabelas que devem virar gráficos;
- registrar origem dos dados;
- preservar números sem alterar significado;
- sinalizar lacunas.

**Saídas:** `data_profile.json`, lista de KPIs, mapa de evidências.

---

### 8.6 Agente de Paleta e Identidade Visual

**Função:** definir cores conforme empresa, setor, tema e tom.
**Responsabilidades:**

- extrair cores de logotipo ou brand kit quando fornecidos;
- inferir paleta setorial quando não houver brand kit;
- definir cores primárias, secundárias, neutras e semânticas;
- garantir contraste adequado;
- diferenciar cores de alerta, risco, oportunidade, status e destaque;
- criar tokens de cor.

**Exemplos de paleta por setor:**

- financeiro: azul profundo, verde, cinzas, branco;
- saúde: azul, verde, branco, tons suaves;
- educação: azul, roxo, amarelo moderado;
- tecnologia: azul, ciano, violeta, dark mode controlado;
- ESG: verdes, terra, neutros, azul institucional;
- jurídico/institucional: vinho, azul marinho, dourado, cinza;
- varejo/marketing: cores mais vibrantes com controle de contraste.

**Saídas:** `design_tokens.colors.json`, paleta comentada.

---

### 8.7 Agente de Tipografia e Hierarquia Editorial

**Função:** definir fontes e hierarquia de leitura.
**Responsabilidades:**

- escolher fontes para título, subtítulo, corpo, legenda e números;
- garantir legibilidade em HTML e PDF;
- definir escala tipográfica;
- ajustar densidade de texto;
- definir padrões para títulos executivos, callouts, notas e apêndices;
- evitar fontes decorativas que prejudiquem leitura.

**Diretriz:**

- relatórios executivos: sans-serif limpa + serif editorial opcional;
- relatórios acadêmicos/técnicos: serif para títulos, sans-serif para corpo ou vice-versa com alta legibilidade;
- dashboards: sans-serif forte, números bem legíveis;
- relatórios premium institucionais: combinação editorial com boa hierarquia.

**Saídas:** `design_tokens.typography.json`, escala tipográfica.

---

### 8.8 Agente de Design System / Atomic Design

**Função:** criar sistema visual reutilizável.
**Responsabilidades:**

- definir átomos: cores, fontes, ícones, linhas, sombras, espaçamentos;
- definir moléculas: cards, badges, callouts, KPI cards, legendas;
- definir organismos: capa, dashboard, mapa mental, matriz, timeline, seção analítica;
- definir templates: executive summary, analytical page, appendix page;
- garantir consistência visual.

**Saídas:** `design_system.md`, tokens, componentes e regras visuais.

---

### 8.9 Agente de Infográficos e Comunicação Visual

**Função:** converter texto e dados em peças visuais.
**Responsabilidades:**

- criar mapas mentais;
- criar fluxogramas;
- criar roadmaps;
- criar funis;
- criar matrizes 2x2;
- criar mapas de stakeholders;
- criar diagramas de causa e efeito;
- criar storyboards visuais;
- criar bento grids e cards de insight.

**Layouts disponíveis:**

- dashboard;
- bento grid;
- hub-and-spoke;
- tree branching;
- winding roadmap;
- circular flow;
- funnel;
- comparison matrix;
- iceberg;
- bridge problem-solution;
- dense modules;
- jigsaw/interconnected parts;
- structural breakdown.

**Saídas:** especificações de infográficos e SVG/HTML dos blocos visuais.

---

### 8.10 Agente de Visualização de Dados

**Função:** escolher gráficos corretos e produzir visualizações.
**Responsabilidades:**

- selecionar gráfico conforme intenção analítica;
- evitar gráficos inadequados;
- criar séries temporais, barras, ranking, waterfall, heatmap, scatter, bubble, treemap, radar quando justificável;
- usar SVG sempre que possível;
- aplicar títulos interpretativos;
- destacar mensagens com anotações visuais;
- criar legendas claras.

**Regras:**

- evolução no tempo → linha/área;
- comparação entre categorias → barras;
- composição simples → barras empilhadas ou donut com poucas categorias;
- variação de ponte → waterfall;
- concentração → heatmap;
- correlação → scatter/bubble;
- hierarquia → treemap;
- processo → fluxo/timeline;
- decisão → matriz ou árvore.

**Saídas:** `chart_specs.json`, gráficos em SVG/HTML.

---

### 8.11 Agente de UX do Site HTML

**Função:** desenhar experiência navegável do relatório em HTML.
**Responsabilidades:**

- criar navegação por seções;
- definir abertura visual;
- criar índice lateral ou superior;
- definir blocos recolhíveis para apêndice;
- garantir responsividade;
- prever animações discretas;
- melhorar leitura em desktop, tablet e mobile.

**Recursos possíveis:**

- navegação sticky;
- cards animados;
- microinterações;
- scroll progress;
- tabs;
- accordions;
- tooltips;
- gráficos interativos;
- mapas mentais expansíveis.

**Saídas:** wireframe HTML e especificação de UX.

---

### 8.12 Agente Front-end / HTML-CSS-JS

**Função:** implementar o relatório como site.
**Responsabilidades:**

- gerar HTML semântico;
- criar CSS premium;
- integrar gráficos e diagramas;
- aplicar design tokens;
- garantir responsividade;
- otimizar assets;
- preparar versão print.

**Stack recomendada:**

- HTML5 semântico;
- CSS moderno;
- CSS Grid e Flexbox;
- SVG inline;
- JavaScript modular;
- Astro, React ou Vite quando houver necessidade de componentes;
- Tailwind CSS opcional, controlado por tokens;
- ECharts SVG;
- D3 SVG;
- Mermaid;
- Markmap;
- Cytoscape.js quando houver grafos complexos.

**Saídas:** `index.html`, `styles.css`, `scripts.js`, assets.

---

### 8.13 Agente de PDF e Print Engineering

**Função:** transformar o HTML em PDF com qualidade de impressão.
**Responsabilidades:**

- criar stylesheet específico para PDF;
- configurar `@page`;
- escolher A4 retrato ou paisagem;
- evitar cortes e estouro de bordas;
- ajustar grids para impressão;
- validar cabeçalhos, rodapés e numeração;
- incorporar fontes;
- garantir que gráficos caibam na página;
- remover metadados de geração quando solicitado.

**Ferramentas recomendadas:**

- Playwright/Chromium para fidelidade HTML/CSS/JS;
- Puppeteer como alternativa;
- WeasyPrint para documentos editoriais estáticos;
- qpdf para validação;
- mutool para renderizar prévias PNG;
- pypdf para limpeza de metadados quando necessário.

**Saídas:** PDF final e relatório de validação.

---

### 8.14 Agente de QA Visual

**Função:** auditar aparência e organização.
**Responsabilidades:**

- verificar se elementos saem das bordas;
- verificar se textos estouram cards;
- verificar se gráficos estão legíveis;
- verificar contraste;
- verificar consistência entre páginas;
- verificar alinhamento, espaçamento e hierarquia;
- revisar páginas renderizadas em PNG antes da entrega.

**Saídas:** `visual_qa_report.md`.

---

### 8.15 Agente de QA Factual e Editorial

**Função:** garantir fidelidade do conteúdo.
**Responsabilidades:**

- conferir se números foram preservados;
- verificar se estatísticas não foram alteradas;
- sinalizar dados sem fonte;
- revisar coerência textual;
- evitar afirmações inventadas;
- preservar termos técnicos relevantes;
- remover segredos, tokens ou credenciais caso apareçam.

**Saídas:** `content_qa_report.md`.

---

### 8.16 Agente de Empacotamento e Entrega

**Função:** organizar arquivos finais.
**Responsabilidades:**

- salvar entregas no diretório definido;
- criar estrutura limpa de arquivos;
- garantir que HTML abra localmente;
- garantir que PDF esteja validado;
- preparar pacote final;
- enviar arquivos ao usuário.

**Saídas:** pacote final com HTML, PDF, assets e logs mínimos de validação.

---

## 9. Pipeline operacional do squad

### Fase 1 — Intake e diagnóstico

1. Receber relatório pré-preenchido e materiais de pesquisa.
2. Identificar setor, objetivo, público e formato final.
3. Classificar tipo de relatório.
4. Extrair KPIs, seções, dados, riscos e recomendações.
5. Criar briefing estruturado.

### Fase 2 — Pesquisa e direção visual

1. Pesquisar referências de relatórios semelhantes.
2. Definir estilo visual.
3. Definir paleta.
4. Definir tipografia.
5. Definir densidade textual e nível de visual-first.
6. Criar design system inicial.

### Fase 3 — Arquitetura editorial

1. Definir tese central.
2. Separar conteúdo em três camadas.
3. Criar sumário executivo visual.
4. Transformar textos longos em blocos visuais.
5. Definir quais dados viram gráficos.
6. Definir quais relações viram mapas mentais, fluxos ou organogramas.

### Fase 4 — Produção visual

1. Criar capa premium.
2. Criar dashboard executivo.
3. Criar infográficos principais.
4. Criar gráficos e diagramas.
5. Criar seção analítica visual.
6. Criar apêndice técnico.

### Fase 5 — Implementação HTML

1. Gerar HTML semântico.
2. Criar CSS com tokens.
3. Integrar JS, gráficos e diagramas.
4. Testar responsividade.
5. Servir localmente para revisão.
6. Enviar link/arquivo HTML para aprovação.

### Fase 6 — Geração PDF

1. Criar versão print específica.
2. Ajustar A4 retrato ou paisagem.
3. Remover interações incompatíveis com PDF.
4. Renderizar PDF.
5. Validar com qpdf/mutool.
6. Gerar prévias PNG de páginas-chave.
7. Corrigir cortes/estouros.
8. Entregar PDF final.

---

## 10. Requisitos funcionais

### RF01 — Importação de conteúdo

O squad deve receber relatório pré-preenchido em múltiplos formatos e converter para estrutura interna.

### RF02 — Briefing de design

O squad deve identificar público, finalidade, tom, setor, formato e densidade desejada.

### RF03 — Paleta automática ou guiada

O squad deve definir paleta com base em:

- brand kit fornecido;
- logotipo;
- setor;
- tema;
- tom institucional;
- preferências do usuário.

### RF04 — Tipografia contextual

O squad deve selecionar fontes e hierarquia conforme tipo de relatório.

### RF05 — Storytelling visual

O squad deve transformar o relatório em narrativa visual com tese, evidências e decisões.

### RF06 — Seleção automática de gráficos

O squad deve recomendar e gerar gráficos adequados ao tipo de dado.

### RF07 — Geração de infográficos

O squad deve gerar mapas mentais, fluxos, funis, matrizes, roadmaps e organogramas.

### RF08 — Geração de HTML

O squad deve entregar site HTML navegável e responsivo.

### RF09 — Geração de PDF

O squad deve entregar PDF A4 validado.

### RF10 — QA visual

O squad deve verificar se não há cortes, estouros, sobreposição ou gráficos ilegíveis.

### RF11 — QA factual

O squad deve preservar números, fontes e conclusões relevantes.

### RF12 — Apêndice técnico

O squad deve preservar conteúdo detalhado em seção final organizada.

---

## 11. Requisitos não funcionais

- Alta qualidade visual.
- Consistência entre HTML e PDF.
- Responsividade no HTML.
- PDF sem cortes e sem estouro de bordas.
- Legibilidade em A4.
- Contraste adequado.
- Reprodutibilidade do pipeline.
- Modularidade de componentes.
- Possibilidade de trocar tema/brand kit.
- Compatibilidade com execução local em Termux quando necessário.
- Segurança: remoção de credenciais, tokens ou segredos.
- Auditabilidade: preservar origem dos dados e decisões visuais.

---

## 12. Stack técnica recomendada

### 12.1 Base

- HTML5 semântico;
- CSS moderno;
- CSS Grid;
- Flexbox;
- SVG;
- JavaScript modular.

### 12.2 Framework opcional

Para relatórios simples:

- HTML/CSS/JS puro.

Para relatórios complexos ou reutilizáveis:

- Astro;
- React + Vite;
- Next.js quando houver necessidade de aplicação mais robusta.

### 12.3 Design system

- CSS variables/tokens;
- Tailwind CSS opcional;
- tokens de cor, tipografia, espaçamento, bordas e sombras;
- componentes reutilizáveis.

### 12.4 Gráficos

- ECharts com renderer SVG para dashboards executivos;
- D3.js para infográficos customizados;
- Chart.js apenas para gráficos simples;
- SVG inline para qualidade em PDF.

### 12.5 Diagramas

- Mermaid para fluxogramas, timelines, sequence diagrams e mindmaps simples;
- Markmap para mapas mentais a partir de Markdown;
- Cytoscape.js para redes complexas;
- Dagre/ELK.js para layout automático de grafos.

### 12.6 PDF

- Playwright/Chromium como padrão para HTML/CSS/JS;
- Puppeteer como alternativa;
- WeasyPrint para relatórios editoriais estáticos;
- qpdf para validação;
- mutool para prévias visuais;
- pypdf para limpeza de metadados quando necessário.

---

## 13. Diretrizes de PDF sem cortes

O squad deve aplicar regras específicas para PDF, não apenas imprimir o HTML de tela.

### Regras obrigatórias

- Definir `@page` explicitamente.
- Usar A4 retrato como padrão, salvo pedido de paisagem.
- Evitar grids largos no modo retrato.
- Usar 1 ou 2 colunas no PDF A4 retrato.
- Evitar `height: 100vh` no print.
- Evitar `overflow: hidden` em blocos textuais.
- Usar `overflow-wrap:anywhere` em textos longos.
- Usar `table-layout: fixed` em tabelas.
- Usar `max-width:100%` para imagens, SVGs e gráficos.
- Renderizar prévias PNG de páginas internas.
- Revisar visualmente capa, páginas de gráficos, páginas de tabela e apêndice.

### Critérios de validação

- PDF abre corretamente.
- `qpdf --check` sem erros.
- Páginas em A4 correto.
- Nenhum texto cortado.
- Nenhum gráfico fora da página.
- Nenhum card sobreposto.
- Tabelas quebram de forma legível.
- Fontes e acentos corretos.
- Arquivo final não contém metadados indesejados quando solicitado.

---

## 14. Animações e interatividade

O HTML pode conter animações discretas, mas o PDF deve ter fallback estático.

### HTML pode usar

- reveal on scroll;
- transições suaves;
- tooltips;
- tabs;
- accordions;
- gráficos interativos;
- filtros simples;
- navegação sticky;
- highlights progressivos;
- mapas mentais expansíveis.

### PDF deve usar

- estado visual final estático;
- gráficos já renderizados;
- diagramas sem dependência de interação;
- layout paginado e previsível.

---

## 15. Contratos de dados entre agentes

### 15.1 Project Brief

```json
{
  "report_type": "annual_report | executive_report | ESG | financial | academic | strategic | operational | consulting",
  "audience": "executives | board | technical_team | public | investors",
  "sector": "string",
  "tone": "institutional | premium | technical | didactic | financial | academic",
  "format": "html_and_pdf",
  "pdf_orientation": "portrait | landscape",
  "brand_assets": [],
  "constraints": []
}
```

### 15.2 Data Profile

```json
{
  "kpis": [],
  "tables": [],
  "charts_needed": [],
  "risks": [],
  "opportunities": [],
  "missing_data": [],
  "source_notes": []
}
```

### 15.3 Design System

```json
{
  "colors": {
    "primary": "#000000",
    "secondary": "#000000",
    "neutral": [],
    "semantic": {
      "risk": "#000000",
      "warning": "#000000",
      "success": "#000000"
    }
  },
  "typography": {
    "title": "string",
    "body": "string",
    "numeric": "string"
  },
  "components": []
}
```

### 15.4 Chart Spec

```json
{
  "chart_id": "string",
  "purpose": "comparison | trend | composition | correlation | ranking | distribution",
  "recommended_chart": "bar | line | heatmap | waterfall | scatter | treemap | funnel",
  "data_source": "string",
  "title": "string",
  "annotation": "string"
}
```

### 15.5 QA Report

```json
{
  "visual_status": "pass | fail | warning",
  "pdf_status": "pass | fail | warning",
  "content_status": "pass | fail | warning",
  "issues": [],
  "fixes_applied": []
}
```

---

## 16. Critérios de aceite

O squad será considerado bem-sucedido quando:

- produzir relatório com aparência premium, não genérica;
- a primeira parte for predominantemente visual;
- o relatório tiver narrativa executiva clara;
- a paleta fizer sentido para empresa/setor;
- a tipografia for adequada e legível;
- gráficos forem escolhidos corretamente;
- mapas mentais, fluxos e infográficos ajudarem a compreender o conteúdo;
- HTML for navegável e responsivo;
- PDF for A4, organizado e sem cortes;
- texto técnico ficar em apêndice, não dominando a camada principal;
- dados forem preservados;
- não houver credenciais ou informações sensíveis;
- entrega final incluir HTML e PDF.

---

## 17. MVP proposto

### MVP 1 — Squad gerador de relatório premium estático

Entradas:

- Markdown ou texto pré-preenchido;
- briefing simples;
- setor/nicho;
- opção de formato PDF.

Saídas:

- HTML premium;
- PDF A4 retrato;
- apêndice técnico;
- QA básico.

Agentes mínimos:

1. Maestro;
2. Intake;
3. Estratégia narrativa;
4. Paleta/tipografia;
5. Infográficos;
6. Visualização de dados;
7. Front-end;
8. PDF/QA.

### MVP 2 — Sistema com templates e brand kit

Adiciona:

- biblioteca de templates;
- extração de cores de logotipo;
- múltiplos estilos por setor;
- HTML mais interativo;
- componentes reutilizáveis.

### MVP 3 — Plataforma avançada

Adiciona:

- editor visual;
- upload de planilhas;
- geração de dashboards interativos;
- versionamento de relatórios;
- exportação para slides;
- histórico de revisões.

---

## 18. Estrutura sugerida do futuro squad

```text
premium-report-design-squad/
├── squad.yaml
├── README.md
├── BRD.md
├── agents/
│   ├── maestro.md
│   ├── intake-diagnostico.md
│   ├── pesquisa-benchmark-visual.md
│   ├── estrategia-narrativa.md
│   ├── dados-e-evidencias.md
│   ├── paleta-identidade.md
│   ├── tipografia-hierarquia.md
│   ├── design-system.md
│   ├── infograficos.md
│   ├── visualizacao-dados.md
│   ├── ux-html.md
│   ├── frontend-html-css-js.md
│   ├── pdf-print-engineering.md
│   ├── qa-visual.md
│   ├── qa-factual-editorial.md
│   └── empacotamento-entrega.md
├── templates/
│   ├── executive-visual-layer.html
│   ├── analytical-visual-layer.html
│   ├── technical-appendix.html
│   └── pdf-print.css
├── components/
│   ├── kpi-card.html
│   ├── risk-matrix.html
│   ├── roadmap.html
│   ├── mindmap.html
│   ├── funnel.html
│   └── chart-block.html
├── references/
│   ├── visual-benchmark.md
│   ├── chart-selection-guide.md
│   ├── pdf-quality-checklist.md
│   └── design-token-guide.md
└── scripts/
    ├── build_html.py
    ├── build_pdf.py
    └── validate_pdf.py
```

---

## 19. Riscos do projeto

### Risco 1 — Relatório continuar muito textual

**Mitigação:** obrigar camada visual executiva antes do apêndice técnico.

### Risco 2 — PDF cortar elementos

**Mitigação:** stylesheet específica para print, renderização de prévias PNG e QA visual.

### Risco 3 — Gráficos bonitos mas errados

**Mitigação:** agente de dados e visualização deve validar tipo de gráfico e preservar números.

### Risco 4 — Paleta inadequada ao setor

**Mitigação:** agente de identidade visual deve usar brand kit, setor e contraste.

### Risco 5 — HTML interativo não converter bem para PDF

**Mitigação:** criar fallback estático para PDF.

### Risco 6 — Template genérico demais

**Mitigação:** biblioteca por tipo de relatório e setor, com curadoria de benchmark visual.

---

## 20. Decisões recomendadas antes de criar o squad

1. Confirmar nome definitivo do squad.
2. Confirmar se o primeiro MVP será em Python + HTML/CSS puro ou React/Astro.
3. Confirmar se o PDF padrão será A4 retrato.
4. Confirmar se o squad deve gerar apenas arquivos locais ou também repositório GitHub.
5. Confirmar se haverá biblioteca inicial de templates setoriais.
6. Confirmar se o usuário deseja que o squad tenha README premium público.

---

## 21. Recomendação final

Recomendo criar o squad inicialmente como **gerador local de relatórios premium em HTML/CSS/PDF**, com pipeline simples, robusto e auditável. A primeira versão deve priorizar:

- entrada em Markdown;
- visual-first;
- paleta/tipografia por setor;
- infográficos principais;
- HTML local para revisão;
- PDF A4 retrato sem cortes;
- QA visual e técnico.

Depois, o squad pode evoluir para templates por setor, dashboards interativos, leitura de planilhas e publicação no GitHub.

A regra central do squad deve ser:

> O relatório premium não é uma conversão de texto. É uma reconstrução visual da decisão, da evidência e da narrativa.
