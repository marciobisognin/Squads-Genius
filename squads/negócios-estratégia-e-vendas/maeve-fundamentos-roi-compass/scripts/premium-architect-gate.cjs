#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const idx = process.argv.findIndex(a => a === '--squad' || a === '--path');
const root = path.resolve(idx >= 0 ? process.argv[idx + 1] : process.cwd());
const required = [
  'squad.yaml','README.md','LICENSE','NOTICE.md','AUTHORS.md','.ip/ownership.json',
  'agents/orchestrator.md','agents/researcher.md','agents/builder.md','agents/validator.md',
  'tasks/analyze-requirements.md','tasks/build-artifacts.md','tasks/validate-release.md',
  'workflows/main.yaml','scripts/smoke-test.cjs','scripts/fundamentos-roi-compass.cjs'
];
const missing = required.filter(f => !fs.existsSync(path.join(root, f)));
const readme = fs.existsSync(path.join(root, 'README.md')) ? fs.readFileSync(path.join(root, 'README.md'), 'utf8') : '';
const sections = ['Para quem é','Objetivo','O que tem dentro','Exemplos de uso','Problemas que o squad reduz'];
const missingSections = sections.filter(s => !readme.toLowerCase().includes(s.toLowerCase()));
const agentsDir = path.join(root, 'agents');
const agentFiles = fs.existsSync(agentsDir) ? fs.readdirSync(agentsDir).filter(f => f.endsWith('.md')) : [];
const commandIssues = [];
for (const f of agentFiles) {
  const txt = fs.readFileSync(path.join(agentsDir, f), 'utf8');
  if (!txt.includes('*help') || !txt.includes('*exit')) commandIssues.push(`${f}: missing *help/*exit`);
}
const score = Math.max(0, 100 - missing.length * 8 - missingSections.length * 5 - commandIssues.length * 5);
const ok = score >= 90 && missing.length === 0 && missingSections.length === 0 && commandIssues.length === 0;
const report = path.join(root, 'validation', 'premium-architect-report.md');
fs.mkdirSync(path.dirname(report), {recursive: true});
fs.writeFileSync(report, `# Premium Architect Report

- Score: ${score}
- Missing files: ${missing.length ? missing.join(', ') : 'none'}
- Missing README sections: ${missingSections.length ? missingSections.join(', ') : 'none'}
- Agent command issues: ${commandIssues.length ? commandIssues.join(', ') : 'none'}

## Decision
${ok ? 'Approved' : 'Rejected'}
`);
console.log(JSON.stringify({ok, before_score: score, after_score: score, report, issues: [...missing, ...missingSections, ...commandIssues]}, null, 2));
if (!ok) process.exit(2);
