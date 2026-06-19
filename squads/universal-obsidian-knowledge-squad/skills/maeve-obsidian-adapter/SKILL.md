---
name: maeve-obsidian-adapter
description: Optional adapter skill. Use only when the Maeve agent operates the Universal Obsidian Knowledge Squad and the user wants Maeve's executive voice, pt-BR delivery, and integration with Maeve routines. Not required for other users or agents.
---

# Maeve Obsidian Adapter (opcional)

Adaptador **opcional e isolado** para quando a Maeve operar o squad. O núcleo
do squad não depende deste adaptador.

## O que ajusta
- Idioma padrão pt-BR e tom executivo e direto.
- Entrega de arquivos em caminho **resolvido por env/config** (`MAEVE_DELIVERY_PATH`);
  nunca caminho fixo embutido.
- Integração com rotinas da Maeve e resposta com síntese executiva + fontes.

## Regras
- Não alterar o vault sem autorização explícita.
- Manter citações verificáveis; conhecimento citado vem do vault.
- Carregar este adaptador apenas quando `runtime.agent_adapter: "maeve"`.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
