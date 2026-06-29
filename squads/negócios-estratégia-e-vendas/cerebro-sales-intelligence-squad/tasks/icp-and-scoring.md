# Tarefa: ICP Profiling e Lead Scoring

## Objetivo
Definir o Perfil de Cliente Ideal (ICP) e construir o modelo de Lead Scoring que orientará a priorização e qualificação de leads para a equipe de vendas.

## Contexto
Esta tarefa integra os outputs dos agentes `icp-profiler` e `lead-scorer`. O ICP fundamenta o modelo de scoring, e o modelo de scoring operacionaliza o ICP em critérios mensuráveis e aplicáveis à base de leads. O resultado é um sistema de qualificação que substitui o subjetivismo por critérios transparentes e auditáveis.

---

## Fase 1 — Definição do ICP

### Entradas Necessárias
- [ ] Lista de clientes atuais com pelo menos: setor, porte (headcount ou faturamento), localização, tempo de relacionamento e indicador de saúde (NPS, churn ou expansão)
- [ ] Dados de MRR/ARR ou ticket médio por cliente (para identificar clientes de alto valor)
- [ ] Stack tecnológica dos clientes (se disponível)
- [ ] Descrição do produto/serviço e seus principais casos de uso

### Atividades

#### 1.1 Segmentação de Clientes por Valor
Identificar os 20% de clientes que representam 80% do valor (Pareto de valor):
- Ordenar clientes por LTV (Lifetime Value) ou MRR/ARR
- Identificar atributos comuns nos top clientes
- Verificar taxa de churn, expansão e referências por segmento

#### 1.2 Análise Firmográfica
Para os clientes de alto valor, mapear:
- **Setor**: CNAE principal ou categoria de negócio
- **Porte**: faturamento anual estimado ou número de funcionários
- **Maturidade**: tempo de existência da empresa
- **Localização**: geografias prioritárias
- **Estrutura**: sociedade anônima, LTDA, multinacional, startup

#### 1.3 Análise Comportamental e de Engajamento
- Mapear touchpoints antes da compra: quantas interações, por qual canal, em qual sequência
- Identificar comportamentos digitais correlacionados com conversão
- Mapear gatilhos de entrada: que evento na vida da empresa precedeu a compra?

#### 1.4 Definição de Personas de Comprador
Para cada segmento de ICP, documentar:
- **Cargo e nível hierárquico** do champion (quem defende internamente)
- **Cargo e nível** do economic buyer (quem assina o cheque)
- **Critérios de avaliação** de cada persona
- **Dores específicas** por persona
- **Métricas de sucesso** de cada persona

#### 1.5 Perfil Negativo (Anti-ICP)
Documentar os critérios que indicam que um lead NÃO deve ser priorizado:
- Setores com histórico de churn elevado
- Portes fora do range ideal
- Clientes que demandam muito serviço para o ticket que pagam
- Geografias com limitações de atendimento ou compliance

### Critério de Conclusão da Fase 1
- ICP Playbook rascunhado com firmografia, comportamento, gatilhos e perfil negativo
- Pelo menos 2 personas documentadas com dores e critérios de avaliação
- Scorecard de atributos com pesos preliminares somando 100%

---

## Fase 2 — Construção do Modelo de Lead Scoring

### Entradas Necessárias
- [ ] ICP Playbook (output da Fase 1)
- [ ] Base de leads com dados disponíveis (firmografia, comportamento digital, engajamento)
- [ ] Histórico de leads qualificados e convertidos (para calibração, se disponível)
- [ ] Dados de ferramentas de automação de marketing (taxa de abertura, clicks, páginas visitadas) — condicionado ao gate LGPD

### Atividades

#### 2.1 Definição das Dimensões de Scoring
Mapear as 4 dimensões do modelo e seus pesos iniciais:
1. **Fit Firmográfico** (peso sugerido: 30%) — alinhamento do lead ao perfil de empresa do ICP
2. **Comportamento Digital** (peso sugerido: 25%) — engajamento com canais digitais
3. **Engajamento Comercial** (peso sugerido: 25%) — interações diretas com o time de vendas
4. **Sinais de Intenção e Urgência** (peso sugerido: 20%) — indicadores de momento de compra

#### 2.2 Definição dos Critérios por Dimensão
Para cada dimensão, definir:
- Critérios observáveis e mensuráveis
- Pontuação associada a cada critério (valor e justificativa)
- Critérios de descarte (pontuação negativa ou eliminação)

#### 2.3 Definição dos Thresholds de Qualificação
| Tier | Score | Status | Ação Recomendada |
|------|-------|--------|-----------------|
| Descartado | 0-30 | Sem ação ativa | Nurturing passivo ou remoção |
| MQL | 31-50 | Marketing Qualified | Nurturing ativo, conteúdo segmentado |
| SQL | 51-70 | Sales Qualified | Contato inicial do SDR |
| SRL | 71-85 | Sales Ready | Escalação para Account Executive |
| Hot Lead | 86-100 | Prioridade máxima | Ação imediata do AE |

#### 2.4 Aplicação e Calibração
- Aplicar o modelo à base de leads disponível
- Verificar se a distribuição de scores faz sentido (evitar que todos os leads fiquem em um único tier)
- Se houver dados históricos: verificar se leads convertidos tinham scores mais altos que os não convertidos
- Ajustar pesos e critérios conforme necessário

#### 2.5 Documentação e Transferência
- Documentar o modelo de forma que qualquer analista possa aplicá-lo manualmente
- Criar guia de interpretação do score para o time de vendas
- Preparar handoff para o sales-playbook-engineer integrar o scoring ao processo de vendas

---

## Validações e Quality Gates

### Checklist de ICP
- [ ] ICP cobre firmografia, comportamento, tecnografia e perfil negativo
- [ ] Pelo menos 2 personas documentadas
- [ ] Mapa de gatilhos com pelo menos 3 eventos
- [ ] Scorecard com pesos somando 100%

### Checklist de Scoring
- [ ] 4 dimensões documentadas com critérios e pesos justificados
- [ ] Thresholds MQL/SQL/SRL/Hot definidos com critério claro
- [ ] Critérios de descarte documentados
- [ ] Distribuição de scores verificada na base de leads

---

## Outputs Esperados

| Artefato | Responsável | Formato |
|----------|-------------|---------|
| ICP Playbook | icp-profiler | Markdown |
| Scorecard de Atributos ICP | icp-profiler | Tabela/JSON |
| Personas de Comprador | icp-profiler | Markdown |
| Mapa de Gatilhos de Entrada | icp-profiler | Markdown |
| Modelo de Lead Scoring documentado | lead-scorer | Markdown |
| Ranking de Leads por Score | lead-scorer | JSON/Tabela |
| Relatório de Calibração | lead-scorer | Markdown |
| Guia de Interpretação do Score | lead-scorer | Markdown |

---

## Observações de Privacidade LGPD
- Dados de comportamento digital de leads individuais só podem ser processados com base legal (ex: legítimo interesse documentado ou consentimento)
- Scores individuais de leads identificáveis são considerados dados de tratamento — aplicar minimização
- Histórico de atividade de leads deve ser anonimizado se compartilhado fora do contexto original de coleta

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
