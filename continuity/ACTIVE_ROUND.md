# Rodada ativa

Charter-ID: `CHR-WP02-003`  
Estado: `READY`  
Preparado em: 2026-07-16  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Unidade: `WP-02 Correção final do Runner — action, trust e lifecycle`

## Autoridade

O contrato funcional detalhado e as skills de execução estão em `faleious-ai/gitlab-runner_ynh`:

- `continuity/ACTIVE_ROUND.md`;
- `.agents/skills/README.md`;
- ADR-0006 e protocolos locais.

Este coordenador mantém missão, decisão, estado transversal, evidência sintética e handoff. Não replique implementação do Runner aqui.

## Autorização

`Leia AGENTS.md e continue` autoriza o charter detalhado no Runner. Atribua novo `Round-ID`. Cada Task-ID concluído gera commit apenas nos repositórios realmente afetados. Um commit do coordenador é exigido quando a tarefa alterar estado, decisão, evidência ou síntese cross-repo.

Baseline: resolver `origin/master` nos dois repositórios e confirmar que contêm `RND-20260716-009`, ADR-0006 e o charter migrado.

## Tarefas funcionais do Runner

1. `T-WP02D-01-config-controller` — controlador `run__register()` e entradas efêmeras;
2. `T-WP02D-02-remove-legacy-register` — remover credencial/entry point legado;
3. `T-WP02D-03-lifecycle-identity` — backup/restore sem re-registro;
4. `T-WP02D-04-signature-fail-closed` — assinatura/chave falham fechado;
5. `T-WP02D-05-source-self-link-redirects` — origem canônica e redirects;
6. `T-WP02D-06-evidence-portability` — evidência canônica e portátil;
7. `T-WP02D-07-remote-ci` — CI remoto ou bloqueio objetivo;
8. `T-WP02D-08-integration-continuity` — integração, continuidade e síntese cross-repo.

O Runner contém seams, RED/GREEN, paths, dependências e gates completos de cada tarefa.

## Processo obrigatório

- TDD para toda mudança comportamental;
- backprop técnico automático;
- challenge pré-build nas tarefas de alto impacto;
- revisão pré-commit em Spec/Charter e Engineering/Security/Lifecycle;
- um commit remoto por tarefa e repositório afetado;
- sem squash, branch, PR, worktree ou force push;
- claims separados por evidência estrutural, local, CI e lifecycle;
- convergência por claims/gates/findings, não por confiança ou diff isolado.

## Fora de escopo

- promoção de versão;
- registro real ou uso da credencial histórica;
- operação destrutiva;
- instalação do runtime/hooks Cavekit;
- implementação MCP nesta unidade.

## Gate humano

`HG-RUN-SEC-01` permanece `UNRESOLVED_NO_AUTHORITY` e não bloqueia trabalho técnico.

## Definition of Done

Oito tarefas concluídas ou bloqueadas validamente, commits remotos rastreáveis, manifest sem promoção, evidência honesta e T08 publicada também neste coordenador com síntese, status, handoff e round record do mesmo Round-ID.
