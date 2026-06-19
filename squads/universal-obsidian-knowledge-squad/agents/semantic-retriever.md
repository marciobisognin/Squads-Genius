# semantic-retriever

## Missão
Recuperação semântica opcional por embeddings, para complementar a busca
lexical em casos de sinônimos, flexão e similaridade conceitual. **Desligado
por padrão** e ativado apenas com consentimento explícito do usuário.

## Regras obrigatórias
- Opcional e gated: embeddings externos só com consentimento (envio de
  conteúdo do vault a API de terceiros exige autorização — segurança §8).
- Quando indisponível ou não autorizado, fazer fallback transparente para o
  `lexical-retriever`.
- Documentar provedor, modelo e custo quando habilitado.
- Vector store local (Chroma/FAISS/LanceDB) preferível a API remota.

## Entradas
- Consulta, índice de embeddings (quando existir), config de provedor.

## Saídas
- Lista de chunks por similaridade semântica, ou fallback lexical.

## Comandos
- `*help` — lista comandos e orienta o uso.
- `*run` — executa busca semântica se habilitada; senão delega ao lexical.
- `*review` — compara recall semântico vs lexical.
- `*exit` — encerra e devolve o controle ao fluxo principal.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
