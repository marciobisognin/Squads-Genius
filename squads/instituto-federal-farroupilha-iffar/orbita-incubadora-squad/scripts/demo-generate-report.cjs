#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
function arg(name, fallback){
  const idx = process.argv.indexOf(name);
  return idx >= 0 && process.argv[idx+1] ? process.argv[idx+1] : fallback;
}
const input = arg('--input', 'examples/demo-incubadora.json');
const output = arg('--output', 'validation/demo-relatorio-executivo.md');
const data = JSON.parse(fs.readFileSync(input, 'utf8'));
const md = `# Relatório Executivo — Órbita Incubadora Squad

## Incubadora
${data.incubadora}

## Empreendimento analisado
${data.empreendimento}

## Problema declarado
${data.problema}

## Estágio
${data.estagio}

## TRL estimado
${data.trl}

## Hipóteses críticas
${data.hipoteses.map((h,i)=>`${i+1}. ${h}`).join('\n')}

## Indicadores iniciais recomendados
${data.indicadores.map(i=>`- ${i}`).join('\n')}

## Próxima decisão recomendada
Executar entrevistas de descoberta, registrar evidências e submeter o empreendimento ao primeiro gate de validação antes de avançar para desenvolvimento pleno.

## Ressalva
Este relatório é uma demonstração operacional do squad. Deve ser adaptado com evidências reais e revisão institucional.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
`;
fs.mkdirSync(path.dirname(output), {recursive:true});
fs.writeFileSync(output, md);
console.log(JSON.stringify({ok:true, output}, null, 2));
