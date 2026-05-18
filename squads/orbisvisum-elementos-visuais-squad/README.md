# OrbisVisum — Squad de Mapeamento Visual e Solução Multiagente

## O que é este squad

O **OrbisVisum** é um squad criado para analisar imagens complexas — como prints, infográficos, carrosséis, telas de sistemas, páginas de documentos, quadros visuais e materiais com muitos elementos — e transformar essas imagens em uma estrutura compreensível, organizada e acionável.

Ele não apenas descreve a imagem. O objetivo é mapear os elementos visuais e textuais, entender a solicitação do usuário e conduzir o problema por uma cadeia de agentes até chegar a uma solução, relatório, blueprint ou artefato final.

## Para que serve

O squad serve para situações em que uma imagem contém informação demais para uma simples descrição. Ele ajuda a:

- identificar todos os elementos visíveis da imagem;
- organizar textos, títulos, categorias, códigos, cores, layouts e relações espaciais;
- separar observação visual de interpretação;
- transformar imagens em diagnóstico, estrutura, taxonomia ou plano de ação;
- encaminhar a solicitação por agentes especializados;
- construir uma resposta final, solução operacional ou material derivado das imagens.

## Estrutura dos agentes

O OrbisVisum opera com 8 agentes principais:

1. **briefing-intake**
   Interpreta a solicitação inicial do usuário, identifica objetivo, contexto, restrições, tipo de entrega esperada e critérios de sucesso.

2. **visual-cartographer**
   Mapeia os elementos visuais das imagens: títulos, blocos, objetos, ícones, cores, hierarquia, composição, páginas, agrupamentos e relações espaciais.

3. **ocr-semantics**
   Extrai textos, siglas, termos, categorias e conceitos presentes na imagem, transformando conteúdo visual em dados estruturados.

4. **problem-framer**
   Converte o mapa visual em uma formulação de problema: o que precisa ser resolvido, construído, explicado, organizado ou validado.

5. **solution-architect**
   Define a arquitetura da solução: sequência de execução, componentes, dependências, formato de saída e critérios de validação.

6. **builder-executor**
   Constrói o entregável final, que pode ser relatório, blueprint, checklist, roteiro, prompt, base de conhecimento, estrutura de squad ou outro artefato solicitado.

7. **quality-sentinel**
   Valida se todos os elementos relevantes foram considerados e se existe rastreabilidade entre imagem, observação, interpretação e solução final.

8. **publication-bridge**
   Organiza a entrega ao usuário, prepara o resumo final, orienta próximos passos e consolida o material para publicação, envio ou reutilização.

## O que o squad entrega no final

Ao final do fluxo, o OrbisVisum entrega um conjunto estruturado de saídas, incluindo:

- inventário das imagens analisadas;
- mapa dos elementos visuais e textuais;
- extração semântica dos conceitos encontrados;
- enquadramento do problema ou objetivo do usuário;
- blueprint da solução;
- artefato final construído conforme a solicitação;
- relatório de validação;
- nota de entrega com síntese e próximos passos.

Na prática, o squad transforma imagens em entendimento, entendimento em decisão e decisão em um entregável utilizável.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
