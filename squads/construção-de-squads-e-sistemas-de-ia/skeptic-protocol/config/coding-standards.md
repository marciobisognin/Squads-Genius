# Coding Standards: SKEPTIC Protocol

1. **Aversão Criminosa a Código Invisível:** Na Fase 1 (Accusation), é um erro fatal emitir código binário, pseudocódigo funcional ou trechos copiáveis de linguagem. Apenas documentação estrutural.
2. **"Red Phase" Obrigatória:** O código de teste (Fase 2) obrigatoriamente tem que quebrar contra uma árvore de código vazia ou vulnerável. `AssertThrows`, validações estritas de erro e fluxos de injeção são a norma.
3. **Pessimismo de Borda:** Comentários ao longo do processo (Fase 4 - Appeal) jamais devem elogiar a implementação, mas elencar exaustivamente o que ela não suportou ou o que ignorou.
4. **Relatório Absoluto:** O `SKEPTIC_REPORT.md` nunca omite uma "Derrota". Se uma acusação se provou complexa demais para a Fase 3 superar, é listada em "Limitações Residuais Acordadas".
5. **Clean Code:** Na Fase 3 (Trial), o desenvolvedor respeita KISS (Keep It Simple, Stupid) e DRY (Don't Repeat Yourself).
