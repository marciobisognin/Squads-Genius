#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

def make_package(theme):
    hook = "ainda há luz no que restou"
    lyrics = f"""[Intro - piano íntimo]

[Verso 1 - voz baixa, vulnerável]
Hoje eu sentei no silêncio da sala
E ouvi meu peito tentando falar
Tem despedida que fecha a porta
Mas deixa uma fresta pro sol entrar

[Pré-Refrão - crescendo]
Se eu tive que perder pra compreender
Que amor também é deixar seguir
Eu junto os pedaços do que ficou
E aprendo de novo a existir

[Refrão - voz potente, banda aberta]
Porque {hook}
Mesmo quando a noite insiste em ficar
Se a dor escreveu meu nome no chão
A esperança me ensina a levantar
Porque {hook}
No fim da estrada eu volto a respirar
O que foi amor não vira cinza
Vira força pra recomeçar

[Verso 2 - piano + guitarra limpa]
Guardei promessas numa caixa antiga
Não pra viver preso ao que passou
Mas pra lembrar que até a ferida
Pode virar caminho se curou

[Ponte - queda dinâmica, quase sussurrado]
E se a saudade vier sem pedir licença
Eu não vou lutar pra esconder
Vou transformar ausência em presença
E cantar até amanhecer

[Refrão Final - belting, harmonias, bateria cheia]
Porque {hook}
Mesmo quando a noite insiste em ficar
Se a dor escreveu meu nome no chão
A esperança me ensina a levantar
Porque {hook}
No fim da estrada eu volto a respirar
O que foi amor não vira cinza
Vira força pra recomeçar

[Outro - piano solo, voz quebrada]
Ainda há luz...
Ainda há luz no que restou.
"""
    style = "Balada pop-rock brasileira cinematográfica, 72-82 BPM, tom menor com resolução esperançosa, começa em piano íntimo e voz vulnerável, cresce com guitarras abertas, baixo sustentado, bateria de arena, pads/cordas discretas, refrão expansivo e catártico, final reduzido em piano."
    voice = "Voz masculina tenor/barítono alto, levemente rouca, emocional e direta; versos em registro íntimo, pré-refrão com tensão crescente, refrão em belting controlado, vibrato em notas longas, harmonias no refrão final."
    instruments = "Piano emocional, guitarra limpa com delay, guitarra distorcida aberta no refrão, baixo sustentado, bateria com tom/snare amplos, pratos no clímax, pads/cordas cinematográficas discretas, reverb de arena no vocal."
    prompt = f"{style} {voice} Tema: {theme}. Letra original em português, narrativa de perda, maturidade e recomeço. Dinâmica whisper-to-roar-to-whisper. Não copiar artistas, músicas, melodias ou letras existentes."
    return f"""# Pacote de Música Original — {theme}

## Conceito
Canção sobre {theme}, com arco de dor, aceitação e recomeço. O impacto vem do contraste entre vulnerabilidade íntima e refrão catártico.

## Letra

{lyrics}

## Estilo musical
{style}

## Voz
{voice}

## Instrumentos
{instruments}

## Prompt para IA musical
{prompt}

## Checklist de originalidade
- [x] Letra original, sem reprodução da referência.
- [x] Gancho próprio: “{hook}”.
- [x] Referência usada apenas como DNA emocional abstrato.
- [x] Sem nome de artista no prompt final.
- [x] Estrutura pronta para IA musical.

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
"""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--theme', default='recomeçar depois de uma perda')
    ap.add_argument('--output', default='generated/song-package.md')
    args=ap.parse_args()
    out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(make_package(args.theme))
    print(out)
if __name__=='__main__': main()
