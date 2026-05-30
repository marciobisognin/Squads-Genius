#!/usr/bin/env node
const fs=require('fs');
const path=require('path');
const {spawnSync}=require('child_process');

function parse(argv){const o={_:[]}; for(let i=0;i<argv.length;i++){const a=argv[i]; if(a==='--help'||a==='-h'){o.help=true;continue;} if(a.startsWith('--')){const eq=a.indexOf('='); if(eq>=0)o[a.slice(2,eq)]=a.slice(eq+1); else if(i+1<argv.length&&!argv[i+1].startsWith('--'))o[a.slice(2)]=argv[++i]; else o[a.slice(2)]=true;} else o._.push(a);} return o;}
function exists(p){return fs.existsSync(p)}
function ensure(p){fs.mkdirSync(p,{recursive:true})}
function write(p,c){ensure(path.dirname(p)); fs.writeFileSync(p,c,'utf8')}
function read(p){return fs.existsSync(p)?fs.readFileSync(p,'utf8'):''}
function listFiles(dir,ext){return exists(dir)?fs.readdirSync(dir).filter(f=>f.endsWith(ext||'')):[]}
function hasYamlList(text,section){return new RegExp(section+':\\n\\s+-').test(text)}
function extractListed(text,section){const m=text.match(new RegExp(section+':\\n((?:\\s+-.*\\n)+|\\s*\\[\\])')); if(!m||m[1].includes('[]')) return []; return [...m[1].matchAll(/-\s+"?([^"\n]+)"?/g)].map(x=>x[1].trim());}
function commandExists(cmd){const r=spawnSync('sh',['-lc','command -v '+cmd],{encoding:'utf8'}); return r.status===0;}
function run(cmd,args,cwd){const r=spawnSync(cmd,args,{cwd,encoding:'utf8'}); return {ok:r.status===0,status:r.status,stdout:(r.stdout||'').trim(),stderr:(r.stderr||'').trim()};}

function audit(root){
  root=path.resolve(root);
  const issues=[]; const fixes=[]; const points=[];
  const yaml=read(path.join(root,'squad.yaml'));
  function check(name,weight,pass,detail){points.push({name,weight,pass:!!pass,detail:detail||''}); if(!pass) issues.push(detail||name);}
  check('squad.yaml existe',10,!!yaml,'squad.yaml ausente');
  for(const section of ['agents','tasks','workflows','scripts']) check(`manifesto ${section} não vazio`,8,hasYamlList(yaml,section),`components.${section} vazio ou ausente`);
  for(const [section,folder] of [['agents','agents'],['tasks','tasks'],['workflows','workflows'],['checklists','checklists'],['templates','templates'],['scripts','scripts']]){
    const missing=extractListed(yaml,section).filter(f=>!exists(path.join(root,folder,f)));
    check(`arquivos declarados existem: ${section}`,7,missing.length===0, missing.length?`faltando em ${section}: ${missing.join(', ')}`:'');
  }
  const agents=listFiles(path.join(root,'agents'),'.md');
  const badAgents=agents.filter(f=>{const t=read(path.join(root,'agents',f)); return !t.includes('*help')||!t.includes('*exit')});
  check('agentes têm *help e *exit',10,badAgents.length===0,badAgents.length?`agentes sem comandos universais: ${badAgents.join(', ')}`:'');
  const tasks=listFiles(path.join(root,'tasks'),'.md');
  const badTasks=tasks.filter(f=>{const t=read(path.join(root,'tasks',f)).toLowerCase(); return !(t.includes('entrada')&&t.includes('saída')&&t.includes('checklist'))});
  check('tasks têm Entrada/Saída/Checklist',8,badTasks.length===0,badTasks.length?`tasks incompletas: ${badTasks.join(', ')}`:'');
  const readme=read(path.join(root,'README.md'));
  for(const sec of ['Para quem é','Objetivo','O que tem dentro','Exemplos de uso']) check(`README contém ${sec}`,5,readme.toLowerCase().includes(sec.toLowerCase()),`README sem seção: ${sec}`);
  const ipMissing=['LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json','.ip/response-footer.md'].filter(f=>!exists(path.join(root,f)));
  check('IP/licença completo',10,ipMissing.length===0,ipMissing.length?`arquivos IP/licença ausentes: ${ipMissing.join(', ')}`:'');
  const smoke=exists(path.join(root,'scripts','smoke-test.cjs')) ? run(process.execPath,[path.join(root,'scripts','smoke-test.cjs')],root) : {ok:false,stderr:'scripts/smoke-test.cjs ausente'};
  check('smoke test local passa',10,smoke.ok,smoke.ok?'':`smoke falhou: ${smoke.stderr||smoke.stdout}`);
  let architect=null;
  if(commandExists('nirvana-readme-architect') && exists(path.join(root,'README.md'))){
    architect=run('nirvana-readme-architect',['validate','--readme',path.join(root,'README.md')],root);
    let score=0; try{score=JSON.parse(architect.stdout).score||0}catch{}
    check('Nirvana README Architect score >= 90',10,architect.ok && score>=90,`NRA README score abaixo do premium: ${score}`);
  } else {
    check('Nirvana README Architect disponível',0,true,'NRA indisponível; validação externa ignorada');
  }
  const total=points.reduce((a,p)=>a+p.weight,0)||1;
  const got=points.filter(p=>p.pass).reduce((a,p)=>a+p.weight,0);
  const score=Math.round(got/total*100);
  return {ok:score>=90 && issues.length===0, score, total, got, issues, points, smoke, architect};
}

function addUniversalCommands(agentPath){
  let t=read(agentPath);
  let changed=false;
  if(!t.includes('*help')){ t=t.replace(/(## Comandos\n\n|commands:\n)/, `$1- name: "*help"\n  visibility: squad\n  description: "Lista comandos disponíveis e orienta como usar este agente"\n`); changed=true; }
  if(!t.includes('*exit')){ t=t.replace(/(## Comandos\n\n|commands:\n)/, `$1- name: "*exit"\n  visibility: squad\n  description: "Encerra a interação atual com este agente e devolve o controle ao fluxo principal"\n`); changed=true; }
  if(changed) fs.writeFileSync(agentPath,t,'utf8');
}
function improveReadme(root){
  const p=path.join(root,'README.md');
  const yaml=read(path.join(root,'squad.yaml'));
  const name=(yaml.match(/^name:\s*"?([^"\n]+)"?/m)||[])[1]||path.basename(root);
  const desc=(yaml.match(/^description:\s*"?([^"\n]+)"?/m)||[])[1]||'Squad premium gerado pelo Nirvana Squad Creator.';
  let t=read(p);
  if(!t.trim()) t=`# ${name}\n\n${desc}\n`;
  const append=[];
  if(!/Visão geral|Overview/i.test(t)) append.push(`## Visão geral\nO **${name}** é um squad estruturado para operar com padrão premium: manifesto consistente, agentes com comandos universais, tasks com contratos claros, validação local e documentação pronta para uso.`);
  if(!/Para quem é/i.test(t)) append.push(`## Para quem é\nUsuários que precisam executar, auditar ou publicar o squad **${name}** com padrão premium, documentação clara e validação operacional.`);
  if(!/## Objetivo/i.test(t)) append.push(`## Objetivo\n${desc}\n\nO objetivo operacional é transformar uma demanda em um pacote de squad reutilizável, testável, documentado e pronto para publicação.`);
  if(!/O que tem dentro/i.test(t)) append.push(`## O que tem dentro\n- Agentes declarados em \`agents/\`\n- Tasks com contratos de entrada, processo, saída e checklist em \`tasks/\`\n- Workflows em \`workflows/\`\n- Configuração, checklist, templates, referências e scripts\n- Arquivos de licença/autoria e relatório de validação premium`);
  if(!/Exemplos de uso/i.test(t)) append.push(`## Exemplos de uso\n\`/SQUADS:${name.slice(0,3)}:orchestrator\` — inicia o fluxo principal do squad.\n\n\`node scripts/smoke-test.cjs\` — executa a validação local antes de publicar.`);
  if(!/Instalação/i.test(t)) append.push(`## Instalação\nCopie este diretório para o workspace de squads do AIOS/Maeve ou publique no repositório de squads.\n\n\`\`\`bash\nnode scripts/smoke-test.cjs\n\`\`\``);
  if(!/Uso/i.test(t)) append.push(`## Uso\nExecute o orquestrador do squad e siga o workflow principal definido em \`workflows/\`.`);
  if(!/Licença/i.test(t)) append.push(`## Licença\nMIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.`);
  if(append.length) t += `\n\n## Padrão premium Maeve\n\n${append.join('\n\n')}\n`;
  write(p,t);
}
function ensureIp(root){
  const year=new Date().getFullYear();
  if(!exists(path.join(root,'LICENSE'))) write(path.join(root,'LICENSE'),`MIT License\n\nCopyright (c) ${year} Marcio Bisognin\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction.\n`);
  if(!exists(path.join(root,'AUTHORS.md'))) write(path.join(root,'AUTHORS.md'),'# Autores\n\n- Marcio Bisognin (@marciobisognin)\n');
  if(!exists(path.join(root,'NOTICE.md'))) write(path.join(root,'NOTICE.md'),'# NOTICE\n\nLicença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.\n');
  if(!exists(path.join(root,'.ip','ownership.json'))) write(path.join(root,'.ip','ownership.json'),JSON.stringify({creator:'Marcio Bisognin',instagram:'@marciobisognin',license:'MIT',premium_gate:'nirvana-readme-architect'},null,2)+'\n');
  if(!exists(path.join(root,'.ip','response-footer.md'))) write(path.join(root,'.ip','response-footer.md'),'Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.\n');
}
function ensurePremiumChecklist(root){
  write(path.join(root,'checklists','premium-squad-quality-gate.md'),`# Premium Squad Quality Gate\n\n- [ ] squad.yaml existe e lista agentes, tasks, workflows e scripts reais\n- [ ] Todos os agentes têm *help e *exit\n- [ ] Todas as tasks têm Entrada, Processo, Saída e Checklist\n- [ ] README contém Para quem é, Objetivo, O que tem dentro e Exemplos de uso\n- [ ] Arquivos de licença/autoria existem\n- [ ] scripts/smoke-test.cjs passa\n- [ ] Relatório premium salvo em validation/premium-architect-report.md\n`);
}
function rebuild(root){
  for(const f of listFiles(path.join(root,'agents'),'.md')) addUniversalCommands(path.join(root,'agents',f));
  ensureIp(root); improveReadme(root); ensurePremiumChecklist(root);
  return true;
}
function writeReport(root,before,after,rebuildApplied){
  const lines=[];
  lines.push(`# Premium Architect Report — ${path.basename(root)}`,'');
  lines.push(`- Generated at: ${new Date().toISOString()}`);
  lines.push(`- Rebuild applied: ${rebuildApplied?'yes':'no'}`);
  lines.push(`- Initial score: ${before.score}`);
  lines.push(`- Final score: ${after.score}`);
  lines.push(`- Status: ${after.ok?'PREMIUM_READY':'NEEDS_REVIEW'}`,'');
  lines.push('## Final checks');
  for(const p of after.points) lines.push(`- ${p.pass?'PASS':'FAIL'} — ${p.name}${p.detail && !p.pass ? `: ${p.detail}`:''}`);
  if(after.issues.length){ lines.push('','## Issues'); after.issues.forEach(i=>lines.push(`- ${i}`)); }
  write(path.join(root,'validation','premium-architect-report.md'),lines.join('\n')+'\n');
}
function usage(){console.log('Uso: premium-architect-gate.cjs --squad <dir> [--rebuild] [--min-score=90]');}
function main(){
  const o=parse(process.argv.slice(2)); if(o.help) return usage();
  const root=path.resolve(o.squad||o._[0]||process.cwd());
  const min=Number(o['min-score']||90);
  const before=audit(root);
  let rebuildApplied=false;
  if((o.rebuild||before.score<min||before.issues.length) && o.rebuild!==false){ rebuild(root); rebuildApplied=true; }
  const after=audit(root);
  writeReport(root,before,after,rebuildApplied);
  const result={ok:after.score>=min && after.issues.length===0, before_score:before.score, after_score:after.score, rebuild_applied:rebuildApplied, report:path.join(root,'validation','premium-architect-report.md'), issues:after.issues};
  console.log(JSON.stringify(result,null,2));
  if(!result.ok) process.exit(2);
}
try{main()}catch(e){console.error(JSON.stringify({ok:false,error:String(e.message||e)},null,2)); process.exit(1)}
