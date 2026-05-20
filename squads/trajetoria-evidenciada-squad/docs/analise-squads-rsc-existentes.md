# Análise do que já existia sobre RSC/TAE

## Artefatos localizados

1. `rsc-tae-ai-studio-squad`
   - Foco: PRD/sistema RSC para Google AI Studio + Tool Gateway.
   - Agentes: Product Owner RSC, critérios normativos, gateway, LGPD e QA.
   - Entregas: contratos de ferramentas, matriz de critérios e relatório de prontidão.
   - Limitação: arquitetura de produto/sistema, não montagem completa do processo individual do servidor.

2. Materiais em `Material herme`
   - Guias, transcrições, modelos, memoriais e consolidados sobre RSC-TAE/PCCTAE.
   - Limitação: referências documentais, não cadeia multiagente operacional de ingestão, separação, pontuação, memorial e auditoria.

3. Skill `normative-document-analysis-termux`
   - Tem padrão para memorial RSC em primeira pessoa com evidências e cuidado contra invenção de fatos.
   - Limitação: workflow de redação/análise, não squad empacotado para organizar o processo inteiro.

## Lacunas frente ao áudio

O pedido exige: coleta de dados do servidor com perguntas quando faltarem informações; indicação da pasta de documentos; preservação dos originais; separação de PDFs compostos; classificação por tipo documental; extração de número, data, assunto e emissor; leitura da planilha de pontuação; enquadramento vantajoso sem reutilizar documento; pasta de revisão manual; montagem do processo final; memorial humanizado em primeira pessoa; auditoria e ciclo de correção com o usuário.

## Decisão de design

Foi criado o `Trajetória Evidenciada Squad`, focado na execução prática do processo individual: documentos → evidências → pontuação → memorial → dossiê protocolável → auditoria.
