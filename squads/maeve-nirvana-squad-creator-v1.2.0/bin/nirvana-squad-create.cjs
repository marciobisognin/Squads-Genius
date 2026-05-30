#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const VERSION = '1.4.1';
const DEFAULT_PROFILE = 'marcio';

const README_DESIGN_PRESETS = {
  'parchment-goal-flow': {
    id: 'parchment-goal-flow',
    label: 'Estilo 1 — Pergaminho / Goal Flow',
    bestFor: 'squads pedagógicos, aprendizado, investigação, leitura, pesquisa, diagnóstico e exploração conceitual',
    visual: 'mapa narrativo em pergaminho, sketchbook, fluxo de missão, blocos orgânicos e setas de descoberta',
    flow: ['chamado inicial', 'contexto', 'investigação', 'hipóteses', 'construção guiada', 'validação', 'entrega'],
    sections: ['Mapa da missão', 'Fluxo explicativo', 'Agentes como guias', 'Trilha de aprendizado/investigação', 'Entregáveis finais']
  },
  'dark-neon-layered-architecture': {
    id: 'dark-neon-layered-architecture',
    label: 'Estilo 2 — Dark Neon / Layered Architecture',
    bestFor: 'squads de negócios, operação, produto, automação, tecnologia, vendas, marketing, governança e arquitetura de agentes',
    visual: 'dashboard dark mode com cards neon, camadas hierárquicas, containers isolados, fluxo top-down/bottom-up e linguagem de sistema operacional',
    flow: ['squad brain', 'orquestrador', 'department/agent brains', 'agentes especializados', 'contexto desce', 'trabalho sobe', 'memória escopada'],
    sections: ['Arquitetura em camadas', 'Squad Brain', 'Maeve Orchestrator', 'Agent Brains', 'Specialized Agents', 'How it flows', 'Entregáveis finais']
  }
};

function detectReadmeStyle(cfg){
  const explicit=String(cfg.readmeStyle || 'auto').toLowerCase();
  if(explicit !== 'auto'){
    if(!README_DESIGN_PRESETS[explicit]) throw new Error('--readme-style inválido: '+explicit);
    return explicit;
  }
  const text=`${cfg.name} ${cfg.objective} ${cfg.description}`.toLowerCase();
  const style1=/pedag[oó]g|educa|aprendiz|alfabet|leitura|aula|ensino|investiga|pesquisa|estudo|diagn[oó]stico|ci[eê]ncia|hist[oó]ria|geografia|neuro|conhecimento|mapa mental|literatura/.test(text);
  const style2=/neg[oó]cio|business|venda|sales|marketing|produto|startup|opera[cç][aã]o|gest[aã]o|processo|governan[cç]a|autom[aá]tica|automacao|automação|sistema|tech|financeiro|contrato|fiscaliza|dashboard|deploy|monitor|arquitetura/.test(text);
  if(style2 && !style1) return 'dark-neon-layered-architecture';
  if(style1 && !style2) return 'parchment-goal-flow';
  return 'parchment-goal-flow';
}

function readmeDesignBlock(styleId){
  const p=README_DESIGN_PRESETS[styleId];
  return `## Estilo visual do README\n\n**Preset aplicado:** ${p.label}.\n\n**Quando usar:** ${p.bestFor}.\n\n**Linguagem visual:** ${p.visual}.\n\n**Fluxo explicativo:**\n${p.flow.map((x,i)=>`${i+1}. ${x}`).join('\n')}\n\n**Blocos recomendados:** ${p.sections.join(' → ')}.\n`;
}

function buildPremiumReadme(cfg){
  const title=titleize(cfg.name);
  const styleId=detectReadmeStyle(cfg);
  const preset=README_DESIGN_PRESETS[styleId];
  const styleNote = styleId === 'dark-neon-layered-architecture'
    ? `Este README deve organizar o squad como uma arquitetura em camadas: cérebro do squad, orquestrador Maeve, cérebros/agentes especializados, fluxo de contexto, fluxo de trabalho, memória escopada e entregáveis finais.`
    : `Este README deve organizar o squad como uma jornada investigativa: mapa da missão, pergunta central, trilha de descoberta, agentes como guias, hipóteses, validação e síntese final.`;
  return `# ${title}\n\n${cfg.description || cfg.objective}\n\n## Para quem é\nUsuários que precisam executar o objetivo: ${cfg.objective}.\n\n## Objetivo\nTransformar uma demanda em processo de squad com análise, produção, validação e publicação.\n\n${readmeDesignBlock(styleId)}\n## Diretriz de construção visual\n${styleNote}\n\n## O que tem dentro\n- 4 agentes operacionais\n- 4 tasks com contrato Entrada/Saída\n- 1 workflow sequencial\n- config, checklist, templates, referências, scripts e arquivos de IP/licença\n- smoke test local em \`scripts/smoke-test.cjs\`\n\n## Estrutura dos agentes\n- **Orchestrator:** coordena o fluxo completo e integra os resultados.\n- **Researcher:** investiga contexto, requisitos, referências e riscos.\n- **Builder:** constrói os artefatos principais do domínio.\n- **Validator:** valida completude, consistência, qualidade e prontidão de publicação.\n\n## O que o squad entrega no final\n- análise estruturada da demanda;\n- artefatos principais do domínio;\n- validação operacional;\n- pacote documentado e pronto para uso/publicação.\n\n## Exemplos de uso\n\`/SQUADS:${cfg.name.slice(0,3)}:orchestrator\` — inicia o fluxo completo.\n\n${cfg.footer}\n`;
}


function ensure(p){ fs.mkdirSync(p,{recursive:true}); }
function write(p,c){ ensure(path.dirname(p)); fs.writeFileSync(p,c,'utf8'); }
function exists(p){ return fs.existsSync(p); }
function slugify(s){ return String(s||'novo-squad').trim().toLowerCase().replace(/[^a-z0-9-]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'') || 'novo-squad'; }
function titleize(slug){ return slug.split('-').filter(Boolean).map(w=>w[0].toUpperCase()+w.slice(1)).join(' '); }
function quoteYaml(s){ return JSON.stringify(String(s||'')); }

function parseArgs(argv){
  const opts={ _:[] };
  for(let i=0;i<argv.length;i++){
    const a=argv[i];
    if(a==='-h' || a==='--help'){ opts.help=true; continue; }
    if(a.startsWith('--')){
      const eq=a.indexOf('=');
      if(eq>=0){ opts[a.slice(2,eq)] = a.slice(eq+1); }
      else {
        const key=a.slice(2);
        if(i+1<argv.length && !argv[i+1].startsWith('--')) opts[key]=argv[++i];
        else opts[key]=true;
      }
    } else opts._.push(a);
  }
  return opts;
}

function usage(){
  console.log(`Nirvana Squad Create v${VERSION}\n\nUso:\n  nirvana-squad-create <nome> [opções]\n\nOpções principais:\n  --mode=scaffold|full          scaffold mínimo ou squad completo validável (default: scaffold)\n  --target=aios|maeve           alvo de runtime/convenções (default: aios)\n  --profile=marcio|generic      autoria e IP padrão (default: marcio)\n  --output=<dir>                diretório de saída; também aceita --output <dir>\n  --objective=<texto>           objetivo do squad\n  --description=<texto>         descrição longa\n  --release                     exige manifesto não vazio e validação bloqueante\n  --smoke-test                  roda smoke test automático depois de gerar\n  --premium-gate                passa pelo Architect Gate premium (default no modo full)\n  --no-premium-gate             desativa o Architect Gate premium\n  --readme-style=auto|parchment-goal-flow|dark-neon-layered-architecture\n                               seleciona o estilo visual do README; auto escolhe por domínio\n  --force                       sobrescreve destino existente\n  -h, --help                    mostra esta ajuda sem criar arquivos\n\nExemplos:\n  nirvana-squad-create meu-squad --mode=full --target=maeve --profile=marcio --output ~/squad-factory/workspaces --objective='Criar ativos com IA' --release --smoke-test\n  nirvana-squad-create meu-squad --output ~/tmp\n`);
}

function removeDirSafe(p){
  if(!exists(p)) return;
  const base=path.basename(p);
  if(!base || base==='/' || base==='.' || p.length < 10) throw new Error('recusa apagar destino inseguro: '+p);
  fs.rmSync(p,{recursive:true,force:true});
}

function licenseText(year, holder){ return `MIT License\n\nCopyright (c) ${year} ${holder}\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n`; }

function authorFor(profile){
  if(profile==='marcio') return {creator:'Marcio Bisognin', instagram:'@marciobisognin', license:'MIT'};
  return {creator:'Author', instagram:'', license:'MIT'};
}

function addIpFiles(root, meta){
  const year=new Date().getFullYear();
  write(path.join(root,'LICENSE'), licenseText(year, meta.creator));
  write(path.join(root,'AUTHORS.md'), `# Autores\n\n- ${meta.creator}${meta.instagram ? ` (${meta.instagram})` : ''}\n`);
  write(path.join(root,'NOTICE.md'), `# NOTICE\n\nLicença: ${meta.license}.\nCriado por ${meta.creator}.${meta.instagram ? `\nInstagram: ${meta.instagram}.` : ''}\n`);
  write(path.join(root,'.ip','ownership.json'), JSON.stringify({
    creator: meta.creator,
    instagram: meta.instagram,
    license: meta.license,
    generated_by: 'nirvana-squad-create',
    generator_version: VERSION,
    attribution_footer: meta.instagram ? `Licença: ${meta.license}. Criado por ${meta.creator}. Instagram: ${meta.instagram}.` : `Licença: ${meta.license}. Criado por ${meta.creator}.`
  },null,2)+'\n');
  write(path.join(root,'.ip','response-footer.md'), `${meta.instagram ? `Licença: ${meta.license}. Criado por ${meta.creator}. Instagram: ${meta.instagram}.` : `Licença: ${meta.license}. Criado por ${meta.creator}.`}\n`);
}

function writeCommonDirs(root){
  ['agents','tasks','workflows','config','checklists','templates','references','scripts','.ip','examples','validation'].forEach(d=>ensure(path.join(root,d)));
}

function writeScaffold(root, cfg){
  writeCommonDirs(root);
  const title=titleize(cfg.name);
  const styleId=detectReadmeStyle(cfg);
  write(path.join(root,'README.md'), `# ${title}\n\nObjetivo: ${cfg.objective}\n\n${readmeDesignBlock(styleId)}\n> Scaffold gerado pelo Nirvana Squad Creator v${VERSION}. Use --mode=full para gerar um squad com agentes, tasks, workflows, README visual e validação inicial.\n`);
  write(path.join(root,'squad.yaml'), `name: ${cfg.name}\nversion: 0.1.0\ndescription: ${quoteYaml(cfg.description || cfg.objective || 'Squad scaffold')}\nslashPrefix: ${cfg.name.slice(0,3)}\nauthor: ${quoteYaml(cfg.meta.creator)}\nlicense: ${cfg.meta.license}\naios:\n  minVersion: "2.1.0"\n  type: squad\ncomponents:\n  agents: []\n  tasks: []\n  workflows: []\n  checklists: []\n  templates: []\n  tools: []\n  scripts: []\nmetadata:\n  target: ${cfg.target}\n  profile: ${cfg.profile}\n`);
  addIpFiles(root,cfg.meta);
}

function agentContent(id, title, purpose, command, cfg){
  return `---\nid: ${id}\nname: ${title}\narchetype: Builder\ndescription: ${quoteYaml(purpose)}\nversion: 0.1.0\n---\n\n# ${title}\n\n## Missão\n${purpose}\n\n## Comandos\n\n- name: "${command}"\n  visibility: squad\n  description: "Executa a responsabilidade principal deste agente"\n- name: "*help"\n  visibility: squad\n  description: "Lista comandos disponíveis e orienta como usar este agente"\n- name: "*exit"\n  visibility: squad\n  description: "Encerra a interação atual com este agente e devolve o controle ao fluxo principal"\n\n## Regra de autoria\nToda resposta final deve preservar o rodapé: ${cfg.footer}\n`;
}
function taskContent(id, title, agent, output){
  return `---\nid: ${id}\nname: ${title}\nagent: ${agent}\natomic_layer: organism\n---\n\n# ${title}\n\n## Entrada\n- Objetivo do usuário\n- Contexto disponível\n\n## Processo\n1. Interpretar a demanda.\n2. Produzir artefato verificável.\n3. Registrar decisões e pendências.\n\n## Saída\n- ${output}\n\n## Checklist\n- [ ] Entrada compreendida\n- [ ] Artefato gerado\n- [ ] Validação básica executada\n`;
}

function writeFull(root, cfg){
  writeCommonDirs(root);
  addIpFiles(root,cfg.meta);
  const title=titleize(cfg.name);
  const footer=cfg.footer;
  cfg.readmeStyle = detectReadmeStyle(cfg);
  write(path.join(root,'README.md'), buildPremiumReadme(cfg));
  const agents=[
    ['orchestrator','Orchestrator','Coordena o fluxo completo do squad.','*run'],
    ['researcher','Researcher','Analisa requisitos, contexto e referências.','*research'],
    ['builder','Builder','Constrói os artefatos principais do domínio.','*build'],
    ['validator','Validator','Valida completude, consistência e prontidão de publicação.','*validate'],
  ];
  for(const [id,t,p,c] of agents) write(path.join(root,'agents',`${id}.md`), agentContent(id,t,p,c,{...cfg,footer}));
  const tasks=[
    ['analyze-requirements','Analyze Requirements','researcher','requirements-analysis.md'],
    ['build-artifacts','Build Artifacts','builder','artifact-pack.md'],
    ['validate-release','Validate Release','validator','validation-report.md'],
    ['publish-package','Publish Package','orchestrator','publish-report.md'],
  ];
  for(const [id,t,a,o] of tasks) write(path.join(root,'tasks',`${id}.md`), taskContent(id,t,a,o));
  write(path.join(root,'workflows','main.yaml'), `id: main\nname: Main Workflow\ndescription: ${quoteYaml('Fluxo principal do squad')}\nsteps:\n  - id: analyze\n    agent: researcher\n    task: analyze-requirements\n    produces: requirements-analysis.md\n  - id: build\n    agent: builder\n    task: build-artifacts\n    requires: analyze\n    produces: artifact-pack.md\n  - id: validate\n    agent: validator\n    task: validate-release\n    requires: build\n    produces: validation-report.md\n  - id: publish\n    agent: orchestrator\n    task: publish-package\n    requires: validate\n    produces: publish-report.md\n`);
  write(path.join(root,'config','tech-stack.md'), `# Tech Stack\n\n- AIOS/Squad runtime\n- Markdown/YAML\n- Node.js para validação local\n`);
  write(path.join(root,'config','source-tree.md'), `# Source Tree\n\n- agents/ — agentes\n- tasks/ — tarefas\n- workflows/ — fluxos\n- scripts/ — automações locais\n- .ip/ — autoria e licença\n`);
  write(path.join(root,'config','coding-standards.md'), `# Coding Standards\n\n- Slugs em kebab-case.\n- Artefatos em Markdown/YAML.\n- Manter rodapé de autoria nos entregáveis finais.\n- README deve seguir o preset visual selecionado: ${cfg.readmeStyle}.\n`);
  write(path.join(root,'references','readme-design-system.md'), `# README Design System\n\n## Preset selecionado\n\n${README_DESIGN_PRESETS[cfg.readmeStyle].label}\n\n## Regra de seleção automática\n\n- Use **parchment-goal-flow** para squads pedagógicos, aprendizado, investigação, leitura, pesquisa e exploração conceitual.\n- Use **dark-neon-layered-architecture** para squads de negócios, produto, operação, automação, governança, marketing, vendas e arquitetura técnica.\n\n## Presets disponíveis\n\n${Object.values(README_DESIGN_PRESETS).map(p=>`### ${p.label}\n- ID: ${p.id}\n- Melhor para: ${p.bestFor}\n- Visual: ${p.visual}\n- Fluxo: ${p.flow.join(' → ')}\n`).join('\n')}\n`);
  write(path.join(root,'checklists','release-checklist.md'), `# Release Checklist\n\n- [ ] squad.yaml lista componentes reais\n- [ ] agentes possuem *help e *exit\n- [ ] tasks possuem entrada, processo, saída e checklist\n- [ ] workflow referencia agentes e tasks existentes\n- [ ] LICENSE, NOTICE.md, AUTHORS.md e .ip/ existem\n- [ ] scripts/smoke-test.cjs passa\n`);
  write(path.join(root,'templates','artifact.template.md'), `# {{title}}\n\n## Contexto\n{{context}}\n\n## Resultado\n{{result}}\n\n${footer}\n`);
  write(path.join(root,'references','operating-pattern.md'), `# Padrão Operacional\n\nEste squad usa pipeline sequencial: análise → construção → validação → publicação.\n`);
  write(path.join(root,'examples','demo-request.md'), `Crie um entregável usando o squad ${cfg.name} para: ${cfg.objective}\n`);
  write(path.join(root,'squad.yaml'), `name: ${cfg.name}\nversion: 0.1.0\ndescription: ${quoteYaml(cfg.description || cfg.objective)}\nslashPrefix: ${cfg.name.slice(0,3)}\nauthor: ${quoteYaml(cfg.meta.creator)}\nlicense: ${cfg.meta.license}\naios:\n  minVersion: "2.1.0"\n  type: squad\ncomponents:\n  agents:\n    - orchestrator.md\n    - researcher.md\n    - builder.md\n    - validator.md\n  tasks:\n    - analyze-requirements.md\n    - build-artifacts.md\n    - validate-release.md\n    - publish-package.md\n  workflows:\n    - main.yaml\n  checklists:\n    - release-checklist.md\n  templates:\n    - artifact.template.md\n  references:\n    - readme-design-system.md\n    - operating-pattern.md\n  tools: []\n  scripts:\n    - smoke-test.cjs\n    - premium-architect-gate.cjs\nconfig:\n  coding-standards: config/coding-standards.md\n  tech-stack: config/tech-stack.md\n  source-tree: config/source-tree.md\nmetadata:\n  target: ${cfg.target}\n  profile: ${cfg.profile}\n  generated_by: nirvana-squad-create@${VERSION}\n  readme_style: ${quoteYaml(cfg.readmeStyle)}\n  response_footer: ${quoteYaml(footer)}\n`);
  write(path.join(root,'scripts','smoke-test.cjs'), `#!/usr/bin/env node\nconst fs=require('fs'); const path=require('path');\nconst root=path.resolve(__dirname,'..');\nconst required=['squad.yaml','README.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json','agents/orchestrator.md','agents/researcher.md','agents/builder.md','agents/validator.md','tasks/analyze-requirements.md','tasks/build-artifacts.md','tasks/validate-release.md','tasks/publish-package.md','workflows/main.yaml','checklists/release-checklist.md'];\nconst missing=required.filter(f=>!fs.existsSync(path.join(root,f)));\nif(missing.length){ console.error(JSON.stringify({ok:false,missing},null,2)); process.exit(1);}\nconst yaml=fs.readFileSync(path.join(root,'squad.yaml'),'utf8');\nfor(const section of ['agents','tasks','workflows','scripts']){ if(!new RegExp(section+':\\\\n\\\\s+-').test(yaml)){ console.error(JSON.stringify({ok:false,error:'manifesto vazio: '+section},null,2)); process.exit(1);} }\nconsole.log(JSON.stringify({ok:true,checked:required.length},null,2));\n`);
  write(path.join(root,'scripts','premium-architect-gate.cjs'), `#!/usr/bin/env node
const fs=require('fs'),path=require('path');
const root=path.resolve(process.argv.includes('--squad')?process.argv[process.argv.indexOf('--squad')+1]:process.cwd());
const required=['squad.yaml','README.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json','agents/orchestrator.md','tasks/analyze-requirements.md','workflows/main.yaml','scripts/smoke-test.cjs'];
const missing=required.filter(f=>!fs.existsSync(path.join(root,f)));
const readme=fs.existsSync(path.join(root,'README.md'))?fs.readFileSync(path.join(root,'README.md'),'utf8'):'';
const sections=['Para quem é','Objetivo','O que tem dentro','Exemplos de uso'];
const missingSections=sections.filter(s=>!readme.toLowerCase().includes(s.toLowerCase()));
const score=Math.max(0,100-(missing.length*8)-(missingSections.length*5));
const report=path.join(root,'validation','premium-architect-report.md'); fs.mkdirSync(path.dirname(report),{recursive:true});
fs.writeFileSync(report,'# Premium Architect Report\n\n- Score: '+score+'\n- Missing: '+missing.join(', ')+'\n- Missing sections: '+missingSections.join(', ')+'\n');
const ok=score>=90 && !missing.length && !missingSections.length;
console.log(JSON.stringify({ok,before_score:score,after_score:score,report,issues:[...missing,...missingSections]},null,2));
if(!ok) process.exit(2);
`);
  fs.chmodSync(path.join(root,'scripts','premium-architect-gate.cjs'),0o755);
}

function validateRelease(root, mode){
  const errors=[];
  const yamlPath=path.join(root,'squad.yaml');
  if(!exists(yamlPath)) errors.push('squad.yaml ausente');
  const yaml=exists(yamlPath)?fs.readFileSync(yamlPath,'utf8'):'';
  if(mode==='full'){
    for(const section of ['agents','tasks','workflows','scripts']) if(!new RegExp(section+':\\n\\s+-').test(yaml)) errors.push(`manifesto sem itens em components.${section}`);
  }
  for(const f of ['LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json','.ip/response-footer.md']) if(!exists(path.join(root,f))) errors.push(`${f} ausente`);
  if(errors.length){ return {ok:false, errors}; }
  return {ok:true, errors:[]};
}

function runSmoke(root){
  const script=path.join(root,'scripts','smoke-test.cjs');
  if(!exists(script)) return {ok:true, skipped:true, reason:'sem smoke-test.cjs'};
  const res=spawnSync(process.execPath,[script],{cwd:root,encoding:'utf8'});
  return {ok:res.status===0, status:res.status, stdout:res.stdout.trim(), stderr:res.stderr.trim()};
}


function runPremiumGate(root, opts){
  const localGate = path.resolve(__dirname, '..', 'scripts', 'premium-architect-gate.cjs');
  const fallbackGate = path.join(process.env.HOME || '', 'squad-factory/workspaces/maeve-nirvana-squad-creator-v1.2.0/scripts/premium-architect-gate.cjs');
  const gate = exists(localGate) ? localGate : fallbackGate;
  if(!exists(gate)) return {ok:false, skipped:false, error:'premium-architect-gate.cjs não encontrado'};
  const args=[gate,'--squad',root,'--min-score=90'];
  if(opts.rebuild !== false) args.push('--rebuild');
  const res=spawnSync(process.execPath,args,{cwd:root,encoding:'utf8'});
  let parsed=null;
  try{ parsed=JSON.parse((res.stdout||'').trim()); }catch{}
  return {ok:res.status===0, status:res.status, result:parsed, stdout:(res.stdout||'').trim(), stderr:(res.stderr||'').trim()};
}

function writeReport(root, cfg, validation, smoke, premium){
  const lines=[];
  lines.push(`# Relatório de geração — ${cfg.name}`,'');
  lines.push(`- Gerado em: ${new Date().toISOString()}`);
  lines.push(`- Modo: ${cfg.mode}`);
  lines.push(`- Target: ${cfg.target}`);
  lines.push(`- Profile: ${cfg.profile}`);
  lines.push(`- Release validation: ${validation.ok ? 'PASS' : 'FAIL'}`);
  lines.push(`- Smoke test: ${smoke.skipped ? 'SKIPPED' : (smoke.ok ? 'PASS' : 'FAIL')}`);
  if(premium) lines.push(`- Premium Architect Gate: ${premium.ok ? 'PASS' : 'FAIL'}${premium.result ? ` (${premium.result.after_score}/100)` : ''}`);
  lines.push(`- Diretório: ${root}`,'');
  if(validation.errors && validation.errors.length){ lines.push('## Erros de validação'); validation.errors.forEach(e=>lines.push(`- ${e}`)); }
  if(smoke.stdout){ lines.push('## Smoke stdout','```json',smoke.stdout,'```'); }
  if(smoke.stderr){ lines.push('## Smoke stderr','```',smoke.stderr,'```'); }
  if(premium && premium.stdout){ lines.push('## Premium Architect Gate stdout','```json',premium.stdout,'```'); }
  if(premium && premium.stderr){ lines.push('## Premium Architect Gate stderr','```',premium.stderr,'```'); }
  write(path.join(root,'validation','generation-report.md'), lines.join('\n')+'\n');
}

function main(){
  const opts=parseArgs(process.argv.slice(2));
  if(opts.help){ usage(); return; }
  const name=slugify(opts._[0] || opts.name || 'novo-squad');
  const mode=String(opts.mode || 'scaffold').toLowerCase();
  if(!['scaffold','full'].includes(mode)) throw new Error('--mode deve ser scaffold ou full');
  const target=String(opts.target || 'aios').toLowerCase();
  if(!['aios','maeve'].includes(target)) throw new Error('--target deve ser aios ou maeve');
  const profile=String(opts.profile || DEFAULT_PROFILE).toLowerCase();
  const meta=authorFor(profile);
  const footer=meta.instagram ? `Licença: ${meta.license}. Criado por ${meta.creator}. Instagram: ${meta.instagram}.` : `Licença: ${meta.license}. Criado por ${meta.creator}.`;
  const out=path.resolve(String(opts.output || process.cwd()).replace(/^~/, process.env.HOME || '~'));
  const objective=String(opts.objective || 'Definir objetivo');
  const description=String(opts.description || objective);
  const readmeStyle=String(opts['readme-style'] || 'auto').toLowerCase();
  const root=path.join(out,name);
  if(exists(root)){
    if(opts.force) removeDirSafe(root);
    else throw new Error('Destino já existe: '+root+' (use --force para sobrescrever)');
  }
  const cfg={name,mode,target,profile,meta,footer,objective,description,readmeStyle};
  if(mode==='full') writeFull(root,cfg); else writeScaffold(root,cfg);
  const validation=validateRelease(root,mode);
  if(opts.release && !validation.ok){ writeReport(root,cfg,validation,{skipped:true}); throw new Error('validação release falhou: '+validation.errors.join('; ')); }
  let smoke={skipped:true};
  let premium=null;
  const premiumEnabled = mode==='full' && opts['no-premium-gate'] !== true;
  if(premiumEnabled) premium=runPremiumGate(root,{rebuild:true});
  if(opts['smoke-test']) smoke=runSmoke(root);
  writeReport(root,cfg,validation,smoke,premium);
  if(premiumEnabled && !premium.ok) throw new Error('premium architect gate falhou: '+(premium.stderr||premium.stdout||premium.error));
  if(opts['smoke-test'] && !smoke.ok) throw new Error('smoke test falhou: '+(smoke.stderr||smoke.stdout));
  console.log(JSON.stringify({ok:true,created:root,mode,target,profile,release_validation:validation,smoke,premium_gate:premium},null,2));
}
try{ main(); }catch(e){ console.error(JSON.stringify({ok:false,error:String(e.message||e)},null,2)); process.exit(1); }
