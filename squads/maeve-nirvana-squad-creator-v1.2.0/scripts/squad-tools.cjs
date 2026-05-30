#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const WORKSPACE_ROOT = process.env.SQUAD_WORKSPACE_ROOT || path.resolve(process.cwd(), '.squad-workspace');

function ensureDir(p){ fs.mkdirSync(p,{recursive:true}); }
function nowISO(){ return new Date().toISOString(); }
function slug(s){ return String(s||'').trim().replace(/[^a-zA-Z0-9._-]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,''); }

function sessionDir(name){
  const safe = slug(name);
  if(!safe) throw new Error('session inválida');
  return path.join(WORKSPACE_ROOT, safe);
}
function configPath(name){ return path.join(sessionDir(name),'config.json'); }
function stateMdPath(name){ return path.join(sessionDir(name),'STATE.md'); }

function atomicWriteJSON(file, data){
  ensureDir(path.dirname(file));
  const tmp = file + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(data,null,2),'utf8');
  fs.renameSync(tmp,file);
}
function readJSON(file){
  if(!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file,'utf8'));
}

function baseState(session, preset='padrao', objective=''){
  const phases = Array.from({length:9}, (_,i)=>({
    phase:i+1,
    status: i===0 ? 'in_progress' : 'pending',
    started_at: i===0 ? nowISO() : null,
    completed_at: null,
    gate: null,
    notes: ''
  }));
  return {
    session,
    preset,
    objective,
    created_at: nowISO(),
    updated_at: nowISO(),
    current_phase: 1,
    decisions: [],
    phases,
    artifacts: {
      agents:0,tasks:0,workflows:0,checklists:0,templates:0,references:0,config:0
    }
  };
}

function regenerateStateMd(name, state){
  const p = stateMdPath(name);
  const lines=[];
  lines.push(`# Pipeline State — ${state.session}`);
  lines.push('');
  lines.push(`- Preset: ${state.preset}`);
  lines.push(`- Objetivo: ${state.objective || '-'}`);
  lines.push(`- Current phase: ${state.current_phase}`);
  lines.push(`- Updated at: ${state.updated_at}`);
  lines.push('');
  lines.push('| Fase | Status | Início | Fim | Gate | Notas |');
  lines.push('|------|--------|--------|-----|------|-------|');
  for(const ph of state.phases){
    lines.push(`| ${ph.phase} | ${ph.status} | ${ph.started_at||'-'} | ${ph.completed_at||'-'} | ${ph.gate||'-'} | ${(ph.notes||'').replace(/\|/g,'/')} |`);
  }
  lines.push('');
  lines.push('## Decisões');
  if(!state.decisions.length){ lines.push('- (nenhuma)'); }
  for(const d of state.decisions){
    lines.push(`- **${d.title}**: ${d.decision} _(at ${d.at})_`);
  }
  lines.push('');
  lines.push('## Artefatos');
  for(const [k,v] of Object.entries(state.artifacts||{})) lines.push(`- ${k}: ${v}`);
  ensureDir(path.dirname(p));
  fs.writeFileSync(p, lines.join('\n'),'utf8');
}

function saveState(name,state){
  state.updated_at = nowISO();
  atomicWriteJSON(configPath(name), state);
  regenerateStateMd(name,state);
}

function getState(name){
  const s = readJSON(configPath(name));
  if(!s) throw new Error(`sessão não encontrada: ${name}`);
  return s;
}

function countArtifacts(name){
  const sdir = sessionDir(name);
  const map={agents:'agents',tasks:'tasks',workflows:'workflows',checklists:'checklists',templates:'templates',references:'references',config:'config'};
  const out={};
  for(const [k,d] of Object.entries(map)){
    const p=path.join(sdir,d);
    out[k]=fs.existsSync(p)?fs.readdirSync(p).filter(f=>fs.statSync(path.join(p,f)).isFile()).length:0;
  }
  return out;
}

function parseFlag(args,key,def=''){
  const prefix=`--${key}=`;
  const f=args.find(a=>a.startsWith(prefix));
  return f ? f.slice(prefix.length) : def;
}

function cmdInit(args){
  const session=args[0];
  if(!session) throw new Error('uso: init <session> [--preset=padrao] [--objective=...]');
  ensureDir(WORKSPACE_ROOT);
  const dir=sessionDir(session);
  ensureDir(dir);
  const preset=parseFlag(args,'preset','padrao');
  const objective=parseFlag(args,'objective','');
  const state=baseState(slug(session),preset,objective);
  saveState(session,state);
  console.log(JSON.stringify({ok:true,action:'init',session:slug(session),workspace:dir},null,2));
}

function cmdResume(args){
  const session=args[0];
  if(!session) throw new Error('uso: resume <session>');
  const s=getState(session);
  console.log(JSON.stringify({ok:true,action:'resume',session:s.session,current_phase:s.current_phase,state:s},null,2));
}

function cmdGet(args){
  const session=args[0];
  if(!session) throw new Error('uso: get <session>');
  const s=getState(session);
  console.log(JSON.stringify({ok:true,action:'get',state:s},null,2));
}

function cmdStateGet(args){ return cmdGet(args); }

function cmdStateAdvance(args){
  const session=args[0];
  if(!session) throw new Error('uso: state advance <session> --phase=N [--notes=...] [--auto-gate=true|false]');
  const phase=Number(parseFlag(args,'phase','0'));
  const notes=parseFlag(args,'notes','');
  const autoGate=(parseFlag(args,'auto-gate','true') || 'true').toLowerCase() !== 'false';
  const reviewer=parseFlag(args,'reviewer','auto-gate');
  if(!phase || phase<1 || phase>9) throw new Error('phase inválida (1..9)');
  const s=getState(session);
  const p=s.phases.find(x=>x.phase===phase);
  if(!p) throw new Error('phase inexistente');
  p.status='completed';
  p.completed_at=nowISO();
  p.notes=notes || p.notes || '';
  if(autoGate){
    p.gate='approved';
    p.gate_reviewer=reviewer;
  }
  if(phase<9){
    const n=s.phases.find(x=>x.phase===phase+1);
    if(n && n.status==='pending'){ n.status='in_progress'; n.started_at=nowISO(); }
    s.current_phase=Math.max(s.current_phase, phase+1);
  } else s.current_phase=9;
  s.artifacts = countArtifacts(session);
  saveState(session,s);
  console.log(JSON.stringify({ok:true,action:'state.advance',phase,current_phase:s.current_phase,auto_gate:autoGate},null,2));
}

function cmdStateGate(args){
  const session=args[0];
  if(!session) throw new Error('uso: state gate <session> --phase=N --result=approved|rejected');
  const phase=Number(parseFlag(args,'phase','0'));
  const result=parseFlag(args,'result','');
  if(!['approved','rejected'].includes(result)) throw new Error('result inválido');
  const reviewer=parseFlag(args,'reviewer','');
  const s=getState(session);
  const p=s.phases.find(x=>x.phase===phase);
  if(!p) throw new Error('phase inexistente');
  p.gate=result;
  p.gate_reviewer=reviewer||null;
  if(result==='rejected'){
    p.status='in_progress';
    s.current_phase=phase;
  }
  saveState(session,s);
  console.log(JSON.stringify({ok:true,action:'state.gate',phase,result},null,2));
}

function cmdStateAddDecision(args){
  const session=args[0];
  if(!session) throw new Error('uso: state add-decision <session> --title=... --decision=...');
  const title=parseFlag(args,'title','');
  const decision=parseFlag(args,'decision','');
  if(!title || !decision) throw new Error('title e decision são obrigatórios');
  const s=getState(session);
  s.decisions.push({title,decision,at:nowISO()});
  saveState(session,s);
  console.log(JSON.stringify({ok:true,action:'state.add-decision',count:s.decisions.length},null,2));
}

function cmdValidate(args){
  const session=args[0];
  if(!session) throw new Error('uso: validate <session> --phase=N');
  const phase=Number(parseFlag(args,'phase','0'));
  const s=getState(session);
  const p=s.phases.find(x=>x.phase===phase);
  if(!p) throw new Error('phase inválida');
  const validations={
    1:['requirements-analysis.md'],
    2:['agents/'],
    3:['tasks/'],
    4:['workflows/','squad.yaml'],
    5:['optimization-report.md'],
    6:['validation-report.md'],
    7:['README.md'],
    8:['deploy-report.md'],
    9:['publish-report.md']
  };
  const req=validations[phase]||[];
  const dir=sessionDir(session);
  const missing=[];
  for(const r of req){
    const pth=path.join(dir,r);
    if(!fs.existsSync(pth)) missing.push(r);
  }
  const pass=missing.length===0;
  console.log(JSON.stringify({ok:true,action:'validate',phase,pass,missing},null,2));
}

function copyDir(src,dst){
  ensureDir(dst);
  for(const ent of fs.readdirSync(src,{withFileTypes:true})){
    if(ent.name === 'snapshots') continue; // evita recursão infinita ao criar snapshot
    const a=path.join(src,ent.name), b=path.join(dst,ent.name);
    if(ent.isDirectory()) copyDir(a,b);
    else if(ent.isFile()) fs.copyFileSync(a,b);
  }
}

function cmdSnapshot(args){
  const session=args[0];
  if(!session) throw new Error('uso: snapshot <session>');
  const src=sessionDir(session);
  if(!fs.existsSync(src)) throw new Error('sessão inexistente');
  const stamp=new Date().toISOString().replace(/[:.]/g,'-');
  const dst=path.join(src,'snapshots',stamp);
  ensureDir(path.dirname(dst));
  copyDir(src,dst);
  console.log(JSON.stringify({ok:true,action:'snapshot',path:dst},null,2));
}

function cmdReportFinal(args){
  const session=args[0];
  if(!session) throw new Error('uso: report final <session> [--target=...] [--marketplace=...]');
  const target=parseFlag(args,'target','N/A');
  const marketplace=parseFlag(args,'marketplace','squads.sh');
  const s=getState(session);
  const completed=s.phases.filter(p=>p.status==='completed').length;
  const approved=s.phases.filter(p=>p.gate==='approved').length;
  const rejected=s.phases.filter(p=>p.gate==='rejected').length;
  const readiness = (completed===9 && approved>=9 && rejected===0) ? 'READY_TO_PUBLISH' : 'NEEDS_REVIEW';
  const pct=Math.round((completed/9)*100);

  const lines=[];
  lines.push(`# Final Publish Report — ${s.session}`);
  lines.push('');
  lines.push(`- Generated at: ${nowISO()}`);
  lines.push(`- Target project: ${target}`);
  lines.push(`- Marketplace: ${marketplace}`);
  lines.push(`- Readiness: **${readiness}**`);
  lines.push(`- Progress: ${completed}/9 (${pct}%)`);
  lines.push(`- Gates approved: ${approved}`);
  lines.push(`- Gates rejected: ${rejected}`);
  lines.push('');
  lines.push('## Phase Summary');
  lines.push('| Phase | Status | Gate | Completed At | Notes |');
  lines.push('|------:|--------|------|--------------|-------|');
  for(const ph of s.phases){
    lines.push(`| ${ph.phase} | ${ph.status} | ${ph.gate||'-'} | ${ph.completed_at||'-'} | ${(ph.notes||'').replace(/\|/g,'/')} |`);
  }
  lines.push('');
  lines.push('## Decisions');
  if(!s.decisions.length) lines.push('- (none)');
  for(const d of s.decisions){ lines.push(`- ${d.title}: ${d.decision} (${d.at})`); }
  lines.push('');
  lines.push('## Artifact Counters');
  for(const [k,v] of Object.entries(s.artifacts||{})) lines.push(`- ${k}: ${v}`);

  const out=path.join(sessionDir(session),'FINAL-PUBLISH-REPORT.md');
  fs.writeFileSync(out, lines.join('\n'),'utf8');
  console.log(JSON.stringify({ok:true,action:'report.final',readiness,output:out,completed,approved,rejected},null,2));
}

function usage(){
  const txt = `Uso:\n  squad-tools.cjs init <session> [--preset=padrao] [--objective=...]\n  squad-tools.cjs resume <session>\n  squad-tools.cjs get <session>\n  squad-tools.cjs validate <session> --phase=N\n  squad-tools.cjs snapshot <session>\n  squad-tools.cjs report final <session> [--target=...] [--marketplace=...]\n  squad-tools.cjs state get <session>\n  squad-tools.cjs state advance <session> --phase=N [--notes=...] [--auto-gate=true|false]\n  squad-tools.cjs state gate <session> --phase=N --result=approved|rejected [--reviewer=...]\n  squad-tools.cjs state add-decision <session> --title=... --decision=...\n`; 
  console.log(txt);
}

function main(){
  try{
    const args=process.argv.slice(2);
    if(!args.length) return usage();
    const [cmd, sub, ...rest]=args;
    if(cmd==='init') return cmdInit([sub,...rest]);
    if(cmd==='resume') return cmdResume([sub,...rest]);
    if(cmd==='get') return cmdGet([sub,...rest]);
    if(cmd==='validate') return cmdValidate([sub,...rest]);
    if(cmd==='snapshot') return cmdSnapshot([sub,...rest]);
    if(cmd==='report'){
      if(sub==='final') return cmdReportFinal(rest);
      throw new Error('report subcommand inválido');
    }
    if(cmd==='state'){
      if(sub==='get') return cmdStateGet(rest);
      if(sub==='advance') return cmdStateAdvance(rest);
      if(sub==='gate') return cmdStateGate(rest);
      if(sub==='add-decision') return cmdStateAddDecision(rest);
      throw new Error('state subcommand inválido');
    }
    return usage();
  }catch(e){
    console.error(JSON.stringify({ok:false,error:String(e.message||e)},null,2));
    process.exit(1);
  }
}
main();
