# Biblioteca de Mentes — Sága Mind-Keeper

Evolui o `mimir_dna` de destilador para um **repositório de mentes** reutilizáveis e
**injetáveis** em agentes de squads ou funcionários de empresas.

## As 5 camadas de uma mente
1. **Cadência de voz** — estatísticas de comprimento de frase.
2. **Textura lexical** — type-token ratio, comprimento médio de palavra.
3. **Estrutura retórica** — proporção de perguntas/exclamações, densidade de vírgulas.
4. **Vetores temáticos** — palavras isoladas de alta frequência (não protegíveis; sem frases).
5. **Marcadores de tom** — primeira/segunda pessoa, registro (formal/coloquial).

## Salvaguardas de PI
- Nenhum n-grama verbatim de 4+ palavras da fonte é emitido (verificado automaticamente).
- A injeção adiciona **apenas descritores abstratos** (`voice_profile`) — nunca texto.
- Perfis declaram proveniência como "referência de estilo", não cópia.

## Uso
```bash
python3 scripts/mind_clone_library.py --library ./dna --add "Voz Institucional" --input material.txt
python3 scripts/mind_clone_library.py --library ./dna --list
python3 scripts/mind_clone_library.py --library ./dna --inject "Voz Institucional" --agent-name "Delivery Builder"
```

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
