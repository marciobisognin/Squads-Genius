#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const root = process.cwd();
const required = [
  'squad.yaml','README.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json',
  'workflows/incubacao-premium.yaml','config/base-metodologica.md',
  'scripts/demo-generate-report.cjs',
  'templates/diagnostico-cerne.md','templates/business-model-canvas.md','templates/value-proposition-canvas.md',
  'templates/cartao-experimento.md','templates/roteiro-entrevista-cliente.md','templates/avaliacao-trl.md',
  'templates/plano-desenvolvimento-empreendimento.md','templates/painel-indicadores.md','templates/edital-selecao.md',
  'templates/matriz-avaliacao.md','templates/relatorio-periodico.md','templates/checklist-graduacao.md'
];
const agents = ['diagnostico-cerne','modelagem-negocios','validacao-mercado','maturidade-tecnologica','mentoria-jornada','indicadores-impacto','ecossistema-parcerias','captacao-pitch'];
for (const a of agents) required.push(`agents/${a}.md`);
const tasks = ['01-diagnostico-institucional.md','02-modelagem-e-validacao.md','03-maturidade-tecnologica.md','04-mentoria-indicadores-impacto.md','05-ecossistema-captacao-entrega.md'];
for (const t of tasks) required.push(`tasks/${t}`);
const missing = required.filter(p => !fs.existsSync(path.join(root,p)));
if (missing.length) { console.error('Missing files:\n' + missing.join('\n')); process.exit(1); }
for (const a of agents) {
  const txt = fs.readFileSync(path.join(root,`agents/${a}.md`),'utf8');
  if (!txt.includes('*help') || !txt.includes('*exit')) { console.error(`Agent ${a} lacks universal commands`); process.exit(2); }
  if (!txt.includes('Licença: MIT')) { console.error(`Agent ${a} lacks license footer`); process.exit(3); }
}
const workflow = fs.readFileSync(path.join(root,'workflows/incubacao-premium.yaml'),'utf8');
for (const a of agents) if (!workflow.includes(a)) { console.error(`Workflow missing agent ${a}`); process.exit(4); }
const readme = fs.readFileSync(path.join(root,'README.md'),'utf8');
for (const term of ['Órbita Incubadora Squad','CERNE','Lean Startup','TRL','O que o squad entrega no final','mermaid']) {
  if (!readme.includes(term)) { console.error(`README missing term: ${term}`); process.exit(5); }
}
console.log(JSON.stringify({ok:true, files: required.length, agents: agents.length, tasks: tasks.length}, null, 2));
