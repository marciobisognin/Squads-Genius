#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function parseArgs(argv){
  const args={_:[]};
  for(let i=0;i<argv.length;i++){
    const a=argv[i];
    if(a.startsWith('--')){
      const [k,v] = a.slice(2).split('=');
      args[k] = v !== undefined ? v : (argv[i+1] && !argv[i+1].startsWith('--') ? argv[++i] : true);
    } else args._.push(a);
  }
  return args;
}
function ensureDir(p){ fs.mkdirSync(p,{recursive:true}); }
function write(p,c){ ensureDir(path.dirname(p)); fs.writeFileSync(p,c); }
function csvEscape(x){ return '"'+String(x).replace(/"/g,'""')+'"'; }

const argv=parseArgs(process.argv.slice(2));
const cmd=argv._[0] || 'help';
const footer='Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.';

function help(){
  console.log(`Nexum Cognitivo CLI\n\nComandos:\n  generate --goal TEXTO --domain DOMINIO --gap LACUNA --minutes 10..15 --out DIR\n  validate --input DIR\n  --help\n`);
}

function generate(){
  const goal=argv.goal || 'Aprender um conteúdo novo com mais retenção';
  const domain=argv.domain || 'aprendizagem';
  const gap=argv.gap || 'memoria';
  let minutes=Number(argv.minutes || 15);
  if(!Number.isFinite(minutes)) minutes=15;
  if(minutes < 10) minutes=10;
  if(minutes > 15) minutes=15;
  const out=path.resolve(argv.out || 'generated/nexum-demo');
  const main=Math.max(6, minutes-7);
  const recovery=2;
  const compression=2;
  const log=Math.max(1, minutes-1-main-recovery-compression);
  const plan={
    goal, domain, dominant_gap: gap, total_minutes: minutes,
    blocks:[
      {name:'Priming metacognitivo', minutes:1, instruction:'Defina a lacuna dominante e o erro provável antes de começar.'},
      {name:'Sprint cognitivo principal', minutes:main, instruction:'Execute uma tarefa única, com atenção sustentada e sem alternar fontes.'},
      {name:'Recuperação ativa', minutes:recovery, instruction:'Feche a fonte e evoque de memória os pontos essenciais.'},
      {name:'Compressão verbal', minutes:compression, instruction:'Explique em 3 frases ou 1 analogia aplicável.'},
      {name:'Registro mínimo', minutes:log, instruction:'Registre foco, clareza, itens evocados, erro dominante e próxima repetição.'}
    ],
    ethics:'Educacional, não clínico. Não promete aumento de QI, diagnóstico ou tratamento.'
  };
  const md=`# Protocolo diário — Nexum Cognitivo\n\n## Meta\n${goal}\n\n## Domínio\n${domain}\n\n## Lacuna dominante\n${gap}\n\n## Sessão de ${minutes} minutos\n\n${plan.blocks.map(b=>`### ${b.name} — ${b.minutes} min\n${b.instruction}`).join('\n\n')}\n\n## Perguntas de recuperação ativa\n\n1. O que eu consigo explicar sem consultar?\n2. Qual foi o erro dominante?\n3. Como aplico isso em um caso real hoje?\n\n## Métrica mínima\n\n- foco_0_10\n- clareza_0_5\n- itens_evocados\n- erro_dominante\n- proxima_repeticao\n\n${footer}\n`;
  ensureDir(out);
  write(path.join(out,'daily_protocol.md'), md);
  write(path.join(out,'micro_sprint_plan.json'), JSON.stringify(plan,null,2));
  write(path.join(out,'metrics_plan.json'), JSON.stringify({focus_0_10:null, clarity_0_5:null, recalled_items:null, dominant_error:'', next_repetition:'', energy_0_5:null}, null,2));
  write(path.join(out,'dashboard_seed.csv'), ['date,goal,domain,gap,focus_0_10,clarity_0_5,recalled_items,dominant_error,next_repetition', [new Date().toISOString().slice(0,10), goal, domain, gap, '', '', '', '', ''].map(csvEscape).join(',')].join('\n'));
  console.log(JSON.stringify({ok:true,out,minutes,files:['daily_protocol.md','micro_sprint_plan.json','metrics_plan.json','dashboard_seed.csv']},null,2));
}

function validate(){
  const input=path.resolve(argv.input || argv.out || 'generated/nexum-demo');
  const required=['daily_protocol.md','micro_sprint_plan.json','metrics_plan.json','dashboard_seed.csv'];
  const missing=required.filter(f=>!fs.existsSync(path.join(input,f)));
  let plan=null;
  try{ plan=JSON.parse(fs.readFileSync(path.join(input,'micro_sprint_plan.json'),'utf8')); }catch(e){}
  const errors=[];
  if(missing.length) errors.push('Arquivos ausentes: '+missing.join(', '));
  if(!plan) errors.push('micro_sprint_plan.json inválido');
  if(plan){
    if(plan.total_minutes < 10 || plan.total_minutes > 15) errors.push('total_minutes fora de 10–15');
    const sum=(plan.blocks||[]).reduce((a,b)=>a+Number(b.minutes||0),0);
    if(sum !== plan.total_minutes) errors.push(`soma dos blocos (${sum}) difere do total (${plan.total_minutes})`);
    if(!String(plan.ethics||'').includes('não clínico')) errors.push('falta limite não clínico');
  }
  const ok=errors.length===0;
  console.log(JSON.stringify({ok,input,checked:required.length,errors},null,2));
  process.exit(ok?0:1);
}

if(cmd==='help' || argv.help || cmd==='--help') help();
else if(cmd==='generate') generate();
else if(cmd==='validate' || argv.validate) validate();
else { console.error('Comando desconhecido: '+cmd); help(); process.exit(1); }
