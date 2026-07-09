# Integração — API pública de catálogo VTEX (triangulação de varejo)

## O que é

Toda loja construída sobre a plataforma VTEX expõe, **sem autenticação**, o endpoint
de busca de catálogo usado pelo próprio frontend:

```
https://{dominio-da-loja}/api/catalog_system/pub/products/search?ft={termos}&_from=0&_to=19
```

O retorno é um array JSON hierárquico: **produto → variações (SKUs) → vendedores →
oferta comercial** (`commertialOffer` com `Price`, `ListPrice`, `AvailableQuantity`,
`IsAvailable`). O squad usa esse endpoint como **fonte complementar** de pesquisa de
preços, na forma da **IN SEGES/ME nº 65/2021, art. 5º, inciso IV** (sítios eletrônicos
especializados ou de domínio amplo).

## Papel na arquitetura do Farol

| Camada | Fonte | Papel |
|---|---|---|
| Primária | Compras.gov.br / PNCP (`compras_gov.py`) | preço de referência estimado |
| Complementar | Varejo VTEX (`vtex_catalog.py`) | triangulação / sanity check |

Regras de ouro implementadas em `enriquecer_dfd_vtex.py`:

1. **Alerta automático só com match de confiança alta** (similaridade Jaccard ≥ 0,45
   entre a descrição do DFD e o nome do produto). Confiança média (≥ 0,25) vira
   comparação *indicativa* com revisão humana; abaixo disso a cotação fica só como
   evidência.
2. **Aba de evidências obrigatória** (`Evidencias VTEX IN65`): uma linha por cotação
   com loja, produto, SKU, vendedor, preço, disponibilidade, similaridade, **URL da
   consulta e data/hora** — os metadados que a IN 65/2021 exige para uso de
   e-commerce na pesquisa de preços.
3. **Varejo nunca substitui a referência primária**: a avaliação escrita na planilha
   é sempre rotulada como "fonte complementar".

## Limites conhecidos do endpoint

- Janela máxima de **50 itens** por requisição (`_to - _from ≤ 49`).
- Paginação profunda limitada a **~2.500 resultados** por consulta.
- **HTTP 206 (Partial Content) é sucesso normal**, não erro.
- Funciona **apenas em lojas VTEX** — validar domínios com
  `python scripts/vtex_catalog.py verificar --lojas dominio1,dominio2`.
- É o endpoint interno do storefront: aberto por design, porém **sem contrato formal
  de estabilidade** — pode mudar sem aviso. Tratar falhas como degradação elegante,
  nunca como bloqueio do pipeline.
- Parâmetros úteis: `ft=` (busca textual), `_from/_to` (paginação), `O=` (ordenação),
  `fq=` (filtro estruturado por marca/categoria/ID).

## Cuidados de comparabilidade

- Preço de varejo é **B2C**: unitário, com margem, impostos e logística embutidos.
  Não é diretamente comparável a preço homologado em licitação por volume; usar como
  referência contextual para detectar sobrepreço/subpreço grosseiro.
- Divergência forte entre varejo e Compras.gov com match de alta confiança costuma
  indicar **erro de especificação ou de unidade de fornecimento** — escalar para o
  saneamento antes de concluir sobre preço.

## Comandos

```bash
# validar se os domínios respondem como loja VTEX
# (exemplos confirmados em 2026-07: www.epocacosmeticos.com.br, www.cobasi.com.br, www.brastemp.com.br;
#  configure lojas do ramo do objeto licitado — nem todo grande varejista roda VTEX)
python scripts/vtex_catalog.py verificar --lojas www.epocacosmeticos.com.br,www.cobasi.com.br

# cotação avulsa de um item
python scripts/vtex_catalog.py buscar --descricao "caneta esferográfica azul escrita média" --csv output/cotacao.csv

# pesquisa de toda a planilha DFD (resumo + evidências)
python scripts/vtex_catalog.py --cache output/.cache planilha-precos "DFD.xlsx" --out output/vtex-varejo

# pipeline completo: auditoria + varejo VTEX na planilha auditada
python scripts/enriquecer_dfd_vtex.py "DFD.xlsx" --out output/farol-varejo-vtex

# empilhar o varejo sobre a planilha já enriquecida com Compras.gov
python scripts/enriquecer_dfd_vtex.py "DFD.xlsx" \
  --planilha-auditada output/farol-compras-gov/DFD_AUDITADA_COMPRAS_GOV.xlsx \
  --out output/farol-varejo-vtex
```

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
