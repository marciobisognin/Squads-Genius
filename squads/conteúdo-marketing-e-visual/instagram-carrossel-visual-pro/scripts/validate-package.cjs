#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const required = [
  'README.md',
  'squad.yaml',
  'agents',
  'tasks',
  'workflows',
  'checklists',
  'templates',
  'references',
  'scripts/build-deliverables.cjs'
];

const root = process.cwd();
const missing = required.filter(p => !fs.existsSync(path.join(root, p)));
console.log(JSON.stringify({ ok: missing.length === 0, missing }, null, 2));
process.exit(missing.length === 0 ? 0 : 1);
