# Tarefa: Análise de Pipeline, Win/Loss e Forecast de Receita

## Objetivo
Diagnosticar a saúde do pipeline de vendas, extrair inteligência de deals ganhos e perdidos, e construir um modelo de forecast de receita com cenários probabilísticos que suporte decisões de planejamento e alocação de recursos.

## Contexto
Esta tarefa integra os outputs dos agentes `pipeline-health-monitor`, `win-loss-analyst` e `revenue-forecast-modeler`. Juntos, eles respondem às perguntas mais críticas da liderança de vendas: "O pipeline está saudável o suficiente para atingir a quota?", "Por que estamos perdendo deals?", e "Quanto de receita podemos esperar fechar neste período?"

---

## Fase 1 — Diagnóstico de Saúde do Pipeline

### Entradas Necessárias
- [ ] Export do CRM com: deals em aberto, estágio, valor estimado, close date estimada, rep responsável, data de criação do deal
- [ ] Metas de quota do período (mensal, trimestral ou anual)
- [ ] Dados de pipeline de períodos anteriores (para comparativo, se disponível)
- [ ] Definição dos estágios do processo de vendas com probabilidade padrão por estágio

### Atividades

#### 1.1 Snapshot de Pipeline
- Calcular o volume total de pipeline por estágio (quantidade de deals e valor)
- Calcular pipeline coverage ratio: pipeline total ÷ quota restante
- Verificar se coverage está acima do mínimo recomendado (3x para sales cycle < 30 dias, 4x para ciclos mais longos)

#### 1.2 Análise de Velocidade
- Calcular tempo médio gasto em cada estágio
- Identificar estágios com tempo médio acima do benchmark
- Calcular Sales Velocity: (N° Deals × Win Rate × Ticket Médio) ÷ Ciclo de Vendas Médio

#### 1.3 Análise de Conversão por Estágio
- Calcular Stage Conversion Rate para cada par de estágios consecutivos
- Identificar o "gargalo de conversão": estágio com pior taxa de avanço
- Comparar conversão atual com histórico (se disponível)

#### 1.4 Mapeamento de Deal Slippage
- Listar todos os deals com close date anterior à data atual
- Classificar por tempo de slippage: moderado (< 30 dias), crítico (30-90 dias), zombie (> 90 dias)
- Identificar o padrão de deals com slippage: estágio mais comum, rep mais afetado, segmento

#### 1.5 Análise de Concentração e Risco
- Identificar deals que representam > 15% do pipeline total (risco de concentração)
- Calcular o Herfindahl Index de concentração do pipeline
- Gerar alerta se um único deal representa > 25% da quota restante

#### 1.6 Deals Estagnados
- Filtrar deals sem atividade registrada nos últimos N dias (por estágio):
  - Qualificação: > 14 dias sem atividade
  - Discovery: > 21 dias sem atividade
  - Proposta: > 30 dias sem atividade
  - Negociação: > 14 dias sem atividade
- Gerar lista de deals estagnados com recomendação de ação por deal

---

## Fase 2 — Análise Win/Loss

### Entradas Necessárias
- [ ] Histórico de deals fechados (won + lost) dos últimos 6-12 meses com: valor, ciclo de vendas, vertical, porte do cliente, rep, estágio em que saiu (para lost), razão de perda declarada, competidor envolvido
- [ ] Histórico de win rate por rep, vertical e produto (se disponível)

### Atividades

#### 2.1 Tabulação de Razões de Perda
- Categorizar todas as razões de perda declaradas nas categorias: competição, preço, produto, processo, timing, relacionamento
- Calcular frequência e valor em risco por categoria
- Identificar top 3 razões que respondem por > 50% do valor perdido

#### 2.2 Análise de Root Cause
Para cada uma das top 3 razões de perda, investigar:
- A razão declarada é o sintoma ou a causa real?
- Que evidências suportam ou contradizem a razão declarada?
- Qual seria a intervenção mais eficaz para reduzir essa causa?

#### 2.3 Identificação de Win Patterns
- Listar os atributos mais comuns nos deals ganhos: segmento, porte, touchpoints, recursos utilizados, cargo do champion
- Identificar o que diferencia deals ganhos dos perdidos em segmentos similares
- Mapear a sequência de ações que precedem o fechamento bem-sucedido

#### 2.4 Análise Competitiva
- Tabular os competidores presentes nos deals perdidos por frequência
- Calcular win rate por competidor (% de vezes que ganhamos quando X estava no deal)
- Identificar os contextos em que cada competidor vence com mais frequência

#### 2.5 Análise de Rep Performance
- Calcular win rate por rep (se dados disponíveis e aprovado no contexto LGPD)
- Identificar diferenças nos padrões de ação entre top performers e performers medianos
- Gerar insights de coaching (anonimizados se necessário)

---

## Fase 3 — Forecast de Receita

### Entradas Necessárias
- [ ] Pipeline atual completo com probabilidades por estágio
- [ ] Win rate histórico (geral, por rep, por vertical — o que estiver disponível)
- [ ] Ciclo de vendas médio histórico
- [ ] Metas de quota do período
- [ ] Histórico de forecast accuracy (previsão vs. real de períodos anteriores, se disponível)

### Atividades

#### 3.1 Forecast Weighted by Stage
- Multiplicar valor de cada deal pela probabilidade padrão do estágio
- Somar para obter o "Weighted Forecast" base

#### 3.2 Forecast Risk-Adjusted
- Ajustar probabilidades com base em: tempo no estágio, atividade recente, ICP score, histórico do rep
- Recalcular forecast com probabilidades ajustadas

#### 3.3 Construção dos Três Cenários
| Cenário | Premissas | Win Rate | Ciclo |
|---------|-----------|----------|-------|
| Conservador | Mercado adverso, deals grandes com risco elevado | -15% vs. histórico | +20% mais longo |
| Realista | Continuidade das condições atuais | Alinhado ao histórico | Nominal |
| Otimista | Melhorias implementadas com playbook e scoring | +10% vs. histórico | -10% mais curto |

#### 3.4 Análise de Sensibilidade
Calcular impacto no forecast base para cada variação:
- Win rate +5 pp → impacto em R$ no forecast
- Win rate -5 pp → impacto em R$ no forecast
- Ciclo de vendas +15 dias → impacto em número de deals fecháveis
- Ticket médio +10% → impacto no forecast
- Pipeline coverage -0.5x → impacto no volume disponível

#### 3.5 Pipeline Gap Analysis
- Calcular: quota meta - forecast realista = gap
- Calcular pipeline adicional necessário para fechar o gap (considerando win rate)
- Identificar as melhores fontes de pipeline adicional (segmento, vertical, upsell)

---

## Validações e Quality Gates

### Checklist de Pipeline Health
- [ ] Pipeline coverage ratio calculado e comparado ao mínimo recomendado
- [ ] Deal slippage identificado e classificado por severidade
- [ ] Gargalo de conversão por estágio identificado
- [ ] Lista de deals estagnados gerada com recomendações

### Checklist de Win/Loss
- [ ] Mínimo de 20 deals analisados (idealmente 10 won + 10 lost)
- [ ] Root cause identificado para top 3 razões de perda
- [ ] Win patterns com pelo menos 3 atributos em comum
- [ ] Análise competitiva com pelo menos o principal competidor

### Checklist de Forecast
- [ ] Três cenários com premissas distintas e explícitas
- [ ] Análise de sensibilidade para pelo menos 3 variáveis
- [ ] Pipeline gap calculado com recomendações de ação
- [ ] Limitações do modelo declaradas

---

## Outputs Esperados

| Artefato | Responsável | Formato |
|----------|-------------|---------|
| Pipeline Health Report | pipeline-health-monitor | Markdown |
| Deal Slippage Report | pipeline-health-monitor | Tabela/JSON |
| Stage Conversion Funnel | pipeline-health-monitor | Markdown |
| Win/Loss Intelligence Report | win-loss-analyst | Markdown |
| Competitive Battle Cards | win-loss-analyst | Markdown |
| Root Cause Analysis Matrix | win-loss-analyst | Tabela |
| Revenue Forecast Report (3 cenários) | revenue-forecast-modeler | Markdown |
| Pipeline Gap Analysis | revenue-forecast-modeler | Markdown |
| Sensitivity Analysis | revenue-forecast-modeler | Tabela/Markdown |
| Executive Forecast Summary | revenue-forecast-modeler | Markdown (1 página) |

---

## Observações de Privacidade LGPD
- Dados de performance por rep são tratamento de dados pessoais — requer base legal (relação empregatícia)
- Análises de rep devem ser usadas exclusivamente para coaching interno
- Razões de perda que envolvam informações do comprador (orçamento, projetos internos) são dados pessoais/empresariais — usar apenas no nível necessário para a análise
- Dados de deals perdidos devem ser anonimizados ao nível de conta antes de qualquer compartilhamento externo

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
