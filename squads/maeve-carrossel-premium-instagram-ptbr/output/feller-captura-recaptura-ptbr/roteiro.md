# Roteiro — Problema de captura-recaptura de Feller

## Slide 01

**O lago invisível**

Como estimar quantos peixes existem se não dá para contar um por um? A estatística resolve olhando uma parte bem escolhida.

## Slide 02

**A ideia de Feller**

Capture alguns peixes, marque, solte de volta e espere eles se misturarem. Depois capture outra amostra.

## Slide 03

**O segredo está na proporção**

Se muitos marcados reaparecem, o lago provavelmente é menor. Se poucos reaparecem, o lago provavelmente é maior.

## Slide 04

**Primeira amostra: M**

M é a quantidade de peixes marcados na primeira captura. Eles viram “sinalizadores” dentro do lago.

## Slide 05

**Segunda amostra: n**

Depois da mistura, capturamos n peixes. Alguns terão a marca; outros não. Essa mistura carrega informação.

## Slide 06

**Recapturados: R**

R é a quantidade de peixes marcados encontrados na segunda amostra. Ele é o número-chave da estimativa.

## Slide 07

**Estimativa intuitiva**

A fração de marcados na amostra deve parecer a fração de marcados no lago: M/N ≈ R/n.

## Slide 08

**A fórmula prática**

Reorganizando a proporção, obtemos N ≈ M × n / R. É uma regra simples para estimar o total oculto.

## Slide 09

**Onde entra a hipergeométrica?**

A distribuição hipergeométrica calcula a chance de recapturar R marcados quando retiramos n peixes de uma população finita sem reposição.

## Slide 10

**Exemplo numérico**

Se marquei 100, recapturei 80 e encontrei 20 marcados, a estimativa é 100×80/20 = 400 peixes.

## Slide 11

**Condições importantes**

O lago precisa ser fechado, as marcas não podem desaparecer, e os peixes marcados devem se misturar como os outros.

## Slide 12

**O poder do método**

A captura-recaptura mostra como uma pequena amostra pode revelar uma população inteira — quando o modelo é bem usado.
