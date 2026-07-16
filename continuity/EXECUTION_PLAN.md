# Plano de execução

Este arquivo define ordem, dependências e fechamento. A decomposição detalhada está em `docs/specifications/WORK_BREAKDOWN.md`.

## Política de execução

- Executar a maior unidade coerente possível até um bloqueio real.
- Não iniciar uma unidade dependente antes de demonstrar os critérios de saída da anterior.
- Um commit por rodada de IA e por repositório afetado.
- Trabalho cruzado usa o mesmo `Round-ID` nos commits de cada repositório.
- Decisões técnicas reversíveis pertencem ao agente; gates humanos seguem `ADR-0004`.

## Sequência canônica

### WP-00 — Bootstrap MAESTRO

Status: `DONE`

Saída: infraestrutura de contexto, memória, decisão, evidência, handoff e persistência.

### WP-01 — Auditoria baseline

Status: `NEXT`

Dependências: WP-00.

Subunidades:

- `WP-01A`: inventário completo de `gitlab_ynh`;
- `WP-01B`: inventário completo de `gitlab-runner_ynh` no repositório próprio;
- `WP-01C`: divergência contra upstream YunoHost;
- `WP-01D`: mapa de riscos, lacunas de teste e pontos dependentes de versão.

Saída obrigatória:

- baseline verificável dos dois pacotes;
- matriz de fontes e versões;
- fluxo de lifecycle;
- divergências classificadas;
- backlog técnico derivado com critérios de aceite.

### WP-02 — Autoupdate do Runner

Status: `PLANNED`

Dependências: WP-01.

Objetivo: descobrir uma versão estável elegível e atualizar runner + helper images como conjunto atômico, com URLs, hashes e testes.

Saída: implementação, testes, política de falha e evidência de install/upgrade/registration/executor/removal.

### WP-03 — Autoupdate do GitLab

Status: `PLANNED`

Dependências: WP-01 e aprendizados de WP-02.

Objetivo: gerar atualização CE/EE por Debian e arquitetura, incorporando resolução de mandatory upgrade stops.

Saída: gerador reproduzível, resolver de caminho de upgrade, validação de fontes e testes de lifecycle.

### WP-04 — Espelhos upstream

Status: `PLANNED`

Dependências: credenciais e ambiente capaz de criar repositórios/mirrors.

Objetivo: espelhar `gitlab-org/gitlab` e `gitlab-org/gitlab-runner` no GitHub em modo somente leitura, com sincronização auditável.

### WP-05 — Repositório coordenador do MCP

Status: `PLANNED`

Dependências: capacidade de criar repositório.

Objetivo: criar `faleious-ai/gitlab-mcp` e mover para ele a autoridade de implementação do servidor MCP, mantendo neste repositório apenas coordenação do pacote e referências.

### WP-06 — Catálogo de API e paridade GitHub

Status: `PLANNED`

Dependências: WP-05 e schema/documentação da versão alvo.

Objetivo: catálogo machine-readable REST/GraphQL, matriz de permissões, edições, versões, risco e mapeamento MCP.

### WP-07 — Implementação MCP por ondas

Status: `PLANNED`

Ondas:

1. descoberta e leitura;
2. colaboração e work items;
3. repositório, commits e refs;
4. CI/CD, jobs, logs e artifacts;
5. releases, packages e registries;
6. grupos, administração e operações privilegiadas permitidas.

Cada onda fecha apenas com contract tests e relatório de cobertura.

### WP-08 — Assurance e operação

Status: `PLANNED`

Objetivo: testes negativos, paginação, idempotência, rate limit, retries, falha parcial, redaction, auditoria, destructive sandbox e compatibilidade por versão/edição.

### WP-09 — Release e manutenção contínua

Status: `PLANNED`

Objetivo: cadência de atualização, indicadores de drift, rollback, changelog, compatibilidade e handoff operacional.

## Regra de promoção

Uma unidade só muda para `DONE` quando:

1. todos os critérios de aceite estão demonstrados;
2. evidências estão indexadas;
3. riscos residuais estão declarados;
4. documentos canônicos refletem o estado real;
5. o commit da rodada foi persistido em `master`.