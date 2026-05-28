#!/usr/bin/env python3
from pathlib import Path
import datetime
root=Path(__file__).resolve().parents[1]; out=root/'output'; out.mkdir(exist_ok=True)
today=datetime.date.today().isoformat()
lines=[f'# Briefing Matinal — {today}', '', '## Prioridades', '', '- Revisar tarefas críticas.', '- Identificar reuniões do dia.', '- Selecionar 1 foco profundo.', '', '## Radar', '', '- Inserir notícias/fonte autorizada.', '- Inserir oportunidades relevantes.', '', '## Recomendações', '', '- Resolver primeiro a tarefa com maior impacto e menor dependência externa.', '- Validar decisões sensíveis com especialista humano.', '', 'Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.']
path=out/f'morning-briefing-{today}.md'; path.write_text('\n'.join(lines), encoding='utf-8')
print(path)
