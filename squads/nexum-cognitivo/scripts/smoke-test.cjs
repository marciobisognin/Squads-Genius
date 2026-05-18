#!/usr/bin/env node
const fs=require('fs'); const path=require('path'); const cp=require('child_process');
const root=path.resolve(__dirname,'..');
const required=['squad.yaml','README.md','TEXTO_EXPLICATIVO_SQUAD.md','TEXTO_PUBLICACAO_REDES_BLOG.md','scripts/nexum-cognitivo.cjs','workflows/nexum-cognitivo-main.yaml'];
const missing=required.filter(f=>!fs.existsSync(path.join(root,f)));
if(missing.length){ console.error(JSON.stringify({ok:false,missing},null,2)); process.exit(1); }
const out=path.join(root,'generated','smoke-demo');
let r=cp.spawnSync(process.execPath,[path.join(root,'scripts','nexum-cognitivo.cjs'),'generate','--goal','reter conceitos de neuroaprendizagem','--domain','estudo','--gap','memoria','--minutes','15','--out',out],{encoding:'utf8'});
if(r.status!==0){ console.error(r.stderr||r.stdout); process.exit(1); }
r=cp.spawnSync(process.execPath,[path.join(root,'scripts','nexum-cognitivo.cjs'),'validate','--input',out],{encoding:'utf8'});
if(r.status!==0){ console.error(r.stderr||r.stdout); process.exit(1); }
console.log(JSON.stringify({ok:true,checked:required.length,generated:path.relative(root,out)},null,2));
