# Plano de execução

Este arquivo define a sequência de longo prazo. A autorização concreta de execução pertence exclusivamente a `continuity/ACTIVE_ROUND.md`.

## Política de execução

- O ChatGPT, como orquestrador/revisor, prepara cada rodada completa após resolver com o usuário todas as perguntas humanas necessárias.
- O Codex executa o charter `READY` até concluir todas as tarefas não bloqueadas.
- Não iniciar trabalho apenas porque aparece como `NEXT` neste arquivo; é necessário charter ativo.
- Executar a maior unidade coerente possível até conclusão ou bloqueio real.
- Planejar paralelismo por DAG; subagentes trabalham em outputs independentes e o Codex integra.
- Não iniciar unidade dependente antes de demonstrar critérios da anterior.
- Um commit normativo por rodada futura e por repositório afetado; trabalho cross-repo usa o mesmo `Round-ID`.
- Decisões técnicas reversíveis pertencem ao mandato; gates humanos seguem ADR-0004/ADR-0005.
- O executor termina como `EXECUTED_AWAITING_REVIEW`; promoção para `DONE` depende de revisão.

## Sequência canônica

### WP-00 — Bootstrap MAESTRO

Status: `DONE`.

### WP-00B — Contrato orquestrador-executor

Status: `DONE`.

Saída: papéis humano/ChatGPT/Codex, charter ativo, revisão independente, resolução de bloqueios e política de subagentes.

### WP-01 — Auditoria baseline

Status: `ACTIVE_CHARTER_READY`.

Charter: `CHR-WP01-001` em `continuity/ACTIVE_ROUND.md`.

Dependências: WP-00 e WP-00B.

Subunidades:

- `WP-01A`: inventário completo de `gitlab_ynh`;
- `WP-01B`: inventário completo de `gitlab-runner_ynh` no repositório próprio;
- `WP-01C`: divergência contra upstream YunoHost;
- `WP-01D`: riscos, lacunas de teste e pontos dependentes de versão.

Saída: baseline verificável, matrizes, lifecycle, divergências e backlog técnico com critérios.

### WP-02 — Autoupdate do Runner

Status: `PLANNED`; depende de WP-01 aceito.

Objetivo: descobrir versão estável elegível e atualizar runner + helper images como conjunto atômico, com URLs, hashes e testes.

### WP-03 — Autoupdate do GitLab

Status: `PLANNED`; depende de WP-01 e aprendizados aceitos de WP-02.

Objetivo: gerar atualização CE/EE por Debian e arquitetura, incorporando mandatory upgrade stops.

### WP-04 — Espelhos upstream

Status: `PLANNED`; depende de credenciais/ambiente para criar repositórios e mirrors.

### WP-05 — Repositório coordenador do MCP

Status: `PLANNED`; depende de capacidade de criar `faleious-ai/gitlab-mcp`.

### WP-06 — Catálogo de API e paridade GitHub

Status: `PLANNED`; depende de WP-05 e schemas/documentação da versão alvo.

### WP-07 — Implementação MCP por ondas

Status: `PLANNED`.

Ondas: descoberta/leitura; colaboração; repositório/commits/refs; CI/CD/artifacts; releases/packages/registries; administração permitida. Cada onda fecha com contract tests e cobertura.

### WP-08 — Assurance e operação

Status: `PLANNED`.

Abrange testes negativos, paginação, idempotência, rate limit, retries, falha parcial, redaction, auditoria e sandbox destrutivo.

### WP-09 — Release e manutenção contínua

Status: `PLANNED`.

## Regra de promoção

Uma unidade só muda para `DONE` quando todos os critérios estão demonstrados, evidências indexadas, riscos residuais declarados, documentos canônicos reconciliados, commits persistidos e revisão do orquestrador registra `ACCEPTED`.
