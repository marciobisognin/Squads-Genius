# Exemplo de execução — SCRIPTORIUM

Caminho ilustrativo de uma sessão completa, do briefing ao artefato publicável.
As fixtures referenciadas estão em `examples/fixtures/`.

## Briefing do usuário
> "Quero escrever um artigo (IMRaD, bilíngue) investigando se copilotos de IA
> com gates de integridade reduzem a alucinação de citações em manuscritos de
> pós-graduação. Tenho ~40 PDFs pré-curados."

## Estágio 0 — Triagem Cynefin
`triador-cynefin` → domínio **Complicated** (há método conhecido: revisão
sistemática + estudo quase-experimental) → modo `revisão-sistemática-PRISMA`.
🧑 Humano confirma.

## Estágio 1 — Investigar (G1)
- `arquiteto-da-questao` → `briefing-de-questao.example.json`.
- `verificador-de-fontes` roda a verificação determinística:

```bash
python3 scripts/verify_citations.py \
    --citations examples/fixtures/citations_input.json \
    --cache examples/fixtures/index_cache.json
```
Resultado: 2 `verificada`, 1 `nao-resolvida` (citação regional PT-BR — **não
bloqueia**), 1 `inexistente` (DOI fabricado — **bloqueia**, exige override ou remoção).

- `critico-adversarial` produz o log do contraditório; auditamos a anti-bajulação:

```bash
python3 scripts/concession_audit.py --log examples/fixtures/contraditorio_log.json
```
Saída: nenhuma concessão com pontuação < 4 → `anti_bajulacao_ok: true`.

🧑 Humano confirma pergunta + método.

## Estágio 2 — Escrever (G2)
Esqueleto IMRaD → mapa de argumentos → draft (com âncoras quote/page/section) →
abstract PT-BR/EN → figuras (VLM). 🧑 Humano aprova o esqueleto antes da redação.

## Gate 2.5 — Integridade (não-pulável)
`auditor-de-integridade` emite `relatorio-integridade.example.json`:
M2 fica **SUSPEITO** (a citação `nao-resolvida` e a `inexistente`) → `veredito: FALHOU`.
→ `guarda-de-auto-cura` corrige (remove a fabricada, etiqueta a regional) e
re-submete. Após PASSAR, 🧑 dá o *ack*.

## Estágio 3 — Parecer (G3)
`ContratoDeParecer` fechado em **fase cega** (`contrato-de-parecer.example.json`),
5 pareceres pontuados, `sintetizador-editorial` aplica o protocolo de 3 passos →
decisão **Revisão-Maior**. 🧑 Humano revê.

## Estágios 4 / 3' / 4' — Revisão com cap de loop
`treinador-de-revisao` conduz resposta ponto-a-ponto; re-parecer gera
`matriz-de-rastreabilidade.example.json` (cada alegação do autor verificada).
Cap rígido: 1 re-revisão. Conteúdo congelado em 4'.

## Gate 4.5 — Integridade final (tolerância zero)
Re-execução profunda dos 7 modos + verificação de alegações **100%**. Todos os
SUSPEITOS de 2.5 estão **RESOLVIDOS**. `PassaporteDossie.status_verificacao = VERIFICADO`.

## Estágio 5 — Finalizar
Exporta Markdown/DOCX/PDF + Declaração de Uso de IA. O *gate* terminal confirma:
nenhuma alegação não-sustentada pendente.

## Estágio 6 — Dossiê-Processo
`passaporte-dossie.example.json` consolidado; auto-reflexão (taxa de concessão,
trajetória de pontuação) e capítulo de Profundidade de Colaboração. A execução é
retomável por `MAESTRO *resume scr-7f3a91c2`.

---
Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
