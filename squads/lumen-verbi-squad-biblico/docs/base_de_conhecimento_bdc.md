# Base de Dados de Conhecimento (BDC)

A BDC é a espinha dorsal do conhecimento do squad. Este repositório versiona a
**camada de metadados** (perfis, mapa semântico, índice de livros). Os **textos
bíblicos integrais não são versionados** por questões de licença/direitos: a BDC
os referencia a partir de versões de domínio público e/ou APIs externas, sempre
citando a versão.

## Camadas

1. **Textos bíblicos canônicos** *(externos)* — múltiplas traduções (ARC, NVI, KJV…)
   e originais (hebraico/aramaico/grego) com marcação de capítulo/versículo.
   Recuperados via fonte pública/API; nunca inventados.
2. **Perfis dos agentes** — `scripts/data/perfis_agentes.json`
   (personas e historiadores: papel, personalidade, estilo, perspectiva, foco, passagens-chave).
3. **Mapa semântico** — `scripts/data/mapa_semantico.json`
   (temas, doutrinas, eventos → agentes relevantes; gatilhos de historiador).
4. **Índice de livros** — `scripts/data/livros_biblia.json`
   (nomes canônicos, abreviações, testamento) para o parser de referências.
5. **Contexto histórico-cultural** *(curadoria do `curador-bdc`)* — eventos,
   costumes, geografia, arqueologia, fontes extrabíblicas (Josefo, Filo, Mar Morto).
6. **Análise linguística** — léxico hebraico-grego-português, concordâncias,
   acionados pelo `critico-textual`.

## Como estender

- **Nova persona/historiador:** acrescente o objeto em `perfis_agentes.json`, crie
  `agents/<id>.md` e registre em `squad.yaml`. Atualize o `mapa_semantico.json`
  com os temas/eventos de afinidade.
- **Novo livro/abreviação:** acrescente em `livros_biblia.json`.
- **Novo tema/evento:** acrescente em `mapa_semantico.json` apontando os agentes.

Após qualquer extensão, rode os testes (`python3 -m pytest -q`) e o
`validate_squad.py` do construtor.

## Integração técnica sugerida (do PRD)

- **Banco vetorial** (Pinecone/Weaviate/Milvus) para embeddings de textos e perfis.
- **Banco relacional/NoSQL** (PostgreSQL/MongoDB) para metadados e histórico.
- **Recuperação de informação** (Elasticsearch/Solr) para busca textual precisa.

Estas integrações são o caminho de produção; o squad versionado entrega a lógica
determinística e os contratos que as alimentam.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
