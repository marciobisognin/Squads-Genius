# Nota de Propriedade Intelectual e Mitologia

## Origem dos nomes
O Bifröst Forge Engine usa nomes e conceitos da **mitologia nórdica**, registrados há
séculos na **Edda Poética** (século XIII, compilada de tradição oral anterior) e na
**Edda em Prosa** de Snorri Sturluson. Esse acervo é **domínio público** e patrimônio
cultural comum da humanidade.

| Elemento no engine | Origem mitológica (domínio público) |
|---|---|
| Allfather / Odin | Óðinn, o Pai-de-Tudo |
| Heimdall | Heimdallr, o vigia de Bifröst |
| Bifröst | a ponte-arco-íris entre os reinos |
| Yggdrasil | a árvore-mundo |
| Nornas | Urðr, Verðandi, Skuld — teceduras do destino |
| Valquíria | as escolhedoras dos caídos |
| Huginn & Muninn | os corvos Pensamento e Memória |
| Mímir | o guardião do poço da sabedoria |
| Eitri, Brokkr | os ferreiros anões de Niðavellir |
| Freyja | deusa associada ao ouro e ao valor |

## O que NÃO é usado (para evitar infração)
- **Não** usamos o nome de nenhum estúdio de cinema ou editora, nem suas marcas.
- **Não** reproduzimos personagens exclusivos, roteiros, diálogos, trilhas, logotipos,
  artes conceituais, figurinos ou grafias/designs proprietários de qualquer franquia.
- **Não** copiamos identidade visual, cores de marca ou ativos de terceiros: o design
  system é gerado deterministicamente a partir do nome do projeto.
- **Não** copiamos código, prompts ou textos de outros projetos; a inspiração conceitual
  (orquestração, auditoria, factories) foi reimplementada de forma original.

## Salvaguardas técnicas
- `mimir_dna.py` extrai apenas padrões estruturais/estatísticos de material público e
  **bloqueia** a emissão de qualquer n-grama verbatim de 4+ palavras.
- `eitri_design.py` deriva cores de um hash do nome do projeto — nunca de uma marca.
- `heimdall_validate.py` faz scan de segredos e rejeita credenciais.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
