# Guia de uso — SCRIPTORIUM

Este guia descreve como operar o squad SCRIPTORIUM em uma sessão e como rodar os
núcleos determinísticos.

## 1. Pré-requisitos
- Python 3.11+ (os scripts não exigem dependências externas).
- (Opcional, produção) Acesso aos índices Semantic Scholar, OpenAlex, Crossref,
  arXiv; Pandoc/Tectonic/Typst para finalização; Ollama para cross-model.

## 2. Ativação como squad (LLM)
1. Leia `squad.yaml`.
2. Assuma a persona do `agents/maestro.md` (orquestrador do StateGraph).
3. Conduza o usuário pelos 10 estágios de `workflows/scriptorium-pipeline.yaml`.
4. Em cada handoff, produza/valide o JSON do contrato correspondente em `templates/`.
5. **Nunca** pule os gates 2.5 e 4.5. Em falha, acione `guarda-de-auto-cura` (máx. 3) antes de escalar.

### Checkpoints humanos (não delegáveis)
- Estágio 1: confirma pergunta + método.
- Estágio 2: aprova o esqueleto antes da redação.
- Gate 2.5 e 4.5: *ack* de integridade.
- Estágio 3: revê a decisão editorial.
- Estágio 5: escolhe o formato de saída.
- Estágio 6: confirma idioma e revê a colaboração.

## 3. Modos de operação
- **Investigação:** completo, rápido, maiêutico, revisão, revisão-de-literatura, scan-comparativo, checagem-de-fatos, revisão-sistemática (PRISMA).
- **Escrita:** completo, plano, só-esboço, revisão, coach-de-revisão, só-abstract, conversão-de-formato, checagem-de-citação, declaração-de-IA, auditoria-de-réplica.
- **Parecer:** completo, re-revisão, rápido, foco-método, guiado, calibração.

## 4. Variáveis de ambiente
| Variável | Efeito |
|---|---|
| `SCR_CROSS_MODEL=1` | Liga o cross-model local (Ollama) na auditoria de integridade e no contraditório. Divergência > 2 pontos é reportada, não suavizada. |
| `SCR_CLAIM_AUDIT=1` | Liga a auditoria de fidelidade opt-in (estágio 4→5), LLM-como-juiz por citação. |

## 5. Núcleos determinísticos

### 5.1 Validar contratos
```bash
python3 scripts/validate_contracts.py
```
Valida as 6 fixtures em `examples/fixtures/` contra os schemas em `templates/`.

### 5.2 Verificação de existência de citação (4 índices, offline)
```bash
python3 scripts/verify_citations.py \
    --citations examples/fixtures/citations_input.json \
    --cache examples/fixtures/index_cache.json \
    [--fuzzy 0.6] [--out output/verificacao.json]
```
- Status por citação: `verificada` / `nao-resolvida` / `inexistente`.
- `inexistente` **apenas** quando um DOI/arXiv-ID exato falha — citações
  regionais/não-indexadas ficam `nao-resolvida` e **não bloqueiam**.
- Código de saída `1` quando há alguma `inexistente` (sinaliza bloqueio do gate
  até *override* humano registrado).

### 5.3 Auditoria anti-bajulação
```bash
python3 scripts/concession_audit.py --log examples/fixtures/contraditorio_log.json
```
- Verifica: concessão só com pontuação ≥ 4; sem concessões consecutivas.
- Reporta a taxa de concessão (não a suaviza). Código de saída `1` se houver violação.

## 6. Retomada de sessão
O `rastreador-de-estado` serializa o `PassaporteDossie`. Para retomar:
```
MAESTRO *resume <hash_passaporte>
```
O `repro_lock` é **documentação pós-hoc**, não garantia de replay byte-a-byte.

## 7. Finalização e segurança
- O *gate* terminal do formatador recusa saída com alegação não-sustentada pendente.
- Nunca publicar `.env`, tokens, chaves ou credenciais (use `gitleaks` no CI).

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
