# Rodada ativa

Charter-ID: `CHR-WP02-004`  
Estado: `READY`  
Preparado em: 2026-07-17  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Unidade: `WP-02E — confiança live, proveniência e fechamento consistente`

## Autoridade

O contrato funcional detalhado está em `faleious-ai/gitlab-runner_ynh/continuity/ACTIVE_ROUND.md`. Este coordenador mantém missão, estado transversal, revisão, síntese e handoff; não replica implementação do Runner.

## Revisão anterior

`RND-20260716-010` / `CHR-WP02-003` recebeu `CORRECTION_REQUIRED` em `continuity/reviews/REV-RND-20260716-010.md`.

Findings:

- P1-F01: transporte da chave oficial rejeita o redirect atual antes do GPG;
- P1-F02: evidência histórica foi promovida sem nova observação;
- P2-F03: continuidade final contém referências pré-publicação;
- P2-F04: default `alpine:latest` diverge do install versionado.

## Autorização

`Leia AGENTS.md e continue` autoriza o charter detalhado no Runner. Atribua novo `Round-ID`. Cada Task-ID concluído gera commit apenas nos repositórios afetados. O coordenador recebe commit na tarefa final de continuidade e em qualquer tarefa que altere decisão/estado cross-repo.

Baseline: resolver `origin/master` nos dois repositórios e confirmar a presença da revisão `RND-20260717-011`, do process backprop Runner `4cefe926732c95344c3d7d129aa9dbe110dcae72` e deste charter.

## Tarefas do Runner

1. `T-WP02E-01-official-key-transport`;
2. `T-WP02E-02-live-trust-observation`;
3. `T-WP02E-03-historical-evidence-repair`;
4. `T-WP02E-04-docker-default-consistency`;
5. `T-WP02E-05-remote-ci-observation`;
6. `T-WP02E-06-integration-gates`;
7. `T-WP02E-07-final-continuity`.

O Runner define seams, RED/GREEN, provenance, paths, dependências e rollback.

## Invariantes

- preservar controller, segurança de token, lifecycle local e fail-closed já aceitos;
- não promover manifest;
- não usar/testar credencial histórica;
- nenhum wildcard genérico para origem da chave;
- novo fato live exige novo artefato ligado ao commit produtor;
- um commit remoto por tarefa, sem branch/PR/worktree/squash/force push;
- CI e lifecycle permanecem no nível efetivamente observado.

## Gate humano

`HG-RUN-SEC-01` permanece `UNRESOLVED_NO_AUTHORITY`, não bloqueante. Nenhuma nova decisão humana é necessária.

## Definition of Done

Sete tarefas concluídas ou bloqueadas validamente, findings resolvidos, manifest `18.6.2~ynh1`, evidência live/provenance honesta e pacote cross-repo em `EXECUTED_AWAITING_REVIEW` sem o Executor declarar aceite.
