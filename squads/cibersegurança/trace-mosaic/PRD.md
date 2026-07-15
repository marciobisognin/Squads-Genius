# PRD — Trace Mosaic

## Problema
Operações de cibersegurança falham quando escopo, proveniência, segurança, evidência e reteste são tratados como detalhes.

## Produto
Converter fontes públicas em inteligência verificável, proporcional e transparente, preservando proveniência, confiança, contradições e privacidade.

## Requisitos funcionais
- definir pergunta e finalidade legítima
- planejar fontes e limites
- normalizar registros
- resolver entidades e contradições
- correlacionar evidências
- atribuir confiança
- revisar privacidade
- emitir inteligência auditável
- CLI determinística com saídas JSON/CSV/Markdown.
- validação estrutural e smoke test local.
- bloqueio explícito de ações ofensivas destrutivas.

## Requisitos não funcionais
- Python standard library; compatível com Termux.
- dados sintéticos nos exemplos.
- nenhum segredo nos outputs.
- arquivos reprodutíveis e hashes quando empacotados.

## Critérios de aceite
- `squad.yaml` e arquivos declarados existem.
- CLI compila e executa os comandos documentados.
- smoke test gera entregáveis não vazios.
- teste unitário passa.
- secret scan não encontra credenciais.

## Integração da trilha de cibersegurança — v2

Este squad incorpora a trilha fornecida por Marcio como um sistema auditável de aprendizagem e operação. Contém 19 recursos/ferramentas e 5 técnicas do seu domínio. O roteador local apenas cataloga, audita disponibilidade e decide `GATED_HANDOFF`, `PLAN_ONLY` ou `DENY`; ele não lança scanners, exploits, payloads ou malware.

```bash
python scripts/capability_router.py catalog
python scripts/capability_router.py audit
python scripts/capability_router.py route --technique osint-source-planning --context public --band 0
```
