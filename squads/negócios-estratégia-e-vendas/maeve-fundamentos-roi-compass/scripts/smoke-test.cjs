#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const root=path.resolve(__dirname,'..');
const required=['squad.yaml','README.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json','agents/orchestrator.md','agents/researcher.md','agents/builder.md','agents/validator.md','tasks/analyze-requirements.md','tasks/build-artifacts.md','tasks/validate-release.md','tasks/publish-package.md','workflows/main.yaml','checklists/release-checklist.md'];
const missing=required.filter(f=>!fs.existsSync(path.join(root,f)));
if(missing.length){ console.error(JSON.stringify({ok:false,missing},null,2)); process.exit(1);}
const yaml=fs.readFileSync(path.join(root,'squad.yaml'),'utf8');
for(const section of ['agents','tasks','workflows','scripts']){ if(!new RegExp(section+':\\n\\s+-').test(yaml)){ console.error(JSON.stringify({ok:false,error:'manifesto vazio: '+section},null,2)); process.exit(1);} }
console.log(JSON.stringify({ok:true,checked:required.length},null,2));
