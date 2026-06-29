#!/usr/bin/env python3
import argparse, datetime
from pathlib import Path

FOOTER = "Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin."
WORDS = {
    "M": ["mala", "mapa", "meia", "mimo", "mula", "mamãe"],
    "F": ["faca", "foca", "fila", "fada", "fubá"],
    "V": ["vaso", "vela", "vida", "vovó"],
    "S": ["sapo", "sino", "sopa", "suco"],
    "L": ["lua", "lata", "lobo", "leão"],
    "N": ["navio", "nove", "nada", "ninho"],
}

def write(path, text):
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')
    print(str(p))

def diagnostico(args):
    data=datetime.date.today().isoformat()
    text=f"""# Diagnóstico rápido — {args.nome}

Idade: {args.idade}
Data: {data}

## Trava informada
{args.trava}

## Hipótese pedagógica inicial
A descrição sugere verificar se a criança já domina a ponte som-letra e se consegue passar de encontros vocálicos para consoante prolongável + vogal.

## Teste de 3 minutos
1. Peça o som de A, E, I, O, U.
2. Peça a leitura de AI, OI, EU, AU, EI.
3. Modele /mmm/ + /a/ = MA.
4. Teste MA em MALA ou MAPA.

## Próximo foco recomendado
Começar por sons funcionais e junção gradual, sem exigir repetição mecânica longa.

## Sinal de progresso
A criança junta um som novo com menos ajuda do adulto.

{FOOTER}
"""
    write(args.saida, text)

def sessao(args):
    text=f"""# Sessão de 15 minutos — {args.foco}

Nível: {args.nivel}

## Minutos 1–2 — Revisão rápida
Revisar vogais e encontros vocálicos com cartões: AI, OI, EU, AU, EI.

## Minutos 3–5 — Foco do dia
Apresentar **{args.foco}** usando som funcional antes do nome da letra.

## Minutos 6–8 — Prática guiada
Alongar a consoante quando possível e aproximar da vogal: “mmmm... a... MA”.

## Minutos 9–11 — Palavra com sentido
Usar palavras curtas relacionadas ao foco. Se o foco envolver M: mala, mapa, mimo, mamãe.

## Minutos 12–15 — Escrita lúdica
Traçar a letra, dizer o som, montar uma sílaba e circular a sílaba dentro de uma palavra.

## Elogio específico
“Você conseguiu juntar os sons. Isso é ler, não adivinhar.”

{FOOTER}
"""
    write(args.saida, text)

def semana(args):
    text=f"""# Trilha semanal — {args.nome}

Foco: {args.foco}

## Segunda
Vogais e encontros vocálicos com gesto e expressão: AI, OI, EU, AU, EI.

## Terça
Consoante prolongável + vogais.

## Quarta
Sílabas abertas e palavras de duas sílabas.

## Quinta
Rastreamento da letra + som + sílaba.

## Sexta
Revisão lúdica e leitura de frases curtas.

## Registro de acompanhamento
- O que leu com ajuda:
- O que leu sozinho(a):
- Onde ainda trava:
- Próximo foco:

{FOOTER}
"""
    write(args.saida, text)

def main():
    ap=argparse.ArgumentParser(description='Maeve Lumen Leitura CLI')
    sub=ap.add_subparsers(dest='cmd', required=True)
    d=sub.add_parser('diagnostico'); d.add_argument('--nome', required=True); d.add_argument('--idade', required=True); d.add_argument('--trava', required=True); d.add_argument('--saida', required=True); d.set_defaults(func=diagnostico)
    s=sub.add_parser('sessao'); s.add_argument('--foco', required=True); s.add_argument('--nivel', default='inicial'); s.add_argument('--saida', required=True); s.set_defaults(func=sessao)
    w=sub.add_parser('semana'); w.add_argument('--nome', required=True); w.add_argument('--foco', required=True); w.add_argument('--saida', required=True); w.set_defaults(func=semana)
    args=ap.parse_args(); args.func(args)
if __name__ == '__main__': main()
