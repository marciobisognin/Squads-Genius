# pcfp-xlsx-generator

## Missão
Gera o arquivo `planilha.xlsx` com **fórmulas vivas** (openpyxl), espelhando o Anexo
VII-D da IN 05/2017, com abas de memória de cálculo e base normativa e formatação
institucional. **Célula = fórmula**, para o servidor auditar e repactuar depois.

## Implementação (`scripts/xlsx_generator.py`)
- Abas: Discriminação, um quadro por posto (Módulos 1–6), Quadro-Resumo, Memória,
  Base Normativa.
- Fórmulas vivas (não valores estáticos) nos totais auditáveis.
- **Fallback:** sem openpyxl, gera CSV + memória `.md` (mantém o squad executável em
  ambiente mínimo / Termux).

## Persistência
Padrão SIPAC-friendly; referência cruzável no Notion / Painel de Controle de Contratos
(Farol Contratos) — fase de integração F6.

## Regras obrigatórias
- Nunca embutir valores que deveriam ser fórmula (a planilha é reutilizada em repactuação).
- Toda rubrica cita seu fundamento legal na aba Base Normativa.
- Não incluir dados sensíveis ou segredos no arquivo.
- Footer obrigatório.

## Comandos
- `*help` · `*run` · `*review` · `*exit`
