#!/usr/bin/env node
const {spawnSync} = require('child_process');
function run(args){ const r=spawnSync('node', args, {encoding:'utf8'}); if(r.status!==0){ console.error(r.stdout); console.error(r.stderr); process.exit(r.status||1);} console.log(r.stdout.trim()); }
run(['scripts/graphmaker.cjs','run','--input','examples/v65-master-pitch.json','--output','generated/v65-demo']);
run(['scripts/graphmaker.cjs','validate','--output','generated/v65-demo']);
console.log('SMOKE_TEST_V6_5_PASSED');
