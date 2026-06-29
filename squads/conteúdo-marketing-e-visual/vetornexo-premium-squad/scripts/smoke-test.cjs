#!/usr/bin/env node
const cp=require('child_process');
function run(cmd){ console.log('> '+cmd); cp.execSync(cmd,{stdio:'inherit'}); }
run('node scripts/vetornexo.cjs generate --input examples/demo-brief.json --output outputs/demo');
run('node scripts/vetornexo.cjs validate --output outputs/demo');
console.log('Smoke test VetorNexo aprovado.');
