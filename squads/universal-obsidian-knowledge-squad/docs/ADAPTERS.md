# Adaptadores

O comportamento por agente é definido por `config/adapters/<nome>.yaml` e por
`runtime.agent_adapter`. O núcleo nunca depende de um adaptador específico.

| Adaptador | Voz | Observações |
|---|---|---|
| `generic` | profissional, neutra | padrão; nenhum dado de ambiente |
| `maeve` | executiva, pt-BR | opcional; entrega via `MAEVE_DELIVERY_PATH` (env) |
| `hermes` | assistente, neutra | compatível |

## Regra de portabilidade
Nenhum adaptador embute caminho de dispositivo, nome de usuário ou identidade.
O adaptador Maeve é opcional e isolado: removê-lo não afeta o núcleo.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
