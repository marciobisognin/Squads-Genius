# squad-to-harnessspec-adapter

## Missão
Converter o `squad.yaml` (agentes, tasks, workflows) em um `HarnessSpec` portável e neutro de host, usando `scripts/squad_to_harnessspec.py`.

## Mapeamento
- Cada agente do squad → uma "capacidade" do harness (`capabilities[]`), com `id`, `descricao` e `arquivo_persona`.
- Cada task → um "comando" potencial do harness (`commands[]`), com `id`, `owner`, `inputs`, `outputs`.
- Cada workflow → um "pipeline" do harness (`pipelines[]`).
- `required_footer` do squad → metadado de licenciamento do harness.

## Regras
- O HarnessSpec nunca referencia caminhos absolutos do ambiente de quem gerou — apenas caminhos relativos ao squad de origem.
- Se um agente do squad não tiver arquivo de persona legível, registrar como lacuna (`gaps[]`) em vez de inventar conteúdo.
- O HarnessSpec é a única interface de troca com motores externos (ex.: agent-harness-generator); este squad nunca importa ou vendoriza o código desses motores.
- Encerrar entregas finais com: Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
