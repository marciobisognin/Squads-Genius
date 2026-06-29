#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const args = process.argv.slice(2);
let root = process.cwd();
if (args.includes('--path')) root = path.resolve(args[args.indexOf('--path')+1]);
if (args.includes('--squad')) root = path.resolve(args[args.indexOf('--squad')+1]);
const required = [
  'squad.yaml','README.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json',
  'TEXTO_EXPLICATIVO_SQUAD.md','TEXTO_PUBLICACAO_REDES_BLOG.md',
  'agents/diretor-nexo.md','agents/minerador-neurocognitivo.md','agents/arquiteto-estimulo-sustentado.md',
  'agents/designer-recuperacao-ativa.md','agents/tradutor-pratico.md','agents/analista-metricas.md','agents/guardiao-etico-cientifico.md',
  'tasks/01-intake-meta-aprendizagem.md','tasks/02-minerar-principios.md','tasks/03-desenhar-microsprint.md','tasks/04-gerar-plano-e-metricas.md','tasks/05-validar-seguranca-e-entrega.md',
  'workflows/nexum-cognitivo-main.yaml','scripts/smoke-test.cjs','scripts/nexum-cognitivo.cjs',
  'templates/intake-aprendizagem.yaml','templates/protocolo-diario.md','templates/plano-metricas.json','references/source-analysis.md'
];
const missing = required.filter(f => !fs.existsSync(path.join(root, f)));
const readme = fs.existsSync(path.join(root,'README.md')) ? fs.readFileSync(path.join(root,'README.md'),'utf8') : '';
const sections = ['Para quem é','Objetivo','O que tem dentro','Exemplos de uso','Limites éticos','Nome escolhido'];
const missingSections = sections.filter(s => !readme.toLowerCase().includes(s.toLowerCase()));
const agents = required.filter(f => f.startsWith('agents/'));
const agentIssues = [];
for (const a of agents) {
  if (!fs.existsSync(path.join(root,a))) continue;
  const txt = fs.readFileSync(path.join(root,a),'utf8');
  if (!txt.includes('*help') || !txt.includes('*exit')) agentIssues.push(a+': comandos universais ausentes');
}
const safetyPhrases = ['não clínico','não diagnostica','não promete'];
const safetyIssues = safetyPhrases.filter(s => !readme.toLowerCase().includes(s));
const issues = [...missing, ...missingSections.map(s=>'README sem seção: '+s), ...agentIssues, ...safetyIssues.map(s=>'README sem limite: '+s)];
const score = Math.max(0, 100 - missing.length*4 - missingSections.length*3 - agentIssues.length*4 - safetyIssues.length*5);
const report = path.join(root,'validation','premium-architect-report.md');
fs.mkdirSync(path.dirname(report), {recursive:true});
fs.writeFileSync(report, `# Premium Architect Report — Nexum Cognitivo\n\n- Score: ${score}\n- Status: ${issues.length ? 'revisar' : 'aprovado'}\n- Arquivos obrigatórios verificados: ${required.length}\n- Issues: ${issues.length ? issues.join('; ') : 'nenhuma'}\n\n`);
const ok = score >= 90 && issues.length === 0;
console.log(JSON.stringify({ok,before_score:score,after_score:score,report,issues}, null, 2));
if(!ok) process.exit(2);
