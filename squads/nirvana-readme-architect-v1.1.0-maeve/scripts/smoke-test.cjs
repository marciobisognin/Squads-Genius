#!/usr/bin/env node
const fs=require('fs'); const path=require('path'); const {spawnSync}=require('child_process');
const root=path.resolve(__dirname,'..');
const required=['squad.yaml','README.md','agents/nra-orchestrator.md','tasks/nra-orchestrator-parse-request.md','workflows/readme-generation-pipeline.yaml','scripts/readme-architect.cjs','bin/nirvana-readme-architect.cjs'];
const missing=required.filter(f=>!fs.existsSync(path.join(root,f)));
if(missing.length){ console.error(JSON.stringify({ok:false,missing},null,2)); process.exit(1); }
for(const f of fs.readdirSync(path.join(root,'agents')).filter(f=>f.endsWith('.md'))){ const t=fs.readFileSync(path.join(root,'agents',f),'utf8'); if(!t.includes('*help')||!t.includes('*exit')){ console.error(JSON.stringify({ok:false,error:'missing universal command',file:f},null,2)); process.exit(1); } }
const demo=path.join(root,'.smoke-demo'); fs.mkdirSync(demo,{recursive:true}); fs.writeFileSync(path.join(demo,'package.json'), JSON.stringify({name:'demo',description:'Demo project',scripts:{start:'node index.js'}},null,2));
const out=path.join(demo,'README.generated.md'); const r=spawnSync(process.execPath,[path.join(root,'scripts/readme-architect.cjs'),'generate','--project',demo,'--output',out,'--mode=quick'],{encoding:'utf8'});
if(r.status!==0 || !fs.existsSync(out)){ console.error(JSON.stringify({ok:false,status:r.status,stdout:r.stdout,stderr:r.stderr},null,2)); process.exit(1); }
console.log(JSON.stringify({ok:true,checked:required.length,generated:out},null,2));
