# PRD — PROJUR Contracts Squad (v2.0)

> **Documento de Requisitos de Produto — versão revisada e expandida**
> Análise crítica do PRD original (v1) + proposta de PRD mais completo, com council de
> agentes SME (Subject-Matter Experts), engine determinística ampliada, schemas, base de
> regras versionada e gates humanos.
>
> Squad: **PROJUR Contracts Squad** — inteligência documental e ciclo de vida (CLM) de
> contratos, convênios, acordos e termos de descentralização do Instituto Federal
> Farroupilha (IFFar).
>
> | Campo | Valor |
> |---|---|
> | Nome técnico | `projur-contracts-squad` |
> | Destino | `IFFar-Squads/squads/projur-contracts-squad/` |
> | Versão do PRD | 2.0 (proposta) |
> | Idioma | pt-BR |
> | Licença | MIT |
> | Autor | Marcio Bisognin |
> | Data | 2026-06-17 |
> | Status | Proposta para aprovação (humano no loop) |

---

## 0. Como ler este documento

Seguindo as regras do construtor (Maeve Genius Forge), todo conteúdo está classificado:

- **[OBS]** Observado — extraído diretamente do PRD original ou do código do repositório.
- **[INF]** Inferido — deduzido com base no contexto.
- **[HIP]** Hipótese — precisa de confirmação (especialmente itens jurídicos).
- **[REC]** Recomendação.
- **[RISCO]** Risco identificado.

> **Aviso jurídico:** este squad produz apoio técnico automatizado. **Não substitui** parecer
> de advogado, procurador ou da Procuradoria Federal junto ao IFFar (art. 53 da Lei
> 14.133/2021). Toda saída exige revisão humana qualificada. Os dispositivos legais citados
> abaixo são **referenciais e precisam de verificação de vigência** antes do uso em produção.

---

## 1. Análise crítica do PRD original (v1)

### 1.1 Pontos fortes [OBS]

1. Pipeline determinístico e linear bem definido (ingestão → extração → classificação →
   metadados → cláusulas → validação → matriz/dicionário → relatório → quality report).
2. Critérios de aceitação **quantitativos** (similaridade ≥ 95%, classificação ≥ 90%, etc.).
3. Saídas claras e úteis para gestão (matriz CSV/XLSX, dicionário de cláusulas, relatório
   executivo, quality report, pacote ZIP).
4. Preocupação com **reprodutibilidade** (checksums idênticos) e com evidência de execução.
5. Estrutura de diretórios coerente com a convenção do repositório.

### 1.2 Lacunas e fragilidades [RISCO]

| # | Lacuna | Impacto | Severidade |
|---|--------|---------|-----------|
| L1 | **Sobreposição** com squads já existentes (`themis-contratos-publicos-squad`, `farol-contratos-licitacoes-iffar`, `squad-pcfp`) sem diferenciação explícita | Retrabalho, confusão de catálogo | Alta |
| L2 | **Sem OCR**: a meta de extração ≥ 95% é irreal para PDFs escaneados (imagem). Contratos físicos digitalizados quebram o pipeline | Pipeline falha em parte real do acervo | Alta |
| L3 | **Sem tratamento de LGPD/PII**: contratos contêm CPF, CNPJ, dados de contato e bancários. Não há agente nem script de detecção/mascaramento | Exposição de dado pessoal nos artefatos | Alta |
| L4 | **Sem vínculo entre instrumentos** (aditivo → contrato-pai; convênio → TED; ata de RP → contratos) nem deduplicação de lote | Matriz inconsistente, contagem dupla | Média |
| L5 | **Ciclo de vida (CLM) ausente**: o problema cita "taxa de renovação" e "vigência", mas nenhum agente cuida de alertas de vencimento, prazos e limites de aditivos | Não entrega o indicador prometido | Média |
| L6 | **Regras de negócio (R01–R05) rasas e inconsistentes**: misturam licitação, PD&I, certificado digital e terceirização; R03 e R04 parecem premissas não verificadas | Conformidade frágil / incorreta | Alta |
| L7 | **Metodologia de métrica indefinida**: como medir "95% de similaridade" sem *gold set* / verdade-base? | Critérios não auditáveis | Média |
| L8 | **Schemas só nomeados**, sem campos. Sem schema de partes, vínculo, alerta, PII, indicadores | Handoffs entre agentes ambíguos | Média |
| L9 | **Sem normalização/validação de CNPJ/CPF e razão social** das partes | Matriz "suja", joins impossíveis | Média |
| L10 | **Sem gates humanos (HITL)** além do quality_report; sem trilha de auditoria nem governança de retenção | Não atende padrão dos squads IFFar | Média |
| L11 | **SMEs jurídicos insuficientes**: 11 agentes, mas só genéricos. Falta especialista em convênios/TED, em fundações de apoio, em PD&I/PI e em LGPD | Profundidade jurídica baixa | Alta |
| L12 | **Sem ingestão incremental/versionamento da matriz** ao longo do tempo | Reprocessa tudo a cada lote | Baixa |

### 1.3 Recomendação de posicionamento [REC]

> **PROJUR não deve duplicar o Themis.** O Themis já faz a **análise jurídica profunda e o
> parecer** de um instrumento. O PROJUR deve ser a **camada de inteligência documental em
> lote e gestão de ciclo de vida (CLM)** que processa centenas de instrumentos, monta a
> **matriz consolidada**, gera **indicadores** e **alimenta** o Themis (parecer) e o Farol
> (contratações) quando um caso merece análise aprofundada.

Cadeia de valor proposta:

```
[Acervo / lote bruto]
        │
        ▼
PROJUR Contracts  ── extrai, classifica, normaliza, vincula, monitora vigência,
(este squad)         gera matriz + indicadores + alertas + dicionário de cláusulas
        │
        ├──► casos com red flag jurídico  ──► Themis (parecer técnico-jurídico)
        ├──► itens em fase de contratação ──► Farol (DFD/preços/licitação)
        └──► planilhas de custo de mão de obra ──► PCFP
```

---

## 2. Visão geral (v2)

O **PROJUR Contracts Squad** é uma equipe multiagente que transforma um **lote** de
instrumentos administrativo-jurídicos do IFFar (PDF nativo, PDF escaneado, DOCX, Markdown)
em uma **matriz consolidada, governada e auditável**, com:

- extração de texto fiel (com **OCR de fallback** para documentos escaneados);
- classificação do tipo de instrumento (contrato, ata de registro de preços, termo aditivo,
  convênio, acordo de cooperação, termo de execução descentralizada — TED, termo de fomento/
  colaboração, contrato com fundação de apoio);
- extração e **normalização** de metadados (número, partes com CNPJ/CPF validados, objeto,
  valor, vigência, base legal);
- segmentação e padronização de cláusulas (dicionário reutilizável);
- **detecção e mascaramento de dados pessoais (LGPD)**;
- **vínculo entre instrumentos** e deduplicação de lote;
- **monitor de ciclo de vida**: alertas de vencimento, prazos de renovação e limites de aditivos;
- validação de conformidade por **rules engine versionada**;
- relatório executivo com **indicadores de gestão**;
- **quality report**, trilha de auditoria e pacote ZIP reprodutível.

### Saídas

| Saída | Formato | Uso |
|---|---|---|
| `matriz_contratos` | CSV / XLSX / JSON | Base de controle, painéis (Power BI / planilha) |
| `dicionario_clausulas` | JSON / Markdown | Padronização e reúso de cláusulas |
| `alertas_vigencia` | CSV / JSON | Gestão de vencimentos e renovações (CLM) |
| `vinculos_instrumentos` | JSON | Aditivo↔contrato, convênio↔TED, ata↔contrato |
| `relatorio_pii` | JSON | Itens sensíveis encontrados/mascarados (LGPD) |
| `indicadores` | JSON | Valor total, distribuição por tipo, taxa de renovação, % cláusulas fora do padrão |
| `relatorio_executivo` | PDF / Markdown | Entrega para a gestão e equipe jurídica |
| `quality_report` | JSON | Evidência de execução e gates |
| `manifest` + `checksums` | JSON | Reprodutibilidade e trilha de auditoria |
| `projur_contracts_squad_pacote` | ZIP | Pacote completo de artefatos |

---

## 3. Problema, objetivos e escopo

### 3.1 Problema [OBS, do v1]

- Centenas de instrumentos recebidos por ano.
- Análise manual lenta e sujeita a omissões.
- Ausência de indicadores de gestão (valor total, distribuição por tipo, taxa de renovação,
  % de cláusulas não padronizadas).
- Falta de fluxo automatizado que extraia texto fiel, identifique metadados, valide
  conformidade e produza matriz pronta para o sistema de controle.

### 3.2 Objetivos (v2)

1. Pipeline determinístico em lote, **resiliente a documentos escaneados** (OCR fallback).
2. Matriz consolidada com partes **normalizadas e validadas** e vínculos entre instrumentos.
3. **Camada CLM**: alertas de vigência, renovação e limites de aditivos.
4. **Conformidade LGPD** by design (detecção e mascaramento de PII).
5. Conformidade legal por **rules engine versionada e fundamentada**.
6. Indicadores e relatório executivo prontos para gestão.
7. Reprodutibilidade total (checksums) e trilha de auditoria.

### 3.3 Não-objetivos (out-of-scope v1) [REC]

- **Parecer jurídico de mérito** (delegado ao Themis).
- **Fase de planejamento/licitação** — DFD/ETP/TR/preços (delegado ao Farol).
- **Planilha de custos de mão de obra** (delegado ao PCFP).
- Assinatura digital, tramitação processual e integração transacional com SIPAC/SEI.
- Decisão administrativa automática (sempre humano no loop).

---

## 4. Personas e usuários [INF]

| Persona | Necessidade |
|---|---|
| Equipe da PROJUR / assessoria jurídica | Triagem rápida, dicionário de cláusulas, red flags para parecer |
| Gestão de contratos / fiscais | Matriz, alertas de vigência, limites de aditivos, indicadores |
| Auditoria / controle interno | Trilha de auditoria, evidências com checksum, conformidade |
| Gabinete / direção | Relatório executivo e indicadores agregados |
| Encarregado de dados (LGPD) | Relatório de PII e garantia de minimização |

---

## 5. Requisitos funcionais (v2)

| Código | Requisito | Métrica mínima | Como medir |
|---|---|---|---|
| RF01 | Extração de texto (PDF nativo, DOCX, MD) | ≥ 95% similaridade vs. gold set | `gold_eval.py` (ratio difflib em amostra rotulada) |
| RF02 | OCR de fallback para PDF escaneado | ≥ 85% similaridade em amostra escaneada | `gold_eval.py` sobre subconjunto OCR |
| RF03 | Classificação do tipo de instrumento | ≥ 90% acerto | matriz de confusão vs. gold set |
| RF04 | Metadados extraídos e preenchidos | ≥ 80% campos preenchidos | contagem sobre schema `instrumento` |
| RF05 | Validação de CNPJ/CPF das partes | 100% dos documentos verificados | dígito verificador (`normalize_parties.py`) |
| RF06 | Cláusulas essenciais identificadas (art. 92, Lei 14.133) | ≥ 70% acerto | checklist vs. gold set |
| RF07 | Detecção de PII (CPF, CNPJ, e-mail, telefone, conta) | ≥ 95% recall em amostra | `detect_pii.py` vs. gold set |
| RF08 | Vínculo entre instrumentos (aditivo↔pai, convênio↔TED) | ≥ 90% precisão | conferência manual de amostra |
| RF09 | Alertas de vigência e limites de aditivo | 100% dos instrumentos com vigência | `vigencia_alertas.py` |
| RF10 | Regras de conformidade aplicadas | ≥ 8 regras distintas | `rules_engine.py` sobre `regras.yaml` |
| RF11 | Matriz consolidada | ≤ 5% campos vazios | `quality_audit.py` |
| RF12 | Indicadores de gestão | gerados sem erro | `compute_indicators.py` |
| RF13 | Quality report | `passed: true` | `quality_audit.py` |
| RF14 | Reprodutibilidade | checksums idênticos entre execuções | `manifest_checksums.py` |

---

## 6. Requisitos não-funcionais (v2) [REC]

- **Determinismo**: nenhum valor numérico ou de conformidade gerado por LLM — apenas pelos
  scripts. O LLM raciocina e decide *quais* regras aplicar; o script calcula. (padrão PCFP).
- **Sem dependências externas obrigatórias**: Python 3.11+, biblioteca padrão. OCR e XLSX são
  **opcionais** com degradação graciosa (se `tesseract`/`openpyxl` ausentes, registra aviso e
  segue com PDF nativo / CSV).
- **LGPD**: minimização, mascaramento configurável, retenção parametrizável, trilha de auditoria;
  nenhum dado sensível em logs ou no ZIP sem mascaramento.
- **Segurança**: nunca publicar `.env`, tokens, chaves; varredura de segredos no quality gate.
- **Auditabilidade**: cada artefato com origem, timestamp e checksum.
- **Idempotência / incremental**: reprocessar o mesmo lote produz o mesmo resultado; novos
  lotes atualizam a matriz sem recomputar o histórico.

---

## 7. Arquitetura e pipeline (v2)

```
Ingestão (lote + dedup + manifest)
   └─► Extração de texto ──(PDF imagem?)──► OCR fallback ──► Normalização de texto
        └─► Classificação de instrumento
             └─► Extração de metadados ──► Normalização/validação de partes (CNPJ/CPF)
                  ├─► Detecção/mascaramento de PII (LGPD)
                  ├─► Segmentação de cláusulas ──► Cláusulas essenciais (art. 92)
                  ├─► Vínculo de instrumentos (aditivo↔pai, convênio↔TED, ata↔contrato)
                  └─► Conformidade (rules engine) + Riscos financeiros + Vigência/aditivos
                       └─► Matriz + Dicionário + Indicadores
                            └─► Relatório executivo
                                 └─► Guardião de evidência (checksums) ──► Quality Audit ──► ZIP
```

---

## 8. Agentes (council SME ampliado)

> v1 tinha 11 agentes genéricos. v2 propõe **18 agentes**, sendo **6 SMEs jurídicos
> especializados** (em negrito), além dos agentes de engine e governança.

### 8.1 Núcleo de pipeline

| # | Agente | Função | Entradas → Saídas |
|---|--------|--------|-------------------|
| A01 | `projur-orchestrator` | Coordena o fluxo, aplica gates, consolida quality_report | lote → plano + relatórios |
| A02 | `intake-triagem` | Recebe lote, deduplica (hash), gera manifest e fila | arquivos → manifest |
| A03 | `extrator-texto-juridico` | PDF nativo/DOCX/MD → texto limpo | documento → texto |
| A04 | `ocr-especialista` | Detecta PDF imagem e aplica OCR de fallback | PDF imagem → texto |
| A05 | `classificador-instrumento` | Detecta o tipo (contrato, ata RP, aditivo, convênio, acordo de cooperação, TED, termo de fomento/colaboração, contrato fundação de apoio) | texto → tipo + confiança |
| A06 | `extrator-metadados` | Nº, partes, objeto, valor, vigência, base legal | texto → metadados |
| A07 | `normalizador-partes` | Valida CNPJ/CPF (dígito verificador), normaliza razão social | metadados → partes canônicas |
| A08 | `analisador-clausulas` | Segmenta cláusulas e verifica essenciais (art. 92, Lei 14.133) | texto → cláusulas |
| A09 | `vinculador-instrumentos` | Liga aditivo↔contrato-pai, convênio↔TED, ata↔contratos | metadados → grafo de vínculos |

### 8.2 Council de SMEs jurídicos [REC]

| # | Agente SME | Especialidade | Base normativa referencial [HIP — verificar vigência] |
|---|------------|---------------|--------------------------------------------------------|
| A10 | **`sme-lei14133-conformidade`** | Contratos administrativos e cláusulas necessárias | Lei 14.133/2021 (arts. 89–104, 124–136); Lei 8.666/1993 (regime legado) |
| A11 | **`sme-convenios-ted-transferencias`** | Convênios, termos de fomento/colaboração, TED | Lei 8.958/1994 (fundações de apoio); Decreto 11.531/2023 (Transferegov); Decreto 10.426/2020 (TED); Lei 13.019/2014 (MROSC) |
| A12 | **`sme-pdi-propriedade-intelectual`** | Cláusulas de PD&I, sigilo, titularidade de PI | Lei 10.973/2004 e Decreto 9.283/2018 (Marco Legal CT&I) |
| A13 | **`sme-lgpd-privacidade`** | Dados pessoais, base legal e minimização | Lei 13.709/2018 (LGPD); orientações ANPD |
| A14 | **`sme-licitacao-enquadramento`** | Modalidade, dispensa/inexigibilidade e fundamentação | Lei 14.133/2021 (arts. 74, 75); limites atualizados por decreto |
| A15 | **`sme-jurisprudencia-controle`** | Confronto com TCU/TCE e CGU (reúso de padrão Themis) | Súmulas/acórdãos TCU; referenciais CGU; Lei 12.846/2013 |

### 8.3 Engine, governança e relato

| # | Agente | Função |
|---|--------|--------|
| A16 | `validador-conformidade` | Aplica a `rules_engine` (regras versionadas) e consolida apontamentos |
| A17 | `auditor-vigencia-riscos` | Alertas de vencimento/renovação, limites de aditivo (25%/50%) e anomalias de valor |
| A18 | `gerador-matriz-dicionario` | Matriz (CSV/XLSX/JSON), dicionário de cláusulas e indicadores |
| A19 | `gerador-relatorio-executivo` | Relatório PDF/MD com indicadores e alertas |
| A20 | `guardiao-evidencia` | Textos limpos, logs, checksums, trilha de auditoria |
| A21 | `quality-auditor` | Verifica saídas e gera `quality_report` |
| A22 | `revisor-humano-hitl` | Ponto de revisão humana obrigatório nos gates |

> Observação: a contagem efetiva pode ser ajustada na implementação; o conjunto acima
> privilegia **profundidade SME** sobre minimalismo, conforme o pedido.

---

## 9. Tasks (v2)

| ID | Owner | Objetivo |
|---|---|---|
| `01_intake_e_deduplicacao` | intake-triagem | Receber lote, deduplicar, gerar manifest |
| `02_extracao_texto_e_ocr` | extrator-texto-juridico / ocr-especialista | Extrair texto fiel; OCR quando imagem |
| `03_classificacao_instrumento` | classificador-instrumento | Detectar tipo e confiança |
| `04_metadados_e_partes` | extrator-metadados / normalizador-partes | Extrair e normalizar metadados; validar CNPJ/CPF |
| `05_pii_lgpd` | sme-lgpd-privacidade | Detectar e mascarar dados pessoais |
| `06_clausulas_essenciais` | analisador-clausulas / sme-lei14133-conformidade | Segmentar e checar cláusulas (art. 92) |
| `07_convenios_ted_pdi` | sme-convenios-ted-transferencias / sme-pdi-propriedade-intelectual | Regras específicas de convênios/TED e PD&I |
| `08_vinculo_instrumentos` | vinculador-instrumentos | Relacionar aditivos, convênios, TEDs, atas |
| `09_conformidade_e_riscos` | validador-conformidade / auditor-vigencia-riscos | Aplicar rules engine, vigência, aditivos, anomalias |
| `10_jurisprudencia_controle` | sme-jurisprudencia-controle | Mapear red flags vs. TCU/CGU (handoff p/ Themis) |
| `11_matriz_dicionario_indicadores` | gerador-matriz-dicionario | Consolidar matriz, dicionário e KPIs |
| `12_relatorio_executivo` | gerador-relatorio-executivo | Gerar relatório PDF/MD |
| `13_evidencia_e_quality` | guardiao-evidencia / quality-auditor | Checksums, trilha e quality_report |

---

## 10. Workflows (v2)

| Workflow | Descrição |
|---|---|
| `lote_completo` | Pipeline integral (intake → quality report → ZIP) |
| `triagem_rapida_red_flags` | Triagem expressa para priorizar casos ao Themis |
| `atualizacao_incremental` | Ingestão incremental sem reprocessar o histórico |
| `monitor_vigencia` | Execução periódica só do CLM (alertas de vencimento/aditivo) |

---

## 11. Scripts determinísticos (engine ampliada)

> v1 tinha ~11 scripts genéricos. v2 propõe **~23 scripts**, todos Python 3.11+, sem
> dependências obrigatórias (OCR/XLSX opcionais com degradação graciosa). Reúso explícito de
> padrões já existentes em Themis e Farol.

| Script | Propósito | Reúso |
|---|---|---|
| `ingest.py` | Lê lote, deduplica por hash, gera manifest | — |
| `ocr_fallback.py` | Detecta PDF imagem e aplica OCR (tesseract opcional) | novo |
| `extract_text.py` | Extrai texto de PDF nativo/DOCX/MD | — |
| `normalize_text.py` | Normaliza acentos, espaços, quebras (base p/ similaridade) | padrão `farol_common.py` |
| `classify_instrument.py` | Classifica tipo por regras + palavras-chave | padrão `analisar_dfd.py` |
| `extract_metadata.py` | Extrai nº, partes, objeto, valor, vigência, base legal | — |
| `normalize_parties.py` | Valida CNPJ/CPF (dígito verificador) e normaliza razão social | novo |
| `parse_money_dates.py` | Converte "1.234,56" e datas BR | reúso `farol_common.py` |
| `extract_clauses.py` | Segmenta cláusulas | — |
| `check_essential_clauses.py` | Checa cláusulas necessárias (art. 92, Lei 14.133) | reúso `checklist_clausulas.py` (Themis) |
| `detect_pii.py` | Detecta CPF, CNPJ, e-mail, telefone, conta (LGPD) | novo |
| `redact_pii.py` | Mascara/anonimiza PII nos artefatos | novo |
| `rules_engine.py` | Carrega `regras.yaml` e aplica regras de conformidade | novo |
| `validate_conformity.py` | Orquestra a aplicação de regras sobre metadados/cláusulas | — |
| `validar_limites_aditivos.py` | Calcula % de aditivos vs. limites (25%/50%) | reúso direto (Themis) |
| `vigencia_alertas.py` | Calcula vencimentos, prazos de renovação, status (CLM) | novo |
| `value_anomaly.py` | Detecta anomalias de valor (mediana/IQR/MAD) | padrão `farol_common.py` |
| `link_instruments.py` | Liga aditivo↔contrato, convênio↔TED, ata↔contratos | novo |
| `build_matrix.py` | Consolida a matriz (CSV/XLSX/JSON) | — |
| `build_dictionary.py` | Gera dicionário de cláusulas | — |
| `compute_indicators.py` | Calcula KPIs (valor total, distribuição, taxa de renovação, % fora do padrão) | novo |
| `generate_report.py` | Gera relatório executivo (PDF/MD) | — |
| `manifest_checksums.py` | Gera e confere checksums (reprodutibilidade) | reúso padrão `evidence` (Farol) |
| `package_zip.py` | Empacota artefatos | — |
| `quality_audit.py` | Verifica saídas e gera `quality_report` | — |
| `gold_eval.py` | Mede métricas (similaridade, acerto de classe) vs. *gold set* | novo |

---

## 12. Schemas (handoffs schema-first)

> v1 tinha 4 schemas só nomeados. v2 propõe **11 schemas JSON** com campos. Reúso da estrutura
> de `finding/case/evidence` do Farol para consistência entre squads IFFar.

| Schema | Campos-chave |
|---|---|
| `instrumento.schema.json` | `id, tipo, numero, partes[], objeto, valor, vigencia_inicio, vigencia_fim, base_legal[], origem, checksum` |
| `parte.schema.json` | `nome_razao_social, documento, tipo_documento (CNPJ/CPF), papel, valido (bool)` |
| `clausula.schema.json` | `id, instrumento_id, rotulo, texto, categoria, essencial (bool), presente (bool)` |
| `validacao.schema.json` | `instrumento_id, regra_id, resultado, classificacao, fundamento, confianca, revisao_humana (bool)` |
| `regra.schema.json` | `id, descricao, condicao, severidade, base_legal, vigente_em, confianca` |
| `matriz.schema.json` | `colunas[], linhas[]` (espelho normalizado de `instrumento`) |
| `vinculo_instrumento.schema.json` | `origem_id, destino_id, tipo_vinculo (aditivo/ted/ata), confianca` |
| `alerta_vigencia.schema.json` | `instrumento_id, status, dias_para_vencimento, percentual_aditivos, acao_recomendada` |
| `pii_finding.schema.json` | `instrumento_id, tipo_pii, trecho_mascarado, posicao, base_legal_lgpd` |
| `indicadores.schema.json` | `valor_total, por_tipo{}, taxa_renovacao, pct_clausulas_fora_padrao, total_instrumentos` |
| `quality_report.schema.json` | `passed (bool), metricas{}, gates{}, issues[], checksums{}` |

---

## 13. Base de regras de negócio (versionada e fundamentada)

> **[RISCO]** As regras R01–R05 do v1 eram inconsistentes e não fundamentadas. v2 propõe uma
> base em `regras.yaml`, **cada regra com `base_legal`, `vigente_em` e `confianca`**, sujeita à
> validação da PROJUR. Itens marcados **[HIP]** precisam de confirmação jurídica antes do uso.

| Código | Regra (referencial) | Base legal [HIP — verificar] | Severidade |
|---|---|---|---|
| R01 | Contrato sem cláusulas necessárias (objeto, vigência, preço, garantia, sanções, foro, anticorrupção, LGPD…) | Art. 92, Lei 14.133/2021 | Crítica |
| R02 | Aditivo que ultrapassa limite de acréscimo/supressão (25% / 50% reforma) | Art. 125, Lei 14.133/2021 | Crítica |
| R03 | Contratação direta sem fundamento de dispensa/inexigibilidade | Arts. 74–75, Lei 14.133/2021 | Alta |
| R04 | Convênio/TED sem plano de trabalho ou prestação de contas | Decreto 11.531/2023; Decreto 10.426/2020 | Alta |
| R05 | Instrumento com fundação de apoio sem amparo legal e seleção | Lei 8.958/1994; Decreto 7.423/2010 | Alta |
| R06 | Projeto de PD&I sem cláusula de titularidade de PI e sigilo | Lei 10.973/2004; Decreto 9.283/2018 | Média |
| R07 | Dado pessoal exposto sem base legal/minimização | Lei 13.709/2018 (LGPD) | Crítica |
| R08 | Vigência expirada ou a vencer em < 90 dias sem renovação | Gestão contratual (CLM) | Alta |
| R09 | Valor acima do limite que exige modalidade/licitação | Lei 14.133/2021 (limites por decreto) | Alta |
| R10 | Partes com CNPJ/CPF inválido ou ausente | Integridade cadastral | Média |

> Cada regra produz um `validacao` com classificação (`erro_confirmado` / `suspeita` /
> `recomendacao` / `depende_justificativa` / `insuficiente`), espelhando o padrão do Farol.

---

## 14. Quality gates e HITL [REC]

| Gate | Condição de aprovação |
|---|---|
| `extracao_completa` | Todos os documentos com texto (nativo ou OCR) |
| `metadados_e_partes_validados` | CNPJ/CPF verificados; ≥ 80% campos preenchidos |
| `pii_tratado` | PII detectado e mascarado; relatório LGPD gerado |
| `conformidade_aplicada` | ≥ 8 regras executadas com fundamento |
| `sem_valor_de_llm` | Números/conformidade vieram só dos scripts |
| `revisao_humana_red_flags` | Casos críticos revisados por humano (handoff Themis) |
| `quality_report_passed` | `passed: true` e checksums reprodutíveis |

> **HITL obrigatório**: nenhuma decisão administrativa é automática; o `revisor-humano-hitl`
> valida red flags e a entrega final, conforme padrão Themis/PCFP/Farol.

---

## 15. Critérios de aceitação (v2)

- Extração fiel (similaridade ≥ 95% nativo; ≥ 85% OCR) — medida por `gold_eval.py`.
- Classificação correta (≥ 90%).
- Metadados preenchidos (≥ 80%) e CNPJ/CPF 100% verificados.
- Cláusulas essenciais (≥ 70%).
- PII detectado (recall ≥ 95%) e mascarado.
- Vínculos corretos (precisão ≥ 90%).
- ≥ 8 regras aplicadas com fundamento e classificação.
- Alertas de vigência e limites de aditivo gerados para 100% dos instrumentos com vigência.
- Matriz completa (≤ 5% campos vazios) e indicadores gerados sem erro.
- Relatório executivo gerado sem erro.
- Quality report `passed: true`.
- ZIP com todos os artefatos.
- Reprodutibilidade (checksums idênticos).

---

## 16. Estrutura de diretórios

```
IFFar-Squads/squads/projur-contracts-squad/
├── squad.yaml
├── README.md
├── PRD.md            (este documento)
├── LICENSE
├── NOTICE.md
├── AUTHORS.md
├── agents/           (A01–A22, .md)
├── tasks/            (01..13, .yaml)
├── workflows/        (lote_completo, triagem_rapida_red_flags, atualizacao_incremental, monitor_vigencia)
├── scripts/          (engine determinística, .py)
├── schemas/          (11 schemas .json)
├── templates/        (relatório, dicionário, regras.yaml)
├── docs/             (base normativa, forge/quality_report.json)
├── tests/            (pytest)
└── examples/         (lote de exemplo + uso)
```

---

## 17. Comandos de execução (v2)

```bash
python scripts/ingest.py --input ./entrada --output ./saida
python scripts/ocr_fallback.py --manifest ./saida/manifest.json
python scripts/extract_text.py --manifest ./saida/manifest.json
python scripts/normalize_text.py --in ./saida/evidencias/textos
python scripts/classify_instrument.py --in ./saida/evidencias/textos
python scripts/extract_metadata.py --in ./saida/instrumentos.json
python scripts/normalize_parties.py --in ./saida/metadados.json
python scripts/detect_pii.py --in ./saida/evidencias/textos --out ./saida/pii.json
python scripts/redact_pii.py --in ./saida/evidencias/textos --pii ./saida/pii.json
python scripts/extract_clauses.py --in ./saida/evidencias/textos
python scripts/check_essential_clauses.py --clausulas ./saida/clausulas.json
python scripts/link_instruments.py --metadados ./saida/metadados.json
python scripts/rules_engine.py --regras ./templates/regras.yaml --metadados ./saida/metadados.json
python scripts/validate_conformity.py --metadados ./saida/metadados.json
python scripts/validar_limites_aditivos.py --vinculos ./saida/vinculos.json
python scripts/vigencia_alertas.py --metadados ./saida/metadados.json --out ./saida/alertas.json
python scripts/value_anomaly.py --metadados ./saida/metadados.json
python scripts/build_matrix.py --metadados ./saida/metadados.json --out ./saida/matriz_contratos.csv
python scripts/build_dictionary.py --clausulas ./saida/clausulas.json --out ./saida/dicionario_clausulas.json
python scripts/compute_indicators.py --matriz ./saida/matriz_contratos.csv --out ./saida/indicadores.json
python scripts/generate_report.py --matriz ./saida/matriz_contratos.csv --indicadores ./saida/indicadores.json --out ./saida/relatorio_executivo.pdf
python scripts/manifest_checksums.py --input ./saida
python scripts/package_zip.py --input ./saida --out ./saida/projur_contracts_squad_pacote.zip
python scripts/quality_audit.py --input ./saida --out ./saida/quality_report.json
python scripts/gold_eval.py --gold ./examples/gold --pred ./saida   # validação de métricas
```

---

## 18. Testes obrigatórios

```
test_ingest.py, test_ocr_fallback.py, test_extract_text.py, test_classify.py,
test_metadata.py, test_normalize_parties.py, test_pii.py, test_clauses.py,
test_link_instruments.py, test_rules_engine.py, test_validate.py,
test_vigencia_alertas.py, test_value_anomaly.py, test_matrix.py,
test_indicators.py, test_quality.py, test_gold_eval.py, smoke_test.py
```

---

## 19. Métricas e metodologia de avaliação [REC]

Para tornar os critérios **auditáveis**, o squad inclui um *gold set* em
`examples/gold/` (amostra rotulada de instrumentos com texto, tipo e metadados corretos).
O `gold_eval.py` calcula:

- **Similaridade de extração**: `difflib.SequenceMatcher.ratio()` entre texto extraído e
  texto-base normalizado.
- **Acerto de classificação**: matriz de confusão por tipo.
- **Recall de PII**: itens sensíveis encontrados / itens rotulados.
- **Precisão de vínculos**: vínculos corretos / vínculos propostos.

> Sem *gold set* não há como afirmar "95% de similaridade" — esta é a lacuna **L7** do v1.

---

## 20. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Documentos escaneados quebram extração | OCR fallback + meta separada (85%) |
| Exposição de PII nos artefatos | `detect_pii` + `redact_pii` + gate `pii_tratado` |
| Regras legais desatualizadas | `regras.yaml` versionado com `vigente_em`; revisão jurídica |
| Sobreposição com Themis/Farol | Posicionamento como camada CLM + handoff explícito |
| "Métricas de fachada" | *gold set* + `gold_eval.py` |
| Decisão automática indevida | HITL obrigatório; "zero decisão administrativa automática" |

---

## 21. Roadmap (faseado, padrão PCFP)

- **F0 — Fundação**: estrutura, `squad.yaml`, schemas, `ingest`, `extract_text`, `gold_eval`,
  `regras.yaml` inicial, golden tests.
- **F1 — MVP**: classificação + metadados + partes + matriz + indicadores + relatório.
- **F2 — Conformidade & LGPD**: `rules_engine`, `detect/redact_pii`, gates HITL, council SME.
- **F3 — CLM**: `vigencia_alertas`, `link_instruments`, `validar_limites_aditivos`, monitor.
- **F4 — OCR & escala**: `ocr_fallback`, ingestão incremental, anomalias de valor.
- **F5 — Integração**: handoff para Themis/Farol/PCFP e exportação para painel de controle.

---

## 22. Próximos passos

1. Aprovação deste PRD pela PROJUR/gestão (humano no loop).
2. Validação jurídica das regras **[HIP]** (R01–R10) e da base normativa.
3. Definição do *gold set* com a equipe (amostra rotulada de instrumentos reais).
4. Scaffold via `forge_squad.py` e implementação faseada (F0→F5).
5. Execução com o lote de minutas PROJUR e `validate_squad.py` (go/no-go).
6. Registro em `SQUAD_INDEX.md` e `IFFar-Squads/README.md`.

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
