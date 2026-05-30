# Nirvana README Architect — Coding Standards

## Linguagem
- Conteúdo do README em Português (PT-BR) com acentuação correta por padrão
- Se o projeto for em inglês, gerar README em inglês
- Variáveis, IDs e código em inglês (padrão internacional)
- UTF-8 obrigatório em todos os arquivos

## Tom e Voz
- Profissional mas acessível
- Direto ao ponto — sem rodeios
- Imperativo para instruções ("Execute", "Configure", "Instale")
- Descritivo para explicações ("O sistema utiliza...", "A arquitetura consiste em...")

## Estrutura
- H1 apenas para o nome do projeto (1 por README)
- H2 para seções principais (TOC aponta para estes)
- H3 para sub-seções dentro de uma seção
- H4 raramente, apenas para detalhes dentro de sub-seções
- Linha em branco antes e depois de cada heading
- Linha em branco antes e depois de code blocks, tables, alerts

## Code Blocks
- SEMPRE especificar linguagem após ` ``` `
- Linguagens comuns: `bash`, `typescript`, `javascript`, `python`, `json`, `yaml`, `sql`, `go`, `rust`, `diff`
- Comandos de terminal: usar `bash` ou `sh`
- Outputs de terminal: usar `text` ou `console`

## Tables
- SEMPRE incluir header e separador
- Alinhar colunas para legibilidade no source
- Usar alinhamento left para texto, center para status, right para números

## Alerts
- NOTE: informações complementares úteis
- TIP: atalhos e dicas práticas
- IMPORTANT: informações que o usuário não pode ignorar
- WARNING: ações que podem causar problemas se ignoradas
- CAUTION: ações que podem causar perda de dados ou danos

## Badges
- Estilo consistente ao longo do README (escolher um: flat, flat-square, for-the-badge)
- Ordenar: build > coverage > version > license > linguagem
- Usar shields.io como fonte padrão

## Emojis
- Usar com parcimônia para scanning visual
- Consistentes ao longo do documento (mesmo emoji para mesmo conceito)
- Nunca como substituto de texto — sempre acompanhados de texto
