# Padrões de Codificação para Pearson Specter Nova Legal Squad

Estes padrões definem convenções para scripts, prompts e estruturas usadas no squad jurídico. Segui-los garante consistência, legibilidade e aderência às melhores práticas em desenvolvimento de sistemas legais.

## Convenções de nomenclatura

* Use nomes de arquivos e funções em inglês. Para arquivos utilize hyphen-case (`exemplo-nome`) e para funções utilize camelCase (`exemploNome`).
* IDs de agentes e tarefas devem ser únicos e descritivos (ex.: `harvey`, `deepResearch`).
* Campos de dados declarados nos contratos (`campo`) devem refletir claramente seu conteúdo, por exemplo `judgeProfile`, `financialAssessment`.

## Organização de código

* Separe scripts e módulos por domínio: intake, pesquisa, auditoria, macro estratégia, estratégia final e compilação de relatórios.
* Evite hard-coding de caminhos ou credenciais. Utilize variáveis de ambiente ou arquivos de configuração seguros.
* Comentários devem explicar o *porquê* das decisões jurídicas e os fundamentos doutrinários relevantes, não apenas descrever o código.

## Logging e erros

* Capture exceções com contexto (caso, agente, entrada) para facilitar depuração.
* Use níveis de log (`INFO`, `WARNING`, `ERROR`) e registre acesso a bases de dados legais, respeitando privacidade e compliance.

## Segurança e privacidade

* Dados sensíveis, como nomes de partes e detalhes financeiros, devem ser mascarados quando armazenados ou transmitidos.
* Respeite LGPD/GDPR e normas de sigilo profissional ao lidar com documentos e e-mails.

## Documentação

* Cada módulo deve incluir um `README.md` descrevendo sua função, entradas, saídas e dependências.
* Este documento deve ser atualizado sempre que houver alterações na arquitetura ou novos requisitos de compliance.