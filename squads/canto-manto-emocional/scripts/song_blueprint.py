#!/usr/bin/env python3
import argparse, textwrap, json

TAGS = "christian,worship,folk-pop,acoustic-guitar,piano,cinematic,emotional,male-vocal,portuguese,hopeful,devotional,soft-drums,strings,pads"

def main():
    ap = argparse.ArgumentParser(description="Gera blueprint para música devocional emocional original.")
    ap.add_argument('--tema', required=True)
    ap.add_argument('--emocao', default='consolo')
    ap.add_argument('--simbolo', default='colo')
    ap.add_argument('--voz', default='masculina íntima, grave, calorosa')
    args = ap.parse_args()
    blueprint = {
        'sinopse_emocional': f"Uma canção sobre {args.tema}, conduzida por {args.emocao}, usando o símbolo '{args.simbolo}' como imagem central de acolhimento.",
        'estrutura': ['Intro falado/imagem', 'Verso 1 cotidiano', 'Pré-refrão de virada', 'Refrão memorável', 'Verso 2 consequência', 'Ponte oração', 'Refrão final catártico', 'Outro simples'],
        'voz': args.voz + '; interpretação próxima, vulnerável, sem imitar artista específico.',
        'instrumentos': ['violão orgânico', 'piano suave', 'pads ambientes', 'baixo discreto', 'bateria/cajón leve', 'cordas no clímax', 'backing vocals final'],
        'tags_heartmula': TAGS,
        'prompt_geracao': f"Canção original em português sobre {args.tema}. Estilo worship/folk-pop acústico-cinemático, emoção de {args.emocao}, símbolo central {args.simbolo}, voz {args.voz}. Crescimento gradual, refrão curto e memorável, final acolhedor. Não imitar artistas, não copiar melodias ou letras existentes.",
        'checklist_originalidade': ['não usar letra de referência', 'não citar artista como clone vocal', 'trocar imagens muito próximas', 'refrão novo', 'melodia nova', 'arranjo próprio']
    }
    print(json.dumps(blueprint, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
