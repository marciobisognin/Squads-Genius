# PRD Master — SQU Oráculo de Aion

## 1. Visão

O SQU Oráculo de Aion é um super squad de inteligência financeira global que organiza uma equipe de agentes especializados para analisar mercados, macroeconomia, geopolítica, história, notícias, fundos, derivativos, sistemas institucionais e risco.

A ideia original do documento fala em encontrar oportunidades assimétricas e maximizar lucros. Nesta versão operacional profissional, a promessa é tecnicamente mais segura e responsável: **identificar hipóteses de assimetria, construir cenários, mapear riscos, gerar relatórios auditáveis e apoiar decisões humanas qualificadas**.

## 2. Problema

Investidores e analistas enfrentam excesso de informação, múltiplas fontes globais, regimes econômicos mutáveis, narrativas contraditórias, assimetrias difíceis de medir e alto risco de viés. Um agente único tende a alucinar, simplificar ou ignorar dimensões críticas. O SQU resolve isso por especialização, debate adversarial e quality gates.

## 3. Usuários

- Investidores educacionais avançados.
- Analistas de mercado.
- Pesquisadores financeiros.
- Consultores e educadores de finanças.
- Gestores que precisam de inteligência macro e setorial.

## 4. Escopo funcional

### 4.1 Coleta e inteligência de mercado

- Notícias financeiras globais.
- Comunicados de bancos centrais.
- Dados de bolsas, ETFs, setores e câmbio.
- Cartas de fundos e filings públicos.
- Séries históricas e eventos catalíticos.
- Literatura e frameworks financeiros.

### 4.2 Análise especializada

- Geopolítica e risco-país.
- Ciclos históricos e regimes econômicos.
- Estratégias clássicas e quantitativas.
- Sistemas institucionais e microestrutura.
- Câmbio e carry trade.
- Bolsas e rotação setorial.
- Bancos centrais e liquidez.
- Opções, derivativos e volatilidade.

### 4.3 Debate adversarial

- Tese Bull.
- Tese Bear.
- Crítica de premissas.
- Sinais conflitantes.
- Pontos que exigem dados adicionais.

### 4.4 Risco e conformidade

- Drawdown e stress test.
- VaR/CVaR quando houver dados.
- Correlação e concentração.
- Suitability básico.
- Bloqueios de linguagem prescritiva.
- Revisão humana obrigatória.

### 4.5 Entrega ao usuário

O output final deve conter:

- resumo executivo;
- ativos/temas em observação;
- tese educacional;
- evidências;
- riscos;
- cenário Bull/Base/Bear;
- perguntas ao usuário;
- plano de acompanhamento;
- disclaimer.

## 5. Arquitetura

Três camadas:

1. **Camada de Especialistas**: coleta e análise paralela.
2. **Camada de Conselho**: debate Bull/Bear, síntese e risco.
3. **Camada de Entrega**: relatório, dashboard, monitoramento e revisão.

## 6. Critérios de aceite

- Todos os agentes estão definidos com função, input e output.
- Toda recomendação é rebaixada para hipótese educacional se não houver dado verificável.
- O relatório separa fato, inferência, hipótese e cenário.
- O agente de compliance pode vetar uma saída.
- O sistema gera demo local sem APIs pagas.
- O pacote contém templates, workflows, PRD, README e scripts.

## 7. Roadmap

### Fase 1 — MVP seguro

- News, Equities, Central Banks, Strategy, Risk e Compliance.
- Dados públicos e relatórios manuais.
- Output em Markdown.

### Fase 2 — Núcleo analítico

- Geopolítica, FX, Fund Letters e Derivatives.
- Debate Bull/Bear.
- Score de evidência.

### Fase 3 — Profundidade institucional

- História, livros/papers, sistemas institucionais e backtesting.
- Base vetorial.
- Relatórios comparativos.

### Fase 4 — Monitoramento

- Alertas.
- Dashboards.
- Rotina periódica.
- Integração com APIs e ferramentas agent-ready.

## 8. Modelo de saída padrão

Cada análise deve seguir o esquema:

1. Pergunta/objetivo do usuário.
2. Restrições de risco e horizonte.
3. Fontes usadas.
4. Síntese macro.
5. Tese Bull.
6. Tese Bear.
7. Riscos e invalidações.
8. Cenários.
9. Hipóteses de assimetria.
10. Próximos dados necessários.
11. Conclusão educacional.
12. Aviso de não recomendação.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
