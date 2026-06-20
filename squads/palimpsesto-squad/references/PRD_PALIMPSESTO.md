# PRD — Squad **PALIMPSESTO**
### Sistema multi-agente de reconstrução contextual imersiva (Filosofia × História × Geografia × Política)

> *Palimpsesto* (gr. *palímpsēstos*, "raspado de novo"): pergaminho reaproveitado em que, sob a escrita nova, as camadas antigas ainda transparecem. Todo fato, texto ou personagem é um palimpsesto — um empilhamento de camadas linguísticas, geográficas, religiosas, políticas e filosóficas. Este squad existe para **raspar e revelar essas camadas**, uma a uma, e então recompô-las numa experiência de imersão total.

**Versão:** 1.1
**Data:** 19/06/2026
**Autor:** Marcio Bisognin
**Repositório-alvo:** `marciobisognin/Squads-Genius`
**Baseline arquitetural:** OMNISCIENT v7.0 (contratos SACP, HITL gate, Cynefin entry-gate, observabilidade Langfuse)
**Changelog v1.1:** inclusão do agente **ÁGON** (contra-perspectiva e contrafactual) na Camada 2, garantindo a multiperspectiva como etapa estrutural — não mais embutida implicitamente em KRATOS.

*Nomes alternativos considerados:* ANAMNESE (recordação platônica), CRONOSCÓPIO, OIKOUMENE, AION. Mantive PALIMPSESTO pela precisão da metáfora; o nome interno do orquestrador pode ser `O Tecelão`.

---

## 1. Sumário executivo

PALIMPSESTO recebe **qualquer objeto de conhecimento histórico-cultural** (um trecho da Bíblia, um evento, uma personalidade, um conceito, um lugar) e devolve não uma explicação, mas uma **reconstrução do mundo ao redor do objeto** — datado, situado geograficamente, traduzido na semântica original da língua falada, encharcado da política, da religião e das ideias da época — e finalmente **narrado em segunda pessoa, no presente histórico**, de modo que o usuário *atravesse* para dentro daquele instante.

A diferença frente a uma resposta comum não é de quantidade, é de **eixo**: a explicação comum responde *"o que isto diz"*; PALIMPSESTO responde *"o que era estar vivo no mundo em que isto foi dito, e o que estas palavras faziam com quem as ouvia"*.

Dois compromissos inegociáveis governam tudo:

1. **Imersão máxima** — a saída precisa transportar, não listar.
2. **Rigor epistemológico máximo** — nada de anacronismo, nada de detalhe inventado disfarçado de fato. Cada afirmação carrega um **grau de certeza**, e a fronteira entre *consenso acadêmico*, *hipótese* e *reconstrução plausível* é sempre visível. Imersão sem rigor vira ficção; o squad recusa esse atalho.

---

## 2. Problema e oportunidade

**Problema.** Explicações de fatos históricos, textos sagrados ou personagens costumam ser:
- *achatadas no tempo* — projetam o presente sobre o passado (anacronismo);
- *cegas à língua* — perdem o que a palavra original significava e conotava;
- *desencarnadas* — sem geografia, clima, cheiro, hierarquia, medo, fé;
- *monodisciplinares* — o historiador ignora a filologia, o teólogo ignora a geopolítica;
- *epistemicamente opacas* — misturam fato consolidado e palpite no mesmo tom de voz.

**Oportunidade.** Um pipeline multi-agente onde cada disciplina é um agente especialista, orquestrados sob um contrato comum, com um agente final dedicado exclusivamente à *experiência* e um agente-guardião dedicado exclusivamente à *verdade*. Nenhum humano consegue, sozinho e em tempo real, ser simultaneamente filólogo do hebraico, geógrafo do Levante, cientista político do Império Romano e narrador. O squad consegue.

---

## 3. Objetivos e métricas de sucesso

| Objetivo | Métrica | Meta v1 |
|---|---|---|
| Imersão | Avaliação humana (1–5) "senti-me transportado" | ≥ 4,3 |
| Rigor | % de afirmações factuais com grau de certeza explícito | 100% |
| Anti-anacronismo | Anacronismos detectados em auditoria por amostragem | < 1 a cada 20 respostas |
| Cobertura multidisciplinar | Nº de camadas ativadas quando pertinentes (das 5 núcleo) | ≥ 4/5 em objetos ricos |
| Rastreabilidade | % de afirmações de alto risco com fonte/escola apontada | ≥ 90% |
| Controle de profundidade | Usuário consegue regular extensão sem perder coerência | 3 níveis funcionais |

---

## 4. Personas e casos de uso

- **O leitor curioso** — leu um versículo, um trecho de Heródoto, uma frase de Maquiavel, e quer *sentir* o mundo por trás.
- **O criador de conteúdo** (você) — material denso e fiel para Reels/Manim, RPG (*Ecos da Singularidade*), roteiros.
- **O estudante/educador** — contexto rigoroso e citável, com graus de certeza para não ensinar lenda como fato.
- **O worldbuilder** — extrair a "textura de época" para construir mundos verossímeis.

Gatilhos típicos: *"explique este versículo"*, *"o que foi a Batalha de Cannas"*, *"quem foi Hipátia"*, *"o que significava 'cidadão' em Atenas"*, *"me leve para Tenochtitlán em 1500"*.

---

## 5. Princípios de design

1. **Camada antes de conclusão.** Reconstruir o mundo precede interpretar o objeto.
2. **A língua é território.** A semântica original de uma palavra-chave vale mais que três parágrafos de paráfrase.
3. **Separar os três tempos.** Tempo do *evento*, tempo da *escrita/registro*, tempo da *descoberta/recepção* — nunca confundi-los (ver §8.1).
4. **Multiperspectiva obrigatória.** O olhar do poder e o olhar do governado; o centro e a margem.
5. **Honestidade epistêmica radical.** "Não se sabe" é uma resposta de primeira classe. Plausível ≠ atestado.
6. **Imersão é o último passo, nunca o primeiro.** Só se narra o que já foi verificado.
7. **Anti-anacronismo como reflexo.** Toda metáfora moderna passa por um filtro: ela ilumina ou ela falsifica?

---

## 6. Arquitetura em 4 camadas

```
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 0 — ENTRADA & ROTEAMENTO                             │
│  Triador (classifica o objeto, define profundidade e trilhas)│
└───────────────┬─────────────────────────────────────────────┘
                │ (contrato SACP-IN)
┌───────────────▼─────────────────────────────────────────────┐
│  CAMADA 1 — RECONSTRUÇÃO (agentes especialistas, paralelos)  │
│  CHRONOS · TERRA · VERBUM · ETHOS · KRATOS · NUMEN · NOÛS    │
└───────────────┬─────────────────────────────────────────────┘
                │ (camadas brutas + claims com certeza)
┌───────────────▼─────────────────────────────────────────────┐
│  CAMADA 2 — CONTRA-PERSPECTIVA, VERIFICAÇÃO & CURADORIA      │
│  ÁGON (advogado dos vencidos / contrafactual)               │
│   → ELENCHUS (guardião das fontes) → O Tecelão (curador)    │
│  ⟲ HITL gate opcional para temas sensíveis                  │
└───────────────┬─────────────────────────────────────────────┘
                │ (dossiê verificado + grafo de certeza)
┌───────────────▼─────────────────────────────────────────────┐
│  CAMADA 3 — IMERSÃO & ENTREGA                                │
│  AEDO (o imersor) + PONTE (conexão com o presente)           │
└─────────────────────────────────────────────────────────────┘
```

Princípio de fluxo: **Camada 1 reconstrói → ÁGON pluraliza (injeta a voz ausente) → ELENCHUS verifica e poda → Camada 3 só então narra.** A imersão jamais ocorre sobre material não verificado, e a reconstrução nunca repousa numa única perspectiva.

---

## 7. Os agentes (detalhamento)

Cada agente abaixo segue o mesmo gabarito: **papel · entradas · saídas · regras de ouro · semente de prompt**.

### 7.0 — `Triador` · Cartógrafo de Entrada (Camada 0)
- **Papel:** classificar o objeto e montar o *plano de escavação*.
- **Classifica em:** {texto sagrado/literário, evento, personalidade, conceito/ideia, lugar, objeto material, processo de longa duração}.
- **Decide:** quais das 7 trilhas da Camada 1 ativar (nem todo objeto precisa de NUMEN ou VERBUM); o **nível de profundidade** (1 = essencial, 2 = imersivo, 3 = exaustivo); o recorte espaço-temporal provável.
- **Saída:** `SACP-IN` (ver §9).
- **Regra de ouro:** na dúvida, ativa mais trilhas — a poda é função da Camada 2, não da entrada.
- **Semente:** *"Você é o cartógrafo de entrada. Classifique o objeto, identifique os três tempos prováveis (evento/registro/recepção), liste as trilhas disciplinares pertinentes e justifique cada exclusão. Não interprete o objeto; apenas mapeie o terreno a escavar."*

### 7.1 — `CHRONOS` · O Estratígrafo do Tempo
- **Papel:** datar e separar os três tempos; construir a linha do tempo de camadas.
- **Entrega:** quando o evento ocorreu; quando foi posto por escrito / registrado; quando foi descoberto, canonizado ou redescoberto; quais camadas de redação/edição existem (ex.: hipótese documental, redações sucessivas).
- **Regra de ouro:** *nunca* colapsar "quando aconteceu" com "quando foi escrito". No exemplo bíblico, isto é o coração da resposta.
- **Semente:** *"Estabeleça a estratigrafia temporal. Distinga rigorosamente: tempo do evento, tempo da escrita, tempo da descoberta/recepção. Aponte camadas de redação e o estado do debate sobre datação, com graus de certeza."*

### 7.2 — `TERRA` · O Cartógrafo (geografia física e humana)
- **Papel:** reconstruir o espaço — clima, relevo, hidrografia, recursos, rotas, distâncias reais, paisagem sonora e olfativa, densidade populacional, fronteiras.
- **Entrega:** como a geografia *condicionava* a vida e o evento (por que ali? o que essa terra permite e proíbe?).
- **Regra de ouro:** geografia não é cenário, é causa. Sempre conectar terreno → economia → poder.
- **Semente:** *"Reconstrua o espaço físico e humano. Traduza a geografia em condições concretas de vida e em vetores de causalidade (recursos, rotas, defensibilidade). Forneça distâncias e tempos de viagem da época, não os modernos."*

### 7.3 — `VERBUM` · O Filólogo (linguística histórica)
- **Papel:** a língua falada e a língua do texto; etimologia e *campo semântico* das palavras-chave; conotações perdidas na tradução; trocadilhos, registros, fórmulas.
- **Entrega:** 2–5 palavras-chave do objeto **na língua original**, com o que significavam *então* (não hoje), o que a tradução apaga e por quê.
- **Regra de ouro:** uma palavra-chave bem reconstruída transforma a compreensão inteira. Priorizar profundidade sobre cobertura.
- **Semente:** *"Identifique a língua falada e a do registro. Selecione as palavras decisivas, dê transliteração, campo semântico de época, conotação cultural e o que a tradução moderna distorce. Sinalize incerteza filológica quando houver."*

### 7.4 — `ETHOS` · O Etnógrafo do Cotidiano
- **Papel:** história das mentalidades e da vida material (escola dos *Annales*) — como comiam, vestiam, trabalhavam, morriam; família, gênero, infância, escravidão; o que era pensável e impensável; medos, honra, tempo, corpo.
- **Entrega:** a *textura sensorial e mental* do cotidiano de uma pessoa comum daquele mundo.
- **Regra de ouro:** descer ao anônimo, não só ao rei. A vida do camponês é dado, não pano de fundo.
- **Semente:** *"Reconstrua o cotidiano e a mentalidade de um indivíduo comum desse mundo: corpo, comida, trabalho, crença vivida, estrutura familiar, percepção do tempo e da morte. Evite projetar sensibilidades modernas."*

### 7.5 — `KRATOS` · O Analista de Poder
- **Papel:** estrutura política e econômica — quem manda, como, sobre quem; instituições, leis, tributo, guerra, facções, economia política; relações centro–periferia e império–súdito.
- **Entrega:** o mapa de forças no qual o objeto está inscrito; interesses materiais por trás dos discursos.
- **Regra de ouro:** todo texto e todo evento tem um vetor de poder. Perguntar sempre: *a quem serve?*
- **Semente:** *"Mapeie o campo de poder: instituições, hierarquias, economia, conflitos e interesses. Mostre como o objeto se posiciona nesse campo e a quem favorece. Distinga ideologia declarada de função real."*

### 7.6 — `NUMEN` · O Historiador das Religiões
- **Papel:** sistemas de crença, mitologia, ritual, sacerdócio, o sagrado e o tabu; como a religião permeava direito, política e cotidiano; concorrência entre cultos.
- **Entrega:** o horizonte religioso da época — o que era óbvio crer, o que era heresia, como o divino se manifestava na vida pública.
- **Regra de ouro:** tratar a religião como sistema vivo e plausível para quem a vivia, sem deboche e sem apologética. Descrição, não juízo de fé.
- **Semente:** *"Reconstrua o sistema religioso operante: panteão/teologia, ritos, sacerdócio, tabus, e a interpenetração entre religião e ordem social. Adote a perspectiva interna do crente da época, mantendo distância analítica."*

### 7.7 — `NOÛS` · O Historiador das Ideias
- **Papel:** a *episteme* da época (Foucault) — cosmovisões, filosofias dominantes, o que se considerava conhecimento, verdade, virtude; correntes em disputa; o "espírito do tempo".
- **Entrega:** as ideias que tornavam aquele objeto *dizível e inteligível*; o pano de fundo conceitual invisível para os contemporâneos.
- **Regra de ouro:** reconstruir o pensável, não avaliá-lo pelo padrão de hoje.
- **Semente:** *"Reconstrua o horizonte intelectual: cosmovisão, correntes filosóficas, noções de verdade/virtude/natureza vigentes. Explicite os pressupostos invisíveis que tornavam o objeto inteligível em seu tempo."*

### 7.8 — `ÁGON` · O Advogado dos Vencidos (contra-perspectiva e contrafactual)
- **Papel:** impedir que a reconstrução seja apenas a versão do vencedor, do poder e da fonte que *sobreviveu*. Revisa os claims da Camada 1 e injeta sistematicamente três coisas: **a perspectiva dos silenciados** (vencidos, escravizados, mulheres, povos sem escrita, hereges, margens); **os contrafactuais** ("e se?" — o que estava em jogo, os caminhos não tomados, as alternativas reais que os contemporâneos viam); e **o viés da fonte** (quem escreveu o registro que chegou até nós, e a quem ele convinha).
- **Entradas:** `claims[]` da Camada 1 + `SACP-IN`.
- **Saídas:** claims adicionais de contra-perspectiva (marcados `origin: AGON`) + `tensions[]` (versões rivais) — que **também passam por ELENCHUS**: a contra-perspectiva não é licença para inventar.
- **Regra de ouro:** a voz dos vencidos é **reconstrução verificável, não compensação ficcional**. Quando a fonte da margem simplesmente não existe, dizer que não existe é a resposta — e essa ausência *já é, ela própria, um fato político* (quem teve direito a registro?).
- **Por que existe:** a maioria esmagadora dos registros que chegam até nós foi escrita por quem venceu e sabia escrever. Sem um agente dedicado, o squad herdaria esse viés silenciosamente, com fluência e autoridade.
- **Nome:** *ágon* — a arena grega da disputa, onde versões rivais competem diante do público.
- **Semente:** *"Você é o advogado dos ausentes. Sobre o material reconstruído, pergunte sempre: de quem é este olhar? Quem está silenciado nesta fonte? Como isto soaria do lado dos vencidos, dos governados, dos sem-escrita? Que caminhos não tomados estavam realmente em jogo? Gere a contra-perspectiva e os contrafactuais — mas apenas o que for reconstruível; onde a fonte falta, declare a ausência como o fato político que ela é."*

### 7.9 — `ELENCHUS` · O Guardião das Fontes (verificação)
- **Papel:** o **freio epistemológico**. Audita cada *claim* dos agentes da Camada 1.
- **Entrega por claim:** fonte/escola, grau de certeza, status {consenso · majoritário · disputado · hipótese · reconstrução plausível · desconhecido}, e **poda** do que for anacrônico, lendário-vendido-como-fato ou alucinado.
- **Poder de veto:** pode rebaixar qualquer afirmação a "plausível/incerto" ou removê-la; sinaliza lacunas honestas ("aqui não se sabe").
- **Regra de ouro:** *na dúvida, rebaixar.* É melhor um "provavelmente" verdadeiro que uma certeza falsa.
- **Nome:** *élenchos* — o exame socrático que testa a alegação até o osso.
- **Semente:** *"Você é o cético rigoroso. Para cada afirmação recebida, atribua fonte, escola e grau de certeza; marque anacronismos e invenções; rebaixe o duvidoso; declare explicitamente o que é desconhecido. Não embeleze. Sua lealdade é à verdade, não à fluência."*

### 7.10 — `O Tecelão` · Curador-Editor / Orquestrador (verificação → entrega)
- **Papel:** orquestra o pipeline, resolve conflitos entre agentes, controla profundidade, monta o **dossiê verificado** e o **grafo de certeza** que alimenta a Camada 3.
- **Entrega:** dossiê coerente, sem redundância, com tensões interpretativas *preservadas* (não achatadas).
- **Regra de ouro:** divergência entre escolas é informação, não defeito — preservar o debate.
- **Semente:** *"Orquestre e cure. Funda as camadas num dossiê coerente, preserve divergências legítimas, elimine redundância, calibre a profundidade ao nível pedido e prepare o material verificado para narração imersiva."*

### 7.11 — `AEDO` · O Imersor (entrega)
- **Papel:** transformar o dossiê verificado em **experiência**. Segunda pessoa, presente histórico, apelo sensorial, ritmo cinematográfico — *te coloca lá*.
- **Restrição dura:** **só pode usar material que passou por ELENCHUS.** Não inventa detalhe sensorial sem ancoragem; quando recria atmosfera plausível mas não atestada, marca-o como recriação.
- **Nome:** o *aedo*, poeta-cantor grego que fazia o passado presente diante da audiência.
- **Semente:** *"Pegue o dossiê verificado e transporte o leitor. Escreva em 2ª pessoa, presente histórico, com densidade sensorial e tensão narrativa. Toda imagem deve ancorar-se em material verificado; sinalize o que é recriação atmosférica. Faça-o sentir o lugar, o medo, a fé, o poder."*

### 7.12 — `PONTE` · Conexão com o Presente (entrega)
- **Papel:** por que isto importa hoje; o que mudou e o que permanece; ecos no presente — sem anacronismo retroativo.
- **Semente:** *"Construa a ponte ao presente: ressonâncias, heranças e contrastes, sem projetar o hoje sobre o passado. Responda 'por que isto ainda nos toca'."*

---

## 8. Orquestração e fluxo

### 8.1 — A regra dos três tempos (núcleo conceitual)
Para o exemplo bíblico, esta regra é o que separa PALIMPSESTO de uma explicação comum:

| Tempo | Pergunta | Agente líder |
|---|---|---|
| **Tempo do evento** | Quando/onde o relatado teria acontecido? | CHRONOS + TERRA |
| **Tempo do registro** | Quando, por quem, em que língua e contexto político-religioso foi *escrito*? | CHRONOS + VERBUM + KRATOS + NUMEN |
| **Tempo da recepção** | Quando foi descoberto/canonizado/relido, e como o sentido se deslocou? | CHRONOS + NOÛS + PONTE |

### 8.2 — Pipeline
1. **Triador** classifica → emite `SACP-IN`.
2. **Camada 1** roda em paralelo as trilhas ativadas; cada agente emite `claims[]` com certeza preliminar.
3. **ÁGON** revisa os claims, injeta a contra-perspectiva (voz ausente, contrafactuais, viés de fonte) e abre `tensions[]`.
4. **ELENCHUS** audita *tudo* (incluindo os claims de ÁGON), atribui certeza, poda, marca lacunas.
5. **(HITL gate opcional)** para temas sensíveis (religião viva, genocídios, disputas identitárias, política contemporânea): pausa para revisão humana.
6. **O Tecelão** funde no dossiê verificado + grafo de certeza, calibra profundidade.
7. **AEDO** narra; **PONTE** fecha com o presente.
8. **Observabilidade** (Langfuse/LangSmith): traço completo, custo, latência, claims rebaixados.

### 8.3 — Modos de profundidade
- **Nível 1 — Vislumbre:** 3 camadas-chave + abertura imersiva curta (~Reels/Manim).
- **Nível 2 — Imersão (default):** todas as trilhas pertinentes + narração completa + ponte.
- **Nível 3 — Escavação:** todas as camadas, divergências de escolas, aparato de fontes, notas filológicas extensas.

---

## 9. Contratos de dados (SACP — handoff JSON)

**`SACP-IN`** (Triador → Camada 1):
```json
{
  "object": "Mt 5,5 — 'Bem-aventurados os mansos...'",
  "object_type": "texto_sagrado",
  "depth": 2,
  "tracks": ["CHRONOS","TERRA","VERBUM","ETHOS","KRATOS","NUMEN","NOUS"],
  "tracks_excluded": [],
  "tentative_window": {"event": "séc. I d.C.", "register": "c. 80–90 d.C.", "region": "Galileia / Síria romana"},
  "sensitivity_flag": "religiao_viva",
  "notes": "Ativar regra dos três tempos; foco filológico em 'praÿs' e 'gē'."
}
```

**`Claim`** (agente da Camada 1 → ELENCHUS):
```json
{
  "agent": "VERBUM",
  "statement": "O grego 'praÿs' não significa 'fraco', mas força contida / domada — usado para o cavalo treinado.",
  "layer": "linguistica",
  "preliminary_certainty": 0.8,
  "source_hint": "léxico do grego koiné; uso clássico do termo",
  "risk": "medio"
}
```

**`VerifiedClaim`** (ELENCHUS → Tecelão):
```json
{
  "statement": "...",
  "certainty": 0.85,
  "status": "majoritario",
  "source": "...",
  "schools_in_dispute": [],
  "anachronism_check": "pass",
  "elenchus_note": "Mantido; conotação bem atestada no koiné."
}
```

**`Dossier`** (Tecelão → AEDO): objeto agregando `verified_claims[]` por camada + `tensions[]` (divergências preservadas) + `certainty_graph` + `depth`.

Grau de certeza → rótulo: `≥0.9 consenso` · `0.7–0.9 majoritário` · `0.4–0.7 disputado/hipótese` · `<0.4 reconstrução plausível` · `null desconhecido`.

---

## 10. Formato da entrega (estrutura da resposta imersiva)

A saída ao usuário (Nível 2) segue esta sequência — projetada para *primeiro transportar, depois explicar, sempre datar a certeza*:

1. **A Travessia** (AEDO) — abertura em 2ª pessoa, presente histórico, que coloca o leitor *no lugar e no instante*.
2. **Os Três Tempos** (CHRONOS) — quando aconteceu, quando foi escrito, quando chegou até nós.
3. **A Terra** (TERRA) — o espaço como força viva.
4. **As Palavras** (VERBUM) — a língua original e o que se perde na tradução.
5. **A Vida** (ETHOS) — o cotidiano e a mentalidade de quem estava lá.
6. **O Poder e o Sagrado** (KRATOS + NUMEN + ÁGON) — o campo político-religioso, incluindo a versão dos governados e das vozes silenciadas.
7. **O Pensável** (NOÛS) — as ideias que davam sentido a tudo.
8. **A Ponte** (PONTE) — por que ainda nos toca.
9. **Aparato** (opcional, Nível 3) — fontes, divergências, graus de certeza, notas.

Marcadores de certeza inline (ex.: `[consenso]`, `[hipótese]`, `[recriação atmosférica]`) acompanham as afirmações de risco.

---

## 11. Exemplo trabalhado (esqueleto)

**Entrada:** *"Explique 'Bem-aventurados os mansos, porque herdarão a terra' (Mt 5,5)."*

- **Triador:** texto sagrado · profundidade 2 · três tempos ON · foco filológico em *praÿs* (manso) e *gē* (terra) · `sensitivity_flag: religiao_viva`.
- **CHRONOS:** evento atribuído ao ministério de Jesus (c. 28–30 d.C.) `[majoritário]`; redação de Mateus c. 80–90 d.C. em grego `[majoritário]`; comunidade provavelmente judaico-cristã pós-destruição do Templo (70 d.C.) `[disputado]` — *três tempos distintos que a leitura ingênua funde*.
- **TERRA:** Galileia/Síria romana; economia de pequenos proprietários sob pressão fiscal; "herdar a terra" ressoa numa população para quem **terra = sobrevivência e dignidade perdida**, não metáfora abstrata.
- **VERBUM:** *praÿs* não é "fraco/submisso" no koiné, mas **força domada, contida** — termo aplicável ao cavalo treinado `[majoritário]`; *gē* oscila entre "a terra (solo)" e "a Terra (criação)" `[disputado]` — a tradução fixa o que o original deixa vibrar.
- **ETHOS:** o que era ser "manso" numa cultura de honra-e-vergonha mediterrânea, onde retaliação era virtude — a bem-aventurança é **contracultural**, não consoladora.
- **KRATOS:** sob ocupação romana e elite herodiana; "herdar a terra" tem carga **politicamente inflamável** (esperança de reversão da ordem) `[hipótese]`.
- **NUMEN:** ecoa o Salmo 37; horizonte apocalíptico judaico do séc. I; "herança" como categoria teológica da aliança.
- **NOÛS:** noção de bem-aventurança (*makarios*) entre ética judaica e ecos da filosofia helenística da felicidade.
- **ÁGON:** *de quem é a promessa?* Do lado romano/herodiano, "os mansos herdarão a terra" não é consolo — é **sedição em estado latente**: anuncia a reversão de uma ordem que tributa e ocupa. E a voz que falta: das mulheres e dos escravizados na multidão da encosta quase nada sobrou em registro `[ausência atestada]` — o silêncio aqui é, ele mesmo, dado político.
- **ELENCHUS:** rebaixa a leitura "puramente espiritual" a `[disputado]`; marca a datação da comunidade como `[hipótese]`; veta qualquer leitura que importe "humildade" no sentido cristão-medieval (anacronismo).
- **AEDO:** *"Você está numa encosta acima do mar da Galileia. O sol bate forte; o cheiro é de poeira e peixe seco. Ao redor, gente que deve impostos a um rei que serve a Roma. E um homem diz que os fracos-sem-fraqueza herdarão exatamente aquilo que lhes foi tirado: a terra..."*
- **PONTE:** por que "força contida" e "herança dos sem-terra" ainda mobilizam.

---

## 12. Guardrails

- **Anti-alucinação:** AEDO só usa material verificado; detalhe sensorial sem ancoragem vira `[recriação atmosférica]` explícita.
- **Anti-anacronismo:** todo termo/conceito moderno passa pelo filtro de ELENCHUS (ilumina vs. falsifica).
- **Honestidade sobre lacunas:** "não se sabe" é saída válida e visível.
- **Religião viva e temas sensíveis:** descrição respeitosa de perspectiva interna, sem apologética nem deboche; HITL gate disponível.
- **Multiperspectiva:** incluir o olhar do governado/marginal, não só do poder.
- **Disputa preservada:** divergência de escolas aparece como tal, nunca achatada num falso consenso.

---

## 13. Stack e implementação

- **Orquestração:** LangGraph (grafo de estados; paralelismo na Camada 1; gate condicional HITL).
- **Contratos:** Pydantic schemas para `SACP-IN`, `Claim`, `VerifiedClaim`, `Dossier`.
- **Modelos:** modelo forte para ELENCHUS/Tecelão/AEDO; modelos mais baratos para trilhas paralelas; chamada à API Anthropic.
- **RAG (fase 2):** base curada de fontes (atlas históricos, léxicos koiné/hebraico, corpora primários, sínteses acadêmicas) para ancorar ELENCHUS.
- **Observabilidade:** Langfuse — traço, custo, latência, taxa de claims rebaixados (KPI de rigor).
- **Saída:** Markdown estruturado §10; variante "roteiro" para Manim/Reels.

---

## 14. Roadmap

- **Fase 0 — PoC:** Triador + 4 trilhas (CHRONOS, VERBUM, KRATOS, NUMEN) + ELENCHUS + AEDO, sem RAG. Valida o fluxo e a regra dos três tempos.
- **Fase 1 — Completo sem RAG:** 7 trilhas + Tecelão + PONTE + 3 níveis de profundidade + observabilidade.
- **Fase 2 — RAG ancorado:** base de fontes curada; ELENCHUS consulta antes de atribuir certeza.
- **Fase 3 — HITL + variantes de saída:** gate para temas sensíveis; export roteiro Manim/RPG (*Ecos da Singularidade*).
- **Fase 4 — Auto-avaliação:** loop estilo Turing Guild auditando anacronismo e calibração de certeza.

---

## 15. Riscos

| Risco | Mitigação |
|---|---|
| Imersão arrasta para a ficção | ELENCHUS antes de AEDO; marcação `[recriação atmosférica]` |
| Anacronismo sutil | Filtro dedicado + auditoria por amostragem |
| Falsa autoridade (palpite com tom de fato) | Grau de certeza obrigatório em 100% das afirmações |
| Custo/latência (muitos agentes) | Paralelismo + roteamento por trilha + modelos escalonados |
| Temas sensíveis | HITL gate + perspectiva interna respeitosa + multiperspectiva |
| Viés de fonte / "história só dos vencedores" | **ÁGON** como etapa obrigatória + RAG curado + preservação explícita de divergências |

---

### Apêndice — Glossário dos agentes
**Triador** (entrada) · **CHRONOS** (tempo) · **TERRA** (geografia) · **VERBUM** (língua) · **ETHOS** (cotidiano/mentalidade) · **KRATOS** (poder) · **NUMEN** (religião) · **NOÛS** (ideias) · **ÁGON** (contra-perspectiva/contrafactual) · **ELENCHUS** (verificação) · **O Tecelão** (curadoria/orquestração) · **AEDO** (imersão) · **PONTE** (presente).
