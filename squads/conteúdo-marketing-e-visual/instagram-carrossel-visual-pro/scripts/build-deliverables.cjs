#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = process.cwd();
const out = path.join(root, 'output');
const dirs = ['slides', 'ppt', 'video', 'publish-package'];

if (!fs.existsSync(out)) fs.mkdirSync(out, { recursive: true });
for (const d of dirs) fs.mkdirSync(path.join(out, d), { recursive: true });

const placeholder = (p, c) => fs.writeFileSync(path.join(out, p), c, 'utf8');
placeholder('carrossel-script.md', '# roteiro\n');
placeholder('carrossel-copy.md', '# copy\n');
placeholder('legenda.txt', 'Legenda final do carrossel.\n');
placeholder('hashtags.txt', '#instagram #carrossel\n');
placeholder('source-log.txt', 'build-deliverables executed\n');

console.log(JSON.stringify({ ok: true, output: out, created: dirs }, null, 2));
