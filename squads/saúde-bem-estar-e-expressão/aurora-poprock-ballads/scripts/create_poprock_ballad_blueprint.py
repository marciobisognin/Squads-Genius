#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

FORBIDDEN = ['Deus', 'Senhor', 'oração', 'orar', 'graça', 'fé', 'louvor', 'worship', 'gospel', 'culto']

def build(args):
    tema = args.tema or 'duas pessoas que se reencontram depois de anos'
    emocao = args.emocao or 'saudade, desejo contido e reencontro'
    simbolo = args.simbolo or 'olhos'
    voz = args.voz or 'voz masculina grave/média, quente e expressiva'
    backing = args.backing or 'backing vocals discretos no refrão final'
    title = args.titulo or 'Quando Teus Olhos Me Chamam'
    instruments = 'piano/teclado emocional, guitarras limpas e arpejadas, baixo redondo, bateria lenta com viradas crescentes, pads nostálgicos e cordas discretas no clímax'
    tags = 'romantic-rock-ballad,emotional-pop-rock,portuguese,male-warm-vocal,piano,clean-electric-guitar,bass,soft-drums,pads,slow-build,nineties-ballad-inspired,nostalgic,heartfelt,anthemic-chorus'
    lyrics = f'''[Intro]
Piano e guitarra limpa, clima nostálgico.

[Verso 1]
Te vi chegando no fim da rua,
como se o tempo voltasse atrás.
A mesma luz atravessou a chuva,
e eu fiquei sem saber o que falar.

Tanta coisa ficou pelo caminho,
tantas frases que eu guardei em mim.
Mas teu silêncio encostou no meu peito
e disse tudo sem chegar ao fim.

[Pré-Refrão]
Se ainda existe alguma chance
entre o que fomos e o que restou,
deixa a noite nos dizer baixinho
que nada terminou.

[Refrão]
Quando teus {simbolo} me chamam,
eu esqueço a distância entre nós.
Meu coração perde a calma,
mas encontra de novo a tua voz.

Quando teus {simbolo} me chamam,
o mundo inteiro fica pra depois.
Se o amor ainda nos alcança,
que ele fale por nós dois.

[Verso 2]
Tem lembranças nas luzes da cidade,
tem promessas que ninguém rasgou.
Eu tentei seguir sem tua metade,
mas nenhuma estrada me levou.

Hoje a vida parece suspensa,
como um filme antes do final.
Tua mão quase toca a minha,
e esse quase já me faz sinal.

[Ponte]
Não diz que é tarde,
não diz que passou.
Tem fogo escondido
onde a cinza ficou.

Se a noite permitir,
se teu medo deixar,
eu fico aqui
até o sol nos encontrar.

[Refrão Final]
Quando teus {simbolo} me chamam,
eu esqueço a distância entre nós.
Meu coração perde a calma,
mas encontra de novo a tua voz.

Quando teus {simbolo} me chamam,
o mundo inteiro fica pra depois.
Se o amor ainda nos alcança,
que ele fale por nós dois.

[Outro]
Piano, guitarra limpa e voz suave.
Que ele fale por nós dois.'''
    prompt = f'''Canção original em português sobre {tema}. Emoção dominante: {emocao}. Atmosfera de balada rock/pop romântica e emocional, inspirada apenas em princípios gerais de baladas dos anos 80/90: {voz}, versos íntimos, refrão amplo e memorável, {instruments}. {backing}. Construção gradual até um clímax vocal no refrão final. Não copiar letra, melodia, progressão reconhecível, timbre específico ou interpretação de artistas existentes. Manter estritamente no território pop rock romântico e balada emocional.'''
    out = f'''# {title}

## Território musical
Pop rock romântico / rock balada / balada emocional em português.

## Tema interpretado
{tema}

## Arco romântico
Encontro inesperado -> memória afetiva -> tensão emocional -> desejo contido -> refrão de entrega romântica -> clímax final -> permanência.

## Letra
{lyrics}

## Voz
{voz}; versos íntimos e controlados, pré-refrão em subida, refrão amplo, sustentado e emocional.

## Backing vocals
{backing}; discretos no primeiro refrão, mais abertos no refrão final, sem roubar a voz principal.

## Instrumentos
{instruments}

## Tags para IA musical
```text
{tags}
```

## Prompt musical
```text
{prompt}
```

## Checklist de originalidade e aderência
- [x] Foco em pop rock / rock romântico / balada emocional
- [x] Foco exclusivo em romance, saudade, reencontro e intensidade afetiva
- [x] Refrão amplo e memorável
- [x] Voz masculina quente e expressiva
- [x] Piano/teclado, guitarras limpas, baixo, bateria lenta e pads nostálgicos
- [x] Instrução explícita para não copiar letra, melodia, timbre ou artista

Licença: MIT. Criado por Marcio Bisognin. Instagram: @marciobisognin.
'''
    for word in FORBIDDEN:
        if re.search(r'(?<![A-Za-zÀ-ÿ])' + re.escape(word.lower()) + r'(?![A-Za-zÀ-ÿ])', out.lower()):
            raise SystemExit(f'Forbidden religious term leaked: {word}')
    od = Path(args.output or 'output')
    od.mkdir(parents=True, exist_ok=True)
    path = od / 'poprock_ballad_blueprint.md'
    path.write_text(out, encoding='utf-8')
    print(path.resolve())

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--tema')
    ap.add_argument('--emocao')
    ap.add_argument('--simbolo')
    ap.add_argument('--voz')
    ap.add_argument('--backing')
    ap.add_argument('--titulo')
    ap.add_argument('--output')
    build(ap.parse_args())
