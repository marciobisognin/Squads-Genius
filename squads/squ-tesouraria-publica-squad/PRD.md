# PRD — SQU Tesouraria & Conformidade Pública

<!-- page 1 -->

🏛 SQU Tesouraria & Conformidade
Pública
PRD — Product Requirements Document
Nome técnico:
squ-tesouraria-publica-squad
Versão alvo: (MVP em )
1.0.0 0.1.0
Domínio: Gestão orçamentária, financeira e de conformidade em
Instituições Federais de Ensino (IFs) — Institutos Federais,
Universidades Federais e órgãos da administração pública
federal
Licença: MIT
Autor: Marcio Bisognin
Idioma operacional: PT-BR
1. Sumário Executivo
O SQU Tesouraria & Conformidade Pública é um squad de
agentes especializados para apoiar equipes de planejamento,
orçamento, execução financeira e auditoria interna de Institutos
e Universidades Federais.
Ele transforma dados de execução orçamentária (LOA, PDI,
SIPAC), achados de auditoria (TCU/CGU), convênios/editais e
indicadores de gestão em dossiês auditáveis, pareceres
técnicos padronizados e simulações de impacto orçamentário
— sempre com rastreabilidade de fontes e revisão humana
obrigatória nos pontos de decisão.

<!-- page 2 -->

Nota essencial: este squad é uma camada de apoio analítico
e documental. Ele não substitui SIAFI, SIPAC ou sistemas de
registro oficiais, não realiza lançamentos contábeis, não
efetua pagamentos e não emite decisão administrativa final.
Toda saída é insumo para revisão de ordenador de despesas,
contador responsável, auditoria interna ou assessoria jurídica.
2. Problema e Oportunidade
Em IFs, a gestão orçamentária e a prestação de contas são
fragmentadas entre:
Planilhas paralelas de acompanhamento de execução por
campus/unidade gestora;
Processos SIPAC dispersos (requisições, empenhos,
convênios, editais);
Ofícios de auditoria (TCU/CGU) com prazos curtos e
exigência de linguagem técnica padronizada;
Indicadores de gestão (PDI, Decisão Normativa TCU de
indicadores de IFs) calculados manualmente e de forma
assíncrona entre setores.
Isso gera retrabalho, risco de glosas/achados recorrentes,
dificuldade de simular cenários (contingenciamento,
remanejamento entre campi, novos editais) e baixa
padronização de pareceres técnicos.
Oportunidade: um squad que organize esses fluxos em agentes
especializados, com guardrails de conformidade, reduz tempo
de elaboração de dossiês, aumenta a consistência de pareceres
e fornece simulações rápidas para apoiar decisões da gestão
(Reitoria, Pró-Reitoria de Administração e Planejamento —
PROAD/PROPLAN).

<!-- page 3 -->

3. Objetivos do Squad
ID Objetivo
Consolidar dados de execução orçamentária (LOA, PDI,
O1 SIPAC/SIAFI) em relatórios padronizados por unidade,
ação e natureza de despesa
Gerar dossiês de prestação de contas auditáveis (Relatório
O2
de Gestão, respostas a achados TCU/CGU, e-Contas)
Simular impactos de cenários orçamentários
O3 (contingenciamento, corte linear, remanejamento entre
campi, novos investimentos do PDI)
Apoiar a gestão de convênios, Termos de Execução
O4 Descentralizada (TED) e editais (Lei 14.133/2021), com
checklists de conformidade
Padronizar a redação de pareceres técnicos e notas
O5
técnicas com fundamentação legal explícita
Fornecer painel de indicadores de gestão (TCU/PDI) para
O6
apoiar decisões da alta gestão
4. Fora de Escopo (Não-Objetivos)
Não substitui SIAFI/SIPAC/Tesouro Gerencial como sistema
de registro oficial.
Não realiza empenho, liquidação, pagamento ou qualquer
lançamento contábil real.
Não emite decisão administrativa final nem assina
documentos em nome da instituição.

<!-- page 4 -->

Não fornece parecer jurídico vinculante — toda peça jurídica
deve passar pela Procuradoria Federal/assessoria jurídica.
Não acessa diretamente sistemas governamentais (SIPAC,
SIAFI, +Brasil, PNCP) — opera sobre dados/exportações
fornecidos pelo usuário.
5. Público-Alvo / Personas
Persona Necessidade principal
Visão consolidada de
Pró-Reitoria de
execução orçamentária e
Administração/Planejamento
simulações para tomada
(PROAD/PROPLAN)
de decisão
Relatórios de execução
Diretor de Administração e do próprio campus,
Planejamento (DAP) de campus pareceres técnicos
rápidos
Consolidação de dados
Analista/Técnico em Contabilidade SIPAC, conferência de
ou Orçamento (TAE) saldos, apoio à prestação
de contas
Organização de respostas
Auditoria Interna / Comissão de a achados TCU/CGU,
Ética histórico de planos de
ação
Checklist de
Gestor de Contratos/Convênios conformidade de editais,
convênios e TED

<!-- page 5 -->

6. Arquitetura do Squad ( )
squad.yaml
squad:
id: squ-tesouraria-publica-squad
name: "SQU Tesouraria & Conformidade Pública"
version: "1.0.0"
description: >
Squad de inteligência orçamentária e de
conformidade para Institutos e
Universidades Federais: dossiês de prestação de
contas, pareceres
técnicos, simulações de impacto orçamentário e
painel de indicadores.
domain: setor-publico-federal
language: pt-BR
license: MIT
author: Marcio Bisognin
entry_point: orcamentista-chefe
agents:
- id: orcamentista-chefe
file: agents/orcamentista-chefe.md
- id: analista-execucao-sipac
file: agents/analista-execucao-sipac.md
- id: auditor-tcu-cgu
file: agents/auditor-tcu-cgu.md
- id: gestor-convenios-editais
file: agents/gestor-convenios-editais.md
- id: redator-pareceres-tecnicos
file: agents/redator-pareceres-tecnicos.md
- id: painel-indicadores
file: agents/painel-indicadores.md
tasks:
- id: consolidar-execucao-orcamentaria
- id: classificar-saldo-restos-a-pagar
- id: montar-dossie-prestacao-contas

<!-- page 6 -->

- id: responder-achado-auditoria
- id: registrar-plano-de-acao
- id: checklist-conformidade-edital
- id: checklist-conformidade-convenio-ted
- id: redigir-parecer-tecnico
- id: simular-cenario-orcamentario
- id: gerar-painel-indicadores
workflows:
- id: execucao-orcamentaria-mensal
file: workflows/execucao-orcamentaria-
mensal.md
- id: prestacao-de-contas-auditoria
file: workflows/prestacao-de-contas-
auditoria.md
- id: simulacao-cenarios-pdi
file: workflows/simulacao-cenarios-pdi.md
guardrails: guardrails.md
7. Estrutura dos Agentes
Agente Camada Função principal
Lê LOA, PDI e matriz
Orçamentista- orçamentária; distribui
Chefe Planejamento referências de teto por
(LOA/PDI) unidade/ação; ponto de entrada
do squad
Consolida dados de
Analista de
empenho/liquidação/pagamento
Execução Execução
e restos a pagar a partir de
SIPAC
exportações SIPAC/SIAFI

<!-- page 7 -->

Agente Camada Função principal
Organiza achados, planos de
Auditor ação, prazos e fundamenta
Conformidade
TCU/CGU respostas com normativos (TCU,
CGU, MCASP, LRF)
Aplica checklists de
Gestor de
Conformidade conformidade para convênios,
Convênios e
contratual TED e editais (Lei 14.133/2021,
Editais
+Brasil, PNCP)
Redator de Padroniza notas técnicas e
Pareceres Documentação pareceres com fundamentação
Técnicos legal e estrutura SIPAC
Compila indicadores de gestão
Painel de
Decisão (PDI, Decisão Normativa TCU de
Indicadores
IFs) e gera leituras executivas
7.1 Orçamentista-Chefe (LOA/PDI)
Persona: especialista em planejamento orçamentário público,
com domínio de PPA, LDO, LOA e PDI institucional.
Responsabilidades:
Interpretar a matriz orçamentária da unidade (créditos,
ações, fontes de recurso, naturezas de despesa).
Relacionar metas do PDI com dotações orçamentárias por
campus/setor.
Servir como ponto de entrada: classifica o pedido do usuário
(execução, prestação de contas, convênio, simulação) e
roteia para o(s) agente(s) corretos.
Sinalizar incoerências entre teto orçamentário informado e
metas do PDI.

<!-- page 8 -->

Entradas: LOA/quadro de detalhamento de despesa (QDD), PDI
vigente, pedido do usuário.
Saídas: matriz de referência orçamentária por unidade/ação,
roteamento para os demais agentes.
7.2 Analista de Execução SIPAC
Persona: analista de orçamento e finanças com domínio dos
estágios da despesa pública (empenho, liquidação, pagamento)
e do ciclo de restos a pagar.
Responsabilidades:
Consolidar planilhas/exportações do SIPAC (execução por
unidade gestora, ação, natureza de despesa, fonte).
Calcular percentuais de execução (empenhado, liquidado,
pago) e saldo disponível por linha orçamentária.
Classificar restos a pagar processados e não processados,
sinalizando prazos de validade.
Apontar inconsistências (ex.: empenhos sem liquidação há
mais de N dias, saldo negativo aparente).
Entradas: extratos/exportações SIPAC, matriz de referência do
Orçamentista-Chefe.
Saídas: relatório de execução orçamentária consolidado (por
unidade, ação, natureza de despesa).
7.3 Auditor TCU/CGU
Persona: auditor interno com domínio de normativos do TCU,
recomendações da CGU, MCASP/PCASP e Lei de
Responsabilidade Fiscal.
Responsabilidades:

<!-- page 9 -->

Organizar achados de auditoria (origem, normativo violado,
prazo, status, unidade responsável).
Estruturar respostas a achados com base em evidências
fornecidas pelo usuário (sem inventar fatos ou dados).
Manter histórico de planos de ação e reincidências por
unidade.
Sinalizar quando um achado exigir manifestação da
Procuradoria Federal/assessoria jurídica.
Entradas: ofícios de auditoria, relatórios de gestão anteriores,
planos de ação em curso.
Saídas: matriz de achados x respostas x evidências x prazos;
minuta de manifestação para revisão humana.
7.4 Gestor de Convênios e Editais
Persona: gestor de contratos e parcerias com domínio da Lei
14.133/2021, plataforma +Brasil (ex-SICONV), TED e Portal
Nacional de Contratações Públicas (PNCP).
Responsabilidades:
Aplicar checklist de conformidade documental para
convênios, TED e processos licitatórios.
Mapear prazos críticos (vigência, prestação de contas de
convênio, publicação no PNCP).
Apontar exigências legais ausentes (termo de referência,
estudo técnico preliminar, matriz de risco).
Gerar lista de pendências por convênio/edital, classificadas
por criticidade.
Entradas: minutas de edital/convênio/TED, cronograma de
vigência, checklist normativo.
Saídas: checklist de conformidade preenchido, lista de
pendências priorizadas.

<!-- page 10 -->

7.5 Redator de Pareceres Técnicos
Persona: redator técnico especializado em documentos
administrativos públicos (notas técnicas, pareceres,
informações processuais no padrão SIPAC).
Responsabilidades:
Estruturar pareceres com seções padrão: contexto,
fundamentação legal, análise, conclusão/recomendação.
Citar normativos de forma rastreável (lei, decreto, instrução
normativa, número e ano) sem inventar dispositivos.
Adaptar tom e formalidade ao destinatário (Reitoria, campus,
órgão de controle).
Sinalizar trechos que exigem confirmação humana de dado
factual (datas, valores, números de processo).
Entradas: outputs dos demais agentes, contexto do processo,
normativos de referência.
Saídas: minuta de parecer técnico/nota técnica formatada para
inclusão em processo SIPAC.
7.6 Painel de Indicadores
Persona: analista de dados institucionais focado em indicadores
de gestão de IFs.
Responsabilidades:
Compilar indicadores de gestão alinhados ao PDI e aos
indicadores de gestão de IFs definidos por normativo do TCU
(ex.: relação candidato/vaga, relação concluintes/aluno,
gastos correntes por aluno, índice de eficiência acadêmica).
Comparar execução orçamentária com metas do PDI e
apontar desvios.
Gerar leitura executiva (1 página) para Reitoria/Conselho.

<!-- page 11 -->

Sinalizar quando dado estiver incompleto ou desatualizado,
em vez de estimar.
Entradas: relatório de execução (Analista SIPAC), metas do PDI,
série histórica de indicadores.
Saídas: painel de indicadores consolidado + leitura executiva.
8. Tasks
Agente
Task Descrição resumida
responsável
consolidar- Analista de Consolida
execucao- Execução empenho/liquidação/pagamento
orcamentaria SIPAC por unidade/ação/natureza
classificar- Analista de
Classifica e sinaliza prazos de
saldo-restos- Execução
restos a pagar
a-pagar SIPAC
montar-
Auditor
dossie- Monta dossiê estruturado para
TCU/CGU +
prestacao- Relatório de Gestão
Redator
contas
responder-
Auditor Estrutura resposta a achado
achado-
TCU/CGU com evidências e prazo
auditoria
registrar- Auditor Registra/atualiza plano de ação
plano-de-acao TCU/CGU e status de reincidência
checklist- Gestor de
Aplica checklist Lei 14.133/2021
conformidade- Convênios e
a minuta de edital
edital Editais

<!-- page 12 -->

Agente
Task Descrição resumida
responsável
checklist- Gestor de
Aplica checklist a convênio/TED
conformidade- Convênios e
(+Brasil)
convenio-ted Editais
redigir- Redator de
Gera minuta de parecer/nota
parecer- Pareceres
técnica padronizada
tecnico Técnicos
Orçamentista-
simular- Simula impacto de corte,
Chefe +
cenario- contingenciamento ou
Analista
orcamentario remanejamento
SIPAC
gerar-painel- Painel de Gera painel + leitura executiva de
indicadores Indicadores indicadores PDI/TCU
9. Workflows
9.1 Execução Orçamentária Mensal
Fluxo recorrente de acompanhamento, usado mensalmente por
DAPs e PROAD/PROPLAN.
flowchart TD
A[Exportação SIPAC do mês] --> B[Orçamentista-
Chefe: classifica unidade/ação/PDI]
B --> C[Analista de Execução SIPAC: consolida
empenho/liquidação/pagamento]
C --> D[Classificação de restos a pagar e alertas
de prazo]
D --> E[Painel de Indicadores: compara execução x
metas PDI]

<!-- page 13 -->

E --> F[Relatório de execução orçamentária +
leitura executiva]
F --> G[Revisão humana: DAP / PROAD]
9.2 Prestação de Contas e Resposta a Auditoria
Fluxo acionado para Relatório de Gestão anual ou resposta a
ofício do TCU/CGU.
flowchart TD
A[Ofício de auditoria ou ciclo de Relatório de
Gestão] --> B[Auditor TCU/CGU: mapeia achados e
normativos]
B --> C[Analista de Execução SIPAC: traz
evidências de execução]
C --> D[Gestor de Convênios e Editais: traz
evidências contratuais, se aplicável]
D --> E[Auditor TCU/CGU: monta matriz achado x
resposta x evidência]
E --> F[Redator de Pareceres Técnicos: redige
minuta de manifestação]
F --> G[Dossiê de prestação de contas]
G --> H[Revisão humana: Auditoria Interna /
Procuradoria / Reitoria]
9.3 Simulação de Cenários Orçamentários (PDI)
Fluxo de apoio à decisão para contingenciamento,
remanejamento entre campi ou novos investimentos do PDI.
flowchart TD
A[Pedido de simulação: corte, contingenciamento ou
novo investimento] --> B[Orçamentista-Chefe: define
premissas e unidades afetadas]
B --> C[Analista de Execução SIPAC: fornece saldo
disponível e execução atual]
C --> D[Orçamentista-Chefe: gera cenários A/B/C

<!-- page 14 -->

com impacto por unidade/ação]
D --> E[Painel de Indicadores: estima impacto nas
metas do PDI]
E --> F[Redator de Pareceres Técnicos: redige nota
técnica com cenários]
F --> G[Revisão humana: PROAD/PROPLAN/Reitoria
decide]
10. Guardrails e Conformidade
Fonte de verdade: o squad não acessa SIAFI/SIPAC
diretamente; trabalha sobre dados/exportações fornecidos
pelo usuário e sempre referencia a origem do dado.
Sem invenção de normativos ou valores: toda citação legal
(lei, decreto, IN, acórdão TCU) deve vir de fonte fornecida ou
ser sinalizada como "a confirmar" — nunca inventada.
Separação fato vs. recomendação: relatórios distinguem
claramente "dado informado", "cálculo derivado" e
"recomendação sujeita a revisão".
Revisão humana obrigatória em: respostas a auditoria,
pareceres técnicos finais, simulações que embasem decisão
orçamentária, qualquer documento que será protocolado.
LGPD: o squad não processa dados pessoais sensíveis de
servidores/alunos além do estritamente necessário para o
documento solicitado; recomenda anonimização quando
possível.
Sem promessa de resultado de auditoria: o squad não
garante que uma resposta "encerrará" um achado — isso
depende de avaliação do órgão de controle.
Versionamento e rastreabilidade: cada dossiê gerado
registra data, fontes utilizadas e versão do squad que o
produziu.

<!-- page 15 -->

11. Entregas (Outputs)
Entrega Finalidade
Visão consolidada de
Relatório de Execução empenho/liquidação/pagamento/restos
Orçamentária a pagar por unidade, ação e natureza de
despesa
Pacote estruturado (achados,
Dossiê de Prestação
evidências, respostas, plano de ação)
de Contas
para Relatório de Gestão/TCU/CGU
Cenários A/B/C de corte,
Simulação de Impacto
contingenciamento ou remanejamento,
Orçamentário
com impacto estimado no PDI
Minuta formatada para inclusão em
Parecer/Nota Técnica
processo SIPAC, com fundamentação
padronizada
legal
Checklist de Lista de pendências priorizadas
Conformidade conforme Lei 14.133/2021 e normas de
(Edital/Convênio/TED) convênios
Leitura executiva de 1 página
Painel de Indicadores
comparando execução x metas
PDI/TCU
institucionais
12. Estrutura de Arquivos do Repositório
squads/squ-tesouraria-publica-squad/
├── squad.yaml

<!-- page 16 -->

├── README.md
├── guardrails.md
├── agents/
│ ├── orcamentista-chefe.md
│ ├── analista-execucao-sipac.md
│ ├── auditor-tcu-cgu.md
│ ├── gestor-convenios-editais.md
│ ├── redator-pareceres-tecnicos.md
│ └── painel-indicadores.md
├── tasks/
│ ├── consolidar-execucao-orcamentaria.md
│ ├── classificar-saldo-restos-a-pagar.md
│ ├── montar-dossie-prestacao-contas.md
│ ├── responder-achado-auditoria.md
│ ├── registrar-plano-de-acao.md
│ ├── checklist-conformidade-edital.md
│ ├── checklist-conformidade-convenio-ted.md
│ ├── redigir-parecer-tecnico.md
│ ├── simular-cenario-orcamentario.md
│ └── gerar-painel-indicadores.md
├── workflows/
│ ├── execucao-orcamentaria-mensal.md
│ ├── prestacao-de-contas-auditoria.md
│ └── simulacao-cenarios-pdi.md
└── templates/
├── modelo-dossie-prestacao-contas.md
├── modelo-parecer-tecnico.md
├── modelo-checklist-edital-14133.md
└── modelo-painel-indicadores.md
13. Métricas de Sucesso (KPIs do Squad)

<!-- page 17 -->

Métrica Meta indicativa
Tempo médio de elaboração de um Redução de ≥ 50% frente
dossiê de prestação de contas ao processo manual
% de achados de auditoria com
resposta estruturada dentro do ≥ 90%
prazo
Aderência das simulações de Desvio documentado e
cenário ao realizado (desvio) revisado a cada ciclo
Pareceres técnicos reaproveitando ≥ 80% das peças geradas
o template padronizado pelo squad
Unidades/campi utilizando o painel Crescimento incremental
de indicadores mensalmente por ciclo de PDI
14. Roadmap de Versões
Versão Escopo
Agentes Orçamentista-Chefe, Analista de Execução
0.1.0
SIPAC e Redator de Pareceres; workflow de
(MVP)
Execução Orçamentária Mensal
Adição do Auditor TCU/CGU e workflow de
0.2.0
Prestação de Contas/Auditoria
Adição do Gestor de Convênios e Editais
0.3.0
(checklists Lei 14.133/2021 e +Brasil)
Painel de Indicadores completo, workflow de
1.0.0 Simulação de Cenários PDI, templates finais e
guardrails consolidados

<!-- page 18 -->

Versão Escopo
Integração com squads correlatos (ex.: RSC-TAE
1.1.0+ Trilhas de Carreira, Aletheia Auditor de Squads) e
suporte multi-instituição (perfis por IF)
15. Riscos e Mitigações
Risco Mitigação
Squad exige data de
Uso de dados
referência da exportação e
desatualizados/incompletos do
sinaliza quando dado está
SIPAC
incompleto
Guardrail de "sem invenção
Citação incorreta de normativo de normativo"; trechos não
legal confirmados ficam
marcados explicitamente
Toda peça é rotulada como
Geração de parecer tratado
"minuta sujeita a revisão" e
como decisão final
exige assinatura humana
Registro de premissas da
Divergência entre simulação e
simulação para auditoria
execução real
posterior do desvio
Recomendação de
Exposição de dados pessoais anonimização e checklist de
(LGPD) dados sensíveis antes de
incluir em dossiês

<!-- page 19 -->

16. Glossário
Termo Significado
LOA Lei Orçamentária Anual
LDO Lei de Diretrizes Orçamentárias
PPA Plano Plurianual
PDI Plano de Desenvolvimento Institucional
Sistema Integrado de Patrimônio,
SIPAC
Administração e Contratos
Sistema Integrado de Administração
SIAFI
Financeira do Governo Federal
TCU Tribunal de Contas da União
CGU Controladoria-Geral da União
Manual/Plano de Contas Aplicado ao Setor
MCASP/PCASP
Público
LRF Lei de Responsabilidade Fiscal
TED Termo de Execução Descentralizada
Plataforma federal de convênios e parcerias
+Brasil
(sucessora do SICONV)
PNCP Portal Nacional de Contratações Públicas
Lei Nova Lei de Licitações e Contratos
14.133/2021 Administrativos

<!-- page 20 -->

Termo Significado
Despesas empenhadas mas não pagas até o
Restos a Pagar
fim do exercício
17. Em uma frase
O SQU Tesouraria & Conformidade Pública transforma a
fragmentação de dados orçamentários, contratuais e de
auditoria em dossiês auditáveis, pareceres padronizados e
simulações de cenário — com rastreabilidade total e revisão
humana em cada decisão.
Licença: MIT
Criado por: Marcio Bisognin
Instagram: @marciobisognin
