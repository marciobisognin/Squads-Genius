# PROJUR Contracts Squad

Camada de **inteligência documental em lote** e **ciclo de vida (CLM)** para contratos,
convênios, acordos de cooperação, termos de fomento/colaboração e termos de execução
descentralizada (TED) do **Instituto Federal Farroupilha (IFFar)**.

O squad transforma um **lote** de instrumentos (PDF nativo, PDF escaneado, DOCX, MD) em uma
**matriz consolidada, governada e auditável**, com extração fiel, classificação, normalização
de partes (CNPJ/CPF), detecção/mascaramento de PII (LGPD), vínculo entre instrumentos,
alertas de vigência, conformidade por engine de regras, indicadores e relatório executivo.

> **Posicionamento:** o PROJUR **não emite parecer de mérito** — ele processa o acervo em
> escala e **encaminha** casos para os squads especializados:
> - `themis-contratos-publicos-squad` → parecer técnico-jurídico;
> - `farol-contratos-licitacoes-iffar` → planejamento/contratação (DFD/ETP/TR/preços);
> - `squad-pcfp` → planilha de custos e formação de preços (mão de obra).

## Disclaimer

Apoio técnico automatizado. **Não substitui** parecer da Procuradoria competente
(art. 53 da Lei 14.133/2021). Os dispositivos legais são **referenciais** e exigem
verificação de vigência. **Toda saída exige revisão humana qualificada.**

## Princípios

- Separar observado, inferido, hipótese, recomendação e risco.
- **Nenhum valor numérico ou de conformidade gerado por LLM** — o cálculo vem dos scripts.
- Todo apontamento jurídico cita norma e indica vigência.
- **LGPD by design**: detectar e mascarar PII; minimização e trilha de auditoria.
- Schema-first; reprodutibilidade por checksum; **humano no loop** obrigatório.

## Estrutura

```
agents/     22 agentes (núcleo de pipeline + council de 6 SMEs jurídicos + governança)
tasks/      13 tarefas
workflows/  4 fluxos (lote_completo, triagem_rapida_red_flags, atualizacao_incremental, monitor_vigencia)
scripts/    22 scripts determinísticos (Python 3.11+, stdlib)
schemas/    11 schemas JSON
templates/  regras.yaml (base de regras versionada)
docs/       base normativa e evidência do forge
tests/      pytest
examples/   lote de exemplo + gold set
```

## Council de SMEs jurídicos

- `sme-lei14133-conformidade` — Lei 14.133/2021 (e legado 8.666/93).
- `sme-convenios-ted-transferencias` — convênios, TED, fomento/colaboração, fundações de apoio.
- `sme-pdi-propriedade-intelectual` — Marco Legal de CT&I (PI, sigilo).
- `sme-lgpd-privacidade` — LGPD.
- `sme-licitacao-enquadramento` — modalidade, dispensa/inexigibilidade.
- `sme-jurisprudencia-controle` — TCU/TCE/CGU (handoff para Themis).

## Uso

Veja [`examples/exemplo_uso.md`](examples/exemplo_uso.md) para o pipeline completo. Resumo:

```bash
python scripts/ingest.py --input ./examples/lote --output ./saida
python scripts/extract_text.py --manifest ./saida/manifest.json --output ./saida
python scripts/classify_instrument.py --in ./saida/evidencias/textos --output ./saida
# ... (demais etapas no exemplo_uso.md)
```

Testes:

```bash
python -m pytest tests/ -q
```

## PRD

O detalhamento completo (análise crítica, agentes, scripts, schemas, regras, métricas e
roadmap) está em [`PRD.md`](PRD.md).

---

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
