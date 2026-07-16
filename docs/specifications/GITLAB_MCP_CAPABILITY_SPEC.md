# Especificação de capacidades do GitLab MCP

Status: `PLANNED`  
Future authority: `faleious-ai/gitlab-mcp`

## Objetivo

Entregar ao agente uma superfície GitLab ampla, previsível e auditável, inspirada na ergonomia do conector GitHub, mas derivada das capacidades reais da API GitLab da instância, versão, edição, licença e credenciais em uso.

## Princípio de cobertura

A cobertura não é número de tools. É a proporção de operações relevantes da API que possuem caminho MCP utilizável, schema, permissão, comportamento de paginação, risco e teste.

## Camadas

1. transporte HTTP/GraphQL;
2. autenticação e descoberta da instância;
3. cliente version-aware;
4. catálogo de operações;
5. normalização de recursos e erros;
6. policy engine e allowlists;
7. tools de alto nível;
8. residual API controlada;
9. auditoria, telemetria e redaction;
10. contract tests e coverage report.

## Registro obrigatório por operação

Cada operação do catálogo deve possuir:

- identificador estável;
- domínio e recurso;
- REST method/path ou GraphQL field;
- versão mínima/máxima conhecida;
- CE/EE/licença;
- escopo/token mínimo;
- parâmetros e schema de resposta;
- paginação;
- upload/download/streaming;
- sincronismo ou job assíncrono;
- mutabilidade;
- idempotência;
- risk class;
- allowlist aplicável;
- tool/workflow correspondente;
- testes e estado de implementação.

## Domínios mínimos

- instância, metadata e capabilities;
- usuários, grupos, namespaces e membros;
- projetos e settings;
- arquivos, trees, blobs, commits, refs, branches e tags;
- issues, work items, epics, labels, milestones e notes;
- merge requests, approvals, discussions e reviews;
- pipelines, jobs, traces, artifacts, schedules, variables e runners;
- releases, packages, dependency/container registries;
- environments, deployments, feature flags e pages;
- wikis, snippets, search e imports/exports;
- hooks, integrations, keys, tokens e protected resources;
- audit events e administração permitida.

## Tipos de tool

### Tools de workflow

Operações comuns e semanticamente fortes, como criar issue, atualizar arquivo com SHA esperado, obter trace de job, revisar MR e executar pipeline.

### Tools de recurso

CRUD/control para recursos específicos, com nomes e schemas estáveis.

### Descoberta

`capabilities.list`, `operation.describe`, `instance.version` e matriz de disponibilidade.

### Residual API

Longa cauda controlada para operação catalogada ainda sem tool dedicada. Deve aceitar somente operação conhecida no catálogo, aplicar schema/policy e impedir URL arbitrária.

## Classes de risco

- `R0_READ`: leitura sem segredo adicional.
- `R1_REVERSIBLE_WRITE`: escrita facilmente reversível.
- `R2_PRIVILEGED_WRITE`: altera configuração, acesso ou execução.
- `R3_DESTRUCTIVE`: exclusão, revogação, rotação, perda ou impacto amplo.

R2 exige autorização explícita e allowlist. R3 exige gate humano contextual e, em testes, namespace efêmero.

## Contrato de erro

Erros normalizados devem preservar:

- categoria;
- status HTTP/GraphQL;
- operação;
- recurso;
- retryability;
- rate-limit metadata;
- trace_id;
- mensagem redigida;
- causa upstream quando segura.

Nunca retornar token, header secreto ou corpo sensível.

## Paginação e volume

Toda listagem deve expor cursor/page token e limite. Downloads grandes, traces e artifacts devem usar referência de arquivo/stream, não conteúdo ilimitado no contexto do modelo.

## Paridade com GitHub

Comparar capacidades por fluxo, não nomes. Cada lacuna recebe uma classe:

- implementável;
- limitada pela API;
- limitada por edição/licença;
- limitada por segurança;
- deliberadamente fora de escopo.

## Assurance mínima

- schema golden tests;
- contract tests por domínio;
- autenticação ausente/inválida;
- paginação completa;
- rate limits e retry-after;
- idempotência e optimistic concurrency;
- falha parcial e batch;
- redaction;
- version/edition availability;
- destructive sandbox;
- comparação catálogo -> API -> tool -> teste.

## Critério de aceite por onda

Uma onda só fecha quando todas as operações declaradas como implementadas possuem teste, documentação, política de risco e evidência; lacunas restantes precisam estar classificadas.