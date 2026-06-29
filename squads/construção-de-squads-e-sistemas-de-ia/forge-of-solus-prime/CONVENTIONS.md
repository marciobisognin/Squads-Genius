# CONVENTIONS.md — Convenções da Forja

## A fronteira determinística
| Lado do LLM (emite só JSON) | Lado do Python (determinístico, auditável) |
|---|---|
| Normalizar briefing em campos | Validar o briefing contra o schema |
| Classificar Cynefin (proposta) | Aplicar regras de roteamento de autonomia/topologia |
| Propor candidatas de ferramentas | **Pontuar** ferramentas (motor `Decimal`) |
| Propor decomposição em tarefas | Verificar contrato de cada tarefa |
| Rascunhar conteúdo de agentes/docs | Renderizar templates, contar tokens, montar ZIP |
| Sugerir correção numa falha | Aplicar patch, rodar testes, recolher evidência |

> **Regra prática:** se um número, um veredito de gate ou um corte de orçamento
> depende do resultado, o cálculo é **Python**. O LLM nunca é a autoridade final
> sobre fatos verificáveis.

## Estilo de código
- Python 3.11+, stdlib-first; dependências externas só quando justificadas.
- Todo script tem `if __name__ == "__main__"`, trata erro e compila.
- Schemas Pydantic v2 com fallback para dataclasses (portabilidade).
- Aritmética com consequência usa `Decimal`.

## Idioma e créditos
- Idioma principal: pt-BR.
- Licença MIT; créditos de autoria (Marcio Bisognin) preservados em README, AUTHORS e footer.
- Footer obrigatório em todos os arquivos:

```text
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
```

## Segurança
- Zero segredos em logs, código ou artefatos.
- Sem rede/credenciais sem gate HITL aprovado.
- Nenhuma ação externa/destrutiva ou publicação sem aprovação humana registrada.

> Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
