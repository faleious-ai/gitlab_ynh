# Especificação do programa

Status: `BASELINE_ACCEPTED`  
Issue coordenadora: `faleious-ai/gitlab_ynh#1`

## Problema

Os pacotes YunoHost precisam acompanhar releases com segurança, enquanto o conector GitLab disponível cobre apenas uma fração da API. O programa deve resolver atualização, análise upstream, paridade funcional e continuidade por agentes sem transformar “latest” em instalação não reproduzível.

## Objetivos

1. manter GitLab e Runner atualizáveis por automação revisável;
2. garantir artefatos fixados e caminhos válidos de upgrade;
3. criar espelhos upstream para análise e continuidade;
4. construir MCP version-aware com cobertura ampla REST/GraphQL;
5. medir cobertura e lacunas por operação;
6. proteger segredos, privilégios e operações destrutivas;
7. permitir continuidade entre agentes a partir do repositório.

## Não objetivos

- alterar o produto GitLab upstream;
- prometer 100% de endpoints como tools de alto nível;
- executar administração destrutiva irrestrita;
- baixar versões não fixadas em runtime;
- manter forks upstream divergentes como fonte autoritativa;
- criar burocracia de PR/branch contrária à política master-only.

## Resultados esperados

### Pacotes

- descoberta de release determinística;
- resolução completa de assets;
- hashes verificados;
- upgrade path obrigatório;
- testes de lifecycle e arquitetura;
- falha fechada em inconsistência.

### MCP

- catálogo de capacidades consultável;
- tools de alto nível para fluxos frequentes;
- mecanismo residual controlado para longa cauda da API;
- autenticação e autorização explícitas;
- paginação, uploads/downloads e operações assíncronas;
- audit trail com `trace_id`;
- contract tests contra instância isolada;
- relatório de cobertura por versão e edição.

### Continuidade

- entrada mínima por `AGENTS.md`;
- estado e handoff atuais;
- rationale em ADRs;
- evidências indexadas;
- um commit por rodada em `master`;
- retomada sem dependência de chat.

## Métricas de sucesso

- 100% dos assets declarados possuem URL e SHA256 verificáveis.
- 100% dos caminhos de upgrade gerados respeitam stops conhecidos para origem/destino.
- 100% das operações MCP expostas possuem schema, escopo, risco e teste.
- cobertura da API é calculada por domínio, não declarada informalmente.
- nenhuma operação destrutiva roda fora de namespace efêmero nos testes.
- cada rodada fecha com status, handoff, evidência e commit.

## Restrições

- YunoHost suportado pelo pacote;
- arquiteturas declaradas em cada manifest;
- diferenças CE/EE e recursos licenciados;
- limites e versões da API GitLab;
- acesso a criação de repos/mirrors pode depender de ambiente externo;
- master deve permanecer executável após cada commit.

## Definition of Done do programa

O programa só está concluído quando:

1. os dois pacotes possuem updater seguro e testes;
2. mirrors são sincronizados e auditáveis;
3. MCP possui catálogo, ondas implementadas e coverage report;
4. segurança e assurance estão demonstradas;
5. documentação operacional e release existem;
6. uma nova IA consegue executar manutenção recorrente pelo protocolo MAESTRO.