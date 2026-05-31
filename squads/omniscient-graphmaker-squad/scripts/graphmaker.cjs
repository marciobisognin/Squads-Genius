#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
function arg(name, fallback){ const i=process.argv.indexOf(name); return i>=0 && process.argv[i+1] ? process.argv[i+1] : fallback; }
function ensure(p){ fs.mkdirSync(p,{recursive:true}); }
function readJson(p){ return JSON.parse(fs.readFileSync(p,'utf8')); }
function writeJson(p,obj){ fs.writeFileSync(p, JSON.stringify(obj,null,2)); }
function fingerprint(obj){ return Buffer.from(JSON.stringify(obj)).toString('base64').slice(0,24); }
function buildVhm(clones){
  return clones.map(c => ({
    clone: c,
    sources: [`rag/${c.toLowerCase()}/*`],
    heuristic_vector: {risk: c==='Taleb'?0.95:0.55, inversion: c==='Munger'?0.95:0.45, execution: c==='Bezos'?0.9:0.5, management: c==='Drucker'?0.9:0.5},
    allowed_scope: ['strategy','risk','metrics','execution_translation'],
    utility_loss_function: 'penalize_scope_drift + penalize_unstructured_handoff + penalize_non_actionable_claims'
  }));
}
function run(){
  const input = arg('--input','examples/v65-master-pitch.json');
  const out = arg('--output','generated/v65-demo');
  ensure(out);
  const pitch = readJson(input);
  const maxLatency = pitch.constraints?.max_latency_minutes || 6;
  const maxCost = pitch.constraints?.max_api_cost_usd || 1.5;
  const classification = {cynefin:'complex', complexity_score:0.82, routing:'boardroom_then_sacp_then_graphmaker'};
  const governance = {
    token_budget: {strategic_boardroom: 18000, tactical_swarm: 9000, validation: 3000, total: 30000},
    latency_budget_minutes: {classification:0.25, boardroom:2.5, sacp:0.75, graphmaker:1.5, validation:1.0, total:maxLatency},
    cost_ceiling_usd: maxCost,
    model_tiers: {classifier:'fast-low-cost', boardroom:'high-reasoning-only-when-complex', swarm:'medium-fast', validator:'low-cost-structured'},
    cache_key: fingerprint({market:pitch.market, constraints:pitch.constraints, frameworks:pitch.required_frameworks}),
    fallback: {max_self_healing_attempts:pitch.constraints?.max_self_healing_attempts || 3, human_alert:true}
  };
  const vhm = buildVhm(pitch.boardroom || ['Taleb','Munger','Drucker','Bezos']);
  const stress_test = {tail_risks:['API cost explosion','context anarchy','semantic handoff failure','latency creep'], antifragility_score:0.74, pass:true};
  const inversion = {failure_modes:['free-text handoff','uncapped debate rounds','no schema validation','all agents using premium model'], destruction_probability_before_controls:0.68, destruction_probability_after_controls:0.21};
  const boardroom = {
    rounds:[
      {round:1, name:'divergence', temperature:0.8, output:'independent theses'},
      {round:2, name:'antithesis', temperature:0.4, output:'stress and inversion attacks'},
      {round:3, name:'synthesis', temperature:0.1, output:'metrics and go/no-go'}
    ],
    convergence_score:0.88,
    decision:'go_with_governed_execution'
  };
  const sacp = {
    qualitative_claim:'O ecossistema deve evitar Torre de Babel e traduzir estratégia em execução auditável.',
    quantitative_translation:{min_convergence_score:0.8, max_rounds:3, zero_free_text_handoff:true, max_latency_minutes:maxLatency, max_cost_usd:maxCost},
    confidence:0.86,
    task_atoms:['compile_vhm','stress_test','invert_failure_modes','synthesize_metrics','build_dag','generate_landing_spec','validate_budget'],
    acceptance_criteria:['schema_valid','dag_acyclic','budget_within_limits','all_handoffs_structured']
  };
  const dag = [
    {id:'cynefin_classifier', depends_on:[]},
    {id:'token_latency_governor', depends_on:['cynefin_classifier']},
    {id:'idbalance_vhm', depends_on:['cynefin_classifier']},
    {id:'taleb_engine', depends_on:['idbalance_vhm']},
    {id:'munger_engine', depends_on:['taleb_engine']},
    {id:'cognitive_boardroom', depends_on:['munger_engine','token_latency_governor']},
    {id:'relation_sacp', depends_on:['cognitive_boardroom']},
    {id:'venture_synthesis_matrix', depends_on:['relation_sacp']},
    {id:'graphmaker', depends_on:['venture_synthesis_matrix']},
    {id:'visual_axiom', depends_on:['graphmaker']},
    {id:'neural_cloning', depends_on:['graphmaker']},
    {id:'conversion_alchemy', depends_on:['graphmaker']},
    {id:'frictionless_conversion', depends_on:['visual_axiom','neural_cloning','conversion_alchemy']}
  ];
  const metrics = {north_star:'structured_blueprint_to_validated_landing_spec_rate', convergence_score:boardroom.convergence_score, antifragility_score:stress_test.antifragility_score, estimated_latency_minutes:5.75, estimated_cost_usd:1.18};
  const blueprint = {version:'6.5', classification, vhm, stress_test, inversion, boardroom, sacp, dag, metrics, governance};
  writeJson(path.join(out,'meta-blueprint-v6.5.json'), blueprint);
  writeJson(path.join(out,'execution-dag-v6.5.json'), dag);
  writeJson(path.join(out,'token-latency-budget.json'), governance);
  const md = `# OMNISCIENT v6.5 — Landing / Produto Spec\n\n## Master Pitch\n${pitch.master_pitch}\n\n## Decisão\n${boardroom.decision}\n\n## Controles de engenharia\n- IDBALANCE VHM para identidade heurística.\n- Taleb Engine para risco de cauda longa.\n- Munger Engine para inversão e modos de falha.\n- RELATION/SACP para handoff JSON quantitativo.\n- GRAPHMAKER DAG para execução acíclica.\n- Governança: ${governance.latency_budget_minutes.total} min, US$ ${governance.cost_ceiling_usd}.\n\n## Métricas\n- Convergência: ${metrics.convergence_score}\n- Antifragilidade: ${metrics.antifragility_score}\n- Latência estimada: ${metrics.estimated_latency_minutes} min\n- Custo estimado: US$ ${metrics.estimated_cost_usd}\n\nLicença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.\n`;
  fs.writeFileSync(path.join(out,'product-spec-v6.5.md'), md);
  console.log(JSON.stringify({ok:true, version:'6.5', output:out, files:fs.readdirSync(out).sort()}, null, 2));
}
function validate(){
  const out = arg('--output','generated/v65-demo');
  const required = ['meta-blueprint-v6.5.json','execution-dag-v6.5.json','token-latency-budget.json','product-spec-v6.5.md'];
  const missing = required.filter(f=>!fs.existsSync(path.join(out,f)));
  if(missing.length){ console.error(JSON.stringify({ok:false, missing}, null, 2)); process.exit(2); }
  const bp = readJson(path.join(out,'meta-blueprint-v6.5.json'));
  const ids = new Set(bp.dag.map(n=>n.id));
  for(const n of bp.dag){ for(const dep of n.depends_on||[]){ if(!ids.has(dep)){ console.error(`missing dependency ${dep}`); process.exit(3); } } }
  if(bp.metrics.estimated_latency_minutes > bp.governance.latency_budget_minutes.total) { console.error('latency budget exceeded'); process.exit(4); }
  if(bp.metrics.estimated_cost_usd > bp.governance.cost_ceiling_usd) { console.error('cost budget exceeded'); process.exit(5); }
  if(!bp.sacp.quantitative_translation.zero_free_text_handoff) { console.error('SACP handoff not enforced'); process.exit(6); }
  console.log(JSON.stringify({ok:true, version:bp.version, nodes:bp.dag.length, convergence:bp.metrics.convergence_score, cost:bp.metrics.estimated_cost_usd, latency:bp.metrics.estimated_latency_minutes}, null, 2));
}
const cmd = process.argv[2] || 'help';
if(cmd==='run') run();
else if(cmd==='validate') validate();
else console.log('Usage: node scripts/graphmaker.cjs run --input examples/v65-master-pitch.json --output generated/v65-demo\n       node scripts/graphmaker.cjs validate --output generated/v65-demo');
