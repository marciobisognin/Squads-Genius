# Task: Análise Completa de Inteligência de Talentos

Esta task conduz o ciclo completo de análise de People Intelligence — desde a validação dos dados brutos de RH até a entrega do relatório People Intelligence Report, passando por mapeamento de competências, perfis comportamentais, benchmarking salarial, análise de cultura e diagnóstico de retenção. O output é um pacote executivo que transforma dados dispersos de RH em inteligência de negócio acionável para decisões estratégicas de pessoas.

## Objetivo
Transformar dados brutos de RH (perfis de colaboradores, avaliações de performance, dados de clima, benchmarks salariais e histórico de turnover) em um People Intelligence Report completo, com mapeamento de competências, Risk Scores de retenção, diagnóstico de fit cultural e recomendações priorizadas por impacto para o ciclo de gestão de talentos.

## Inputs Necessários
- Base de dados de colaboradores: nome/ID, cargo, área, nível hierárquico, data de admissão, faixa salarial atual
- Resultados de avaliações de desempenho dos últimos 12 meses (por colaborador ou consolidados por área)
- Dados de pesquisa de clima organizacional (últimos 6 a 12 meses) ou NPS interno por área
- Histórico de turnover dos últimos 24 meses com motivo de desligamento quando disponível
- Benchmarks salariais de mercado por cargo e região (fontes externas ou dados contratados)
- Dados demográficos (com consentimento documentado conforme LGPD): gênero, raça/etnia, geração, PcD
- Resultados de avaliações comportamentais (DISC, Big Five, CliftonStrengths ou equivalentes), quando existentes
- Contexto estratégico da organização: objetivos de negócio para 12-36 meses, áreas de expansão, posições críticas

## Etapas

1. **Intake, estruturação e validação dos dados (gate_intake)**
   Receber todos os inputs, verificar completude mínima (≥ 80% de cobertura dos colaboradores no escopo), anonimizar dados sensíveis conforme LGPD e documentar consentimentos. Registrar fontes, datas e premissas. Se dados estiverem incompletos, emitir checklist de pendências e aguardar complementação antes de prosseguir. Entregar o pacote validado ao pipeline.

2. **Mapeamento de competências e identificação de HiPos**
   Acionar o talent-mapper para construir a taxonomia de competências da organização, cruzar perfis existentes com os requisitos de cargo e os objetivos estratégicos, identificar gaps críticos por área e nível hierárquico, e produzir a lista de colaboradores de alto potencial (HiPo) com critérios objetivos documentados. Gerar a matriz de skills com calor visual e recomendações de PDI priorizadas.

3. **Perfilamento comportamental e revisão humana (gate_comportamental)**
   Acionar o psychometric-profiler para sintetizar os dados de avaliações comportamentais disponíveis em perfis acionáveis por colaborador. Mapear a dinâmica de cada time (complementaridade, tensões potenciais). Submeter todos os perfis a revisão obrigatória por psicólogo organizacional ou HRBP sênior antes de qualquer circulação. Integrar os perfis validados aos outputs de competências.

4. **Benchmarking salarial e análise de risco de remuneração**
   Acionar o market-salary-intel para calcular o posicionamento competitivo da organização por cargo e nível (percentis 25/50/75 do mercado). Identificar colaboradores com gap salarial de risco (abaixo do P50 do mercado para a função). Avaliar a proposta de valor ao empregado (EVP) e o posicionamento de employer branding. Integrar os dados salariais ao Risk Score de retenção na etapa seguinte.

5. **Análise de fit cultural e diagnóstico de clima**
   Acionar o culture-fit-analyst para cruzar os valores individuais com a cultura organizacional declarada e vivida, calcular o score de alinhamento por colaborador, diagnosticar o clima por área (NPS interno, satisfação por dimensão), mapear subculturas e identificar focos de conflito. Entregar o Diagnóstico de Clima e o Plano de Ação Cultural como inputs para o design de onboarding e a análise de retenção.

6. **Monitoramento de risco de retenção e emissão de alertas**
   Acionar o retention-risk-sentinel para calcular o Risk Score de turnover por colaborador (combinando gap salarial, satisfação com gestão, estagnação de carreira, fit cultural e tempo sem promoção). Identificar colaboradores com score ≥ 70 (risco alto/crítico) e emitir alertas para gestores com recomendações de intervenção imediata. Atualizar o dashboard de tendências de rotatividade.

7. **Consolidação, revisão cruzada e entrega do People Intelligence Report (gate_entrega_final)**
   O talent-orchestrator integra todos os outputs parciais, verifica consistência cruzada entre análises, classifica cada entregável por nível de confidencialidade, produz o sumário executivo com recomendações priorizadas (imediato / 90 dias / 1 ano) e monta o pacote final. Submeter à aprovação do RH sênior e do patrocinador do projeto antes da entrega. Registrar o log completo de quality gates executados como apêndice de auditoria.

## Critérios de Conclusão
- [ ] Gate de intake aprovado: dados com cobertura ≥ 80% e LGPD verificada
- [ ] Matriz de competências entregue com gaps críticos classificados por prioridade
- [ ] Perfis comportamentais revisados e aprovados por especialista humano
- [ ] Benchmarking salarial com posicionamento competitivo e lista de risco documentada
- [ ] Diagnóstico de clima com NPS interno por área e plano de ação cultural
- [ ] Risk Scores de retenção calculados e alertas emitidos para colaboradores em risco crítico
- [ ] People Intelligence Report consolidado com sumário executivo e recomendações priorizadas
- [ ] Gate de entrega final aprovado: consistência verificada, confidencialidade classificada, relatório sem dados pessoais identificáveis na versão de distribuição ampla
- [ ] Log de quality gates incluído como apêndice de auditoria

## Output Esperado
People Intelligence Report completo contendo: (1) Sumário executivo com 5-10 recomendações priorizadas por impacto e urgência; (2) Matriz de competências com gaps críticos e lista HiPo; (3) Perfis comportamentais consolidados por time; (4) Posicionamento salarial competitivo e lista de risco de remuneração; (5) Diagnóstico de clima e mapa de subculturas; (6) Dashboard de Risk Scores de retenção com alertas ativos; (7) Apêndice técnico com metodologias, fontes e log de quality gates. O relatório é entregue em versão executiva (síntese visual) e técnica (detalhamento analítico), classificado por nível de confidencialidade.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
