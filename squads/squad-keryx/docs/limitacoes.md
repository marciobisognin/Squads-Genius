# KÊRYX — Limitações, riscos e mitigações

## Fora de escopo (v1)
- Publicação automática no Instagram (Graph API) → fase futura (F6).
- **Texto educativo renderizado pela IA de imagem.** No Trilho B a IA gera só a arte; todo
  texto é vetorial sobreposto (letterer determinístico) — evita "texto garbled".
- Vídeo/Reels (coberto por outro pipeline).
- Caption/legenda do post → fase futura.

## Riscos & mitigações (resumo do PRD seção 15)
| Risco | Mitigação |
|---|---|
| Overflow de texto | Loop KANON↔auto-fit + re-paginação determinística |
| Render não-reprodutível | Fontes embutidas, `networkidle`, render_hash em testes |
| Conteúdo clichê | MOMUS + exigência de `cotidiano_hook` por slide |
| Erro factual sobre livros/autores | MOMUS com `web_search` em afirmações verificáveis |
| Repetição de temas | `store` anti-repetição com janela configurável |
| Uso indevido de marca de terceiros | Canto = slot da marca **do usuário** |
| [B] Texto garbled da IA | Texto 100% vetorial sobreposto |
| [B] Personagem inconsistente | Character sheet obrigatório + seed por painel + gate HITL |
| [B] Custo/latência de imagem | Gate de roteiro antes de gerar; lote; cache por seed+prompt |
| [B] Imitar artista vivo | ZEUXIS cria arte original; sem nomes de artistas nos prompts |

## Premissas
- Ambiente de render (jinja2 + playwright + pillow) instalado para gerar PNG/PDF reais;
  sem ele, os scripts degradam para manifesto + hashes determinísticos (auditáveis).
- Backend de geração de imagem do Trilho B é **plugável** e não acompanha este squad.

## Nota de IP & atribuição
Os sistemas baoyu (@JimLiu/baoyu-skills, MIT) são usados como **vocabulário de design** e
**reimplementados** sob arquitetura própria — sem copiar código ou identidade visual de marcas.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
