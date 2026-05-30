#!/usr/bin/env node
const fs=require('fs');
const path=require('path');

function usage(){
  console.log(`Nirvana README Architect CLI\n\nUso:\n  nirvana-readme-architect generate --project <dir> [--output README.md] [--mode=quick|full]\n  nirvana-readme-architect scan --project <dir>\n  nirvana-readme-architect validate --readme <file>\n`);
}
function parse(argv){
  const opts={_:[]};
  for(let i=0;i<argv.length;i++){
    const a=argv[i];
    if(a==='-h'||a==='--help'){opts.help=true;continue;}
    if(a.startsWith('--')){const eq=a.indexOf('='); if(eq>=0) opts[a.slice(2,eq)]=a.slice(eq+1); else if(i+1<argv.length&&!argv[i+1].startsWith('--')) opts[a.slice(2)]=argv[++i]; else opts[a.slice(2)]=true;}
    else opts._.push(a);
  }
  return opts;
}
function readJson(p){ try{return JSON.parse(fs.readFileSync(p,'utf8'));}catch{return null;} }
function list(dir){ try{return fs.readdirSync(dir).filter(x=>!['.git','node_modules','.venv','venv','__pycache__'].includes(x));}catch{return [];} }
function scan(project){
  project=path.resolve(project||process.cwd());
  const pkg=readJson(path.join(project,'package.json'));
  const py=fs.existsSync(path.join(project,'pyproject.toml'));
  const req=fs.existsSync(path.join(project,'requirements.txt'));
  const files=list(project);
  const dirs=files.filter(f=>{try{return fs.statSync(path.join(project,f)).isDirectory()}catch{return false}});
  const stack=[];
  if(pkg) stack.push('Node.js');
  if(py||req) stack.push('Python');
  if(files.includes('Dockerfile')) stack.push('Docker');
  const scripts=pkg && pkg.scripts ? Object.keys(pkg.scripts) : [];
  let type='Projeto';
  if(pkg?.bin) type='CLI';
  else if(pkg?.dependencies?.express || pkg?.dependencies?.fastify) type='API Node.js';
  else if(pkg?.dependencies?.react || pkg?.dependencies?.next) type='Web App';
  else if(py || req) type='Python';
  return {project,name:pkg?.name||path.basename(project),description:pkg?.description||'',type,stack, scripts, dirs:dirs.slice(0,30), files:files.slice(0,40)};
}
function badge(label,msg,color='blue'){return `![${label}](https://img.shields.io/badge/${encodeURIComponent(label)}-${encodeURIComponent(msg)}-${color}?style=flat-square)`}
function generate(data, mode='full'){
  const sections=[];
  sections.push(`${badge('README','Nirvana','8A2BE2')} ${badge('Quality','Generated','10b981')}\n`);
  sections.push(`# ${data.name}\n`);
  if(data.description) sections.push(`> ${data.description}\n`);
  sections.push(`## Visão geral\n\nEste é um projeto do tipo **${data.type}**. Este README foi gerado a partir de uma varredura automática da estrutura local do projeto.\n`);
  sections.push(`## Stack identificada\n\n${data.stack.length?data.stack.map(s=>`- ${s}`).join('\n'):'- Stack não identificada automaticamente'}\n`);
  if(data.scripts.length) sections.push(`## Scripts disponíveis\n\n${data.scripts.map(s=>`- \`npm run ${s}\``).join('\n')}\n`);
  sections.push(`## Estrutura\n\n<details>\n<summary>Arquivos e diretórios principais</summary>\n\n\`\`\`text\n${[...data.dirs.map(d=>d+'/'),...data.files.filter(f=>!data.dirs.includes(f))].slice(0,60).join('\n')}\n\`\`\`\n</details>\n`);
  sections.push(`## Instalação\n\n\`\`\`bash\n# ajuste conforme o gerenciador do projeto\n${data.stack.includes('Node.js')?'npm install':'# instalar dependências'}\n\`\`\`\n`);
  sections.push(`## Uso\n\n\`\`\`bash\n# exemplo\n${data.scripts.includes('start')?'npm start':data.scripts.includes('dev')?'npm run dev':'# executar comando principal do projeto'}\n\`\`\`\n`);
  if(mode==='full'){
    sections.push(`## Qualidade\n\n- [ ] Instalação documentada\n- [ ] Uso principal documentado\n- [ ] Scripts validados\n- [ ] Licença indicada\n`);
    sections.push(`## Contribuição\n\nAbra uma issue ou pull request com descrição clara da alteração proposta.\n`);
  }
  sections.push(`## Licença\n\nDefinir conforme o projeto.\n`);
  return sections.join('\n');
}
function validate(file){
  const text=fs.readFileSync(file,'utf8');
  const checks=[
    ['title',/^#\s+/m],['overview',/vis[aã]o geral|overview/i],['install',/instala/i],['usage',/uso|usage/i],['license',/licen[çc]a|license/i],['codeblock',/```/],['list',/^[-*]\s+/m]
  ];
  const results=checks.map(([k,re])=>({check:k,pass:re.test(text)}));
  const score=Math.round(results.filter(r=>r.pass).length/checks.length*100);
  return {ok:score>=75,score,results};
}
function main(){
  const opts=parse(process.argv.slice(2));
  if(opts.help||!opts._.length) return usage();
  const cmd=opts._[0];
  if(cmd==='scan'){console.log(JSON.stringify(scan(opts.project),null,2)); return;}
  if(cmd==='generate'){
    const data=scan(opts.project); const md=generate(data, opts.mode||'full');
    const out=path.resolve(opts.output||path.join(data.project,'README.md'));
    fs.writeFileSync(out,md,'utf8');
    const v=validate(out);
    console.log(JSON.stringify({ok:true,output:out,analysis:data,validation:v},null,2)); return;
  }
  if(cmd==='validate'){ const file=path.resolve(opts.readme||opts._[1]||'README.md'); console.log(JSON.stringify(validate(file),null,2)); return;}
  usage();
}
try{main()}catch(e){console.error(JSON.stringify({ok:false,error:String(e.message||e)},null,2)); process.exit(1)}
