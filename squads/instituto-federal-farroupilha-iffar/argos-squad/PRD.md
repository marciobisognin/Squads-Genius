# PRD — Squad ARGOS
## Vigilância de Diários Oficiais (DOU + DOEs + DOMs) com Relatórios por Interesse

> **Codinome:** ARGOS — em referência a Argos Panoptes, o vigia de cem olhos que nunca dormem todos ao mesmo tempo. Cada "olho" é um adapter determinístico de coleta sobre uma fonte oficial.
>
> **Idioma:** PT-BR · **Repositório-alvo:** `squads/argos/`

---

## 1. TÉLOS — Visão e Propósito

Sistema operável via **CLI** que monitora o **Diário Oficial da União**, os **Diários Oficiais Estaduais** e (opcionalmente) **Diários Municipais**, filtra publicações por **perfis de interesse** declarativos em YAML e entrega **relatórios estruturados** (Markdown/HTML/JSON) com resumos gerados por LLM — sob a invariante de que **a coleta é 100% determinística e o LLM nunca decide o que existe, apenas classifica e sintetiza o que foi coletado**.

**Problema:** Não existe API pública unificada para os 27 DOEs. O DOU tem dataset oficial (INLABS), os municípios têm o Querido Diário, e os estados são um deserto de dados fragmentado em 27 portais heterogêneos.

**Tese do ARGOS:** resolver a lacuna por **adapters incrementais sob contrato único**, aproveitando o que já existe em open source (INLABS, API do Querido Diário, padrões do Ro-DOU) em vez de reinventar.

**Usuário primário:** servidor público / analista monitorando atos relevantes para contratos e licitações; extensível a qualquer perfil de interesse (pesquisa, jornalismo, compliance).

### 1.1 Fora de escopo
- Interface web (CLI-first; relatórios HTML são artefatos estáticos).
- Diários do Judiciário e do Legislativo (foco: Executivo).
- Burlar bloqueios anti-robô de portais (fontes sem via legítima entram em backlog, nunca em produção via evasão).
- OCR de PDFs escaneados (camada opcional futura).

---

## 2. FONTES DE DADOS — Estratégia em Três Anéis

| Anel | Fonte | Via de acesso | Custo | Maturidade |
|---|---|---|---|---|
| **A — União** | DOU | **INLABS** (XML + PDF oficial, Imprensa Nacional, gratuito desde 01/01/2020, requer credencial de portal) | R$ 0 | Alta — dataset estruturado |
| **B — Municípios** | DOMs | **API pública do Querido Diário** (`api.queridodiario.ok.org.br`) | R$ 0 | Alta — ~60 req/min sugeridas pela OKBR |
| **C — Estados** | 27 DOEs | **Adapters próprios** sob contrato `AdapterDiario` (padrão httpx/Scrapy, um por estado, incremental) | R$ 0 + esforço | Construção progressiva |

**Decisões vinculantes:**
1. DOU **exclusivamente via INLABS** (XML). O portal de busca da Imprensa Nacional bloqueia robôs desde 2023; não usar Selenium contra ele. O INLABS é a via oficial e legítima, com autenticação por usuário/senha do portal.
2. Anel C começa pelo **DOE-RS**, depois SC/PR/SP, depois demanda.
3. Todo adapter novo passa por **gate HITL de homologação** (§11) antes de entrar no roster de produção.
4. Adapters priorizam, nesta ordem: API oficial documentada → API "escondida" (JSON descoberto por inspeção legítima) → HTML parseável → PDF nato-digital (extração de texto). PDF escaneado = fora de escopo.

---

## 3. INVARIANTES ARQUITETURAIS

1. **LLMs emitem apenas JSON estruturado** validado por Pydantic v2 com `extra="forbid"`. Falha de validação → retry limitado → dead-letter.
2. **Coleta, deduplicação, filtragem lexical e agregação são determinísticas** (Python puro). O LLM entra somente após o corpus estar fixado e hasheado.
3. **Nenhuma aritmética em LLM.** Contagens, estatísticas do relatório e scores lexicais em Python; valores monetários extraídos de atos preservados como `Decimal`.
4. **Orquestração:** LangGraph `StateGraph` com estado tipado.
5. **Handoffs:** contrato SACP entre nós (payload + `corpus_hash` + proveniência).
6. **Reprodutibilidade:** dado o mesmo `corpus_hash` + `perfil_hash` + `model_profile` pinado, o pipeline determinístico produz bytes idênticos; a camada LLM registra seed/temperatura e é auditável via replay no Langfuse.
7. **Proveniência obrigatória:** toda linha do relatório carrega `fonte`, `edicao`, `data_publicacao`, `url_original`. Publicação sem URL verificável não entra no relatório.
8. **Egress control:** allowlist explícita de domínios por adapter (INLABS, QD, portal de cada DOE). Qualquer outro destino → bloqueio + evento.
9. **Cortesia de rede:** rate limit por fonte (QD ≤ 30 req/min — metade da referência da OKBR), backoff exponencial, `User-Agent` identificado com contato.
10. **Sem branding de framework guarda-chuva.** O squad é autocontido.

---

## 4. ROSTER DE MENTES E MOTORES

### 4.1 Motores determinísticos (Python puro, sem LLM)

| Motor | Função |
|---|---|
| **OPHTHALMOI** ("os olhos") | Família de adapters de coleta. Cada olho implementa o contrato `AdapterDiario` para uma fonte (INLABS, QD, DOE-RS, …). |
| **MNÉMON** | Memória de estado: SQLite local com edições já processadas, hashes de conteúdo, cursores por fonte. Garante idempotência e deduplicação. |
| **KANON-LEX** | Filtro lexical determinístico: aplica `termos`, `termos_ignorados`, regex de órgãos e `pubtype` do perfil sobre o corpus, produzindo o subconjunto candidato **antes** de qualquer LLM. |
| **TEKMÉRION** | Verificador de evidência: valida que cada excerto citado existe byte a byte no texto-fonte e que toda URL responde (HEAD/GET com cache). |
| **STATISTA** | Agregações do relatório (contagens por fonte/órgão/categoria) em Python. |

### 4.2 Mentes LLM (JSON-only, perfis de modelo pinados)

| Mente | Papel | Saída |
|---|---|---|
| **HÉGEMON** | Orquestrador do grafo; roteia por Cynefin no intake (perfil simples/claro → caminho curto; perfil ambíguo → nó de desambiguação). | `RoteamentoIntake` |
| **KRITÉS** | Classificador de relevância: recebe candidatos do KANON-LEX + perfil; emite score 0–100, categoria e justificativa curta por publicação. | `ClassificacaoPublicacao[]` |
| **LACONICUS** | Sintetizador: resumo de 2–3 linhas por publicação relevante + sumário executivo do dia. Proibido introduzir fatos ausentes do excerto. | `SintesePublicacao[]` |
| **ELENCHUS** | Gate adversarial: audita amostra (100% se N ≤ 20; senão amostragem estratificada) buscando alucinação, excerto não literal, categoria incoerente. Veto reencaminha ao KRITÉS/LACONICUS com feedback (máx. 2 ciclos → dead-letter). | `VereditoAuditoria` |
| **ANGELOS** | Compositor de entrega: monta Markdown/HTML final a partir do JSON aprovado (template determinístico Jinja2; a mente só preenche campos livres de prosa do sumário). | `RelatorioComposto` |

---

## 5. GRAFO — LangGraph StateGraph (9 nós, 3 gates)

```
[1 intake_perfil] ──► [2 coleta_ophthalmoi] ──► [3 normalizacao_dedup (MNÉMON)]
        │                                              │
        ▼                                              ▼
   HÉGEMON valida                          [4 filtro_lexical (KANON-LEX)]
   perfil (Cynefin)                                    │
                                                       ▼
                                        ◆ GATE 1 — determinístico
                                        (corpus_hash fixado; schema OK;
                                         quotas de fonte respeitadas)
                                                       │
                                                       ▼
                                          [5 classificacao (KRITÉS)]
                                                       │
                                                       ▼
                                          [6 sintese (LACONICUS)]
                                                       │
                                                       ▼
                                        ◆ GATE 2 — adversarial (ELENCHUS
                                          + TEKMÉRION: evidência literal,
                                          URLs vivas, zero alucinação)
                                                       │
                                                       ▼
                                          [7 agregacao (STATISTA)]
                                                       │
                                                       ▼
                                          [8 composicao (ANGELOS)]
                                                       │
                                                       ▼
                                        ◆ GATE 3 — HITL opcional
                                        (homologação de fonte/perfil novo,
                                         ou flag --hitl)
                                                       │
                                                       ▼
                                          [9 entrega (arquivo/e-mail/webhook)]
```

**Falhas:** qualquer nó excedido em retries → **dead-letter** (`.argos/dlq/` com payload SACP completo) + circuit breaker por fonte (3 falhas consecutivas de um adapter → fonte suspensa na execução, relatório marca a lacuna explicitamente — **nunca silencia fonte ausente**).

---

## 6. CONTRATOS PYDANTIC

```python
from pydantic import BaseModel, HttpUrl, Field
from datetime import date
from typing import Literal

class PublicacaoNormalizada(BaseModel, extra="forbid"):
    id_canonico: str            # sha256(fonte + edicao + secao + offset)
    fonte: str                  # "DOU-INLABS" | "QD-4305207" | "DOE-RS" ...
    esfera: Literal["federal", "estadual", "municipal"]
    uf: str | None
    data_publicacao: date
    edicao: str
    secao: str | None           # "DO1" | "DO2" | "DO3" | "DO1E" (extra)
    orgao: str | None           # caminho hierárquico normalizado
    tipo_ato: str | None        # Portaria, Edital, Extrato, ...
    identifica: str | None      # rótulo do ato (INLABS <Identifica>)
    ementa: str | None
    texto: str                  # texto puro, tags removidas
    url_original: HttpUrl
    pagina: str | None
    hash_conteudo: str

class PerfilInteresse(BaseModel, extra="forbid"):
    nome: str
    fontes: list[str]
    termos: list[str] = Field(min_length=1)
    termos_ignorados: list[str] = []
    orgaos: list[str] = []
    tipos_ato: list[str] = []
    secoes: list[str] = []      # filtro por seção do DOU, se aplicável
    janela: Literal["DIA", "SEMANA", "MES"] = "DIA"
    entrega: list[Literal["arquivo", "email", "webhook"]] = ["arquivo"]

class ClassificacaoPublicacao(BaseModel, extra="forbid"):
    id_canonico: str
    relevancia: int = Field(ge=0, le=100)
    categoria: str
    justificativa: str = Field(max_length=280)
    excerto_evidencia: str      # DEVE existir literalmente no texto (TEKMÉRION)

class SintesePublicacao(BaseModel, extra="forbid"):
    id_canonico: str
    resumo: str = Field(max_length=400)

class VereditoAuditoria(BaseModel, extra="forbid"):
    aprovado: bool
    itens_reprovados: list[str] = []
    motivos: dict[str, str] = {}
```

### 6.1 Contrato `AdapterDiario` (o coração do Anel C)

```python
from typing import Protocol
from datetime import date

class AdapterDiario(Protocol):
    codigo: str                         # "DOE-RS"
    dominios_permitidos: list[str]      # allowlist de egress
    rate_limit_rpm: int

    def listar_edicoes(self, inicio: date, fim: date) -> list["EdicaoRef"]: ...
    def obter_publicacoes(self, ref: "EdicaoRef") -> list[PublicacaoNormalizada]: ...
    def healthcheck(self) -> "StatusFonte": ...
```

Todo adapter acompanha: fixture de teste com edição real congelada, teste de contrato, e ficha de homologação HITL (fonte, base legal de acesso, fragilidades de layout).

---

## 7. PERFIL DE INTERESSE — YAML (exemplo)

```yaml
perfil:
  nome: contratos-iffar
  fontes: [DOU-INLABS, DOE-RS, QD-4305207]   # QD: Frederico Westphalen
  secoes: [DO1, DO3]                          # atos normativos + contratos/licitações
  termos:
    - "Instituto Federal Farroupilha"
    - "IFFar"
    - "repactuação"
    - "conta-depósito vinculada"
  termos_ignorados:
    - "concurso público"
  orgaos:
    - "Ministério da Educação"
  tipos_ato: [Extrato, Portaria, Aviso, Edital]
  janela: DIA
  entrega: [arquivo, email]
```

---

## 8. CLI — Especificação

```
argos fontes listar                    # roster de adapters e status (healthcheck)
argos fontes homologar DOE-RS          # suíte de contrato + ficha HITL (§11)
argos perfil validar contratos-iffar   # Pydantic + dry-run
argos buscar --perfil contratos-iffar --data 2026-07-02
argos buscar --perfil contratos-iffar --janela SEMANA --hitl
argos relatorio abrir --ultimo
argos dlq listar | argos dlq reprocessar <id>
argos replay <run_id>                  # replay determinístico (auditoria)
```

**Integração com agente CLI:** o ARGOS expõe uma **SKILL.md** (`argos-vigilancia-diarios`) descrevendo comandos, contratos e o padrão de cron com **Etapa 0 explícita de carregamento de contexto** (perfis disponíveis, estado do MNÉMON), já que execuções agendadas não têm memória implícita. O agente CLI vira o operador humano-assistido do squad: interpreta pedidos em linguagem natural ("o que saiu sobre repactuação esta semana?") e os traduz em invocações determinísticas do `argos buscar`.

---

## 9. RELATÓRIO — Estrutura de saída

1. **Cabeçalho de auditoria:** run_id, corpus_hash, perfil_hash, fontes consultadas × fontes com falha (explícitas), janela temporal.
2. **Sumário executivo** (LACONICUS, ≤ 8 linhas).
3. **Achados por categoria**, cada item com: título do ato, órgão, fonte/edição/data, resumo (≤ 3 linhas), excerto-evidência literal, **link para a edição original**.
4. **Estatísticas** (STATISTA): volumes por fonte, órgão, tipo de ato.
5. **Apêndice de lacunas:** fontes suspensas por circuit breaker, itens em dead-letter.

Formatos: `.md` (canônico), `.html` (Jinja2 determinístico), `.json` (integração).

---

## 10. ADAPTER DOU-INLABS — Especificação Detalhada

O olho `DOU-INLABS` é o primeiro a entrar em produção. É o de maior maturidade porque consome um **dataset oficial estruturado** — não há scraping de portal.

### 10.1 Fatos de fundamento
- INLABS disponibiliza **XML + PDF das edições completas do DOU**, gratuito desde 01/01/2020.
- Acesso exige **credencial de portal** (usuário/senha), como confirma a integração do Ro-DOU (conexão `inlabs_portal`).
- A Imprensa Nacional publica scripts de exemplo (Bash, Python 3) para download automatizado no repositório `Imprensa-Nacional/inlabs`.
- Indisponibilidades do serviço são de responsabilidade da Central da Imprensa Nacional, não do adapter — o circuit breaker trata isso como lacuna, não como falha do ARGOS.

> **Nota de verificação:** a estrutura de atributos/tags do XML abaixo reflete o layout consolidado do INLABS. Como o schema pode sofrer ajustes pontuais, o adapter deve **validar contra fixtures congeladas** (§13) e tratar campos ausentes como `None` — nunca assumir presença.

### 10.2 Seções do DOU

| Código | Seção | Conteúdo típico |
|---|---|---|
| **DO1** | Seção 1 | Atos normativos: leis, decretos, portarias, resoluções, instruções normativas |
| **DO2** | Seção 2 | Atos de pessoal: nomeações, exonerações, aposentadorias |
| **DO3** | Seção 3 | Contratos, editais, avisos de licitação, extratos, ratificações |
| **DO1E/DO2E/DO3E** | Edições extras | Publicações extraordinárias |

Para o perfil `contratos-iffar`, o foco é **DO1** (instruções normativas, portarias) e **DO3** (extratos de contrato, avisos, editais).

### 10.3 Fluxo do adapter (determinístico)

```
listar_edicoes(inicio, fim):
  1. autenticar no portal INLABS (POST credenciais → cookie de sessão)
     - credenciais vêm de variável de ambiente / secret store, nunca hardcoded
  2. para cada dia útil no intervalo [inicio, fim]:
       montar URL do pacote diário por seção (DO1, DO2, DO3 + extras)
  3. retornar list[EdicaoRef] (uma ref por seção-dia disponível)

obter_publicacoes(ref):
  1. baixar o pacote .zip da seção-dia (com cookie de sessão)
  2. verificar no MNÉMON se hash do zip já foi processado → se sim, retornar cache
  3. descompactar → iterar cada arquivo .xml (um <article> por matéria)
  4. parsear (§10.4) → PublicacaoNormalizada[]
  5. registrar hash + cursor no MNÉMON
  6. limpar arquivos temporários (não persistir zips além do TTL de cache)

healthcheck():
  - tentar autenticar + HEAD no pacote do último dia útil
  - retornar StatusFonte(ok|degradado|indisponivel, latencia, ultima_edicao)
```

### 10.4 Parsing do XML (`<article>`)

Cada matéria é um elemento `<article>` com atributos de metadado e um `<body>` com o conteúdo. O parser mapeia:

| Origem no XML | Campo `PublicacaoNormalizada` | Observação |
|---|---|---|
| `@id` / `@name` | compõe `id_canonico` (com hash) | identificador da matéria |
| `@pubName` | `secao` | ex.: `DO1`, `DO3` |
| `@pubDate` | `data_publicacao` | normalizar para ISO `date` |
| `@artType` | `tipo_ato` (bruto) | ex.: "Portaria", "Extrato de Contrato" |
| `@artCategory` | `orgao` | caminho hierárquico separado por `/` → normalizar |
| `@numberPage` / `@pdfPage` | `pagina` | página no PDF da edição |
| `@editionNumber` | compõe `edicao` | número da edição |
| `<body>/<Identifica>` | `identifica` | rótulo do ato (ex.: "PORTARIA Nº 123") |
| `<body>/<Ementa>` | `ementa` | resumo oficial, quando presente |
| `<body>/<Titulo>`, `<SubTitulo>` | prefixo do `texto` | |
| `<body>/<Texto>` | corpo de `texto` | **remover tags HTML internas** → texto puro |

**Regras de parsing:**
1. O conteúdo de `<Texto>` frequentemente contém HTML embutido (`<p>`, `<br>`, entidades). Passar por um sanitizador determinístico → texto puro estável (mesma entrada ⇒ mesma saída byte a byte).
2. `id_canonico = sha256(f"DOU-INLABS|{secao}|{edicao}|{@id}")` para idempotência entre execuções.
3. `hash_conteudo = sha256(texto_puro_normalizado)` para detectar republicações/retificações.
4. `url_original` deve apontar para a página oficial de leitura da matéria no DOU (padrão `in.gov.br/web/dou/-/...` quando derivável do metadado) **ou**, na ausência, para o PDF da seção-dia. Nunca deixar vazio — item sem URL é descartado com log.
5. `@artCategory` normalizado: aparar espaços, unificar caixa, dividir em `orgao_raiz / orgao_folha` para permitir filtro por órgão do perfil.

### 10.5 Egress e credenciais
- `dominios_permitidos = ["inlabs.in.gov.br", "in.gov.br"]`.
- Credenciais em `INLABS_USER` / `INLABS_PASSWORD` (env) ou secret store; jamais em YAML de perfil ou em commit.
- Cookie de sessão mantido em memória durante o run; renovado sob 401/expiração; nunca persistido em disco.

### 10.6 Cache e idempotência (MNÉMON)
- Tabela `edicoes_processadas(fonte, secao, data, edicao, hash_zip, processado_em)`.
- Tabela `publicacoes(id_canonico, hash_conteudo, primeira_vez_em, ultima_vez_em)`.
- Reexecução do mesmo dia: se `hash_zip` bate, retorna do cache sem baixar de novo (respeito ao servidor + reprodutibilidade).
- Retificação detectada quando `id_canonico` reaparece com `hash_conteudo` diferente → marcada no relatório como **"republicação/retificação"**.

### 10.7 Erros e resiliência
| Situação | Tratamento |
|---|---|
| 401 / sessão expirada | Reautenticar 1×; se falhar, `StatusFonte=indisponivel` + lacuna no relatório |
| Pacote do dia ainda não publicado | Não é erro; cursor não avança; retry no próximo run |
| Zip corrompido / XML malformado | Isolar a matéria com falha em DLQ; **demais matérias do pacote seguem** |
| Servidor INLABS fora do ar | Circuit breaker; relatório declara lacuna; orientar reporte à Central da IN |

---

## 11. HOMOLOGAÇÃO HITL DE FONTES — Protocolo e Ficha

Todo adapter do Anel C (estadual) — e qualquer fonte nova em geral — só entra no roster de produção após **homologação humana**. Isto protege contra três riscos: acesso por via ilegítima, parsing frágil que produz lixo silencioso, e proveniência quebrada.

### 11.1 Quando a homologação é obrigatória
- Primeiro cadastro de um adapter novo.
- Mudança estrutural no parser de uma fonte existente (novo layout do portal).
- Reativação de fonte que ficou suspensa por circuit breaker por > 30 dias.

### 11.2 Gate técnico automático (pré-requisito da ficha)
Antes de o humano avaliar, `argos fontes homologar <CODIGO>` roda e **deve passar**:
1. **Teste de contrato:** o adapter implementa `AdapterDiario` (assinaturas, tipos).
2. **Fixtures congeladas:** ≥ 2 edições reais salvas em `tests/fixtures/<codigo>/`; parse reproduzível byte a byte.
3. **Proveniência:** 100% das publicações da fixture têm `url_original` viva (TEKMÉRION) e `data_publicacao` válida.
4. **Idempotência:** rodar 2× a mesma edição ⇒ mesmos `id_canonico`.
5. **Egress:** nenhuma requisição fora de `dominios_permitidos`.
6. **Cortesia:** `rate_limit_rpm` declarado e respeitado no dry-run.

Só com o gate técnico verde a ficha é aberta para assinatura humana.

### 11.3 Ficha de Homologação de Fonte (template)

```markdown
# FICHA DE HOMOLOGAÇÃO — Fonte <CODIGO>
Data: <YYYY-MM-DD> · Responsável (HITL): <nome/matrícula>

## 1. Identificação
- Código do adapter: DOE-RS
- Esfera / UF: estadual / RS
- Nome oficial da publicação: Diário Oficial do Estado do Rio Grande do Sul
- Órgão publicador: <ex.: CORAG / Secretaria X>
- URL-base do portal: <https://...>

## 2. Base legal e legitimidade de acesso  [BLOQUEANTE]
- [ ] Acesso por via oficial e pública (API documentada / portal aberto / dados abertos)
- [ ] Sem contorno de mecanismo anti-robô (sem CAPTCHA burlado, sem Selenium contra bloqueio)
- [ ] Termos de uso do portal revisados e compatíveis
- Método de acesso: ( ) API oficial  ( ) API JSON exposta  ( ) HTML  ( ) PDF nato-digital
- Observações legais: __________

## 3. Qualidade de extração
- Nº de edições em fixture: ____   Período coberto: ____
- Campos preenchidos de forma confiável:
  - [ ] data_publicacao   [ ] orgao   [ ] tipo_ato   [ ] texto puro   [ ] url_original
- Taxa de matérias com URL verificável na fixture: ____%  (meta: 100%)
- Fragilidades conhecidas de layout: __________
- Estratégia de detecção de quebra: __________ (ex.: healthcheck + assert de estrutura)

## 4. Resultado do gate técnico automático
- Contrato AdapterDiario: ( ) PASS ( ) FAIL
- Idempotência: ( ) PASS ( ) FAIL
- Egress allowlist: ( ) PASS ( ) FAIL
- Proveniência (URLs vivas): ( ) PASS ( ) FAIL

## 5. Decisão HITL
- ( ) HOMOLOGADO para produção
- ( ) HOMOLOGADO com ressalvas (fonte em modo "observação", não bloqueante no relatório)
- ( ) REPROVADO — motivo: __________
- Assinatura / carimbo de tempo: __________
```

### 11.4 Estados de uma fonte no roster
- **`producao`** — homologada; falhas contam para circuit breaker.
- **`observacao`** — homologada com ressalvas; coleta rodando, mas lacunas não disparam alarme (período de confiança).
- **`suspensa`** — circuit breaker aberto; relatório declara a ausência; requer nova homologação para religar após 30 dias.
- **`backlog`** — fonte sem via legítima de acesso; documentada, não coletada. Registrar pedido via LAI quando cabível.

---

## 12. ESQUELETO DOE-RS (primeiro olho estadual)

Passos de implementação, sem código final — o adapter concreto nasce da inspeção legítima do portal:

1. **Descoberta:** inspecionar o portal do DOE-RS para identificar a via de acesso menos frágil (preferir endpoint JSON, se exposto; senão HTML de listagem por data; PDF como último recurso).
2. **`listar_edicoes(inicio, fim)`:** mapear como o portal expõe edições por data (parâmetro de query, calendário, ou índice).
3. **`obter_publicacoes(ref)`:** extrair matérias; se a granularidade for de edição inteira (não por matéria), segmentar por marcadores de ato (regex de "PORTARIA Nº", "EXTRATO", etc.) de forma determinística e conservadora — sem inventar fronteiras.
4. **Normalização:** preencher `esfera="estadual"`, `uf="RS"`, e o máximo de metadado confiável; deixar `None` o que não for seguro.
5. **Fixtures + ficha:** congelar 2+ edições, rodar gate técnico, abrir ficha HITL (§11.3).
6. **Modo `observacao`** por 2 semanas antes de promover a `producao`.

---

## 13. LAYOUT DE REPOSITÓRIO E PLANO DE TESTES

### 13.1 Layout

```
squads/argos/
├── SKILL.md                      # skill do agente CLI (argos-vigilancia-diarios)
├── model_profile.yaml            # modelos/temperaturas pinados por mente
├── pyproject.toml
├── src/argos/
│   ├── cli.py                    # entrypoint (argos ...)
│   ├── graph.py                  # StateGraph LangGraph (9 nós, 3 gates)
│   ├── state.py                  # estado tipado do grafo
│   ├── contracts.py              # Pydantic (§6) + AdapterDiario Protocol
│   ├── ophthalmoi/               # adapters (os "olhos")
│   │   ├── base.py               # AdapterDiario + utilidades de egress/rate-limit
│   │   ├── dou_inlabs.py         # §10
│   │   ├── querido_diario.py
│   │   └── doe_rs.py             # §12
│   ├── engines/
│   │   ├── mnemon.py             # SQLite: cursores, cache, dedup
│   │   ├── kanon_lex.py          # filtro lexical determinístico
│   │   ├── tekmerion.py          # verificação de evidência/URL
│   │   └── statista.py           # agregações
│   ├── minds/
│   │   ├── hegemon.py krites.py laconicus.py elenchus.py angelos.py
│   ├── report/
│   │   ├── templates/*.jinja2    # markdown/html determinísticos
│   │   └── compose.py
│   └── delivery/ (arquivo|email|webhook)
├── perfis/
│   └── contratos-iffar.yaml
└── tests/
    ├── fixtures/<codigo>/*.xml   # edições reais congeladas
    ├── test_contrato_adapters.py
    ├── test_golden_report.py
    └── test_mnemon_idempotencia.py
```

### 13.2 Plano de testes por camada

| Camada | Tipo de teste | Critério |
|---|---|---|
| Adapters (OPHTHALMOI) | Contrato + fixtures congeladas | Parse reproduzível byte a byte; 100% URL viva na fixture |
| MNÉMON | Propriedade de idempotência | 2 execuções ⇒ mesmos `id_canonico`; cache evita redownload |
| KANON-LEX | Unitário determinístico | `termos`/`termos_ignorados`/regex órgão dão subconjunto exato esperado |
| TEKMÉRION | Unitário | Excerto não literal é reprovado; URL morta é reprovada |
| Grafo | Golden report | Corpus fixo + perfil fixo + modelo pinado ⇒ relatório idêntico ao golden (partes determinísticas) e schema-válido (partes LLM) |
| Gates | Integração | Gate 2 veta item com excerto fabricado; Gate 3 exige assinatura para fonte nova |
| CLI | Smoke | Todos os comandos de §8 respondem; `--hitl` bloqueia entrega até aprovação |

---

## 14. OBSERVABILIDADE, SLOs E QUOTAS

- **Langfuse:** trace por run; spans por nó; custo de tokens por mente; tags `perfil`, `fonte`, `gate`.
- **SLOs iniciais:** run diário do perfil padrão ≤ 10 min; zero itens no relatório sem URL verificada (SLO absoluto); taxa de veto do ELENCHUS < 5% em regime.
- **Quota engine:** teto de tokens por run e por mente; teto de requisições por fonte; estouro → degradação declarada no relatório (nunca corte silencioso).
- **Modelos pinados:** `model_profile.yaml` com modelo/versão/temperatura por mente; mudança de perfil = novo PR.

---

## 15. ROADMAP

| Fase | Entrega | Critério de pronto |
|---|---|---|
| **F0** | Grafo + **DOU-INLABS (§10)** + KANON-LEX + relatório MD | Run diário reproduzível do perfil `contratos-iffar` só com DOU |
| **F1** | Adapter Querido Diário + Gate 2 completo (ELENCHUS + TEKMÉRION) | Busca mista DOU+QD com auditoria adversarial |
| **F2** | **DOE-RS (§12)** + **homologação HITL (§11)** + DLQ/replay | DOE-RS homologado com fixtures congeladas e ficha assinada |
| **F3** | SKILL.md + cron (Etapa 0) + entrega e-mail/webhook | Operação autônoma agendada |
| **F4** | DOEs SC/PR/SP + guia "como escrever um olho" | 4 UFs em produção |
| **F5+** | Demais UFs por demanda; OCR opcional; painel de cobertura | — |

---

## 16. RISCOS E MITIGAÇÕES

| Risco | Mitigação |
|---|---|
| Mudança de layout de portal estadual quebra adapter | Testes de contrato com fixtures + healthcheck no início do run + circuit breaker + lacuna explícita no relatório |
| Bloqueio anti-robô em DOE | Fonte sai de produção até haver via legítima; nunca evasão. Registrar pedido via LAI quando cabível |
| Alucinação em resumo | Gate 2: excerto-evidência literal obrigatório (TEKMÉRION byte a byte) + ELENCHUS |
| Sobrecarga da API do Querido Diário | Rate limit conservador (≤ 30 rpm), cache local no MNÉMON, janelas incrementais por cursor |
| Deriva de custo de tokens | KANON-LEX filtra antes do LLM; quota engine; teto de publicações por run |
| INLABS indisponível | Retry com backoff + fallback para reprocessamento no dia seguinte via cursor do MNÉMON |

---

## 17. DEFINIÇÃO DE PRONTO

- [ ] DOU-INLABS em produção com parsing validado por fixtures (§10, §13)
- [ ] ≥ 1 DOE homologado com **ficha assinada** (§11) e 2 semanas em `producao` estáveis
- [ ] Querido Diário integrado (busca mista)
- [ ] 100% dos itens de relatório com URL verificada e excerto literal validado
- [ ] Replay determinístico de qualquer run dos últimos 30 dias
- [ ] Suíte de testes por camada (§13.2) verde no CI
- [ ] SKILL.md publicada e cron diário estável por 2 semanas sem intervenção
- [ ] Zero referência a frameworks guarda-chuva no documento e no código

---

*Squad ARGOS — "cem olhos, um contrato".*
