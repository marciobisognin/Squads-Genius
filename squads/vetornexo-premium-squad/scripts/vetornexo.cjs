#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
function arg(name, def=null){ const i=process.argv.indexOf(name); return i>=0 && process.argv[i+1] ? process.argv[i+1] : def; }
function ensure(p){ fs.mkdirSync(p,{recursive:true}); }
function readJson(p){ return JSON.parse(fs.readFileSync(p,'utf8')); }
function footer(){ return 'Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.'; }
const blocks = [
 ['Fundação estratégica',['Branding','Copywriting','Email Marketing','Social Media Marketing','Inbound Marketing','Omnichannel','Afiliados','Personalização','Co-Marketing','Demand Generation']],
 ['Medição e controle',['CTR','CAC','LTV','ROAS','Engagement per Post','NPS','Conversion Rate','Average Order Value','CPM','ARPU']],
 ['Desenho do funil',['Top of Funnel','Middle of Funnel','Bottom of Funnel','A/B Testing','User Experience','Call to Action','Lead Scoring','Marketing Qualified Lead','Sales Qualified Lead','Landing Page']],
 ['Psicologia e persuasão',['FOMO','Urgência','Escassez','Prova Social','Neuromarketing','Pain & Solution','Cores e Emoções','Heurísticas Cognitivas','Framing Effect','Autoridade']],
 ['Aquisição de tráfego e performance',['Pay Per Click','Social Media Marketing','SEO','SEM','Video Marketing','Remarketing','Programmatic Ads','Tráfego Orgânico','Google Trends','CRM']],
 ['Tecnologia, IA e novas tendências',['Generative AI','Prompt Engineering','Realidade Virtual','Realidade Aumentada','AI Agents','Metaverso','Customer Experience','UX Writing','Human-in-the-Loop','Programmatic']],
 ['Publicidade e mídia paga',['Facebook Ads','Google Ads','TikTok Ads','YouTube Ads','LinkedIn Ads','Twitter Ads','Pinterest Ads','Display Ads','Native Ads','Pay Per Lead']],
 ['Marketing de conteúdo',['Blogging','Video Blog','Podcasts','Whitepapers','Ebooks','Newsletters','Instagram Content','Twitter Content','YouTube Content','Microcontent']],
 ['Automação, dados e personalização',['Chatbots','Dynamic Remarketing','Lookalike Audiences','API Marketing','Machine Learning','Natural Language Processing','Predictive Segmentation','Customer Data Platforms','Conversational Marketing','Behavioral Targeting']],
 ['Influência e afiliados',['Influencer Marketing','Microinfluenciadores','Macroinfluenciadores','Plataformas de Monetização','Affiliate Networks','Sponsored Content','Parcerias Estratégicas','Revenue Sharing','Brand Advocacy','Assessoria de Imprensa']],
 ['Customer Success e relacionamento',['Customer Success','Client Satisfaction','Suporte ao Cliente','Reviews e Depoimentos','Feedback Loop','Corporate Social Responsibility','Net Promoter Score','Programa de Fidelidade','Comunidade','Retenção de Clientes']],
 ['Vendas e conversão',['Sales Conversion','Upsell','Cross-Sell','Lead Generation','Nurturing','Rebuttal Techniques','Oferta Irresistível','Closing the Deal']]
];
function generate(){
 const input=arg('--input','examples/demo-brief.json'); const out=arg('--output','outputs/demo'); ensure(out);
 const b=readJson(input);
 const title = `# Solução implementada — ${b.nome_operacao || 'Operação de Marketing'}\n\n`;
 let md = title + `## Objetivo\n${b.objetivo}\n\n## Oferta\n${b.oferta}\n\n## Público\n${b.publico}\n\n## Arquitetura de execução por blocos\n`;
 blocks.forEach((bl,idx)=>{ md += `\n### ${idx+1}. ${bl[0]}\n`; bl[1].forEach(x=>{ md += `- ${x}: ação definida, métrica associada e próximo passo operacional.\n`;}); });
 md += `\n## Rota dos agentes\n1. briefing-intake → briefing operacional.\n2. visual-cartographer → mapa estrutural.\n3. ocr-semantics → inventário semântico.\n4. problem-framer → problema reduzido.\n5. solution-architect → arquitetura.\n6. builder-executor → pacote implementado.\n7. quality-sentinel → validação final.\n\n## Próximo passo\nExecutar o plano de 30 dias, revisar métricas semanalmente e priorizar otimizações por impacto em conversão e receita.\n\n${footer()}\n`;
 fs.writeFileSync(path.join(out,'SOLUCAO_IMPLEMENTADA.md'), md);
 fs.writeFileSync(path.join(out,'DASHBOARD_METRICAS.md'), `# Dashboard de métricas\n\n- CTR: qualidade de anúncio/chamada.\n- CAC: custo de aquisição.\n- LTV: valor vitalício.\n- ROAS: retorno de mídia.\n- Engagement per Post: resposta ao conteúdo.\n- NPS: satisfação/indicação.\n- Conversion Rate: eficiência do funil.\n- AOV: ticket médio.\n- CPM: custo de alcance.\n- ARPU: receita média por usuário.\n\n${footer()}\n`);
 fs.writeFileSync(path.join(out,'BACKLOG_IMPLEMENTACAO.md'), `# Backlog de implementação\n\n## Prioridade alta\n- Definir oferta irresistível e landing page.\n- Instalar CRM, pixel/eventos e dashboard.\n- Criar sequência de nutrição e follow-up.\n\n## Prioridade média\n- Testes A/B de CTA, promessa e criativos.\n- Remarketing e lookalike audiences.\n- Conteúdo TOFU/MOFU/BOFU.\n\n## Prioridade baixa\n- Parcerias, afiliados e comunidade.\n- Programas de fidelidade e advocacy.\n\n${footer()}\n`);
 fs.writeFileSync(path.join(out,'PLANO_30_DIAS.md'), `# Plano de 30 dias\n\n- Dias 1-7: briefing, branding, copy, oferta, métricas e funil mínimo.\n- Dias 8-14: landing page, conteúdo, CRM, email e campanhas iniciais.\n- Dias 15-21: mídia paga, remarketing, automação e testes A/B.\n- Dias 22-30: otimização por métricas, vendas, retenção e relatório executivo.\n\n${footer()}\n`);
 fs.writeFileSync(path.join(out,'FUNIL_E_CAMPANHAS.md'), `# Funil e campanhas\n\n## TOFU\nConteúdo educativo, vídeo curto, SEO, social e anúncios de alcance.\n\n## MOFU\nLead magnet, newsletter, prova social, comparação, estudo de caso e nutrição.\n\n## BOFU\nOferta, urgência ética, call to action, diagnóstico, fechamento, upsell e cross-sell.\n\n${footer()}\n`);
 console.log(JSON.stringify({ok:true, output:out, files:fs.readdirSync(out)}, null, 2));
}
function validate(){ const out=arg('--output','outputs/demo'); const req=['SOLUCAO_IMPLEMENTADA.md','DASHBOARD_METRICAS.md','BACKLOG_IMPLEMENTACAO.md','PLANO_30_DIAS.md','FUNIL_E_CAMPANHAS.md']; const missing=req.filter(f=>!fs.existsSync(path.join(out,f))); if(missing.length){ console.error(JSON.stringify({ok:false,missing},null,2)); process.exit(2);} const solution=fs.readFileSync(path.join(out,'SOLUCAO_IMPLEMENTADA.md'),'utf8'); const absent=blocks.map(b=>b[0]).filter(x=>!solution.includes(x)); if(absent.length){ console.error(JSON.stringify({ok:false,absent},null,2)); process.exit(3);} console.log(JSON.stringify({ok:true, checked:req.length, blocks:blocks.length},null,2)); }
const cmd=process.argv[2]; if(cmd==='generate') generate(); else if(cmd==='validate') validate(); else { console.log('Uso: node scripts/vetornexo.cjs generate --input examples/demo-brief.json --output outputs/demo | validate --output outputs/demo'); }
