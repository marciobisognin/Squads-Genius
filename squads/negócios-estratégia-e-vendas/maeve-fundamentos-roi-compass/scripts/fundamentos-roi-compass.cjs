#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
function args(argv){ const o={}; for(let i=2;i<argv.length;i++){ const a=argv[i]; if(a.startsWith('--')){ if(a.includes('=')){ const [k,...rest]=a.slice(2).split('='); o[k]=rest.join('='); } else { o[a.slice(2)] = argv[i+1] && !argv[i+1].startsWith('--') ? argv[++i] : true; } } } return o; }
const a = args(process.argv);
const objetivo = a.objetivo || 'não informado';
const recurso = a.recurso || 'recurso não informado';
const basico = (a.basico || 'parcial').toLowerCase();
const lacunas = a.lacunas || 'não informadas';
let decisao = 'AVALIAR COM CAUTELA';
let risco = 'médio';
let acao = 'Rodar um ciclo curto de prática antes de investir pesado.';
if(['ausente','não iniciado','nao iniciado','fraco'].some(x=>basico.includes(x))){ decisao='NÃO COMPRAR AINDA / CONSOLIDAR BÁSICO'; risco='alto'; acao='Definir básico mínimo, pedir para IA ensinar e praticar 7 dias antes de novo investimento.'; }
else if(['consistente','feito','dominado'].some(x=>basico.includes(x))){ decisao='PODE ACELERAR, SE HOUVER COMPROMISSO DE IMPLEMENTAÇÃO'; risco='baixo a médio'; acao='Comprar/usar apenas com plano de aplicação, métrica e entrega concreta.'; }
const md = `# Diagnóstico — Maeve Fundamentos ROI Compass\n\n## Objetivo\n${objetivo}\n\n## Recurso avaliado\n${recurso}\n\n## Básico atual\n${basico}\n\n## Lacunas declaradas\n${lacunas}\n\n## Perguntas dos áudios\n- O que eu quero?\n- Para onde estou indo?\n- O que preciso dominar?\n- O que estou fazendo para isso?\n- Já faço o básico bem feito?\n- Isso acelera clareza ou acelera caos?\n\n## Decisão\n**${decisao}**\n\n## Risco de acelerar caos/distração\n${risco}\n\n## Próxima ação\n${acao}\n\n## Papel recomendado da IA\n- Explicitar lacunas.\n- Ensinar fundamentos que faltam.\n- Gerar contexto antes de executar.\n- Criar plano prático proporcional ao momento.\n\n## Condição de ROI\nO recurso só tende a gerar ROI se houver atitude, comprometimento, prática e implementação real.\n\nLicença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.\n`;
if(a.out){ fs.mkdirSync(path.dirname(path.resolve(a.out)), {recursive:true}); fs.writeFileSync(a.out, md); }
console.log(JSON.stringify({ok:true, decisao, risco, out:a.out||null}, null, 2));
