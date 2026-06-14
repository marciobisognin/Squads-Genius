# PRD — Manim Science Studio Squad

PRD — Manim Science Studio Squad

manim-science-studio-squad · v1.0 · Produto Interno · PT-BR

Sumário Executivo

O Manim Science Studio Squad é um sistema multi-agente de automação editorial para produção de Reels educativos científicos em português brasileiro. O squad orquestra sete agentes especializados que, em pipeline sequencial com revisões paralelas, entregam um pacote de produção completo por vídeo: roteiro narrado, storyboard detalhado, código Manim renderizável, configuração de narração TTS com prosódia, revisão epistêmica, comandos FFmpeg de montagem final e calendário editorial estratégico. O objetivo primário é reduzir o tempo de produção de um Reel científico de alta qualidade de ~20 horas manuais para menos de 2 horas de operação humana supervisionada.

Contexto e Motivação

1.1 Problema

Criadores de conteúdo científico em PT-BR enfrentam três gargalos simultâneos:

Produção visual custosa: animações matemáticas e físicas de qualidade exigem domínio de Manim, Python e FFmpeg — habilidades raras na comunidade criativa brasileira.

Rigor epistêmico inconsistente: simplificações excessivas ou erros factuais destroem credibilidade em canais científicos.

Cadência editorial irregular: a falta de planejamento sistemático resulta em publicações espaçadas e perda de audiência.

1.2 Oportunidade

O mercado de vídeos científicos curtos em PT-BR (física, matemática, filosofia da ciência) está em crescimento acelerado. Canais como "Física e Afins", "Matemática Rio" e similares acumulam audiências de centenas de

milhares com produção ainda majoritariamente manual. Um sistema que automatize o pipeline técnico preservando rigor científico tem potencial de 10x a cadência de publicação sem degradar qualidade.

1.3 Decisão de Construir

A solução foi escolhida em detrimento de ferramentas genéricas de geração de vídeo (Synthesia, HeyGen) porque:

Manim produz animações matemáticas que nenhum gerador de vídeo comercial replica.

O controle fino de prosódia para narração científica PT-BR requer pipelines TTS customizados.

A revisão epistêmica especializada (física/filosofia) exige agentes com bases de conhecimento científico verificável.

Objetivos e Métricas de Sucesso

2.1 Objetivos de Negócio

2.2 Critérios de Sucesso do Produto

(Definition of Done)

Um ciclo de produção é considerado concluído quando o squad entrega, para cada vídeo:

�Script PT-BR validado e aprovado pelo Revisor Epistêmico

�Storyboard cena-a-cena com anotações de câmera e timing

�Código Manim (scene.py) executável sem erros em Manim CE 0.18+

�Arquivo de narração TTS gerado com marcações de prosódia SSML

�Relatório de revisão epistêmica com fontes verificadas

�Sequência de comandos FFmpeg para montagem final

�Slot confirmado no calendário editorial

2.3 Métricas de Produto (KPIs Operacionais)

Latência de pipeline: tempo entre briefing de tópico e entrega do pacote completo ≤ 45 minutos

Taxa de aprovação na primeira revisão: % de pacotes aceitos sem solicitação de retrabalho ≥ 80%

Cobertura de revisão epistêmica: 100% das afirmações quantitativas e causais com fonte primária

Executabilidade do código Manim: 0% de erros de runtime na primeira execução

Escopo e Limites

3.1 Dentro do Escopo (v1.0)

Reels educativos de 30s a 90s em PT-BR

Tópicos de física clássica, física quântica, matemática pura/aplicada e filosofia da ciência

Animações Manim com fundo preto, paleta de cores científica padrão

Narração TTS via Edge-TTS (voz pt-BR-AntonioNeural ou pt-BR-FranciscaNeural)

Montagem final via FFmpeg (sobreposição de narração + música de fundo + legendas)

Calendário editorial para até 52 semanas (1

ano)

Exportação de pacote em formato ZIP estruturado

3.2 Fora do Escopo (v1.0)

Upload automático para Instagram/TikTok/YouTube Shorts (v2.0)

Personalização de avatar ou talking head

Animações 3D complexas (Blender/Three.js)

Idiomas além do PT-BR (v2.0: EN, ES)

A/B testing automatizado de thumbnails

3.3 Premissas

O operador humano fornece: (a) tópico científico, (b) nível de complexidade alvo (iniciante/intermediário/avançado), (c) duração desejada do Reel

Ambiente Python 3.11+ com Manim CE instalado está disponível no servidor de execução

FFmpeg 6.0+ instalado no servidor de renderização

Arquitetura Multi-Agente

4.1 Visão Geral do Pipeline

INPUT (Briefing do Operador)

│

▼

┌──────────────────┐

│ [A1] Roteirista │ ──► Script PT-BR (JSON estruturado)

│ Científico │

└──────────────────┘

│

▼

┌──────────────────┐

│ [A2] Diretor de │ ──► Storyboard (Markdown + timing)

│ Storyboard │

└──────────────────┘

│

┌────┴────┐

▼ ▼

┌────────┐ ┌────────────────┐

│ [A3] │ │ [A4] Diretor │

│ Codif. │ │ de Narração │

│ Manim │ │ (TTS/Prosódia) │

└───┬────┘ └───────┬────────┘

│ │

└────┬──────────┘

│

▼

┌──────────────────────┐

│ [A5] Revisor │ ──► Relatório de Revisão

│ Epistêmico │ (Aprovação ou Retrabalho)

└──────────────────────┘

│

┌────┴── [RETRABALHO → A1/A3]

▼

┌──────────────────┐

│ [A6] Editor │ ──► Comandos FFmpeg finais

│ FFmpeg │

└──────────────────┘

│

▼

┌──────────────────────────┐

│ [A7] Estrategista de │ ──► Slot no Calendário

│ Calendário Editorial │ + Recomendações SEO

└──────────────────────────┘

│

▼

OUTPUT (Pacote ZIP)

4.2 Modos de Operação

Especificação Detalhada dos Agentes

Agente A1 — Roteirista Científico

Identificador: scientific-scriptwriter

Responsabilidade primária: Produzir o roteiro narrativo do Reel em PT-BR, calibrado para o público-alvo e duração especificada, com precisão conceitual e linguagem acessível.

5.1.1 Entradas

5.1.2 Saídas

{

"script_id": "uuid-v4",

"topic": "string",

"complexity_level": "string",

"total_estimated_duration_sec": 75,

"word_count": 180,

"segments": [

{

"segment_id": "S01",

"type": "hook",

"text": "string (narração PT-BR)",

"duration_sec": 8,

"key_concepts": ["conceito_1", "conceito_2"],

"visual_cue": "descrição do que deve aparecer na tela"

}

],

"key_equations": ["LaTeX string"],

"references_suggested": ["autor, obra, ano"],

"production_notes": "string"

}

5.1.3 Estrutura de Segmentos Obrigatórios

Hook (5–10s): abertura com pergunta ou fato surpreendente

Contexto (10–15s): por que este conceito importa

Desenvolvimento (30–50s): explicação central com analogias

Momento Matemático (10–15s): equação/fórmula central animada

Síntese (5–10s): insight final e convite ao engajamento

5.1.4 Regras de Negócio

Nunca usar o termo "complexo" para descrever o tópico ao espectador

Toda afirmação quantitativa deve ser acompanhada de reference_tag para validação pelo A5

Densidade máxima: 2,5 palavras/segundo de narração

O hook deve ser formulado como pergunta ou afirmação que desafie intuição cotidiana

Jargão técnico: máximo 3 termos por minuto, cada um explicado imediatamente

5.1.5 Critérios de Qualidade

Coerência narrativa avaliada por score de fluxo lógico (A-B-C-D-E) ≥ 4/5

Correspondência entre visual_cue e capacidade do Manim validada pelo A3

Nenhum segmento com duração < 3s ou > 20s sem justificativa

Agente A2 — Diretor de Storyboard

Identificador: storyboard-director

Responsabilidade primária: Traduzir o roteiro em storyboard cena-a-cena com especificações visuais precisas para o A3 (código Manim) e para o A4 (sincronização de narração).

5.2.1 Entradas

Saída completa do A1 (script_id + JSON do script)

aspect_ratio: 9:16 (Reels, default) ou 16:9

visual_style: minimalista_científico (default) / colorido_didático / darkboard

5.2.2 Saídas

Storyboard: [SCRIPT_ID]

Duração total: Xs | Cenas: N | Estilo: [visual_style]

───

Cena 01 — Hook [00:00 – 00:08]

Tipo: Introdução

Narração sincronizada: "[texto exato do segmento S01]"

Elementos visuais:

Fundo: preto (#000000)

Texto central: "Por que o universo tem um limite de precisão?"

Animação: texto aparece letra por letra (Write)

Transição saída: FadeOut (0.5s)

Especificação Manim:

Classe: HookScene

Objetos: Text, Write, FadeOut

Câmera: estática

Timing relativo: t=0s aparece texto, t=6s fade out

Notas de direção: Fonte Fira Math Bold, tamanho 40pt, branco puro

5.2.3 Campos Obrigatórios por Cena

5.2.4 Regras de Storyboard

Máximo de 3 elementos visuais simultâneos por cena (lei de carga cognitiva)

Equações LaTeX devem usar MathTex, nunca Text com símbolos Unicode

Toda transição entre cenas deve ter duração explícita (mínimo 0.3s)

Cenas com duração > 15s devem ter no mínimo 2 animações distintas

A paleta de cores deve ser consistente ao longo de todo o storyboard

Agente A3 — Codificador Manim

Identificador: manim-coder

Responsabilidade primária: Converter o storyboard em código Python Manim CE funcional, organizado em cenas modulares, com documentação inline e capacidade de renderização imediata.

5.3.1 Entradas

Storyboard completo do A2

manim_version: 0.18.x (default) ou posterior especificado

render_quality: low_quality (dev) / medium_quality / high_quality (default: medium_quality)

output_format: mp4 (default) / gif / webm

5.3.2 Estrutura do Código Gerado

manim_scene_[SCRIPT_ID].py

Gerado por: Manim Science Studio Squad - Agente A3

Script ID: [uuid]

Tópico: [topic]

Gerado em: [ISO datetime]

from manim import *

from manim import config as manim_config

=== CONFIGURAÇÃO GLOBAL ===

manim_config.background_color = BLACK

MAIN_FONT = "Fira Math"

PRIMARY_COLOR = "#4FC3F7" # azul ciência

SECONDARY_COLOR = "#81C784" # verde complementar

ACCENT_COLOR = "#FFB74D" # laranja destaque

TEXT_COLOR = WHITE

=== CONSTANTES DE TIMING ===

HOOK_DURATION = 8

CONTEXT_DURATION = 12

... (por segmento)

=== FUNÇÕES UTILITÁRIAS ===

def make_title(text: str, scale: float = 1.0) -> Text:

"""Cria título padronizado com fonte e cor padrão do canal."""

return Text(text, font=MAIN_FONT, color=TEXT_COLOR).scale(scale)

def make_equation(latex: str) -> MathTex:

"""Cria equação LaTeX com estilo padrão."""

return MathTex(latex, color=PRIMARY_COLOR)

=== CENAS ===

class HookScene(Scene):

"""Cena 01 - Hook [00:00 - 00:08]

Narração: "[texto sincronizado]"

"""

def construct(self):

# Objeto 1: Texto principal

question = make_title(

"Por que o universo tem um limite de precisão?",

scale=0.8

)

# Animação sequencial com timing explícito

self.play(Write(question), run_time=3)

self.wait(3)

self.play(FadeOut(question), run_time=0.5)

self.wait(0.5)

class ContextScene(Scene):

"""Cena 02 - Contexto [00:08 - 00:20]"""

def construct(self):

pass # [implementação completa por cena]

=== COMPOSIÇÃO FINAL ===

class FullVideo(Scene):

"""Composição sequencial de todas as cenas para renderização única."""

def construct(self):

# Executa todas as subscenas em sequência

scenes = [HookScene, ContextScene] # lista completa

for SceneClass in scenes:

scene_instance = SceneClass()

scene_instance.construct()

5.3.3 Padrões de Código Obrigatórios

5.3.4 Comandos de Renderização Gerados

Renderização em qualidade de desenvolvimento (rápida)

manim -pql manim_scene_[ID].py FullVideo

Renderização em qualidade de produção

manim -pqh manim_scene_[ID].py FullVideo --format mp4

Renderização de cena específica para debug

manim -pql manim_scene_[ID].py HookScene

5.3.5 Restrições de Código

Proibido usar self.wait() com valores hardcoded não documentados

Toda MathTex deve ter color explícito

Tex e Text não devem ser misturados no mesmo

objeto composto

Animações de câmera somente via CameraFrame — nunca self.camera.move_to()

Versão mínima do Python: 3.11 (uso de match statements permitido)

Agente A4 — Diretor de Narração (Prosódia/TTS)

Identificador: narration-director

Responsabilidade primária: Produzir o arquivo de narração em PT-BR com prosódia otimizada para conteúdo científico, usando SSML para controle fino de ritmo, ênfase e pausas, e gerando o áudio via Edge-TTS.

5.4.1 Entradas

Script do A1 (segmentos com text e duration_sec)

voice_id: pt-BR-AntonioNeural (masculino, default) ou pt-BR-FranciscaNeural (feminino)

speech_rate: slow / medium (default) / fast

background_music: none / ambient_space / minimal_piano / electronic_subtle

5.4.2 SSML Gerado por Segmento

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"

xmlns:mstts="https://www.w3.org/2001/mstts"

xml:lang="pt-BR">

<!-- HOOK - 8 segundos -->

<voice name="pt-BR-AntonioNeural">

<!-- Pausa pré-hook: 0.5s de silêncio dramático -->

<break time="500ms"/>

<!-- Pergunta com ênfase ascendente -->

<prosody rate="medium" pitch="+2st" volume="loud">

Por que o universo tem

</prosody>

<break time="200ms"/>

<prosody rate="slow" pitch="+4st" volume="x-loud" emphasis="strong">

um limite de precisão?

</prosody>

<break time="1000ms"/>

</voice>

<!-- CONTEXTO - 12 segundos -->

<voice name="pt-BR-AntonioNeural">

<prosody rate="medium" pitch="0st">

Werner Heisenberg descobriu, em 1927, que

<emphasis level="moderate">nunca podemos saber</emphasis>

ao mesmo tempo, com precisão absoluta, a posição

<break time="150ms"/>

e a velocidade de uma partícula.

</prosody>

<break time="600ms"/>

</voice>

</speak>

5.4.3 Regras de Prosódia Científica

5.4.4 Comando de Geração de Áudio

Geração via Edge-TTS

edge-tts

--voice "pt-BR-AntonioNeural"

--file narration_[SCRIPT_ID].ssml

--write-media narration_[SCRIPT_ID].mp3

--write-subtitles narration_[SCRIPT_ID].vtt

Conversão para formato de produção

ffmpeg -i narration_[SCRIPT_ID].mp3

-ar 44100 -ac 2 -b:a 192k

narration_[SCRIPT_ID]final.aac

5.4.5 Metadados de Sincronização

O agente também produz um arquivo de timestamps sync[SCRIPT_ID].json:

{

"segments": [

{

"segment_id": "S01",

"audio_start_ms": 500,

"audio_end_ms": 8200,

"video_scene": "HookScene",

"sync_offset_ms": 0

}

]

}

Agente A5 — Revisor Epistêmico

Identificador: epistemic-reviewer

Responsabilidade primária: Verificar a precisão científica e filosófica de todas as afirmações do script, validar equações, confirmar atribuições históricas e emitir relatório de aprovação ou lista de correções obrigatórias.

5.5.1 Entradas

Script completo do A1

Código Manim do A3 (verificação de equações renderizadas)

domain_focus: lista de domínios para

verificação aprofundada

5.5.2 Taxonomia de Revisão

5.5.3 Checklist de Revisão Epistêmica

Física:

�Leis de conservação respeitadas nas afirmações

�Unidades SI corretas e consistentes

�Equações dimensionalmente coerentes

�Constantes físicas com valores atualizados (CODATA 2022)

�Distinção clara entre modelo e realidade

�Interpretações quânticas identificadas como interpretações, não fatos

Matemática:

�Provas ou derivações sem saltos lógicos não declarados

�Domínio de validade das equações explicitado

�Notação consistente com convenção internacional

Filosofia da Ciência:

�Distinção entre hipótese, teoria e lei científica

�Atribuições históricas verificadas (cientista, ano, publicação)

�Causalidade versus correlação distinguidas

�Falsificabilidade das afirmações avaliada

Geral:

�Nenhuma afirmação "é provado que..." sem referência

�Analogias identificadas como analogias, não como equivalências

�Linguagem de certeza calibrada ao consenso científico atual

5.5.4 Relatório de Saída

Relatório de Revisão Epistêmica

Script ID: [uuid]

Tópico: [topic]

Revisor: Agente A5 - Revisor Epistêmico

Data: [ISO datetime]

Veredicto: ✅ APROVADO | ⚠️ APROVADO COM RESSALVAS | ❌ REPROVADO

───

Achados Críticos (0)

Nenhum.

Achados Major (1)

Ref.: Segmento S03, linha 2

Afirmação original: "O gato de Schrödinger prova que partículas existem em dois estados ao mesmo tempo"

Problema: Confunde experimento mental com afirmação ontológica. Apresenta interpretação de Copenhague como fato universal.

Correção sugerida: "O gato de Schrödinger ilustra o paradoxo da superposição quântica — uma das interpretações mais debatidas da mecânica quântica"

Fonte: Schrödinger, E. (1935). Die gegenwärtige Situation in der Quantenmechanik.

Naturwissenschaften, 23(48).

Fontes Verificadas

Afirmação

Fonte Primária

Verificado

Princípio da Incerteza (1927)

Heisenberg, W. (1927), Z. Phys. 43, 172

✅

ΔxΔp ≥ ħ/2

Robertson (1929) generalização

✅

5.5.5 Fluxo de Retrabalho

A5 emite ❌ REPROVADO

│

├─► Achados CRÍTICOS → retorna ao A1 (reescrita de segmentos)

│ └─► A1 → A2 → A3 paralelo A4 → A5 (novo

ciclo)

│

└─► Achados MAJOR only → retorna ao A1 (correções pontuais)

└─► A1 (patch) → A5 (verificação rápida)

A5 emite ✅ APROVADO ou ⚠️ APROVADO COM RESSALVAS

└─► Segue para A6

SLA de retrabalho: máximo 2 ciclos de revisão por vídeo. No terceiro ciclo, escala para revisão humana.

Agente A6 — Editor FFmpeg

Identificador: ffmpeg-editor

Responsabilidade primária: Produzir a sequência completa e comentada de comandos FFmpeg para montar o vídeo final, integrando animação Manim, narração TTS, música de fundo, legendas e ajustes de cor/formato para publicação em Reels.

5.6.1 Entradas

Arquivo MP4 renderizado pelo Manim (video_[ID].mp4)

Arquivo de áudio de narração (narration_[ID]final.aac)

Arquivo VTT de legendas (narration[ID].vtt)

Arquivo de metadados de sincronização do A4 (sync_[ID].json)

output_format: reels_9x16 (default) / shorts_9x16 / standard_16x9

music_track: caminho do arquivo ou none

5.6.2 Script FFmpeg Gerado

#!/bin/bash

ffmpeg_pipeline_[SCRIPT_ID].sh

Gerado por: Manim Science Studio Squad - Agente A6

Tópico: [topic] | Script ID: [uuid]

Saída alvo: Reels 9:16, 1080x1920, H.264

set -e # para em caso de erro

INPUT_VIDEO="video_[ID].mp4"

INPUT_AUDIO="narration_[ID]final.aac"

INPUT_MUSIC="music_ambient.mp3"

INPUT_SUBS="narration[ID].vtt"

OUTPUT_FILE="final_reel_[ID].mp4"

==========================================

PASSO 1: Converter vídeo para 9:16 (Reels)

============================

==============

Manim renderiza em 16:9 por padrão; convertemos para 9:16

ffmpeg -i "$`INPUT_VIDEO"

-vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black"

-c:v libx264 -preset slow -crf 18

video_resized_[ID].mp4

==========================================

PASSO 2: Processar música de fundo

============================

==============

Reduz volume da música para -18dB (narração em foreground)

ffmpeg -i "`$INPUT_MUSIC"

-af "volume=-18dB,afade=t=out:st=70:d=3"

-t 90

music_processed_[ID].aac

==========================================

PASSO 3: Mix de áudio (narração + música)

==========================================

ffmpeg -i "$`INPUT_AUDIO" -i music_processed_[ID].aac

-filter_complex "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout]"

-map "[aout]" -ar 44100 -b:a 256k

audio_mixed_[ID].aac

==========================================

PASSO 4: Sincronizar vídeo + áudio misto

==========================================

ffmpeg -i video_resized_[ID].mp4 -i audio_mixed_[ID].aac

-c:v copy -c:a aac -b:a 256k -shortest

video_with_audio_[ID].mp4

==========================================

PASSO 5: Adicionar legendas queimadas (burnt-in)

==========================================

Fontes: Fira Sans Bold, branca com shadow para legibilidade

ffmpeg -i video_with_audio_[ID].mp4

-vf "subtitles=`$INPUT_SUBS:force_style='FontName=Fira Sans,FontSize=18,PrimaryColour=&HFFFFFF,Outli

neColour=&H000000,Outline=2,Shadow=1,Alignment=2,MarginV=80'"

-c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p

video_with_subs_[ID].mp4

==========================================

PASSO 6: Color grading e normalização

==========================================

Brightness leve (+0.05) + contraste (+1.1) para telas OLED

Normalização de loudness EBU R128 para plataformas (-14 LUFS)

ffmpeg -i video_with_subs_[ID].mp4

-vf "eq=brightness=0.05:contrast=1.1:saturation=1.05"

-af "loudnorm=I=-14:TP=-1.5:LRA=11"

-c:v libx264 -preset slow -crf 17

-c:a aac -b:a 256k

-movflags +faststart

"$`OUTPUT_FILE"

==========================================

PASSO 7: Limpeza de arquivos temporários

==========================================

rm -f video_resized_[ID].mp4 music_processed_[ID].aac

audio_mixed_[ID].aac video_with_audio_[ID].mp4

video_with_subs_[ID].mp4

echo "✅ Reel finalizado: `$OUTPUT_FILE"

echo "📊 Metadados:"

ffprobe -v quiet -print_format json -show_format -show_streams "$OUTPUT_FILE"

5.6.3 Especificações de Output por Plataforma

Agente A7 — Estrategista de Calendário Editorial

Identificador: editorial-calendar-strategist

Responsabilidade primária: Alocar cada vídeo produzido no calendário editorial otimizando para engajamento de audiência, diversidade temática, sazonalidade acadêmica e oportunidades de trending científico.

5.7.1 Entradas

Metadados do vídeo produzido (tópico, complexidade, duração)

Calendário editorial existente (JSON com slots ocupados)

publishing_cadence: 1x/semana / 3x/semana (default) / diário

target_platforms: lista de plataformas alvo

audience_timezone: America/Sao_Paulo (default)

5.7.2 Algoritmo de Alocação

Fatores considerados (peso relativo):

Janelas de publicação prioritárias (horário de Brasília):

5.7.3 Saída: Slot de Calendário

{

"calendar_entry": {

"entry_id": "CAL-2025-W23-03",

"script_id": "[uuid]",

"topic": "Princípio da Incerteza de Heisenberg",

"scheduled_datetime": "2025-06-04T18:30:00-03:00",

"platforms": ["instagram_reels", "youtube_shorts"],

"hashtags_suggested": [

"#FísicaQuântica", "#Heisenberg", "#CiênciaBrasileira",

"#Física", "#Educação", "#MecânicaQuântica"

],

"caption_suggested": "O universo tem um limite de precisão — e isso muda tudo que você pensa sobre a realidade. 🔬⚡

O Princípio da Incerteza de Heisenberg em 60 segundos.

#FísicaQuântica #Ciência",

"thumbnail_notes": "Frame do momento da equação ΔxΔp (t≈45s) com texto overlay 'Impossível saber tudo'",

"seo_title": "Princípio da Incerteza de Heisenberg explicado em 60 segundos",

"strategic_notes": "Publicar semana antes do vestibular FUVEST — alta busca por física

quântica",

"next_topic_suggestion": "Dualidade onda-partícula (complementa narrativa de QM)"

}

}

5.7.4 Relatório Mensal de Calendário

O A7 também produz um relatório mensal consolidado com:

Distribuição temática: pizza de tópicos publicados/planejados

Cobertura de complexidade: % iniciante / intermediário / avançado

Gap analysis: tópicos de alta demanda ainda não cobertos

Previsão de engajamento: baseada em padrões históricos do canal

Sugestões de tópicos: top 5 tópicos recomendados para próximo mês

6. Estrutura do Pacote de Entrega

6.1 Pacote ZIP por Vídeo

reel_[SCRIPT_ID][topic_slug]/

│

├── 📄 README.md # Sumário do pacote, instruções de uso

├── 📋 metadata.json # Metadados completos do vídeo

│

├── 01_script/

│ ├── script[ID].json # Script estruturado (A1)

│ └── script_[ID]readable.md # Versão legível para humanos

│

├── 02_storyboard/

│ └── storyboard[ID].md # Storyboard completo (A2)

│

├── 03_manim/

│ ├── manim_scene_[ID].py # Código Manim (A3)

│ ├── render_commands.sh # Comandos de renderização

│ └── assets/ # Imagens/SVG usados nas cenas

│

├── 04_narration/

│ ├── narration_[ID].ssml # SSML com prosódia (A4)

│ ├── narration_[ID]final.aac # Áudio gerado

│ ├── narration[ID].vtt # Legendas WebVTT

│ └── sync_[ID].json # Metadados de sincronização

│

├── 05_review/

│ └── epistemic_review_[ID].md # Relatório de revisão (A5)

│

├── 06_ffmpeg/

│ └── ffmpeg_pipeline_[ID].sh # Script de montagem (A6)

│

└── 07_calendar/

└── calendar_entry_[ID].json # Slot e metadados editoriais (A7)

7. Modelo de Dados

7.1 Entidade Central: ProductionJob

interface ProductionJob {

job_id: string; // UUID v4

created_at: ISO8601;

updated_at: ISO8601;

status: JobStatus; // enum abaixo

// Input

briefing: {

topic: string;

complexity_level: 'iniciante' | 'intermediário' | 'avançado';

target_duration_sec: number;

tone?: string;

forbidden_terms?: string[];

};

// Agentes

agents: {

A1_scriptwriter: AgentResult;

A2_storyboard: AgentResult;

A3_manim: AgentResult;

A4_narration: AgentResult;

A5_review: AgentResult;

A6_ffmpeg: AgentResult;

A7_calendar: AgentResult;

};

// Output

package_path: string; // caminho do ZIP final

review_cycles: number; // quantas vezes passou pelo A5

human_review_required: boolean;

}

type JobStatus =

| 'briefing_received'

| 'scripting'

| 'storyboarding'

| 'coding_and_narration'

| 'under_review'

| 'rework_required'

| 'approved'

| 'editing'

| 'scheduling'

| 'package_ready'

| 'failed'

| 'human_escalation';

interface AgentResult {

agent_id: string;

started_at: ISO8601;

completed_at: ISO8601;

status: 'pending' | 'running' | 'completed' | 'failed';

output_path: string;

error?: string;

metrics: Record<string, number>;

}

8. Requisitos Técnicos

8.1 Dependências de Runtime

[runtime.python]

version = ">=3.11"

[dependencies]

manim = ">=0.18.0"

edge-tts = ">=6.1.0"

ffmpeg-python = ">=0.2.0"

pydantic = ">=2.0"

jinja2 = ">=3.1" # templates de SSML e scripts

openai = ">=1.0" # LLM backbone dos agentes

httpx = ">=0.24" # requests assíncronos

[system.binaries]

ffmpeg = ">=6.0"

manim = "*" # via pip, não system

8.2 Variáveis de Ambiente

LLM

OPENAI_API_KEY=sk-...

LLM_MODEL=gpt-4o # backbone dos agentes A1, A2, A5, A7

LLM_CODE_MODEL=gpt-4o # backbone do A3 (código)

TTS

EDGE_TTS_VOICE_MASC=pt-BR-AntonioNeural

EDGE_TTS_VOICE_FEM=pt-BR-FranciscaNeural

Storage

OUTPUT_BASE_PATH=/media/productions

TEMP_PATH=/tmp/manim-studio

Manim

MANIM_QUALITY=medium_quality # dev: low_quality

MANIM_PREVIEW=false # não abrir janela em CI/CD

8.3 Recursos Computacionais Recomendados

9. Segurança e Compliance

9.1 Controles de Segurança

Sandboxing de código Manim: execução em

container Docker isolado sem acesso à rede

Validação de input: todos os campos de briefing validados via Pydantic com limites de tamanho

Rate limiting: máximo 10 jobs/hora por operador para evitar abuso de LLM

Auditoria: todos os jobs logados com job_id, user_id e timestamps imutáveis

9.2 Propriedade Intelectual

Equações e derivações matemáticas: domínio público por natureza

Conteúdo gerado pelo squad: pertence integralmente ao operador/canal

Músicas de fundo: somente tracks royalty-free com licença Creative Commons 0 ou equivalente

Fontes tipográficas: somente fontes com licença OFL (Fira Math, Fira Sans)

9.3 Precisão e Responsabilidade Editorial

O Relatório de Revisão Epistêmica (A5) é necessário mas não suficiente: o operador humano é o responsável editorial final

Vídeos com veredicto ⚠️ APROVADO COM

RESSALVAS devem ter as ressalvas lidas pelo operador antes da publicação

O squad não publica autonomamente: o upload é sempre uma ação humana deliberada

10. Roadmap

v1.0 — MVP (Meses 1–3)

�Pipeline sequencial completo (A1 → A7)

�Pacote ZIP estruturado

�Suporte a tópicos de física e matemática

�TTS PT-BR com SSML básico

�Storyboard em Markdown

v1.5 — Consolidação (Meses 4–6)

�Interface web para briefing (formulário + preview de script)

�Biblioteca de templates Manim reutilizáveis (A3)

�Integração com Google Calendar / Notion para A7

�Dashboard de métricas de produção

�Suporte a filosofia da ciência como domínio do A5

v2.0 — Escala (Meses 7–12)

�Upload automático para Instagram e YouTube Shorts via API

�Suporte a inglês (EN-US) e espanhol (ES-MX)

�Geração automática de thumbnail com IA

�A/B testing de hooks (dois scripts por tópico)

�Fine-tuning do modelo de narração para voz customizada do canal

�Modo colaborativo (múltiplos operadores com permissões)

11. Glossário

Documento mantido pelo time de Produto do Manim Science Studio Squad. Última revisão: Junho 2026.
