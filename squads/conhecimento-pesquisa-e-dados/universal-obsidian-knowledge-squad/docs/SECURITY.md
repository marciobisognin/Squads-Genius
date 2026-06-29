# Segurança e Privacidade

1. Nunca alterar notas sem autorização explícita (write/curate bloqueados por padrão).
2. Nunca indexar segredos (token, chave, `.env`): notas com padrão de segredo
   são puladas e reportadas.
3. Pastas privadas excluídas via `exclude_patterns`.
4. Mecanismo de exclusão é próprio do squad (não há `.obsidianignore` nativo).
5. Resposta citada separada de inferência do agente.
6. Toda afirmação do vault tem fonte verificável.
7. Índice local por padrão.
8. Conteúdo do vault não vai a APIs externas sem consentimento explícito.
9. Embeddings externos são opcionais, gated e documentados.
10. Modo `write` bloqueado por padrão.
11. Nenhum conteúdo de vault, índice ou caminho pessoal é versionado (`.gitignore`).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
